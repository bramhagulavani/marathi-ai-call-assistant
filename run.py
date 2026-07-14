#!/usr/bin/env python3
"""
run.py — single entry point for the whole project.

    python run.py chat                    # text-mode simulated call
    python run.py chat --audio call.wav   # first caller turn from an audio file, then text
    python run.py dashboard               # launch the call-log web dashboard

This replaces the old setup where phase0-poc/main.py and
phase1-conversation-logic/main.py were two separate, partially-duplicated
entry points, and phase3-dashboard/app.py had to be run from inside its
own folder for relative paths to work.
"""

import argparse

from app import config


def main():
    parser = argparse.ArgumentParser(description="Marathi AI Call Assistant")
    subparsers = parser.add_subparsers(dest="command", required=True)

    chat_parser = subparsers.add_parser("chat", help="Run a simulated call in the terminal")
    chat_parser.add_argument("--audio", help="Optional audio file for the caller's first message", default=None)
    chat_parser.add_argument("--caller-number", help="Caller phone number to record in the summary", default="Unknown")
    chat_parser.add_argument("--no-speak", action="store_true", help="Don't play audio replies out loud")

    subparsers.add_parser("dashboard", help="Launch the call-log web dashboard")

    args = parser.parse_args()

    if args.command == "chat":
        config.require_groq_key()
        from app.call_assistant import run_call
        run_call(first_audio_file=args.audio, caller_number=args.caller_number, speak=not args.no_speak)

    elif args.command == "dashboard":
        from app.dashboard.server import main as run_dashboard
        run_dashboard()


if __name__ == "__main__":
    main()
