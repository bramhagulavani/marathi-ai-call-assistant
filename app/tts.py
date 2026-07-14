# tts.py — Text-to-Speech using gTTS (Google Translate TTS, free, no key).
# Converts Marathi text into an audio file and plays it.

import os
import platform

from gtts import gTTS

from . import config


def speak_marathi(text: str, output_filename: str = "reply.mp3", play: bool = True) -> str:
    """
    Converts Marathi text to speech, saves it under data/audio/, optionally
    plays it, and returns the saved file path.
    """
    print(f"[TTS] Converting to speech: {text}")

    output_path = config.AUDIO_OUTPUT_DIR / output_filename
    gTTS(text=text, lang="mr", slow=False).save(str(output_path))
    print(f"[TTS] Audio saved to: {output_path}")

    if play:
        _play_audio(str(output_path))

    return str(output_path)


def _play_audio(file_path: str) -> None:
    system = platform.system()
    print(f"[TTS] Playing audio on {system}...")

    if system == "Windows":
        os.system(f'start "" "{file_path}"')
    elif system == "Darwin":  # macOS
        os.system(f'afplay "{file_path}"')
    elif system == "Linux":
        if os.system("which mpg123 > /dev/null 2>&1") == 0:
            os.system(f'mpg123 -q "{file_path}"')
        elif os.system("which ffplay > /dev/null 2>&1") == 0:
            os.system(f'ffplay -nodisp -autoexit -loglevel quiet "{file_path}"')
        else:
            print("[TTS] Audio saved but no player found. Install mpg123 or ffplay:")
            print("      sudo apt install mpg123")


if __name__ == "__main__":
    speak_marathi(
        "नमस्कार! मी तुमचा मराठी AI सहाय्यक आहे. कृपया आपला निरोप सांगा, मी पोहोचवतो.",
        "test_reply.mp3",
    )
    print("Done.")
