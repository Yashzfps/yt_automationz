from __future__ import annotations


def seconds_to_srt_timestamp(value: float) -> str:
    millis = int(round(value * 1000))
    hours = millis // 3_600_000
    millis %= 3_600_000
    minutes = millis // 60_000
    millis %= 60_000
    seconds = millis // 1000
    millis %= 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


def segments_to_srt(segments: list[dict]) -> str:
    rows: list[str] = []
    for idx, segment in enumerate(segments, start=1):
        rows.append(str(idx))
        rows.append(
            f"{seconds_to_srt_timestamp(float(segment['start']))} --> "
            f"{seconds_to_srt_timestamp(float(segment['end']))}"
        )
        rows.append(str(segment["text"]).strip())
        rows.append("")
    return "\n".join(rows).strip() + "\n"
