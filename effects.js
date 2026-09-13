/* =========================================================================
   ANVESH AI — Member 1 Frontend Prototype
   effects.js — sound cues (Web Audio, no audio files needed) + confetti
   burst + tiny particle "pop" effect for the voice button.
   Toggle sound off any time via state.soundOn (wired to the topbar button).
   ========================================================================= */

let audioCtx = null;
function getCtx() {
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  return audioCtx;
}

// Simple tone/chime generator — no external audio files required.
function tone(freq, startTime, duration, type = "sine", gain = 0.08) {
  const ctx = getCtx();
  const osc = ctx.createOscillator();
  const g = ctx.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, startTime);
  g.gain.setValueAtTime(0, startTime);
  g.gain.linearRampToValueAtTime(gain, startTime + 0.02);
  g.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);
  osc.connect(g).connect(ctx.destination);
  osc.start(startTime);
  osc.stop(startTime + duration + 0.02);
}

function playSound(name) {
  if (!state.soundOn) return;
  try {
    const ctx = getCtx();
    const now = ctx.currentTime;
    if (name === "click")   tone(520, now, 0.08, "sine", 0.06);
    if (name === "mic-on")  { tone(440, now, 0.12, "sine", 0.07); tone(660, now + 0.08, 0.14, "sine", 0.06); }
    if (name === "mic-off") { tone(660, now, 0.08, "sine", 0.05); tone(440, now + 0.06, 0.1, "sine", 0.05); }
    if (name === "success") { tone(523, now, 0.12, "triangle", 0.07); tone(659, now + 0.1, 0.12, "triangle", 0.07); tone(784, now + 0.2, 0.22, "triangle", 0.08); }
    if (name === "pop")     tone(880 + Math.random() * 200, now, 0.09, "square", 0.03);
    if (name === "whoosh")  tone(180, now, 0.18, "sawtooth", 0.03);
    if (name === "error")   { tone(220, now, 0.16, "sawtooth", 0.05); tone(160, now + 0.12, 0.2, "sawtooth", 0.05); }
  } catch (e) { /* audio not available — fail silently, never block the UI */ }
}

// ---- Confetti burst (pure DOM, no canvas needed) --------------------------
function confettiBurst(originEl) {
  const colors = ["#FF3D81", "#7C3AED", "#FACC15", "#38BDF8", "#34D399", "#FB923C"];
  const rect = originEl ? originEl.getBoundingClientRect() : { left: window.innerWidth / 2, top: window.innerHeight / 3, width: 0, height: 0 };
  const originX = rect.left + rect.width / 2;
  const originY = rect.top + rect.height / 2;

  for (let i = 0; i < 26; i++) {
    const piece = document.createElement("div");
    piece.className = "confetti-piece";
    const size = 6 + Math.random() * 6;
    piece.style.width = size + "px";
    piece.style.height = (size * 0.4) + "px";
    piece.style.background = colors[i % colors.length];
    piece.style.left = originX + "px";
    piece.style.top = originY + "px";
    const angle = Math.random() * Math.PI * 2;
    const dist = 90 + Math.random() * 140;
    const dx = Math.cos(angle) * dist;
    const dy = Math.sin(angle) * dist - 60;
    const rot = (Math.random() * 720 - 360) + "deg";
    piece.style.setProperty("--dx", dx + "px");
    piece.style.setProperty("--dy", dy + "px");
    piece.style.setProperty("--rot", rot);
    piece.style.animationDelay = (Math.random() * 0.15) + "s";
    document.body.appendChild(piece);
    setTimeout(() => piece.remove(), 1400);
  }
}

// ---- Real voice-over (Web Speech Synthesis — no audio files needed) ------
// speak() reads text out loud using the browser's built-in TTS voice.
// onStart/onEnd let the caller sync a mascot animation to when it's talking.
function speak(text, { onStart, onEnd, lang = "en-IN" } = {}) {
  if (!("speechSynthesis" in window)) {
    if (onEnd) onEnd();
    return false;
  }
  window.speechSynthesis.cancel(); // stop anything already playing
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = lang;
  utter.rate = 0.98;
  utter.pitch = 1.05;
  utter.onstart = () => onStart && onStart();
  utter.onend = () => onEnd && onEnd();
  utter.onerror = () => onEnd && onEnd();
  window.speechSynthesis.speak(utter);
  return true;
}

function stopSpeaking() {
  if ("speechSynthesis" in window) window.speechSynthesis.cancel();
}

let popInterval = null;
function startMicPops(micEl) {
  stopMicPops();
  popInterval = setInterval(() => {
    const rect = micEl.getBoundingClientRect();
    const piece = document.createElement("div");
    piece.className = "voice-pop";
    const size = 8 + Math.random() * 14;
    piece.style.width = piece.style.height = size + "px";
    piece.style.left = (rect.left + rect.width / 2 + (Math.random() * 60 - 30)) + "px";
    piece.style.top = (rect.top + 10) + "px";
    document.body.appendChild(piece);
    playSound("pop");
    setTimeout(() => piece.remove(), 1100);
  }, 420);
}
function stopMicPops() {
  if (popInterval) { clearInterval(popInterval); popInterval = null; }
}
