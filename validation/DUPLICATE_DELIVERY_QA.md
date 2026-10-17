# Duplicate-delivery convergence QA

Prepared 17 October 2026.

## Reliability weakness

Two identical mutation deliveries can reach a server before either one has written its request receipt. The existing compare-and-swap prevented duplicate state changes, but the losing delivery could still receive a stale-revision or uniqueness error even though the same request had just succeeded. That behaviour is safe, but it makes ambiguous network retries harder for an MCP client to recover from.

## Enhancement

Release 0.14.0 re-reads the payload-bound request receipt after a write conflict or a losing compare-and-swap. If another delivery committed the same operation and canonical input, the loser returns that committed result. A different operation or changed input still fails closed. The database batch still prevents a losing state proposal from creating a receipt.

The zero-setup retry proof now sends two identical `record_outcome` requests concurrently, requires both responses to return the same revision, performs a later exact replay, rejects a changed observation under the same request ID, reads the case, and requires exactly one persisted outcome.

## Local verification

Release 0.14.0 passed the four payload-bound receipt tests, lint, production build and all 31 public-workflow checks. Actual Chrome ran the local Worker proof and visibly reported protocol 2025-11-25, five tools, the MCP App, two overlapping deliveries converged on revision 2, the exact replay recovered it, changed input was rejected, one deferred outcome persisted, pages 45 and 24, and the browser-recomputed SHA-256 matched the returned evidence.

## Production verification

Main commit `86ae3178b2f5899d9a94108fdce4942a59fdcdba` was pushed to the public repository. The current-release wording was published as public evaluation Site version 72 in successful deployment `appgdep_6ad32628c62c819195994a3bbf8fdc67`. The `hosted-mcp` source became Sites commit `e1a394f63d1e8992c3cb5678790d24a69045ec1c`, MCP Site version 38 and successful deployment `appgdep_6ad3273fa87c8191be48148646581102`. Both Sites remained public.

Actual production Chrome showed release 0.14.0 and ran the retry proof against the public Streamable HTTP endpoint. It visibly reported protocol 2025-11-25, five discovered tools, the loaded MCP App, both overlapping deliveries converged on revision 2, the later exact replay recovered that result, changed input was rejected, and one deferred outcome persisted. Pages 45 and 24 were retained, the browser-recomputed SHA-256 matched, and the rendered App showed the original fictional observation plus the no-inspection and no-diagnosis limits. The public evaluation page visibly described the same overlapping-delivery proof and linked to it.

## Evidence boundary

The browser sends two requests concurrently, but it cannot force a particular internal scheduling interleaving. A passing run demonstrates the production endpoint's result for that overlapping client pattern; it is not a load, availability, or distributed-systems benchmark. All data is fixed and fictional.
