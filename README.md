# Marathi AI Call Assistant 🇮🇳📞

An AI-powered call assistant that answers phone calls **in Marathi** on behalf of a user when they're busy, driving, in a lecture, in a meeting, sleeping, or simply don't want to pick up. Instead of a traditional voicemail, it holds a real, natural, two-way conversation with the caller in Marathi, understands the purpose of the call, and gives the user a short summary afterward.

Most existing AI call-screening tools (Google's Pixel call screening, Truecaller, etc.) are English-first, with weak or absent regional language support. This project focuses specifically on **natural Marathi conversation**, for the large number of users in Maharashtra who are far more comfortable speaking Marathi than English.

## ✨ Key Features

- **Marathi-first conversation** — listens, understands, and replies naturally in Marathi
- **Context-aware responses** — asks relevant follow-up questions (e.g. meeting time, delivery details)
- **Call categorization** — tags calls as personal, business, delivery, family, or emergency
- **Urgency detection** — flags and notifies the user immediately for urgent matters
- **Call summary dashboard** — simple web view of past calls and key details
- **Adjustable tone** — formal, friendly, or professional speaking style

## 🛠 Tech Stack (Free-tier, student-friendly)

| Component | Tool |
|---|---|
| Speech-to-Text | Whisper (local, free, open-source) |
| Language Understanding & Reply | Google Gemini API (free tier) |
| Text-to-Speech | Google Cloud TTS (free tier) |
| Call Interception | Android `CallScreeningService` API |
| Dashboard | Simple web app (HTML/JS or React) |

## 🗺 Roadmap

| Phase | Focus | Deliverable |
|---|---|---|
| **Phase 0** | Proof of concept: STT → LLM → TTS loop on a laptop | Marathi voice-in, voice-out chatbot demo |
| **Phase 1** | Conversation logic: call classification & info extraction | AI reliably extracts caller name, purpose, key details |
| **Phase 2** | Android integration via `CallScreeningService` | AI actually answers a real incoming phone call |
| **Phase 3** | Web dashboard for call summaries | Web page showing caller history and details |
| **Phase 4** | Polish: tone settings, edge cases, demo prep | Presentation-ready working system |

> Phase 2 (real phone-call interception) is the most technically demanding part of the project. Phases 0 and 1 form the core intelligence and are the most reliable to fully complete. A simulated web-based demo is an acceptable fallback if Phase 2 isn't fully finished in time.

## 📂 Project Structure

```
marathi-ai-call-assistant/
├── README.md
├── docs/
│   └── Marathi_AI_Call_Assistant_Proposal.docx
├── phase0-poc/
│   ├── stt.py
│   ├── llm.py
│   ├── tts.py
│   └── main.py
├── phase1-conversation-logic/
├── phase2-android-integration/
├── phase3-dashboard/
├── requirements.txt
└── .gitignore
```

## 🚀 Status

🔨 Currently building **Phase 0** — proof of concept.

## 📌 Future Scope

- Spam call detection
- Support for additional regional languages
- Calendar integration for automatic scheduling
- Voice personalization

## 👥 Contributors

- Bramha - MARCO
- Tanmay - 