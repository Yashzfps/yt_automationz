from app.services.metadata.providers import DeterministicMetadataProvider


def test_deterministic_provider_shape() -> None:
    provider = DeterministicMetadataProvider()
    data = provider.generate("This is a transcript", {"file_name": "sample.mp4"})
    assert len(data["title_alternatives"]) == 3
    assert data["recommended_title"]
    assert isinstance(data["hashtags"], list)
