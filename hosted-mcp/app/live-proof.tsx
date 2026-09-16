"use client";

import { useState } from "react";

type Proof = {
  protocol: string;
  server: string;
  tools: number;
  app: string;
  check: string;
  pages: string;
  continuity: string;
  fingerprint: string;
};

function parseSse(text: string) {
  const line = text.split(/\r?\n/).find((value) => value.startsWith("data: "));
  if (!line) throw new Error("The endpoint returned no MCP message.");
  const message = JSON.parse(line.slice(6));
  if (message.error) throw new Error(message.error.message || "MCP request failed.");
  return message.result;
}

async function request(id: number, method: string, params: Record<string, unknown> = {}) {
  const response = await fetch("/api/mcp", {
    method: "POST",
    headers: {
      Accept: "application/json, text/event-stream",
      "Content-Type": "application/json",
      "MCP-Protocol-Version": "2025-11-25",
    },
    body: JSON.stringify({ jsonrpc: "2.0", id, method, params }),
  });
  if (!response.ok) throw new Error(`MCP request failed with HTTP ${response.status}.`);
  return parseSse(await response.text());
}

async function callTool(id: number, name: string, args: Record<string, unknown>) {
  const result = await request(id, "tools/call", { name, arguments: args });
  if (result.isError) throw new Error(`${name} returned an MCP tool error.`);
  return result.structuredContent;
}

