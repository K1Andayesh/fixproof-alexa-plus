# Controlled handover retrieval evaluation

Captured 15 September 2026. This evaluation asks whether a reader can recover case facts from FixProof's structured handover more reliably than from an ordinary chronological transcript.

## Result

| Format | Blind reads | Correct fields | Field accuracy | Critical errors |
| --- | ---: | ---: | ---: | ---: |
| Ordinary transcript | 8 | 71 / 80 | 88.8% | 2 |
| FixProof structured handover | 8 | 76 / 80 | 95.0% | 0 |

In this controlled synthetic run, the structured handover improved exact fact retrieval by 5 of 80 scored fields and eliminated the two critical errors made from the transcript. Both transcript critical errors occurred in the safety-stop case, where a reader lost or changed the explicit safety report.

This supports a narrow claim: for these fictional cases and local readers, FixProof's structure made the recorded facts easier to retrieve accurately. It does not establish customer impact, comprehension by people, time saved, a successful repair or reduced waste.

## Method

- Four fictional cases cover performed, deferred, skipped, pending and safety-stop evidence across all four implemented issue paths.
- Each case is expressed in two formats containing the same ten scored facts: an ordinary chronological transcript and the actual Markdown returned by `fixproof.server.handover`.
- Two independent local model families read every case and format: `qwen3.5:9b` and `gemma3:12b-it-qat`.
- The readers receive the same format-neutral extraction prompt, JSON schema, temperature 0 and seed 42. They are not told which format is FixProof output.
- Ten fields are scored per read: reported issue, model, reference match, performed checks, deferred checks, pending check, safety report, diagnosis status, resolution status and cited pages.
- A critical error is an invented diagnosis, invented resolution, a deferred or pending check reported as performed, or loss of an explicit safety report.

The full prompts, inputs, extracted outputs, per-field scores, model digests and runtimes are in [`HANDOVER_RETRIEVAL_EVAL.json`](HANDOVER_RETRIEVAL_EVAL.json). Reproduce the run with:

```powershell
python validation/evaluate_handover_retrieval.py
```

The script requires a local Ollama service and the two named reader models. Model output can vary with runtime or model versions. This is one pre-declared synthetic suite, not an independent evaluation or statistical study.
