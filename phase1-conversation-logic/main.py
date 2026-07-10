# main.py — Phase 1 Entry Point
# Full pipeline: Smart Conversation + Call Classification + Summary Generation
# This builds directly on Phase 0 and adds intelligence layer on top

import os
import sys
import time

# Import Phase 0 components
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'phase0-poc'))
from tts import speak_marathi

# Import Phase 1 components
from conversation import get_smart_reply
from classifier import classify_call
from summary import generate_summary, print_summary

# ---------------------------------------------------------------------------
# INITIAL CLASSIFIER — quick check after first 2 exchanges
# Detects call type early so AI can switch to the right conversation style
# ---------------------------------------------------------------------------

def detect_call_type_early(conversation_history: list) -> str:
    """
    After the first 1-2 caller messages, do a quick classification
    so we can switch to the right conversation style early.
    """
    if len(conversation_history) >= 2:
        result = classify_call(conversation_history)
        return result.get("call_type", "unknown")
    return "unknown"


def run_phase1():
    """
    Phase 1 full conversation loop:
    - Greets caller in Marathi
    - Detects call type after first exchange
    - Uses smart type-specific conversation prompts
    - Classifies and extracts info at the end
    - Generates and saves a structured call summary
    """

    print("\n" + "="*55)
    print("   MARATHI AI CALL ASSISTANT — PHASE 1")
    print("   Smart Conversation + Call Classification")
    print("   Type 'exit' or 'बाय' to end the call")
    print("="*55)

    conversation_history = []
    current_call_type = "unknown"

    # Step 1: Greet the caller
    greeting = "नमस्कार! मी एक स्वयंचलित मराठी सहाय्यक आहे. ते सध्या उपलब्ध नाहीत. कृपया आपला निरोप सांगा, मी त्यांना कळवेन."
    print(f"\nAI: {greeting}")
    speak_marathi(greeting, "greeting.mp3")

    turn = 0

    while True:
        print()
        caller_input = input("Caller (type in Marathi or English): ").strip()

        # End call
        if caller_input.lower() in ["exit", "bye", "बाय", "ठीक आहे", "धन्यवाद"]:
            farewell = "धन्यवाद! मी हा निरोप त्यांना नक्की पोहोचवेन. नमस्कार!"
            print(f"\nAI: {farewell}")
            speak_marathi(farewell, "farewell.mp3")
            break

        if not caller_input:
            continue

        turn += 1

        # Step 2: After first exchange, detect call type
        if turn == 1:
            # Add first message to history for classification
            conversation_history.append({"role": "user", "text": caller_input})
            # Quick early classification
            current_call_type = detect_call_type_early(conversation_history)
            print(f"[SYSTEM] Detected call type: {current_call_type}")
        else:
            conversation_history.append({"role": "user", "text": caller_input})

        # Step 3: Generate smart reply based on call type
        ai_reply = get_smart_reply(
            caller_input,
            conversation_history[:-1],  # history excluding current message
            call_type=current_call_type
        )

        # Store AI reply in history
        conversation_history.append({"role": "assistant", "text": ai_reply})

        # Step 4: Speak and display reply
        print(f"\nAI: {ai_reply}")
        speak_marathi(ai_reply, "ai_reply.mp3")

        # Re-classify every 3 turns for better accuracy as conversation develops
        if turn % 3 == 0:
            updated_type = detect_call_type_early(conversation_history)
            if updated_type != "unknown":
                current_call_type = updated_type

    # Step 5: Final classification of full conversation
    print("\n[SYSTEM] Generating final call analysis...")
    final_classification = classify_call(conversation_history)

    # Step 6: Generate and display summary
    summary = generate_summary(
        conversation_history=conversation_history,
        classification=final_classification,
        caller_number="Unknown"  # Phase 2 will add real number
    )
    print_summary(summary)


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    # Check API key
    if not os.getenv("GROQ_API_KEY"):
        print("\n ERROR: GROQ_API_KEY is not set!")
        print("  Please set it like this:")
        print("  Windows  → $env:GROQ_API_KEY='your_key_here'")
        print("  Mac/Linux → export GROQ_API_KEY=your_key_here")
        sys.exit(1)

    run_phase1()