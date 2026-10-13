from pydantic import BaseModel, Field


class MetadataDraft(BaseModel):
    title_alternatives: list[str] = Field(min_length=3, max_length=3)
    recommended_title: str
    description: str
    hashtags: list[str]
    tags: list[str]
    summary: str
    pinned_comment: str | None = None


class MetadataUpdateRequest(BaseModel):
    metadata: MetadataDraft
