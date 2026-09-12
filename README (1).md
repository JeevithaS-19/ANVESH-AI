# ANVESH AI - Frontend Prototype (Member 1)

Four separate files, ready to run as-is and easy to keep editing:

```
anvesh-frontend/
  index.html   -> markup + link/script tags only
  styles.css   -> every design token and style rule
  api.js       -> config, in-memory state, and the mock/real API layer
  app.js       -> router, screen templates, event binding
```

Covers every screen listed for Member 1 in the 2-Day Execution Plan (Section 7):

1. Language selection
2. Voice interaction + text fallback
3. Beneficiary profile (collected + missing fields)
4. Skill-gap screen
5. NSQF/training recommendation screen
6. Occupation match + compatibility score + "why this recommendation"
7. Opportunities screen (training / employment / livelihood)
8. Loading, empty, and error states on every data-dependent screen
9. Multilingual language picker (6 languages wired for the demo)
10. Responsive layout (mobile-first, works down to ~360px)

## How to run it
Open index.html in a browser - no build step, no install. Double-click the
file, or serve the folder with any static server (e.g. `python3 -m http.server`
from inside this folder) if your browser blocks local file-to-file loading.

## Where to make changes
- Colors, fonts, spacing, layout -> styles.css. All colors are CSS variables
  at the top of the file (--teal, --marigold, etc.) - change them once,
  everything updates.
- Screen content / journey steps / adding a new screen -> app.js. Each
  screen is one function inside the SCREENS object; the journey tracker
  order comes from the STEPS array in api.js.
- Anything about data or the backend connection -> api.js.

## Connecting to Member 2's real backend
api.js is the only file that should need touching for this:
1. Set API_BASE_URL near the top of api.js to the deployed FastAPI URL.
2. Set USE_MOCK = false.
3. Inside Api.processInput() and Api.getRecommendation(), uncomment and
   adapt the fetch() stubs already sketched in comments - they already
   point at the endpoints from the plan (/voice/process, /recommendation).
4. Confirm field names match exactly what M2 ships. app.js renders
   whatever shape api.js returns, so if the contract in Section 13 is
   respected, no rendering code needs to change.

## What's mocked vs. real right now
- Mocked: STT/TTS audio capture (voice input is simulated with a demo
  transcript after a short delay - swap for real audio capture + M2's
  endpoint), and all recommendation/skill-gap data (api.js).
- Real and working already: all navigation, all screen rendering, language
  switching, the text-fallback input path, loading/empty/error state
  handling, and the explainability toggle.

## Still needed before demo day
- Wire real audio capture (MediaRecorder API in app.js's voice screen) ->
  send to M2's /voice/process endpoint instead of the simulated transcript.
- Add actual multilingual label translations for whichever languages the
  team commits to (currently only English copy is written; the language
  picker already supports Hindi, Kannada, Tamil, Telugu, Bengali).
- Replace mock data in api.js with real fetch() calls once M2's API is live.
