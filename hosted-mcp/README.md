# FixProof hosted MCP

This Cloudflare Worker-compatible Sites project exposes the FixProof workflow as a public Streamable HTTP MCP endpoint. It uses the official `@modelcontextprotocol/server` 2.x SDK and D1 for fictional-case continuity across client connections.

The public endpoint accepts fictional evaluation data only. `start_case` requires `fictional_demo: true` and rejects other calls. Do not send personal or real appliance data.

## Local run

```powershell
npm ci
npm run db:generate
npm run build
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_familiar_la_nuit.sql
npm start -- --port 8790
```

Connect an MCP client to `http://127.0.0.1:8790/api/mcp`. The `/mcp` route remains a local-compatible alias. From the repository root, exercise the complete two-connection flow with:

```powershell
.\.venv\Scripts\python.exe fixproof\hosted_mcp_smoke.py
```

The server exposes `start_case`, `read_case`, `ask_fixproof`, `record_outcome`, and `prepare_handover`. It covers three exact Bosch models and nine bounded, source-backed issue paths. Each selected check returns the official manual identity, exact page URL, verification date, and locally verified source hash.
