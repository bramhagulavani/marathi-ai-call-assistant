# groq_client.py — single cached, async Groq client shared across the app.
# Async because the whole live-call pipeline (conversation streaming,
# classification) now runs inside the FastAPI WebSocket event loop.

from functools import lru_cache
from groq import AsyncGroq

from . import config


@lru_cache(maxsize=1)
def get_client() -> AsyncGroq:
    config.require_groq_key()
    return AsyncGroq(api_key=config.GROQ_API_KEY)
