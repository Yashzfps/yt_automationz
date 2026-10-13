from app.services.captions.srt import seconds_to_srt_timestamp, segments_to_srt


def test_seconds_to_srt_timestamp() -> None:
    assert seconds_to_srt_timestamp(0) == "00:00:00,000"
    assert seconds_to_srt_timestamp(61.432) == "00:01:01,432"


def test_segments_to_srt() -> None:
    text = segments_to_srt(
        [
            {"start": 0.0, "end": 1.1, "text": "Hello"},
            {"start": 1.1, "end": 2.5, "text": "World"},
        ]
    )
    assert "00:00:00,000 --> 00:00:01,100" in text
    assert "World" in text
