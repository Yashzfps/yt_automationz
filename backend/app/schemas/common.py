from datetime import datetime

from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None


class JobSummary(BaseModel):
    id: int
    kind: str
    status: str
    stage: str
    progress: float
    retries: int
    error_message: str | None
    created_at: datetime
