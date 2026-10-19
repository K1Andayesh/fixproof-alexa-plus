"use client";

import { useRef, useState } from "react";

type Proof = {
  protocol: string;
  server: string;
  tools: number;
  app: string;
  check: string;
  pages: string;
  continuity: string;
  fingerprint: string;
  integrity: string;
  scope?: string;
  retry?: string;
};

type ProofVariant = "streaks" | "scope" | "retry";

type ProofRun = {
  proof: Proof;
  appHtml: string;
  handover: Record<string, unknown>;
};

const proofLabels: Record<ProofVariant, string> = {
  streaks: "Cited continuity",
  scope: "Scope boundary",
  retry: "Delivery safety",
};

const proofStages: Record<ProofVariant, readonly string[]> = {
  streaks: ["Negotiate MCP protocol", "Discover five tools and the MCP App", "Exercise cited-check persistence", "Recompute the evidence fingerprint"],
  scope: ["Negotiate MCP protocol", "Discover five tools and the MCP App", "Exercise scope-boundary persistence", "Recompute the evidence fingerprint"],
  retry: ["Negotiate MCP protocol", "Discover five tools and the MCP App", "Converge duplicate delivery and reject changed input", "Recompute the evidence fingerprint"],
};

function sortForDigest(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(sortForDigest);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([left], [right]) => left < right ? -1 : left > right ? 1 : 0)
        .map(([key, item]) => [key, sortForDigest(item)]),
    );
  }
  return value;
}

