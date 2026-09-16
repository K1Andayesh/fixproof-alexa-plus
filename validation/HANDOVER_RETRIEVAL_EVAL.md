# Controlled handover retrieval evaluation

Captured 16 September 2026. This evaluation asks whether a reader can recover case facts from FixProof's structured handover more reliably than from an ordinary chronological transcript.

## Result

| Format | Blind reads | Correct fields | Field accuracy | Critical errors |
| --- | ---: | ---: | ---: | ---: |
| Ordinary transcript | 24 | 215 / 240 | 89.6% | 5 |
| FixProof structured handover | 24 | 230 / 240 | 95.8% | 0 |

In this controlled synthetic run, the structured handover improved exact fact retrieval by 15 of 240 scored fields and eliminated the five critical errors made from the transcript. Two transcript errors lost or changed an explicit safety report; three incorrectly classified a deferred or pending check as performed.

The advantage was not universal. The handover scored higher for the drying, detergent, safety-stop, rust and clouding cases, lower for the food-remnant and wash-noise cases, and tied for odour. The aggregate result supports the evidence structure's value while showing that format alone does not guarantee better retrieval on every case.

This supports a narrow claim: for these fictional cases and local readers, FixProof's structure made the recorded facts easier to retrieve accurately. It does not establish customer impact, comprehension by people, time saved, a successful repair or reduced waste.

## Method

- Eight fictional cases cover performed, deferred, skipped, pending and safety-stop evidence across all eight implemented issue paths.
- Each case is expressed in two formats containing the same ten scored facts: an ordinary chronological transcript and the actual Markdown returned by `fixproof.server.handover`.
- Three independent local model families read every case and format: `qwen3.5:9b`, `gemma3:12b-it-qat` and `gpt-oss:20b`.
- The readers receive the same format-neutral extraction prompt, JSON schema, temperature 0 and seed 42. They are not told which format is FixProof output.
- GPT-OSS uses its required low reasoning mode; Qwen and Gemma use reasoning disabled. Every result records that runtime setting alongside its token counts and latency.
- Ten fields are scored per read: reported issue, model, reference match, performed checks, deferred checks, pending check, safety report, diagnosis status, resolution status and cited pages.
- A critical error is an invented diagnosis, invented resolution, a deferred or pending check reported as performed, or loss of an explicit safety report.

The full prompts, inputs, extracted outputs, per-field scores, model digests and runtimes are in [`HANDOVER_RETRIEVAL_EVAL.json`](HANDOVER_RETRIEVAL_EVAL.json). Reproduce the run with:

```powershell
python validation/evaluate_handover_retrieval.py
```

The script requires a local Ollama service and the two named reader models. Model output can vary with runtime or model versions. This is one pre-declared synthetic suite, not an independent evaluation or statistical study.
