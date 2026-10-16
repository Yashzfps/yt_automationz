from pydantic import BaseModel, Field


class SourceConfigIn(BaseModel):
    path: str = Field(min_length=1)
    recursive: bool = True


class SourceConfigOut(BaseModel):
    id: int
    path: str
    recursive: bool


class DiagnosticsOut(BaseModel):
    ffmpeg_available: bool
    ffprobe_available: bool
    faster_whisper_available: bool
    ollama_reachable: bool
    youtube_client_secrets_present: bool
    youtube_token_present: bool
    demo_mode: bool
