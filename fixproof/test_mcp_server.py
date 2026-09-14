import tempfile
import unittest
import uuid
from unittest.mock import patch

from mcp import Client

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


if __name__ == "__main__":
    unittest.main()
