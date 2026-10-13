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
- Public MCP Site v35 deployed successfully from source commit `a6818e4767dba6c0720d8ffe155947030c127f76`.
- Production Chrome completed the retry-safety proof: protocol `2025-11-25`, five discovered tools, one persisted outcome for the repeated request ID, and a matching browser-recomputed evidence fingerprint.
- After the pass, Chrome exposed a direct `application/json` export containing the exact returned case, evidence and integrity record. The exported JSON parsed successfully and retained `fictional_demo: true`.
- The exact exported JSON was pasted into the separate public receiver. It recomputed `9276dde699d1674647844d6f1cfafb87d85afa12c4dff767d562daa3cb95810d`, matched the exported fingerprint, and rendered the same case, model, reference and evidence counts.
- The receiver produced no console warnings or errors. The automation browser could inspect the direct download payload but did not surface a filesystem download event for the data URL, so filesystem-level download capture remains unverified.

## Claim boundary

The round trip proves that the live MCP result can be carried into an independent browser receiver and checked for changed evidence fields. It does not prove authorship, physical inspection, diagnosis, repair success, customer validation, or Alexa-device execution.
