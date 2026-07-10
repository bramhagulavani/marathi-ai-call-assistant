# llm.py — Language Model using Groq API (free tier, no region restrictions)
# Uses Llama 3 model via Groq for fast, free Marathi conversation

import os
from groq import Groq

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
    Takes what the caller said (in Marathi or English text).
    Returns the AI assistant's natural Marathi reply as a string.
    conversation_history: list of previous messages for context across turns.
    """

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set.")

    client = Groq(api_key=api_key)

    # Build full message list: system prompt + history + current message
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in conversation_history:
        messages.append({
            "role": msg["role"],
            "content": msg["text"]
        })

    messages.append({"role": "user", "content": caller_text})

    print(f"[LLM] Caller said: {caller_text}")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Best free Groq model for Marathi
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )

    reply = response.choices[0].message.content.strip()
    print(f"[LLM] AI Reply: {reply}")
    return reply


# Quick test — run this file directly to test LLM alone
if __name__ == "__main__":
    test_input = "नमस्कार, मी रवी बोलतोय. उद्याच्या मीटिंगबद्दल सांगायचं होतं."
    reply = get_marathi_reply(test_input)
    print(f"\nCaller: {test_input}")
    print(f"AI Reply: {reply}")