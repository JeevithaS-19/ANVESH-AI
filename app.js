/* =========================================================================
   ANVESH AI — Member 1 Frontend Prototype
   app.js — router, screen templates, event binding, data-flow glue.
   Depends on api.js being loaded first (uses Api, STEPS, LANGUAGES, state).
   ========================================================================= */

// ============================ Router ======================================
function goTo(stepId) {
  window.location.hash = stepId;
}

window.addEventListener("hashchange", render);
window.addEventListener("DOMContentLoaded", () => {
  if (!window.location.hash) window.location.hash = "language";
  render();
});

function currentStep() {
  const id = (window.location.hash || "#language").replace("#", "");
  return STEPS.find(s => s.id === id) ? id : "language";
}

function renderTracker(activeId) {
  const activeIdx = STEPS.findIndex(s => s.id === activeId);
  const el = document.getElementById("journeyTracker");
  el.innerHTML = STEPS.map((s, i) => {
    const cls = i === activeIdx ? "active" : (i < activeIdx ? "done" : "");
    return `<div class="j-step ${cls}"><span class="j-num">${i < activeIdx ? "✓" : i + 1}</span>${escapeHtml(s.label)}</div>`;
  }).join("");
  document.getElementById("topLangLabel").textContent = labelFor(state.language);
}

function render() {
  const step = currentStep();
  renderTracker(step);
  const main = document.getElementById("mainScreen");
  main.innerHTML = SCREENS[step]();
  bindScreenEvents(step);
}

