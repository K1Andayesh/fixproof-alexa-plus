# Video v10 QA

Prepared 17 September 2026 against the deployed four-model FixProof catalog and saved public MCP client trace.

## Result

- Duration: 2:38.87, below the competition's three-minute limit.
- H.264 High, 1920×1080, 30 fps, progressive yuv420p; AAC-LC, 48 kHz mono.
- Natural Australian neural narration: `en-AU-WilliamMultilingualNeural`.
- Measured audio: -16.1 LUFS integrated, -1.4 dBFS true peak, 2.1 LU loudness range.
- Thirty-nine open-caption cues and a separate English (Australia) WebVTT file.
- Full-file decode passed with FFmpeg `-v error -xerror` without an error.
- Opening, four-model catalog, hosted MCP trace and closing frames were inspected at video resolution, including rendered caption placement.

The revised cards distinguish ten paths for three exact Bosch models from eight separately mapped paths for Electrolux ESF8735ROX. The MCP excerpt is derived from `HOSTED_MCP.json` and reports the public endpoint, negotiated protocol, discovered tools, cross-connection observation, non-repeated check and advertised App resource. The recorded browser sequence remains a fictional case; the video does not show Alexa-device execution, repair success or independent customer testing. The controlled retrieval result is expressly synthetic.

## Checksums

- MP4 SHA-256: `2FEF018D2BDB03279CC41D74400DAC0CEA603DF1213DF808602E23365E62D9D2`
- VTT SHA-256: `4F82808F49C759E2DD5C6F4175C4CC3C58CF67D16B1133DEEF6DACFE8098B026`
- Poster SHA-256: `9605A42CE8FE1ADCC191B48165FCC4545991118F6D1CBB3F2BB2B0E7F4C990B3`

The public Sites version 56 deployed on 17 September 2026. Production Chrome loaded the new MP4 at ready state 4 with its English (Australia) track showing; playback advanced beyond 27 seconds and the rendered caption was visible over the video. The deployed MP4, VTT and poster each matched the reviewed local SHA-256 value above. The in-app browser crashed when its native video control was activated, so Chrome was used for the playback check; the production page itself remained available.
