# server.py — Dashboard backend. Reads call summaries from data/call_logs/
# (via config.py, so it works no matter what directory the process is
# started from — the original app.py used a relative "static" mount and
# a "../phase1-conversation-logic/call_logs" path that both broke unless
# you launched it from exactly the right folder) and serves them to the
# frontend.

import glob
import json
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .. import config

app = FastAPI(title="Marathi AI Call Assistant — Dashboard")


@app.get("/api/calls")
def get_all_calls():
    """Returns all call summaries, newest first."""
    calls = []
    pattern = os.path.join(config.CALL_LOGS_DIR, "summary_*.json")
    for filepath in sorted(glob.glob(pattern), reverse=True):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                calls.append(json.load(f))
            except json.JSONDecodeError:
                continue
    return {"total": len(calls), "calls": calls}


@app.get("/api/calls/{call_id}")
def get_single_call(call_id: str):
    """Returns a single call summary by call_id."""
    for call in get_all_calls()["calls"]:
        if call.get("call_id") == call_id:
            return call
    return {"error": "Call not found"}


@app.get("/api/stats")
def get_stats():
    """Returns summary statistics for the dashboard header."""
    calls = get_all_calls()["calls"]
    by_type: dict = {}
    for c in calls:
        t = c.get("call_type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1

    return {
        "total_calls": len(calls),
        "urgent_calls": sum(1 for c in calls if c.get("urgency") == "high"),
        "by_type": by_type,
    }


# Serve the frontend (index.html/style.css/script.js) using an absolute path
# so this works regardless of the current working directory.
app.mount("/", StaticFiles(directory=str(config.DASHBOARD_STATIC_DIR), html=True), name="static")


def main():
    import uvicorn
    print("\nMarathi AI Call Assistant — Dashboard")
    print(f"Open your browser at: http://localhost:{config.DASHBOARD_PORT}")
    print("Press Ctrl+C to stop\n")
    uvicorn.run(app, host=config.DASHBOARD_HOST, port=config.DASHBOARD_PORT)


if __name__ == "__main__":
    main()
