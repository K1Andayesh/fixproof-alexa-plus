"""Connect to a running FixProof MCP endpoint and exercise one fictional case."""

import asyncio
import json
import os
import uuid
from datetime import datetime, timezone

from mcp import Client


async def main() -> None:
    url = os.environ.get("FIXPROOF_MCP_URL", "http://127.0.0.1:8771/mcp")
    async with Client(url, raise_exceptions=True) as client:
        tools = await client.list_tools()
        annotations = {
            tool.name: tool.annotations.model_dump(by_alias=True, exclude_none=True)
            for tool in tools.tools
        }
        assert annotations['read_case']['readOnlyHint'] is True
        assert annotations['prepare_handover']['readOnlyHint'] is True
        assert all(item['openWorldHint'] is False for item in annotations.values())
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
        async with Client(url, raise_exceptions=True) as reconnected:
            reread = await reconnected.call_tool('read_case', {'case_id': case['case_id']})
            carried = reread.structured_content
            assert carried['reported_issue'] == 'Plates and glasses are still wet after a wash.'
            assert carried['recorded_outcomes'][pending['step_id']]['outcome'] == 'Not yet tested'
            continued_result = await reconnected.call_tool('ask_fixproof', {
                'request_id': str(uuid.uuid4()), 'case_id': case['case_id'],
                'revision': carried['revision'], 'user_message': 'What should I check next?'
            })
            continued = continued_result.structured_content
            next_pending = continued['pending_check']
            assert next_pending is not None and next_pending['step_id'] != pending['step_id']
            safety_result = await reconnected.call_tool('ask_fixproof', {
                'request_id': str(uuid.uuid4()), 'case_id': case['case_id'],
                'revision': continued['revision'], 'user_message': 'There is smoke from the door.'
            })
            stopped = safety_result.structured_content
            assert stopped['status'] == 'Handover ready' and stopped['pending_check'] is None
        async with Client(url, raise_exceptions=True) as final_client:
            reread = await final_client.call_tool('read_case', {'case_id': case['case_id']})
            final_state = reread.structured_content
            assert final_state['safety_report'] == 'There is smoke from the door.'
            safety_handover = await final_client.call_tool('prepare_handover', {'case_id': case['case_id']})
            assert '## Safety report' in safety_handover.structured_content['markdown']
            food_case_result = await final_client.call_tool('start_case', {
                'request_id': str(uuid.uuid4()),
                'reported_issue': 'Food remnants remain on plates after the wash.',
                'model': 'Bosch SMS6HAI02A/01',
                'model_confirmed': True,
                'fictional_demo': True,
            })
            food_case = food_case_result.structured_content
            food_assessed_result = await final_client.call_tool('ask_fixproof', {
                'request_id': str(uuid.uuid4()), 'case_id': food_case['case_id'],
                'revision': food_case['revision'], 'user_message': 'What should I check first?'
            })
            food_assessed = food_assessed_result.structured_content
            food_pending = food_assessed['pending_check']
            assert food_pending is not None and food_pending['step_id'].startswith('food_')
            food_citations = food_pending.get('citations', [])
            assert food_citations and all(citation['url'].startswith('https://') for citation in food_citations)
            detergent_case_result = await final_client.call_tool('start_case', {
                'request_id': str(uuid.uuid4()),
                'reported_issue': 'Detergent residue remains inside the appliance after the wash.',
                'model': 'Bosch SMS6HAI02A/01',
                'model_confirmed': True,
                'fictional_demo': True,
            })
            detergent_case = detergent_case_result.structured_content
            detergent_assessed_result = await final_client.call_tool('ask_fixproof', {
                'request_id': str(uuid.uuid4()), 'case_id': detergent_case['case_id'],
                'revision': detergent_case['revision'], 'user_message': 'What should I check first?'
            })
            detergent_assessed = detergent_assessed_result.structured_content
            detergent_pending = detergent_assessed['pending_check']
            assert detergent_pending is not None and detergent_pending['step_id'].startswith('detergent_')
            detergent_citations = detergent_pending.get('citations', [])
            assert detergent_citations and all(citation['url'].endswith('#page=42') for citation in detergent_citations)
        judge_trace = [
            {
                'connection': 1,
                'operation': 'tools/list',
                'observed': {
                    'protocol_version': client.protocol_version,
                    'tools': [tool.name for tool in tools.tools],
                    'annotations_present': sorted(annotations),
                },
            },
            {
                'connection': 1,
                'operation': 'start_case',
                'request': {
                    'reported_issue': 'Plates and glasses are still wet after a wash.',
                    'model': 'Bosch SMS6HAI02A/01',
                    'model_confirmed': True,
                    'fictional_demo': True,
                },
                'observed': {
                    'case_id': case['case_id'],
                    'revision': case['revision'],
                    'status': case['status'],
                },
            },
            {
                'connection': 1,
                'operation': 'ask_fixproof',
                'request': {'user_message': 'What should I check first?'},
                'observed': {
                    'step_id': pending['step_id'],
                    'citations': [citation['url'] for citation in citations],
                    'source_hash_present': all(bool(citation['content_sha256']) for citation in citations),
                },
            },
            {
                'connection': 1,
                'operation': 'record_outcome + prepare_handover',
                'request': {
                    'outcome': 'Not yet tested',
                    'observation': 'Fictional MCP transport verification.',
                },
                'observed': {
                    'user_reports_performed': restored['evidence_summary']['user_reports_performed'],
                    'deferred_or_skipped': restored['evidence_summary']['deferred_or_skipped'],
                    'handover_schema': evidence['schema_version'],
                    'recorded_evidence_status': evidence['checks'][0]['evidence_status'],
                },
            },
            {
                'connection': 2,
                'operation': 'read_case + ask_fixproof',
                'request': {'user_message': 'What should I check next?'},
                'observed': {
                    'issue_preserved': carried['reported_issue'] == 'Plates and glasses are still wet after a wash.',
                    'outcome_preserved': carried['recorded_outcomes'][pending['step_id']]['outcome'],
                    'previous_step': pending['step_id'],
                    'next_step': next_pending['step_id'],
                    'previous_step_not_repeated': next_pending['step_id'] != pending['step_id'],
                },
            },
            {
                'connection': 2,
                'operation': 'ask_fixproof',
                'request': {'user_message': 'There is smoke from the door.'},
                'observed': {
                    'status': stopped['status'],
                    'pending_check': stopped['pending_check'],
                },
            },
            {
                'connection': 3,
                'operation': 'read_case + prepare_handover',
                'observed': {
                    'safety_report_preserved': final_state['safety_report'],
                    'handover_contains_safety_section': '## Safety report' in safety_handover.structured_content['markdown'],
                },
            },
        ]
        print(
            json.dumps(
                {
                    "captured_at": datetime.now(timezone.utc).isoformat(),
                    "capture_scope": "Fictional local transport verification; no household or customer data.",
                    "transport": "Streamable HTTP",
                    "protocol_version": client.protocol_version,
                    "tools": [tool.name for tool in tools.tools],
                    "tool_annotations": annotations,
                    "case_id": case["case_id"],
                    "selected_step": pending["step_id"],
                    "selected_step_citations": [citation["url"] for citation in citations],
                    "source_hash_in_tool_contract": all(bool(citation["content_sha256"]) for citation in citations),
                    "recorded_outcome": recorded["recorded_outcomes"][pending["step_id"]]["outcome"],
                    "handover_contains_observation": "Fictional MCP transport verification." in handover["markdown"],
                    "machine_readable_handover": evidence["schema_version"],
                    "handover_preserves_evidence_status": evidence["checks"][0]["evidence_status"],
                    "deferred_not_counted_as_performed": True,
                    "cross_connection_issue_preserved": True,
                    "cross_connection_outcome_preserved": True,
                    "recorded_check_not_repeated": next_pending['step_id'] != pending['step_id'],
                    "continued_step": next_pending['step_id'],
                    "safety_stop_survives_client_reconnect": True,
                    "safety_report_in_handover": True,
                    "source_backed_paths": 3,
                    "food_path_selected_step": food_pending['step_id'],
                    "food_path_citations": [citation['url'] for citation in food_citations],
                    "detergent_path_selected_step": detergent_pending['step_id'],
                    "detergent_path_citations": [citation['url'] for citation in detergent_citations],
                    "judge_trace": judge_trace,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
