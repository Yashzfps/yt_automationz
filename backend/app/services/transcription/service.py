from __future__ import annotations

from pathlib import Path

from app.core.config import settings


class TranscriptionError(RuntimeError):
    pass


def _load_whisper_model() -> object:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise TranscriptionError(
            "faster-whisper is not installed. Install backend with transcription extras."
        ) from exc

    return WhisperModel(
        settings.whisper_model,
        device=settings.whisper_device,
        compute_type=settings.whisper_compute_type,
    )


def transcribe_media(path: Path, language_mode: str = "auto") -> tuple[str, list[dict]]:
    model = _load_whisper_model()
    language = None if language_mode.lower() == "auto" else language_mode
    try:
        segments, _ = model.transcribe(str(path), language=language)
    except Exception as exc:  # noqa: BLE001
        raise TranscriptionError(f"Transcription failed: {exc}") from exc

    joined: list[str] = []
    structured: list[dict] = []
    for seg in segments:
        txt = seg.text.strip()
        if txt:
            joined.append(txt)
        structured.append({"start": seg.start, "end": seg.end, "text": txt})
    transcript = " ".join(joined).strip()
    if not transcript:
        raise TranscriptionError("Transcription completed but no speech text was produced")
    return transcript, structured
