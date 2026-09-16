# Video v8 QA

Validated 16 September 2026 against the current three-model, eight-path FixProof release.

## Result

- Duration: 2:15.38, below the three-minute competition limit.
- Video: H.264, 1920x1080, 30 fps, progressive yuv420p.
- Audio: AAC-LC, 48 kHz mono, natural Australian neural voice (`en-AU-WilliamMultilingualNeural`).
- Loudness analysis: -16.13 LUFS integrated, -1.41 dB true peak, 2.10 LU loudness range.
- Captions: embedded open captions plus a separate English (Australia) WebVTT track.
- Full-file decode: passed with FFmpeg `-v error -xerror` and no output.
- Visual review: six-frame contact sheet and full-resolution opening and breadth frames checked. Counts read 3 exact models, 8 source-backed paths, 26 bounded checks and 46 automated checks.
- Claims stay bounded: the closing card states that Alexa device testing and customer validation remain ahead.

## Checksums

- MP4 SHA-256: `0F8D51A8B4CF4B14ACCCB9CBF8380C009BE13D57C0555FF51291207B374A98CC`
- VTT SHA-256: `3983AD1B08C6967E3F5E43A986A839D535EB09A158A2C5C23FBD04276AF55361`
- Poster SHA-256: `1AB8DB7C7315E9DED8FBC143EEC7840F25F165615DE71546CD2FB07466DE776D`

Production browser playback and deployed-file checksum verification are recorded in `RELIABILITY_REVIEW.md` after deployment.

- Local Chrome playback: media reached readyState 4 at 1920x1080, advanced beyond four seconds, displayed captions visibly, and emitted no console warnings or errors.
- WebVTT parser: FFmpeg converted all 33 cue IDs to SRT without error.

