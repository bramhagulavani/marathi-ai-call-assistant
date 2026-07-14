# config.py — single source of truth for paths, env vars, and settings.
# Every other module reads its configuration from here instead of
# hardcoding relative paths or re-reading environment variables.

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv is optional; if it isn't installed, environment
    # variables must be exported manually before running the app.
    pass

# ---------------------------------------------------------------------------
# PATHS (all resolved from this file's location, so behavior no longer
# depends on which directory the app happens to be launched from)
# ---------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
CALL_LOGS_DIR = DATA_DIR / "call_logs"
AUDIO_OUTPUT_DIR = DATA_DIR / "audio"

DASHBOARD_STATIC_DIR = APP_DIR / "dashboard" / "static"

CALL_LOGS_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# LLM / STT SETTINGS
# ---------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "medium")

DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8000"))


def require_groq_key() -> str:
    """Raise a clear, actionable error if GROQ_API_KEY isn't configured."""
    if not GROQ_API_KEY:
        raise SystemExit(
            "\nERROR: GROQ_API_KEY is not set.\n"
            "  1) Copy .env.example to .env\n"
            "  2) Put your key in it: GROQ_API_KEY=your_key_here\n"
            "  (or export it directly: export GROQ_API_KEY=your_key_here)\n"
            "  Get a free key at: https://console.groq.com/keys\n"
        )
    return GROQ_API_KEY