// ============================ Screens =====================================
const SCREENS = {

  language: () => `
    <div class="screen">
      <div class="eyebrow">Step 1 of 7</div>
      <h2>Choose your language</h2>
      <p class="lede">Pick the language you're most comfortable speaking. You can switch anytime.</p>
      <div class="lang-grid">
        ${LANGUAGES.map(l => `
          <button class="lang-card ${state.language === l.code ? "selected" : ""}" data-lang="${l.code}">
            <span class="native">${l.native}</span>
            <span class="roman">${l.roman}</span>
          </button>
        `).join("")}
      </div>
      <div class="actions">
        <button class="btn btn-primary" onclick="goTo('voice')">Continue</button>
      </div>
    </div>
  `,

  voice: () => `
    <div class="screen">
      <div class="eyebrow">Step 2 of 7</div>
      <h2>Tell ANVESH about yourself</h2>
      <p class="lede">Speak naturally about your education, skills and what kind of work you're looking for — no forms to fill.</p>
      <div class="card voice-stage">
        <button class="mic-btn" id="micBtn" aria-label="Start speaking">🎙️</button>
        <div class="voice-status" id="voiceStatus">Tap the microphone to start speaking</div>
        <div class="transcript-box" id="transcriptBox"></div>
        <div class="fallback-note">Prefer to type instead?</div>
        <div class="text-fallback">
          <input type="text" id="fallbackInput" placeholder="e.g. I studied B.Tech, I know Python, looking for developer roles..." />
          <button class="btn btn-primary" id="fallbackSend">Send</button>
        </div>
      </div>
    </div>
  `,

  profile: () => {
    if (state.loading.profile) return loadingState("Building your profile", "Reading what you told ANVESH and organising it.");
    if (state.errors.profile) return errorState(state.errors.profile, "profile");
    if (!state.profile) return emptyState("No profile yet", "Complete the voice or text step first so ANVESH has something to work with.", "voice", "Go to voice step");

    const p = state.profile.entities;
    const fields = [
      ["Name", p.name],
      ["Education", (p.education || []).join(", ")],
      ["Skills", (p.skills || []).join(", ")],
      ["Experience", p.experience],
      ["Location", p.location],
      ["Work preference", p.job_preference],
    ];

    return `
      <div class="screen">
        <div class="eyebrow">Step 3 of 7</div>
        <h2>Your profile so far</h2>
        <p class="lede">Here's what ANVESH understood. Missing details are asked one at a time.</p>
        <div class="card">
          <div class="field-list">
            ${fields.map(([label, value]) => `
              <div class="field-row">
                <span class="field-label">${escapeHtml(label)}</span>
                ${value ? `<span class="field-value">${escapeHtml(String(value))}</span>` : `<span class="tag tag-missing">Missing</span>`}
              </div>
            `).join("")}
          </div>
          ${!state.profile.profile_complete ? `
            <div class="next-q">
              <strong>ANVESH will ask next</strong>
              ${escapeHtml(state.profile.next_question)}
            </div>
          ` : `<div class="next-q"><strong>Profile complete</strong>All required details are in. Ready to check your skill gap.</div>`}
        </div>
        <div class="actions">
          <button class="btn btn-ghost" onclick="goTo('voice')">Add more detail</button>
          <button class="btn btn-primary" onclick="loadRecommendation()">See my skill gap</button>
        </div>
      </div>
    `;
  },

  skillgap: () => {
    if (state.loading.rec) return loadingState("Comparing your skills", "Matching what you have against what the role needs.");
    if (state.errors.rec) return errorState(state.errors.rec, "skillgap");
    if (!state.skillGap) return emptyState("No skill-gap data yet", "Go back and complete your profile first.", "profile", "Go to profile");

    const g = state.skillGap;
    const pct = 100 - g.gap_percent;
    return `
      <div class="screen">
        <div class="eyebrow">Step 4 of 7</div>
        <h2>Your skill gap</h2>
        <p class="lede">Compared against the role ANVESH thinks fits you best.</p>
        <div class="card">
          <div class="skill-cols">
            <div class="skill-block">
              <h4>Skills you already have</h4>
              <div class="chip-list">${g.matched_skills.map(s => `<span class="chip chip-have">${escapeHtml(s)}</span>`).join("")}</div>
            </div>
            <div class="skill-block">
              <h4>Skills to build</h4>
              <div class="chip-list">${g.missing_skills.map(s => `<span class="chip chip-need">${escapeHtml(s)}</span>`).join("")}</div>
            </div>
          </div>
          <div class="gap-bar-wrap">
            <div class="gap-bar-track"><div class="gap-bar-fill" style="width:${pct}%"></div></div>
            <div class="gap-bar-caption"><span>${pct}% match</span><span>${g.missing_skills.length} skill(s) to close the gap</span></div>
          </div>
        </div>
        <div class="actions">
          <button class="btn btn-ghost" onclick="goTo('profile')">Back to profile</button>
          <button class="btn btn-primary" onclick="goTo('nsqf')">See training pathway</button>
        </div>
      </div>
    `;
  },

  nsqf: () => {
    if (!state.recommendation) return emptyState("No training pathway yet", "Complete the skill-gap step first.", "skillgap", "Go to skill gap");
    return `
      <div class="screen">
        <div class="eyebrow">Step 5 of 7</div>
        <h2>Recommended training pathway</h2>
        <p class="lede">NSQF-aligned courses that close your missing skills.</p>
        <div class="card">
          ${state.recommendation.pathway.map(item => `
            <div class="nsqf-item">
              <div class="nsqf-level">${escapeHtml(item.level)}</div>
              <div>
                <div class="nsqf-title">${escapeHtml(item.title)}</div>
                <div class="nsqf-meta">${escapeHtml(item.meta)}</div>
              </div>
            </div>
          `).join("")}
        </div>
        <div class="actions">
          <button class="btn btn-ghost" onclick="goTo('skillgap')">Back</button>
          <button class="btn btn-primary" onclick="goTo('occupation')">See best-fit occupation</button>
        </div>
      </div>
    `;
  },

  occupation: () => {
    if (!state.recommendation) return emptyState("No match yet", "Complete the earlier steps first.", "skillgap", "Go to skill gap");
    const r = state.recommendation.rec;
    return `
      <div class="screen">
        <div class="eyebrow">Step 6 of 7</div>
        <h2>Your best-fit occupation</h2>
        <p class="lede">Based on your profile, skills and location.</p>
        <div class="card">
          <div class="score-wrap">
            <div class="score-ring" style="--pct:${r.compatibility_score}">
              <div class="score-num">${r.compatibility_score}<span>/ 100</span></div>
            </div>
            <div>
              <div class="occ-title">${escapeHtml(r.occupation)}</div>
              <div class="occ-sub">${r.matched_skills.length} of ${r.matched_skills.length + r.missing_skills.length} required skills matched</div>
            </div>
          </div>
          <button class="explain-toggle" id="explainToggle">Why this recommendation? ▾</button>
          <div class="explain-body" id="explainBody">${escapeHtml(r.explanation)}</div>
        </div>
        <div class="actions">
          <button class="btn btn-ghost" onclick="goTo('nsqf')">Back</button>
          <button class="btn btn-primary" onclick="goTo('opportunities')">See opportunities</button>
        </div>
      </div>
    `;
  },

  opportunities: () => {
    if (!state.recommendation) return emptyState("No opportunities yet", "Complete the earlier steps first.", "skillgap", "Go to skill gap");
    const opps = state.recommendation.opportunities;
    return `
      <div class="screen">
        <div class="eyebrow">Step 7 of 7</div>
        <h2>Opportunities for you</h2>
        <p class="lede">Training, employment and livelihood options mapped to your pathway.</p>
        ${opps.map(o => `
          <div class="opp-card">
            <span class="opp-type ${o.type}">${o.type}</span>
            <div class="opp-title">${escapeHtml(o.title)}</div>
            <div class="opp-meta">${escapeHtml(o.meta)}</div>
          </div>
        `).join("")}
        <div class="card" style="margin-top:18px; text-align:center;">
          <p class="lede" style="margin:0 0 14px;">ANVESH can read this out loud, or you can revisit any earlier step.</p>
          <div class="actions" style="margin-top:0; justify-content:center;">
            <button class="btn btn-ghost" onclick="goTo('occupation')">Back</button>
            <button class="btn btn-primary" id="playTts">🔊 Play recommendation</button>
          </div>
        </div>
      </div>
    `;
  },
};

