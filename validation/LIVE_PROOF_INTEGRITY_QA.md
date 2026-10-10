# Live MCP proof integrity QA

Prepared 10 October 2026 for the public FixProof MCP judge endpoint.

## Risk addressed

The zero-setup proof previously displayed the tool count and server-supplied evidence digest, but it did not independently verify either claim in the judge's browser. Five unexpected tools could satisfy the count, and a changed evidence object could still be shown beside an unverified digest.

## Implemented boundary

Each live proof now requires the exact five-tool contract by name. After `prepare_handover`, the browser checks the fingerprint declaration, canonicalizes the returned evidence with `fixproof-sorted-json-v1`, recomputes SHA-256 with Web Crypto, and fails the proof if the digest differs. A passing result explicitly states that browser recomputation matched the returned evidence.

This detects changed evidence fields in the returned handover. It does not prove authorship, appliance inspection, diagnosis, or repair success.

## Verification

- The production build completes with the added client-side canonicalization and digest check.
- Browser QA runs the deployed retry-safety proof through the production Streamable HTTP endpoint and verifies: `Live proof passed`, exact five-tool discovery, retry idempotency, and the visible browser-recomputation result.
- The deployed Site remains public and its release readiness endpoint stays read-only.
