# ANVESH AI - Frontend Prototype (Member 1)
## Update: bright animated redesign + live backend wiring

## Files

```
anvesh-frontend/
  index.html    -> markup + link/script tags only
  styles.css    -> bright theme, all colors as CSS variables, animations
  api.js        -> config, session state, and the REAL API layer (+ mock fallback)
  effects.js    -> sound cues (Web Audio, no audio files) + confetti + mic-pop particles
  app.js        -> router, screen templates, event binding
```

Open `index.html` in a browser (or serve the folder locally, see below) -
no build step, no install.

---

## PART 1 — What changed visually

- **Bright palette** instead of the earlier muted tones: violet/purple +
  hot pink + sky blue + yellow + mint, all defined as CSS variables at the
  top of `styles.css` (`--violet`, `--pink`, `--sky`, `--yellow`, `--mint`).
  Change the look of the whole app by editing those variables in one place.
- **Floating background blobs** - soft blurred color blobs drifting slowly
  behind the app for a lively, non-flat background.
- **Bouncy, glowing buttons** - buttons lift and glow on hover, squash
  slightly on click.
- **Animated journey tracker** - the current step pops and glows; completed
  steps turn into a green checkmark.
- **Voice screen "popping" visualization**:
  - the mic button pulses two expanding rings while listening
  - a 7-bar waveform bounces at different speeds while listening
  - small glowing bubbles "pop" upward from the mic every ~0.4s while
    listening (pure CSS/DOM particles, no images/canvas needed)
- **Confetti burst** - fires when you move from the occupation-match screen
  to the opportunities screen (the "you got a plan!" moment).
- **Animated score ring, skill-match bar, and gradient shimmer** on the
  skill-gap and occupation screens.
- **Sound cues** (Web Audio API - synthesized tones, no audio files to
  download or host): a click tone on buttons, a rising tone when the mic
  turns on / falling tone when it turns off, a 3-note success chime when
  data loads, soft "pop" blips while listening, and a descending tone on
  errors. There's a 🔊/🔇 toggle in the top bar - sound defaults on but is
  one tap to mute.
- All animations respect `prefers-reduced-motion` where practical.

## PART 2 — What changed under the hood (real backend wiring)

Per your teammate's message, Member 2's FastAPI backend (`member2-backend`
branch) now has these live:

| Endpoint | Used for |
|---|---|
| `GET /health` | shown live in the top bar as a status dot (green = online, red = offline/demo data, yellow = checking) |
| `POST /session/` | called once when the app loads, to get a `session_id` used on every later call |
| `POST /voice/process` | called with `{ text, language_code, session_id }` every time you speak or type - this is the real, working integration with Member 3's VoicePipeline |
| `POST /recommendations/` | called with the profile once you reach the skill-gap step |
| `GET /opportunities/` | called alongside recommendations for the final screen |
| `POST /profile/`, `GET /profile/{id}`, `GET /session/{id}` | not called yet from the UI - see "Not yet wired" below |

**Before you test against the real backend:** open `api.js` and set
```js
const API_BASE_URL = "http://localhost:8000"; // or wherever member2-backend is deployed
```
Your teammate mentioned they still need to add CORS on their side - until
that's done (or if the backend isn't running), every call **falls back
automatically to realistic mock data** so your UI never breaks. You'll see
a small "⚠ demo data" badge next to any screen currently showing mock
data instead of a real response, and the top-bar dot will read "Backend
offline (demo data)".

**Why the fallback matters right now:** `/recommendations/` and
`/opportunities/` are still placeholders on the backend per your
teammate's note, so even once CORS is fixed, those two will likely keep
falling back to mock data until M2 finishes them. `/voice/process` is
fully implemented on their end, so that one should start returning real
data as soon as `API_BASE_URL` and CORS are sorted.

### Not yet wired (nothing to build, just not connected yet)
- `POST /profile/` - could be called after `/voice/process` succeeds, to
  persist the profile server-side. Not required for the demo to work
  since `/voice/process` already returns everything the UI needs.
- `GET /session/{id}` / `GET /profile/{id}` - only needed if you add a
  "resume my session" feature later.

---

## PART 3 — Real voice capture (no backend needed for this part)

The mic button now uses the browser's built-in **Web Speech API**
(`SpeechRecognition` / `webkitSpeechRecognition`) to turn your actual voice
into real text, live, entirely in the browser:
- Tap the mic, speak, tap again (or pause) to finish.
- You'll see your real words appear in the transcript box as you talk.
- That real transcript — not a hardcoded sentence — is what gets sent to
  `/voice/process`.
- Language is passed through as a locale (`en-IN`, `hi-IN`, `kn-IN`,
  `ta-IN`, `te-IN`, `bn-IN`) matching whichever language is selected on
  step 1.

**Browser support:** works today in Chrome and Edge (desktop and
Android). It is **not** supported in Firefox or most iOS browsers — in
those cases the mic button is automatically disabled and the status text
tells the person to use the text box instead, which still works
everywhere.

