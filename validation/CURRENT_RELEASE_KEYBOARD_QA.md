# Current-release keyboard QA

Prepared 2 October 2026 after testing the dated release snapshot in Chrome.

## Observed gap

Activating **Watch the current 2:39 walkthrough** changed the URL fragment and scrolled to the walkthrough, but keyboard focus remained on the document. That left keyboard and screen-reader users without a reliable focus cue at the destination.

## Improvement

The walkthrough heading is now programmatically focusable. The existing internal-link handler moves focus to it after activation, matching the behaviour already used by the verifier, impact evidence and fictional-case routes.

## Verification boundary

The changed route was exercised with the keyboard in Chrome and backed by a regression assertion. This verifies browser focus continuity; it is not a claim of full screen-reader or end-to-end keyboard-only case testing.
