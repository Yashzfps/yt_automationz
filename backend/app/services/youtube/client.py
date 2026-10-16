from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC
from pathlib import Path

from app.core.config import settings


class YoutubeUnavailableError(RuntimeError):
    pass


@dataclass
class UploadResult:
    status: str
    video_id: str | None = None
    error: str | None = None


def _require_google_deps() -> tuple[object, object, object]:
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise YoutubeUnavailableError(
            "Google API dependencies missing. Install backend with youtube extras."
        ) from exc
    return Request, Credentials, build


def oauth_status() -> dict:
    secrets = settings.youtube_client_secrets_path.exists()
    token = settings.youtube_token_path.exists()
    return {"client_secret_present": secrets, "token_present": token}


def revoke_token() -> bool:
    if settings.youtube_token_path.exists():
        settings.youtube_token_path.unlink()
        return True
    return False


def upload_video(file_path: Path, metadata: dict, privacy_status: str, publish_at=None) -> UploadResult:
    if settings.demo_mode:
        return UploadResult(status="demo-complete", video_id=f"demo_{file_path.stem}")

    Request, Credentials, build = _require_google_deps()
    if not settings.youtube_client_secrets_path.exists():
        raise YoutubeUnavailableError("Google OAuth client secret not configured")
    if not settings.youtube_token_path.exists():
        raise YoutubeUnavailableError("YouTube OAuth token not found. Connect account in settings.")

    creds = Credentials.from_authorized_user_file(str(settings.youtube_token_path))
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            settings.youtube_token_path.write_text(creds.to_json(), encoding="utf-8")
        else:
            raise YoutubeUnavailableError("OAuth token invalid and cannot be refreshed")

    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": metadata.get("recommended_title", file_path.stem),
            "description": metadata.get("description", ""),
            "tags": metadata.get("tags", []),
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": privacy_status,
        },
    }
    if publish_at:
        body["status"]["publishAt"] = publish_at.astimezone(UTC).isoformat().replace("+00:00", "Z")

    try:
        from googleapiclient.http import MediaFileUpload

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=MediaFileUpload(str(file_path), resumable=True),
        )
        response = None
        while response is None:
            _, response = request.next_chunk()
        return UploadResult(status="completed", video_id=response.get("id"))
    except Exception as exc:  # noqa: BLE001
        return UploadResult(status="failed", error=str(exc))
