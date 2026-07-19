// script.js — Live Call frontend.
//
// - Browser-native speech recognition captures the caller's speech and
//   sends finalized text fragments to the server over a persistent
//   WebSocket (no audio file ever leaves the browser).
// - The server streams back small JSON text frames (what the AI is
//   saying) interleaved with raw binary audio-byte frames.
// - Binary frames are appended directly to a MediaSource SourceBuffer,
//   which decodes and schedules them for continuous, gapless playback
//   as they arrive — no waiting for a complete audio file.

const startBtn = document.getElementById("startBtn");
const endBtn = document.getElementById("endBtn");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const callTypeBadge = document.getElementById("callTypeBadge");
const transcriptLog = document.getElementById("transcriptLog");
const summaryBox = document.getElementById("summaryBox");
const playbackEl = document.getElementById("playbackEl");

let ws = null;
let recognition = null;
let mediaSource = null;
let sourceBuffer = null;
let audioQueue = [];
let pendingAssistantText = null;

// ---------------------------------------------------------------------------
// STREAMED AUDIO PLAYBACK — MediaSource decodes+schedules chunks as they
// arrive, giving continuous gapless playback without ever touching disk.
// ---------------------------------------------------------------------------
function initPlayback() {
  mediaSource = new MediaSource();
  playbackEl.src = URL.createObjectURL(mediaSource);
  mediaSource.addEventListener("sourceopen", () => {
    sourceBuffer = mediaSource.addSourceBuffer("audio/mpeg");
    sourceBuffer.addEventListener("updateend", appendNextChunk);
  });
  // Unlocks autoplay on first user gesture (the "Start Call" click).
  playbackEl.play().catch(() => {});
}

function queueAudioChunk(bytes) {
  audioQueue.push(bytes);
  appendNextChunk();
}

function appendNextChunk() {
  if (!sourceBuffer || sourceBuffer.updating || audioQueue.length === 0) return;
  const chunk = audioQueue.shift();
  try {
    sourceBuffer.appendBuffer(chunk);
  } catch (err) {
    console.error("appendBuffer failed:", err);
  }
}

// ---------------------------------------------------------------------------
// MICROPHONE + CONTINUOUS SPEECH RECOGNITION
// ---------------------------------------------------------------------------
function startRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    setStatus("ended", "Speech recognition not supported in this browser (use Chrome).");
    return false;
  }

  recognition = new SpeechRecognition();
  recognition.lang = "mr-IN";
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onresult = (event) => {
    const result = event.results[event.results.length - 1];
    if (result.isFinal) {
      const text = result[0].transcript.trim();
      if (text) {
        addLogLine("caller", text);
        sendTranscript(text);
      }
    }
  };

  recognition.onerror = (event) => {
    console.warn("Speech recognition error:", event.error);
  };

  recognition.onend = () => {
    // Browsers auto-stop recognition after silence; restart while the call is live.
    if (ws && ws.readyState === WebSocket.OPEN) {
      recognition.start();
    }
  };

  recognition.start();
  return true;
}

function sendTranscript(text) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: "transcript", text }));
  }
}

// ---------------------------------------------------------------------------
// WEBSOCKET — persistent, full-duplex connection to the server
// ---------------------------------------------------------------------------
function connectWebSocket() {
  const protocol = location.protocol === "https:" ? "wss:" : "ws:";
  ws = new WebSocket(`${protocol}//${location.host}/ws/call`);
  ws.binaryType = "arraybuffer";

  ws.onopen = () => setStatus("live", "Live — listening");

  ws.onmessage = (event) => {
    if (typeof event.data === "string") {
      handleServerMessage(JSON.parse(event.data));
    } else {
      queueAudioChunk(new Uint8Array(event.data));
    }
  };

  ws.onclose = () => setStatus("ended", "Call ended");
  ws.onerror = (err) => console.error("WebSocket error:", err);
}

function handleServerMessage(message) {
  switch (message.type) {
    case "assistant_text":
      addLogLine("ai", message.text);
      break;
    case "call_type":
      callTypeBadge.textContent = message.value.replace("_", " ");
      callTypeBadge.classList.remove("hidden");
      break;
    case "summary":
      showSummary(message.data);
      break;
    case "audio_end":
      break; // no action needed; MSE queue keeps flowing
  }
}

// ---------------------------------------------------------------------------
// UI HELPERS
// ---------------------------------------------------------------------------
function setStatus(state, text) {
  statusDot.className = `status-dot ${state}`;
  statusText.textContent = text;
}

function addLogLine(speaker, text) {
  const empty = transcriptLog.querySelector(".log-empty");
  if (empty) empty.remove();

  const line = document.createElement("div");
  line.className = `log-line ${speaker}`;
  const label = document.createElement("div");
  label.className = "speaker";
  label.textContent = speaker === "caller" ? "Caller" : "AI Assistant";
  const body = document.createElement("div");
  body.textContent = text;
  line.appendChild(label);
  line.appendChild(body);
  transcriptLog.appendChild(line);
  transcriptLog.scrollTop = transcriptLog.scrollHeight;
}

function showSummary(summary) {
  if (!summary || !summary.call_id) return;
  summaryBox.classList.remove("hidden");
  summaryBox.textContent =
    `Call ID: ${summary.call_id}\n` +
    `Caller: ${summary.caller_name}\n` +
    `Type: ${summary.call_type}   Urgency: ${summary.urgency}\n` +
    `Purpose: ${summary.purpose}\n` +
    `Action needed: ${summary.action_needed}`;
}

// ---------------------------------------------------------------------------
// START / END CALL
// ---------------------------------------------------------------------------
startBtn.addEventListener("click", async () => {
  try {
    // Request microphone permission (required even though recognition uses
    // its own audio path — this both prompts the user and unlocks audio).
    await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (err) {
    setStatus("ended", "Microphone permission denied.");
    return;
  }

  setStatus("connecting", "Connecting...");
  summaryBox.classList.add("hidden");
  callTypeBadge.classList.add("hidden");
  transcriptLog.innerHTML = "";
  audioQueue = [];

  initPlayback();
  connectWebSocket();
  const recognitionStarted = startRecognition();

  startBtn.classList.add("hidden");
  endBtn.classList.remove("hidden");

  if (!recognitionStarted) {
    endBtn.classList.add("hidden");
    startBtn.classList.remove("hidden");
  }
});

endBtn.addEventListener("click", () => {
  if (recognition) recognition.onend = null; // stop auto-restart
  if (recognition) recognition.stop();
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: "end_call" }));
  }
  endBtn.classList.add("hidden");
  startBtn.classList.remove("hidden");
});
