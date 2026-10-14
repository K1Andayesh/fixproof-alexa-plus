# Changed-field proof QA

Date: 2026-10-14

## Judge-facing gap

The receiver already rejected altered evidence, but the public judge tour required someone to edit a JSON file manually. That made the negative integrity proof slower and easier to skip.

## Improvement

- After an unchanged bundle passes, the receiver now offers **Run changed-field check**.
- The action clones the verified evidence in memory, changes only the reported issue, and checks that copy against the original exported fingerprint.
- It does not overwrite the pasted bundle, upload data, or imply that a matching fingerprint proves authorship.
- A mismatch removes the action, so the result cannot be mistaken for another valid evidence rendering.

## Verification

- The existing portable-evidence regression now checks the helper's changed digest, mismatch verdict, visible control, and rendered negative result.
- `node --check dist/app.js` passed.
- `node --test validation/test_public_workflow.cjs` passed all 31 workflow regressions.
- Public FixProof Site v71 deployed successfully from commit `35d355b1841916fd62e064b5cee377762cbaea62`.
- Production Chrome generated a fresh fictional bundle through the live MCP retry-safety proof, then pasted that exact bundle into the receiver.
- The unchanged bundle matched fingerprint `9453706b00c4089a39f3b55c87c7a1b4f9224bfcdbf527eb8faa1e75ae5178af` and exposed **Run changed-field check**.
- The one-click check changed the local copy, produced recomputed fingerprint `e5238b88d1448452df52c7bc7b20b45f9d440e7717107466441da5409930e501`, displayed the mismatch, removed the valid-only action, and emitted no browser warnings or errors.

## Claim boundary

This proves changed-field detection for the demonstrated local mutation. It does not prove authorship, identity, physical inspection, diagnosis, repair success, customer validation, or Alexa-device execution.
