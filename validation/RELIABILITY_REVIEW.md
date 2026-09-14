# FixProof reliability improvement — 14 September 2026

## Defensible claim

In the evaluated workflows, FixProof preserves the distinction between a suggestion, a deferred check and a user-reported performed check. The real MCP endpoint persists the evidence into a sourced handover and preserves a safety stop across a new client connection. Tested lexical hazard reports stop the local workflow without relying on the AI provider.

This is a prototype reliability claim, not a probability of winning, an appliance-safety certification, or evidence of customer impact.

## Changes

- HTTP and MCP now use the same functions to record outcomes and apply safety stops.
- Initial issues, follow-up messages and outcome observations can stop troubleshooting. Pending checks are cleared without inventing completion; the exact report is preserved in the handover.
- A stopped HTTP case cannot be reopened or labelled resolved through the status action.
- Informational and clarification replies retain the pending check. A request for the next step does not silently replace it.
- The public-interface source shows performed, deferred/skipped and pending evidence separately. A recorded check can be revisited when another check is not pending, retaining previous record history.
- Handover summaries explicitly state that deferred/skipped records do not establish performed work.

## Evidence collected

| Verification | Result | Scope |
| --- | --- | --- |
| Python HTTP/MCP regression suite | 17 tests passed | Real HTTP workflow tests and in-process MCP client tests; AI decisions are stubbed where specified |
| Public application-logic regression suite | 6 tests passed | Real application JavaScript with a small DOM double; not browser or usability QA |
| Local AI evaluation | 8/8 scenarios passed | Running local Qwen model; see LOCAL_AI_EVAL.json |
| Real Streamable HTTP MCP exercise | Passed | All five tools, source-backed selection via real local AI, explicit deferred outcome, handover, safety stop and read through another client connection; see RELIABILITY_MCP.json |
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

The lexical hazard preflight is conservative and incomplete. It can stop on negated or non-appliance uses of words such as smoke; the first transport fixture used the phrase "smoke test" and triggered this policy. The fixture now says "transport verification". This is a known false-positive limitation, not evidence that all hazards are detected. Unrecognised phrasing still depends on the model and may be missed. The policy is not a medical, legal or appliance-safety authority.

The new interface has logic-test coverage but no fresh browser/visual QA in this revision. Earlier browser evidence describes the previously published version and must not be attributed to this revision. There has been no independent user or repair-professional evaluation.

## Release evidence

- Commit `10947a144001ccf984010fbeea6a15f414a4cf30` was pushed to the public GitHub repository and the Sites source repository.
- The exact archive from that commit was saved as Site version 5 and production deployment `appgdep_6aa7a554527c8191ac32d36359af96a4` succeeded on 14 September 2026.
- The public page showed 23 automated checks and 8/8 local-AI scenarios after deployment.
- A resumed production case showed one user-reported performed check separately from three checks with no recorded outcome while retaining the persistent safety stop.
- Devpost's public and submitted project copy showed the new reliability claims and remained `SUBMITTED`, with 5/5 steps complete.

The strongest next evidence is an independent owner/professional assessment of the handover. Additional test counts alone cannot establish that it saves time or increases the chance of winning.
