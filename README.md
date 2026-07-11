# Marathi AI Call Assistant 🇮🇳📞

An AI-powered call assistant that answers phone calls **in Marathi** on behalf of a user when they're busy, driving, in a lecture, in a meeting, sleeping, or simply don't want to pick up. Instead of a traditional voicemail, it holds a real, natural, two-way conversation with the caller in Marathi, understands the purpose of the call, and gives the user a structured summary afterward.

Most existing AI call-screening tools (Google's Pixel call screening, Truecaller, etc.) are English-first, with weak or absent regional language support. This project focuses specifically on **natural Marathi conversation**, for the large number of users in Maharashtra who are far more comfortable speaking Marathi than English.

---

## ✨ Key Features

- **Marathi-first conversation** — listens, understands, and replies naturally in Marathi
- **Context-aware responses** — asks relevant follow-up questions (e.g. meeting time, delivery details)
- **Call categorization** — tags calls as personal, business, delivery, family, or emergency
- **Urgency detection** — flags and immediately alerts the user for high-priority matters
- **Call summary dashboard** — web dashboard showing past calls, transcripts, and key details
- **Adjustable tone** — formal, friendly, or professional speaking style (upcoming)

---

## 🛠 Tech Stack (Free-tier, student-friendly)

| Component | Tool | Status |
|---|---|---|
| Speech-to-Text | Whisper (local, free, open-source) | ✅ Integrated |
| Language Understanding & Reply | Groq API — LLaMA 3.3 70B (free tier) | ✅ Integrated |
| Text-to-Speech | gTTS — Google Translate TTS (free, no key needed) | ✅ Integrated |
| Conversation Logic | Custom classifier + smart prompts (Python) | ✅ Built |
| Call Summary & Logging | JSON-based call logger with urgency detection | ✅ Built |
| Dashboard Backend | FastAPI (Python) | ✅ Built |
| Dashboard Frontend | HTML + CSS + JavaScript | ✅ Built |
| Call Interception | Android `CallScreeningService` API (Java) | 🔜 Phase 2 |

> **Note:** Originally planned with Google Gemini API, switched to Groq API due to free-tier quota restrictions in India. Groq provides the same quality with no region restrictions.

---

## 🗺 Roadmap

| Phase | Focus | Deliverable | Status |
|---|---|---|---|
| **Phase 0** | Proof of concept: STT → LLM → TTS loop | Marathi voice-in, voice-out chatbot demo | ✅ Complete |
| **Phase 1** | Conversation logic: classification & info extraction | AI extracts caller name, purpose, key details | ✅ Complete |
| **Phase 2** | Android integration via `CallScreeningService` | AI answers a real incoming phone call | 🔜 Upcoming |
| **Phase 3** | Web dashboard for call summaries | Web page showing caller history and details | ✅ Complete |
| **Phase 4** | Polish: tone settings, edge cases, demo prep | Presentation-ready working system | 🔜 Upcoming |

> Phase 2 (real phone-call interception) is the most technically demanding part of the project. It requires Android Java development and telephony permissions. Phases 0, 1, and 3 form the working core of the project and are fully functional.

---

## 📂 Project Structure

```
marathi-ai-call-assistant/
├── README.md
├── docs/
│   └── Marathi_AI_Call_Assistant_Proposal.docx
├── phase0-poc/
│   ├── stt.py              # Whisper-based Marathi Speech-to-Text
│   ├── llm.py              # Groq API — LLaMA 3.3 conversation engine
│   ├── tts.py              # gTTS Marathi Text-to-Speech
│   └── main.py             # Phase 0 entry point — text & audio modes
├── phase1-conversation-logic/
│   ├── classifier.py       # Call type detection & structured info extraction
│   ├── conversation.py     # Smart type-specific Marathi conversation prompts
│   ├── summary.py          # Call summary generator with urgency alerts
│   ├── main.py             # Phase 1 entry point — full intelligent pipeline
│   └── call_logs/          # Auto-generated JSON call summaries
├── phase2-android-integration/
│   └── (upcoming)
├── phase3-dashboard/
│   ├── app.py              # FastAPI backend serving call logs via REST API
│   └── static/
│       ├── index.html      # Dashboard layout — stats bar + split panel
│       ├── style.css       # Dark theme, urgency color coding, IBM Plex typography
│       └── script.js       # Dynamic call list, detail panel, stats display
├── requirements.txt
└── .gitignore
```

---

## 🚀 Current Status

**Phase 0, 1, and 3 are fully working and tested.**

- ✅ AI greets caller in spoken Marathi
- ✅ Understands English and Marathi input from caller
- ✅ Detects call type (business, meeting, delivery, emergency, personal)
- ✅ Asks smart follow-up questions based on call type
- ✅ Extracts caller name, purpose, time, location automatically
- ✅ Detects urgency level and fires alert for high-priority calls
- ✅ Saves structured JSON summary after every call
- ✅ Web dashboard displays all past calls with full transcript and details

---

## ⚙️ How to Run

### Prerequisites
```bash
pip install openai-whisper groq gTTS ffmpeg-python fastapi uvicorn
# Also install ffmpeg and add it to PATH
```

### Phase 0 — Basic Marathi conversation demo
```bash
cd phase0-poc
# Set API key
$env:GROQ_API_KEY="your_groq_key_here"    # Windows
export GROQ_API_KEY="your_groq_key_here"   # Mac/Linux

python main.py                  # Text mode
python main.py your_audio.wav   # Audio mode
```

### Phase 1 — Smart conversation with classification and summary
```bash
cd phase1-conversation-logic
$env:GROQ_API_KEY="your_groq_key_here"
python main.py
# Type 'exit' or 'बाय' to end the call and generate summary
```

### Phase 3 — Web Dashboard
```bash
cd phase3-dashboard
python app.py
# Open http://localhost:8000 in your browser
```

---

## 📌 Future Scope

- Phase 2: Real phone call interception via Android `CallScreeningService` (Java)
- Spam call detection and automatic filtering
- Support for additional regional languages (Hindi, Kannada, Telugu)
- Calendar integration for automatic meeting scheduling from call content
- Voice personalization — assistant mimics user's speaking style

---

## 👥 Contributors

| Name | Role |
|---|---|
| Bramha | AI Pipeline, Conversation Logic, Backend |
| Tanmay | (add role here) |

---

## 📄 License

This project is built for academic and research purposes.