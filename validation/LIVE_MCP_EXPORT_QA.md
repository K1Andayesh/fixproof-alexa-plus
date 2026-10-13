# Live MCP evidence export QA

Date: 2026-10-13

## Judge-facing gap

The public MCP proof rendered its returned handover and independently verified the evidence fingerprint, but a judge could not take that exact result into the separate receiver flow. The portable handover claim therefore required either an MCP client or a different browser-simulation case.

## Improvement

- A passing live proof now offers **Download exact evidence JSON**.
- The file is created entirely in the browser from the exact `prepare_handover` structured result already fingerprinted and rendered on screen.
- A neighbouring **Open receiver verifier** link leads to the public local-only receiver, which recomputes `fixproof-sorted-json-v1` SHA-256 without uploading the file.
- The export is available only after the live proof passes, so a stopped or failed run cannot produce a judge-facing evidence file.

## Verification

- `npm run build` — passed.
- `npm run lint` — passed.
- `node validation/test_public_workflow.cjs` — all 31 browser-workflow regressions passed.
- Public production Chrome export and receiver round trip — pending deployment.

## Claim boundary

The round trip proves that the live MCP result can be carried into an independent browser receiver and checked for changed evidence fields. It does not prove authorship, physical inspection, diagnosis, repair success, customer validation, or Alexa-device execution.