async function evidenceSha256(evidence: Record<string, unknown>) {
  const canonical = JSON.stringify(sortForDigest(evidence));
  const hash = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonical));
  return Array.from(new Uint8Array(hash), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

function parseSse(text: string) {
  const line = text.split(/\r?\n/).find((value) => value.startsWith("data: "));
  if (!line) throw new Error("The endpoint returned no MCP message.");
  const message = JSON.parse(line.slice(6));
  if (message.error) throw new Error(message.error.message || "MCP request failed.");
  return message.result;
}

async function request(id: number, method: string, params: Record<string, unknown> = {}, signal?: AbortSignal) {
  const response = await fetch("/api/mcp", {
    method: "POST",
    headers: {
      Accept: "application/json, text/event-stream",
      "Content-Type": "application/json",
      "MCP-Protocol-Version": "2025-11-25",
    },
    body: JSON.stringify({ jsonrpc: "2.0", id, method, params }),
    signal,
  });
  if (!response.ok) throw new Error(`MCP request failed with HTTP ${response.status}.`);
  return parseSse(await response.text());
}

async function callTool(id: number, name: string, args: Record<string, unknown>, signal?: AbortSignal) {
  const result = await request(id, "tools/call", { name, arguments: args }, signal);
  if (result.isError) throw new Error(`${name} returned an MCP tool error.`);
  return result.structuredContent;
}

export function LiveProof() {
  const activeProof = useRef<AbortController | null>(null);
  const abortReason = useRef<"timeout" | "stopped" | null>(null);
  const [state, setState] = useState<"idle" | "running" | "passed" | "failed">("idle");
  const [phase, setPhase] = useState(0);
  const [variant, setVariant] = useState<ProofVariant>("streaks");
  const [proof, setProof] = useState<Proof | null>(null);
  const [suite, setSuite] = useState<Array<{ variant: ProofVariant; proof: Proof }>>([]);
  const [appView, setAppView] = useState<{ html: string; handover: Record<string, unknown> } | null>(null);
  const [error, setError] = useState("");

  async function run(selectedVariant: ProofVariant, suiteMode = false): Promise<ProofRun | null> {
    const controller = new AbortController();
    abortReason.current = null;
    activeProof.current = controller;
    const timeout = window.setTimeout(() => {
      abortReason.current = "timeout";
      controller.abort();
    }, 15_000);
    if (!suiteMode) {
      setState("running");
      setPhase(1);
      setVariant(selectedVariant);
      setProof(null);
      setSuite([]);
      setAppView(null);
      setError("");
    }
    try {
      const initialized = await request(1, "initialize", {
        protocolVersion: "2025-11-25",
        capabilities: {},
        clientInfo: { name: "FixProof browser judge probe", version: "1.0.0" },
      }, controller.signal);
      if (!suiteMode) setPhase(2);
      const listed = await request(2, "tools/list", {}, controller.signal);
      const expectedTools = ["ask_fixproof", "prepare_handover", "read_case", "record_outcome", "start_case"];
      const discoveredTools = listed.tools.map((item: { name: string }) => item.name).sort();
      if (JSON.stringify(discoveredTools) !== JSON.stringify(expectedTools)) throw new Error("The expected five-tool contract was not discoverable.");
      const resources = await request(3, "resources/list", {}, controller.signal);
      const app = resources.resources.find((item: { uri: string }) => item.uri === "ui://fixproof/handover.html");
      if (!app || app.mimeType !== "text/html;profile=mcp-app") throw new Error("The handover MCP App was not discoverable.");
      const appContents = await request(4, "resources/read", { uri: app.uri }, controller.signal);
      const appHtml = appContents.contents?.[0]?.text;
      if (typeof appHtml !== "string" || !appHtml.includes("FixProof repair handover")) throw new Error("The handover MCP App did not load.");
      if (!suiteMode) setPhase(3);

      const started = await callTool(5, "start_case", {
        request_id: crypto.randomUUID(),
        reported_issue: selectedVariant === "scope"
          ? "This fictional dishwasher displays error code E:61-03 after the wash."
          : "Removable streaks remain on glasses after this fictional wash.",
        model: "Bosch SMS6HCI02A/72",
        model_confirmed: true,
        fictional_demo: true,
      }, controller.signal);
      const guided = await callTool(6, "ask_fixproof", {
        request_id: crypto.randomUUID(),
        case_id: started.case_id,
        revision: started.revision,
        user_message: "What should I check first?",
      }, controller.signal);
      let restored;
      let handover;
      let selectedCheck;
      let selectedPages;
      let continuity;
      let scope: string | undefined;
      let retry: string | undefined;
      if (selectedVariant === "scope") {
        if (guided.status !== "Handover ready" || guided.pending_check || guided.latest_event?.kind !== "scope") throw new Error("The error-code report was not kept outside the verified scope.");
        restored = await callTool(7, "read_case", { case_id: started.case_id }, controller.signal);
        handover = await callTool(8, "prepare_handover", { case_id: started.case_id }, controller.signal);
        if (restored.status !== "Handover ready" || handover.evidence.checks?.length || handover.evidence.scope_report !== started.reported_issue) throw new Error("The scope boundary did not persist into the handover.");
        selectedCheck = "None";
        selectedPages = "none";
        continuity = "Scope boundary restored by read_case";
        scope = "Error-code report retained · no check selected";
      } else {
        const pending = guided.pending_check;
        if (!pending) throw new Error("The cited streaks check was not selected.");
        const mutationRequestId = crypto.randomUUID();
        const outcomeArgs = {
          request_id: mutationRequestId,
          case_id: started.case_id,
          revision: guided.revision,
          step_id: pending.step_id,
          outcome: "Not yet tested",
          observation: "Fictional browser proof; no appliance was inspected.",
        };
        let recorded;
        if (selectedVariant === "retry") {
          // Send two identical deliveries before either response is consumed.
          // Both must converge on the same committed receipt, then a later exact
          // replay must recover it while changed input fails closed.
          const [firstDelivery, duplicateDelivery] = await Promise.all([
            callTool(7, "record_outcome", outcomeArgs, controller.signal),
            callTool(8, "record_outcome", outcomeArgs, controller.signal),
          ]);
          if (firstDelivery.revision !== duplicateDelivery.revision) throw new Error("Duplicate deliveries returned different revisions.");
          recorded = await callTool(9, "record_outcome", outcomeArgs, controller.signal);
          if (recorded.revision !== firstDelivery.revision) throw new Error("The exact replay did not recover the duplicate-delivery result.");
          const conflict = await request(10, "tools/call", {
            name: "record_outcome",
            arguments: { ...outcomeArgs, observation: "Different fictional observation that must be rejected." },
          }, controller.signal);
          const conflictText = conflict.content?.find?.((item: { type: string }) => item.type === "text")?.text || "";
          if (!conflict.isError || !conflictText.includes("different operation or input")) throw new Error("Changed input reused the request ID without a conflict.");
          restored = await callTool(11, "read_case", { case_id: started.case_id }, controller.signal);
          handover = await callTool(12, "prepare_handover", { case_id: started.case_id }, controller.signal);
          const savedOutcomes = Object.keys(restored.recorded_outcomes || {});
          if (savedOutcomes.length !== 1 || restored.revision !== recorded.revision) throw new Error("The retried mutation changed persisted case state.");
          retry = `Two overlapping deliveries converged on revision ${recorded.revision} · exact replay recovered it · changed input rejected · one outcome persisted`;
        } else {
          recorded = await callTool(7, "record_outcome", outcomeArgs, controller.signal);
          restored = await callTool(8, "read_case", { case_id: started.case_id }, controller.signal);
          handover = await callTool(9, "prepare_handover", { case_id: started.case_id }, controller.signal);
        }
        const restoredObservation = restored.recorded_outcomes?.[pending.step_id]?.observation;
        if (restoredObservation !== "Fictional browser proof; no appliance was inspected.") throw new Error("The recorded observation did not persist.");
        selectedCheck = pending.title;
        selectedPages = pending.citations.map((item: { page: number }) => item.page).join(", ");
        continuity = `${recorded.evidence_summary.deferred_or_skipped} deferred · restored by read_case`;
      }

      if (!suiteMode) setPhase(4);
      const integrity = handover.evidence_integrity;
      if (integrity?.algorithm !== "sha256" || integrity?.canonicalization !== "fixproof-sorted-json-v1" || integrity?.covers !== "evidence" || integrity?.authorship_proof !== false) {
        throw new Error("The handover fingerprint declaration was missing or unsupported.");
      }
      const recomputedDigest = await evidenceSha256(handover.evidence);
      if (recomputedDigest !== integrity.digest) throw new Error("The browser-recomputed evidence fingerprint did not match the handover.");

      const proofResult: Proof = {
        protocol: initialized.protocolVersion,
        server: initialized.serverInfo.version,
        tools: listed.tools.length,
        app: `${app.name} · ${app.mimeType}`,
        check: selectedCheck,
        pages: selectedPages,
        continuity,
        fingerprint: handover.evidence_integrity.digest,
        integrity: "Browser recomputation matched the returned evidence",
        scope,
        retry,
      };
      if (suiteMode) return { proof: proofResult, appHtml, handover };
      setProof(proofResult);
      setAppView({ html: appHtml, handover });
      setPhase(5);
      setState("passed");
      return { proof: proofResult, appHtml, handover };
    } catch (reason) {
      if (suiteMode) throw reason;
      setError(
        abortReason.current === "timeout"
          ? "The production endpoint did not complete within 15 seconds. No result was claimed; try again."
          : abortReason.current === "stopped"
            ? "Proof stopped before completion. No result was claimed; run it again when ready."
            : reason instanceof Error ? reason.message : "The live proof failed.",
      );
      setState("failed");
    } finally {
      window.clearTimeout(timeout);
      if (activeProof.current === controller) activeProof.current = null;
    }
  }

  async function runSuite() {
    abortReason.current = null;
    setState("running");
    setVariant("streaks");
    setPhase(1);
    setProof(null);
    setSuite([]);
    setAppView(null);
    setError("");
    try {
      const results: Array<{ variant: ProofVariant; proof: Proof }> = [];
      let finalRun: ProofRun | null = null;
      for (const selectedVariant of ["streaks", "scope", "retry"] as const) {
        setVariant(selectedVariant);
        setPhase(1);
        finalRun = await run(selectedVariant, true);
        if (!finalRun) throw new Error(`${proofLabels[selectedVariant]} did not return a result.`);
        results.push({ variant: selectedVariant, proof: finalRun.proof });
        setSuite([...results]);
      }
      if (!finalRun) throw new Error("The judge suite returned no result.");
      setProof(finalRun.proof);
      setAppView({ html: finalRun.appHtml, handover: finalRun.handover });
      setPhase(5);
      setState("passed");
    } catch (reason) {
      setError(
        abortReason.current === "timeout"
          ? "A live suite case did not complete within 15 seconds. No suite pass was claimed; try again."
          : abortReason.current === "stopped"
            ? "Suite stopped before completion. No suite pass was claimed; run it again when ready."
            : reason instanceof Error ? reason.message : "The live judge suite failed.",
      );
      setState("failed");
    }
  }

  function stop() {
    abortReason.current = "stopped";
    activeProof.current?.abort();
  }

  const exportCaseId = typeof appView?.handover.case_id === "string" ? appView.handover.case_id.slice(0, 8) : "fictional";
  const exportHref = appView ? `data:application/json;charset=utf-8,${encodeURIComponent(`${JSON.stringify(appView.handover, null, 2)}\n`)}` : "";
  const suiteReport = suite.length === 3 ? {
    schema_version: "fixproof-judge-suite-v1",
    generated_at: new Date().toISOString(),
    endpoint: "https://fixproof-mcp.keyvan-andayesh.chatgpt.site/api/mcp",
    protocol: suite[0].proof.protocol,
    server: suite[0].proof.server,
    tools_discovered: suite[0].proof.tools,
    fictional_demo_only: true,
    cases: suite.map((result) => ({
      id: result.variant,
      title: proofLabels[result.variant],
      result: "passed",
      evidence: result.proof.scope || result.proof.retry || `${result.proof.check} · pages ${result.proof.pages} · ${result.proof.continuity}`,
      fingerprint: result.proof.fingerprint,
      browser_recomputation: "matched",
    })),
    limits: [
      "Fixed fictional cases only",
      "No appliance inspection, diagnosis, repair result, customer validation, or authorship proof",
    ],
  } : null;
  const suiteReportHref = suiteReport ? `data:application/json;charset=utf-8,${encodeURIComponent(`${JSON.stringify(suiteReport, null, 2)}\n`)}` : "";

  return (
    <section className="mx-auto max-w-6xl px-6 pb-16 lg:px-10" aria-labelledby="live-proof-title">
      <div className="grid gap-6 rounded-[2rem] border border-[#c9d5cf] bg-white p-7 shadow-[0_18px_60px_rgba(18,57,47,.08)] lg:grid-cols-[.75fr_1.25fr] lg:p-9">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#6a857a]">Zero-setup judge proof</p>
          <h2 id="live-proof-title" className="mt-3 text-3xl font-bold tracking-[-0.03em]">Call the live MCP now.</h2>
          <p className="mt-4 leading-7 text-[#52645b]">Choose a fixed fictional case. Every path calls the production MCP endpoint, then shows the returned handover App. The boundary path prevents an unsupported error code from becoming guidance; the retry path sends two overlapping copies of one mutation, replays the exact request, rejects changed input under that request ID, and confirms that only one outcome persists.</p>
          <button id="judge-suite-proof" onClick={runSuite} disabled={state === "running"} className="mt-6 rounded-full bg-[#163a31] px-6 py-3 font-semibold text-white disabled:cursor-wait disabled:opacity-60">
            {state === "running" ? "Running live proof…" : "Run complete judge suite"}
          </button>
          <button onClick={() => run("streaks")} disabled={state === "running"} className="mt-3 block rounded-full border border-[#a8c3b4] bg-white px-6 py-3 font-semibold text-[#163a31] disabled:cursor-wait disabled:opacity-60">
            Run cited continuity proof
          </button>
          <button onClick={() => run("scope")} disabled={state === "running"} className="mt-3 block rounded-full border border-[#a8c3b4] bg-white px-6 py-3 font-semibold text-[#163a31] disabled:cursor-wait disabled:opacity-60">
            Run scope boundary proof
          </button>
          <button id="retry-proof" onClick={() => run("retry")} disabled={state === "running"} className="mt-3 block rounded-full border border-[#a8c3b4] bg-white px-6 py-3 font-semibold text-[#163a31] disabled:cursor-wait disabled:opacity-60">
            Run retry-safety proof
          </button>
          {state === "running" && (
            <button onClick={stop} className="mt-3 block rounded-full border border-[#c08a83] bg-white px-6 py-3 font-semibold text-[#7b332c]">
              Stop proof
            </button>
          )}
          <p className="mt-3 text-xs leading-5 text-[#6a7b74]">Uses only hard-coded fictional data. It does not inspect or diagnose an appliance.</p>
        </div>
        <div className="rounded-2xl bg-[#f3f6f2] p-5" aria-live="polite">
          {state === "idle" && <p className="text-sm leading-6 text-[#61766e]">Ready. No request has been sent yet.</p>}
          {state === "running" && <p className="text-sm font-semibold text-[#36574c]">Live verification in progress · step {phase} of {proofStages[variant].length}</p>}
          {state === "failed" && <p className="text-sm font-semibold text-[#8a352c]">Proof failed: {error}</p>}
          {state === "passed" && proof && (
            <div>
              <p className="font-bold text-[#1d6848]">{suite.length === 3 ? "Complete judge suite passed · 3/3" : "Live proof passed"}</p>
              {suite.length === 3 && (
                <>
                  <ul className="mt-4 grid gap-2" aria-label="Judge suite results">
                    {suite.map((result) => (
                      <li key={result.variant} className="rounded-xl border border-[#c9d5cf] bg-white px-4 py-3 text-sm">
                        <strong className="text-[#1d6848]">✓ {proofLabels[result.variant]}</strong>
                        <span className="mt-1 block text-[#52645b]">{result.proof.scope || result.proof.retry || `${result.proof.check} · pages ${result.proof.pages} · ${result.proof.continuity}`}</span>
                        <span className="mt-1 block text-xs text-[#6a7b74]">Browser fingerprint recomputation matched</span>
                      </li>
                    ))}
                  </ul>
                  <a id="download-judge-suite" href={suiteReportHref} download="fixproof-live-judge-suite.json" className="mt-4 inline-block rounded-full bg-[#163a31] px-5 py-2.5 text-sm font-semibold text-white">
                    Download verified suite report
                  </a>
                  <p className="mt-2 text-xs leading-5 text-[#6a7b74]">Generated in this browser from the three live results. It includes each returned fingerprint and the proof limits.</p>
                </>
              )}
              <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
                <div><dt className="text-[#6a7b74]">Protocol · server</dt><dd className="font-semibold">{proof.protocol} · {proof.server}</dd></div>
                <div><dt className="text-[#6a7b74]">Discovery</dt><dd className="font-semibold">{proof.tools} tools · MCP App loaded</dd></div>
                <div><dt className="text-[#6a7b74]">{proof.scope ? "Boundary" : "Selected check"}</dt><dd className="font-semibold">{proof.scope || `${proof.check} · pages ${proof.pages}`}</dd></div>
                <div><dt className="text-[#6a7b74]">Continuity</dt><dd className="font-semibold">{proof.continuity}</dd></div>
                {proof.retry && <div className="sm:col-span-2"><dt className="text-[#6a7b74]">Retry safety</dt><dd className="font-semibold">{proof.retry}</dd></div>}
                <div className="sm:col-span-2"><dt className="text-[#6a7b74]">Evidence integrity</dt><dd className="font-semibold">{proof.integrity}</dd></div>
              </dl>
              <p className="mt-4 text-xs text-[#6a7b74]">{proof.app}</p>
              <code className="mt-2 block break-all text-xs text-[#36574c]">SHA-256 {proof.fingerprint}</code>
            </div>
          )}
          <ol className="mt-5 grid gap-2 border-t border-[#d8e2dc] pt-4" aria-label="Live proof stages">
            {proofStages[variant].map((label, index) => {
              const stage = index + 1;
              const complete = phase > stage;
              const current = state === "running" && phase === stage;
              const failed = state === "failed" && phase === stage;
              return (
                <li key={label} aria-current={current ? "step" : undefined} className={`flex items-center gap-3 text-sm ${complete ? "font-semibold text-[#1d6848]" : failed ? "font-semibold text-[#8a352c]" : current ? "font-semibold text-[#36574c]" : "text-[#71827a]"}`}>
                  <span aria-hidden="true" className="w-5 text-center">{complete ? "✓" : failed ? "!" : current ? "●" : "○"}</span>
                  <span>{label}</span>
                </li>
              );
            })}
          </ol>
        </div>
      </div>
      {state === "passed" && appView && (
        <div className="mt-6 rounded-[2rem] border border-[#c9d5cf] bg-white p-5 shadow-[0_18px_60px_rgba(18,57,47,.08)] sm:p-7">
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#6a857a]">Live MCP App preview</p>
          <h3 className="mt-2 text-2xl font-bold tracking-[-0.03em]">Inspect the live handover App.</h3>
          <p className="mt-2 text-sm leading-6 text-[#52645b]">This sandbox renders the App resource just read from the live MCP server, with the fictional handover returned by <code>prepare_handover</code>. Clients without MCP Apps still receive Markdown and structured evidence.</p>
          <div className="mt-4 flex flex-wrap gap-3">
            <a href={exportHref} download={`fixproof-live-${exportCaseId}.json`} className="rounded-full bg-[#163a31] px-5 py-2.5 text-sm font-semibold text-white">
              Download exact evidence JSON
            </a>
            <a href="https://fixproof-alexa.keyvan-andayesh.chatgpt.site/#verify-title" target="_blank" rel="noopener" className="rounded-full border border-[#a8c3b4] bg-white px-5 py-2.5 text-sm font-semibold text-[#163a31]">
              Open receiver verifier ↗
            </a>
          </div>
          <p className="mt-3 text-xs leading-5 text-[#6a7b74]">The download contains the exact fictional <code>prepare_handover</code> result shown below. The receiver recomputes its fingerprint locally without uploading the file.</p>
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
