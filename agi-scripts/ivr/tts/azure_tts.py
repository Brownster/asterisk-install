"""Stub text-to-speech module."""

from pathlib import Path


def synthesize_speech_to_file(text: str, output_file: str) -> str:
    """Create an empty WAV file to mimic TTS output."""
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    return str(path)
