# RIN - Local AI YouTube Shorts Automation Studio

RIN is a **Windows-first local desktop-style workflow** (served locally via FastAPI + React) for managing YouTube Shorts production: folder discovery, local transcription, Roman Hinglish captions, metadata drafting, upload queueing, and scheduling.

> This repository now provides a runnable end-to-end foundation with truthful diagnostics. If models, ffmpeg, OAuth credentials, or APIs are missing, RIN reports configuration issues instead of fake success.

## Current foundation capabilities

- Local backend on `127.0.0.1:8787` with persistent SQLite state.
- Source folder configuration (multi-source) + recursive media scan for `mp4/mov/mkv/webm`.
- FFprobe-based validation/media facts collection.
- Fingerprint-based duplicate prevention.
- Persistent batch jobs with startup recovery of interrupted jobs.
- Local transcription integration path via `faster-whisper` (errors clearly if unavailable).
- Default Roman Hinglish caption generation.
- SRT export generation.
- Metadata generation interface:
  - deterministic local provider
  - Ollama provider integration path (configured through env)
- YouTube integration path through **official** Google APIs and resumable uploads.
- Scheduling preview API with timezone, interval, and daily limit validation.
- Frontend dashboard routes:
  - Overview
  - Video Library
  - Caption Studio
  - AI Metadata
  - Upload Queue
  - Schedule Calendar
  - Published Videos
  - History and Logs
  - Settings
- Explicit demo mode endpoint and UI messaging.

## What is intentionally not faked

- No fake upload success without valid Google OAuth/API configuration.
- No fake transcription if `faster-whisper` is unavailable.
- No silent skipping when ffmpeg/ffprobe/Ollama are missing.

## Prerequisites (Windows)

1. Python 3.11+
2. Node.js 20+
3. FFmpeg/FFprobe available on PATH
4. Optional:
   - `faster-whisper` model/runtime support
   - Ollama running locally for LLM metadata
   - Google Cloud OAuth credentials for YouTube uploads

## Setup

```powershell
# from repository root
./scripts/install.ps1
./scripts/check_environment.ps1
```

Copy and edit env values:

```powershell
copy .env.example .env
```

## Run

```powershell
./scripts/start.ps1
```

- Frontend: http://127.0.0.1:5173
- Backend: http://127.0.0.1:8787

## Backend commands

```powershell
cd backend
..\.venv\Scripts\python -m pytest
..\.venv\Scripts\python -m ruff check app tests
```

## Frontend commands

```powershell
cd frontend
npm run typecheck
npm run lint
npm run build
```

## OAuth / YouTube notes

- Uses official YouTube Data API v3 client flow only.
- Keep `client_secret.json` and token files under `./secrets` (gitignored).
- Unverified OAuth projects may be restricted by Google (use private/manual fallback where needed).

## Security & privacy

- Local-first processing.
- Secrets, tokens, local databases, outputs, and logs are ignored by `.gitignore`.
- No credential placeholders with live secrets are committed.

## Troubleshooting quick checks

- `GET /health/diagnostics` reports ffmpeg/ffprobe/model/provider/OAuth presence.
- If transcription fails, install transcription extras and ensure model availability.
- If upload fails, verify Google client secret + token and API enablement.

## Clean start

To reset local state, delete local runtime artifacts only (never committed):

- `rin.db`
- `storage/`
- `outputs/`
- `secrets/youtube_token.json`

## Limitations in this foundation

- This is a production-minded foundation, not a packaged native `.exe` yet.
- Windows native folder picker endpoint is available only when backend runs on Windows.
- Caption burn-in renderer is not yet enabled in this baseline (SRT export is implemented).

## Future improvements

- Native desktop packaging
- Rich caption timeline editor
- Thumbnail extraction & management
- Smarter transcript-based quality scoring and batch guardrails
