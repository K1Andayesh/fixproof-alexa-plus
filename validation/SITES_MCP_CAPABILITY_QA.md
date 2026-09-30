# Native Sites MCP capability

Verified 30 September 2026.

The hosted FixProof project now declares the native `mcp` capability in `.openai/hosting.json`. Its existing `POST /mcp` route exposes the same five-tool, D1-backed server and self-contained MCP App as the public `/api/mcp` judge endpoint. This closes the gap between having a callable MCP route and having the hosting platform provision the Site's ChatGPT/Codex plugin connection.

## Verification boundary

- The declaration does not change the fictional-only data policy or the public Site audience.
- Tool discovery contains no case data. Case-bearing tools accept only explicitly fictional demonstration cases and remain bounded to the four exact models.
- The public browser proof remains available without plugin installation.
- A successful deployment and a subsequent Site metadata read must expose an MCP connection URL and provisioned plugin ID before the platform-integration claim is treated as verified.

The Site-hosted plugin connection is additional integration evidence. It does not establish Alexa-device execution, customer validation, appliance inspection, diagnosis or repair success.
