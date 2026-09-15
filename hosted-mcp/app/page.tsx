const tools = ["start_case", "read_case", "ask_fixproof", "record_outcome", "prepare_handover"];

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f7f7f1] text-[#163a31]">
      <section className="mx-auto grid min-h-screen max-w-6xl content-center gap-12 px-6 py-16 lg:grid-cols-[1.15fr_.85fr] lg:px-10">
        <div>
          <p className="mb-5 text-sm font-bold uppercase tracking-[0.18em] text-[#547267]">FixProof · Alexa+ track</p>
          <h1 className="max-w-3xl text-5xl font-bold leading-[1.02] tracking-[-0.045em] sm:text-7xl">A live MCP endpoint judges can call.</h1>
          <p className="mt-7 max-w-2xl text-lg leading-8 text-[#425f56]">
            The public FixProof server carries a fictional dishwasher issue through exact-model, page-cited checks and a structured repair handover. Its state survives new client connections, and every handover includes a reproducible evidence fingerprint.
          </p>
          <div className="mt-9 flex flex-wrap gap-3">
            <a className="rounded-full bg-[#163a31] px-6 py-3 font-semibold text-white" href="https://fixproof-alexa.keyvan-andayesh.chatgpt.site">Try the browser experience</a>
            <a className="rounded-full border border-[#9eb4ab] px-6 py-3 font-semibold" href="https://github.com/K1Andayesh/fixproof-alexa-plus">Inspect the source</a>
          </div>
          <div className="mt-12 rounded-2xl border border-[#c9d5cf] bg-white p-6 shadow-[0_18px_60px_rgba(18,57,47,.08)]">
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#6a857a]">Streamable HTTP endpoint</p>
            <code className="mt-3 block break-all text-base font-semibold text-[#163a31]">https://fixproof-mcp.keyvan-andayesh.chatgpt.site/api/mcp</code>
            <p className="mt-3 text-sm leading-6 text-[#61766e]">Protocol 2025-11-25 and later · JSON responses · no login · fictional evaluation cases only</p>
          </div>
        </div>

        <aside className="rounded-[2rem] bg-[#163a31] p-7 text-[#f7f7f1] shadow-[0_24px_80px_rgba(18,57,47,.2)] sm:p-9">
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#c6d8a4]">Five-tool persistent workflow</p>
          <ol className="mt-6 space-y-3">
            {tools.map((tool, index) => (
              <li className="flex items-center gap-4 rounded-xl border border-white/15 bg-white/[.04] p-4" key={tool}>
                <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-[#dff1b7] text-sm font-bold text-[#163a31]">{index + 1}</span>
                <code className="text-sm font-semibold sm:text-base">{tool}</code>
              </li>
            ))}
          </ol>
          <div className="mt-7 border-t border-white/15 pt-6 text-sm leading-6 text-[#d3e1db]">
            Three exact Bosch models · eight source-backed paths · revision checks · idempotent request IDs · D1 persistence · SHA-256 evidence fingerprint
          </div>
          <div className="mt-5 rounded-xl bg-[#dff1b7] p-4 text-sm font-semibold leading-6 text-[#163a31]">
            This endpoint refuses non-fictional cases. It does not diagnose faults, inspect appliances, or claim repair success.
          </div>
        </aside>
      </section>
    </main>
  );
}
