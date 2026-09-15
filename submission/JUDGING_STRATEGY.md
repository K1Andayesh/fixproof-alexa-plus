# FixProof judging strategy

Prepared 14 September 2026 against the four equally weighted Alexa+ judging criteria. This is an evidence plan, not a prediction of placement.

## Technical implementation

**Lead proof:** a judge-callable five-tool MCP workflow over public HTTPS using the official TypeScript SDK and D1 continuity, plus the deeper local Python/SQLite/Qwen implementation with bounded model decisions, self-contained page citations, request idempotency, stale-write protection, Origin rejection, and an official MCP App.

**Judge should see:** open **Call the live public MCP endpoint** in the implementation card, then inspect the captured run. The official client evidence records five live tools, exact page URLs, D1 continuity across new connections without repeating a recorded check, 42 passing automated checks and fifteen live local-AI scenarios. The 2:15 video shows the public MCP endpoint and current three-model, six-path scope; the five-block trace shows the deeper local MCP Apps path.

## Design and user experience

**Lead proof:** one action at a time, exact-model source links, explicit outcome choices, reload/resume, spoken playback, typed fallback, and a handover that separates recorded facts from unresolved limits in both the public simulation and an inline MCP App.

**Judge should see:** start a case, save `Issue unchanged`, reload, resume, preview the handover, then use the four boundary shortcuts.

## Potential impact

**Lead story:** the Australian Productivity Commission found significant and unnecessary barriers to repair for some products and identified restricted access to repair information among them. DCCEEW reports that Australia created 511,000 tonnes of e-waste in 2019. FixProof tests a narrow response: keep verified instructions and user-confirmed outcomes portable between the household, assistant and technician. Six source-backed paths now run against three independently verified exact-model catalogs, showing that the evidence pattern can change references without blending sources.

**Judge should see:** the public impact card first, including the controlled retrieval result, then complete one check and open the handover. In eight blind reads per format, two independent local model families recovered 76/80 exact fields with zero critical errors from the structured handover versus 71/80 fields and two critical errors from equal-fact transcripts.

**Evidence boundary:** official sources establish the repair and e-waste context; they do not establish FixProof's effect. The retrieval result is a small synthetic machine-reader evaluation, not customer validation. There is no time-saving, repair-success, cost or waste-reduction claim. See `validation/IMPACT_EVIDENCE.md` and `validation/HANDOVER_RETRIEVAL_EVAL.md`.

## Quality of the idea

**Lead distinction:** the product is a persistent evidence workflow, not another troubleshooting answer. AI chooses only an approved step ID; application code owns the instruction and citation; only the user records an outcome. The result becomes a portable, human-readable MCP App inside the conversation while retaining machine-readable evidence and a text fallback.

**Memorable line:** The next repair conversation starts with evidence.

## Optional bonus evidence

Submit the friction log for the optional bonus. It documents two concrete developer-experience issues, reproducible steps, workarounds, severity, and actionable suggestions.

## Completed submission

The entry was submitted on 14 September 2026, with the public project at https://devpost.com/software/fixproof. The current 2:15 release walkthrough is embedded on the live evaluation page. Devpost still points to the earlier https://youtu.be/T-yjzCHgvus video until the new MP4 and captions are published on YouTube and the submission is updated. Eligibility attestations were confirmed before submission.

## Current release evidence

The reliability changes in validation/RELIABILITY_REVIEW.md have 28 Python tests, fourteen public-interface logic tests and fifteen passing live local-AI scenarios. The public MCP deployment adds a judge-callable five-tool HTTPS route with D1 continuity. The controlled retrieval evaluation adds 16 blind-format reads across two local model families. Independent owner/professional validation remains missing; no time-saving or winning-probability claim is supported.
