# Live proof timeout and cancellation QA

Date: 2026-10-11

## Risk addressed

The judge-facing live MCP proof previously waited indefinitely if the production endpoint stalled. A stalled request could leave every proof action disabled and provide no bounded result.

## Implemented behavior

- Every proof run now shares one `AbortController` across discovery, resource reads, tool calls, persistence checks, and integrity verification.
- A 15-second deadline aborts the run and reports that no result was claimed.
- A visible **Stop proof** action appears while a run is active. Stopping aborts the pending request, reports that no result was claimed, and restores the proof actions for a retry.
- Successful runs retain the existing five-tool, MCP App, persistence, retry-safety, and browser-recomputed SHA-256 checks.

## Verification

- `npm run build` — passed.
- `npm run lint` — passed.
- Production browser QA is recorded after deployment below.

## Claim boundary

Cancellation and timeout prove that the browser exits a stalled proof without displaying success. They do not prove endpoint availability, physical appliance inspection, diagnosis, repair success, or authorship of returned evidence.
