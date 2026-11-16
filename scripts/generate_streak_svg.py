#!/usr/bin/env python3
"""Generate an animated GitHub-streak SVG (squares light up diagonally with flash).
Designed to run in GitHub Actions daily to stay live without any 3rd-party dependencies.
Usage: python scripts/generate_streak_svg.py [username] [output.svg]
"""
import sys, json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
USER = sys.argv[1] if len(sys.argv) > 1 else "prasanthzodiac"
OUT  = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "contrib-heatmap.svg")

def get_data(user):
    snap = os.path.join(ROOT, "data", "contributions.json")
    if os.path.exists(snap):
        with open(snap, "r", encoding="utf-8") as f:
            d = json.load(f)
        if d.get("username", "").lower() == user.lower() and all("level" in x for x in d.get("days", [])):
            return {"contributions": d["days"], "total": d["total_contributions"]}
    raise RuntimeError(f"Snapshot {snap} not found. Run fetch_contributions.py first.")

data = get_data(USER)
contribs = data["contributions"]
total = data["total"]

CELL, GAP, RAD, LEFT, TOP = 13, 3, 2.5, 34, 28
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
FLASH = "#b4ffaa"
GRAY = "#7d8590"
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

n = len(contribs)
NW = (n + 6) // 7
W = LEFT + NW*(CELL+GAP) + 16
H = TOP + 7*(CELL+GAP) + 32

REVEAL, DUR = 3.2, 0.5
maxorder = (NW-1) + 6*0.55

rects, labels = [], []
sd = datetime.date.fromisoformat(contribs[0]["date"])
last_m = None
for wk in range(NW):
    d = sd + datetime.timedelta(days=wk*7)
    if d.month != last_m:
        last_m = d.month
        labels.append(f'<text class="lbl" x="{LEFT+wk*(CELL+GAP)}" y="{TOP-10}">{MONTHS[d.month-1]}</text>')

for name, r in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
    labels.append(f'<text class="lbl" x="4" y="{TOP+r*(CELL+GAP)+CELL-2}">{name}</text>')

for i, c in enumerate(contribs):
    wk, row, lvl = i//7, i%7, c["level"]
    x = LEFT + wk*(CELL+GAP)
    y = TOP + row*(CELL+GAP)
    delay = round((wk + row*0.55)/maxorder * REVEAL, 3)
    cls = "c g" if lvl >= 1 else "c e"
    rects.append(
        f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RAD}" '
        f'fill="{COLORS[lvl]}" style="animation-delay:{delay}s"/>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#0d1117"/>
    <stop offset="100%" stop-color="#161b22"/>
  </linearGradient>
</defs>
<style>
  text.lbl {{ fill:{GRAY}; font-size:12px; font-weight:500; }}
  text.total {{ fill:#e6edf3; font-size:14px; font-weight:600; }}
  text.legend {{ fill:{GRAY}; font-size:11px; }}
  .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
  .g {{ animation:pop {DUR}s ease-out both, flash {DUR+0.15}s ease-out both; }}
  @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.1)}} 100%{{opacity:1;transform:scale(1)}} }}
  @keyframes flash {{ 0%{{filter:brightness(2.2)}} 50%{{filter:brightness(2.2)}} 100%{{filter:brightness(1)}} }}
  @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
</style>
<rect width="{W}" height="{H}" rx="8" fill="url(#bg)" stroke="#30363d" stroke-width="1"/>
{''.join(labels)}
{''.join(rects)}
<g transform="translate({LEFT}, {H-12})">
  <text class="total" x="0" y="0">{total} contributions in the last year</text>
  <g transform="translate({W - LEFT - 130}, -8)">
    <text class="legend" x="-32" y="9">Less</text>
    <rect x="0" y="0" width="10" height="10" rx="2" fill="{COLORS[0]}"/>
    <rect x="13" y="0" width="10" height="10" rx="2" fill="{COLORS[1]}"/>
    <rect x="26" y="0" width="10" height="10" rx="2" fill="{COLORS[2]}"/>
    <rect x="39" y="0" width="10" height="10" rx="2" fill="{COLORS[3]}"/>
    <rect x="52" y="0" width="10" height="10" rx="2" fill="{COLORS[4]}"/>
    <text class="legend" x="66" y="9">More</text>
  </g>
</g>
</svg>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"Wrote {OUT}: {n} days, {total} contributions")
