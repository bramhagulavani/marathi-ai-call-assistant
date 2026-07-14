# classifier.py — Call Classification and Structured Info Extraction.
# Analyzes the conversation so far and extracts structured data from it.

import json

from . import config
from .groq_client import get_client

CALL_CATEGORIES = [
    "meeting_request",  # Caller wants to schedule or discuss a meeting
    "delivery",          # Courier, food, or package delivery related
    "emergency",          # Urgent family, medical, or critical situation
    "personal",           # Friend or family calling for general chat/message
    "business",           # Business inquiry, client, or work related
    "unknown",             # Cannot determine the purpose
]

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
    """Takes the full conversation history, returns structured classification dict."""
    client = get_client()

    conversation_text = "".join(
        f"{'कॉलर' if msg['role'] == 'user' else 'AI सहाय्यक'}: {msg['text']}\n"
        for msg in conversation_history
    )
    prompt = CLASSIFICATION_PROMPT.format(conversation=conversation_text)

    print("[CLASSIFIER] Analyzing call...")
    response = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.1,  # low temperature for consistent structured output
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw)
        print(f"[CLASSIFIER] call_type={result.get('call_type', 'unknown')} "
              f"urgency={result.get('urgency', 'low')}")
        return result
    except json.JSONDecodeError:
        print("[CLASSIFIER] Warning: could not parse JSON, falling back to raw text")
        return {
            "call_type": "unknown",
            "caller_name": "unknown",
            "purpose": raw,
            "key_details": {},
            "urgency": "low",
            "action_needed": "कॉल तपासा",
        }


if __name__ == "__main__":
    test_conversation = [
        {"role": "user", "text": "नमस्कार, मी अमित बोलतोय. उद्या सकाळी ११ वाजता पुण्यात मीटिंग आहे."},
        {"role": "assistant", "text": "नमस्कार अमित, मीटिंग कुठे होणार आहे?"},
        {"role": "user", "text": "FC Road वर, Cafe Coffee Day मध्ये."},
    ]
    print(json.dumps(classify_call(test_conversation), ensure_ascii=False, indent=2))
