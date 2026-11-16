#!/usr/bin/env python3
"""
Render a high-aesthetic Neofetch Terminal Card SVG (840 x 880)
that pairs seamlessly with stats.svg on the right.
No noisy ASCII blobs -- clean typography, crisp ASCII banner, specs, and glowing accents.
"""
import os
import sys

W, H = 840, 880
PAD = 28
TITLEBAR_H = 34

BG = "#0d1117"
BG2 = "#111722"
TILE = "#161b22"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
GREEN = "#3fb950"
CYAN = "#58a6ff"
BLUE = "#79c0ff"
YELLOW = "#d29922"
PURPLE = "#bc8cff"

# ASCII header emblem
ASCII_LOGO = [
    r"    ____  ____  ___   _____ ___    _   ________  __  __",
    r"   / __ \/ __ \/   | / ___//   |  / | / /_  __/ / / / /",
    r"  / /_/ / /_/ / /| | \__ \/ /| | /  |/ / / /   /_/ /_/ ",
    r" / ____/ _, _/ ___ |___/ / ___ |/ /|  / / /   _   _    ",
    r"/_/   /_/ |_/_/  |_/____/_/  |_/_/ |_/ /_/   (_) (_)   ",
]

SPECS = [
    ("USER", "prasanth@zodiac", CYAN, True),
    ("ROLE", "Full-Stack Software Engineer & AI Explorer", INK, False),
    ("EDU", "B.E. Computer Science & Engineering", INK, False),
    ("FOCUS", "Next.js Enterprise SaaS & Local LLM Pipelines", GREEN, False),
    ("FRONTEND", "Next.js 15, React 18, TypeScript, Tailwind CSS, Vite", BLUE, False),
    ("BACKEND", "Node.js, Express, MySQL, Python, RESTful APIs", YELLOW, False),
    ("AI / ML", "Ollama (LLaMA-3), Offline Scraping, Data Workflows", PURPLE, False),
    ("DEVOPS", "Git, GitHub Actions, AWS, Vercel, Docker", CYAN, False),
    ("PROJECTS", "College CMS, Company Intel AI, Billing SaaS, Valorae", INK, False),
    ("STATUS", "Available for high-impact roles & collaborations", GREEN, True),
]

