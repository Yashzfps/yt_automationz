from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import UploadRecord, VideoAsset
from app.schemas.youtube import UploadRequest, UploadResponse
from app.services.youtube.client import YoutubeUnavailableError, upload_video

router = APIRouter(prefix="/youtube", tags=["youtube"])


@router.post("/upload", response_model=UploadResponse)
def upload(payload: UploadRequest, db: Session = Depends(get_db)) -> UploadResponse:
    asset = db.get(VideoAsset, payload.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    existing = db.scalar(select(UploadRecord).where(UploadRecord.video_asset_id == asset.id))
    if existing and existing.youtube_video_id:
        return UploadResponse(
            record_id=existing.id,
            status=existing.upload_status,
            youtube_video_id=existing.youtube_video_id,
            error_message=existing.error_message,
        )

    record = existing or UploadRecord(video_asset_id=asset.id, privacy_status=payload.privacy_status)
    if not existing:
        db.add(record)
        db.flush()

    record.requested_publish_at = payload.publish_at
    record.upload_status = "uploading"
    db.commit()

    try:
        result = upload_video(Path(asset.source_path), asset.metadata_json or {}, payload.privacy_status, payload.publish_at)
    except YoutubeUnavailableError as exc:
        record.upload_status = "failed"
        record.error_message = str(exc)
        db.commit()
        return UploadResponse(record_id=record.id, status=record.upload_status, error_message=record.error_message)

    record.upload_status = result.status
    record.youtube_video_id = result.video_id
    record.error_message = result.error
    db.commit()

    return UploadResponse(
        record_id=record.id,
        status=record.upload_status,
        youtube_video_id=record.youtube_video_id,
        error_message=record.error_message,
    )
