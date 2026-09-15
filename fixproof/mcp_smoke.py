"""Connect to a running FixProof MCP endpoint and exercise one fictional case."""

import asyncio
import json
import os
import uuid
from datetime import datetime, timezone

from mcp import Client
from mcp.client import advertise
from mcp.server.apps import APP_MIME_TYPE, EXTENSION_ID


async def main() -> None:
    url = os.environ.get("FIXPROOF_MCP_URL", "http://127.0.0.1:8771/mcp")
    app_support = advertise(EXTENSION_ID, {"mimeTypes": [APP_MIME_TYPE]})
    async with Client(url, raise_exceptions=True, extensions=[app_support]) as client:
        tools = await client.list_tools()
        handover_tool = next(tool for tool in tools.tools if tool.name == "prepare_handover")
        app_uri = handover_tool.meta["ui"]["resourceUri"]
        assert app_uri == "ui://fixproof/handover.html"
        assert EXTENSION_ID in client.server_capabilities.extensions
        resources = await client.list_resources()
        app_resource = next(item for item in resources.resources if str(item.uri) == app_uri)
        assert app_resource.mime_type == APP_MIME_TYPE
        app_resource_ui = app_resource.meta["ui"]
        assert "csp" not in app_resource_ui and "permissions" not in app_resource_ui
        app_document = await client.read_resource(app_uri)
        app_html = app_document.contents[0].text
        assert app_document.contents[0].mime_type == APP_MIME_TYPE
        assert "FixProof repair handover" in app_html
        assert "innerHTML" not in app_html
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
        handover_text = "\n".join(
            getattr(item, "text", "") for item in handover_result.content
        )
        assert "Fictional MCP transport verification." in handover_text, repr(handover_result.content)
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
            streaks_case_result = await final_client.call_tool('start_case', {
                'request_id': str(uuid.uuid4()),
                'reported_issue': 'Removable streaks remain on glasses and cutlery after the wash.',
                'model': 'Bosch SMS6HAI02A/01',
                'model_confirmed': True,
                'fictional_demo': True,
            })
            streaks_case = streaks_case_result.structured_content
            streaks_assessed_result = await final_client.call_tool('ask_fixproof', {
                'request_id': str(uuid.uuid4()), 'case_id': streaks_case['case_id'],
                'revision': streaks_case['revision'], 'user_message': 'What should I check first?'
            })
            streaks_assessed = streaks_assessed_result.structured_content
            streaks_pending = streaks_assessed['pending_check']
            assert streaks_pending is not None and streaks_pending['step_id'].startswith('streaks_')
            streaks_citations = streaks_pending.get('citations', [])
            assert streaks_citations and all(citation['url'].startswith('https://') for citation in streaks_citations)
            second_model_result = await final_client.call_tool('start_case', {
                'request_id': str(uuid.uuid4()),
                'reported_issue': 'Detergent residue remains inside the appliance after the wash.',
                'model': 'Bosch SMS6HCI01A/38',
                'model_confirmed': True,
                'fictional_demo': True,
            })
            second_model_case = second_model_result.structured_content
            second_model_assessed_result = await final_client.call_tool('ask_fixproof', {
                'request_id': str(uuid.uuid4()), 'case_id': second_model_case['case_id'],
                'revision': second_model_case['revision'], 'user_message': 'What should I check first?'
            })
            second_model_assessed = second_model_assessed_result.structured_content
            second_model_pending = second_model_assessed['pending_check']
            assert second_model_pending is not None and second_model_pending['step_id'].startswith('detergent_')
            second_model_citations = second_model_pending.get('citations', [])
            assert second_model_citations
            assert all(citation['url'].startswith('https://media3.bsh-group.com/Documents/9001720311_B.pdf#page=') for citation in second_model_citations)
            assert any(citation['url'].endswith('#page=46') for citation in second_model_citations)
            assert all(citation['content_sha256'] == 'b2bb4608cd266752804e8c02b3e251bb31e6c32f95824e602614b13f83240fc9' for citation in second_model_citations)
            second_model_handover_result = await final_client.call_tool(
                'prepare_handover', {'case_id': second_model_case['case_id']}
            )
            second_model_evidence = second_model_handover_result.structured_content['evidence']
            assert second_model_evidence['model']['reported'] == 'Bosch SMS6HCI01A/38'
            assert second_model_evidence['reference']['service_url'] == 'https://www.bosch-home.com.au/en/productservice/SMS6HCI01A-38'
        judge_trace = [
            {
                'connection': 1,
                'operation': 'tools/list',
                'observed': {
                    'protocol_version': client.protocol_version,
                    'tools': [tool.name for tool in tools.tools],
                    'annotations_present': sorted(annotations),
                    'mcp_apps_extension': EXTENSION_ID in client.server_capabilities.extensions,
                    'handover_app_uri': app_uri,
                    'handover_app_mime_type': app_resource.mime_type,
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
                    "mcp_app": {
                        "extension": EXTENSION_ID,
                        "advertised": EXTENSION_ID in client.server_capabilities.extensions,
                        "tool": "prepare_handover",
                        "resource_uri": app_uri,
                        "mime_type": app_resource.mime_type,
                        "prefers_border": app_resource_ui["prefersBorder"],
                        "self_contained": "<script src=" not in app_html and "<link " not in app_html,
                        "external_resource_csp_declared": "csp" in app_resource_ui,
                        "device_permissions_declared": "permissions" in app_resource_ui,
                        "text_fallback_contains_observation": "Fictional MCP transport verification." in handover_text,
                    },
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
                    "source_backed_paths": 4,
                    "exact_models": 2,
                    "food_path_selected_step": food_pending['step_id'],
                    "food_path_citations": [citation['url'] for citation in food_citations],
                    "detergent_path_selected_step": detergent_pending['step_id'],
                    "detergent_path_citations": [citation['url'] for citation in detergent_citations],
                    "streaks_path_selected_step": streaks_pending['step_id'],
                    "streaks_path_citations": [citation['url'] for citation in streaks_citations],
                    "second_model": second_model_evidence['model']['reported'],
                    "second_model_selected_step": second_model_pending['step_id'],
                    "second_model_citations": [citation['url'] for citation in second_model_citations],
                    "second_model_service_url": second_model_evidence['reference']['service_url'],
                    "second_model_source_hash_verified": all(
                        citation['content_sha256'] == 'b2bb4608cd266752804e8c02b3e251bb31e6c32f95824e602614b13f83240fc9'
                        for citation in second_model_citations
                    ),
                    "judge_trace": judge_trace,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
