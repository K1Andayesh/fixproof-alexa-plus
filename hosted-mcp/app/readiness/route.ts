import { env } from "cloudflare:workers";
import { FIXPROOF_MCP_VERSION } from "../../lib/release";

export const dynamic = "force-dynamic";

const requiredColumns = {
  cases: ["id", "revision", "body", "created_at"],
  requests: ["id", "case_id", "body", "created_at"],
} as const;

type ColumnRow = { name: string };

export async function GET() {
  const responseHeaders = { "Cache-Control": "no-store" };
  try {
    if (!env.DB) throw new Error("missing binding");
    const [caseColumns, requestColumns] = await env.DB.batch([
      env.DB.prepare("PRAGMA table_info(cases)"),
      env.DB.prepare("PRAGMA table_info(requests)"),
    ]);
    const actual = {
      cases: new Set((caseColumns.results as ColumnRow[]).map((row) => row.name)),
      requests: new Set((requestColumns.results as ColumnRow[]).map((row) => row.name)),
    };
    const schemaReady = Object.entries(requiredColumns).every(([table, columns]) =>
      columns.every((column) => actual[table as keyof typeof actual].has(column)),
    );
    if (!schemaReady) {
      return Response.json({
        status: "not_ready",
        service: "FixProof MCP",
        version: FIXPROOF_MCP_VERSION,
        checks: { database_binding: "available", persistence_schema: "incomplete", mutation: "none" },
      }, { status: 503, headers: responseHeaders });
    }
    return Response.json({
      status: "ready",
      service: "FixProof MCP",
      version: FIXPROOF_MCP_VERSION,
      checks: {
        database_binding: "available",
        persistence_schema: "cases + requests",
        required_columns: 8,
        mutation: "none",
      },
    }, { headers: responseHeaders });
  } catch {
    return Response.json({
      status: "not_ready",
      service: "FixProof MCP",
      version: FIXPROOF_MCP_VERSION,
      checks: { database_binding: "unavailable", persistence_schema: "unchecked", mutation: "none" },
    }, { status: 503, headers: responseHeaders });
  }
}
