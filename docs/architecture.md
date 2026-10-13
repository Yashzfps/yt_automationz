# RIN Architecture (Foundation)

- Backend: FastAPI (127.0.0.1), SQLAlchemy 2.x, SQLite persistence, startup recovery for interrupted jobs.
- Workflow stages: discovery -> validation/media info -> transcription -> caption generation -> SRT export -> metadata generation -> review -> upload.
- Caption mode: Roman Hinglish default.
- Metadata providers: deterministic local provider + Ollama adapter (explicitly errors if unavailable).
- YouTube integration: official Google client libraries with OAuth token file usage and resumable upload support.
- Frontend: React + Vite + TypeScript + Tailwind + Framer Motion + Lucide dashboard routes.
- Demo mode: explicit API + UI messaging that no real YouTube publishing occurs.
