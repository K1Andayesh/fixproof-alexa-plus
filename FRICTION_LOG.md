# Amazon Developer Hackathon friction log

## Alexa+ implementation-path checklist

- **Task attempted:** Determine the eligible Alexa+ implementation path and the exact runtime evidence required for judging.
- **Steps taken:** Read the track overview, official rules, and submission requirements; compared the simulated-experience exception with the general runtime-hook requirement; implemented and tested the stronger MCP option.
- **Expected result:** One Alexa+ checklist connecting each implementation choice to the required repository and demo evidence.
- **Actual result:** The necessary facts were available, but split across track and submission sections. It was easy to read the general runtime-hook rule without finding its simulation exception.
- **Severity:** Important. A team can spend meaningful build time resolving an eligibility question before product work begins.
- **Workaround:** Cross-reference the overview and rules, then verify the official MCP SDK over Streamable HTTP with a real client.
- **Actionable suggestion:** Publish a decision table for Agent Skill, MCP, and simulated experience, with the required code and video evidence for each route.

## MCP transport verification

- **Task attempted:** Prove that the self-hosted agent surface was a real MCP endpoint rather than a set of similarly named HTTP functions.
- **Steps taken:** Added the official MCP Python SDK, exposed five tools through Streamable HTTP, connected with an independent MCP client, checked the negotiated protocol version and tool discovery, then tested an invalid browser Origin.
- **Expected result:** A short end-to-end verification recipe in the Alexa+ resources.
- **Actual result:** The SDK made implementation straightforward, but the evidence checklist had to be assembled from MCP documentation and hackathon requirements.
- **Severity:** Nice-to-have.
- **Workaround:** Retained the integration test, HTTP smoke client, and visible protocol/tool output in the repository and demo.
- **Actionable suggestion:** Provide a minimal judge-ready MCP verification example that prints the negotiated protocol version, discovered tools, one tool result, and Origin-guard behavior.

## Competition rules link continuity

- **Task attempted:** Recheck the official rules and the 16 September repository update before final submission work.
- **Steps taken:** Opened the previously published competition rules URL, confirmed that it returned HTTP 404, found the current Devpost competition URL, and rechecked the live rules page there.
- **Expected result:** The former official competition URL would redirect to the current rules page so saved links and entrant checklists remained usable.
- **Actual result:** `https://amazon-alexa-plus.devpost.com/rules` returned HTTP 404 on 26 September 2026, while `https://amazonappdev2026.devpost.com/rules` returned HTTP 200. Finding the current rules required a separate search.
- **Severity:** Important. A stale saved link can hide a rules update during the submission window.
- **Workaround:** Use the current [Amazon App Dev Challenge rules page](https://amazonappdev2026.devpost.com/rules) and recheck it from the competition landing page before submission.
- **Actionable suggestion:** Keep redirects from retired competition slugs through the submission and judging periods, and publish a canonical rules URL in update notices.
