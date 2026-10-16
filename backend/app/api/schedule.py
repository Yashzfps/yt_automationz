from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.schedule import SchedulePreviewRequest, ScheduleSlot
from app.services.scheduling.planner import build_schedule

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post("/preview", response_model=list[ScheduleSlot])
def preview_schedule(payload: SchedulePreviewRequest) -> list[ScheduleSlot]:
    try:
        slots = build_schedule(
            payload.start_at,
            payload.timezone,
            payload.interval_minutes,
            payload.daily_limit,
            payload.count,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return [ScheduleSlot(index=i + 1, publish_at=slot) for i, slot in enumerate(slots)]
