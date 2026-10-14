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
- Production browser verification is recorded after deployment.

## Claim boundary

This proves changed-field detection for the demonstrated local mutation. It does not prove authorship, identity, physical inspection, diagnosis, repair success, customer validation, or Alexa-device execution.
