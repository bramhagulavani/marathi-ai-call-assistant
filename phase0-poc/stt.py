# stt.py — Speech-to-Text using Whisper (runs locally, completely free)
# Converts Marathi audio file into text

import whisper

def transcribe_audio(audio_path: str) -> str:
    """
    Takes the path to an audio file (mp3/wav/m4a etc.)
    Returns the transcribed Marathi text as a string.
    """
    print("[STT] Loading Whisper model...")
    # 'medium' model gives the best balance between speed and Marathi accuracy
    # Options: tiny, base, small, medium, large (larger = more accurate but slower)
    model = whisper.load_model("medium")

    print(f"[STT] Transcribing audio: {audio_path}")
    # force language to Marathi so Whisper doesn't auto-detect wrong language
    result = model.transcribe(audio_path, language="mr")

    transcribed_text = result["text"].strip()
    print(f"[STT] Transcribed Text: {transcribed_text}")
    return transcribed_text


# Quick test — run this file directly to test STT alone
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python stt.py <path_to_audio_file>")
        print("Example: python stt.py test_audio.wav")
    else:
        text = transcribe_audio(sys.argv[1])
        print(f"\nResult: {text}")