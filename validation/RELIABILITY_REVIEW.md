# FixProof reliability improvement — 14 September 2026

## Defensible claim

In the evaluated workflows, FixProof preserves the distinction between a suggestion, a deferred check and a user-reported performed check. Across three source-backed issue paths, the real MCP endpoint persists the evidence into both readable Markdown and a versioned structured handover, returns exact page URLs and a verified content hash with supported guidance, and preserves a safety stop across a new client connection. Tested lexical hazard reports stop the local workflow without relying on the AI provider.

This is a prototype reliability claim, not a probability of winning, an appliance-safety certification, or evidence of customer impact.

## Changes

- HTTP and MCP now use the same functions to record outcomes and apply safety stops.
- Initial issues, follow-up messages and outcome observations can stop troubleshooting. Pending checks are cleared without inventing completion; the exact report is preserved in the handover.
- A stopped HTTP case cannot be reopened or labelled resolved through the status action.
- Informational and clarification replies retain the pending check. A request for the next step does not silently replace it.
- The public-interface source shows performed, deferred/skipped and pending evidence separately. A recorded check can be revisited when another check is not pending, retaining previous record history.
- Handover summaries explicitly state that deferred/skipped records do not establish performed work.
- Supported MCP checks and informational guidance return self-contained citations containing document identity, exact page URL, source-verification date and content hash.
- MCP handovers expose the evidence boundary directly in a versioned object: every recorded check carries its performed or deferred status, observation and citations alongside the readable Markdown.
- Every MCP tool declares client-planning annotations for read-only access, retry-safe idempotency, non-destructive writes and closed-world operation.
- A new MCP client can resume the case, retain the issue and explicit outcome, and obtain a different remaining check without repeating the recorded one.
- A second, separately bounded food-remnant path adds four checks grounded in manual pages 36, 37 and 42. Cross-path questions do not replace an awaiting check or mix the two evidence sequences.
- A third detergent-residue path adds two checks grounded in the manual's page-42 dispenser guidance and remains isolated from the other evidence sequences.
- A public impact card now connects official Australian repair and e-waste context to the demonstrated handover mechanism, while naming the product outcomes that remain unmeasured. The sources and claim boundary are recorded in `IMPACT_EVIDENCE.md`.

## Evidence collected

| Verification | Result | Scope |
| --- | --- | --- |
| Python HTTP/MCP regression suite | 25 tests passed | Real HTTP workflow tests and in-process MCP client tests; AI decisions are stubbed where specified |
| Public application-logic regression suite | 10 tests passed | Real application JavaScript with a small DOM double; not browser or usability QA |
| Local AI evaluation | 12/12 scenarios passed | Running local Qwen model, including explicit no-hazard and technical-phrase cases; see LOCAL_AI_EVAL.json |
| Real Streamable HTTP MCP exercise | Passed | All five tools, source-backed selection via real local AI for drying, food-remnant and detergent-residue cases, explicit deferred outcome, cross-connection evidence continuity, non-repetition of the recorded check, handover and a safety stop preserved through another connection; see RELIABILITY_MCP.json |
| Chrome UI exercise | Passed | Production detergent-residue path selected a page-42 check, recorded the path-neutral `Issue unchanged` outcome, and produced a readable handover with the observation and citation; no console warnings or errors |
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

The revised interface was exercised and visually inspected in Chrome from the production Site version 15. This is developer QA, not an independent user or repair-professional evaluation.

## Release evidence

- Product commit `9098de6d5ec122366222cc6329412a61813e981e` was pushed to the public GitHub repository and the Sites source repository.
- The exact archive from that commit was saved as Site version 14 and production deployment `appgdep_6aa8bf21cc308191b4ac8defd3d72439` succeeded on 15 September 2026.
- Impact-evidence commit `ba138c4638bcfb5102955278fe8068dc6c91d7a8` was pushed to the public GitHub repository and the Sites source repository.
- The exact archive from that commit was saved as Site version 15 and production deployment `appgdep_6aa8ccc2bedc81918ed2762d17b57ef5` succeeded on 15 September 2026.
- The real HTTP MCP exercise returned all five tool-annotation objects alongside `fixproof-handover-1`, preserved the issue and deferred outcome through a new client connection, selected a different remaining drying check, included exact-page citations and the source hash, preserved a later safety stop through another connection, and selected `food_spacing` and `detergent_tray` with page-42 citations for two additional cases.
- The production page showed three source-backed paths, 35 automated checks and 12/12 local-AI scenarios. Its implementation card described the Markdown plus structured-evidence handover contract, client-planning hints, cross-connection continuity and three-path MCP evidence.
- Production Chrome QA exercised the detergent-residue path from selection through page-42 guidance, the `Issue unchanged` outcome and a readable handover carrying the detergent-path label, observation and source. The browser console reported no warnings or errors.
- Site-version-15 Chrome QA verified the impact card at a 1920 × 911 desktop viewport and a 390 × 844 phone viewport. Its three-part argument stacked correctly on mobile, produced no horizontal overflow, exposed the exact Productivity Commission and DCCEEW links, and clearly separated the demonstrated handover from unmeasured outcomes. The detergent-residue case still started correctly and the console reported no warnings or errors.
- Devpost remained publicly accessible and submitted. Its public story still reflects the previous 25-check release and does not yet describe the structured handover or tool annotations.

The strongest next evidence is an independent owner/professional assessment of the handover. Additional test counts alone cannot establish that it saves time or increases the chance of winning.
