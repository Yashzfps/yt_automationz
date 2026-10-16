from datetime import datetime

from pydantic import BaseModel, Field


class SchedulePreviewRequest(BaseModel):
    start_at: datetime
    timezone: str
    interval_minutes: int = Field(ge=1)
    daily_limit: int = Field(ge=1)
    count: int = Field(ge=1)


class ScheduleSlot(BaseModel):
    index: int
    publish_at: datetime
