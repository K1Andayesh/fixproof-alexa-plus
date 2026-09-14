# Revised demo and hazard-flow verification

Observed 14 September 2026 using actual Chrome interactions and fictional cases.

## Defect found during recording

The hosted question form was hidden while a check was pending. Scenario shortcuts still wrote to that hidden field, making the Safety shortcut appear unresponsive. The old hazard path also left a pending check in state and omitted the hazard report from the handover.

## Corrected behavior observed in the local browser

1. Start a fictional drying case and ask for the first check.
2. While Allow drying to finish is pending, choose Safety. The visible question field contains the smoke/electrical-smell report.
3. Submit. The pending check and outcome form disappear; Stop using the appliance appears; further troubleshooting controls are disabled.
4. Reload and resume. The warning and stopped state remain, with zero outcomes recorded.
5. Preview the handover. Status is Handover ready, no outcomes are invented, and the Safety report preserves the exact reported hazard.

The code also checks the initial issue for a hazard. That entry path is separate from the pending-check sequence above.

## Runtime and video evidence

A fresh MCP client run negotiated protocol 2026-07-28, discovered all five workflow tools, selected waiting, recorded Not yet tested, and returned handover_contains_observation=true. The demo identifies this as captured client output, distinct from the guided browser simulation.

The replacement video uses edited actual browser captures, an Australian synthetic narrator, timed captions, and a clearly labelled revised local safety scene. It does not claim an uncut recording, Alexa device execution, customer validation, fault diagnosis, or a successful repair. Full video/audio decode completed successfully at 1920 by 1080, 30 fps, approximately 2 minutes 24 seconds.

This is workflow verification, not physical appliance safety certification or evidence from external users.