**Why this didn't need to wait on the backend:** speech-to-text can
happen in two different places — in the browser (what this now does,
zero backend involvement) or on the server via Member 3's VoicePipeline
(what `/voice/process` currently expects as plain `text`, already
transcribed). Both are valid; this project's contract has the frontend
sending text, so doing the transcription step in the browser is a
complete, correct answer — not a workaround.

**If the team later wants server-side transcription instead** (e.g. for
better accuracy on Indian languages, or to reuse Member 3's Whisper-based
pipeline for the actual audio), that needs a new backend endpoint that
accepts an audio file/blob (today's `/voice/process` only accepts text).
That part genuinely would be Member 2/3's work — capturing the audio
itself and sending it up is still just a few lines in `app.js`
(`MediaRecorder` API) whenever they're ready for it.

## PART 4 — Landing page (landing.html)

A separate marketing "front door" for the project, distinct from the app
in `index.html`:

```
landing.html  -> editorial hero, steps grid, statement banner, footer
landing.css   -> its own palette + the hero/orb animations
landing.js    -> real voice-over via the browser's SpeechSynthesis API
```

- **Hero:** a dawn-gradient panel (deep indigo night fading to marigold)
  with an original illustrated "voice orb" character that rises up on
  load and radiates pulsing sound-wave rings — this stands in for the
  "person popping out" idea, without using stock photography of real
  people (which can't legally be reused here).
- **"▶ Hear ANVESH" button:** a genuinely working voice-over using the
  browser's built-in text-to-speech (no audio file, no backend). While
  it's actually speaking, the orb's mouth animates in sync; it stops the
  instant speech ends. Tap again to stop early.
- **Steps grid, statement banner, channel strip, footer:** editorial
  structure inspired by the reference you shared, rebuilt with ANVESH's
  own palette and real project content (the actual 4-step journey, the
  actual web/IVR/WhatsApp access channels from the plan, actual team/PS
  info) instead of placeholder text.
- **"Start speaking" / "Open the app"** buttons link straight into
  `index.html`, so `landing.html` is the site's front door and `index.html`
  is the working assistant.

To preview: open `landing.html` directly, or serve the folder locally (see
below) and visit it first — that's the intended entry point now.

## PART 4 — Landing/hero page redesign (bright, editorial, "wow" entry)

Added a brand-new **landing screen** (the `#landing` route, shown before
language selection) so the first thing a person sees isn't a plain form:

- **Full-width vibrant hero band** (violet → pink gradient) with a bold
  headline, a one-line pitch, and two CTAs: "Start with ANVESH" and
  "Hear ANVESH speak."
- **An original illustrated mascot character** (`mascot.js`) — a friendly
  waving voice-assistant figure with headphones and a mic, built entirely
  from SVG shapes. It pops up with a bounce on page load, idles with a
  gentle float, waves continuously, and has three floating skill/training/
  job badges orbiting it. Pulsing sound-wave rings radiate behind it,
  and while the voice-over is speaking it visibly pulses in sync.
- **A real voice-over** — "Hear ANVESH speak" uses the browser's built-in
  text-to-speech (`speechSynthesis`, added to `effects.js`) to actually
  read a welcome line out loud, synced to the mascot's speaking animation.
  No audio file, no backend call.
- **A feature strip** (4 cards: Talk naturally / See your skill gap / Get
  a training pathway / Real opportunities) — a condensed, visual preview
  of the 7-step journey.
- **A bold color-block CTA band** (deep plum/violet, matching the
  reference design's "Universal Wellness" band) with a big statement and
  a final "Begin your journey" button.
- **A dark footer band** with the brand name.

This was modeled after a reference beauty-brand design the user shared —
same idea of full-bleed color bands, a bold hero, and a strong visual
"hook" - but built with **original illustrated artwork instead of stock
photography** of real people, since real photos of people aren't
something this app has the rights to use in code. The mascot achieves the
same "someone's popping out of the screen to greet you" effect without
that licensing risk.

Clicking the ANVESH logo in the top bar, or navigating to `#landing`,
returns to this page at any time.

## Where to make changes
- **Colors, fonts, spacing, animation timing** -> `styles.css`
- **Sound cues or confetti/particle behavior** -> `effects.js`
- **Screen content / journey steps / adding a new screen** -> `app.js`
  (each screen is one function inside the `SCREENS` object)
- **Anything about the backend connection or endpoints** -> `api.js`

## How to run it
Double-click `index.html`, or - recommended, since browsers sometimes
block local file-to-file `<script src>` loading - run a local server from
inside this folder:
```
python3 -m http.server 8000
```
then open `http://localhost:8000`.

## Still needed before demo day
- Confirm `API_BASE_URL` and that M2 has added CORS, then flip real data
  on for `/voice/process`.
- Once M2 finishes `/recommendations/` and `/opportunities/`, the "⚠ demo
  data" badge on those screens should disappear on its own - no frontend
  changes needed if the response shape matches what's documented in
  `api.js`.
- Wire real audio capture (`MediaRecorder` API in `app.js`'s voice screen)
  instead of the simulated transcript.
- Add actual multilingual label translations for whichever languages the
  team commits to (the picker already supports Hindi, Kannada, Tamil,
  Telugu, Bengali - only English copy is written so far).

## PART 5 — Per-screen cinematic backgrounds + mascot everywhere (matches the mood-board mockups)

Every screen now has its own real photographic backdrop (in `assets/`),
matching the reference mockups exactly:

| Screen | Background file |
|---|---|
| Landing / Language / Voice | `bg-voice.jpg` |
| Profile | `bg-profile.jpg` |
| Skill Gap | `bg-skillgap.jpg` |
| Training Pathway (NSQF) | `bg-nsqf.jpg` |
| Occupation Match | `bg-occupation.jpg` |
| Opportunities | `bg-opportunities.jpg` |

**How it works:** `app.js` sets `document.body.dataset.scene = <step>` on
every render. `styles.css` has a `body[data-scene="..."]::before` rule per
screen that swaps the fixed background image, with a strong dark gradient
overlay (heavier on the left, where the real UI sits) so the actual
working text/buttons stay fully legible over the photo.

**Important limitation to know about:** the 6 reference images are
AI-generated *flattened mockups* — the headline text, buttons, and cards
you see in them are baked into the pixels, not separate layers. There
was no way to extract "just the background" from them. Instead, the dark
overlay is tuned strong enough to hide that baked-in fake text, and the
*real, working* headline/buttons/cards from this app sit on top of it.
The photographic mood (desk, city skyline, plants, books) comes through;
the fake text underneath does not.

**Also added, matching the mockups:**
- The mascot + a contextual speech bubble now appear on every inner
  screen (not just the landing page) — see `sceneMascot()` in `app.js`.
- Decorative handwritten-style notes ("Small steps, big dreams",
  "Progress not perfection", etc.) scattered per screen — see
  `stickyNotes()` in `app.js`. These hide on narrow screens to avoid
  clutter.
- The profile screen now has a left sidebar (Dashboard / My Profile /
  Learning Path / Skill Gap / Training / Opportunities), matching the
  reference profile mockup. The links are functional — they navigate to
  the matching screen.

**If you want unique images for the remaining screens** (language
selection currently reuses the voice screen's photo) or want to swap any
of these six for something else, generate a new image in the same style
and drop it into `assets/`, then update the matching `body[data-scene=...]`
rule in `styles.css` and, for the landing page specifically, the
`<img src="assets/...">` in `app.js`'s `landing` screen template.

## PART 6 — Landing hero corrected: one consistent photo, no duplicate mascot

Fixed a mismatch from the previous round: the landing page now uses its
own dedicated photo (`assets/bg-landing.jpg` — the mountain/sunset scene
with the person and the mascot already together in frame), instead of
reusing the voice screen's desk photo.

Since that photo already shows the mascot, the speech bubble, and the
Skills/Training/Jobs cards baked into the scene itself, the separate
floating SVG mascot that was previously drawn on top of the landing hero
has been removed — it was competing with the photo's own mascot instead
of matching it. The overlay gradient on landing is also lighter than on
other screens, specifically so the person and mascot in the photo stay
clearly visible; only the left third (where the real headline and
buttons sit) is darkened enough for legibility.

The "Hear ANVESH speak" button still works exactly as before (real
browser text-to-speech) — it now gives a subtle pulse on the button
itself while speaking, instead of animating a mascot that no longer
exists on this screen.

All 6 other screens (voice/language reuse `bg-voice.jpg`; profile,
skill-gap, NSQF, occupation, and opportunities each keep their own photo)
are unchanged from Part 5 and still show the custom SVG mascot + speech
bubble, since those photos don't already contain one.

## PART 7 — One consistent interior background, not one photo per screen

Per feedback, the per-screen photos (a different image behind each of
voice/profile/skillgap/nsqf/occupation/opportunities) were removed —
having a different image "pop" behind every step was distracting rather
than immersive.

Now:
- **Landing page** keeps its own dedicated photo (`assets/bg-landing.jpg`
  — the mountain/sunset scene) exactly as before.
- **Every other screen** shares one single background:
  `assets/bg-app.jpg`, a dark modern workspace photo (laptop with code,
  blurred city skyline at night). This is set once in `styles.css` on
  `body::before` and no longer changes per step.

The old per-screen images (`bg-voice.jpg`, `bg-profile.jpg`,
`bg-skillgap.jpg`, `bg-nsqf.jpg`, `bg-occupation.jpg`,
`bg-opportunities.jpg`) have been deleted from `assets/` since nothing
references them anymore.

If you want a different interior background later, replace
`assets/bg-app.jpg` with a new image of the same filename — no code
changes needed. If you want the background to vary by screen again,
reintroduce `body[data-scene="..."]::before` overrides in `styles.css`
(the `data-scene` attribute is still set on `<body>` by `app.js` on every
render, so the hook is still there — it's just unused for backgrounds now).
