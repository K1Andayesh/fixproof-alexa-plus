r"""FixProof MCP server using the official MCP Python SDK.

Run from the repository root:
    .venv\Scripts\python.exe fixproof\mcp_server.py

Clients connect to http://127.0.0.1:8771/mcp by default.
"""

from __future__ import annotations

import json
import os
import uuid
from typing import Any, Literal

from mcp.server import MCPServer

import server as workflow


HOST = os.environ.get("FIXPROOF_MCP_HOST", "127.0.0.1")
PORT = int(os.environ.get("FIXPROOF_MCP_PORT", "8771"))

mcp = MCPServer(
    "FixProof",
    version="0.2.0",
    website_url="https://fixproof-alexa.keyvan-andayesh.chatgpt.site",
    instructions=(
        "Carry an appliance issue through source-linked checks and a repair handover. "
        "Only user-confirmed outcomes count as attempted. Never claim a diagnosis, a "
        "physical inspection, or a verified repair. The current reference catalog covers "
        "Bosch SMS6HAI02A/01 drying guidance only."
    ),
)


def _request_id(value: str) -> str:
    return workflow.clean(value, 80)


def _cached(request_id: str) -> dict | None:
    with workflow.db() as connection:
        row = connection.execute(
            "SELECT body FROM requests WHERE id=?", (request_id,)
        ).fetchone()
    return json.loads(row["body"]) if row else None


def _save_new(case: dict, request_id: str) -> dict:
    body = json.dumps(case)
    with workflow.db() as connection:
        connection.execute("BEGIN IMMEDIATE")
        cached = connection.execute(
            "SELECT body FROM requests WHERE id=?", (request_id,)
        ).fetchone()
        if cached:
            return json.loads(cached["body"])
        connection.execute("INSERT INTO cases VALUES (?,?)", (case["id"], body))
        connection.execute(
            "INSERT INTO requests VALUES (?,?,?)", (request_id, case["id"], body)
        )
    return case


def _save_updated(case: dict, request_id: str, expected_revision: int) -> dict:
    case["revision"] = expected_revision + 1
    body = json.dumps(case)
    with workflow.db() as connection:
        connection.execute("BEGIN IMMEDIATE")
        cached = connection.execute(
            "SELECT body FROM requests WHERE id=?", (request_id,)
        ).fetchone()
        if cached:
            return json.loads(cached["body"])
        row = connection.execute(
            "SELECT body FROM cases WHERE id=?", (case["id"],)
        ).fetchone()
        if not row:
            raise ValueError("Case not found.")
        current = json.loads(row["body"])
        if current["revision"] != expected_revision:
            raise ValueError("This case changed. Read it again before continuing.")
        connection.execute(
            "UPDATE cases SET body=? WHERE id=?", (body, case["id"])
        )
        connection.execute(
            "INSERT INTO requests VALUES (?,?,?)", (request_id, case["id"], body)
        )
    return case


def _citations(pages: list[int]) -> list[dict[str, Any]]:
    """Return self-contained source references for an MCP guidance result."""
    source = workflow.SOURCE
    return [
        {
            "title": source["title"],
            "document": source["document"],
            "page": page,
            "url": f'{source["url"]}#page={page}',
            "source_verified": source["verified"],
            "content_sha256": source["sha256"],
        }
        for page in pages
    ]


def _case_view(case: dict) -> dict:
    pending = case.get("pending")
    latest = dict(case["events"][-1]) if case["events"] else None
    if latest and latest.get("pages"):
        latest["citations"] = _citations(latest["pages"])
    return {
        "case_id": case["id"],
        "revision": case["revision"],
        "status": case["status"],
        "model": case["model"],
        "model_confirmed": case["verified"],
        "fictional_demo": case["demo"],
        "reported_issue": case["issue"],
        "reference_match": {
            "supported": workflow.is_supported(case["model"]) and case["verified"],
            "catalog_model": workflow.MODEL,
            "user_confirmed_model": case["verified"],
            "document": workflow.SOURCE["document"],
            "source_verified": workflow.SOURCE["verified"],
        },
        "recorded_outcomes": case["attempts"],
        "safety_report": case.get("safety_report"),
        "evidence_summary": {
            "user_reports_performed": sum(a['outcome'] in workflow.PERFORMED for a in case['attempts'].values()),
            "deferred_or_skipped": sum(a['outcome'] not in workflow.PERFORMED for a in case['attempts'].values()),
        },
        "pending_check": (
            {
                "step_id": pending,
                **workflow.STEPS[pending],
                "citations": _citations(workflow.STEPS[pending]["pages"]),
            }
            if pending
            else None
        ),
        "latest_event": latest,
    }


