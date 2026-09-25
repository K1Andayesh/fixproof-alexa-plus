# Retry-safety judge proof — 25 September 2026

## Enhancement

The public MCP landing page now offers a zero-setup **Run retry-safety proof** path. It opens a fixed fictional streaks case, selects a cited check, sends the same `record_outcome` mutation twice with the same `request_id`, reads the case back, and prepares the returned MCP App handover.

The proof passes only when:

- the retry returns the byte-equivalent structured result from the first mutation;
- both calls report the same case revision;
- `read_case` contains exactly one recorded outcome;
- that one outcome retains the fixed fictional observation; and
- the handover App and evidence fingerprint still render.

## Local verification

`npm run lint` and `npm run build` passed in `hosted-mcp/`. Actual Chrome clicked the new proof against the local Worker and D1 database. The visible result reported protocol 2025-11-25, server 0.12.0, five tools, the MCP App, manual pages 45 and 24, revision 2 returned twice, and one persisted outcome. The rendered App showed 0 reported-performed checks, 1 deferred check, 2 citations, the fixed fictional observation and a 64-digit fingerprint. No real appliance or personal data was used.

## Boundary

This demonstrates idempotent handling for one repeated `record_outcome` request through the real MCP route and persistence layer. It does not simulate every network failure, prove general availability, or establish repair outcomes.

## Production verification

Pending deployment.
