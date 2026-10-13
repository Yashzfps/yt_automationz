from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "RIN"
    environment: str = "local"
    bind_host: str = "127.0.0.1"
    bind_port: int = 8787
    database_url: str = "sqlite:///./rin.db"
    storage_dir: Path = Field(default=Path("./storage"))
    output_dir: Path = Field(default=Path("./outputs"))
    ffmpeg_path: str = "ffmpeg"
    ffprobe_path: str = "ffprobe"

    whisper_enabled: bool = True
    whisper_model: str = "small"
    whisper_device: str = "auto"
    whisper_compute_type: str = "int8"
    transcription_concurrency: int = 1

    metadata_provider: str = "deterministic"
    ollama_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.1:8b"

    youtube_client_secrets_path: Path = Field(default=Path("./secrets/client_secret.json"))
    youtube_token_path: Path = Field(default=Path("./secrets/youtube_token.json"))

    demo_mode: bool = False


settings = Settings()
