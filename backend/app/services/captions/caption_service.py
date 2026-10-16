from __future__ import annotations

import re


def to_roman_hinglish(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    replacements = {
        " हूँ ": " hu ",
        " हैं ": " hain ",
        " और ": " aur ",
        " नहीं ": " nahi ",
    }
    padded = f" {normalized.lower()} "
    for src, dst in replacements.items():
        padded = padded.replace(src, dst)
    return padded.strip().capitalize()


def build_captions(transcript: str, mode: str = "roman_hinglish") -> str:
    if mode == "roman_hinglish":
        return to_roman_hinglish(transcript)
    return transcript
