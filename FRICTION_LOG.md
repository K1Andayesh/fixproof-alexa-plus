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
