from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import VideoAsset
from app.schemas.metadata import MetadataUpdateRequest

router = APIRouter(prefix="/metadata", tags=["metadata"])


@router.get("/{asset_id}")
def get_metadata(asset_id: int, db: Session = Depends(get_db)) -> dict:
    asset = db.get(VideoAsset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"asset_id": asset_id, "metadata": asset.metadata_json}


@router.put("/{asset_id}")
def update_metadata(asset_id: int, payload: MetadataUpdateRequest, db: Session = Depends(get_db)) -> dict:
    asset = db.get(VideoAsset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    asset.metadata_json = payload.metadata.model_dump()
    asset.approval_state = "metadata_approved"
    db.commit()
    return {"asset_id": asset_id, "status": "updated"}
