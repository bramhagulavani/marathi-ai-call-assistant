# groq_client.py — single cached Groq client shared by conversation.py and
# classifier.py. Previously each module created a brand-new Groq(...) client
# on every single API call; this reuses one client for the process lifetime.

from functools import lru_cache
from groq import Groq

from . import config


@lru_cache(maxsize=1)
def get_client() -> Groq:
    config.require_groq_key()
    return Groq(api_key=config.GROQ_API_KEY)
