from __future__ import annotations

import json
import subprocess
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import VideoAsset, VideoSource
from app.services.video.fingerprint import file_fingerprint

SUPPORTED_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}


def validate_source_path(path: Path) -> tuple[bool, str | None]:
    if not path.exists():
        return False, "Path does not exist"
    if not path.is_dir():
        return False, "Path is not a directory"
    return True, None


def list_video_files(path: Path, recursive: bool) -> list[Path]:
    pattern = "**/*" if recursive else "*"
    results: list[Path] = []
    for candidate in path.glob(pattern):
        if candidate.is_file() and candidate.suffix.lower() in SUPPORTED_EXTENSIONS:
            results.append(candidate)
    return sorted(results)


def ffprobe_info(path: Path) -> tuple[bool, dict, str | None]:
    cmd = [
        settings.ffprobe_path,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-show_entries",
        "stream=width,height,codec_type",
        "-of",
        "json",
        str(path),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        payload = json.loads(proc.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as exc:
        return False, {}, str(exc)

    duration = None
    if "format" in payload and payload["format"].get("duration"):
        duration = float(payload["format"]["duration"])

    width = None
    height = None
    for stream in payload.get("streams", []):
        if stream.get("codec_type") == "video":
            width = stream.get("width")
            height = stream.get("height")
            break

    return True, {"duration_seconds": duration, "width": width, "height": height}, None


def sync_scan(db: Session, source: VideoSource, recursive: bool | None = None) -> list[VideoAsset]:
    chosen_recursive = source.recursive if recursive is None else recursive
    files = list_video_files(Path(source.path), chosen_recursive)
    discovered: list[VideoAsset] = []
    for file_path in files:
        fp = file_fingerprint(file_path)
        existing = db.scalar(select(VideoAsset).where(VideoAsset.fingerprint == fp))
        if existing:
            discovered.append(existing)
            continue
        valid, media_info, reason = ffprobe_info(file_path)
        asset = VideoAsset(
            source_id=source.id,
            source_path=str(file_path),
            fingerprint=fp,
            file_name=file_path.name,
            extension=file_path.suffix.lower(),
            size_bytes=file_path.stat().st_size,
            duration_seconds=media_info.get("duration_seconds") if valid else None,
            width=media_info.get("width") if valid else None,
            height=media_info.get("height") if valid else None,
            valid=valid,
            invalid_reason=reason,
        )
        db.add(asset)
        db.flush()
        discovered.append(asset)
    db.commit()
    return discovered
