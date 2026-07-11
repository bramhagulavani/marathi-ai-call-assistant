// script.js — Marathi AI Call Assistant Dashboard Frontend

const CALL_TYPE_LABELS = {
  meeting_request: "📅 Meeting Request",
  delivery:        "📦 Delivery",
  emergency:       "🚨 Emergency",
  personal:        "👤 Personal",
  business:        "💼 Business",
  unknown:         "❓ Unknown"
};

let allCalls = [];
let activeCallId = null;

// -------------------------------------------------------------------------
// LOAD DASHBOARD
// -------------------------------------------------------------------------
async function loadDashboard() {
  await loadStats();
  await loadCalls();
}

async function loadStats() {
  try {
    const res = await fetch("/api/stats");
    const data = await res.json();

    document.querySelector("#statTotal .stat-number").textContent  = data.total_calls  ?? 0;
    document.querySelector("#statUrgent .stat-number").textContent = data.urgent_calls ?? 0;
    document.querySelector("#statBusiness .stat-number").textContent = data.by_type?.business   ?? 0;
    document.querySelector("#statPersonal .stat-number").textContent = data.by_type?.personal   ?? 0;

  } catch (err) {
    console.error("Failed to load stats:", err);
  }
}

async function loadCalls() {
  const listEl = document.getElementById("callList");
  listEl.innerHTML = `<div class="loading">Loading calls...</div>`;

  try {
    const res = await fetch("/api/calls");
    const data = await res.json();
    allCalls = data.calls ?? [];

    if (allCalls.length === 0) {
      listEl.innerHTML = `<div class="empty-state">No calls yet.<br>Run Phase 1 to generate call logs.</div>`;
      return;
    }

    listEl.innerHTML = "";
    allCalls.forEach(call => {
      listEl.appendChild(buildCallCard(call));
    });

    // Auto-select first call
    if (allCalls.length > 0) {
      showCallDetail(allCalls[0]);
    }

  } catch (err) {
    listEl.innerHTML = `<div class="empty-state">Could not connect to server.<br>Make sure app.py is running.</div>`;
    console.error(err);
  }
}

// -------------------------------------------------------------------------
// BUILD CALL CARD (left panel)
// -------------------------------------------------------------------------
function buildCallCard(call) {
  const card = document.createElement("div");
  card.className = "call-card";
  card.dataset.callId = call.call_id;

  const urgency = call.urgency ?? "low";
  const typeLabel = CALL_TYPE_LABELS[call.call_type] ?? "❓ Unknown";
  const callerName = call.caller_name ?? "Unknown";
  const purpose = call.purpose ?? "N/A";
  const time = call.timestamp ?? "";

  card.innerHTML = `
    <div class="call-card-top">
      <span class="caller-name">${callerName}</span>
      <span class="urgency-badge ${urgency}">${urgencyLabel(urgency)}</span>
    </div>
    <div class="call-type-label">${typeLabel}</div>
    <div class="call-purpose">${purpose}</div>
    <div class="call-time">${time}</div>
  `;

  card.addEventListener("click", () => {
    document.querySelectorAll(".call-card").forEach(c => c.classList.remove("active"));
    card.classList.add("active");
    showCallDetail(call);
  });

  return card;
}

// -------------------------------------------------------------------------
// SHOW CALL DETAIL (right panel)
// -------------------------------------------------------------------------
function showCallDetail(call) {
  activeCallId = call.call_id;
  const panel = document.getElementById("detailPanel");
  const urgency = call.urgency ?? "low";
  const typeLabel = CALL_TYPE_LABELS[call.call_type] ?? "❓ Unknown";
  const details = call.key_details ?? {};
  const transcript = call.transcript ?? [];

  // Emergency alert
  const alertHTML = urgency === "high" ? `
    <div class="alert-box">🚨 URGENT — This call needs immediate attention!</div>
  ` : "";

  // Key details grid
  const detailFields = [
    { label: "Call Type",    value: typeLabel },
    { label: "Urgency",      value: urgencyLabel(urgency) },
    { label: "Caller Name",  value: call.caller_name ?? "Unknown" },
    { label: "Phone Number", value: call.caller_number ?? "Unknown" },
    { label: "Time",         value: details.time     ?? "—" },
    { label: "Date",         value: details.date     ?? "—" },
    { label: "Location",     value: details.location ?? "—" },
    { label: "Extra Info",   value: details.extra    ?? "—" },
  ];

  const detailGridHTML = detailFields.map(f => `
    <div class="detail-field">
      <div class="detail-field-label">${f.label}</div>
      <div class="detail-field-value">${f.value}</div>
    </div>
  `).join("");

  // Transcript
  const transcriptHTML = transcript.length === 0
    ? "<div style='color:var(--muted);font-size:13px;'>No transcript available.</div>"
    : transcript.map(line => {
        const isCaller = line.startsWith("Caller:");
        const speakerClass = isCaller ? "caller" : "ai";
        const speakerLabel = isCaller ? "Caller" : "AI Assistant";
        const text = line.replace(/^(Caller|AI Assistant): /, "");
        return `
          <div class="transcript-line">
            <div class="speaker ${speakerClass}">${speakerLabel}</div>
            <div>${text}</div>
          </div>
        `;
      }).join("");

  panel.innerHTML = `
    <div class="detail-header">
      <div>
        <div class="detail-caller">${call.caller_name ?? "Unknown Caller"}</div>
        <div class="detail-call-id">${call.call_id}</div>
      </div>
      <span class="urgency-badge ${urgency}">${urgencyLabel(urgency)}</span>
    </div>

    ${alertHTML}

    <div class="action-box">
      <div class="action-box-label">✅ Action Needed</div>
      <div class="action-box-value">${call.action_needed ?? "N/A"}</div>
    </div>

    <div class="detail-grid">${detailGridHTML}</div>

    <div class="transcript-title">Full Conversation Transcript</div>
    <div class="transcript-box">${transcriptHTML}</div>
  `;
}

// -------------------------------------------------------------------------
// HELPERS
// -------------------------------------------------------------------------
function urgencyLabel(urgency) {
  return { high: "🔴 High", medium: "🟡 Medium", low: "🟢 Low" }[urgency] ?? "🟢 Low";
}

// -------------------------------------------------------------------------
// INIT
// -------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", loadDashboard);