#!/usr/bin/env python3
"""
Render the streak and activity metrics card from data/contributions.json
as an animated terminal-window SVG that sits beside avatar-ascii.svg.

The canvas matches avatar-ascii.svg (840 x 880) so both panels align perfectly
when the README renders them side by side.
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data", "contributions.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "stats.svg")

BG = "#0d1117"
BG2 = "#111722"
TILE = "#161b22"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
GREEN = "#39d353"
CYAN = "#58a6ff"
BAR = "#26a641"

W, H = 840, 880
PAD = 20
TITLEBAR_H = 34
COLS, ROWS = 2, 3
GAP = 16
TILE_W = (W - PAD * 2 - GAP * (COLS - 1)) / COLS
TILE_H = 145
TILES_TOP = TITLEBAR_H + PAD + 6
CHART_TOP = TILES_TOP + ROWS * TILE_H + (ROWS - 1) * GAP + GAP

TILE_STAGGER = 0.15
SLIDE_DUR = 0.45
COUNT_DUR = 1.2
FRAMES = 16
BAR_START = TILE_STAGGER * COLS * ROWS + 0.4
BAR_STAGGER = 0.06
BAR_DUR = 0.6

def short(d):
    dt = datetime.date.fromisoformat(d)
    return f"{dt.strftime('%b')} {dt.day}"

def span(s):
    return f'{short(s["start"])} – {short(s["end"])}' if s.get("length") and s.get("start") else "—"

with open(SRC, "r", encoding="utf-8") as f:
    data = json.load(f)

cur = data.get("current_streak", {"length": 0})
lng = data.get("longest_streak", {"length": 0})
best = data.get("best_day", {"count": 0, "date": ""})
n_days = len(data.get("days", []))

tiles = [
    ("current streak", cur.get("length", 0), " days", span(cur), GREEN),
    ("longest streak", lng.get("length", 0), " days", span(lng), CYAN),
    ("busiest day", best.get("count", 0), " contribs", short(best["date"]) if best.get("date") else "—", INK),
    ("total contributions", data.get("total_contributions", 0), "", f"across past {n_days} days", INK),
    ("active days", data.get("active_days", 0), f" / {n_days}", f"{round(data.get('active_days', 0) / max(1, n_days) * 100, 1)}% of year", GREEN),
    ("avg / active day", data.get("avg_per_active_day", 0), "", "contributions", INK),
]

def make_counter(final_val, suffix, color, delay, cx, cy, font_size=42):
    is_float = isinstance(final_val, float)
    out = [f'<g class="counter">']
    out.append(
        f'<text x="{cx}" y="{cy}" text-anchor="middle" fill="{color}" '
        f'font-size="{font_size}" font-weight="700" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">'
        f'{final_val}{suffix}</text>'
    )
    out.append("</g>")
    return "".join(out)

tiles_svg = []
for i, (label, val, suf, cap, acc) in enumerate(tiles):
    c = i % COLS
    r = i // COLS
    x = PAD + c * (TILE_W + GAP)
    y = TILES_TOP + r * (TILE_H + GAP)
    delay = round(i * TILE_STAGGER, 2)
    cx = x + TILE_W / 2
    cy = y + 78
    cnt = make_counter(val, suf, acc, delay + 0.15, cx, cy)
    tiles_svg.append(f'''
    <g class="tile" style="animation-delay:{delay}s">
      <rect x="{x}" y="{y}" width="{TILE_W}" height="{TILE_H}" rx="10"
            fill="{TILE}" stroke="{FRAME}" stroke-width="1"/>
      <text x="{x + 16}" y="{y + 26}" fill="{MUTED}" font-size="13" font-weight="600"
            letter-spacing="0.5" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif">
        {label.upper()}
      </text>
      {cnt}
      <text x="{cx}" y="{y + 118}" text-anchor="middle" fill="{MUTED}" font-size="12"
            font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif">
        {cap}
      </text>
    </g>''')

monthly = data.get("monthly", [])[-12:]
m_max = max((m["total"] for m in monthly), default=1) or 1
chart_w = W - PAD * 2
chart_h = H - CHART_TOP - PAD - 26
bar_w = (chart_w - (len(monthly) - 1) * 10) / max(1, len(monthly))

bars_svg = []
for i, m in enumerate(monthly):
    bx = PAD + i * (bar_w + 10)
    frac = m["total"] / m_max
    bh = max(4.0, frac * (chart_h - 40))
    by = CHART_TOP + chart_h - bh
    b_delay = round(BAR_START + i * BAR_STAGGER, 2)
    m_name = datetime.date.fromisoformat(m["month"] + "-01").strftime("%b")
    bars_svg.append(f'''
    <g class="bar-col">
      <rect class="bar" x="{bx}" y="{by}" width="{bar_w}" height="{bh}" rx="4"
            fill="{BAR}" style="animation-delay:{b_delay}s;transform-origin:{bx + bar_w/2}px {CHART_TOP + chart_h}px"/>
      <text x="{bx + bar_w/2}" y="{by - 6}" text-anchor="middle" fill="{MUTED}"
            font-size="11" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">{m["total"]}</text>
      <text x="{bx + bar_w/2}" y="{CHART_TOP + chart_h + 18}" text-anchor="middle"
            fill="{MUTED}" font-size="12" font-weight="500" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif">
        {m_name}
      </text>
    </g>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="wbg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{BG2}"/>
    <stop offset="100%" stop-color="{BG}"/>
  </linearGradient>
</defs>
<style>
  .tile {{
    transform-box: fill-box;
    opacity: 0;
    animation: slidein {SLIDE_DUR}s cubic-bezier(0.2, 0.7, 0.2, 1) both;
  }}
  .bar {{
    transform-box: fill-box;
    animation: growin {BAR_DUR}s cubic-bezier(0.2, 0.7, 0.2, 1) both;
  }}
  @keyframes slidein {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to {{ opacity: 1; transform: none; }}
  }}
  @keyframes growin {{
    from {{ transform: scaleY(0); }}
    to {{ transform: scaleY(1); }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .tile, .bar {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
  }}
</style>
<rect width="{W}" height="{H}" rx="12" fill="url(#wbg)" stroke="{FRAME}" stroke-width="1"/>
<rect width="{W}" height="{TITLEBAR_H}" rx="12" fill="#161b22"/>
<rect y="{TITLEBAR_H-10}" width="{W}" height="10" fill="#161b22"/>
<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-width="1"/>
<circle cx="20" cy="{TITLEBAR_H/2}" r="5" fill="#ff5f56"/>
<circle cx="36" cy="{TITLEBAR_H/2}" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="{TITLEBAR_H/2}" r="5" fill="#27c93f"/>
<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" font-weight="600"
      font-family="ui-monospace,SFMono-Regular,Menlo,monospace" text-anchor="middle">
  activity-insights - prasanth@zodiac
</text>
{''.join(tiles_svg)}
<g class="chart">
  <text x="{PAD}" y="{CHART_TOP - 10}" fill="{MUTED}" font-size="13" font-weight="600"
        letter-spacing="0.5" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif">
    CONTRIBUTIONS BY MONTH
  </text>
  <line x1="{PAD}" y1="{CHART_TOP + chart_h}" x2="{W - PAD}" y2="{CHART_TOP + chart_h}" stroke="{FRAME}" stroke-width="1"/>
  {''.join(bars_svg)}
</g>
</svg>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"Wrote {OUT}: {W} x {H}, {len(svg)//1024} KB")
