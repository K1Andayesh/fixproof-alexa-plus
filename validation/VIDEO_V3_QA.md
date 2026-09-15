# Current-release demo video verification — 15 September 2026

Superseded by `VIDEO_V4_QA.md`; retained as release history.

## Purpose and evidence boundary

This 2:14 walkthrough replaces the stale one-path closing claim in the earlier submitted video with the current four-path product state. It uses edited real browser captures, the production Site 17 start page, a compact excerpt derived from the fresh saved MCP smoke result, and a newly generated Australian neural narration track. It does not claim an uncut recording, Alexa device execution, customer validation, appliance inspection, diagnosis, repair success, time savings, or a winning probability.

The narrator is `en-AU-WilliamMultilingualNeural`, the newer Australian multilingual neural voice available through the installed Edge TTS client. The script uses shorter conversational sentences and per-scene pacing. This is an objective voice and script change from the earlier `en-AU-NatashaNeural` render; naturalness remains subjective and no independent listener preference is claimed.

## Media checks

- File: `dist/fixproof-demo-v3.mp4`
- Duration: 133.665 seconds
- Video: H.264, 1920 by 1080, 30 fps
- Audio: AAC, 48 kHz, mono
- Integrated loudness: -16.12 LUFS; true peak: -1.43 dBTP; loudness range: 2.10 LU
- Full video and audio decode: passed
- Burned captions: visually present in the nine-scene contact sheet
- WebVTT captions: included as `dist/fixproof-demo-v3.vtt`
- MP4 SHA-256: `836c34f8a78ea840be3b8e05e9bf2e3a29c5d0c5a13c7a8a1bc0422bfb290730`
- SRT SHA-256: `85c578d6c4e139dd3c8b866fea0f49c458b2180ec90dc40ee5a7d2fc2b202a30`

## Content checks

- Production start-page capture visibly shows four source-backed paths, 37 automated tests, 13/13 local-AI scenarios, the simulation boundary, and the sourced impact card.
- The walkthrough demonstrates a source-linked check, an explicit fictional outcome, reload and resume, selection of a different remaining check, the repair handover, and the safety stop.
- A separate breadth scene states the current 14-check, four-path scope.
- The MCP scene states Streamable HTTP, five tools, four paths and cross-client continuity. Its visible excerpt matches fields in `validation/RELIABILITY_MCP.json`.
- The closing frame states the one-model scope and identifies Alexa device testing and customer validation as future work.

## Publication state

The current video, poster and captions are embedded in production Site version 18 at https://fixproof-alexa.keyvan-andayesh.chatgpt.site. Deployment `appgdep_6aa8f91761588191817ba3f7f648a15c` succeeded from product commit `aa20c32d55d2cc6a301766313f830a7e475d0153`.

Production Chrome loaded the media at ready state 4 with the expected 133.665-second duration, 1920 by 1080 dimensions and one enabled English (Australia) caption track. Clicking the visible player advanced playback beyond two seconds, and the browser console reported no warnings or errors. The desktop layout kept the poster and start-case form readable without overlap.

The Devpost submission and YouTube video still need to be updated together after the new YouTube upload is complete. Those browser actions require action-time confirmation under the Computer Use policy.
