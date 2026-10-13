from pydantic import BaseModel


class ScanRequest(BaseModel):
    source_ids: list[int]
    recursive_override: bool | None = None


class AssetOut(BaseModel):
    id: int
    source_path: str
    file_name: str
    extension: str
    size_bytes: int
    duration_seconds: float | None
    width: int | None
    height: int | None
    valid: bool
    invalid_reason: str | None
    approval_state: str


class BatchRequest(BaseModel):
    asset_ids: list[int]
    quantity: int
    generate_captions: bool = True
    burn_in: bool = False
    export_srt: bool = True
    generate_metadata: bool = True
    upload_mode: str = "manual"
