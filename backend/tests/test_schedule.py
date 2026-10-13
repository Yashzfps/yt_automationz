from datetime import UTC, datetime, timedelta

import pytest

from app.services.scheduling.planner import build_schedule


def test_schedule_builds_slots() -> None:
    start = datetime.now(UTC) + timedelta(hours=1)
    slots = build_schedule(start, "UTC", interval_minutes=60, daily_limit=2, count=3)
    assert len(slots) == 3
    assert slots[0] < slots[1]


def test_schedule_rejects_past_time() -> None:
    with pytest.raises(ValueError):
        build_schedule(datetime.now(UTC) - timedelta(hours=1), "UTC", 30, 3, 3)
