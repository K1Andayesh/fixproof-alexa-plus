# Handover receiver schema check

Checked 16 September 2026. This is a receiver-side evidence-integrity correction, not a claim of authenticated provenance.

## Reproduced issue

The production browser receiver accepted a deliberately malformed `fixproof-handover-1` object whose `model` and `reference` were strings. The independently recomputed digest matched because the digest covered those malformed fields. The visible result said the fingerprint matched, then displayed `Model: undefined` and `Reference: undefined · undefined`. The fingerprint alone cannot establish that a bundle conforms to the expected schema.

## Change and checks

- The browser receiver now checks essential version-one field types, nested checks and page citations, a supported reference or an unmatched model without recorded/pending checks, and the explicit `authorship_proof: false` integrity declaration before recomputing the fingerprint. Pasted input has the same 1 MB limit as uploaded files.
- The independent Python verifier applies equivalent structural checks. It continues to reject duplicate JSON keys and non-finite values; the browser's standard JSON parser does not expose duplicate keys, so that stricter CLI behavior is not claimed for the browser.
- The malformed matching-digest fixture now receives a schema-error verdict in the actual local browser UI. A separate fictional unmatched-model bundle with a matching digest displays `No verified reference for this model` rather than an undefined value.
- Seventeen public-interface logic tests and nine independent verifier tests passed. The TypeScript-exported fictional handover fixture still verifies in Python. Browser checks were developer QA, not an independent user evaluation.

A matching fingerprint detects changes against the digest supplied in the same bundle. It cannot establish who produced the bundle, whether its claims are true, or whether a physical check or repair occurred.
