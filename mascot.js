/* =========================================================================
   ANVESH AI — Member 1 Frontend Prototype
   mascot.js — original illustrated voice-assistant character (pure SVG,
   no stock photography / no real people — safe to use and reuse freely).
   Exported as a template string so app.js can drop it into the landing
   hero without inlining a huge SVG blob in app.js itself.
   ========================================================================= */

const MASCOT_SVG = `
<svg viewBox="0 0 320 380" class="mascot-svg" aria-hidden="true">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF3D81"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
    <linearGradient id="headGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFE8A3"/>
      <stop offset="100%" stop-color="#FDBF5A"/>
    </linearGradient>
    <radialGradient id="ringGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- sound rings -->
  <circle class="sound-ring r1" cx="160" cy="190" r="90" fill="none" stroke="#38BDF8" stroke-width="4" opacity="0"/>
  <circle class="sound-ring r2" cx="160" cy="190" r="90" fill="none" stroke="#FACC15" stroke-width="4" opacity="0"/>
  <circle class="sound-ring r3" cx="160" cy="190" r="90" fill="none" stroke="#FF3D81" stroke-width="4" opacity="0"/>

  <!-- ground glow -->
  <ellipse cx="160" cy="352" rx="92" ry="16" fill="#5B21B6" opacity="0.18"/>

  <!-- body -->
  <path d="M100 380 L100 260 Q100 190 160 190 Q220 190 220 260 L220 380 Z" fill="url(#bodyGrad)"/>

  <!-- waving arm -->
  <g class="wave-arm">
    <path d="M206 220 Q252 200 258 150" stroke="url(#bodyGrad)" stroke-width="26" stroke-linecap="round" fill="none"/>
    <circle cx="259" cy="146" r="16" fill="#FDBF5A"/>
  </g>

  <!-- still arm holding mic -->
  <path d="M114 225 Q84 245 82 285" stroke="url(#bodyGrad)" stroke-width="24" stroke-linecap="round" fill="none"/>
  <g transform="translate(66,272)">
    <rect x="0" y="0" width="26" height="40" rx="13" fill="#FF3D81"/>
    <rect x="10" y="38" width="6" height="16" fill="#5B21B6"/>
    <rect x="2" y="52" width="22" height="6" rx="3" fill="#5B21B6"/>
  </g>

  <!-- head -->
  <circle cx="160" cy="140" r="66" fill="url(#headGrad)"/>

  <!-- headphone band -->
  <path d="M100 118 Q160 40 220 118" stroke="#5B21B6" stroke-width="10" fill="none" stroke-linecap="round"/>
  <rect x="88" y="112" width="20" height="34" rx="10" fill="#5B21B6"/>
  <rect x="212" y="112" width="20" height="34" rx="10" fill="#5B21B6"/>

  <!-- face -->
  <circle cx="138" cy="142" r="7" fill="#241536"/>
  <circle cx="182" cy="142" r="7" fill="#241536"/>
  <path d="M136 168 Q160 188 184 168" stroke="#241536" stroke-width="6" fill="none" stroke-linecap="round"/>
  <circle cx="118" cy="156" r="9" fill="#FF3D81" opacity="0.35"/>
  <circle cx="202" cy="156" r="9" fill="#FF3D81" opacity="0.35"/>

  <!-- floating badges -->
  <g class="badge badge-1"><circle cx="42" cy="90" r="26" fill="#FACC15"/><text x="42" y="97" font-size="24" text-anchor="middle">🎯</text></g>
  <g class="badge badge-2"><circle cx="278" cy="230" r="26" fill="#34D399"/><text x="278" y="237" font-size="24" text-anchor="middle">📚</text></g>
  <g class="badge badge-3"><circle cx="60" cy="330" r="24" fill="#38BDF8"/><text x="60" y="337" font-size="22" text-anchor="middle">💼</text></g>
</svg>
`;
