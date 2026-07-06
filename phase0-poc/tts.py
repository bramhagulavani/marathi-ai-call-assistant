# tts.py — Text-to-Speech using gTTS (Google Translate TTS, completely free)
# Converts Marathi text into an audio file and plays it

from gtts import gTTS
import os
import platform

def speak_marathi(text: str, output_file: str = "reply.mp3") -> str:
    """
    Takes a Marathi text string.
    Converts it to speech and saves it as an mp3 file.
    Also plays the audio automatically.
    Returns the path to the saved audio file.
    """
    print(f"[TTS] Converting to speech: {text}")

    # Create Marathi TTS audio
    tts = gTTS(text=text, lang="mr", slow=False)
    tts.save(output_file)
    print(f"[TTS] Audio saved to: {output_file}")

    # Play the audio automatically based on OS
    play_audio(output_file)

    return output_file


def play_audio(file_path: str):
    """
    Plays an audio file.
    Works on Windows, Mac, and Linux automatically.
    """
    system = platform.system()
    print(f"[TTS] Playing audio on {system}...")

    if system == "Windows":
        os.system(f"start {file_path}")
    elif system == "Darwin":   # macOS
        os.system(f"afplay {file_path}")
    elif system == "Linux":
        # Try multiple players in order of availability
        if os.system("which mpg123 > /dev/null 2>&1") == 0:
            os.system(f"mpg123 -q {file_path}")
        elif os.system("which ffplay > /dev/null 2>&1") == 0:
            os.system(f"ffplay -nodisp -autoexit -loglevel quiet {file_path}")
        else:
            print("[TTS] Audio file saved. Install mpg123 or ffplay to auto-play.")
            print(f"      Run: sudo apt install mpg123")


# Quick test — run this file directly to test TTS alone
if __name__ == "__main__":
    test_text = "नमस्कार! मी तुमचा मराठी AI सहाय्यक आहे. कृपया आपला निरोप सांगा, मी पोहोचवतो."
    speak_marathi(test_text, "test_reply.mp3")
    print("Done! Check test_reply.mp3")