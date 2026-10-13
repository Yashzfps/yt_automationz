from app.services.captions.caption_service import build_captions


def test_build_caption_roman_hinglish_normalizes_spaces() -> None:
    result = build_captions("  Yeh   test hai  aur   fun hai ")
    assert "aur" in result.lower()
    assert "  " not in result