export function LiveProof() {
  const [state, setState] = useState<"idle" | "running" | "passed" | "failed">("idle");
  const [proof, setProof] = useState<Proof | null>(null);
  const [appView, setAppView] = useState<{ html: string; handover: Record<string, unknown> } | null>(null);
  const [error, setError] = useState("");

  async function run() {
    setState("running");
    setProof(null);
    setAppView(null);
    setError("");
    try {
      const initialized = await request(1, "initialize", {
        protocolVersion: "2025-11-25",
        capabilities: {},
        clientInfo: { name: "FixProof browser judge probe", version: "1.0.0" },
      });
      const listed = await request(2, "tools/list");
      const resources = await request(3, "resources/list");
      const app = resources.resources.find((item: { uri: string }) => item.uri === "ui://fixproof/handover.html");
      if (!app || app.mimeType !== "text/html;profile=mcp-app") throw new Error("The handover MCP App was not discoverable.");
      const appContents = await request(4, "resources/read", { uri: app.uri });
      const appHtml = appContents.contents?.[0]?.text;
      if (typeof appHtml !== "string" || !appHtml.includes("FixProof repair handover")) throw new Error("The handover MCP App did not load.");

      const started = await callTool(5, "start_case", {
        request_id: crypto.randomUUID(),
        reported_issue: "Removable streaks remain on glasses after this fictional wash.",
        model: "Bosch SMS6HCI02A/72",
        model_confirmed: true,
        fictional_demo: true,
      });
      const guided = await callTool(6, "ask_fixproof", {
        request_id: crypto.randomUUID(),
        case_id: started.case_id,
        revision: started.revision,
        user_message: "What should I check first?",
      });
      const pending = guided.pending_check;
      const recorded = await callTool(7, "record_outcome", {
        request_id: crypto.randomUUID(),
        case_id: started.case_id,
        revision: guided.revision,
        step_id: pending.step_id,
        outcome: "Not yet tested",
        observation: "Fictional browser proof; no appliance was inspected.",
      });
      const restored = await callTool(8, "read_case", { case_id: started.case_id });
      const handover = await callTool(9, "prepare_handover", { case_id: started.case_id });
      const restoredObservation = restored.recorded_outcomes?.[pending.step_id]?.observation;
      if (restoredObservation !== "Fictional browser proof; no appliance was inspected.") throw new Error("The recorded observation did not persist.");

      setProof({
        protocol: initialized.protocolVersion,
        server: initialized.serverInfo.version,
        tools: listed.tools.length,
        app: `${app.name} · ${app.mimeType}`,
        check: pending.title,
        pages: pending.citations.map((item: { page: number }) => item.page).join(", "),
        continuity: `${recorded.evidence_summary.deferred_or_skipped} deferred · restored by read_case`,
        fingerprint: handover.evidence_integrity.digest,
      });
      setAppView({ html: appHtml, handover });
      setState("passed");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "The live proof failed.");
      setState("failed");
    }
  }

  return (
    <section className="mx-auto max-w-6xl px-6 pb-16 lg:px-10" aria-labelledby="live-proof-title">
      <div className="grid gap-6 rounded-[2rem] border border-[#c9d5cf] bg-white p-7 shadow-[0_18px_60px_rgba(18,57,47,.08)] lg:grid-cols-[.75fr_1.25fr] lg:p-9">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#6a857a]">Zero-setup judge proof</p>
          <h2 id="live-proof-title" className="mt-3 text-3xl font-bold tracking-[-0.03em]">Call the live MCP now.</h2>
          <p className="mt-4 leading-7 text-[#52645b]">Runs a fixed fictional case through protocol negotiation, discovery, a cited check, explicit outcome storage, cross-request read-back, and the fingerprinted handover.</p>
          <button onClick={run} disabled={state === "running"} className="mt-6 rounded-full bg-[#163a31] px-6 py-3 font-semibold text-white disabled:cursor-wait disabled:opacity-60">
            {state === "running" ? "Running live proof…" : "Run live MCP proof"}
          </button>
          <p className="mt-3 text-xs leading-5 text-[#6a7b74]">Uses only hard-coded fictional data. It does not inspect or diagnose an appliance.</p>
        </div>
        <div className="rounded-2xl bg-[#f3f6f2] p-5" aria-live="polite">
          {state === "idle" && <p className="text-sm leading-6 text-[#61766e]">Ready. No request has been sent yet.</p>}
          {state === "running" && <p className="text-sm font-semibold text-[#36574c]">Calling the production Streamable HTTP endpoint…</p>}
          {state === "failed" && <p className="text-sm font-semibold text-[#8a352c]">Proof failed: {error}</p>}
          {state === "passed" && proof && (
            <div>
              <p className="font-bold text-[#1d6848]">Live proof passed</p>
              <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
                <div><dt className="text-[#6a7b74]">Protocol · server</dt><dd className="font-semibold">{proof.protocol} · {proof.server}</dd></div>
                <div><dt className="text-[#6a7b74]">Discovery</dt><dd className="font-semibold">{proof.tools} tools · MCP App loaded</dd></div>
                <div><dt className="text-[#6a7b74]">Selected check</dt><dd className="font-semibold">{proof.check} · pages {proof.pages}</dd></div>
                <div><dt className="text-[#6a7b74]">Continuity</dt><dd className="font-semibold">{proof.continuity}</dd></div>
              </dl>
              <p className="mt-4 text-xs text-[#6a7b74]">{proof.app}</p>
              <code className="mt-2 block break-all text-xs text-[#36574c]">SHA-256 {proof.fingerprint}</code>
            </div>
          )}
        </div>
      </div>
      {state === "passed" && appView && (
        <div className="mt-6 rounded-[2rem] border border-[#c9d5cf] bg-white p-5 shadow-[0_18px_60px_rgba(18,57,47,.08)] sm:p-7">
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#6a857a]">Live MCP App preview</p>
          <h3 className="mt-2 text-2xl font-bold tracking-[-0.03em]">Inspect the live handover App.</h3>
          <p className="mt-2 text-sm leading-6 text-[#52645b]">This sandbox renders the App resource just read from the live MCP server, with the fictional handover returned by <code>prepare_handover</code>. Clients without MCP Apps still receive Markdown and structured evidence.</p>
          <iframe
            title="Fictional FixProof MCP App handover"
            className="mt-5 h-[42rem] w-full rounded-2xl border border-[#d9e5dd] bg-[#f5f8f5]"
            sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox"
            referrerPolicy="no-referrer"
            srcDoc={appView.html}
            onLoad={(event) => event.currentTarget.contentWindow?.postMessage({ result: { structuredContent: appView.handover } }, "*")}
          />
        </div>
      )}
    </section>
  );
}
