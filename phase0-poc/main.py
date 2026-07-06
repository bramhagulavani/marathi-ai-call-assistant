# main.py — Phase 0 Entry Point
# Chains STT → LLM → TTS into a working Marathi AI conversation loop
# This is the full proof-of-concept — run this file to test everything together

import os
import time
from stt import transcribe_audio
from llm import get_marathi_reply
from tts import speak_marathi

# ---------------------------------------------------------------------------
# MODE SELECTION
# ---------------------------------------------------------------------------
# Phase 0 supports two modes:
#
# MODE 1 — AUDIO FILE MODE (default)
#   Provide a recorded Marathi audio file as input (mp3/wav/m4a)
#   Good for testing with pre-recorded clips
#
# MODE 2 — TEXT MODE (simpler, for quick testing without audio)
#   Type what the "caller" says as text directly in the terminal
#   Skips STT, tests LLM + TTS only
# ---------------------------------------------------------------------------

def run_audio_mode(audio_file: str):
    """
    Full pipeline: audio file → STT → LLM → TTS → spoken reply
    Simulates a single exchange with a caller.
    """
    print("\n" + "="*55)
    print("   MARATHI AI CALL ASSISTANT — PHASE 0 DEMO")
    print("="*55)

    # Step 1: Play a greeting first
    print("\n[STEP 1] AI greets the caller...")
    greeting = "नमस्कार! मी एक स्वयंचलित मराठी सहाय्यक आहे. ते सध्या उपलब्ध नाहीत. कृपया आपला निरोप सांगा."
    speak_marathi(greeting, "greeting.mp3")
    time.sleep(1)

    # Step 2: Transcribe what the caller said
    print(f"\n[STEP 2] Transcribing caller audio: {audio_file}")
    caller_text = transcribe_audio(audio_file)

    # Step 3: Generate AI reply in Marathi
    print("\n[STEP 3] Generating Marathi reply...")
    ai_reply = get_marathi_reply(caller_text)

    # Step 4: Convert reply to speech and play it
    print("\n[STEP 4] Speaking the reply...")
    speak_marathi(ai_reply, "ai_reply.mp3")

    # Step 5: Print summary
    print("\n" + "="*55)
    print("CALL SUMMARY")
    print("="*55)
    print(f"Caller said : {caller_text}")
    print(f"AI replied  : {ai_reply}")
    print("="*55)


def run_text_mode():
    """
    Text-only mode: type caller's words → LLM → TTS spoken reply
    Good for testing the AI conversation quality without audio files.
    Runs as a loop (multi-turn conversation) until you type 'exit'
    """
    print("\n" + "="*55)
    print("   MARATHI AI CALL ASSISTANT — TEXT MODE")
    print("   (Type what the caller says, AI replies in Marathi)")
    print("   Type 'exit' to end the call")
    print("="*55)

    # Play greeting
    greeting = "नमस्कार! मी एक स्वयंचलित मराठी सहाय्यक आहे. ते सध्या उपलब्ध नाहीत. कृपया आपला निरोप सांगा."
    print(f"\nAI Greeting: {greeting}")
    speak_marathi(greeting, "greeting.mp3")

    conversation_history = []

    while True:
        print()
        caller_input = input("Caller (type in Marathi or English): ").strip()

        if caller_input.lower() in ["exit", "bye", "बाय", "ठीक आहे"]:
            farewell = "धन्यवाद! मी हा निरोप पोहोचवतो. नमस्कार!"
            print(f"\nAI: {farewell}")
            speak_marathi(farewell, "farewell.mp3")
            break

        if not caller_input:
            continue

        # Get AI reply
        ai_reply = get_marathi_reply(caller_input, conversation_history)

        # Store conversation for context
        conversation_history.append({"role": "user", "text": caller_input})
        conversation_history.append({"role": "model", "text": ai_reply})

        # Speak the reply
        print(f"\nAI: {ai_reply}")
        speak_marathi(ai_reply, "ai_reply.mp3")

    # Print full conversation summary
    print("\n" + "="*55)
    print("FULL CONVERSATION SUMMARY")
    print("="*55)
    for i, msg in enumerate(conversation_history):
        role = "Caller" if msg["role"] == "user" else "AI"
        print(f"{role}: {msg['text']}")
    print("="*55)


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    # Check Gemini API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("\n ERROR: GEMINI_API_KEY is not set!")
        print("  Please set it like this:")
        print("  Windows  → set GEMINI_API_KEY=your_key_here")
        print("  Mac/Linux → export GEMINI_API_KEY=your_key_here")
        print("\n  Get your free key at: https://aistudio.google.com/apikey")
        sys.exit(1)

    # Choose mode based on argument
    if len(sys.argv) > 1:
        # Audio file provided — run full pipeline
        audio_path = sys.argv[1]
        if not os.path.exists(audio_path):
            print(f"ERROR: Audio file not found: {audio_path}")
            sys.exit(1)
        run_audio_mode(audio_path)
    else:
        # No file provided — run text mode
        print("\nNo audio file provided. Starting in TEXT MODE.")
        print("Tip: To use audio mode, run:  python main.py your_audio.wav")
        run_text_mode()