# summary.py — Call Summary Generator
# Generates a clean, structured summary after every call ends
# Saves it to a JSON file for the dashboard (Phase 3) to read later

import json
import os
from datetime import datetime


def generate_summary(
    conversation_history: list,
    classification: dict,
    caller_number: str = "Unknown"
) -> dict:
    """
    Generates a structured call summary from the conversation and classification.
    Saves it to call_logs/summary_<timestamp>.json
    Returns the summary dictionary.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Build the full transcript
    transcript = []
    for msg in conversation_history:
        role = "Caller" if msg["role"] == "user" else "AI Assistant"
        transcript.append(f"{role}: {msg['text']}")

    # Build structured summary
    summary = {
        "call_id": f"CALL_{filename_timestamp}",
        "timestamp": timestamp,
        "caller_number": caller_number,
        "caller_name": classification.get("caller_name", "Unknown"),
        "call_type": classification.get("call_type", "unknown"),
        "purpose": classification.get("purpose", "N/A"),
        "urgency": classification.get("urgency", "low"),
        "key_details": classification.get("key_details", {}),
        "action_needed": classification.get("action_needed", "N/A"),
        "transcript": transcript,
        "total_turns": len(conversation_history) // 2
    }

    # Save to call_logs folder
    os.makedirs("call_logs", exist_ok=True)
    filepath = f"call_logs/summary_{filename_timestamp}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"[SUMMARY] Call summary saved to: {filepath}")
    return summary


def print_summary(summary: dict):
    """
    Prints a clean, readable call summary in the terminal.
    """
    urgency_emoji = {
        "high": "🔴 HIGH",
        "medium": "🟡 MEDIUM",
        "low": "🟢 LOW"
    }.get(summary.get("urgency", "low"), "🟢 LOW")

    call_type_label = {
        "meeting_request": "📅 Meeting Request",
        "delivery": "📦 Delivery",
        "emergency": "🚨 Emergency",
        "personal": "👤 Personal",
        "business": "💼 Business",
        "unknown": "❓ Unknown"
    }.get(summary.get("call_type", "unknown"), "❓ Unknown")

    print("\n" + "="*55)
    print("         CALL SUMMARY")
    print("="*55)
    print(f"📞 Call ID      : {summary['call_id']}")
    print(f"🕐 Time         : {summary['timestamp']}")
    print(f"👤 Caller Name  : {summary['caller_name']}")
    print(f"📱 Number       : {summary['caller_number']}")
    print(f"📂 Call Type    : {call_type_label}")
    print(f"⚡ Urgency      : {urgency_emoji}")
    print(f"💬 Purpose      : {summary['purpose']}")

    # Print key details if available
    details = summary.get("key_details", {})
    if any(v for v in details.values() if v and v != "null"):
        print("\n📋 Key Details:")
        if details.get("time") and details["time"] != "null":
            print(f"   ⏰ Time     : {details['time']}")
        if details.get("date") and details["date"] != "null":
            print(f"   📅 Date     : {details['date']}")
        if details.get("location") and details["location"] != "null":
            print(f"   📍 Location : {details['location']}")
        if details.get("extra") and details["extra"] != "null":
            print(f"   ℹ️  Extra    : {details['extra']}")

    print(f"\n✅ Action Needed: {summary['action_needed']}")
    print(f"\n💾 Saved to     : call_logs/{summary['call_id']}.json")
    print("="*55)

    # Alert if emergency
    if summary.get("urgency") == "high":
        print("\n🚨 URGENT ALERT: This call needs immediate attention!")
        print("="*55)