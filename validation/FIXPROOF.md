# FixProof: implemented local feasibility MVP

Prepared 9 September 2026 after Keyvan confirmed no suitable caregiver testers are currently available. FixProof is now the active implemented direction following the instruction to continue to a proper state. It is not a validated winner or a validated customer proposition.

## First deliverable

One browser case that goes from a reported dishwasher drying, food-remnant, detergent-residue, removable-streak, wash-noise, cutlery-rust, irreversible-glass-clouding, unpleasant-interior-odour or door-related-starting problem to a concise repair handover: exact model, verified reference, user-confirmed attempts, observed outcomes, and questions still unresolved.

The core question is whether recording and carrying the evidence forward is more useful than a manual plus ordinary chat. Source-backed answers alone are insufficient differentiation.

## Initial reference candidate

Bosch SMS6HAI02A/01, chosen as a public demonstration model rather than a claim about Keyvan's appliance. On 9 September 2026, the [exact service page](https://www.bosch-home.com.au/en/productservice/SMS6HAI02A-01) User Manual link opened [9001676154_A.pdf](https://media3.bsh-group.com/Documents/9001676154_A.pdf). Its cover names SMS6HAI02A; its document footer is 9001676154 (010805) 650 V1, Australian English, 56 pages. The /01 applicability is established by the exact service-page link, not a suffix printed on the cover.

Pages 23, 27, 35, 36, 37, 40, 41, 42, 44, 45, 46 and 48 were extracted and visually inspected. Pages 36–37 show filter maintenance; page 42 lists causes and checks for food remnants and detergent residue; pages 23, 40 and 41 support the drying path; pages 23, 27, 44 and 45 support the removable-streak path; page 48 supports the wash-noise path; and page 45 supports both the cutlery-rust and irreversible-glass-clouding paths; pages 35–36 support the unpleasant-interior-odour care path; and visually inspected troubleshooting pages 47, 51 and 48–49 support the door-related-starting path across the three models. SHA-256: `af965b35d3447c81adfc56bf652f75f8da565d47a9d4dc9c1e55030ae521a47c`. The public-facing catalog contains original short summaries and page links, not the full manual. Downloaded PDF and rendered pages remain under ignored `tmp/`.

### Second exact-model reference

Bosch SMS6HCI01A/38 was added on 15 September 2026 as an independent catalog entry rather than an alias for the first manual. The [exact service page](https://www.bosch-home.com.au/en/productservice/SMS6HCI01A-38) User Manual link opened [9001720311_B.pdf](https://media3.bsh-group.com/Documents/9001720311_B.pdf). Its cover names SMS6HCI01A and Australian information for use; its document footer is 9001720311 (050605) 650 A1, 60 pages. The /38 applicability is established by the exact service-page link.

Pages 24-25, 28, 38-39, 44-46, 48-50, 51 and 52 were extracted and visually inspected. They support the same thirty-one application-owned check summaries, with model-specific page mappings; page 49 supports both the cutlery-rust and irreversible-glass-clouding paths, while pages 37–38 support the unpleasant-interior-odour care path. SHA-256: `b2bb4608cd266752804e8c02b3e251bb31e6c32f95824e602614b13f83240fc9`. Each case now carries its selected model's manual URL, service URL, page citations and source hash through the browser and MCP handover.

### Third exact-model reference

Bosch SMS6HCI02A/72 was added on 15 September 2026 as another independent catalog entry. The [exact service page](https://www.bosch-home.com.au/en/productservice/SMS6HCI02A-72) User Manual link opened [9002017246_A.pdf](https://media3.bsh-group.com/Documents/9002017246_A.pdf). Its cover names SMS6HCI02A and Australian information for use; its document footer is 9002017246 (050605) 650 V1, 56 pages. The /72 applicability is established by the exact service-page link.

Pages 23-24, 27-28, 36-37, 41-50 were extracted and visually inspected. They support the same thirty-one check summaries and both informational results with a third independent page map; page 46 supports both the cutlery-rust and irreversible-glass-clouding paths, while pages 35–36 support the unpleasant-interior-odour care path. SHA-256: `b499156281a114882fd254e11400bc6318db71020eab2c4cfac9848264b4b476`.

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

The ordered technical work above is implemented in `fixproof/`; see [QA evidence](FIXPROOF_QA.md). Local Qwen 3.5 4B classifies user symptoms and selects from thirty-one source-backed checks across ten bounded paths, including water left inside after a programme after excluding recorded checks. The server supplies instructions and references. User actions alone record outcomes and status. Explicit revisiting preserves prior history. Markdown export contains recorded facts and identified uncertainties.

Customer comparison with a manual-and-notes baseline remains open. No appliance owner or repair professional has tested the product. CareRelay is parked; the earlier `prototype/` remains a historical intake/persistence spike.

## Water-retention source extension

The new path is grounded in the exact linked manuals' troubleshooting and filter pages: SMS6HAI02A/01 page 46 plus filter pages 36-37; SMS6HCI01A/38 page 50 plus filter pages 38-39; SMS6HCI02A/72 page 48 plus filter pages 36-37. The troubleshooting entries distinguish an unfinished programme from a filter obstruction. Only programme status and user-level filter cleaning are guided here; error codes, pump and hose work remain outside verified scope. The downloaded PDFs and visually checked rendered pages remain under ignored tmp/.
