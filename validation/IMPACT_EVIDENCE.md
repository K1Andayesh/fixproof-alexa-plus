# FixProof potential-impact evidence

Checked 15 September 2026. This note separates the public problem context from outcomes the prototype has actually demonstrated.

## Official problem context

The Australian Productivity Commission's 2021 Right to Repair inquiry found significant and unnecessary barriers to repair for some products. Its report identifies manufacturer restrictions on repair supplies, including information, tools and parts, and discusses improved access to repair information as part of the policy response.

- Source: [Productivity Commission — Right to Repair inquiry report](https://www.pc.gov.au/inquiries-and-research/repair/report/)
- Relevance: supports the existence of an Australian repair-information problem. It does not evaluate FixProof.

The Australian Department of Climate Change, Energy, the Environment and Water reports that Australia created 511,000 tonnes of e-waste in 2019. Its e-stewardship page describes looking after electrical and electronic products as an environmental issue.

- Source: [DCCEEW — E-Stewardship in Australia](https://www.dcceew.gov.au/environment/protection/waste/e-waste)
- Relevance: establishes the scale of the broader waste context. It does not show that FixProof reduces e-waste.

## Demonstrated product response

FixProof demonstrates a narrow mechanism relevant to that context:

- exact-model instructions remain tied to manufacturer pages;
- a suggestion is not recorded as performed until the user supplies an outcome;
- observations persist across a new MCP connection and a browser reload;
- a repair handover carries performed, deferred and unresolved evidence forward;
- unsupported issues and unconfirmed models do not receive model-specific steps.

The reproducible evidence is in `validation/RELIABILITY_REVIEW.md`, `validation/RELIABILITY_MCP.json`, `validation/LOCAL_AI_EVAL.json` and the automated test suites.

## Outcomes still to measure

The prototype has no independent user or repair-professional study. It therefore makes no claim about time saved, avoided repeat work, successful repairs, cost savings, replacement decisions or e-waste avoided. Those are evaluation targets, not current results.

A controlled synthetic retrieval check provides narrower evidence about the mechanism. Two independent local model families read the same seven fictional cases as ordinary transcripts and as FixProof handovers. Across fourteen blind reads per format, exact field retrieval was 133/140 (95.0%) from the structured handover and 127/140 (90.7%) from the transcript; the handover had zero critical evidence errors and the transcript had two. The complete inputs, outputs and scoring are in `HANDOVER_RETRIEVAL_EVAL.json`. This tests machine retrieval from a small synthetic set, not human comprehension or real-world impact.

A credible next study would give the same fictional case and handover to appliance owners and repair professionals, then compare repeated questions, missing facts, time to understand the case and confidence in the next safe action against an ordinary chat transcript.
