/* =========================================================================
   ANVESH AI — Member 1 Frontend Prototype
   api.js — app config, in-memory state, and the mock/real API layer.

   HOW TO CONNECT TO THE REAL BACKEND (Member 2 / FastAPI):
   - Everything the UI needs is fetched through the `Api` object below.
   - Right now Api.* functions return mocked, delayed data shaped exactly
     like the contracts frozen in the team's execution plan (Section 13).
   - To go live: set USE_MOCK = false and set API_BASE_URL below, then
     implement the fetch() calls in each Api.* function (stubs are already
     sketched in comments next to each mock).
   ========================================================================= */

const USE_MOCK = true;
const API_BASE_URL = "https://your-anvesh-backend.example.com"; // <-- M2 sets this

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
  profile: null,      // filled after "voice/text" step, matches M3->M2 shape
  skillGap: null,      // matches M4 response shape
  recommendation: null,
  opportunities: null,
  loading: {},
  errors: {},
};

// =========================== Mock API layer ==============================
// Field names below mirror Section 13 "Exact Module Contracts" exactly,
// so swapping USE_MOCK to false and wiring real fetch() calls should not
// require changing any rendering code.
const Api = {

  // M3 -> M2 style response after voice/text input is processed
  async processInput(text, languageCode) {
    if (USE_MOCK) {
      await delay(1100);
      if (!text || text.trim().length < 2) {
        throw new ApiError("EMPTY_INPUT", "I didn't catch that. Try again or type your answer.");
      }
      return {
        transcription: text,
        language: { language_code: languageCode, language: labelFor(languageCode), confidence: 0.94 },
        intent: "career_guidance",
        entities: {
          name: "Hitha",
          education: ["B.Tech, Computer Science"],
          skills: ["Python", "Basic Web Development"],
          experience: "1 year (freelance)",
          location: "Bengaluru, Karnataka",
          job_preference: "hybrid",
        },
        profile_complete: false,
        next_question: "What kind of work are you hoping to do next — technical, field-based, or something else?",
      };
      // REAL CALL WOULD LOOK LIKE:
      // const res = await fetch(`${API_BASE_URL}/voice/process`, {
      //   method: "POST", headers: {"Content-Type":"application/json"},
      //   body: JSON.stringify({ text, language_code: languageCode })
      // });
      // if (!res.ok) throw new ApiError("BACKEND_ERROR", "Something went wrong. Please try again.");
      // return await res.json();
    }
  },

  // Returns skill-gap + recommendation + opportunities together for the prototype
  async getRecommendation(profile) {
    if (USE_MOCK) {
      await delay(1300);
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
      // REAL CALL:
      // const res = await fetch(`${API_BASE_URL}/recommendation`, {
      //   method: "POST", headers: {"Content-Type":"application/json"},
      //   body: JSON.stringify(profile)
      // });
      // if (!res.ok) throw new ApiError("BACKEND_ERROR", "Could not generate a recommendation right now.");
      // return await res.json();
    }
  },
};

function ApiError(code, message) { this.code = code; this.message = message; }
function delay(ms) { return new Promise(r => setTimeout(r, ms)); }
function labelFor(code) { const l = LANGUAGES.find(l => l.code === code); return l ? l.roman : code; }
