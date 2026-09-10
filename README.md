# FixProof

A local voice-first Alexa+ experience simulation for the Amazon Developer Hackathon 2026. FixProof carries a dishwasher issue through source-linked checks, explicit user outcomes and a repair handover. It is an independent prototype, not a live Alexa integration or manufacturer service.

## Try the hosted workflow

Open [the public FixProof evaluation build](https://fixproof-alexa.keyvan-andayesh.chatgpt.site). It uses a fixed source-backed sequence and browser storage so an appliance owner or repair professional can test the core workflow without installing anything. The hosted interface states that it is a simulation and does not run the local AI implementation.

## Run on Windows

Requires Python 3.10+ and a running local Ollama instance with `qwen3.5:4b` already installed. No Python/JavaScript packages or cloud credentials are needed.

```powershell
python fixproof/server.py
```

Open http://127.0.0.1:8768 and choose **Open demonstration case**. Ask for a check, open its source, record an outcome, reload, ask what is next and prepare a handover. The demonstration is fictional and does not establish appliance ownership or a successful repair.

If Ollama is unavailable, case creation, saved records and export still work. AI requests report failure and retain the draft. Start your local Ollama service and retry. Do not change another application's model configuration to run this project.

Optional environment variables: `FIXPROOF_MODEL`, `FIXPROOF_OLLAMA`, `FIXPROOF_PORT`, `FIXPROOF_DATA`. Defaults: `qwen3.5:4b`, `http://127.0.0.1:11434`, `8768`, `fixproof/data`. Keep the provider local unless remote data transfer and cost are approved. No model download is performed by the application.

## Implemented

- Exact reference model Bosch SMS6HAI02A/01; manufacturer manual pages 23, 40 and 41 visually checked.
- Local AI classifies symptoms, then selects from remaining source-backed checks. Server supplies instruction text and citations. Unsupported/unconfirmed models do not receive model-specific checks.
- SQLite history, revision checks and request idempotency. Outcomes, deferred/skipped checks and user-reported resolution remain distinct. Explicitly revisit recorded outcomes to update them.
- Reload/resume, model traces, manufacturer links, handover preview and Markdown download.
- Optional Chrome speech input fills the question for review without submitting it. Browser speech output can read the latest FixProof response aloud. The typed path remains available throughout.
- Loopback binding, Host/Origin checks, bounded requests, parameterized SQL and no arbitrary source URL fetching.

## Verify

```powershell
python -m unittest discover -s fixproof -p test_server.py -v
python fixproof/evaluate.py
node --check fixproof/app.js
```

Live evaluations use the local model and write `validation/LOCAL_AI_EVAL.json`. Tests use an isolated temporary database. See [QA evidence](validation/FIXPROOF_QA.md), [scope](validation/FIXPROOF.md) and [submission draft](submission/DRAFT.md).

## Boundaries

Local, single-user MVP: no authentication, encrypted storage, remote sharing, physical inspection, live Alexa/device integration or customer validation. Do not expose this development server publicly. AI can misclassify novel phrasing; the evaluated set is small. Four checks do not cover the whole manual or prove a repair is needed.

Chrome provides speech recognition and may use its online service; spoken transcripts can therefore leave the computer before FixProof receives them. The UI states this before the microphone control. Speech input never submits automatically. The microphone permission path has not been accepted or end-to-end tested; typed input and spoken playback were browser-tested.

Personal case data in `fixproof/data/` and reference downloads in `tmp/` are ignored. Do not publish these folders. Original brief summaries and source links are included, not a redistributed manual. The source is released under the MIT License.

The `dist/` folder is the transparent hosted evaluation build. It uses a fixed source-backed sequence and browser storage so external testers can assess the workflow without access to the local Ollama service. It identifies that limitation in the interface. No final competition entry has been submitted.
