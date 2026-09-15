# Current-release demo video verification — 15 September 2026

## Purpose and evidence boundary

This 2:14 walkthrough replaces the stale one-model closing frame with the current three-model, four-path scope and adds the judge-callable public MCP endpoint. It uses edited browser captures, saved public-client evidence, and the selected Australian neural narrator. It does not claim an uncut recording, Alexa device execution, customer validation, appliance inspection, diagnosis, repair success, time savings, or a winning probability.

The narrator remains `en-AU-WilliamMultilingualNeural`, with short sentences and per-scene pacing. Naturalness is subjective and no independent listener preference is claimed.

## Media checks

- File: `dist/fixproof-demo-v4.mp4`
- Duration: 133.856 seconds
- Video: H.264, 1920 by 1080, 30 fps
- Audio: AAC, 48 kHz, mono
- Integrated loudness: -16.1 LUFS; true peak: -1.4 dBFS; loudness range: 2.0 LU
- Full video and audio decode with `ffmpeg -xerror`: passed
- Burned captions: visually present across the nine-scene contact sheet
- WebVTT captions: included as `dist/fixproof-demo-v4.vtt`
- MP4 SHA-256: `53f9489c5fc03a4ebd47079fdbc6070adfd4be1e423786fae4db76008dbd00af`
- WebVTT SHA-256: `52726ef9678d4f6588245434b38a902c34d2d14063c81ad12a605b0d548afa05`
- Poster SHA-256: `7a1351428a32b9d539d31f5d0aa847ed339746bc6afe3b4f5374a1eb0f870b57`

## Content checks

- The breadth scene states three exact models, four source-backed paths, fourteen bounded checks and 38 automated checks.
- The public-MCP scene displays the anonymous HTTPS endpoint, negotiated protocol 2026-07-28, all five tool names, preserved observation, non-repetition and fictional-only status from `validation/HOSTED_MCP.json`.
- The closing frame states the current three-model, four-path scope and retains the Alexa-device and customer-validation limits.
- The earlier journey scenes still demonstrate an exact page citation, explicit fictional outcome, reload/resume, a different remaining check, handover, and safety stop.
- A nine-scene contact sheet was visually inspected. The updated catalog, MCP and closing cards were legible and free of the prior middle-dot encoding defect.

## Publication state

The files are prepared for the public evaluation build. Production publication and browser media playback verification are recorded in `validation/RELIABILITY_REVIEW.md` after deployment.

The Devpost submission and YouTube video still need to be updated together. Those browser actions require action-time confirmation under the Computer Use policy.
