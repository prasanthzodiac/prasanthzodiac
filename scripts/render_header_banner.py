#!/usr/bin/env python3
"""
Generate a world-class, designer-level SVG banner for Prasanth Zodiac.
Committed locally as header-banner.svg so it never breaks, rate-limits, or goes down.
Dimensions: 1200 x 340 (responsive viewBox).
Features:
- Cosmic dark gradient with subtle isometric grid & glowing nebula orbs
- Zodiac constellation stars with CSS twinkle
- Premium gradient typography for 'PRASANTH ZODIAC'
- Polished badge pills for core stack & role
"""
import os

OUT_PATH = r"C:\Users\sarat\Documents\BLUE\Zodiac\header-banner.svg"

W, H = 1200, 340

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#050811" />
      <stop offset="50%" stop-color="#0a0f1d" />
      <stop offset="100%" stop-color="#0d1117" />
    </linearGradient>

    <!-- Glowing Nebula Orbs -->
    <radialGradient id="nebula-cyan" cx="20%" cy="30%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.22" />
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="nebula-purple" cx="80%" cy="60%" r="50%">
      <stop offset="0%" stop-color="#818cf8" stop-opacity="0.20" />
      <stop offset="100%" stop-color="#818cf8" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="nebula-emerald" cx="50%" cy="90%" r="40%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#10b981" stop-opacity="0" />
    </radialGradient>

    <!-- Typography Gradients -->
    <linearGradient id="title-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="40%" stop-color="#f0f9ff" />
      <stop offset="70%" stop-color="#7dd3fc" />
      <stop offset="100%" stop-color="#38bdf8" />
    </linearGradient>

    <linearGradient id="badge-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#818cf8" stop-opacity="0.15" />
    </linearGradient>

    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.5" />
      <stop offset="50%" stop-color="#818cf8" stop-opacity="0.2" />
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.5" />
    </linearGradient>

    <!-- Subtle Grid Pattern -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#38bdf8" stroke-width="0.75" stroke-opacity="0.04" />
      <circle cx="40" cy="40" r="1" fill="#38bdf8" fill-opacity="0.12" />
    </pattern>
  </defs>

  <style>
    @keyframes pulse {{
      0%, 100% {{ opacity: 0.18; transform: scale(1); }}
      50% {{ opacity: 0.28; transform: scale(1.04); }}
    }}
    @keyframes twinkle {{
      0%, 100% {{ opacity: 0.3; transform: scale(0.8); }}
      50% {{ opacity: 1; transform: scale(1.2); }}
    }}
    @keyframes float {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-4px); }}
    }}
    @keyframes sweep {{
      0% {{ transform: translateX(-100%); }}
      100% {{ transform: translateX(200%); }}
    }}
    .glow-cyan {{ animation: pulse 6s ease-in-out infinite; transform-origin: 20% 30%; }}
    .glow-purple {{ animation: pulse 7s ease-in-out infinite alternate; transform-origin: 80% 60%; }}
    .star-1 {{ animation: twinkle 3s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
    .star-2 {{ animation: twinkle 4s ease-in-out infinite 1.5s; transform-box: fill-box; transform-origin: center; }}
    .star-3 {{ animation: twinkle 3.5s ease-in-out infinite 0.7s; transform-box: fill-box; transform-origin: center; }}
    .main-title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'SF Pro Display', Roboto, 'Helvetica Neue', sans-serif; }}
    .sub-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
  </style>

  <!-- Background Base -->
  <rect width="{W}" height="{H}" rx="16" fill="url(#bg-grad)" stroke="#1e293b" stroke-width="1.5" />
  <rect width="{W}" height="{H}" rx="16" fill="url(#grid)" />

  <!-- Ambient Glows -->
  <circle cx="240" cy="100" r="280" fill="url(#nebula-cyan)" class="glow-cyan" />
  <circle cx="960" cy="200" r="300" fill="url(#nebula-purple)" class="glow-purple" />
  <circle cx="600" cy="300" r="220" fill="url(#nebula-emerald)" />

  <!-- Constellation Nodes & Zodiac Stars -->
  <g stroke="#38bdf8" stroke-width="0.8" stroke-opacity="0.2" fill="none">
    <line x1="80" y1="60" x2="160" y2="110" />
    <line x1="160" y1="110" x2="220" y2="70" />
    <line x1="220" y1="70" x2="310" y2="120" />
    <line x1="1020" y1="80" x2="1090" y2="140" />
    <line x1="1090" y1="140" x2="1140" y2="90" />
  </g>

  <!-- Twinkling Star Points -->
  <circle cx="80" cy="60" r="2" fill="#bae6fd" class="star-1" />
  <circle cx="160" cy="110" r="2.5" fill="#ffffff" class="star-2" />
  <circle cx="220" cy="70" r="2" fill="#38bdf8" class="star-3" />
  <circle cx="310" cy="120" r="3" fill="#ffffff" class="star-1" />
  <circle cx="1020" cy="80" r="2" fill="#c084fc" class="star-2" />
  <circle cx="1090" cy="140" r="3" fill="#ffffff" class="star-3" />
  <circle cx="1140" cy="90" r="2" fill="#818cf8" class="star-1" />
  <circle cx="920" cy="50" r="1.5" fill="#ffffff" class="star-2" />
  <circle cx="140" cy="260" r="2" fill="#38bdf8" class="star-3" />
  <circle cx="1060" cy="280" r="2.5" fill="#ffffff" class="star-1" />

  <!-- Center Content Container -->
  <g transform="translate(600, 170)" text-anchor="middle">
    <!-- Top Pill Badge -->
    <g transform="translate(0, -96)">
      <rect x="-190" y="-15" width="380" height="30" rx="15" fill="url(#badge-grad)" stroke="url(#border-grad)" stroke-width="1" />
      <circle cx="-168" cy="0" r="4" fill="#38bdf8" />
      <text x="10" y="4.5" fill="#e0f2fe" font-size="11.5" font-weight="700" letter-spacing="2.5" class="sub-text">
        FULL-STACK DEVELOPER &amp; AI EXPLORER
      </text>
    </g>

    <!-- Main Name Title -->
    <text x="0" y="-12" fill="url(#title-grad)" font-size="58" font-weight="900" letter-spacing="3" class="main-title">
      PRASANTH ZODIAC
    </text>

    <!-- Subtitle / Mission -->
    <text x="0" y="32" fill="#94a3b8" font-size="16" font-weight="500" letter-spacing="0.8" class="main-title">
      Building scalable web applications, enterprise platforms &amp; intelligent AI systems
    </text>

    <!-- Tech Stack Mini Badges Bar -->
    <g transform="translate(0, 78)">
      <!-- Pill 1 -->
      <g transform="translate(-325, 0)">
        <rect x="-48" y="-13" width="96" height="26" rx="13" fill="#1e293b" stroke="#334155" stroke-width="1" />
        <text x="0" y="4" fill="#38bdf8" font-size="11" font-weight="600" class="sub-text">Next.js 15</text>
      </g>
      <!-- Pill 2 -->
      <g transform="translate(-195, 0)">
        <rect x="-48" y="-13" width="96" height="26" rx="13" fill="#1e293b" stroke="#334155" stroke-width="1" />
        <text x="0" y="4" fill="#60a5fa" font-size="11" font-weight="600" class="sub-text">React 18</text>
      </g>
      <!-- Pill 3 -->
      <g transform="translate(-65, 0)">
        <rect x="-55" y="-13" width="110" height="26" rx="13" fill="#1e293b" stroke="#334155" stroke-width="1" />
        <text x="0" y="4" fill="#38bdf8" font-size="11" font-weight="600" class="sub-text">TypeScript</text>
      </g>
      <!-- Pill 4 -->
      <g transform="translate(65, 0)">
        <rect x="-44" y="-13" width="88" height="26" rx="13" fill="#1e293b" stroke="#334155" stroke-width="1" />
        <text x="0" y="4" fill="#facc15" font-size="11" font-weight="600" class="sub-text">Python</text>
      </g>
      <!-- Pill 5 -->
      <g transform="translate(185, 0)">
        <rect x="-48" y="-13" width="96" height="26" rx="13" fill="#1e293b" stroke="#334155" stroke-width="1" />
        <text x="0" y="4" fill="#4ade80" font-size="11" font-weight="600" class="sub-text">Node.js</text>
      </g>
      <!-- Pill 6 -->
      <g transform="translate(320, 0)">
        <rect x="-60" y="-13" width="120" height="26" rx="13" fill="#1e293b" stroke="#334155" stroke-width="1" />
        <text x="0" y="4" fill="#c084fc" font-size="11" font-weight="600" class="sub-text">Ollama (LLaMA-3)</text>
      </g>
    </g>
  </g>
</svg>
'''

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Generated {OUT_PATH}: {len(svg)} bytes")
