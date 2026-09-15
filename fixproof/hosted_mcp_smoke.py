"""Exercise the public, fictional-only FixProof MCP endpoint end to end."""

import asyncio
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from mcp import Client


async def call(client: Client, name: str, arguments: dict) -> dict:
    result = await client.call_tool(name, arguments)
    if result.is_error:
        raise RuntimeError(f"{name} failed: {result.content}")
    return result.structured_content


async def main() -> None:
    url = os.environ.get("FIXPROOF_HOSTED_MCP_URL", "http://127.0.0.1:8790/mcp")
    async with Client(url, raise_exceptions=True) as client:
        protocol_version = client.protocol_version
        listed = await client.list_tools()
        names = [tool.name for tool in listed.tools]
        assert names == ["start_case", "read_case", "ask_fixproof", "record_outcome", "prepare_handover"]
        assert all(tool.annotations.open_world_hint is False for tool in listed.tools)
        started = await call(client, "start_case", {
            "request_id": str(uuid.uuid4()),
            "reported_issue": "Removable streaks remain on glasses after the fictional wash.",
            "model": "Bosch SMS6HCI02A/72",
            "model_confirmed": True,
            "fictional_demo": True,
        })
        assessed = await call(client, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": started["case_id"],
            "revision": started["revision"], "user_message": "What should I check first?",
        })
        pending = assessed["pending_check"]
        assert pending["step_id"] == "streaks_rinse_setting"
        assert [item["page"] for item in pending["citations"]] == [45, 24]
        assert all("9002017246_A.pdf" in item["url"] for item in pending["citations"])
        recorded = await call(client, "record_outcome", {
            "request_id": str(uuid.uuid4()), "case_id": started["case_id"],
            "revision": assessed["revision"], "step_id": pending["step_id"],
            "outcome": "Issue unchanged", "observation": "Fictional hosted MCP verification.",
        })
        assert recorded["evidence_summary"] == {"user_reports_performed": 1, "deferred_or_skipped": 0}

    async with Client(url, raise_exceptions=True) as reconnected:
        restored = await call(reconnected, "read_case", {"case_id": started["case_id"]})
        assert restored["recorded_outcomes"]["streaks_rinse_setting"]["observation"] == "Fictional hosted MCP verification."
        handover = await call(reconnected, "prepare_handover", {"case_id": started["case_id"]})
        assert "Fictional hosted MCP verification." in handover["markdown"]
        assert handover["evidence"]["reference"]["service_url"].endswith("SMS6HCI02A-72")
        continued = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": started["case_id"],
            "revision": restored["revision"], "user_message": "What should I check next?",
        })
        assert continued["pending_check"]["step_id"] == "streaks_add_rinse_aid"
        stopped = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": started["case_id"],
            "revision": continued["revision"], "user_message": "There is smoke from the fictional appliance.",
        })
        assert stopped["status"] == "Handover ready"
        assert stopped["pending_check"] is None
        noise_started = await call(reconnected, "start_case", {
            "request_id": str(uuid.uuid4()),
            "reported_issue": "There is a knocking or rattling noise during the fictional wash.",
            "model": "Bosch SMS6HCI02A/72",
            "model_confirmed": True,
            "fictional_demo": True,
        })
        noise_assessed = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": noise_started["case_id"],
            "revision": noise_started["revision"], "user_message": "What should I check first?",
        })
        noise_pending = noise_assessed["pending_check"]
        assert noise_pending["step_id"].startswith("noise_")
        assert noise_pending["citations"]
        assert all(item["page"] in {49, 50} for item in noise_pending["citations"])
        assert all("9002017246_A.pdf" in item["url"] for item in noise_pending["citations"])

    evidence = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": url,
        "protocol_version": protocol_version,
        "tools": names,
        "exact_models": 3,
        "source_backed_paths": 5,
        "case_id": started["case_id"],
        "selected_step": pending["step_id"],
        "selected_citations": [item["url"] for item in pending["citations"]],
        "noise_path_selected_step": noise_pending["step_id"],
        "noise_path_citations": [item["url"] for item in noise_pending["citations"]],
        "recorded_observation_preserved_after_reconnect": True,
        "next_check_not_repeated": True,
        "safety_stop_cleared_pending_check": True,
        "fictional_only": True,
    }
    output = Path(os.environ.get("FIXPROOF_HOSTED_MCP_EVIDENCE", "validation/HOSTED_MCP.json"))
    output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"HOSTED_MCP_OK protocol={protocol_version} tools={len(names)} step={pending['step_id']}")


if __name__ == "__main__":
    asyncio.run(main())
