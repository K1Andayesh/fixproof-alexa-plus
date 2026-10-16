# Payload-bound request-receipt QA — 16 October 2026

## Judge-facing weakness

The public MCP server previously cached a successful write by `request_id` alone. Replaying the exact request was idempotent, but accidental reuse of that ID for a different tool or changed payload could return the earlier result instead of reporting a conflict. The endpoint accepts fictional cases only, but this still weakened the workflow contract and could hide a client bug.

## Enhancement

Each new request receipt now stores the operation name and a SHA-256 digest of the canonical operation-plus-input object beside the committed case result. An exact replay returns the original result. Reuse with another operation or any changed input fails closed and tells the client to generate a new request ID. Older unbound receipts also fail closed rather than being treated as safe replays.

The zero-setup retry proof now exercises all three properties through the production MCP route:

1. deliberately ignore the first successful `record_outcome` response;
2. replay the exact operation and payload under the same request ID and recover the committed revision;
3. change only the fictional observation under that ID, require a tool error, then confirm through `read_case` that the original observation is the sole persisted outcome.

## Verification plan

- `npm run test:receipts` covers exact replay, changed payload, cross-tool reuse and legacy receipt rejection.
- `npm run lint` and `npm run build` cover the hosted implementation and browser proof.
- The existing 31 public-workflow tests remain green.
- Actual browser QA must show the local and production retry proof passing, one persisted outcome, the original fictional observation, matching browser-recomputed evidence fingerprint, and no console warnings or errors.

## Local verification

Release 0.13.0 passed the four receipt tests, lint, production build and all 31 public-workflow checks. Actual Chrome ran the local Worker proof and visibly reported protocol 2025-11-25, five tools, the MCP App, exact-retry recovery at revision 2, changed-input rejection, one persisted deferred outcome, pages 45 and 24, and a matching 64-digit fingerprint. The rendered handover retained the original fixed fictional observation rather than the rejected replacement. The browser console contained no warnings or errors.

## Boundary

This proves receipt binding and replay behaviour for the tested fixed fictional mutation. It does not authenticate a client, sign a receipt, force a network connection to drop at the commit boundary, prove general availability, or establish any appliance outcome.
