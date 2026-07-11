# app.py — Phase 3 Dashboard Backend
# FastAPI server that reads call_logs/ and serves them to the frontend

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os
import glob

app = FastAPI()

# Path to call_logs folder (from Phase 1)
CALL_LOGS_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'phase1-conversation-logic', 'call_logs'
)

# -------------------------------------------------------------------------
# API ROUTES
# -------------------------------------------------------------------------

@app.get("/api/calls")
def get_all_calls():
    """
    Returns list of all call summaries sorted by newest first.
    """
    calls = []
    pattern = os.path.join(CALL_LOGS_PATH, "summary_*.json")
    files = glob.glob(pattern)

    for filepath in sorted(files, reverse=True):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                calls.append(data)
            except json.JSONDecodeError:
                continue

    return {"total": len(calls), "calls": calls}


@app.get("/api/calls/{call_id}")
def get_single_call(call_id: str):
    """
    Returns a single call summary by call_id.
    """
    pattern = os.path.join(CALL_LOGS_PATH, f"summary_*.json")
    for filepath in glob.glob(pattern):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if data.get("call_id") == call_id:
                    return data
            except json.JSONDecodeError:
                continue
    return {"error": "Call not found"}


@app.get("/api/stats")
def get_stats():
    """
    Returns summary statistics for the dashboard header.
    """
    calls = get_all_calls()["calls"]
    total = len(calls)
    urgent = sum(1 for c in calls if c.get("urgency") == "high")
    by_type = {}
    for c in calls:
        t = c.get("call_type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1

    return {
        "total_calls": total,
        "urgent_calls": urgent,
        "by_type": by_type
    }


# Serve static frontend files
app.mount("/", StaticFiles(directory="static", html=True), name="static")


# -------------------------------------------------------------------------
# RUN
# -------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    print("\n Marathi AI Call Assistant — Dashboard")
    print(" Open your browser at: http://localhost:8000")
    print(" Press Ctrl+C to stop\n")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)