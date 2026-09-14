"""Connect to a running FixProof MCP endpoint and exercise one fictional case."""

import asyncio
import json
import os
import uuid

from mcp import Client


async def main() -> None:
    url = os.environ.get("FIXPROOF_MCP_URL", "http://127.0.0.1:8771/mcp")
    async with Client(url, raise_exceptions=True) as client:
        tools = await client.list_tools()
        result = await client.call_tool(
            "start_case",
            {
                "request_id": str(uuid.uuid4()),
                "reported_issue": "Plates and glasses are still wet after a wash.",
                "model": "Bosch SMS6HAI02A/01",
                "model_confirmed": True,
                "fictional_demo": True,
            },
        )
        case = result.structured_content
        assessed_result = await client.call_tool(
            "ask_fixproof",
            {
                "request_id": str(uuid.uuid4()),
                "case_id": case["case_id"],
                "revision": case["revision"],
                "user_message": "What should I check first?",
            },
        )
        assessed = assessed_result.structured_content
        pending = assessed["pending_check"]
        if pending is None:
            raise RuntimeError("The clear drying scenario did not produce a bounded check.")
        recorded_result = await client.call_tool(
            "record_outcome",
            {
                "request_id": str(uuid.uuid4()),
                "case_id": case["case_id"],
                "revision": assessed["revision"],
                "step_id": pending["step_id"],
                "outcome": "Not yet tested",
                "observation": "Fictional MCP transport smoke test.",
            },
        )
        recorded = recorded_result.structured_content
        handover_result = await client.call_tool(
            "prepare_handover", {"case_id": case["case_id"]}
        )
        handover = handover_result.structured_content
        print(
            json.dumps(
                {
                    "protocol_version": client.protocol_version,
                    "tools": [tool.name for tool in tools.tools],
                    "case_id": case["case_id"],
                    "selected_step": pending["step_id"],
                    "recorded_outcome": recorded["recorded_outcomes"][pending["step_id"]]["outcome"],
                    "handover_contains_observation": "Fictional MCP transport smoke test." in handover["markdown"],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
