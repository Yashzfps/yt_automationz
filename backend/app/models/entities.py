from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class JobStatus(StrEnum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class VideoSource(Base):
    __tablename__ = "video_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String(1000), unique=True)
    recursive: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class VideoAsset(Base):
    __tablename__ = "video_assets"
    __table_args__ = (UniqueConstraint("fingerprint", name="uq_video_fingerprint"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int | None] = mapped_column(ForeignKey("video_sources.id"), nullable=True)
    source_path: Mapped[str] = mapped_column(String(1200), unique=True)
    fingerprint: Mapped[str] = mapped_column(String(128), index=True)
    file_name: Mapped[str] = mapped_column(String(255))
    extension: Mapped[str] = mapped_column(String(16))
    size_bytes: Mapped[int] = mapped_column(Integer)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    valid: Mapped[bool] = mapped_column(Boolean, default=False)
    invalid_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    transcript_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    transcript_segments: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    captions_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    srt_path: Mapped[str | None] = mapped_column(String(1200), nullable=True)
    rendered_video_path: Mapped[str | None] = mapped_column(String(1200), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    approval_state: Mapped[str] = mapped_column(String(32), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    source: Mapped[VideoSource | None] = relationship()


class WorkflowJob(Base):
    __tablename__ = "workflow_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(32))
    status: Mapped[JobStatus] = mapped_column(SAEnum(JobStatus), default=JobStatus.pending)
    stage: Mapped[str] = mapped_column(String(64), default="queued")
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    retries: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    progress: Mapped[float] = mapped_column(Float, default=0)
    cancel_requested: Mapped[bool] = mapped_column(Boolean, default=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class UploadRecord(Base):
    __tablename__ = "upload_records"
    __table_args__ = (UniqueConstraint("video_asset_id", name="uq_upload_video_asset"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    video_asset_id: Mapped[int] = mapped_column(ForeignKey("video_assets.id"))
    upload_status: Mapped[str] = mapped_column(String(64), default="pending")
    youtube_video_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resumable_session_uri: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    requested_publish_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    privacy_status: Mapped[str] = mapped_column(String(16), default="private")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
