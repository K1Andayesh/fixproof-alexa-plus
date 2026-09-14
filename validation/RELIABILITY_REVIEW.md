# FixProof reliability improvement — 14 September 2026

## Defensible claim

In the evaluated workflows, FixProof preserves the distinction between a suggestion, a deferred check and a user-reported performed check. The real MCP endpoint persists the evidence into a sourced handover, returns exact page URLs and a verified content hash with supported guidance, and preserves a safety stop across a new client connection. Tested lexical hazard reports stop the local workflow without relying on the AI provider.

This is a prototype reliability claim, not a probability of winning, an appliance-safety certification, or evidence of customer impact.

## Changes

- HTTP and MCP now use the same functions to record outcomes and apply safety stops.
- Initial issues, follow-up messages and outcome observations can stop troubleshooting. Pending checks are cleared without inventing completion; the exact report is preserved in the handover.
- A stopped HTTP case cannot be reopened or labelled resolved through the status action.
- Informational and clarification replies retain the pending check. A request for the next step does not silently replace it.
- The public-interface source shows performed, deferred/skipped and pending evidence separately. A recorded check can be revisited when another check is not pending, retaining previous record history.
- Handover summaries explicitly state that deferred/skipped records do not establish performed work.
- Supported MCP checks and informational guidance return self-contained citations containing document identity, exact page URL, source-verification date and content hash.

## Evidence collected

| Verification | Result | Scope |
| --- | --- | --- |
| Python HTTP/MCP regression suite | 19 tests passed | Real HTTP workflow tests and in-process MCP client tests; AI decisions are stubbed where specified |
| Public application-logic regression suite | 7 tests passed | Real application JavaScript with a small DOM double; not browser or usability QA |
| Local AI evaluation | 10/10 scenarios passed | Running local Qwen model, including explicit no-hazard and technical-phrase cases; see LOCAL_AI_EVAL.json |
| Real Streamable HTTP MCP exercise | Passed | All five tools, source-backed selection via real local AI, explicit deferred outcome, handover, safety stop and read through another client connection; see RELIABILITY_MCP.json |
| Chrome UI exercise | Passed | Explicit no-hazard and technical phrases continued to a supported check; a mixed report containing a leak stopped the workflow and cleared the pending outcome |
| JavaScript syntax and whitespace checks | Passed | Both interfaces |

Reproduce:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s fixproof -p "test*.py" -v
node --test validation/test_public_workflow.cjs
python fixproof/evaluate.py
# With the local MCP server running:
.\.venv\Scripts\python.exe fixproof/mcp_smoke.py
```

## Limitations and release state

The lexical hazard preflight is conservative and incomplete. It now excludes tested explicit no-hazard statements such as "no smoke" and technical phrases such as "smoke test", while still stopping when another hazard remains in the same report. This narrow context handling does not establish full language understanding. Unrecognised phrasing still depends on the model and may be missed. The policy is not a medical, legal or appliance-safety authority.

The revised interface was exercised and visually inspected in Chrome from the local release build. This is developer QA, not an independent user or repair-professional evaluation.

## Release evidence

- Commit `1bd1ff49d34dfbeb8168eca26b2ec842fbe01eb4` was pushed to the public GitHub repository and the Sites source repository.
- The exact archive from that commit was saved as Site version 7 and production deployment `appgdep_6aa80667cfd88191a4eb0bfe5b345a65` succeeded on 14 September 2026.
- The production page showed 26 automated checks and 10/10 local-AI scenarios after deployment.
- In production Chrome QA, the evidence card described the structured citation contract. A fictional case returned the supported step "Allow drying to finish" with the clickable exact-page citation `Manual · p. 41`, linking to the verified manual at page 41.
- Devpost remained publicly accessible and the competition submission remained `SUBMITTED`, with 5/5 steps complete.

The strongest next evidence is an independent owner/professional assessment of the handover. Additional test counts alone cannot establish that it saves time or increases the chance of winning.
