import { createMcpHandler, McpServer } from "@modelcontextprotocol/server";
import * as z from "zod/v4";
import {
  askFixProof,
  caseView,
  handover,
  models,
  outcomes,
  readCase,
  recordOutcome,
  startCase,
} from "../../lib/fixproof";
import { handoverAppHtml } from "../../lib/handover-app";

export const dynamic = "force-dynamic";

const readOnly = { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false };
const localWrite = { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false };
const outputSchema = z.looseObject({});
const handoverAppUri = "ui://fixproof/handover.html";
const handoverAppMime = "text/html;profile=mcp-app";

function result(value: Record<string, unknown>, text?: string) {
  return {
    content: [{ type: "text" as const, text: text ?? JSON.stringify(value, null, 2) }],
    structuredContent: value,
  };
}

function buildServer() {
  const server = new McpServer(
    { name: "FixProof", version: "0.11.0", websiteUrl: "https://fixproof-alexa.keyvan-andayesh.chatgpt.site" },
    {
      capabilities: { tools: {}, resources: {} },
      instructions: "Public judge endpoint for fictional FixProof evaluations. Use only the four listed exact Bosch or Electrolux models and fictional_demo=true. The three Bosch models cover drying, food-remnant, detergent-residue, removable-streak, wash-noise, cutlery-rust, irreversible-glass-clouding, unpleasant-interior-odour, door-related-starting and water-left-inside-after-programme paths. Electrolux ESF8735ROX covers drying, food-remnant, detergent-residue, removable-streak, unpleasant-interior-odour and door-related-starting paths only. Never offer a check lacking a citation for the selected exact model. Error codes, pump and hose work remain outside scope. Never send personal or real appliance data. Only explicit user outcomes count as attempted. Never claim a diagnosis, physical inspection, or verified repair.",
    },
  );

  server.registerResource(
    "FixProof repair handover",
    handoverAppUri,
    {
      title: "FixProof repair handover",
      description: "A compact evidence view for appliance owners and repair professionals.",
      mimeType: handoverAppMime,
      _meta: { ui: { prefersBorder: true } },
    },
    async (uri) => ({
      contents: [{
        uri: uri.href,
        mimeType: handoverAppMime,
        text: handoverAppHtml,
        _meta: { ui: { prefersBorder: true } },
      }],
    }),
  );

  server.registerTool(
    "start_case",
    {
      title: "Start a fictional FixProof case",
      description: `Start a persisted fictional evaluation case. Do not send personal or real appliance data. Supported models: ${models.join(", ")}.`,
      inputSchema: z.object({
        request_id: z.string().min(1).max(100),
        reported_issue: z.string().min(1).max(300),
        model: z.enum(models as [string, ...string[]]),
        model_confirmed: z.literal(true),
        fictional_demo: z.literal(true),
      }),
      outputSchema,
      annotations: localWrite,
    },
    async (input) => result(await startCase(input)),
  );

  server.registerTool(
    "read_case",
    {
      title: "Read a FixProof case",
      description: "Read the current revision, pending check, recorded evidence, citations, and safety state for a fictional case.",
      inputSchema: z.object({ case_id: z.string().uuid() }),
      outputSchema,
      annotations: readOnly,
    },
    async ({ case_id }) => result(caseView(await readCase(case_id))),
  );

  server.registerTool(
    "ask_fixproof",
    {
      title: "Ask FixProof",
      description: "Select one remaining bounded check from the exact-model catalog, request clarification, or stop on a tested safety report.",
      inputSchema: z.object({
        request_id: z.string().min(1).max(100),
        case_id: z.string().uuid(),
        revision: z.number().int().nonnegative(),
        user_message: z.string().min(1).max(300),
      }),
      outputSchema,
      annotations: localWrite,
    },
    async (input) => result(await askFixProof(input)),
  );

  server.registerTool(
    "record_outcome",
    {
      title: "Record a check outcome",
      description: "Record only the fictional user's explicit outcome for the currently pending check.",
      inputSchema: z.object({
        request_id: z.string().min(1).max(100),
        case_id: z.string().uuid(),
        revision: z.number().int().nonnegative(),
        step_id: z.string().min(1).max(80),
        outcome: z.enum(outcomes),
        observation: z.string().max(300).optional().default(""),
      }),
      outputSchema,
      annotations: localWrite,
    },
    async (input) => result(await recordOutcome(input)),
  );

  server.registerTool(
    "prepare_handover",
    {
      title: "Prepare a repair handover",
      description: "Return readable Markdown, versioned machine-readable evidence, exact-model provenance, limits, and a reproducible SHA-256 evidence fingerprint.",
      inputSchema: z.object({ case_id: z.string().uuid() }),
      outputSchema,
      annotations: readOnly,
      _meta: { ui: { resourceUri: handoverAppUri } },
    },
    async ({ case_id }) => {
      const value = await handover(await readCase(case_id));
      return result(value, value.markdown);
    },
  );

  return server;
}

const handler = createMcpHandler(buildServer);

export async function POST(request: Request) {
  return handler.fetch(request);
}

export async function GET(request: Request) {
  return handler.fetch(request);
}

export async function DELETE(request: Request) {
  return handler.fetch(request);
}

export function OPTIONS() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "content-type, accept, mcp-protocol-version, mcp-session-id, last-event-id",
      "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
      "Access-Control-Expose-Headers": "mcp-session-id, mcp-protocol-version",
    },
  });
}
