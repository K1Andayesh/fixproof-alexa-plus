# Video v9 QA

Validated 16 September 2026 against the current three-model, nine-path FixProof release.

## Result

- Duration: 2:38.09, below the three-minute competition limit.
- Video: H.264 High, 1920x1080, 30 fps, progressive yuv420p.
- Audio: AAC-LC, 48 kHz mono, natural Australian neural voice (`en-AU-WilliamMultilingualNeural`).
- Loudness analysis: -16.14 LUFS integrated, -1.41 dBFS true peak, 2.00 LU loudness range.
- Captions: 39 embedded open-caption cues plus a separate English (Australia) WebVTT track.
- Full-file decode: passed with FFmpeg `-v error -xerror` and no output.
- Visual review: seven-frame contact sheet plus full-resolution opening and retrieval-evidence frames checked. Counts read 3 exact models, 9 source-backed paths, 29 bounded checks and 48 automated checks.
- The added evidence scene reports the complete controlled result: 254/270 fields and zero critical errors from structured handovers versus 243/270 and five critical errors from equal-fact transcripts across 54 format-blind reads.
- Claims stay bounded: the evidence scene labels the result synthetic, and the closing card states that Alexa device testing and customer validation remain ahead.

## Checksums

- MP4 SHA-256: `6B89DC2FFF7B6F1E07465BED4EFE607B38316D24854E1AE1D1A3C3AC8A61AF2A`
- VTT SHA-256: `1C9F8B3F25252C56646D9B50E9BA8421C7CDB0A52AB09B88446FDC38FF4F35EF`
- Poster SHA-256: `C6ADB3BF68B106A74C61CD6249EF4C978437F09045182AB7E20C09658A5FB44E`

Production browser playback and deployed-file checksum verification are recorded in `RELIABILITY_REVIEW.md` after deployment.