def generate():
    svg_lines = []
    
    # 1. ASCII Logo rendering
    logo_top = TITLEBAR_H + 24
    line_h = 16
    for idx, line in enumerate(ASCII_LOGO):
        y = logo_top + idx * line_h
        delay = round(0.05 + idx * 0.05, 2)
        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        svg_lines.append(
            f'<text class="ascii-logo" x="{PAD + 10}" y="{y}" style="animation-delay:{delay}s">{escaped}</text>'
        )

    # Divider
    div_y = logo_top + len(ASCII_LOGO) * line_h + 16
    svg_lines.append(
        f'<line x1="{PAD}" y1="{div_y}" x2="{W - PAD}" y2="{div_y}" stroke="{FRAME}" stroke-width="1"/>'
    )

    # 2. Specs list
    specs_top = div_y + 26
    spec_gap = 32
    for idx, (label, val, col, bold) in enumerate(SPECS):
        y = specs_top + idx * spec_gap
        delay = round(0.3 + idx * 0.07, 2)
        weight = "700" if bold else "500"
        svg_lines.append(f'''
        <g class="spec-row" style="animation-delay:{delay}s">
          <text x="{PAD + 12}" y="{y}" fill="{CYAN}" font-size="13" font-weight="700" letter-spacing="1">{label}:</text>
          <text x="{PAD + 120}" y="{y}" fill="{col}" font-size="13.5" font-weight="{weight}">{val}</text>
        </g>
        ''')

    # 3. Terminal bottom box (Command & Palette)
    box_y = specs_top + len(SPECS) * spec_gap + 14
    box_h = H - box_y - PAD
    
    terminal_box = f'''
    <g class="term-box" style="animation-delay:1.05s">
      <rect x="{PAD}" y="{box_y}" width="{W - PAD * 2}" height="{box_h}" rx="8"
            fill="{TILE}" stroke="{FRAME}" stroke-width="1"/>
      
      <!-- Command prompt -->
      <text x="{PAD + 16}" y="{box_y + 28}" font-size="13" font-weight="600">
        <tspan fill="{GREEN}">prasanth@zodiac</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{BLUE}">~</tspan><tspan fill="{INK}">$</tspan>
        <tspan fill="{INK}"> npm run build &amp;&amp; ./deploy-featured.sh</tspan>
      </text>
      
      <text x="{PAD + 16}" y="{box_y + 54}" fill="{MUTED}" font-size="12.5" font-weight="500">
        <tspan fill="{GREEN}">✓</tspan> 6 production projects compiled • system optimal
      </text>

      <!-- Color dots -->
      <g transform="translate({PAD + 16}, {box_y + 82})">
        <circle cx="8" cy="0" r="7" fill="#0d1117" stroke="{FRAME}"/>
        <circle cx="30" cy="0" r="7" fill="#ff7b72"/>
        <circle cx="52" cy="0" r="7" fill="#3fb950"/>
        <circle cx="74" cy="0" r="7" fill="#d29922"/>
        <circle cx="96" cy="0" r="7" fill="#58a6ff"/>
        <circle cx="118" cy="0" r="7" fill="#bc8cff"/>
        <circle cx="140" cy="0" r="7" fill="#39c5cf"/>
        <circle cx="162" cy="0" r="7" fill="#e6edf3"/>
        <text x="184" y="5" class="cursor">_</text>
      </g>
    </g>
    '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Courier New,monospace">
<defs>
  <linearGradient id="wbg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{BG2}"/>
    <stop offset="100%" stop-color="{BG}"/>
  </linearGradient>
</defs>
<style>
  .ascii-logo {{
    fill: {CYAN};
    font-size: 13.5px;
    font-weight: 700;
    opacity: 0;
    animation: fadein 0.4s ease-out both;
  }}
  .spec-row {{
    opacity: 0;
    transform-box: fill-box;
    animation: slidein 0.35s cubic-bezier(0.2, 0.7, 0.2, 1) both;
  }}
  .term-box {{
    opacity: 0;
    animation: fadein 0.5s ease-out both;
  }}
  .cursor {{
    fill: {GREEN};
    font-weight: 700;
    font-size: 18px;
    animation: blink 1s steps(2, start) infinite;
  }}
  @keyframes fadein {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
  }}
  @keyframes slidein {{
    from {{ opacity: 0; transform: translateX(-12px); }}
    to {{ opacity: 1; transform: none; }}
  }}
  @keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .ascii-logo, .spec-row, .term-box {{ opacity: 1 !important; animation: none !important; }}
    .cursor {{ animation: none !important; }}
  }}
</style>

<!-- Terminal Frame -->
<rect width="{W}" height="{H}" rx="12" fill="url(#wbg)" stroke="{FRAME}" stroke-width="1"/>
<rect width="{W}" height="{TITLEBAR_H}" rx="12" fill="#161b22"/>
<rect y="{TITLEBAR_H-10}" width="{W}" height="10" fill="#161b22"/>
<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-width="1"/>

<!-- Titlebar Controls -->
<circle cx="20" cy="{TITLEBAR_H/2}" r="5" fill="#ff5f56"/>
<circle cx="36" cy="{TITLEBAR_H/2}" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="{TITLEBAR_H/2}" r="5" fill="#27c93f"/>
<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" font-weight="600" text-anchor="middle">
  neofetch - prasanth@zodiac
</text>

<!-- Terminal Content -->
{''.join(svg_lines)}
{terminal_box}
</svg>'''

    out_path = r"C:\Users\sarat\Documents\BLUE\Zodiac\neofetch.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {out_path}: {W}x{H}, {len(svg)} bytes")

if __name__ == "__main__":
    generate()
