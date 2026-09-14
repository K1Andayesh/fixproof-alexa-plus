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


def _case_view(case: dict) -> dict:
    pending = case.get("pending")
    return {
        "case_id": case["id"],
        "revision": case["revision"],
        "status": case["status"],
        "model": case["model"],
        "model_confirmed": case["verified"],
        "fictional_demo": case["demo"],
        "reported_issue": case["issue"],
        "recorded_outcomes": case["attempts"],
        "pending_check": (
            {"step_id": pending, **workflow.STEPS[pending]} if pending else None
        ),
        "latest_event": case["events"][-1] if case["events"] else None,
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
    the model, supplies instruction text and citations. It never diagnoses a fault.
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
    case["events"] += [
        {"role": "user", "text": message, "at": workflow.now()},
        {"role": "assistant", "at": workflow.now(), **reply},
    ]
    case["pending"] = reply.get("step")
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
    if case["status"] != "Open" or case.get("pending") != step_id:
        raise ValueError("That check is not currently awaiting an outcome.")
    note = observation.strip()
    if len(note) > 2000:
        raise ValueError("Observation is too long.")
    case["attempts"][step_id] = {
        "outcome": outcome,
        "note": note,
        "at": workflow.now(),
    }
    case["events"].append(
        {
            "role": "record",
            "text": note,
            "step": step_id,
            "outcome": outcome,
            "at": workflow.now(),
        }
    )
    case["pending"] = None
    return _case_view(_save_updated(case, request_id, revision))


@mcp.tool(structured_output=True)
def prepare_handover(case_id: str) -> dict[str, Any]:
    """Return an evidence-backed Markdown handover without claiming diagnosis."""
    workflow.init()
    case = workflow.read_case(workflow.clean(case_id, 80))
    return {
        "case_id": case["id"],
        "revision": case["revision"],
        "status": case["status"],
        "markdown": workflow.handover(case),
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
