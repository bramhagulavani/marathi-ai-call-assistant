# llm.py — Language Model using Google Gemini API (free tier)
# Takes Marathi caller text, returns a natural Marathi reply

import google.generativeai as genai
import os

# ---------------------------------------------------------------------------
# SYSTEM PROMPT — this is the "personality" of your AI assistant
# This tells Gemini exactly how to behave as a Marathi call assistant
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """
तुम्ही एक बुद्धिमान आणि विनम्र मराठी फोन सहाय्यक आहात.
तुम्ही वापरकर्त्याच्या वतीने फोन कॉलला उत्तर देत आहात.
वापरकर्ता सध्या उपलब्ध नाही — ते व्यस्त, व्याख्यानात, झोपलेले किंवा गाडी चालवत असू शकतात.

तुमची कामे:
1. कॉल करणाऱ्या व्यक्तीशी नैसर्गिक आणि सभ्य मराठीत बोला.
2. कॉलचा उद्देश समजून घ्या — उदा. वैयक्तिक निरोप, मीटिंग विनंती, डिलिव्हरी, व्यवसाय, किंवा तातडीची बाब.
3. आवश्यक असल्यास योग्य प्रश्न विचारा — उदा. मीटिंगची वेळ, ठिकाण, किंवा कॉलरचे नाव.
4. तातडीची परिस्थिती असेल तर ते ओळखा आणि स्पष्टपणे सांगा.
5. उत्तरे नेहमी संक्षिप्त, स्पष्ट आणि नैसर्गिक मराठीत द्या — खूप मोठी उत्तरे देऊ नका.
6. संभाषण संपल्यावर कॉलरचे आभार माना.

महत्त्वाचे: फक्त मराठीत बोला. इंग्रजी किंवा हिंदी वापरू नका.
"""

def get_marathi_reply(caller_text: str, conversation_history: list = []) -> str:
    """
    Takes what the caller said (in Marathi text form).
    Returns the AI assistant's natural Marathi reply as a string.

    conversation_history: list of previous messages in this call
                          (so the AI remembers context across turns)
    """

    # Get Gemini API key from environment variable (never hardcode API keys!)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set. Please set it first.")

    genai.configure(api_key=api_key)

    # Use Gemini 1.5 Flash — fast, free tier, good multilingual support
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

    # Build conversation history for context across multiple turns in a call
    history = []
    for msg in conversation_history:
        history.append({
            "role": msg["role"],
            "parts": [msg["text"]]
        })

    # Start or continue conversation
    chat = model.start_chat(history=history)

    print(f"[LLM] Caller said: {caller_text}")
    response = chat.send_message(caller_text)

    reply = response.text.strip()
    print(f"[LLM] AI Reply: {reply}")
    return reply


# Quick test — run this file directly to test LLM alone
if __name__ == "__main__":
    test_input = "नमस्कार, मी रवी बोलतोय. उद्याच्या मीटिंगबद्दल सांगायचं होतं."
    reply = get_marathi_reply(test_input)
    print(f"\nCaller: {test_input}")
    print(f"AI Reply: {reply}")