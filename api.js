/* =========================================================================
   ANVESH AI — Member 1 Frontend Prototype
   api.js — app config, in-memory state, and the API layer.

   REAL BACKEND WIRING (Member 2 / FastAPI, branch member2-backend):
   - API_BASE_URL points at Member 2's FastAPI server. Change this to
     wherever it's actually deployed (or http://localhost:8000 while
     testing locally against their branch).
   - Every function below tries the REAL endpoint first. If it fails
     (backend not running yet, CORS not enabled yet, or a placeholder
     endpoint that isn't implemented yet — /recommendations/ and
     /opportunities/ are still placeholders per M2's update), it falls
     back to realistic mock data so the demo never breaks mid-flow.
   - Once M2's placeholders are filled in, the real response just starts
     flowing through automatically — nothing in app.js needs to change,
     since app.js only ever reads the shape documented next to each
     mock fallback below.
   ========================================================================= */

const API_BASE_URL = "http://localhost:8000"; // <-- change to M2's real deployed URL
const ENDPOINTS = {
  health:          `${API_BASE_URL}/health`,
  session:         `${API_BASE_URL}/session/`,
  profile:         `${API_BASE_URL}/profile/`,
  voiceProcess:    `${API_BASE_URL}/voice/process`,
  recommendations: `${API_BASE_URL}/recommendations/`,
  opportunities:   `${API_BASE_URL}/opportunities/`,
};

const REQUEST_TIMEOUT_MS = 6000;

// ---- Journey step definitions (used for the tracker + routing order) ----
const STEPS = [
  { id: "language",   label: "Language" },
  { id: "voice",       label: "Voice / Text" },
  { id: "profile",     label: "Profile" },
  { id: "skillgap",    label: "Skill Gap" },
  { id: "nsqf",        label: "Training Path" },
  { id: "occupation",  label: "Best Match" },
  { id: "opportunities", label: "Opportunities" },
];

const LANGUAGES = [
  { code: "en", native: "English", roman: "English" },
  { code: "hi", native: "हिन्दी", roman: "Hindi" },
  { code: "kn", native: "ಕನ್ನಡ", roman: "Kannada" },
  { code: "ta", native: "தமிழ்", roman: "Tamil" },
  { code: "te", native: "తెలుగు", roman: "Telugu" },
  { code: "bn", native: "বাংলা", roman: "Bengali" },
];

// ---- App state (in-memory only — no localStorage, per prototype rules) --
const state = {
  language: "en",
  transcript: "",
  sessionId: null,
  backendOnline: null,   // null = unknown/checking, true/false once checked
  usingMockData: false,  // flips true whenever a fallback was used, shown subtly in UI
  soundOn: true,
  profile: null,
  skillGap: null,
  recommendation: null,
  opportunities: null,
  loading: {},
  errors: {},
};

function ApiError(code, message) { this.code = code; this.message = message; }
function delay(ms) { return new Promise(r => setTimeout(r, ms)); }
function labelFor(code) { const l = LANGUAGES.find(l => l.code === code); return l ? l.roman : code; }

