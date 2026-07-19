#!/usr/bin/env python3
"""
run.py — starts the single server that hosts everything:
    - the real-time voice call page + WebSocket:  http://localhost:8000/call
    - the call-log dashboard:                     http://localhost:8000/

The old terminal-based `python run.py chat` mode has been fully replaced
by the browser real-time flow (browser mic + speech recognition in,
streamed AI voice out), so there's nothing left to dispatch between.
"""

from app import config


def main():
    config.require_groq_key()
    from app.dashboard.server import main as run_server
    run_server()


if __name__ == "__main__":
    main()
