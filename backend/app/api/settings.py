from __future__ import annotations

import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import VideoSource
from app.schemas.settings import SourceConfigIn, SourceConfigOut
from app.services.video.discovery import validate_source_path
from app.services.youtube.client import oauth_status, revoke_token

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/sources", response_model=list[SourceConfigOut])
def list_sources(db: Session = Depends(get_db)) -> list[SourceConfigOut]:
    rows = db.scalars(select(VideoSource).order_by(VideoSource.id.desc())).all()
    return [SourceConfigOut(id=s.id, path=s.path, recursive=s.recursive) for s in rows]


@router.post("/sources", response_model=SourceConfigOut)
def add_source(payload: SourceConfigIn, db: Session = Depends(get_db)) -> SourceConfigOut:
    source_path = Path(payload.path).expanduser()
    valid, reason = validate_source_path(source_path)
    if not valid:
        raise HTTPException(status_code=400, detail=reason)
    existing = db.scalar(select(VideoSource).where(VideoSource.path == str(source_path)))
    if existing:
        return SourceConfigOut(id=existing.id, path=existing.path, recursive=existing.recursive)
    source = VideoSource(path=str(source_path), recursive=payload.recursive)
    db.add(source)
    db.commit()
    db.refresh(source)
    return SourceConfigOut(id=source.id, path=source.path, recursive=source.recursive)


@router.post("/sources/windows-picker")
def windows_folder_picker() -> dict:
    if os.name != "nt":
        raise HTTPException(status_code=400, detail="Native folder picker only supported on Windows")
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    selected = filedialog.askdirectory()
    root.destroy()
    if not selected:
        raise HTTPException(status_code=400, detail="No folder selected")
    return {"selected_path": selected}


@router.get("/youtube/oauth-status")
def get_oauth_status() -> dict:
    return oauth_status()


@router.post("/youtube/disconnect")
def disconnect_youtube() -> dict:
    removed = revoke_token()
    return {"disconnected": removed}
