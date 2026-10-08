# Saved-case recovery QA

Prepared 8 October 2026 for the public FixProof evaluation build.

## Risk addressed

The browser previously displayed **Resume saved case** whenever the storage key existed, then parsed it only after activation. Truncated JSON, an old incompatible shape, or an unsupported pending check could throw before the judge reached the core flow.

## Implemented boundary

The public build now validates the saved case before showing Resume and again immediately before restoring it. It checks the case identity, exact supported model, workflow, event shape, outcome values, pending check, and status. Legacy cases without `model` or `workflow` retain the documented Bosch drying defaults. Invalid data is removed from browser storage, Resume stays hidden, and an accessible status message asks the judge to start a new fictional case.

The recovery path does not upload, retain, or inspect personal appliance data. The public build remains a fictional evaluation only.

## Verification

- Automated regression injects truncated JSON and a structurally valid case with an unsupported pending check. Both fail closed, clear the bad record, hide Resume, expose the recovery status, and leave application state unset.
- A real browser run seeds malformed same-origin storage through a temporary local QA page, loads the current build, and verifies the recovery message, hidden Resume control, available start form, cleared storage key, and an empty warning/error console.
- The unchanged valid-state regression still restores a recorded outcome and excludes that check from the next suggestion.

