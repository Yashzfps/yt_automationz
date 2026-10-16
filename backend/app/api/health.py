from __future__ import annotations

import shutil
import subprocess

import httpx
from fastapi import APIRouter

from app.core.config import settings
from app.schemas.settings import DiagnosticsOut
from app.services.youtube.client import oauth_status

router = APIRouter(prefix="/health", tags=["health"])


def _is_command_available(command: str) -> bool:
    if shutil.which(command):
        return True
    try:
        subprocess.run([command, "-version"], check=False, capture_output=True)
        return True
    except Exception:  # noqa: BLE001
        return False


def _is_faster_whisper_available() -> bool:
    try:
        import faster_whisper  # noqa: F401

        return True
    except Exception:  # noqa: BLE001
        return False


def _is_ollama_reachable() -> bool:
    try:
        response = httpx.get(f"{settings.ollama_url}/api/tags", timeout=3)
        return response.is_success
    except Exception:  # noqa: BLE001
        return False


@router.get("/ping")
def ping() -> dict:
    return {"status": "ok", "bind": f"{settings.bind_host}:{settings.bind_port}"}


@router.get("/diagnostics", response_model=DiagnosticsOut)
def diagnostics() -> DiagnosticsOut:
    oauth = oauth_status()
    return DiagnosticsOut(
        ffmpeg_available=_is_command_available(settings.ffmpeg_path),
        ffprobe_available=_is_command_available(settings.ffprobe_path),
        faster_whisper_available=_is_faster_whisper_available(),
        ollama_reachable=_is_ollama_reachable(),
        youtube_client_secrets_present=oauth["client_secret_present"],
        youtube_token_present=oauth["token_present"],
        demo_mode=settings.demo_mode,
    )
