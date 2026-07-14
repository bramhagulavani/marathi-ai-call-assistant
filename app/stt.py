# stt.py — Speech-to-Text using Whisper (runs locally, free, no API key).
# Converts a Marathi audio file into text.

from functools import lru_cache

from . import config


@lru_cache(maxsize=1)
def _load_model():
    # Cached so the (large) Whisper model is loaded once per process,
    # not once per transcription call.
    import whisper
    print(f"[STT] Loading Whisper model ({config.WHISPER_MODEL_SIZE})...")
    return whisper.load_model(config.WHISPER_MODEL_SIZE)


def transcribe_audio(audio_path: str) -> str:
    """Takes a path to an audio file (mp3/wav/m4a). Returns transcribed Marathi text."""
    model = _load_model()
    print(f"[STT] Transcribing audio: {audio_path}")
    # language="mr" forces Marathi so Whisper doesn't auto-detect wrong language
    result = model.transcribe(audio_path, language="mr")
    text = result["text"].strip()
    print(f"[STT] Transcribed text: {text}")
    return text


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m app.stt <path_to_audio_file>")
    else:
        print(f"\nResult: {transcribe_audio(sys.argv[1])}")
