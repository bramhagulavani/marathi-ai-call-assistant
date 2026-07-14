# conversation.py — Smart Conversation Manager.
#
# This replaces the old duplicated setup where phase0/llm.py defined one
# generic Marathi persona and phase1/conversation.py defined a second,
# slightly different one used for call-type-specific replies. There is now
# a single BASE_PROMPT and a single set of per-call-type prompts, and a
# single "unknown" type doubles as the generic/first-turn persona — so
# there's exactly one place that defines how the assistant talks.

from . import config
from .groq_client import get_client

BASE_PROMPT = """
तुम्ही एक बुद्धिमान आणि विनम्र मराठी फोन सहाय्यक आहात.
तुम्ही वापरकर्त्याच्या वतीने फोन कॉलला उत्तर देत आहात.
वापरकर्ता सध्या उपलब्ध नाही — ते व्यस्त, व्याख्यानात, झोपलेले किंवा गाडी चालवत असू शकतात.
उत्तरे नेहमी संक्षिप्त, स्पष्ट आणि नैसर्गिक मराठीत द्या — खूप मोठी उत्तरे देऊ नका.
फक्त मराठीत बोला. इंग्रजी किंवा हिंदी वापरू नका.
"""

CALL_TYPE_PROMPTS = {
    "meeting_request": BASE_PROMPT + """
हा मीटिंग विनंतीचा कॉल आहे. खालील माहिती गोळा करा:
1. कॉलरचे नाव आणि संस्था
2. मीटिंगची तारीख आणि वेळ
3. मीटिंगचे ठिकाण
4. मीटिंगचा उद्देश
सर्व माहिती मिळाल्यावर सांगा की वापरकर्त्याला कळवले जाईल.
""",

    "delivery": BASE_PROMPT + """
हा डिलिव्हरीचा कॉल आहे. खालील माहिती गोळा करा:
1. डिलिव्हरी कंपनीचे नाव
2. कोणती वस्तू आहे
3. डिलिव्हरीची वेळ
4. पर्यायी व्यवस्था असेल तर (शेजारी देणे, इ.)
""",

    "emergency": BASE_PROMPT + """
हा तातडीचा कॉल आहे. शांतपणे पण त्वरेने खालील माहिती गोळा करा:
1. कोण बोलत आहे आणि काय झाले आहे
2. कुठे आहेत ते
3. किती तातडीचे आहे
तातडीची माहिती मिळताच सांगा की वापरकर्त्याला ALERT पाठवले जाईल.
""",

    "personal": BASE_PROMPT + """
हा वैयक्तिक कॉल आहे. विनम्रपणे:
1. कॉलरचे नाव विचारा
2. निरोप काय आहे ते विचारा
3. कॉलबॅक हवा आहे का ते विचारा
""",

    "business": BASE_PROMPT + """
हा व्यवसायिक कॉल आहे. व्यावसायिकपणे:
1. कॉलरचे नाव आणि कंपनी विचारा
2. कॉलचा उद्देश विचारा
3. कोणती कारवाई हवी आहे ते विचारा
""",

    "unknown": BASE_PROMPT + """
कॉलचा उद्देश अस्पष्ट आहे. विनम्रपणे:
1. कॉलरचे नाव विचारा
2. कशाबद्दल फोन केला ते विचारा
3. निरोप गोळा करा
""",
}


def get_smart_reply(caller_text: str, conversation_history: list, call_type: str = "unknown") -> str:
    """
    Generates a Marathi reply using the system prompt for the detected call type.

    caller_text: what the caller just said
    conversation_history: prior turns, as [{"role": "user"/"assistant", "text": ...}, ...]
    call_type: category from classifier.py, or "unknown" before it's been detected
    """
    client = get_client()
    system_prompt = CALL_TYPE_PROMPTS.get(call_type, CALL_TYPE_PROMPTS["unknown"])

    messages = [{"role": "system", "content": system_prompt}]
    for msg in conversation_history:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["text"]})
    messages.append({"role": "user", "content": caller_text})

    print(f"[CONVERSATION] Call type: {call_type} | Caller said: {caller_text}")

    response = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )

    reply = response.choices[0].message.content.strip()
    print(f"[CONVERSATION] AI reply: {reply}")
    return reply


if __name__ == "__main__":
    test_input = "नमस्कार, मी अमित. उद्या मीटिंग आहे."
    reply = get_smart_reply(test_input, [], call_type="meeting_request")
    print(f"\nCaller: {test_input}\nAI: {reply}")
