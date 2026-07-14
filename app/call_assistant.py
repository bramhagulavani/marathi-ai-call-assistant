# call_assistant.py — Unified call loop.
#
# This merges what used to be two separate, diverging entry points
# (phase0-poc/main.py and phase1-conversation-logic/main.py) into one
# flow: greet -> converse turn by turn -> classify early -> use the
# right call-type prompt -> re-classify periodically -> on end, run a
# final classification and save/print a structured summary.
#
# The first caller turn can optionally come from an audio file (Whisper
# STT); every turn after that is typed, matching how the original text
# mode worked. This keeps both original "modes" as one coherent call
# instead of two separate demos with duplicated loop logic.

import os

from .classifier import classify_call
from .conversation import get_smart_reply
from .stt import transcribe_audio
from .summary import generate_summary, print_summary
from .tts import speak_marathi

GREETING = "नमस्कार! मी एक स्वयंचलित मराठी सहाय्यक आहे. ते सध्या उपलब्ध नाहीत. कृपया आपला निरोप सांगा, मी त्यांना कळवेन."
FAREWELL = "धन्यवाद! मी हा निरोप त्यांना नक्की पोहोचवेन. नमस्कार!"
EXIT_WORDS = {"exit", "bye", "बाय", "ठीक आहे", "धन्यवाद"}
RECLASSIFY_EVERY_N_TURNS = 3


def _detect_call_type_early(conversation_history: list) -> str:
    """After enough turns exist, run a quick classification pass."""
    if len(conversation_history) >= 2:
        return classify_call(conversation_history).get("call_type", "unknown")
    return "unknown"


def run_call(first_audio_file: str | None = None, caller_number: str = "Unknown", speak: bool = True) -> dict:
    """
    Runs one full simulated call:
      1. Greets the caller (spoken + printed).
      2. Optionally transcribes a first caller message from an audio file.
      3. Loops reading typed caller input, replying with a call-type-aware
         Marathi response, and periodically re-classifying the call type.
      4. On exit, classifies the full conversation and saves a summary.
    Returns the summary dict.
    """
    print("\n" + "=" * 55)
    print("   MARATHI AI CALL ASSISTANT")
    print("   Type 'exit' or 'बाय' to end the call")
    print("=" * 55)

    print(f"\nAI: {GREETING}")
    speak_marathi(GREETING, "greeting.mp3", play=speak)

    conversation_history: list = []
    current_call_type = "unknown"
    turn = 0

    if first_audio_file:
        if not os.path.exists(first_audio_file):
            raise FileNotFoundError(f"Audio file not found: {first_audio_file}")
        print(f"\n[STEP] Transcribing first caller message: {first_audio_file}")
        caller_input = transcribe_audio(first_audio_file)
        print(f"Caller (audio): {caller_input}")
        turn += 1
        conversation_history.append({"role": "user", "text": caller_input})
        current_call_type = _detect_call_type_early(conversation_history)
        print(f"[SYSTEM] Detected call type: {current_call_type}")

        ai_reply = get_smart_reply(caller_input, conversation_history[:-1], call_type=current_call_type)
        conversation_history.append({"role": "assistant", "text": ai_reply})
        print(f"\nAI: {ai_reply}")
        speak_marathi(ai_reply, "ai_reply.mp3", play=speak)

    while True:
        print()
        caller_input = input("Caller (type in Marathi or English): ").strip()

        if caller_input.lower() in EXIT_WORDS:
            print(f"\nAI: {FAREWELL}")
            speak_marathi(FAREWELL, "farewell.mp3", play=speak)
            break

        if not caller_input:
            continue

        turn += 1
        conversation_history.append({"role": "user", "text": caller_input})

        if turn == 1:
            current_call_type = _detect_call_type_early(conversation_history)
            print(f"[SYSTEM] Detected call type: {current_call_type}")

        ai_reply = get_smart_reply(caller_input, conversation_history[:-1], call_type=current_call_type)
        conversation_history.append({"role": "assistant", "text": ai_reply})

        print(f"\nAI: {ai_reply}")
        speak_marathi(ai_reply, "ai_reply.mp3", play=speak)

        if turn % RECLASSIFY_EVERY_N_TURNS == 0:
            updated_type = _detect_call_type_early(conversation_history)
            if updated_type != "unknown":
                current_call_type = updated_type

    if not conversation_history:
        print("\n[SYSTEM] No conversation took place — nothing to summarize.")
        return {}

    print("\n[SYSTEM] Generating final call analysis...")
    final_classification = classify_call(conversation_history)
    summary = generate_summary(conversation_history, final_classification, caller_number=caller_number)
    print_summary(summary)
    return summary
