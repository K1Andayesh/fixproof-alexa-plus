# FixProof: implemented local feasibility MVP

Prepared 9 September 2026 after Keyvan confirmed no suitable caregiver testers are currently available. FixProof is now the active implemented direction following the instruction to continue to a proper state. It is not a validated winner or a validated customer proposition.

## First deliverable

One browser case that goes from a reported dishwasher drying, food-remnant or detergent-residue problem to a concise repair handover: exact model, verified reference, user-confirmed attempts, observed outcomes, and questions still unresolved.

The core question is whether recording and carrying the evidence forward is more useful than a manual plus ordinary chat. Source-backed answers alone are insufficient differentiation.

## Initial reference candidate

Bosch SMS6HAI02A/01, chosen as a public demonstration model rather than a claim about Keyvan's appliance. On 9 September 2026, the [exact service page](https://www.bosch-home.com.au/en/productservice/SMS6HAI02A-01) User Manual link opened [9001676154_A.pdf](https://media3.bsh-group.com/Documents/9001676154_A.pdf). Its cover names SMS6HAI02A; its document footer is 9001676154 (010805) 650 V1, Australian English, 56 pages. The /01 applicability is established by the exact service-page link, not a suffix printed on the cover.

Pages 23, 36, 37, 40, 41 and 42 were extracted and visually inspected. Pages 36–37 show filter maintenance and page 42 lists causes and checks for food remnants and detergent residue; pages 23, 40 and 41 support the drying path. SHA-256: `af965b35d3447c81adfc56bf652f75f8da565d47a9d4dc9c1e55030ae521a47c`. The public-facing catalog contains original short summaries and page links, not the full manual. Downloaded PDF and rendered pages remain under ignored `tmp/pdfs/`.

## Ordered work

1. Retrieve the linked manufacturer manual, verify its model coverage and record document version, language, source URL and page references. Use original concise summaries; do not bundle copyrighted manuals without permission.
2. Write five controlled cases: supported symptom, wrong/unknown model, insufficient evidence, already-tried step, and unresolved issue requiring a handover.
3. Implement one real AI interaction behind the existing local UI. A proposed step must point to applicable evidence. User completion and symptom resolution are separate records. Determine available model access and budget before any paid calls.
4. Create a local export with the user's issue, confirmed appliance identity, evidence links, recorded steps, their outcomes and unresolved questions. Do not infer a diagnosis, warranty coverage or completed repair.
5. Test in the actual browser: record -> next step -> evidence inspection -> confirm attempt/outcome -> reload -> resume -> export. Include missing evidence and interrupted requests.
6. Compare the result with a simple manual-and-notes baseline. Technical correctness is demonstrable without caregiver recruitment; customer value still needs feedback from an appliance owner or technician before making strong claims.

## Exit evidence

- Correct model/source matching across the controlled cases.
- No unsupported citations or invented completed actions in the evaluated runs.
- Saved history survives reload and the next interaction uses it.
- Export contains only recorded facts and identified uncertainties.
- A reviewer can understand the handover without reading the whole chat.

The ordered technical work above is implemented in `fixproof/`; see [QA evidence](FIXPROOF_QA.md). Local Qwen 3.5 4B classifies user symptoms and selects from ten source-backed checks across drying, food-remnant and detergent-residue paths after excluding recorded checks. The server supplies instructions and references. User actions alone record outcomes and status. Explicit revisiting preserves prior history. Markdown export contains recorded facts and identified uncertainties.

Customer comparison with a manual-and-notes baseline remains open. No appliance owner or repair professional has tested the product. CareRelay is parked; the earlier `prototype/` remains a historical intake/persistence spike.
