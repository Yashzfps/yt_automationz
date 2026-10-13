from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from pathlib import Path

from app.database.session import SessionLocal
from app.models import JobStatus, VideoAsset, WorkflowJob
from app.services.captions.caption_service import build_captions
from app.services.captions.srt import segments_to_srt
from app.services.metadata.providers import MetadataProviderError, get_metadata_provider
from app.services.transcription.service import TranscriptionError, transcribe_media

logger = logging.getLogger(__name__)


class JobRunner:
    def __init__(self) -> None:
        self._tasks: dict[int, asyncio.Task] = {}

    def start(self, job_id: int) -> None:
        if job_id in self._tasks and not self._tasks[job_id].done():
            return
        self._tasks[job_id] = asyncio.create_task(self._run(job_id))

    def request_cancel(self, job_id: int) -> None:
        with SessionLocal() as db:
            job = db.get(WorkflowJob, job_id)
            if job:
                job.cancel_requested = True
                db.commit()

    async def _run(self, job_id: int) -> None:
        with SessionLocal() as db:
            job = db.get(WorkflowJob, job_id)
            if not job:
                return
            job.status = JobStatus.running
            job.started_at = datetime.now(UTC)
            job.stage = "transcription"
            db.commit()

        try:
            await self._process(job_id)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Job failed", extra={"job_id": job_id})
            with SessionLocal() as db:
                job = db.get(WorkflowJob, job_id)
                if job:
                    job.status = JobStatus.failed
                    job.error_message = str(exc)
                    job.completed_at = datetime.now(UTC)
                    db.commit()

    async def _process(self, job_id: int) -> None:
        with SessionLocal() as db:
            job = db.get(WorkflowJob, job_id)
            if not job:
                return
            payload = job.payload
            asset_ids = payload.get("asset_ids", [])[: payload.get("quantity", len(payload.get("asset_ids", [])))]

        total = max(len(asset_ids), 1)
        for idx, asset_id in enumerate(asset_ids, start=1):
            with SessionLocal() as db:
                job = db.get(WorkflowJob, job_id)
                if not job:
                    return
                if job.cancel_requested:
                    job.status = JobStatus.cancelled
                    job.stage = "cancelled"
                    job.completed_at = datetime.now(UTC)
                    db.commit()
                    return
                asset = db.get(VideoAsset, asset_id)
                if not asset:
                    continue

            await self._process_asset(job_id, asset_id)

            with SessionLocal() as db:
                job = db.get(WorkflowJob, job_id)
                if job:
                    job.progress = idx / total
                    db.commit()

        with SessionLocal() as db:
            job = db.get(WorkflowJob, job_id)
            if job:
                job.stage = "completed"
                job.status = JobStatus.completed
                job.progress = 1.0
                job.completed_at = datetime.now(UTC)
                db.commit()

    async def _process_asset(self, job_id: int, asset_id: int) -> None:
        with SessionLocal() as db:
            asset = db.get(VideoAsset, asset_id)
            job = db.get(WorkflowJob, job_id)
            if not asset or not job:
                return

            transcript = asset.transcript_text
            segments = asset.transcript_segments or []
            if not transcript:
                try:
                    transcript, segments = transcribe_media(Path(asset.source_path), "auto")
                    asset.transcript_text = transcript
                    asset.transcript_segments = segments
                except TranscriptionError as exc:
                    raise RuntimeError(str(exc)) from exc

            captions = build_captions(transcript)
            asset.captions_text = captions
            job.stage = "captions"
            db.commit()

            if job.payload.get("export_srt", True):
                srt_text = segments_to_srt(segments) if segments else ""
                output_dir = Path("outputs/srt")
                output_dir.mkdir(parents=True, exist_ok=True)
                srt_path = output_dir / f"{asset.id}.srt"
                srt_path.write_text(srt_text, encoding="utf-8")
                asset.srt_path = str(srt_path)

            if job.payload.get("generate_metadata", True):
                provider = get_metadata_provider()
                facts = {
                    "file_name": asset.file_name,
                    "duration_seconds": asset.duration_seconds,
                    "width": asset.width,
                    "height": asset.height,
                }
                try:
                    asset.metadata_json = provider.generate(transcript, facts)
                except MetadataProviderError as exc:
                    raise RuntimeError(str(exc)) from exc

            asset.approval_state = "ready_for_review"
            job.stage = "review"
            db.commit()

        await asyncio.sleep(0)


job_runner = JobRunner()
