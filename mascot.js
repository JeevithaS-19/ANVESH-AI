/* =========================================================================
   ANVESH AI — Member 1 Frontend Prototype
   mascot.js — original illustrated robot voice-assistant (pure SVG,
   no stock imagery, no real people — safe to reuse anywhere).
   Redesigned to match the rounded navy/glass robot look from the
   reference hero image: soft rounded body, glowing cyan face, small
   headphone ears, one waving arm, glowing chest waveform.
   ========================================================================= */

const MASCOT_SVG = `
<svg viewBox="0 0 300 340" class="mascot-svg" aria-hidden="true">
  <defs>
    <linearGradient id="botBody" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F4F7FF"/>
      <stop offset="100%" stop-color="#D3DCF2"/>
    </linearGradient>
    <linearGradient id="botHead" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1B2A4A"/>
      <stop offset="100%" stop-color="#0E1830"/>
    </linearGradient>
    <radialGradient id="faceGlow" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#7DE6FF"/>
      <stop offset="100%" stop-color="#38BDF8"/>
    </radialGradient>
  </defs>

  <!-- sound rings -->
  <circle class="sound-ring r1" cx="150" cy="180" r="86" fill="none" stroke="#38BDF8" stroke-width="3" opacity="0"/>
  <circle class="sound-ring r2" cx="150" cy="180" r="86" fill="none" stroke="#A78BFA" stroke-width="3" opacity="0"/>
  <circle class="sound-ring r3" cx="150" cy="180" r="86" fill="none" stroke="#F472B6" stroke-width="3" opacity="0"/>

  <!-- ground glow -->
  <ellipse cx="150" cy="330" rx="78" ry="14" fill="#38BDF8" opacity="0.18"/>

  <!-- legs -->
  <rect x="118" y="272" width="24" height="46" rx="12" fill="url(#botBody)"/>
  <rect x="158" y="272" width="24" height="46" rx="12" fill="url(#botBody)"/>

  <!-- body -->
  <rect x="98" y="176" width="104" height="108" rx="34" fill="url(#botBody)"/>
  <!-- chest waveform -->
  <g stroke="#38BDF8" stroke-width="4" stroke-linecap="round" fill="none" class="chest-wave">
    <line x1="122" y1="232" x2="122" y2="232"><animate attributeName="y1" values="222;242;222" dur="1s" repeatCount="indefinite"/></line>
    <line x1="136" y1="232" x2="136" y2="232"><animate attributeName="y1" values="212;250;212" dur="0.9s" repeatCount="indefinite"/></line>
    <line x1="150" y1="232" x2="150" y2="232"><animate attributeName="y1" values="205;255;205" dur="1.1s" repeatCount="indefinite"/></line>
    <line x1="164" y1="232" x2="164" y2="232"><animate attributeName="y1" values="215;248;215" dur="0.85s" repeatCount="indefinite"/></line>
    <line x1="178" y1="232" x2="178" y2="232"><animate attributeName="y1" values="222;240;222" dur="1s" repeatCount="indefinite"/></line>
  </g>

  <!-- waving arm -->
  <g class="wave-arm">
    <rect x="192" y="188" width="20" height="70" rx="10" fill="url(#botBody)" transform="rotate(18 202 188)"/>
    <circle cx="234" cy="150" r="14" fill="#D3DCF2"/>
  </g>
  <!-- still arm -->
  <rect x="88" y="196" width="20" height="66" rx="10" fill="url(#botBody)" transform="rotate(-8 98 196)"/>

  <!-- head -->
  <rect x="88" y="66" width="124" height="110" rx="40" fill="url(#botHead)"/>
  <!-- headphone ears -->
  <path d="M92 100 Q60 100 60 140 Q60 168 92 168" stroke="#0E1830" stroke-width="14" fill="none" stroke-linecap="round"/>
  <path d="M208 100 Q240 100 240 140 Q240 168 208 168" stroke="#0E1830" stroke-width="14" fill="none" stroke-linecap="round"/>
  <circle cx="60" cy="140" r="16" fill="#1B2A4A"/>
  <circle cx="240" cy="140" r="16" fill="#1B2A4A"/>

  <!-- glowing face screen -->
  <rect x="112" y="98" width="76" height="52" rx="20" fill="#08101F"/>
  <circle class="eye eye-l" cx="134" cy="124" r="8" fill="url(#faceGlow)"/>
  <circle class="eye eye-r" cx="166" cy="124" r="8" fill="url(#faceGlow)"/>
  <path d="M132 138 Q150 148 168 138" stroke="#7DE6FF" stroke-width="3" fill="none" stroke-linecap="round"/>

  <!-- antenna -->
  <line x1="150" y1="66" x2="150" y2="46" stroke="#0E1830" stroke-width="6" stroke-linecap="round"/>
  <circle class="antenna-dot" cx="150" cy="40" r="8" fill="#F472B6"/>

  <!-- floating badges -->
  <g class="badge badge-1"><circle cx="46" cy="70" r="24" fill="#A78BFA"/><text x="46" y="77" font-size="22" text-anchor="middle">🎯</text></g>
  <g class="badge badge-2"><circle cx="260" cy="210" r="24" fill="#38BDF8"/><text x="260" y="217" font-size="22" text-anchor="middle">📚</text></g>
  <g class="badge badge-3"><circle cx="60" cy="300" r="22" fill="#F472B6"/><text x="60" y="307" font-size="20" text-anchor="middle">💼</text></g>
</svg>
`;
