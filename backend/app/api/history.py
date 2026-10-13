from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import UploadRecord, WorkflowJob

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/jobs")
def jobs(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.scalars(select(WorkflowJob).order_by(WorkflowJob.created_at.desc())).all()
    return [
        {
            "id": j.id,
            "kind": j.kind,
            "status": j.status.value,
            "stage": j.stage,
            "error": j.error_message,
            "created_at": j.created_at,
            "completed_at": j.completed_at,
        }
        for j in rows
    ]


@router.get("/uploads")
def uploads(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.scalars(select(UploadRecord).order_by(UploadRecord.updated_at.desc())).all()
    return [
        {
            "id": r.id,
            "video_asset_id": r.video_asset_id,
            "status": r.upload_status,
            "youtube_video_id": r.youtube_video_id,
            "error": r.error_message,
            "updated_at": r.updated_at,
        }
        for r in rows
    ]
