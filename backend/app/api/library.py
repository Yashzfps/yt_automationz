from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import VideoAsset, VideoSource
from app.schemas.library import AssetOut, ScanRequest
from app.services.video.discovery import sync_scan

router = APIRouter(prefix="/library", tags=["library"])


@router.post("/scan", response_model=list[AssetOut])
def scan_sources(payload: ScanRequest, db: Session = Depends(get_db)) -> list[AssetOut]:
    assets: list[VideoAsset] = []
    for source_id in payload.source_ids:
        source = db.get(VideoSource, source_id)
        if not source:
            raise HTTPException(status_code=404, detail=f"Source {source_id} not found")
        assets.extend(sync_scan(db, source, payload.recursive_override))

    return [
        AssetOut(
            id=a.id,
            source_path=a.source_path,
            file_name=a.file_name,
            extension=a.extension,
            size_bytes=a.size_bytes,
            duration_seconds=a.duration_seconds,
            width=a.width,
            height=a.height,
            valid=a.valid,
            invalid_reason=a.invalid_reason,
            approval_state=a.approval_state,
        )
        for a in assets
    ]


@router.get("/assets", response_model=list[AssetOut])
def list_assets(db: Session = Depends(get_db)) -> list[AssetOut]:
    rows = db.scalars(select(VideoAsset).order_by(VideoAsset.updated_at.desc())).all()
    return [
        AssetOut(
            id=a.id,
            source_path=a.source_path,
            file_name=a.file_name,
            extension=a.extension,
            size_bytes=a.size_bytes,
            duration_seconds=a.duration_seconds,
            width=a.width,
            height=a.height,
            valid=a.valid,
            invalid_reason=a.invalid_reason,
            approval_state=a.approval_state,
        )
        for a in rows
    ]
