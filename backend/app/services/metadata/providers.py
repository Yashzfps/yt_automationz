from __future__ import annotations

import textwrap
from abc import ABC, abstractmethod

import httpx

from app.core.config import settings


class MetadataProviderError(RuntimeError):
    pass


class BaseMetadataProvider(ABC):
    @abstractmethod
    def generate(self, transcript: str, media_facts: dict) -> dict:
        raise NotImplementedError


class DeterministicMetadataProvider(BaseMetadataProvider):
    def generate(self, transcript: str, media_facts: dict) -> dict:
        stem = media_facts.get("file_name", "video").rsplit(".", 1)[0]
        snippet = " ".join(transcript.split()[:24])
        fallback = f"{stem} short"
        alt = [
            f"{fallback} | quick cut",
            f"{fallback} | behind scenes",
            f"{fallback} | creator update",
        ]
        return {
            "title_alternatives": alt,
            "recommended_title": alt[0],
            "description": textwrap.shorten(snippet or fallback, width=350, placeholder="..."),
            "hashtags": ["#shorts", "#creator", "#rin"],
            "tags": [stem, "shorts", "automation"],
            "summary": textwrap.shorten(snippet or fallback, width=120, placeholder="..."),
            "pinned_comment": "Aapko video kaisa laga? Comment zaroor karein!",
        }


class OllamaMetadataProvider(BaseMetadataProvider):
    def generate(self, transcript: str, media_facts: dict) -> dict:
        prompt = (
            "Generate YouTube Shorts metadata JSON with keys: title_alternatives(3),"
            "recommended_title,description,hashtags,tags,summary,pinned_comment. "
            f"Transcript: {transcript}\nMedia facts: {media_facts}"
        )
        try:
            response = httpx.post(
                f"{settings.ollama_url}/api/generate",
                json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
                timeout=45,
            )
            response.raise_for_status()
            payload = response.json()
            text = payload.get("response", "")
        except Exception as exc:  # noqa: BLE001
            raise MetadataProviderError(f"Ollama provider unavailable: {exc}") from exc

        if not text:
            raise MetadataProviderError("Ollama returned empty response")
        return DeterministicMetadataProvider().generate(transcript, media_facts)


def get_metadata_provider() -> BaseMetadataProvider:
    if settings.metadata_provider.lower() == "ollama":
        return OllamaMetadataProvider()
    return DeterministicMetadataProvider()
