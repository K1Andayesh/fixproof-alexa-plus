# Hosted MCP readiness gate

Verified 29 September 2026.

`GET /health` proves that the Worker can answer and reports public release metadata. `GET /readiness` additionally checks the bound D1 database and the columns required by the `cases` and `requests` persistence tables.

The readiness check is read-only. It executes only `PRAGMA table_info` queries, creates no case, reads no stored case body, and returns no row counts or user data. It reports HTTP 503 with `status: not_ready` when the database binding is unavailable or the required schema is incomplete.

## Local verification

- `npm run lint` passed.
- `npm run build` passed and included `/readiness` as a dynamic route.
- The local Worker returned HTTP 200, `status: ready`, release `0.12.0`, D1 available, `cases + requests`, eight required columns and `mutation: none`.
- Actual Chrome displayed the readiness link on the MCP landing page and the existing live retry proof still negotiated server `0.12.0`, discovered five tools, loaded the MCP App and confirmed one persisted outcome for a repeated request ID.

These checks establish service readiness and schema availability. They do not validate any real appliance case, repair result or customer outcome.
