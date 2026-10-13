from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import JobStatus, VideoAsset, WorkflowJob
from app.schemas.common import JobSummary
from app.schemas.library import BatchRequest
from app.workers.job_runner import job_runner

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.post("/batch", response_model=JobSummary)
def create_batch(payload: BatchRequest, db: Session = Depends(get_db)) -> JobSummary:
    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    assets = db.scalars(select(VideoAsset).where(VideoAsset.id.in_(payload.asset_ids))).all()
    if not assets:
        raise HTTPException(status_code=400, detail="No valid assets selected")

    job = WorkflowJob(
        kind="batch_process",
        status=JobStatus.pending,
        stage="queued",
        payload=payload.model_dump(),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    job_runner.start(job.id)
    return JobSummary(
        id=job.id,
        kind=job.kind,
        status=job.status.value,
        stage=job.stage,
        progress=job.progress,
        retries=job.retries,
        error_message=job.error_message,
        created_at=job.created_at,
    )


@router.get("/jobs", response_model=list[JobSummary])
def list_jobs(db: Session = Depends(get_db)) -> list[JobSummary]:
    rows = db.scalars(select(WorkflowJob).order_by(WorkflowJob.created_at.desc())).all()
    return [
        JobSummary(
            id=r.id,
            kind=r.kind,
            status=r.status.value,
            stage=r.stage,
            progress=r.progress,
            retries=r.retries,
            error_message=r.error_message,
            created_at=r.created_at,
        )
        for r in rows
    ]


@router.post("/jobs/{job_id}/cancel")
def cancel_job(job_id: int, db: Session = Depends(get_db)) -> dict:
    job = db.get(WorkflowJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.cancel_requested = True
    db.commit()
    job_runner.request_cancel(job_id)
    return {"status": "cancellation_requested", "job_id": job_id}