// ---------------------- Reusable state screens ----------------------------
function loadingState(title, desc) {
  return `<div class="screen"><div class="state-box"><div class="spinner"></div><div class="state-title">${escapeHtml(title)}</div><div class="state-desc">${escapeHtml(desc)}</div></div></div>`;
}
function emptyState(title, desc, goStep, cta) {
  return `<div class="screen"><div class="state-box"><div class="icon-badge empty">–</div><div class="state-title">${escapeHtml(title)}</div><div class="state-desc">${escapeHtml(desc)}</div><button class="btn btn-primary" onclick="goTo('${goStep}')">${escapeHtml(cta)}</button></div></div>`;
}
function errorState(err, retryStep) {
  const timeout = err.code === "TIMEOUT";
  return `<div class="screen"><div class="state-box"><div class="icon-badge err">!</div>
    <div class="state-title">${timeout ? "This is taking too long" : "Something went wrong"}</div>
    <div class="state-desc">${escapeHtml(err.message)}</div>
    <button class="btn btn-primary" onclick="retry('${retryStep}')">Try again</button>
  </div></div>`;
}

function retry(step) {
  if (step === "profile") { state.errors.profile = null; processTranscript(state.transcript); }
  if (step === "skillgap") { state.errors.rec = null; loadRecommendation(); }
}

// ---------------------- Screen-specific event binding ----------------------
function bindScreenEvents(step) {
  if (step === "language") {
    document.querySelectorAll(".lang-card").forEach(card => {
      card.addEventListener("click", () => {
        state.language = card.dataset.lang;
        render();
      });
    });
  }

  if (step === "voice") {
    const micBtn = document.getElementById("micBtn");
    const status = document.getElementById("voiceStatus");
    const transcriptBox = document.getElementById("transcriptBox");
    let listening = false;

    micBtn.addEventListener("click", () => {
      listening = !listening;
      micBtn.classList.toggle("listening", listening);
      if (listening) {
        status.textContent = "Listening… speak now";
        transcriptBox.classList.remove("show");
        // Simulate STT capture for the prototype demo.
        setTimeout(() => {
          if (!listening) return;
          const demoUtterance = "I studied B.Tech in Computer Science, I know Python and some web development, and I have one year of freelance experience. I'm looking for a hybrid developer job in Bengaluru.";
          transcriptBox.textContent = demoUtterance;
          transcriptBox.classList.add("show");
          status.textContent = "Got it — processing…";
          micBtn.classList.remove("listening");
          listening = false;
          processTranscript(demoUtterance);
        }, 1800);
      } else {
        status.textContent = "Tap the microphone to start speaking";
      }
    });

    document.getElementById("fallbackSend").addEventListener("click", submitFallback);
    document.getElementById("fallbackInput").addEventListener("keydown", (e) => {
      if (e.key === "Enter") submitFallback();
    });

    function submitFallback() {
      const val = document.getElementById("fallbackInput").value.trim();
      if (!val) return;
      status.textContent = "Processing your message…";
      processTranscript(val);
    }
  }

  if (step === "occupation") {
    const toggle = document.getElementById("explainToggle");
    const body = document.getElementById("explainBody");
    if (toggle) {
      toggle.addEventListener("click", () => {
        body.classList.toggle("show");
        toggle.textContent = body.classList.contains("show") ? "Why this recommendation? ▴" : "Why this recommendation? ▾";
      });
    }
  }

  if (step === "opportunities") {
    const playBtn = document.getElementById("playTts");
    if (playBtn) {
      playBtn.addEventListener("click", () => {
        playBtn.textContent = "🔊 Playing…";
        // REAL INTEGRATION: call M3's TTS endpoint and play returned audio.
        setTimeout(() => { playBtn.textContent = "🔊 Play recommendation"; }, 1600);
      });
    }
  }
}

// ---------------------- Data flow between screens --------------------------
async function processTranscript(text) {
  state.transcript = text;
  state.loading.profile = true;
  state.errors.profile = null;
  goTo("profile");
  render();
  try {
    const result = await Api.processInput(text, state.language);
    state.profile = result;
  } catch (e) {
    state.errors.profile = e;
  } finally {
    state.loading.profile = false;
    render();
  }
}

async function loadRecommendation() {
  state.loading.rec = true;
  state.errors.rec = null;
  goTo("skillgap");
  render();
  try {
    const result = await Api.getRecommendation(state.profile);
    state.skillGap = result.skillGap;
    state.recommendation = {
      pathway: result.nsqf_pathway,
      rec: result.recommendation,
      opportunities: result.opportunities,
    };
  } catch (e) {
    state.errors.rec = e;
  } finally {
    state.loading.rec = false;
    render();
  }
}

// ---------------------- Utilities ------------------------------------------
function escapeHtml(str) {
  return String(str ?? "").replace(/[&<>"']/g, m => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
  }[m]));
}
