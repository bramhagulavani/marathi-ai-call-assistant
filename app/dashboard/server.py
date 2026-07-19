# server.py — single FastAPI app serving:
#   - the persistent WebSocket used for the real-time voice call (/ws/call)
#   - the live-call browser page (/call)
#   - the call-log dashboard (/) and its REST API (/api/*)
# One process, one port — this is the "persistent, full-duplex connection"
# server referenced in the architecture notes.

import glob
import json
import os

from fastapi import FastAPI, WebSocket
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .. import config
from ..live.call_session import handle_call

app = FastAPI(title="Marathi AI Call Assistant")


# ---------------------------------------------------------------------------
# REAL-TIME CALL — persistent two-way event channel
# ---------------------------------------------------------------------------
@app.websocket("/ws/call")
async def ws_call(websocket: WebSocket):
    await handle_call(websocket)


# ---------------------------------------------------------------------------
# DASHBOARD REST API — reads the JSON call summaries written by call_session
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# STATIC FRONTENDS — absolute paths, so this works from any working directory.
# /call must be mounted before the catch-all "/" mount.
# ---------------------------------------------------------------------------
@app.get("/call")
def call_redirect():
    return RedirectResponse(url="/call/")


app.mount("/call", StaticFiles(directory=str(config.LIVE_STATIC_DIR), html=True), name="live")
app.mount("/", StaticFiles(directory=str(config.DASHBOARD_STATIC_DIR), html=True), name="dashboard")


def main():
    import uvicorn
    print("\nMarathi AI Call Assistant")
    print(f"  Live call:  http://localhost:{config.SERVER_PORT}/call")
    print(f"  Dashboard:  http://localhost:{config.SERVER_PORT}/")
    print("Press Ctrl+C to stop\n")
    uvicorn.run(app, host=config.SERVER_HOST, port=config.SERVER_PORT)


if __name__ == "__main__":
    main()
