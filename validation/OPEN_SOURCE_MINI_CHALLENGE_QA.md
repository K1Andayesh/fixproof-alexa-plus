# Open Source mini-challenge evidence QA

## Purpose

The public FixProof evaluation page now assembles the four items required by the competition rules for the Open Source mini-challenge: contribution URL, project repository URL, GitHub username, and a description of what the contribution does and why it matters.

## Published evidence

- Contribution: `K1Andayesh/fixproof-evidence-verifier@2f50996`, the initial six-file, 320-line implementation.
- Project repository: the separate public `fixproof-evidence-verifier` repository.
- GitHub username: `K1Andayesh`.
- Function: a Python standard-library verifier that checks the FixProof sorted-JSON SHA-256 fingerprint offline, exercises a TypeScript-exported fictional fixture, detects changed fields, and rejects malformed inputs.
- License: public MIT license.

## Claim boundary

A matching fingerprint detects changes relative to the supplied digest. It does not establish authorship, trusted provenance, physical inspection, or repair success. The sample is fictional and is not uploaded by the verifier.

## Browser checks

- Confirm all four evidence cells are visible and readable on desktop and mobile widths.
- Confirm the contribution commit, repository, username, and license links resolve to their public GitHub targets.
- Confirm the limitation statement remains visible with the evidence.

This public proof improves judge access to the evidence. The official Devpost mini-challenge fields still need the same URLs and description entered through the submission editor.
