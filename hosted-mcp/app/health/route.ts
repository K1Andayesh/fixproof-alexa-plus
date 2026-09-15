import { models } from "../../lib/fixproof";

export function GET() {
  return Response.json({
    status: "ok",
    service: "FixProof MCP",
    version: "0.5.0",
    transport: "Streamable HTTP",
    protocol_minimum: "2025-11-25",
    endpoint: "/mcp",
    tools: ["start_case", "read_case", "ask_fixproof", "record_outcome", "prepare_handover"],
    exact_models: models.length,
    data_policy: "Fictional evaluation cases only. Do not send personal or real appliance data.",
  });
}
