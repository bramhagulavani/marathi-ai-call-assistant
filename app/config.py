# config.py — single source of truth for paths, env vars, and settings.

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

# Only text data (JSON call summaries) touches disk. Audio is never written
# to or read from disk anywhere in the app — it's generated and consumed
# entirely as in-memory streams over the WebSocket connection.
DATA_DIR = PROJECT_ROOT / "data"
CALL_LOGS_DIR = DATA_DIR / "call_logs"
CALL_LOGS_DIR.mkdir(parents=True, exist_ok=True)

DASHBOARD_STATIC_DIR = APP_DIR / "dashboard" / "static"
LIVE_STATIC_DIR = APP_DIR / "live" / "static"

# ---------------------------------------------------------------------------
# LLM SETTINGS
# ---------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# ---------------------------------------------------------------------------
# TTS SETTINGS — edge-tts (free, streams raw audio bytes natively, no key)
# ---------------------------------------------------------------------------
EDGE_TTS_VOICE = os.getenv("EDGE_TTS_VOICE", "mr-IN-AarohiNeural")

# ---------------------------------------------------------------------------
# SERVER SETTINGS
# ---------------------------------------------------------------------------
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))


def require_groq_key() -> str:
    if not GROQ_API_KEY:
        raise SystemExit(
            "\nERROR: GROQ_API_KEY is not set.\n"
            "  1) Copy .env.example to .env\n"
            "  2) Put your key in it: GROQ_API_KEY=your_key_here\n"
            "  Get a free key at: https://console.groq.com/keys\n"
        )
    return GROQ_API_KEY
