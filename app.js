/* =========================================================================
   ANVESH AI — Member 1 Frontend Prototype
   app.js — router, screen templates, event binding, data-flow glue.
   Depends on api.js and effects.js being loaded first.
   ========================================================================= */

// ============================ Router ======================================
function goTo(stepId) {
  stopSpeaking();
  window.location.hash = stepId;
}

window.addEventListener("hashchange", render);
window.addEventListener("DOMContentLoaded", async () => {
  injectBlobs();
  if (!window.location.hash) window.location.hash = "landing";
  render();
  Api.checkHealth().then(updateStatusDot);
  Api.createSession();
});

function injectBlobs() {
  const wrap = document.createElement("div");
  wrap.innerHTML = `<div class="blob blob-1"></div><div class="blob blob-2"></div><div class="blob blob-3"></div>`;
  document.body.prepend(...wrap.children);
}

function currentStep() {
  const id = (window.location.hash || "#landing").replace("#", "");
  if (id === "landing") return "landing";
  return STEPS.find(s => s.id === id) ? id : "landing";
}

function updateStatusDot() {
  const dots = document.querySelectorAll(".js-status-dot");
  const labels = document.querySelectorAll(".js-status-label");
  if (!dots.length) return;
  const cls = "status-dot " + (state.backendOnline === null ? "checking" : state.backendOnline ? "online" : "offline");
  const text = state.backendOnline === null ? t("statusChecking") : state.backendOnline ? t("statusLive") : t("statusOffline");
  dots.forEach(d => d.className = cls);
  labels.forEach(l => l.textContent = text);
}

function renderTracker(activeId) {
  const el = document.getElementById("journeyTracker");
  const app = document.getElementById("app");
  if (activeId === "landing") {
    el.innerHTML = "";
    el.style.display = "none";
    app.classList.add("on-landing");
  } else {
    el.style.display = "";
    app.classList.remove("on-landing");
    const activeIdx = STEPS.findIndex(s => s.id === activeId);
    el.innerHTML = STEPS.map((s, i) => {
      const cls = i === activeIdx ? "active" : (i < activeIdx ? "done" : "");
      return `<div class="j-step ${cls}"><span class="j-num">${i < activeIdx ? "✓" : i + 1}</span>${escapeHtml(t(s.key))}</div>`;
    }).join("");
  }
  document.querySelectorAll(".js-lang-label").forEach(el => el.textContent = labelFor(state.language));
  updateStatusDot();
  document.querySelectorAll(".js-sound-toggle").forEach(el => el.textContent = state.soundOn ? "🔊" : "🔇");
}

function render() {
  setDocumentLanguage();
  const step = currentStep();
  document.body.dataset.scene = step;
  renderTracker(step);
  const main = document.getElementById("mainScreen");
  main.innerHTML = SCREENS[step]();
  bindScreenEvents(step);
}

// ---------------------- Shared decorative helpers ---------------------
// Every inner screen gets the mascot + a contextual speech bubble, plus a
// couple of scattered handwritten-style notes, echoing the reference mood
// board. sceneMascot() is dropped into a screen's markup wherever it fits.
function sceneMascot(bubbleText, opts = {}) {
  const size = opts.size || 150;
  return `
    <div class="scene-mascot ${opts.className || ""}">
      <div class="speech-bubble scene-bubble">${escapeHtml(bubbleText)}</div>
      <div class="mascot-wrap" style="width:${size}px">${MASCOT_SVG}</div>
    </div>
  `;
}

function stickyNotes(notes) {
  return notes.map((n, i) => `<div class="sticky-note note-${i + 1}">${escapeHtml(n)}</div>`).join("");
}

