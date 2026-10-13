from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import demo, health, history, library, metadata, schedule, settings, workflow, youtube
from app.core.config import settings as app_settings
from app.core.logging import configure_logging
from app.database.init_db import initialize_database, recover_jobs_on_startup

configure_logging()

app = FastAPI(title="RIN API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(settings.router)
app.include_router(library.router)
app.include_router(workflow.router)
app.include_router(metadata.router)
app.include_router(schedule.router)
app.include_router(youtube.router)
app.include_router(history.router)
app.include_router(demo.router)


@app.on_event("startup")
def startup() -> None:
    initialize_database()
    recover_jobs_on_startup()
    app_settings.storage_dir.mkdir(parents=True, exist_ok=True)
    app_settings.output_dir.mkdir(parents=True, exist_ok=True)
