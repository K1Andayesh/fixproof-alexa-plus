# Core-flow keyboard QA

Prepared 3 October 2026 after keyboard testing the public evaluation workflow in Chrome.

## Observed gap

Starting or resuming a case replaces the entire introduction, but focus could remain on the now-hidden start or resume control. Asking for a check also revealed its outcome form without moving focus to the cited instruction. Keyboard and screen-reader users could therefore lose their place during the core workflow.

## Improvement

- Starting or resuming moves focus to the fictional case heading, or to the safety alert when the initial report stops the flow.
- A supported answer moves focus to the newly revealed check heading.
- Saving an outcome returns focus to the question field so the next step can be requested without traversing the page again.
- The case heading, check heading and safety alert are programmatically focusable while staying out of the normal Tab sequence.

## Verification boundary

The full start, ask and deferred-outcome path was exercised with keyboard input in Chrome, with focus checked after each transition. This verifies focus continuity for the core path; it is not a full screen-reader certification or validation of every optional control.
