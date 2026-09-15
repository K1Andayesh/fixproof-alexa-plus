# FixProof video v7 QA

Verified 16 September 2026.

- Purpose: judge walkthrough for the current three-model, seven-path release.
- Visible claims: 3 exact models, 7 source-backed paths, 23 bounded checks, 44 automated checks, and 16 live local-AI scenarios.
- Narration: `en-AU-WilliamMultilingualNeural`, delivered as a conversational Australian voice.
- Runtime: 135.77 seconds (2:15), 1920 by 1080.
- Captions: English (Australia) WebVTT track, embedded on the public evaluation page.
- Full-file FFmpeg decode: passed with `-xerror` and no decode errors.
- Audio measurement: -16.1 LUFS integrated, -1.4 dBFS true peak, 1.9 LU loudness range.
- SHA-256: `72D8EE663B45655477B71A9A33C33BD33917C9DB06180BCB691D71EB8E7BB027`.
- Visual inspection: opening, breadth, public-MCP and closing frames were checked at 1920 by 1080. The final MCP frame visibly says `Seven issue paths`; text remains inside the frame.
- Evidence boundary: every case shown is fictional. The closing frame says that Alexa device testing and customer validation remain ahead.

Local release Chrome loaded the v7 media, showed the English captions and visibly advanced playback to six seconds. The opening frame showed the current 3-model, 7-path and 23-check scope without overlap. Production verification is recorded after deployment in `RELIABILITY_REVIEW.md`.
