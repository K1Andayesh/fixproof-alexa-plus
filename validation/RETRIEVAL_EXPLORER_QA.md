# Controlled retrieval explorer QA

## Purpose

The public impact evidence now lets a judge inspect all 54 scored reads across nine fictional cases and three local reader models without interpreting the raw JSON artifact.

## Evidence boundary

The explorer reads the already published `handover-retrieval-eval.json` artifact in the browser. It exposes both formats, all scored fields, and critical errors. It explicitly reports that structured handovers scored lower in two scenarios and tied in one. This is a synthetic machine-reader evaluation; it does not establish human comprehension, repair outcomes, time saved, customer impact, or reduced waste.

## Browser checks

- Open the public impact section and activate **Explore all 54 scored reads**.
- Confirm the dialog names the fictional case and displays transcript and structured-handover scores side by side.
- Change both the case and reader model and confirm the comparison updates.
- Confirm missed fields and critical errors remain visible rather than being omitted.
- Confirm the complete JSON artifact remains downloadable.
- Close the dialog and confirm focus returns to the explorer button.
