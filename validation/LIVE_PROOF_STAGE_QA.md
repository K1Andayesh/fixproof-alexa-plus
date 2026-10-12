# Live proof stage transparency QA

Date: 2026-10-12

## Judge-facing gap

The zero-setup MCP proof previously showed one generic loading message while it negotiated the protocol, discovered tools and the App, mutated and restored persistent state, retried a write, and recomputed the evidence fingerprint. A judge could not tell which assertion was currently being exercised or where a failure occurred.

## Improvement

The public proof now exposes four ordered stages:

1. Negotiate MCP protocol.
2. Discover five tools and the MCP App.
3. Exercise cited-check persistence, scope-boundary persistence, or persistence plus retry safety, matching the selected proof.
4. Recompute the evidence fingerprint.

The active stage uses `aria-current="step"`; completed stages remain visibly marked, and a stopped or failed run marks the stage at which it ended. The checklist describes the actual assertions already enforced by the browser proof and does not add a new product or impact claim.

## Verification

- `npm run build` — passed.
- `npm run lint` — passed.
- `node validation/test_public_workflow.cjs` — all 31 browser-workflow regressions passed.
- Public MCP Site v32 deployed successfully and remained public.
- Production Chrome observed exactly one `aria-current="step"` item while the retry proof was running. Its four labels matched the protocol, discovery, retry/persistence, and integrity assertions.
- The completed retry proof marked all four stages complete, returned one persisted outcome after the duplicate request ID, matched the browser-recomputed SHA-256, rendered the MCP App, and produced no console warnings or errors.
- Stopping a scope proof marked its exact scope-boundary stage as failed, left the fingerprint stage pending, and displayed no false success.

## Claim boundary

The stage list makes the live browser checks easier to inspect. It does not prove appliance inspection, diagnosis, repair success, evidence authorship, customer validation, or Alexa-device execution.
