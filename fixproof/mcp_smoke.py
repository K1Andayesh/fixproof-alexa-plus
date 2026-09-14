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
        citations = pending.get("citations", [])
        assert citations and all(citation["url"].startswith("https://") for citation in citations)
        assert all(citation["content_sha256"] for citation in citations)
        recorded_result = await client.call_tool(
            "record_outcome",
            {
                "request_id": str(uuid.uuid4()),
                "case_id": case["case_id"],
                "revision": assessed["revision"],
                "step_id": pending["step_id"],
                "outcome": "Not yet tested",
                "observation": "Fictional MCP transport verification.",
            },
        )
        recorded = recorded_result.structured_content
        handover_result = await client.call_tool(
            "prepare_handover", {"case_id": case["case_id"]}
        )
        handover = handover_result.structured_content
        restored_result = await client.call_tool('read_case', {'case_id': case['case_id']})
        restored = restored_result.structured_content
        assert restored['evidence_summary'] == {'user_reports_performed': 0, 'deferred_or_skipped': 1}
        assert 'Fictional MCP transport verification.' in handover['markdown']
        evidence = handover['evidence']
        assert evidence['schema_version'] == 'fixproof-handover-1'
        assert evidence['checks'][0]['evidence_status'] == 'deferred_or_skipped'
        assert evidence['checks'][0]['citations'][0]['content_sha256']
        safety_result = await client.call_tool('ask_fixproof', {
            'request_id': str(uuid.uuid4()), 'case_id': case['case_id'],
            'revision': restored['revision'], 'user_message': 'There is smoke from the door.'
        })
        stopped = safety_result.structured_content
        assert stopped['status'] == 'Handover ready' and stopped['pending_check'] is None
        async with Client(url, raise_exceptions=True) as reconnected:
            reread = await reconnected.call_tool('read_case', {'case_id': case['case_id']})
            assert reread.structured_content['safety_report'] == 'There is smoke from the door.'
            safety_handover = await reconnected.call_tool('prepare_handover', {'case_id': case['case_id']})
            assert '## Safety report' in safety_handover.structured_content['markdown']
        print(
            json.dumps(
                {
                    "protocol_version": client.protocol_version,
                    "tools": [tool.name for tool in tools.tools],
                    "case_id": case["case_id"],
                    "selected_step": pending["step_id"],
                    "selected_step_citations": [citation["url"] for citation in citations],
                    "source_hash_in_tool_contract": all(bool(citation["content_sha256"]) for citation in citations),
                    "recorded_outcome": recorded["recorded_outcomes"][pending["step_id"]]["outcome"],
                    "handover_contains_observation": "Fictional MCP transport verification." in handover["markdown"],
                    "machine_readable_handover": evidence["schema_version"],
                    "handover_preserves_evidence_status": evidence["checks"][0]["evidence_status"],
                    "deferred_not_counted_as_performed": True,
                    "safety_stop_survives_client_reconnect": True,
                    "safety_report_in_handover": True,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
