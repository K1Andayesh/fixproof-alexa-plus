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

export const dynamic = "force-dynamic";

const readOnly = { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false };
const localWrite = { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false };
const outputSchema = z.looseObject({});

function result(value: Record<string, unknown>, text?: string) {
  return {
    content: [{ type: "text" as const, text: text ?? JSON.stringify(value, null, 2) }],
    structuredContent: value,
  };
}

function buildServer() {
  const server = new McpServer(
    { name: "FixProof", version: "0.6.0", websiteUrl: "https://fixproof-alexa.keyvan-andayesh.chatgpt.site" },
    {
      capabilities: { tools: {} },
      instructions: "Public judge endpoint for fictional FixProof evaluations. Use only the three listed exact Bosch models and fictional_demo=true. The verified catalog covers drying, food-remnant, detergent-residue, removable-streak, wash-noise, cutlery-rust and irreversible-glass-clouding paths. Never send personal or real appliance data. Only explicit user outcomes count as attempted. Never claim a diagnosis, physical inspection, or verified repair.",
    },
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
      description: "Return a readable Markdown handover and versioned machine-readable evidence with exact-model provenance and limits.",
      inputSchema: z.object({ case_id: z.string().uuid() }),
      outputSchema,
      annotations: readOnly,
    },
    async ({ case_id }) => {
      const value = handover(await readCase(case_id));
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
