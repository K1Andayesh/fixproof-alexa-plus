# Duplicate-delivery convergence QA

Prepared 17 October 2026.

## Reliability weakness

Two identical mutation deliveries can reach a server before either one has written its request receipt. The existing compare-and-swap prevented duplicate state changes, but the losing delivery could still receive a stale-revision or uniqueness error even though the same request had just succeeded. That behaviour is safe, but it makes ambiguous network retries harder for an MCP client to recover from.

## Enhancement

Release 0.14.0 re-reads the payload-bound request receipt after a write conflict or a losing compare-and-swap. If another delivery committed the same operation and canonical input, the loser returns that committed result. A different operation or changed input still fails closed. The database batch still prevents a losing state proposal from creating a receipt.

The zero-setup retry proof now sends two identical `record_outcome` requests concurrently, requires both responses to return the same revision, performs a later exact replay, rejects a changed observation under the same request ID, reads the case, and requires exactly one persisted outcome.

## Local verification

Release 0.14.0 passed the four payload-bound receipt tests, lint, production build and all 31 public-workflow checks. Actual Chrome ran the local Worker proof and visibly reported protocol 2025-11-25, five tools, the MCP App, two overlapping deliveries converged on revision 2, the exact replay recovered it, changed input was rejected, one deferred outcome persisted, pages 45 and 24, and the browser-recomputed SHA-256 matched the returned evidence.

## Evidence boundary

The browser sends two requests concurrently, but it cannot force a particular internal scheduling interleaving. A passing run demonstrates the production endpoint's result for that overlapping client pattern; it is not a load, availability, or distributed-systems benchmark. All data is fixed and fictional.
