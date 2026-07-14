# summary.py — Call Summary Generator.
# Builds a structured summary after a call ends and saves it as JSON
# under data/call_logs/ (single shared location, see config.py) so the
# dashboard can read it regardless of which directory the app was run from.

import json
from datetime import datetime

from . import config


def generate_summary(conversation_history: list, classification: dict, caller_number: str = "Unknown") -> dict:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    transcript = [
        f"{'Caller' if msg['role'] == 'user' else 'AI Assistant'}: {msg['text']}"
        for msg in conversation_history
    ]

    summary = {
        "call_id": f"CALL_{file_timestamp}",
        "timestamp": timestamp,
        "caller_number": caller_number,
        "caller_name": classification.get("caller_name", "Unknown"),
        "call_type": classification.get("call_type", "unknown"),
        "purpose": classification.get("purpose", "N/A"),
        "urgency": classification.get("urgency", "low"),
        "key_details": classification.get("key_details", {}),
        "action_needed": classification.get("action_needed", "N/A"),
        "transcript": transcript,
        "total_turns": len(conversation_history) // 2,
    }

    filepath = config.CALL_LOGS_DIR / f"summary_{file_timestamp}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"[SUMMARY] Call summary saved to: {filepath}")
    return summary


def print_summary(summary: dict) -> None:
    urgency_label = {"high": "🔴 HIGH", "medium": "🟡 MEDIUM", "low": "🟢 LOW"}.get(
        summary.get("urgency", "low"), "🟢 LOW"
    )
    call_type_label = {
        "meeting_request": "📅 Meeting Request",
        "delivery": "📦 Delivery",
        "emergency": "🚨 Emergency",
        "personal": "👤 Personal",
        "business": "💼 Business",
        "unknown": "❓ Unknown",
    }.get(summary.get("call_type", "unknown"), "❓ Unknown")

    print("\n" + "=" * 55)
    print("         CALL SUMMARY")
    print("=" * 55)
    print(f"📞 Call ID      : {summary['call_id']}")
    print(f"🕐 Time         : {summary['timestamp']}")
    print(f"👤 Caller Name  : {summary['caller_name']}")
    print(f"📱 Number       : {summary['caller_number']}")
    print(f"📂 Call Type    : {call_type_label}")
    print(f"⚡ Urgency      : {urgency_label}")
    print(f"💬 Purpose      : {summary['purpose']}")

    details = summary.get("key_details", {})
    if any(v for v in details.values() if v and v != "null"):
        print("\n📋 Key Details:")
        for key, icon, label in [
            ("time", "⏰", "Time"), ("date", "📅", "Date"),
            ("location", "📍", "Location"), ("extra", "ℹ️ ", "Extra"),
        ]:
            value = details.get(key)
            if value and value != "null":
                print(f"   {icon} {label:<9}: {value}")

    print(f"\n✅ Action Needed: {summary['action_needed']}")
    print(f"\n💾 Saved to     : {config.CALL_LOGS_DIR / (summary['call_id'] + '.json')}")
    print("=" * 55)

    if summary.get("urgency") == "high":
        print("\n🚨 URGENT ALERT: This call needs immediate attention!")
        print("=" * 55)
