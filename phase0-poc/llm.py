# llm.py — Language Model using Google Gemini API (free tier)
# Updated to use new google-genai package (google.generativeai is deprecated)

import os
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# SYSTEM PROMPT — personality of your Marathi AI call assistant
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
    conversation_history: list of previous messages for context across turns.
    """

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    # Initialize new google-genai client
    client = genai.Client(api_key=api_key)

    # Build conversation history for context
    history = []
    for msg in conversation_history:
        role = "user" if msg["role"] == "user" else "model"
        history.append(types.Content(role=role, parts=[types.Part(text=msg["text"])]))

    # Add current caller message
    history.append(types.Content(role="user", parts=[types.Part(text=caller_text)]))

    print(f"[LLM] Caller said: {caller_text}")

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=300,
            temperature=0.7,
        )
    )

    reply = response.text.strip()
    print(f"[LLM] AI Reply: {reply}")
    return reply


# Quick test
if __name__ == "__main__":
    test_input = "नमस्कार, मी रवी बोलतोय. उद्याच्या मीटिंगबद्दल सांगायचं होतं."
    reply = get_marathi_reply(test_input)
    print(f"\nCaller: {test_input}")
    print(f"AI Reply: {reply}")