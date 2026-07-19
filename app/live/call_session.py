# call_session.py — one live call over a single persistent WebSocket.
#
# Replaces the old file-path-passing CLI loop (app/call_assistant.py) end
# to end:
#   - The client sends live speech-to-text transcript fragments as JSON
#     text frames (event listener side of the two-way channel).
#   - The LLM reply is requested with stream=True and tokens are grouped
#     into sentences as they arrive (no waiting for the full reply).
#   - Each finished sentence is hnaded straight to the streaming TTS
#     pipeline, and every raw audio byte chunk it produces is pushed to
#     the client immediately as a binary WebSocket frame (event emitter
#     side) — never buffered to a file.
#   - Only the final structured summary (text/JSON, not audio) is written
#     to disk, same as before.

import json
import re

from fastapi import WebSocket, WebSocketDisconnect

from ..classifier import classify_call
from ..conversation import stream_smart_reply
from ..summary import generate_summary
from ..tts import stream_speech

GREETING = "नमस्कार! मी एक स्वयंचलित मराठी सहाय्यक आहे. ते सध्या उपलब्ध नाहीत. कृपया आपला निरोप सांगा, मी त्यांना कळवेन."
FAREWELL = "धन्यवाद! मी हा निरोप त्यांना नक्की पोहोचवेन. नमस्कार!"

# Splits streamed text into sentences on Marathi/English sentence-ending
# punctuation, so TTS can start on sentence 1 while the LLM is still
# generating sentence 2.
_SENTENCE_END = re.compile(r"[।!?.]+")
RECLASSIFY_EVERY_N_TURNS = 3


async def _speak_and_send(ws: WebSocket, text: str) -> None:
    """Streams one sentence to the client: text frame, then N binary audio frames."""
    await ws.send_text(json.dumps({"type": "assistant_text", "text": text}))
    async for audio_chunk in stream_speech(text):
        await ws.send_bytes(audio_chunk)
    await ws.send_text(json.dumps({"type": "audio_end"}))


async def _stream_reply_and_speak(ws: WebSocket, caller_text: str, history: list, call_type: str) -> str:
    """Consumes streamed LLM tokens, speaks each completed sentence as it forms, returns full reply text."""
    buffer = ""
    full_reply = ""

    async for delta in stream_smart_reply(caller_text, history, call_type):
        buffer += delta
        full_reply += delta

        while True:
            match = _SENTENCE_END.search(buffer)
            if not match:
                break
            sentence, buffer = buffer[: match.end()].strip(), buffer[match.end():]
            if sentence:
                await _speak_and_send(ws, sentence)

    if buffer.strip():
        await _speak_and_send(ws, buffer.strip())

    return full_reply.strip()


async def handle_call(ws: WebSocket, caller_number: str = "Unknown") -> None:
    await ws.accept()

    conversation_history: list = []
    current_call_type = "unknown"
    turn = 0

    try:
        await _speak_and_send(ws, GREETING)

        while True:
            raw = await ws.receive_text()
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                continue

            if message.get("type") == "end_call":
                await _speak_and_send(ws, FAREWELL)
                break

            if message.get("type") != "transcript":
                continue

            caller_text = (message.get("text") or "").strip()
            if not caller_text:
                continue

            turn += 1
            conversation_history.append({"role": "user", "text": caller_text})

            if turn == 1 or turn % RECLASSIFY_EVERY_N_TURNS == 0:
                classification = await classify_call(conversation_history)
                detected = classification.get("call_type", "unknown")
                if detected != "unknown":
                    current_call_type = detected
                await ws.send_text(json.dumps({"type": "call_type", "value": current_call_type}))

            reply_text = await _stream_reply_and_speak(
                ws, caller_text, conversation_history[:-1], current_call_type
            )
            conversation_history.append({"role": "assistant", "text": reply_text})

    except WebSocketDisconnect:
        pass
    finally:
        if conversation_history:
            classification = await classify_call(conversation_history)
            summary = generate_summary(conversation_history, classification, caller_number=caller_number)
            try:
                await ws.send_text(json.dumps({"type": "summary", "data": summary}))
            except Exception:
                pass  # socket already closed client-side
