"""Exercise the public, fictional-only FixProof MCP endpoint end to end."""

import asyncio
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from mcp import Client


def evidence_sha256(evidence: dict) -> str:
    canonical = json.dumps(
        evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


async def call(client: Client, name: str, arguments: dict) -> dict:
    result = await client.call_tool(name, arguments)
    if result.is_error:
        raise RuntimeError(f"{name} failed: {result.content}")
    return result.structured_content


async def main() -> None:
    url = os.environ.get("FIXPROOF_HOSTED_MCP_URL", "http://127.0.0.1:8790/mcp")
    async with Client(url, raise_exceptions=True) as client:
        protocol_version = client.protocol_version
        server_version = client.server_info.version
        server_instructions = client.instructions or ""
        for path in (
            "drying", "food-remnant", "detergent-residue", "removable-streak",
            "wash-noise", "cutlery-rust", "irreversible-glass-clouding",
            "unpleasant-interior-odour", "door-related-starting", "water-left-inside-after-programme",
        ):
            assert path in server_instructions
        listed = await client.list_tools()
        names = [tool.name for tool in listed.tools]
        assert names == ["start_case", "read_case", "ask_fixproof", "record_outcome", "prepare_handover"]
        assert all(tool.annotations.open_world_hint is False for tool in listed.tools)
        handover_tool = next(tool for tool in listed.tools if tool.name == "prepare_handover")
        assert handover_tool.meta == {"ui": {"resourceUri": "ui://fixproof/handover.html"}}
        listed_resources = await client.list_resources()
        assert len(listed_resources.resources) == 1
        app_resource = listed_resources.resources[0]
        assert str(app_resource.uri) == "ui://fixproof/handover.html"
        assert app_resource.mime_type == "text/html;profile=mcp-app"
        app_result = await client.read_resource(str(app_resource.uri))
        assert len(app_result.contents) == 1
        app_content = app_result.contents[0]
        assert app_content.mime_type == "text/html;profile=mcp-app"
        assert "FixProof repair handover" in app_content.text
        assert "window.addEventListener(\"message\"" in app_content.text
        assert "<script src=" not in app_content.text
        assert "<link " not in app_content.text
        assert "innerHTML" not in app_content.text
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
        integrity = handover["evidence_integrity"]
        assert integrity["algorithm"] == "sha256"
        assert integrity["canonicalization"] == "fixproof-sorted-json-v1"
        assert integrity["digest"] == evidence_sha256(handover["evidence"])
        assert integrity["authorship_proof"] is False
        assert integrity["digest"] in handover["markdown"]
        changed_evidence = dict(handover["evidence"])
        changed_evidence["reported_issue"] = "Changed after handover."
        assert integrity["digest"] != evidence_sha256(changed_evidence)
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
        rust_started = await call(reconnected, "start_case", {
            "request_id": str(uuid.uuid4()),
            "reported_issue": "Rust spots appear on the cutlery after the fictional wash.",
            "model": "Bosch SMS6HCI02A/72",
            "model_confirmed": True,
            "fictional_demo": True,
        })
        rust_assessed = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": rust_started["case_id"],
            "revision": rust_started["revision"], "user_message": "What should I check first?",
        })
        rust_pending = rust_assessed["pending_check"]
        assert rust_pending["step_id"].startswith("rust_")
        assert rust_pending["citations"]
        assert all(item["page"] == 46 for item in rust_pending["citations"])
        clouding_started = await call(reconnected, "start_case", {
            "request_id": str(uuid.uuid4()),
            "reported_issue": "Clouding on the fictional glassware does not wipe off.",
            "model": "Bosch SMS6HCI02A/72",
            "model_confirmed": True,
            "fictional_demo": True,
        })
        clouding_assessed = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": clouding_started["case_id"],
            "revision": clouding_started["revision"], "user_message": "What should I check first?",
        })
        clouding_pending = clouding_assessed["pending_check"]
        assert clouding_pending["step_id"].startswith("clouding_")
        assert clouding_pending["citations"]
        assert all(item["page"] == 46 for item in clouding_pending["citations"])
        odour_started = await call(reconnected, "start_case", {
            "request_id": str(uuid.uuid4()),
            "reported_issue": "There is an unpleasant odour inside the fictional dishwasher.",
            "model": "Bosch SMS6HCI01A/38",
            "model_confirmed": True,
            "fictional_demo": True,
        })
        odour_assessed = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": odour_started["case_id"],
            "revision": odour_started["revision"], "user_message": "What should I check first?",
        })
        odour_pending = odour_assessed["pending_check"]
        assert odour_pending["step_id"] == "odour_wipe_interior"
        assert [item["page"] for item in odour_pending["citations"]] == [38]
        starting_started = await call(reconnected, "start_case", {
            "request_id": str(uuid.uuid4()),
            "reported_issue": "The fictional dishwasher will not start because the door will not close securely.",
            "model": "Bosch SMS6HCI02A/72",
            "model_confirmed": True,
            "fictional_demo": True,
        })
        starting_assessed = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": starting_started["case_id"],
            "revision": starting_started["revision"], "user_message": "What should I check first?",
        })
        starting_pending = starting_assessed["pending_check"]
        assert starting_pending["step_id"] == "starting_close_door"
        assert [item["page"] for item in starting_pending["citations"]] == [48]
        water_pages = {}
        for model, pages in (
            ("Bosch SMS6HAI02A/01", [46]),
            ("Bosch SMS6HCI01A/38", [50]),
            ("Bosch SMS6HCI02A/72", [48]),
        ):
            water_started = await call(reconnected, "start_case", {
                "request_id": str(uuid.uuid4()),
                "reported_issue": "Water remains inside this fictional dishwasher after the programme ended.",
                "model": model, "model_confirmed": True, "fictional_demo": True,
            })
            water_assessed = await call(reconnected, "ask_fixproof", {
                "request_id": str(uuid.uuid4()), "case_id": water_started["case_id"],
                "revision": water_started["revision"], "user_message": "What should I check first?",
            })
            water_pending = water_assessed["pending_check"]
            assert water_pending["step_id"] == "water_cycle"
            assert [item["page"] for item in water_pending["citations"]] == pages
            water_pages[model] = [item["url"] for item in water_pending["citations"]]
        error_issue = "This fictional dishwasher displays error code E:61-03 after the wash."
        error_started = await call(reconnected, "start_case", {
            "request_id": str(uuid.uuid4()), "reported_issue": error_issue,
            "model": "Bosch SMS6HCI02A/72", "model_confirmed": True, "fictional_demo": True,
        })
        error_assessed = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": error_started["case_id"],
            "revision": error_started["revision"], "user_message": "What should I check first?",
        })
        assert error_assessed["status"] == "Handover ready"
        assert error_assessed["pending_check"] is None
        assert error_assessed["latest_event"]["kind"] == "scope"
        error_handover = await call(reconnected, "prepare_handover", {"case_id": error_started["case_id"]})
        assert error_handover["evidence"]["scope_report"] == error_issue
        assert "No check was selected" in error_handover["markdown"]
        assert error_handover["evidence"]["checks"] == []
        assert error_handover["evidence_integrity"]["digest"] == evidence_sha256(error_handover["evidence"])
        drying_started = await call(reconnected, "start_case", {
            "request_id": str(uuid.uuid4()),
            "reported_issue": "The fictional glasses remain wet after the wash.",
            "model": "Bosch SMS6HCI02A/72", "model_confirmed": True, "fictional_demo": True,
        })
        drying_assessed = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": drying_started["case_id"],
            "revision": drying_started["revision"], "user_message": "What should I check first?",
        })
        assert drying_assessed["pending_check"]["step_id"] == "programme"
        error_report = "Actually this fictional appliance shows E:24 and will not drain."
        scoped = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": drying_started["case_id"],
            "revision": drying_assessed["revision"], "user_message": error_report,
        })
        assert scoped["status"] == "Handover ready" and scoped["pending_check"] is None
        scoped_handover = await call(reconnected, "prepare_handover", {"case_id": drying_started["case_id"]})
        assert scoped_handover["evidence"]["scope_report"] == error_report

        electrolux_checks = {}
        for issue, path, expected_step, expected_pages in (
            ("The fictional plates remain wet after washing.", "drying", "rinse_aid", [20]),
            ("Food remnants remain on the fictional plates.", "food", "food_spacing", [15]),
            ("Detergent remains in the fictional dispenser.", "detergent", "electrolux_dispenser_lid", [21]),
            ("Removable streaks remain on fictional glasses.", "streaks", "streaks_rinse_setting", [20]),
            ("There is an unpleasant odour inside the fictional dishwasher.", "odour", "electrolux_clean_interior", [16, 18]),
            ("The fictional dishwasher will not start because its door will not close.", "starting", "starting_close_door", [18]),
        ):
            opened = await call(reconnected, "start_case", {
                "request_id": str(uuid.uuid4()), "reported_issue": issue,
                "model": "Electrolux ESF8735ROX", "model_confirmed": True, "fictional_demo": True,
            })
            answered = await call(reconnected, "ask_fixproof", {
                "request_id": str(uuid.uuid4()), "case_id": opened["case_id"],
                "revision": opened["revision"], "user_message": "What should I check first?",
            })
            check = answered["pending_check"]
            assert check["step_id"] == expected_step
            assert [citation["page"] for citation in check["citations"]] == expected_pages
            assert all("resource.electrolux.com.au" in citation["url"] for citation in check["citations"])
            electrolux_checks[path] = [citation["url"] for citation in check["citations"]]
        unsupported_model_path = await call(reconnected, "start_case", {
            "request_id": str(uuid.uuid4()),
            "reported_issue": "The fictional cutlery has rust spots after a wash.",
            "model": "Electrolux ESF8735ROX", "model_confirmed": True, "fictional_demo": True,
        })
        unsupported_model_path_answer = await call(reconnected, "ask_fixproof", {
            "request_id": str(uuid.uuid4()), "case_id": unsupported_model_path["case_id"],
            "revision": unsupported_model_path["revision"], "user_message": "What should I check first?",
        })
        assert unsupported_model_path_answer["pending_check"] is None
        assert unsupported_model_path_answer["latest_event"]["kind"] == "scope"

    evidence = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": url,
        "protocol_version": protocol_version,
        "server_version": server_version,
        "server_instructions": server_instructions,
        "evidence_fingerprint": integrity["digest"],
        "evidence_fingerprint_verified_by_client": True,
        "changed_evidence_detected": True,
        "authorship_proof_claimed": False,
        "tools": names,
        "mcp_app": {
            "tool": handover_tool.name,
            "resource_uri": str(app_resource.uri),
            "mime_type": app_resource.mime_type,
            "self_contained": True,
            "safe_dom_rendering": True,
        },
        "exact_models": 4,
        "source_backed_paths": 10,
        "electrolux_citations_by_path": electrolux_checks,
        "electrolux_unmapped_path_rejected_without_check": True,
        "case_id": started["case_id"],
        "selected_step": pending["step_id"],
        "selected_citations": [item["url"] for item in pending["citations"]],
        "noise_path_selected_step": noise_pending["step_id"],
        "noise_path_citations": [item["url"] for item in noise_pending["citations"]],
        "rust_path_selected_step": rust_pending["step_id"],
        "rust_path_citations": [item["url"] for item in rust_pending["citations"]],
        "clouding_path_selected_step": clouding_pending["step_id"],
        "clouding_path_citations": [item["url"] for item in clouding_pending["citations"]],
        "odour_path_selected_step": odour_pending["step_id"],
        "odour_path_citations": [item["url"] for item in odour_pending["citations"]],
        "starting_path_selected_step": starting_pending["step_id"],
        "starting_path_citations": [item["url"] for item in starting_pending["citations"]],
        "water_retention_citations_by_model": water_pages,
        "recorded_observation_preserved_after_reconnect": True,
        "next_check_not_repeated": True,
        "safety_stop_cleared_pending_check": True,
        "unsupported_error_code_rejected_without_check": True,
        "later_error_report_cleared_pending_check": True,
        "fictional_only": True,
    }
    output = Path(os.environ.get("FIXPROOF_HOSTED_MCP_EVIDENCE", "validation/HOSTED_MCP.json"))
    output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"HOSTED_MCP_OK protocol={protocol_version} tools={len(names)} step={pending['step_id']}")


if __name__ == "__main__":
    asyncio.run(main())
