# Marathi AI Call Assistant 🇮🇳📞

A real-time, browser-based AI call assistant that speaks with callers **live, in Marathi**, entirely over a persistent streaming connection — no audio ever touches disk.

## ✨ Key Features

- **Live, full-duplex voice conversation** in the browser — no file uploads, no request/response round-trips
- **Streaming everywhere**: LLM tokens stream in, are grouped into sentences, and streamed straight into TTS; TTS audio bytes stream straight to the browser and play back gaplessly as they arrive
- **Call categorization & urgency detection**, same as before, running live during the call
- **Call summary dashboard** — reviews past calls after they end

## 🏗 Architecture

```
Browser mic → Web Speech API (STT, in-browser) → WebSocket text frame
                                                        ↓
                                          FastAPI WebSocket endpoint
                                                        ↓
                                Groq LLM (stream=True) → text token stream
                                                        ↓
                                  sentence buffer → edge-tts (streaming)
                                                        ↓
                                     raw audio byte chunks → WebSocket
                                                        ↓
                         Browser MediaSource → gapless streamed playback
```

One persistent WebSocket per call (`/ws/call`) carries everything: JSON text frames for transcripts/replies/status, and raw binary frames for audio. Nothing is buffered to a complete file at any stage — text is handled token-by-token, audio chunk-by-chunk.

## 🛠 Tech Stack

| Component | Tool |
|---|---|
| Speech-to-Text | Browser-native Web Speech API (client-side, live) |
| LLM (understanding + reply) | Groq API — Llama 3.3 70B, streamed |
| Text-to-Speech | edge-tts — free, streams raw audio bytes natively |
| Transport | FastAPI WebSocket (persistent, full-duplex) |
| Audio playback | MediaSource Extensions (gapless chunked playback) |
| Dashboard | FastAPI REST + HTML/CSS/JS |

## 📂 Project Structure

```
marathi-ai-call-assistant/
├── run.py                        # starts the one server (call page + dashboard)
├── requirements.txt
├── .env.example
├── app/
│   ├── config.py                  # paths & settings (no audio-output paths — none needed)
│   ├── groq_client.py              # shared AsyncGroq client
│   ├── conversation.py             # stream_smart_reply() — yields LLM tokens as they arrive
│   ├── classifier.py               # call type + structured info extraction
│   ├── tts.py                      # stream_speech() — yields raw audio bytes as edge-tts produces them
│   ├── summary.py                  # builds & saves the JSON call summary (text only)
│   ├── live/
│   │   ├── call_session.py          # WebSocket orchestrator: tokens → sentences → TTS → socket
│   │   └── static/                  # live call page (index.html, style.css, script.js)
│   └── dashboard/
│       ├── server.py                # FastAPI app: /ws/call, /api/*, static mounts
│       └── static/                  # call-log dashboard page
└── data/
    └── call_logs/                   # generated call summaries (JSON text only)
```

## ⚙️ Setup

```bash
pip install -r requirements.txt

cp .env.example .env
# edit .env and set GROQ_API_KEY (free key: https://console.groq.com/keys)
```

## 🚀 Usage

```bash
python run.py
```

- **Live call:** open `http://localhost:8000/call`, click **Start Call**, allow microphone access, and speak. The assistant replies with streamed Marathi voice in real time.
- **Dashboard:** open `http://localhost:8000/` to review past call summaries and transcripts.

Use **Chrome** — it has the most complete support for both the Web Speech API and MediaSource-based MP3 streaming used here.

## 🗺 Status

| Area | Status |
|---|---|
| Real-time streaming voice call (browser ↔ server) | ✅ Working |
| Streaming LLM reply generation | ✅ Working |
| Streaming TTS, no disk I/O | ✅ Working |
| Call classification, urgency detection | ✅ Working |
| Call summary dashboard | ✅ Working |
| Real phone call interception (Android `CallScreeningService`) | 🔜 Not built |

## 👥 Contributors

| Name | Role |
|---|---|
| Bramha | AI Pipeline, Conversation Logic, Backend |
| Tanmay | (add role here) |

## 📄 License

Built for academic and research purposes.
