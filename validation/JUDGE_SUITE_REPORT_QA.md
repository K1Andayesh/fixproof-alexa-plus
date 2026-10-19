# Downloadable live judge-suite report QA

## Why this exists

A visible 3/3 result is useful during a browser session, but it disappears when the tab closes. The hosted MCP page now creates a downloadable JSON report directly from the three live proof results so a judge can retain and inspect the exact protocol version, server version, tool count, bounded assertion, returned evidence fingerprint, and browser-recomputation result for every case.

The report is created only after the full suite passes. It contains fixed fictional proof data and explicitly states that it is not appliance inspection, diagnosis, repair success, customer validation, or authorship proof.

## Required report contract

- schema `fixproof-judge-suite-v1`
- production MCP endpoint
- negotiated protocol and returned server version
- exactly five discovered tools
- exactly three passed cases: `streaks`, `scope`, and `retry`
- a 64-character SHA-256 evidence fingerprint and `browser_recomputation: matched` for every case
- the evidence boundaries in `limits`

## Verification record

Verified locally on 19 October 2026:

- hosted MCP lint and production build passed
- four request-receipt tests and 31 public-workflow tests passed
- Chrome completed the real three-case suite and exposed **Download verified suite report**
- the browser-generated JSON used schema `fixproof-judge-suite-v1`, server `0.16.0`, five tools, all three expected case IDs, three 64-character fingerprints, three matched recomputations, and two explicit limit statements

Production Chrome verification, Site versions, and deployment identifiers are appended after deployment.
