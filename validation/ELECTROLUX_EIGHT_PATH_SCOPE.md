# Electrolux ESF8735ROX source map

Checked 17 September 2026 against the official [ESF8735ROX product page](https://www.electrolux.com.au/dishwashers/built-in/esf8735rox/) and [26-page English manual](https://resource.electrolux.com.au/Public/File/?Id=33277). The cover names ESF8735ROX and ESF8735RKX. The downloaded reference file has SHA-256 `7089b73bb67e976e348397074b2052e55d373caaa9ded6330a60b137eaf2400d`. Page numbers below are the printed manual numbers and PDF page numbers; pages 16, 18, 19, 20 and 21 were rendered and visually checked for this expansion.

| Issue path | User-level checks and cited pages |
| --- | --- |
| Wet tableware | Rinse aid (20), cooling (15), AirDry or documented door-opening alternative (15, 20) |
| Food remnants | Loading and spray-arm clearance (15), filter cleaning (16, 17, 20), more intensive programme (20) |
| Detergent residue | Keep basket items clear of dispenser lid (21); check blocked or clogged spray arm (21) |
| Removable white streaks | Lower excessive rinse-aid setting (20); use the correct detergent quantity on its packaging (20, 15) |
| Knocking or rattling during wash | Arrange tableware properly in baskets (19); check that spray arms rotate freely (19) |
| Rust spots on cutlery | Keep silver and stainless steel cutlery apart (20) |
| Interior odour | Clean interior and gasket after deactivating and unplugging (16, 18); review repeated short programmes (18); use a dishwasher-specific cleaner according to its packaging (18) |
| Door-related starting | Check door closure (18); clear tableware protruding from baskets (19) |

Only these eight paths are enabled for this exact model. The Bosch-specific check text and pages are never used for an Electrolux-only step. Irreversible glass clouding, water retention and error-code/pump/hose diagnosis are not mapped for this model in this release, even where the manual discusses a related problem. The prototype is a bounded evidence workflow, not a diagnosis or permission to attempt appliance repair. New paths were exercised with fictional reports and source-page assertions; they do not establish real-world effectiveness.

Verification: 33 Python and 21 public-interface checks passed; the 19-scenario baseline local-model evaluation and the [seven-case Electrolux evaluation](ELECTROLUX_LOCAL_AI_EVAL.json) passed. The official MCP client was updated to exercise all eight Electrolux paths and confirm an unmapped glass-clouding report produces no check; production evidence is recorded in [HOSTED_MCP.json](HOSTED_MCP.json). Browser QA remains to be repeated against the newly published release.
