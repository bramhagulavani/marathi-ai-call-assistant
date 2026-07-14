# Marathi AI Call Assistant 🇮🇳📞

An AI-powered call assistant that answers phone calls **in Marathi** on behalf of a user who's busy, driving, in a lecture, in a meeting, or asleep. Instead of a traditional voicemail, it holds a real, natural, two-way conversation with the caller in Marathi, understands the purpose of the call, and gives the user a structured summary afterward.

## ✨ Key Features

- **Marathi-first conversation** — listens, understands, and replies naturally in Marathi
- **Context-aware responses** — asks relevant follow-up questions (meeting time, delivery details, etc.)
- **Call categorization** — tags calls as personal, business, delivery, emergency, meeting request
- **Urgency detection** — flags high-priority matters
- **Call summary dashboard** — web dashboard showing past calls, transcripts, and key details

## 🛠 Tech Stack

| Component | Tool |
|---|---|
| Speech-to-Text | Whisper (local, free) |
| LLM (understanding + reply) | Groq API — Llama 3.3 70B (free tier) |
| Text-to-Speech | gTTS |
| Dashboard backend | FastAPI |
| Dashboard frontend | HTML + CSS + JS |
| Call interception (real phone calls) | Android `CallScreeningService` — not built yet |

## 📂 Project Structure

```
marathi-ai-call-assistant/
├── run.py                     # single entry point: `python run.py chat|dashboard`
├── requirements.txt
├── .env.example                # copy to .env and add your GROQ_API_KEY
├── app/
│   ├── config.py                # all paths & settings, resolved absolutely
│   ├── groq_client.py            # one shared, cached Groq client
│   ├── stt.py                    # Whisper speech-to-text
│   ├── tts.py                    # gTTS text-to-speech
│   ├── conversation.py           # call-type-aware Marathi reply generation
│   ├── classifier.py             # call type + structured info extraction
│   ├── summary.py                # builds & saves the JSON call summary
│   ├── call_assistant.py         # the call loop (greet → converse → summarize)
│   └── dashboard/
│       ├── server.py             # FastAPI app serving /api/calls, /api/stats
│       └── static/               # index.html, style.css, script.js
├── data/
│   ├── call_logs/                # generated call summaries (JSON)
│   └── audio/                    # generated TTS audio files
└── docs/
    └── Marathi_AI_Call_Assistant_Proposal.docx
```

Everything lives in one `app/` package now instead of three disconnected `phaseN-*` folders that each duplicated setup, prompts, and paths.

## ⚙️ Setup

```bash
pip install -r requirements.txt
# also install ffmpeg and make sure it's on PATH

cp .env.example .env
# edit .env and set GROQ_API_KEY (free key: https://console.groq.com/keys)
```

## 🚀 Usage

**Simulated call (text mode):**
```bash
python run.py chat
# type what the caller says each turn; type 'exit' or 'बाय' to end the call
```

**Simulated call starting from a recorded audio file:**
```bash
python run.py chat --audio path/to/caller_message.wav
# first turn is transcribed from the file, rest of the call continues as text
```

**Dashboard:**
```bash
python run.py dashboard
# open http://localhost:8000
```

Every completed call writes a `summary_<timestamp>.json` file to `data/call_logs/`, which the dashboard reads automatically — no matter which directory you launch either command from.

## 🗺 Status & Roadmap

| Area | Status |
|---|---|
| Marathi conversation (STT → LLM → TTS) | ✅ Working |
| Call classification & structured extraction | ✅ Working |
| Urgency detection & alerts | ✅ Working |
| Call summary dashboard | ✅ Working |
| Real phone call interception (Android `CallScreeningService`) | 🔜 Not built |
| Adjustable tone (formal/friendly/professional) | 🔜 Not built |

## 📌 Future Scope

- Real phone call interception via Android `CallScreeningService` (Java)
- Spam call detection and filtering
- Support for additional regional languages
- Calendar integration for automatic meeting scheduling
- Voice personalization

## 👥 Contributors

| Name | Role |
|---|---|
| Bramha | AI Pipeline, Conversation Logic, Backend |
| Tanmay | (add role here) |

## 📄 License

Built for academic and research purposes.
