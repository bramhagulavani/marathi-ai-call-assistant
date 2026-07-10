# classifier.py — Call Classification and Info Extraction
# Analyzes the conversation and extracts structured data from it

import os
import json
from groq import Groq

# ---------------------------------------------------------------------------
# CALL CATEGORIES
# ---------------------------------------------------------------------------
CALL_CATEGORIES = [
    "meeting_request",    # Caller wants to schedule or discuss a meeting
    "delivery",           # Courier, food, or package delivery related
    "emergency",          # Urgent family, medical, or critical situation
    "personal",           # Friend or family calling for general chat/message
    "business",           # Business inquiry, client, or work related
    "unknown"             # Cannot determine the purpose
]

# ---------------------------------------------------------------------------
# CLASSIFICATION PROMPT
# ---------------------------------------------------------------------------
CLASSIFICATION_PROMPT = """
तुम्ही एक कॉल विश्लेषण तज्ञ आहात. खालील संभाषण वाचा आणि फक्त JSON format मध्ये उत्तर द्या.

संभाषण:
{conversation}

खालील JSON structure मध्ये फक्त माहिती द्या, कोणताही अतिरिक्त मजकूर नको:
{{
    "call_type": "<meeting_request/delivery/emergency/personal/business/unknown>",
    "caller_name": "<कॉलरचे नाव किंवा unknown>",
    "purpose": "<कॉलचा मुख्य उद्देश एका वाक्यात>",
    "key_details": {{
        "time": "<वेळ किंवा null>",
        "location": "<ठिकाण किंवा null>",
        "date": "<तारीख किंवा null>",
        "extra": "<इतर महत्त्वाची माहिती किंवा null>"
    }},
    "urgency": "<high/medium/low>",
    "action_needed": "<वापरकर्त्याने काय करायला हवे>"
}}
"""

def classify_call(conversation_history: list) -> dict:
    """
    Takes the full conversation history.
    Returns a structured dictionary with call classification and extracted info.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set.")

    client = Groq(api_key=api_key)

    # Format conversation for the prompt
    conversation_text = ""
    for msg in conversation_history:
        role = "कॉलर" if msg["role"] == "user" else "AI सहाय्यक"
        conversation_text += f"{role}: {msg['text']}\n"

    prompt = CLASSIFICATION_PROMPT.format(conversation=conversation_text)

    print("[CLASSIFIER] Analyzing call...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.1,   # Low temperature for consistent structured output
    )

    raw = response.choices[0].message.content.strip()

    # Clean up response — remove markdown code blocks if present
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw)
        print(f"[CLASSIFIER] Call Type: {result.get('call_type', 'unknown')}")
        print(f"[CLASSIFIER] Urgency: {result.get('urgency', 'low')}")
        return result
    except json.JSONDecodeError:
        print(f"[CLASSIFIER] Warning: Could not parse JSON, returning raw text")
        return {
            "call_type": "unknown",
            "caller_name": "unknown",
            "purpose": raw,
            "key_details": {},
            "urgency": "low",
            "action_needed": "कॉल तपासा"
        }


# Quick test
if __name__ == "__main__":
    test_conversation = [
        {"role": "user", "text": "नमस्कार, मी अमित बोलतोय. उद्या सकाळी ११ वाजता पुण्यात मीटिंग आहे."},
        {"role": "assistant", "text": "नमस्कार अमित, मीटिंग कुठे होणार आहे?"},
        {"role": "user", "text": "FC Road वर, Cafe Coffee Day मध्ये."},
    ]
    result = classify_call(test_conversation)
    print("\nClassification Result:")
    print(json.dumps(result, ensure_ascii=False, indent=2))