def _handover_evidence(case: dict) -> dict[str, Any]:
    """Return the handover facts as a stable, machine-readable evidence bundle."""
    checks = []
    for step_id, attempt in case["attempts"].items():
        step = workflow.STEPS[step_id]
        checks.append(
            {
                "step_id": step_id,
                "title": step["title"],
                "evidence_status": (
                    "user_reports_performed"
                    if attempt["outcome"] in workflow.PERFORMED
                    else "deferred_or_skipped"
                ),
                "outcome": attempt["outcome"],
                "observation": attempt["note"],
                "recorded_at": attempt["at"],
                "citations": _citations(step["pages"]),
            }
        )
    pending = case.get("pending")
    return {
        "schema_version": "fixproof-handover-1",
        "case_id": case["id"],
        "case_status": case["status"],
        "reported_issue": case["issue"],
        "model": {
            "reported": case["model"],
            "user_confirmed": case["verified"],
            "fictional_demo": case["demo"],
            "catalog_match": workflow.is_supported(case["model"]),
        },
        "reference": {
            "title": workflow.SOURCE["title"],
            "document": workflow.SOURCE["document"],
            "url": workflow.SOURCE["url"],
            "source_verified": workflow.SOURCE["verified"],
            "content_sha256": workflow.SOURCE["sha256"],
        },
        "checks": checks,
        "suggested_awaiting_outcome": (
            {
                "step_id": pending,
                "title": workflow.STEPS[pending]["title"],
                "citations": _citations(workflow.STEPS[pending]["pages"]),
            }
            if pending
            else None
        ),
        "safety_report": case.get("safety_report"),
        "limits": [
            "No physical inspection was performed.",
            "No fault or repair requirement was diagnosed.",
            "Deferred or skipped checks do not establish performed work.",
        ],
    }


@mcp.tool(structured_output=True)
def start_case(
    request_id: str,
    reported_issue: str,
    model: str,
    model_confirmed: bool,
    fictional_demo: bool = False,
) -> dict[str, Any]:
    """Start a persisted case.

    Use a stable unique request_id so a retried tool call cannot create a duplicate.
    model_confirmed must only be true when the user read the exact model from the
    appliance label. Set fictional_demo for demonstration data.
    """
    workflow.init()
    request_id = _request_id(request_id)
    cached = _cached(request_id)
    if cached:
        return _case_view(cached)
    issue = workflow.clean(reported_issue)
    model = workflow.clean(model, 100)
    case = {
        "id": str(uuid.uuid4()),
        "created": workflow.now(),
        "model": model,
        "verified": model_confirmed is True,
        "demo": fictional_demo is True,
        "issue": issue,
        "status": "Open",
        "revision": 0,
        "events": [
            {"role": "user", "text": issue, "at": workflow.now()},
            {
                "role": "assistant",
                "kind": "intro",
                "text": (
                    "Case saved. Ask FixProof for a source-backed check. Only an "
                    "outcome the user explicitly records counts as attempted."
                ),
                "at": workflow.now(),
            },
        ],
        "attempts": {},
        "pending": None,
    }
    if workflow.hazard_report(issue):
        workflow.stop_for_safety(case, issue)
        case['events'].append(dict(role='assistant', at=workflow.now(), **workflow.safety_reply()))
    return _case_view(_save_new(case, request_id))


@mcp.tool(structured_output=True)
def read_case(case_id: str) -> dict[str, Any]:
    """Read current case state before taking a revision-sensitive action."""
    workflow.init()
    return _case_view(workflow.read_case(workflow.clean(case_id, 80)))


@mcp.tool(structured_output=True)
def ask_fixproof(
    request_id: str, case_id: str, revision: int, user_message: str
) -> dict[str, Any]:
    """Assess the user's message and propose one bounded source-backed next step.

    This may call the configured local Ollama model. The application, rather than
    the model, supplies instruction text and self-contained page citations. It never
    diagnoses a fault.
    """
    workflow.init()
    request_id = _request_id(request_id)
    cached = _cached(request_id)
    if cached:
        return _case_view(cached)
    case = workflow.read_case(workflow.clean(case_id, 80))
    if case["revision"] != revision:
        raise ValueError("This case changed. Read it again before continuing.")
    if case["status"] != "Open":
        raise ValueError("Reopen the case before requesting more checks.")
    message = workflow.clean(user_message)
    reply = workflow.assess(case, message)
    workflow.apply_reply(case, message, reply)
    return _case_view(_save_updated(case, request_id, revision))


@mcp.tool(structured_output=True)
def record_outcome(
    request_id: str,
    case_id: str,
    revision: int,
    step_id: str,
    outcome: Literal[
        "Still wet", "Improved, not resolved", "Not yet tested", "Skipped"
    ],
    observation: str = "",
) -> dict[str, Any]:
    """Record what the user says happened after the currently pending check."""
    workflow.init()
    request_id = _request_id(request_id)
    cached = _cached(request_id)
    if cached:
        return _case_view(cached)
    case = workflow.read_case(workflow.clean(case_id, 80))
    if case["revision"] != revision:
        raise ValueError("This case changed. Read it again before continuing.")
    workflow.record_evidence(case, step_id, outcome, observation)
    return _case_view(_save_updated(case, request_id, revision))


@mcp.tool(structured_output=True)
def prepare_handover(case_id: str) -> dict[str, Any]:
    """Return human-readable Markdown and a structured evidence handover."""
    workflow.init()
    case = workflow.read_case(workflow.clean(case_id, 80))
    return {
        "case_id": case["id"],
        "revision": case["revision"],
        "status": case["status"],
        "markdown": workflow.handover(case),
        "evidence": _handover_evidence(case),
    }


if __name__ == "__main__":
    workflow.init()
    mcp.run(
        transport="streamable-http",
        host=HOST,
        port=PORT,
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
    )
