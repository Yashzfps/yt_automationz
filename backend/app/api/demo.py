from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/sample")
def sample_records() -> dict:
    now = datetime.now(UTC)
    return {
        "mode": "demo",
        "warning": "Demo mode only. No real publishing or YouTube API calls happen.",
        "videos": [
            {
                "id": 9001,
                "file_name": "demo_short_1.mp4",
                "status": "ready_for_review",
                "estimated_publish": now.isoformat(),
            },
            {
                "id": 9002,
                "file_name": "demo_short_2.mp4",
                "status": "scheduled",
                "estimated_publish": now.isoformat(),
            },
        ],
    }