// ---- fetch with a timeout, so a dead/unreachable backend fails fast ------
async function fetchJson(url, options = {}) {
  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    if (!res.ok) throw new ApiError("HTTP_" + res.status, `Backend responded with ${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(t);
  }
}

// ============================== Api layer =================================
const Api = {

  // GET /health — used once on load to show a live backend status dot
  async checkHealth() {
    try {
      await fetchJson(ENDPOINTS.health);
      state.backendOnline = true;
    } catch (e) {
      state.backendOnline = false;
    }
    return state.backendOnline;
  },

  // POST /session/ — called once on app load
  async createSession() {
    try {
      const data = await fetchJson(ENDPOINTS.session, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ started_at: new Date().toISOString() }),
      });
      state.sessionId = data.session_id || data.id || null;
      return state.sessionId;
    } catch (e) {
      // Non-fatal — the demo can still run without a persisted session.
      state.sessionId = "local-" + Math.random().toString(36).slice(2, 10);
      return state.sessionId;
    }
  },

  // POST /voice/process — the real, working integration with M3's VoicePipeline
  async processInput(text, languageCode) {
    if (!text || text.trim().length < 2) {
      throw new ApiError("EMPTY_INPUT", "I didn't catch that. Try again or type your answer.");
    }
    try {
      const data = await fetchJson(ENDPOINTS.voiceProcess, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text,
          language_code: languageCode,
          session_id: state.sessionId,
        }),
      });
      state.usingMockData = false;
      // Expected shape from M2: language, intent, skills, job_domain,
      // entities, profile, profile_complete, next_question.
      return normalizeVoiceResponse(data, text, languageCode);
    } catch (e) {
      // Backend not up yet / CORS not enabled yet / endpoint erroring —
      // fall back to a realistic mock so the UI still demos end to end.
      state.usingMockData = true;
      await delay(900);
      return mockVoiceResponse(text, languageCode);
    }
  },

  // POST /recommendations/ (placeholder on M2's side right now) +
  // GET /opportunities/ (also a placeholder) — tried together, each
  // falling back independently to mock data if not yet implemented.
  async getRecommendation(profile) {
    let recPayload;
    try {
      recPayload = await fetchJson(ENDPOINTS.recommendations, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: state.sessionId, profile }),
      });
      state.usingMockData = false;
    } catch (e) {
      state.usingMockData = true;
      await delay(1000);
      recPayload = mockRecommendationPayload();
    }

    let opportunities;
    try {
      const oppUrl = `${ENDPOINTS.opportunities}?session_id=${encodeURIComponent(state.sessionId || "")}`;
      const oppData = await fetchJson(oppUrl);
      opportunities = oppData.opportunities || oppData;
    } catch (e) {
      state.usingMockData = true;
      opportunities = mockRecommendationPayload().opportunities;
    }

    return {
      skillGap: recPayload.skillGap || recPayload.skill_gap,
      nsqf_pathway: recPayload.nsqf_pathway,
      recommendation: recPayload.recommendation,
      opportunities,
    };
  },
};

// ---- Normalizers / mocks (kept here so app.js never has to guess shapes) --
function normalizeVoiceResponse(data, text, languageCode) {
  return {
    transcription: data.text || text,
    language: data.language || { language_code: languageCode, language: labelFor(languageCode) },
    intent: data.intent || "career_guidance",
    entities: data.entities || data.profile || {},
    profile_complete: !!data.profile_complete,
    next_question: data.next_question || "Could you tell me a bit more about your skills?",
  };
}

function mockVoiceResponse(text) {
  return {
    transcription: text,
    language: { language_code: state.language, language: labelFor(state.language), confidence: 0.94 },
    intent: "career_guidance",
    entities: {
      name: "Ravi Kumar",
      education: ["B.Tech, Computer Science"],
      skills: ["Python", "Basic Web Development"],
      experience: "1 year (freelance)",
      location: "Bengaluru, Karnataka",
      job_preference: "hybrid",
    },
    profile_complete: false,
    next_question: "What kind of work are you hoping to do next — technical, field-based, or something else?",
  };
}

function mockRecommendationPayload() {
  return {
    skillGap: {
      matched_skills: ["Python", "Web Development", "Communication"],
      missing_skills: ["Data Structures", "REST APIs", "Database Basics"],
      gap_percent: 34,
    },
    nsqf_pathway: [
      { level: "NSQF 5", title: "Full Stack Web Development", meta: "6-month certified course · linked to Data Structures, REST APIs" },
      { level: "NSQF 4", title: "Database Fundamentals (SQL)", meta: "6-week short course · linked to Database Basics" },
    ],
    recommendation: {
      occupation: "Junior Software Developer",
      compatibility_score: 78,
      matched_skills: ["Python", "Web Development", "Communication"],
      missing_skills: ["Data Structures", "REST APIs", "Database Basics"],
      explanation: "This pathway is recommended because the profile already covers the core programming and web-development skills most junior developer roles need. The missing skills are foundational and can be closed with a single short-format course, and Bengaluru has an active hiring market for this role.",
    },
    opportunities: [
      { type: "training", title: "Full Stack Development Bootcamp — NSDC Partner Center", meta: "Bengaluru · Starts in 12 days · Free (PM-AJAY linked)" },
      { type: "employment", title: "Junior Developer (Trainee) — local IT services firm", meta: "Bengaluru · Entry-level · Hybrid" },
      { type: "livelihood", title: "Freelance web development gigs via district skill portal", meta: "Remote-friendly · Flexible hours" },
    ],
  };
}
