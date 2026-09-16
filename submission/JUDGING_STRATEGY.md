# FixProof judging strategy

Prepared 14 September 2026 against the four equally weighted Alexa+ judging criteria. This is an evidence plan, not a prediction of placement.

## Technical implementation

**Lead proof:** a judge-callable five-tool MCP workflow over public HTTPS using the official TypeScript SDK, D1 continuity and a self-contained inline MCP App, plus the deeper local Python/SQLite/Qwen implementation with bounded model decisions, self-contained page citations, request idempotency, stale-write protection, Origin rejection, and a cross-runtime SHA-256 fingerprint over each structured handover.

**Judge should see:** open **Call the live public MCP endpoint** in the implementation card, then choose **Run live MCP proof**. The browser calls the production protocol directly and reports negotiation, five-tool discovery, exact page selection, D1 read-back and the handover fingerprint. It then renders the actual `ui://` App resource with that fictional evidence in a sandboxed frame. **Run scope boundary proof** separately shows an unsupported error-code report reaching a no-check handover rather than a drying instruction. The saved official-client evidence verifies continuity across fresh connections without repeating a recorded check, alongside 54 passing automated checks and 26 live local-AI scenarios across the baseline and Electrolux expansion. The earlier 2:38 video shows nine paths and the controlled retrieval result; the live product now exposes ten Bosch paths plus an Electrolux eight-path subset.

## Design and user experience

**Lead proof:** one action at a time, exact-model source links, explicit outcome choices, reload/resume, spoken playback, typed fallback, and a handover that separates recorded facts from unresolved limits in both the public simulation and an inline MCP App. The zero-install build exports the same versioned evidence schema and fingerprint as a portable JSON file, then verifies and renders that file for the receiving person entirely in the browser.

**Judge should see:** start a case, save `Issue unchanged`, reload, resume, preview the fingerprinted handover, download the evidence JSON, then use **Verify evidence JSON** to confirm an unchanged copy and reject a changed field before using the four boundary shortcuts.

## Potential impact

**Lead story:** the Australian Productivity Commission found significant and unnecessary barriers to repair for some products and identified restricted access to repair information among them. DCCEEW reports that Australia created 511,000 tonnes of e-waste in 2019. FixProof tests a narrow response: keep verified instructions and user-confirmed outcomes portable between the household, assistant and technician. Ten source-backed paths run across three exact Bosch models; eight mapped guidance paths also run against an exact Electrolux model, showing second-manufacturer coverage without blending sources or implying unsupported paths.

**Judge should see:** the public impact card first, including the controlled retrieval result, then complete one check and open the handover. In twenty-seven blind reads per format, three independent local model families recovered 254/270 exact fields with zero critical errors from the structured handover versus 243/270 fields and five critical errors from equal-fact transcripts across all nine paths.

**Evidence boundary:** official sources establish the repair and e-waste context; they do not establish FixProof's effect. The retrieval result is a small synthetic machine-reader evaluation, not customer validation. There is no time-saving, repair-success, cost or waste-reduction claim. See `validation/IMPACT_EVIDENCE.md` and `validation/HANDOVER_RETRIEVAL_EVAL.md`.

## Quality of the idea

**Lead distinction:** the product is a persistent evidence workflow, not another troubleshooting answer. AI chooses only an approved step ID; application code owns the instruction and citation; only the user records an outcome. The result becomes a portable, human-readable MCP App inside the conversation while retaining machine-readable evidence, a text fallback and a reproducible fingerprint. The public receiving surface closes the loop by recomputing that fingerprint and showing whether the exact evidence still matches, without claiming authorship.

**Memorable line:** The next repair conversation starts with evidence.

## Optional bonus evidence

Submit the friction log for the optional bonus. It documents two concrete developer-experience issues, reproducible steps, workarounds, severity, and actionable suggestions.

## Open Source mini-challenge

The [additional FixProof Evidence Verifier](https://github.com/K1Andayesh/fixproof-evidence-verifier) is a standalone MIT-licensed Python project created during the hackathon window, separate from the primary FixProof repository. Its [initial contribution](https://github.com/K1Andayesh/fixproof-evidence-verifier/commit/2f50996) validates a fictional bundle exported by the public TypeScript MCP service without network access or third-party dependencies. Nine tests cover the cross-runtime fixture, changed and malformed evidence, and command-line behavior. The mini-challenge submission still needs these new contribution and repository URLs entered into the existing Devpost entry.

## Completed submission

The entry was submitted on 14 September 2026, with the public project at https://devpost.com/software/fixproof. The current 2:38 release walkthrough is embedded on the live evaluation page. Devpost still points to the earlier https://youtu.be/T-yjzCHgvus video until the new MP4 and captions are published on YouTube and the submission is updated. Eligibility attestations were confirmed before submission.

## Current release evidence

The current release has 33 Python tests, 21 public-interface logic tests and 19 passing live local-AI scenarios. The public MCP deployment adds a judge-callable five-tool HTTPS route with D1 continuity and a self-contained inline handover App. The controlled retrieval evaluation adds 54 blind-format reads across three local model families and its original nine paths. Independent owner/professional validation remains missing; no time-saving or winning-probability claim is supported. The public Devpost description and linked video still describe an earlier release; update them before judges review the entry.
