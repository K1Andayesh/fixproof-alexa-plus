# Retry-safety judge proof — 25 September 2026

## Enhancement

The public MCP landing page offers a zero-setup **Run retry-safety proof** path. It opens a fixed fictional streaks case, selects a cited check, sends `record_outcome`, deliberately discards that first successful response, retries with the same `request_id`, reads the case back, and prepares the returned MCP App handover.

The current proof passes only when:

- the retry returns a committed result after the first response was intentionally ignored;
- `read_case` contains exactly one recorded outcome at the retry's committed revision;
- that one outcome retains the fixed fictional observation; and
- the handover App and evidence fingerprint still render.

## Local verification

`npm run lint` and `npm run build` passed in `hosted-mcp/`. Actual Chrome clicked the new proof against the local Worker and D1 database. The visible result reported protocol 2025-11-25, server 0.12.0, five tools, the MCP App, manual pages 45 and 24, revision 2 returned twice, and one persisted outcome. The rendered App showed 0 reported-performed checks, 1 deferred check, 2 citations, the fixed fictional observation and a 64-digit fingerprint. No real appliance or personal data was used.

## Boundary

This exercises the recovery decision a client makes after losing a successful response at its boundary. The production request completes and its returned value is deliberately ignored before the same request ID is retried. It does not force a transport connection to drop at the commit boundary, simulate every network failure, prove general availability, or establish repair outcomes.

## Production verification

MCP Site version 22 was saved from commit `5bfc1156343295a7f01a7f87a4f2432a772f3dcb` and production deployment `appgdep_6ab5e4d7dfb08191ace15b2a80ab97e6` succeeded. Actual Chrome ran the retry path against `https://fixproof-mcp.keyvan-andayesh.chatgpt.site/api/mcp`. The visible production result reported protocol 2025-11-25, server 0.12.0, five tools, the MCP App, revision 2 returned twice and one persisted outcome. The rendered App showed one deferred check, two source citations, the fixed fictional observation, a matching 64-digit fingerprint and the no-diagnosis boundary.
