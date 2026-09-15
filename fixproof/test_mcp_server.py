import tempfile
import unittest
import uuid
from unittest.mock import patch

from mcp import Client
from mcp.client import advertise
from mcp.server.apps import APP_MIME_TYPE, EXTENSION_ID

import mcp_server


class MCPWorkflowTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        mcp_server.workflow.DATA = mcp_server.workflow.Path(self.tmp.name)
        mcp_server.workflow.init()

    async def asyncTearDown(self):
        self.tmp.cleanup()

    async def call(self, client, name, arguments):
        result = await client.call_tool(name, arguments)
        self.assertFalse(result.is_error)
        return result.structured_content

    async def test_safety_stop_through_mcp_and_persisted_read(self):
        async with Client(mcp_server.mcp, raise_exceptions=True) as client:
            for entry in ['initial', 'message', 'observation']:
                with self.subTest(entry=entry):
                    c=await self.call(client,'start_case',dict(request_id=str(uuid.uuid4()),reported_issue='Smoke from the door.' if entry=='initial' else 'Plates are wet.',model=mcp_server.workflow.MODEL,model_confirmed=True,fictional_demo=True))
                    if entry!='initial':
                        reply=dict(kind='step',step='waiting',**mcp_server.workflow.STEPS['waiting'])
                        with patch.object(mcp_server.workflow,'assess',return_value=reply):
                            c=await self.call(client,'ask_fixproof',dict(request_id=str(uuid.uuid4()),case_id=c['case_id'],revision=c['revision'],user_message='Next?'))
                        with patch.object(mcp_server.workflow,'infer',side_effect=TimeoutError('Offline')):
                            if entry=='message':
                                c=await self.call(client,'ask_fixproof',dict(request_id=str(uuid.uuid4()),case_id=c['case_id'],revision=c['revision'],user_message='Smoke from the door.'))
                            else:
                                c=await self.call(client,'record_outcome',dict(request_id=str(uuid.uuid4()),case_id=c['case_id'],revision=c['revision'],step_id='waiting',outcome='Not yet tested',observation='Smoke from the door.'))
                    restored=await self.call(client,'read_case',dict(case_id=c['case_id']))
                    self.assertEqual(restored['status'],'Handover ready');self.assertIsNone(restored['pending_check'])
                    self.assertEqual(restored['safety_report'],'Smoke from the door.')
                    self.assertEqual(restored['evidence_summary']['user_reports_performed'],0)
                    handover=await self.call(client,'prepare_handover',dict(case_id=c['case_id']))
                    self.assertIn('## Safety report',handover['markdown'])
                    result=await client.call_tool('record_outcome',dict(request_id=str(uuid.uuid4()),case_id=c['case_id'],revision=c['revision'],step_id='waiting',outcome='Still wet'))
                    self.assertTrue(result.is_error)

    async def test_tools_expose_a_persistent_evidence_flow(self):
        async with Client(mcp_server.mcp, raise_exceptions=True) as client:
            tools = await client.list_tools()
            self.assertEqual(
                {tool.name for tool in tools.tools},
                {"start_case", "read_case", "ask_fixproof", "record_outcome", "prepare_handover"},
            )
            request_id = str(uuid.uuid4())
            started = await self.call(
                client,
                "start_case",
                {
                    "request_id": request_id,
                    "reported_issue": "Plates are wet.",
                    "model": mcp_server.workflow.MODEL,
                    "model_confirmed": True,
                    "fictional_demo": True,
                },
            )
            duplicate = await self.call(
                client,
                "start_case",
                {
                    "request_id": request_id,
                    "reported_issue": "A retry must not create another case.",
                    "model": mcp_server.workflow.MODEL,
                    "model_confirmed": True,
                    "fictional_demo": True,
                },
            )
            self.assertEqual(started["case_id"], duplicate["case_id"])

            reply = {"kind": "step", "step": "waiting", **mcp_server.workflow.STEPS["waiting"]}
            with patch.object(mcp_server.workflow, "assess", return_value=reply):
                assessed = await self.call(
                    client,
                    "ask_fixproof",
                    {
                        "request_id": str(uuid.uuid4()),
                        "case_id": started["case_id"],
                        "revision": started["revision"],
                        "user_message": "What should I check first?",
                    },
                )
            self.assertEqual(assessed["pending_check"]["step_id"], "waiting")
            citation = assessed["pending_check"]["citations"][0]
            self.assertEqual(citation["page"], 41)
            self.assertEqual(citation["document"], mcp_server.workflow.SOURCE["document"])
            self.assertEqual(citation["content_sha256"], mcp_server.workflow.SOURCE["sha256"])
            self.assertEqual(citation["url"], mcp_server.workflow.SOURCE["url"] + "#page=41")
            self.assertTrue(assessed["reference_match"]["supported"])

            recorded = await self.call(
                client,
                "record_outcome",
                {
                    "request_id": str(uuid.uuid4()),
                    "case_id": started["case_id"],
                    "revision": assessed["revision"],
                    "step_id": "waiting",
                    "outcome": "Still wet",
                    "observation": "Still wet after waiting.",
                },
            )
            self.assertEqual(recorded["recorded_outcomes"]["waiting"]["outcome"], "Still wet")

            restored = await self.call(client, "read_case", {"case_id": started["case_id"]})
            self.assertEqual(restored["revision"], recorded["revision"])
            handover = await self.call(client, "prepare_handover", {"case_id": started["case_id"]})
            self.assertIn("Still wet after waiting.", handover["markdown"])
            self.assertIn("not a diagnosis", handover["markdown"])

    async def test_informational_guidance_returns_page_citations(self):
        async with Client(mcp_server.mcp, raise_exceptions=True) as client:
            for model,page in ((mcp_server.workflow.MODEL,41),("Bosch SMS6HCI01A/38",44),("Bosch SMS6HCI02A/72",42)):
                started = await self.call(client, "start_case", {
                    "request_id": str(uuid.uuid4()), "reported_issue": "Only plastic is wet.",
                    "model": model, "model_confirmed": True, "fictional_demo": True,
                })
                info = {"kind": "info", **mcp_server.workflow.info_for(model)["plastic"]}
                with patch.object(mcp_server.workflow, "assess", return_value=info):
                    result = await self.call(client, "ask_fixproof", {
                        "request_id": str(uuid.uuid4()), "case_id": started["case_id"],
                        "revision": started["revision"], "user_message": "Is plastic different?",
                    })
                self.assertIsNone(result["pending_check"])
                self.assertEqual(result["latest_event"]["kind"], "info")
                source=mcp_server.workflow.source_for(model)
                self.assertEqual(result["latest_event"]["citations"][0]["url"],source["url"]+f"#page={page}")

    async def test_handover_returns_machine_readable_evidence_boundaries(self):
        async with Client(mcp_server.mcp, raise_exceptions=True) as client:
            started = await self.call(client, "start_case", {
                "request_id": str(uuid.uuid4()), "reported_issue": "Plates are wet.",
                "model": mcp_server.workflow.MODEL, "model_confirmed": True,
                "fictional_demo": True,
            })
            reply = {"kind": "step", "step": "waiting", **mcp_server.workflow.STEPS["waiting"]}
            with patch.object(mcp_server.workflow, "assess", return_value=reply):
                assessed = await self.call(client, "ask_fixproof", {
                    "request_id": str(uuid.uuid4()), "case_id": started["case_id"],
                    "revision": started["revision"], "user_message": "What is first?",
                })
            recorded = await self.call(client, "record_outcome", {
                "request_id": str(uuid.uuid4()), "case_id": started["case_id"],
                "revision": assessed["revision"], "step_id": "waiting",
                "outcome": "Not yet tested", "observation": "Will test after dinner.",
            })
            handover = await self.call(client, "prepare_handover", {
                "case_id": recorded["case_id"],
            })
            evidence = handover["evidence"]
            self.assertEqual(evidence["schema_version"], "fixproof-handover-1")
            self.assertEqual(evidence["checks"][0]["evidence_status"], "deferred_or_skipped")
            self.assertEqual(evidence["checks"][0]["observation"], "Will test after dinner.")
            self.assertEqual(evidence["checks"][0]["citations"][0]["page"], 41)
            self.assertEqual(evidence["reference"]["content_sha256"], mcp_server.workflow.SOURCE["sha256"])
            self.assertIn("No fault or repair requirement was diagnosed.", evidence["limits"])

    async def test_tools_publish_client_planning_annotations(self):
        app_support = advertise(EXTENSION_ID, {"mimeTypes": [APP_MIME_TYPE]})
        async with Client(
            mcp_server.mcp, raise_exceptions=True, extensions=[app_support]
        ) as client:
            listed = {tool.name: tool for tool in (await client.list_tools()).tools}
            for name in ("read_case", "prepare_handover"):
                self.assertTrue(listed[name].annotations.read_only_hint)
                self.assertTrue(listed[name].annotations.idempotent_hint)
                self.assertFalse(listed[name].annotations.open_world_hint)
            for name in ("start_case", "ask_fixproof", "record_outcome"):
                self.assertFalse(listed[name].annotations.read_only_hint)
                self.assertTrue(listed[name].annotations.idempotent_hint)
                self.assertFalse(listed[name].annotations.destructive_hint)
                self.assertFalse(listed[name].annotations.open_world_hint)
            self.assertEqual(
                listed["prepare_handover"].meta["ui"]["resourceUri"],
                mcp_server.HANDOVER_APP_URI,
            )
            self.assertIn(EXTENSION_ID, client.server_capabilities.extensions)
            resources = await client.list_resources()
            handover_resource = next(
                item for item in resources.resources
                if str(item.uri) == mcp_server.HANDOVER_APP_URI
            )
            self.assertEqual(handover_resource.mime_type, APP_MIME_TYPE)
            self.assertTrue(handover_resource.meta["ui"]["prefersBorder"])
            loaded = await client.read_resource(mcp_server.HANDOVER_APP_URI)
            self.assertEqual(loaded.contents[0].mime_type, APP_MIME_TYPE)
            self.assertIn("FixProof repair handover", loaded.contents[0].text)
            self.assertNotIn("innerHTML", loaded.contents[0].text)

    async def test_new_client_resumes_without_repeating_recorded_check(self):
        def deterministic_infer(prompt, context, schema):
            raw = {
                "model": "continuity-test",
                "prompt_eval_count": 1,
                "eval_count": 1,
            }
            if "Classify the dishwasher issue" in prompt:
                return {"category": "drying"}, raw
            available = context["available_checks"]
            self.assertNotIn("waiting", available)
            return {"step": "rinse_aid"}, raw

        async with Client(mcp_server.mcp, raise_exceptions=True) as first_client:
            started = await self.call(first_client, "start_case", {
                "request_id": str(uuid.uuid4()), "reported_issue": "Plates are wet.",
                "model": mcp_server.workflow.MODEL, "model_confirmed": True,
                "fictional_demo": True,
            })
            first_reply = {"kind": "step", "step": "waiting", **mcp_server.workflow.STEPS["waiting"]}
            with patch.object(mcp_server.workflow, "assess", return_value=first_reply):
                assessed = await self.call(first_client, "ask_fixproof", {
                    "request_id": str(uuid.uuid4()), "case_id": started["case_id"],
                    "revision": started["revision"], "user_message": "What should I check first?",
                })
            recorded = await self.call(first_client, "record_outcome", {
                "request_id": str(uuid.uuid4()), "case_id": started["case_id"],
                "revision": assessed["revision"], "step_id": "waiting",
                "outcome": "Still wet", "observation": "Waited 30 minutes; still wet.",
            })

        async with Client(mcp_server.mcp, raise_exceptions=True) as next_client:
            restored = await self.call(next_client, "read_case", {"case_id": started["case_id"]})
            self.assertEqual(restored["revision"], recorded["revision"])
            self.assertEqual(restored["recorded_outcomes"]["waiting"]["outcome"], "Still wet")
            with patch.object(mcp_server.workflow, "infer", side_effect=deterministic_infer):
                continued = await self.call(next_client, "ask_fixproof", {
                    "request_id": str(uuid.uuid4()), "case_id": started["case_id"],
                    "revision": restored["revision"], "user_message": "What should I check next?",
                })
            self.assertEqual(continued["pending_check"]["step_id"], "rinse_aid")
            self.assertNotEqual(continued["pending_check"]["step_id"], "waiting")
            handover = await self.call(next_client, "prepare_handover", {"case_id": started["case_id"]})
            self.assertIn("Waited 30 minutes; still wet.", handover["markdown"])
            self.assertEqual(handover["evidence"]["checks"][0]["step_id"], "waiting")


if __name__ == "__main__":
    unittest.main()
