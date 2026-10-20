# Downloadable live judge-suite report QA

## Why this exists

A visible 3/3 result is useful during a browser session, but it disappears when the tab closes. The hosted MCP page now creates a downloadable JSON report directly from the three live proof results so a judge can retain and inspect the exact protocol version, server version, tool count, bounded assertion, complete evidence object, integrity declaration, returned fingerprint, and browser-recomputation result for every case.

The report is created only after the full suite passes. It contains fixed fictional proof data and explicitly states that it is not appliance inspection, diagnosis, repair success, customer validation, or authorship proof.

## Required report contract

- schema `fixproof-judge-suite-v1`
- production MCP endpoint
- negotiated protocol and returned server version
- exactly five discovered tools
- exactly three passed cases: `streaks`, `scope`, and `retry`
- a complete evidence object, supported integrity declaration, 64-character SHA-256 fingerprint, and `browser_recomputation: matched` for every case
- a repository verifier URL so every digest can be recomputed without the live service
- the evidence boundaries in `limits`

## Verification record

Verified locally on 20 October 2026:

- hosted MCP lint and production build passed
- four request-receipt tests, 31 public-workflow tests, and two focused verifier checks passed
- Chrome completed the real three-case suite and exposed **Download verified suite report**
- the browser-generated JSON used schema `fixproof-judge-suite-v1`, server `0.17.0`, all three expected case IDs, three complete evidence objects, three integrity declarations, and two explicit limit statements
- an independent browser recomputation of all three canonical evidence objects matched both digest fields, and the report exposed the repository verifier URL

Verified in production Chrome on 20 October 2026:

- main Site version 75, deployment `appgdep_6ad71b5919888191a12b89d798776f2d`, succeeded
- MCP Site version 43, deployment `appgdep_6ad71d50de6c819185f5479ffcd54205`, succeeded with MCP capability
- the main Site described the self-contained JSON proof report, stated that its evidence fingerprints can be independently recomputed, and routed to the live suite
- the production suite passed 3/3 on server `0.17.0`; its report contained five-tool discovery, all three complete evidence objects and integrity declarations, the verifier URL, and the explicit limits
- an independent browser recomputation matched both digest fields for all three production evidence objects


## Independent verification

Run `node validation/verify_judge_suite_report.cjs fixproof-live-judge-suite.json`. The verifier requires the exact three case IDs, validates the integrity declaration, canonicalizes each included evidence object, recomputes SHA-256, and compares it with both returned digest fields. Its focused checks also prove that a changed evidence field fails verification.
