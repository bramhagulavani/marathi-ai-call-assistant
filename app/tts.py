# tts.py — Text-to-Speech, fully in-memory and streaming.
#
# Replaces the old gTTS-based module, which could only make one blocking
# request that returned a complete MP3 file written to disk. edge-tts
# streams synthesized audio as it's generated: as soon as a text chunk is
# handed to it, raw audio byte chunks start arriving, well before the full
# utterance has finished synthesizing. Nothing here ever touches disk.

import edge_tts

from . import config


async def stream_speech(text: str):
    """
    Async generator: takes a piece of Marathi text and yields raw audio
    byte chunks as edge-tts produces them. Callers forward each chunk
    onward (e.g. straight into a WebSocket) as it arrives — see
    app/live/call_session.py.
    """
    communicate = edge_tts.Communicate(text, voice=config.EDGE_TTS_VOICE)
    async for event in communicate.stream():
        if event["type"] == "audio":
            yield event["data"]


if __name__ == "__main__":
    import asyncio

    async def _test():
        total_bytes = 0
        async for chunk in stream_speech("नमस्कार! मी तुमचा मराठी AI सहाय्यक आहे."):
            total_bytes += len(chunk)
        print(f"Streamed {total_bytes} bytes of audio (nothing written to disk).")

    asyncio.run(_test())
