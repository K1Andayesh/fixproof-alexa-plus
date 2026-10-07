# FixProof product feedback

Prepared 7 October 2026 for the Build, Ship, Shape submission. This answers the required feedback prompts for every developer tool, API, or SDK that materially implements the submitted experience. Each statement is tied to repository or runtime evidence; it does not claim Alexa-device execution or independent user validation.

## Official MCP Python SDK 2.2.0

- **Used for:** the local five-tool FixProof server, Streamable HTTP transport, tool annotations, structured results, Origin handling, and the `ui://fixproof/handover.html` MCP App resource.
- **Worked well:** one server contract supported tool discovery, readable Markdown, structured JSON, and the App resource. An independent client negotiated protocol `2026-07-28`, exercised all five tools, reconnected, and recovered persisted state.
- **Needs work:** entrants would benefit from one judge-ready verification recipe that prints the negotiated protocol version, discovered tools, one structured result, App metadata, and invalid-Origin behaviour. We assembled that proof from several documentation surfaces.
- **Onboarding:** getting a basic tool running was direct; proving transport, persistence, retry behaviour, and App fallback for judging took substantially more work than hello world.
- **Build with it again?** **Yes.** The protocol kept the agent surface inspectable and client-independent while application code retained control of instructions and citations.
- **Evidence:** [`fixproof/mcp_server.py`](../fixproof/mcp_server.py), [`fixproof/mcp_smoke.py`](../fixproof/mcp_smoke.py), [`validation/RELIABILITY_MCP.json`](../validation/RELIABILITY_MCP.json).

## Official MCP TypeScript SDK 2.0.0 and MCP Apps extension

- **Used for:** the public judge-callable five-tool server, its Streamable HTTP routes, tool planning hints, and the self-contained handover App with text and structured fallbacks.
- **Worked well:** the same bounded workflow could run on public HTTPS, return a sandboxed App, and remain useful to clients that only consume Markdown or JSON.
- **Needs work:** a single end-to-end example should show public and authenticated routes, resource registration, App metadata, client fallback, and deployment-specific persistence together. That would reduce ambiguity between an MCP-shaped API and a protocol-verifiable server.
- **Onboarding:** the tool surface was quick to express; production proof required a separate client trace, resource checks, and a visible zero-setup browser proof.
- **Build with it again?** **Yes.** The SDK made the runtime requirement observable rather than leaving judges to infer it from endpoint names.
- **Evidence:** [`hosted-mcp/app/mcp/route.ts`](../hosted-mcp/app/mcp/route.ts), [`hosted-mcp/README.md`](../hosted-mcp/README.md), [`validation/HOSTED_MCP.json`](../validation/HOSTED_MCP.json).

## Sites hosting and D1

- **Used for:** the public evaluation site, public MCP deployment, and persistent fictional case and request-receipt records across client connections.
- **Worked well:** D1 enabled revision checks and idempotent request receipts in the same workflow, while the public Sites deployment made both product and protocol evidence available without judge setup.
- **Needs work:** the Windows packaging helper attempted a Unix shell path without preserving Windows separators, so releases required a manual `git archive` fallback after the source push. Portable packaging diagnostics and a documented Windows path would shorten release verification. D1 deployment guidance would also benefit from a concise readiness-and-migration checklist.
- **Onboarding:** the initial static site path was fast. Adding a Worker-compatible MCP service, D1 migration, and source-to-version provenance required more platform-specific setup.
- **Build with it again?** **Yes.** The combined hosting and state layer made the evidence publicly reproducible, provided the packaging path remains independently verifiable.
- **Evidence:** [public evaluation build](https://fixproof-alexa.keyvan-andayesh.chatgpt.site), [public MCP proof](https://fixproof-mcp.keyvan-andayesh.chatgpt.site), [`validation/RETRY_SAFETY_QA.md`](../validation/RETRY_SAFETY_QA.md).

## Ollama API with Qwen 3.5 4B

- **Used for:** local symptom classification and selection from server-provided remaining check IDs. Application code supplies all instructions and citations.
- **Worked well:** the local endpoint kept fictional evaluation data on the development machine and allowed exact structured decisions against a small bounded catalog. The recorded suite passed 26 of 26 scenarios across the baseline and Electrolux-specific sets.
- **Needs work:** model availability, digest, JSON behaviour, latency, and host resources remain environment-dependent. A portable evaluation must record the model digest and retain deterministic application-side validation rather than trusting free-form output.
- **Onboarding:** connecting to an already-running local model was simple; reliable structured decisions required separate classification and selection prompts plus strict result validation.
- **Build with it again?** **Yes, for bounded local classification.** It is not used as a source of repair instructions or as evidence that a physical diagnosis is correct.
- **Evidence:** [`fixproof/server.py`](../fixproof/server.py), [`validation/LOCAL_AI_EVAL.json`](../validation/LOCAL_AI_EVAL.json), [`validation/ELECTROLUX_LOCAL_AI_EVAL.json`](../validation/ELECTROLUX_LOCAL_AI_EVAL.json).

## Browser SpeechRecognition and SpeechSynthesis APIs

- **Used for:** optional `en-AU` speech input with review before sending, and spoken playback of the latest visible response.
- **Worked well:** the APIs allowed a progressive enhancement with typed input and visible text as complete fallbacks. No transcript is submitted automatically.
- **Needs work:** support and speech-service behaviour vary by browser, and the browser may use an online recognition service. Permission denial, recognition accuracy, and microphone capture were not evaluated in this submission, so those behaviours must remain explicit and optional.
- **Onboarding:** feature detection and fallback were straightforward; trustworthy UX required status messages, review-before-send, and no automatic submission.
- **Build with it again?** **Yes, only as optional input and playback.** The typed workflow remains the reference path.
- **Evidence:** [`dist/app.js`](../dist/app.js), [`validation/FIXPROOF_QA.md`](../validation/FIXPROOF_QA.md).

## Related optional feedback

The separate [`FRICTION_LOG.md`](../FRICTION_LOG.md) records three reproducible issues in the competition implementation path, MCP verification path, and rules-link continuity using the required task, steps, expected result, actual result, severity, workaround, and actionable suggestion fields.


