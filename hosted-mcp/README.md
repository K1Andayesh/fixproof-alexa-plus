# FixProof hosted MCP

This Cloudflare Worker-compatible Sites project exposes the FixProof workflow as a public Streamable HTTP MCP endpoint. It uses the official `@modelcontextprotocol/server` 2.x SDK and D1 for fictional-case continuity across client connections. The `prepare_handover` tool advertises a self-contained MCP App at `ui://fixproof/handover.html`, while retaining readable Markdown and machine-readable JSON fallbacks.

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

The server exposes `start_case`, `read_case`, `ask_fixproof`, `record_outcome`, and `prepare_handover`. It also exposes the handover App as a `text/html;profile=mcp-app` resource. The App has no external scripts, styles, images, or network calls; it renders only the structured handover returned by the tool. The server covers three exact Bosch models and nine bounded, source-backed issue paths. Each selected check returns the official manual identity, exact page URL, verification date, and locally verified source hash.

The landing page offers two fixed-fictional-case proofs against the production endpoint. **Run live MCP proof** selects a cited streaks check, records a deferred outcome, reads it back and renders the handover App in a sandboxed iframe. **Run scope boundary proof** reports standing water and drainage, then verifies that no drying check was selected, the scope report survived a read-back and the App shows the unsupported issue. This lets a judge inspect the returned App without configuring a separate MCP host; the iframe preview does not claim Alexa device execution. The server refuses drainage, pump and error-code reports rather than reclassifying their water wording as a supported drying path.
