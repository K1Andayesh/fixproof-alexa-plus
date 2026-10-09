# Browser storage fallback QA

Prepared 9 October 2026 for the public FixProof evaluation build.

## Risk addressed

The public evaluation previously wrote every case event directly to browser storage. If storage was blocked or exhausted, that write could throw and interrupt the judge flow even though the in-memory case was otherwise usable.

## Implemented boundary

Storage reads, writes, and removal now fail safely. When a write fails, the active fictional case continues in the current tab and an accessible status message explains that reload recovery is unavailable. The application does not claim persistence when the browser refused the write.

## Verification

- The regression suite replaces the storage writer with a throwing implementation, then starts a case and requests the first check. The case remains open, the documented check is selected, and the limitation is visible.
- Browser QA blocks same-origin storage writes, starts the public flow, confirms the case workspace and first source-backed check remain usable, and confirms the recovery limitation is visible without warning or error logs.
- Normal persistence and malformed-state recovery regressions remain green.

This is a browser-resilience test with fictional data. It does not establish appliance behavior, repair success, or external user validation.