// ============================ Screens =====================================
const SCREENS = {

  landing: () => `
    <div class="screen landing-screen">
      <section class="hero-photo">
        <img class="hero-photo-img" src="assets/bg-landing.jpg" alt="" />
        <div class="hero-photo-overlay hero-photo-overlay-light"></div>

        <nav class="hero-nav">
          <div class="brand">
            <div class="brand-mark" onclick="goTo('landing')" style="cursor:pointer">AI</div>
            <div>
              <div class="brand-name brand-name-dark">ANVESH AI</div>
              <div class="brand-sub brand-sub-dark">${t("skillPathfinder")}</div>
            </div>
          </div>
          <div class="hero-nav-links">
            <a href="#landing" data-nav="home"">${t("home")}</a>
            <a href="#" data-nav="about"">${t("about")}</a>
            <a href="#" data-nav="features"">${t("features")}</a>
            <a href="#" data-nav="how"">${t("how")}</a>
          </div>
          <div class="top-actions">
            <button class="pill-btn glass js-status-pill" title="${t("backendStatus")}">
              <span class="status-dot checking js-status-dot"></span>
              <span class="js-status-label">${t("statusChecking")}</span>
            </button>
            <button class="pill-btn glass js-sound-toggle" onclick="toggleSound()" title="${t("toggleSound")}">🔊</button>
            <label class="language-select-wrap" title="${t("language")}">
              <span class="language-icon">🌐</span>
              <select class="pill-btn glass js-landing-language" aria-label="${t("language")}">
                ${LANGUAGES.map(l => `<option value="${l.code}" ${state.language === l.code ? "selected" : ""}>${escapeHtml(l.native)}</option>`).join("")}
              </select>
            </label>
          </div>
        </nav>

        <div class="hero-content">
          <div class="hero-text">
            <div class="hero-kicker">${t("kicker")}</div>
            <h1 class="hero-title">${t("heroTitle1")} <span class="grad-blue">${t("heroTitle2")}</span><br>${t("heroTitle3")} <span class="grad-pink">${t("heroTitle4")}</span></h1>
            <p class="hero-sub">${t("heroSub")}</p>
            <div class="hero-actions">
              <button class="btn btn-primary btn-lg" id="heroStart">${t("start")}</button>
              <button class="btn btn-outline-light btn-lg" id="heroVoiceOver">${t("hear")}</button>
            </div>
          </div>

          <div class="hero-mascot-stage">
            <div class="brain-caption">
              <svg class="brain-outline" viewBox="0 0 80 60" aria-hidden="true">
                <path d="M20 30c-6 0-9-6-6-11 1-4 6-6 6-6 2-4 8-5 11-2 3-3 9-2 11 2 0 0 5 2 6 6 3 5 0 11-6 11 1 5-2 10-8 10-3 3-9 3-12 0-6 0-9-5-8-10z" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.4"/>
                <path d="M30 15v22M40 13v26M50 16v20" stroke="rgba(255,255,255,0.35)" stroke-width="1" fill="none"/>
              </svg>
              <div class="brain-text">${t("plan")}</div>
            </div>
            <div class="speech-bubble">${t("future")}</div>
            <div class="mascot-wrap" id="mascotWrap">
              ${MASCOT_SVG}
            </div>
            <div class="floating-cards">
              <div class="glass-card"><span>👤</span> ${t("skills")}</div>
              <div class="glass-card"><span>🎓</span> ${t("training")}</div>
              <div class="glass-card"><span>💼</span> ${t("jobs")}</div>
            </div>
            <div class="dream-caption">${t("dream")}</div>
          </div>
        </div>
      </section>

      <section class="feature-strip" id="featuresSection">
        <div class="section-kicker">${t("help")}</div>
        <h2 class="section-title">${t("oneConversation")}</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-tile tile-1">🗣️</div>
            <div class="feature-name">${t("talkNaturally")}</div>
            <div class="feature-desc">${t("talkNaturallyDesc")}</div>
          </div>
          <div class="feature-card">
            <div class="feature-tile tile-2">🎯</div>
            <div class="feature-name">${t("skillGapCard")}</div>
            <div class="feature-desc">${t("skillGapDesc")}</div>
          </div>
          <div class="feature-card">
            <div class="feature-tile tile-3">📚</div>
            <div class="feature-name">${t("trainingPath")}</div>
            <div class="feature-desc">${t("trainingDesc")}</div>
          </div>
          <div class="feature-card">
            <div class="feature-tile tile-4">💼</div>
            <div class="feature-name">${t("realOpp")}</div>
            <div class="feature-desc">${t("realOppDesc")}</div>
          </div>
        </div>
      </section>

      <section class="band-cta" id="howSectionTarget">
        <h2>${t("realSkills")}<br>${t("realOpportunities")}</h2>
        <p>${t("bandDesc")}</p>
        <button class="btn btn-inverse btn-lg" id="bandCtaStart">${t("begin")}</button>
      </section>

      <footer class="site-footer">
        <div class="footer-brand">ANVESH AI</div>
        <div class="footer-note">${t("prototype")}</div>
      </footer>
    </div>
  `,

  language: () => `
    <div class="screen">
      <div class="eyebrow">${stepText(1)}</div>
      <h2>${t("chooseLanguage")}</h2>
      <p class="lede">${t("chooseLanguageDesc")}</p>
      <div class="lang-grid">
        ${LANGUAGES.map(l => `
          <button class="lang-card ${state.language === l.code ? "selected" : ""}" data-lang="${l.code}">
            <span class="native">${l.native}</span>
            <span class="roman">${l.roman}</span>
          </button>
        `).join("")}
      </div>
      <div class="actions">
        <button class="btn btn-primary" onclick="playSound('click'); goTo('voice')">${t("continue")}</button>
      </div>
    </div>
  `,

  voice: () => `
    <div class="screen">
      ${sceneMascot(t("listenMascot"))}
      ${stickyNotes([t("smallSteps"), t("betterFuture")])}
      <div class="eyebrow">${stepText(2)}</div>
      <h2>${t("tell")}</h2>
      <p class="lede">${t("tellDesc")}</p>
      <div class="card voice-stage">
        <div class="mic-wrap">
          <div class="mic-ring"></div>
          <div class="mic-ring"></div>
          <button class="mic-btn" id="micBtn" aria-label="${t("startSpeaking")}">🎙️</button>
        </div>
        <div class="waveform" id="waveform">
          ${Array.from({length:7}).map(() => `<span></span>`).join("")}
        </div>
        <div class="voice-status" id="voiceStatus">${speechSupported() ? t("tapMic") : t("unsupported")}</div>
        <div class="transcript-box" id="transcriptBox"></div>
        <div class="fallback-note">${t("preferType")}</div>
        <div class="text-fallback">
          <input type="text" id="fallbackInput" placeholder="${escapeHtml(t("placeholder"))}" />
          <button class="btn btn-primary" id="fallbackSend">${t("send")}</button>
        </div>
      </div>
    </div>
  `,

  profile: () => {
    if (state.loading.profile) return loadingState(t("building"), t("buildingDesc"));
    if (state.errors.profile) return errorState(state.errors.profile, "profile");
    if (!state.profile) return emptyState(t("noProfile"), t("noProfileDesc"), "voice", t("goVoice"));

    const p = state.profile.entities;
    const fields = [
      [t("name"), p.name],
      [t("education"), Array.isArray(p.education) ? p.education.join(", ") : p.education],
      [t("skillsLabel"), Array.isArray(p.skills) ? p.skills.join(", ") : p.skills],
      [t("experience"), p.experience],
      [t("location"), p.location],
      [t("workPreference"), p.job_preference],
    ];

    return `
      <div class="screen">
        ${sceneMascot(t("profileReady"))}
        ${stickyNotes([t("keepGoing"), t("betterFuture")])}
        <div class="profile-layout">
          <aside class="profile-sidebar">
            <button class="side-link" onclick="playSound('click'); goTo('landing')">🏠 ${t("dashboard")}</button>
            <button class="side-link active">👤 ${t("myProfile")}</button>
            <button class="side-link" onclick="playSound('click'); goTo('nsqf')">🎓 ${t("learningPath")}</button>
            <button class="side-link" onclick="playSound('click'); goTo('skillgap')">📊 ${t("skillGapNav")}</button>
            <button class="side-link" onclick="playSound('click'); goTo('nsqf')">🎯 ${t("training")}</button>
            <button class="side-link" onclick="playSound('click'); goTo('opportunities')">💼 ${t("opportunitiesNav")}</button>
          </aside>
          <div class="profile-main">
            <div class="eyebrow">${stepText(3)}</div>
            <h2>${t("profileTitle")} ${mockTag()}</h2>
            <p class="lede">${t("profileDesc")}</p>
            <div class="card">
              <div class="field-list">
                ${fields.map(([label, value]) => `
                  <div class="field-row">
                    <span class="field-label">${escapeHtml(label)}</span>
                    ${value ? `<span class="field-value">${escapeHtml(String(value))}</span>` : `<span class="tag tag-missing">${t("missing")}</span>`}
                  </div>
                `).join("")}
              </div>
              ${!state.profile.profile_complete ? `
                <div class="next-q">
                  <strong>${t("askNext")}</strong>
                  ${escapeHtml(state.profile.next_question)}
                </div>
              ` : `<div class="next-q"><strong>${t("profileComplete")}</strong>${t("profileCompleteDesc")}</div>`}
            </div>
            <div class="actions">
              <button class="btn btn-ghost" onclick="playSound('click'); goTo('voice')">${t("addDetail")}</button>
              <button class="btn btn-primary" onclick="playSound('click'); loadRecommendation()">${t("seeGap")}</button>
            </div>
          </div>
        </div>
      </div>
    `;
  },

  skillgap: () => {
    if (state.loading.rec) return loadingState(t("skillGapTitle"), t("skillGapDesc"));
    if (state.errors.rec) return errorState(state.errors.rec, "skillgap");
    if (!state.skillGap) return emptyState(t("noGap"), t("noGapDesc"), "profile", t("goVoice"));

    const g = state.skillGap;
    const pct = 100 - g.gap_percent;
    return `
      <div class="screen">
        ${sceneMascot(t("youGotThis"))}
        ${stickyNotes([t("betterSkills"), t("progress")])}
        <div class="eyebrow">${stepText(4)}</div>
        <h2>${t("skillGapTitle")} ${mockTag()}</h2>
        <p class="lede">${t("skillGapDesc")}</p>
        <div class="card">
          <div class="skill-cols">
            <div class="skill-block">
              <h4>${t("have")}</h4>
              <div class="chip-list">${g.matched_skills.map(s => `<span class="chip chip-have">✅ ${escapeHtml(s)}</span>`).join("")}</div>
            </div>
            <div class="skill-block">
              <h4>${t("build")}</h4>
              <div class="chip-list">${g.missing_skills.map(s => `<span class="chip chip-need">🎯 ${escapeHtml(s)}</span>`).join("")}</div>
            </div>
          </div>
          <div class="gap-bar-wrap">
            <div class="gap-bar-track"><div class="gap-bar-fill" style="--fillw:${pct}%"></div></div>
            <div class="gap-bar-caption"><span>${pct}${t("match")}</span><span>${g.missing_skills.length} ${t("skillsToClose")}</span></div>
          </div>
        </div>
        <div class="actions">
          <button class="btn btn-ghost" onclick="playSound('click'); goTo('profile')">${t("backProfile")}</button>
          <button class="btn btn-primary" onclick="playSound('click'); goTo('nsqf')">${t("seeTraining")}</button>
        </div>
      </div>
    `;
  },

  nsqf: () => {
    if (!state.recommendation) return emptyState(t("noPath"), t("noPathDesc"), "skillgap", t("goGap"));
    return `
      <div class="screen">
        ${sceneMascot(t("learnBuild"))}
        ${stickyNotes([t("learnBuildGrow")])}
        <div class="eyebrow">${stepText(5)}</div>
        <h2>${t("trainingTitle")} ${mockTag()}</h2>
        <p class="lede">${t("trainingDesc")}</p>
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
          <button class="btn btn-ghost" onclick="playSound('click'); goTo('skillgap')">${t("back")}</button>
          <button class="btn btn-primary" onclick="playSound('click'); goTo('occupation')">${t("bestFit")}</button>
        </div>
      </div>
    `;
  },

  occupation: () => {
    if (!state.recommendation) return emptyState(t("noMatch"), t("noMatchDesc"), "skillgap", t("goGap"));
    const r = state.recommendation.rec;
    return `
      <div class="screen">
        ${sceneMascot(t("greatChoice"))}
        ${stickyNotes([t("canDo")])}
        <div class="eyebrow">${stepText(6)}</div>
        <h2>${t("occupationTitle")} ${mockTag()}</h2>
        <p class="lede">${t("occupationDesc")}</p>
        <div class="card">
          <div class="score-wrap">
            <div class="score-ring" style="--pct:${r.compatibility_score}">
              <div class="score-num">${r.compatibility_score}<span>/ 100</span></div>
            </div>
            <div>
              <div class="occ-title">${escapeHtml(r.occupation)} 💼</div>
              <div class="occ-sub">${r.matched_skills.length} ${t("matched")} ${r.matched_skills.length + r.missing_skills.length}</div>
            </div>
          </div>
          <button class="explain-toggle" id="explainToggle">${t("why")} ▾</button>
          <div class="explain-body" id="explainBody">${escapeHtml(r.explanation)}</div>
        </div>
        <div class="actions">
          <button class="btn btn-ghost" onclick="playSound('click'); goTo('nsqf')">${t("back")}</button>
          <button class="btn btn-primary" id="toOpportunities">${t("seeOpp")}</button>
        </div>
      </div>
    `;
  },

  opportunities: () => {
    if (!state.recommendation) return emptyState(t("noOpp"), t("noOppDesc"), "skillgap", t("goGap"));
    const opps = state.recommendation.opportunities;
    return `
      <div class="screen">
        ${sceneMascot(t("dreamPlan"))}
        ${stickyNotes([t("newOpp"), t("brighter")])}
        <div class="eyebrow">${stepText(7)}</div>
        <h2>${t("opportunitiesTitle")} ${mockTag()}</h2>
        <p class="lede">${t("opportunitiesDesc")}</p>
        ${opps.map(o => `
          <div class="opp-card">
            <span class="opp-type ${o.type}">${escapeHtml(t(o.type + "Type"))}</span>
            <div class="opp-title">${escapeHtml(o.title)}</div>
            <div class="opp-meta">${escapeHtml(o.meta)}</div>
          </div>
        `).join("")}
        <div class="card" style="margin-top:18px; text-align:center;">
          <p class="lede" style="margin:0 0 14px;">${t("readAloud")}</p>
          <div class="actions" style="margin-top:0; justify-content:center;">
            <button class="btn btn-ghost" onclick="playSound('click'); goTo('occupation')">${t("back")}</button>
            <button class="btn btn-primary" id="playTts">${t("play")}</button>
          </div>
        </div>
      </div>
    `;
  },
};

