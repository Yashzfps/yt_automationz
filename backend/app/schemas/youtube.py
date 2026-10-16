from datetime import datetime

from pydantic import BaseModel


class UploadRequest(BaseModel):
    asset_id: int
    privacy_status: str = "private"
    publish_at: datetime | None = None


class UploadResponse(BaseModel):
    record_id: int
    status: str
    youtube_video_id: str | None = None
    error_message: str | None = None
