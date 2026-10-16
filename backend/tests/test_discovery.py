from pathlib import Path

from app.services.video.discovery import list_video_files, validate_source_path


def test_validate_source_path(tmp_path: Path) -> None:
    valid, reason = validate_source_path(tmp_path)
    assert valid is True
    assert reason is None


def test_list_video_files_filters_supported_extensions(tmp_path: Path) -> None:
    (tmp_path / "a.mp4").write_bytes(b"x")
    (tmp_path / "b.txt").write_text("x", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.webm").write_bytes(b"y")

    top_only = list_video_files(tmp_path, recursive=False)
    recursive = list_video_files(tmp_path, recursive=True)

    assert len(top_only) == 1
    assert len(recursive) == 2