function mockTag() {
  return state.usingMockData ? `<span class="mock-badge">${t("demo")}</span>` : "";
}

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
    <div class="state-title">${timeout ? t("timeout") : t("error")}</div>
    <div class="state-desc">${escapeHtml(err.message)}</div>
    <button class="btn btn-primary" onclick="retry('${retryStep}')">${t("retry")}</button>
  </div></div>`;
}

function retry(step) {
  playSound("click");
  if (step === "profile") { state.errors.profile = null; processTranscript(state.transcript); }
  if (step === "skillgap") { state.errors.rec = null; loadRecommendation(); }
}

// ---------------------- Screen-specific event binding ----------------------
function bindScreenEvents(step) {
  if (step === "landing") {
    document.getElementById("heroStart").addEventListener("click", () => {
      playSound("success");
      confettiBurst(document.getElementById("heroStart"));
      setTimeout(() => goTo("language"), 300);
    });
    document.getElementById("bandCtaStart").addEventListener("click", () => {
      playSound("click");
      goTo("language");
    });
    const landingLanguage = document.querySelector(".js-landing-language");
    landingLanguage?.addEventListener("change", (e) => {
      playSound("click");
      state.language = e.target.value;
      setDocumentLanguage();
      render();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    document.getElementById("heroVoiceOver").addEventListener("click", (e) => {
      const btn = e.currentTarget;
      const mascotWrap = document.getElementById("mascotWrap");
      const greeting = t("heroGreeting");
      btn.textContent = t("speaking");
      btn.classList.add("speaking-pulse");
      if (mascotWrap) mascotWrap.classList.add("speaking");
      const started = speak(greeting, {
        lang: SPEECH_LOCALES[state.language] || "en-IN",
        onEnd: () => {
          btn.textContent = t("hear");
          btn.classList.remove("speaking-pulse");
          if (mascotWrap) mascotWrap.classList.remove("speaking");
        },
      });
      if (!started) {
        btn.textContent = t("voiceUnsupported");
        btn.classList.remove("speaking-pulse");
        if (mascotWrap) mascotWrap.classList.remove("speaking");
      }
    });

    const navHome = document.querySelector('[data-nav="home"]');
    const navAbout = document.querySelector('[data-nav="about"]');
    const navFeatures = document.querySelector('[data-nav="features"]');
    const navHow = document.querySelector('[data-nav="how"]');
    const scrollToId = (id) => (e) => {
      e.preventDefault();
      playSound("click");
      document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
    };
    navHome?.addEventListener("click", (e) => { e.preventDefault(); playSound("click"); window.scrollTo({ top: 0, behavior: "smooth" }); });
    navAbout?.addEventListener("click", scrollToId("featuresSection"));
    navFeatures?.addEventListener("click", scrollToId("featuresSection"));
    navHow?.addEventListener("click", scrollToId("howSectionTarget"));
    return;
  }

  if (step === "language") {
    document.querySelectorAll(".lang-card").forEach(card => {
      card.addEventListener("click", () => {
        playSound("click");
        state.language = card.dataset.lang;
        render();
      });
    });
  }

  if (step === "voice") {
    const micBtn = document.getElementById("micBtn");
    const status = document.getElementById("voiceStatus");
    const transcriptBox = document.getElementById("transcriptBox");
    const waveform = document.getElementById("waveform");

    if (!speechSupported()) {
      micBtn.disabled = true;
      micBtn.style.opacity = "0.4";
      micBtn.style.cursor = "not-allowed";
    } else {
      micBtn.addEventListener("click", () => toggleRealListening(micBtn, status, transcriptBox, waveform));
    }

    document.getElementById("fallbackSend").addEventListener("click", submitFallback);
    document.getElementById("fallbackInput").addEventListener("keydown", (e) => {
      if (e.key === "Enter") submitFallback();
    });

    function submitFallback() {
      const val = document.getElementById("fallbackInput").value.trim();
      if (!val) return;
      playSound("click");
      status.textContent = t("processing");
      processTranscript(val);
    }
  }

  if (step === "occupation") {
    const toggle = document.getElementById("explainToggle");
    const body = document.getElementById("explainBody");
    if (toggle) {
      toggle.addEventListener("click", () => {
        playSound("click");
        body.classList.toggle("show");
        toggle.textContent = body.classList.contains("show") ? `${t("why")} ▴` : `${t("why")} ▾`;
      });
    }
    const toOpp = document.getElementById("toOpportunities");
    if (toOpp) {
      toOpp.addEventListener("click", (e) => {
        playSound("success");
        confettiBurst(e.currentTarget);
        setTimeout(() => goTo("opportunities"), 350);
      });
    }
  }

  if (step === "opportunities") {
    const playBtn = document.getElementById("playTts");
    if (playBtn) {
      playBtn.addEventListener("click", () => {
        playSound("whoosh");
        playBtn.textContent = t("playing");
        // REAL INTEGRATION: call M3's TTS endpoint and play returned audio.
        setTimeout(() => { playBtn.textContent = t("play"); }, 1600);
      });
    }
  }
}

// ---------------------- Real speech-to-text (Web Speech API) ---------------
// This runs entirely in the browser — no backend call needed to turn the
// user's voice into text. Supported today in Chrome/Edge (desktop &
// Android). Not supported in Firefox or most iOS browsers — speechSupported()
// detects that and the UI falls back to the text box automatically.
function speechSupported() {
  return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
}

const SPEECH_LOCALES = { en: "en-IN", hi: "hi-IN", kn: "kn-IN", ta: "ta-IN", te: "te-IN", bn: "bn-IN" };

let recognizer = null;
let isListening = false;

function toggleRealListening(micBtn, status, transcriptBox, waveform) {
  if (isListening) {
    recognizer && recognizer.stop();
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognizer = new SpeechRecognition();
  recognizer.lang = SPEECH_LOCALES[state.language] || "en-IN";
  recognizer.interimResults = true;
  recognizer.continuous = false;
  recognizer.maxAlternatives = 1;

  let finalTranscript = "";

  recognizer.onstart = () => {
    isListening = true;
    micBtn.classList.add("listening");
    waveform.classList.add("live");
    playSound("mic-on");
    startMicPops(micBtn);
    status.textContent = t("listening");
    transcriptBox.classList.remove("show");
    transcriptBox.textContent = "";
  };

  recognizer.onresult = (event) => {
    let interim = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const chunk = event.results[i][0].transcript;
      if (event.results[i].isFinal) finalTranscript += chunk + " ";
      else interim += chunk;
    }
    transcriptBox.textContent = (finalTranscript + interim).trim();
    transcriptBox.classList.add("show");
  };

  recognizer.onerror = (event) => {
    stopListeningUI(micBtn, waveform);
    playSound("error");
    if (event.error === "not-allowed" || event.error === "service-not-allowed") {
      status.textContent = t("permission");
    } else if (event.error === "no-speech") {
      status.textContent = t("noSpeech");
    } else {
      status.textContent = t("voiceProblem");
    }
  };

  recognizer.onend = () => {
    stopListeningUI(micBtn, waveform);
    const text = finalTranscript.trim();
    if (text) {
      status.textContent = t("gotIt");
      playSound("mic-off");
      processTranscript(text);
    } else if (status.textContent === "Listening… speak now") {
      status.textContent = t("tapMic");
    }
  };

  recognizer.start();
}

function stopListeningUI(micBtn, waveform) {
  isListening = false;
  micBtn.classList.remove("listening");
  waveform.classList.remove("live");
  stopMicPops();
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
    playSound("success");
  } catch (e) {
    state.errors.profile = e;
    playSound("error");
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
    const result = await Api.getRecommendation(state.profile.entities);
    state.skillGap = result.skillGap;
    state.recommendation = {
      pathway: result.nsqf_pathway,
      rec: result.recommendation,
      opportunities: result.opportunities,
    };
    playSound("success");
  } catch (e) {
    state.errors.rec = e;
    playSound("error");
  } finally {
    state.loading.rec = false;
    render();
  }
}

function toggleSound() {
  state.soundOn = !state.soundOn;
  document.querySelectorAll(".js-sound-toggle").forEach(el => el.textContent = state.soundOn ? "🔊" : "🔇");
  if (state.soundOn) playSound("click");
}

// ---------------------- Utilities ------------------------------------------
function escapeHtml(str) {
  return String(str ?? "").replace(/[&<>"']/g, m => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
  }[m]));
}
