# FixProof QA evidence — updated 14 September 2026

## Result

Working local MVP at http://127.0.0.1:8768. Real Qwen 3.5 4B inference through the existing local Ollama service; no paid API or model downloads. The exact source manual is documented in [FIXPROOF.md](FIXPROOF.md). This is implementation evidence, not customer validation or a physical appliance test.

## Actual Chrome UI checks

| Journey | Observed result |
| --- | --- |
| New fictional demo case | Saved with explicit fictional model identity and Open status |
| Ask for drying assessment | Real AI trace and manual-linked check visible; zero outcomes until explicit user action |
| Record waiting outcome | Fictional observation and Still wet saved; issue stayed Open |
| Reload browser / restart app process | Same case, history, outcome and revision restored |
| Natural follow-up after waiting | Final implementation selected rinse aid, excluding the recorded waiting check |
| Record Not yet tested | Export/record used that label, not completed or resolved |
| Prepare handover / preview | Handover ready; unresolved statement, model provenance, user notes and outcomes visible |
| Reopen and update deferred outcome | Rinse aid changed from Not yet tested to Still wet; earlier event retained in history |
| Unknown, unconfirmed model | No applicable reference warning; request received scope response and no check |
| Model endpoint deliberately unavailable | Visible error, revision unchanged, no assistant reply fabricated, message retained |
| Reload after failed request, restore provider, retry | Draft survived; retry created one reply at revision 1 and cleared draft |
| Two tabs editing same case | Old revision could not overwrite Handover ready with resolved; visible reload instruction |
| Desktop screenshot inspection | Readable two-column layout; no overlapping controls observed at tested desktop size |
| Voice-first UI | Chrome exposed an enabled Speak control, review-before-send privacy text, and typed fallback |
| Spoken response | Browser action completed and the live status returned to Ready; audible output could not be independently measured |
| Hosted judge-mode shortcuts | Plastic, safety hazard, unsupported issue, and unclear report each reached the intended bounded response |
| Safety stop persistence | Hazard language produced an explicit stop/handover response; after reload the case remained Handover ready and the ask form stayed unavailable |
| Handover completeness | Preview showed the exact model, recorded outcome, source, observation, and unresolved limits without overlap |

Main case: `5af1e227-332c-4d5f-ab7d-6da4312082d5`. Isolated failure/recovery case: `26f996b7-e461-462e-8365-c5a6d5374ba8`; unknown-model case: `84ae5f0b-433a-4991-87d4-9b35e52e5117`, both in ignored temporary data. All notes are fictional QA observations.

The download link was clicked and the server served the attachment. Its actual native download location was not verified: Chrome's internal downloads page was blocked by browser policy, and no workaround was attempted. The application's export endpoint was independently checked for 200 status, Markdown content type, attachment filename, page links and factual content. Its returned bytes are saved as [EXAMPLE_HANDOVER.md](EXAMPLE_HANDOVER.md). This separate file is endpoint evidence, not proof of the browser's disk save.

## Automated and live-model checks

- Eight standard-library workflow tests pass: duplicate request, origin guard, pending outcome requirement, separate resolution, SQLite persistence, stale writes, model failure, wrong/unconfirmed model gating, invalid model output, exclusion of recorded checks and explicit outcome revisiting. Some tests cover multiple assertions.
- One MCP integration test passes through the official SDK's in-process client, covering tool discovery, idempotent case creation, bounded next-step selection, explicit outcome persistence, read-back and handover content.
- A separate client connected to the running Streamable HTTP endpoint at `/mcp`, negotiated protocol `2026-07-28`, discovered all five tools, created a fictional case, obtained a real local-AI selected check, recorded an outcome and verified that the handover retained its observation. A request with an untrusted browser Origin was rejected with HTTP 403.
- Eight local-model scenarios pass: drying, unclear symptom, plastic, inside-wall condensation, unsupported error/drainage issue, hazard, already-recorded check and exhausted catalog. Full results and local latency/token observations: [LOCAL_AI_EVAL.json](LOCAL_AI_EVAL.json).
- Python compilation and JavaScript syntax checks pass.
- A source-only rehearsal copy under ignored `tmp/` passed the eight workflow tests and syntax checks. A focused scan found no email address, personal path or credential marker. Test-generated `__pycache__` remains excluded by the project `.gitignore`; the rehearsal intentionally contains no database or downloaded manual.
- The improved hosted-source build passed an actual Chrome desktop journey at `http://127.0.0.1:8769`: start the fictional exact-model case, request the first source-backed check, record a Still wet observation, reload, resume the saved case, and preview a handover containing the saved outcome, page 41 source and unresolved/unverified limits. The tested view had no visible overlap. Judge-mode shortcuts also exercised plastic, hazard, unsupported-issue, and unclear-report boundaries. These source changes remain local until the public Site is republished.

Two defects found and fixed during work: combined classification/selection occasionally assumed drying for an unclear report or failed to move past a recorded check. Classification now runs separately on user evidence; selection's schema is restricted to remaining catalog IDs. SQLite connections are explicitly closed after each transaction; the Windows test database cleanup exposed the original missing close.

The first main case retains the earlier clarification response as truthful QA history. Use a fresh demo case for final recording.

## Limits and next validation

- Small controlled evaluation set, not a robust safety or multilingual benchmark. No repair diagnosis, physical inspection or actual appliance outcome verified.
- Native mobile viewport, screen reader, keyboard-only end-to-end, long-running load and forced lost HTTP response after successful commit remain untested. Retry idempotency and stale versions have automated coverage; ordinary provider failure has UI coverage.
- Microphone capture was not started because accepting a Chrome microphone permission requires separate user authorization. Chrome exposed the API and the control remained enabled, but transcript accuracy and permission-denial UI remain unverified. The app states that Chrome may use an online recognition service and never auto-submits a transcript.
- No native Alexa account connection or voice/device execution tested. The product is labelled as an Alexa+ experience simulation.
- No owner/technician feedback or baseline comparison yet. Do not claim saved repair cost, repair accuracy, market demand or a better win probability.
- External owner/technician feedback, video recording/publication and final submission remain pending. Local pitch/demo/feedback draft is in `submission/DRAFT.md`.
