# One-click MCP judge suite QA

## Purpose

The hosted MCP page now turns three separate proof paths into one judge action. The suite uses fixed fictional data and checks the public protocol and tool contract, cited-check continuity, unsupported-scope persistence, overlapping duplicate-delivery convergence, changed-input rejection, one-outcome persistence, and browser-side SHA-256 recomputation for every returned handover.

This is a judge-comprehension improvement. It does not claim appliance inspection, diagnosis, repair success, customer validation, or authorship proof.

## Reproduce

1. Open the public MCP page and choose **Run complete judge suite**.
2. Wait for **Complete judge suite passed · 3/3**.
3. Inspect the three result rows: **Cited continuity**, **Scope boundary**, and **Delivery safety**.
4. Confirm each row reports that its browser fingerprint recomputation matched.
5. Inspect the live MCP App preview for the final fictional handover.

## Verification record

Verified locally on 18 October 2026:

- hosted MCP lint passed
- hosted MCP production build passed
- four request-receipt tests passed
- 31 public-workflow tests passed
- Chrome ran the real local UI and displayed **Complete judge suite passed · 3/3**, with all three result rows and matched browser fingerprint recomputation

The final production Site version and deployment IDs are appended after deployment.
