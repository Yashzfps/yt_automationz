from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def build_schedule(
    start_at,
    timezone_name: str,
    interval_minutes: int,
    daily_limit: int,
    count: int,
):
    tz = ZoneInfo(timezone_name)
    cursor = start_at.astimezone(tz)
    if cursor <= datetime.now(tz=tz):
        raise ValueError("Start time must be in the future")

    slots = []
    day_count = 0
    while len(slots) < count:
        slots.append(cursor)
        day_count += 1
        if day_count >= daily_limit:
            next_day = (cursor + timedelta(days=1)).replace(hour=cursor.hour, minute=cursor.minute)
            cursor = next_day
            day_count = 0
        else:
            cursor = cursor + timedelta(minutes=interval_minutes)
    return slots
