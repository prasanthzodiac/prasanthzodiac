"""
Convert an avatar/portrait photo into a clean, monochrome ASCII-art SVG
with self-typing terminal SMIL wipe animation.
Usage: python scripts/make_ascii_svg.py [input_image] [output_svg]
"""
from PIL import Image, ImageEnhance, ImageFilter
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "avatar.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "avatar-ascii.svg")

COLS = int(os.environ.get("COLS", 100))
ART_W_TARGET = 800
CELL_W = ART_W_TARGET / COLS
CELL_H = CELL_W * 15 / 8
ROWS = round(COLS * 8 / 15)
RAMP = " .`:-=+*cs#%@"

CONTRAST = 1.15
BRIGHTNESS = 1.05
GAMMA = 1.15
WHITE_FLOOR = 0.85

PAD = 20
TITLEBAR_H = 34
STATUS_H = 28
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = 840.0
CANVAS_H = 880.0

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#c9d1d9"
CURSOR = "#58a6ff"

ROW_DUR = 5.0 / ROWS
STAGGER = ROW_DUR

if not os.path.exists(SRC):
    # fallback to downloading github avatar
    import urllib.request
    print(f"Downloading avatar to {SRC}...")
    urllib.request.urlretrieve("https://avatars.githubusercontent.com/u/168949457?v=4", SRC)

im = Image.open(SRC).convert("L")
im = ImageEnhance.Brightness(im).enhance(BRIGHTNESS)
im = ImageEnhance.Contrast(im).enhance(CONTRAST)
im = im.resize((COLS, ROWS), Image.LANCZOS)
px = im.load()

rows_txt = []
for y in range(ROWS):
    chars = []
    for x in range(COLS):
        lum = px[x, y] / 255.0
        lum = pow(lum, GAMMA)
        if lum >= WHITE_FLOOR:
            chars.append(" ")
            continue
        idx = int((1.0 - lum) * (len(RAMP) - 1) + 0.5)
        idx = max(0, min(len(RAMP) - 1, idx))
        chars.append(RAMP[idx])
    rows_txt.append("".join(chars))

art_top = TITLEBAR_H + (CANVAS_H - TITLEBAR_H - STATUS_H - ART_H) / 2

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
)
parts.append('<defs>')
parts.append(
    f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
)
parts.append('</defs>')
parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
parts.append(
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>'
)
parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
parts.append(f'<circle cx="20" cy="{TITLEBAR_H/2}" r="5" fill="#ff5f56"/>')
parts.append(f'<circle cx="36" cy="{TITLEBAR_H/2}" r="5" fill="#ffbd2e"/>')
parts.append(f'<circle cx="52" cy="{TITLEBAR_H/2}" r="5" fill="#27c93f"/>')
parts.append(
    f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" font-weight="600" text-anchor="middle">'
    f'avatar.ascii - prasanth@zodiac</text>'
)

font_sz = round(CELL_H * 0.95, 2)
art_left = (CANVAS_W - ART_W) / 2

for i, r in enumerate(rows_txt):
    esc = html.escape(r)
    y = art_top + (i + 1) * CELL_H - (CELL_H - font_sz) / 2
    delay = i * STAGGER
    clip_id = f"c{i}"
    parts.append(f'<clipPath id="{clip_id}">')
    parts.append(
        f'<rect x="{art_left}" y="{y - font_sz}" width="0" height="{CELL_H}">'
        f'<animate attributeName="width" from="0" to="{ART_W}" dur="{ROW_DUR:.3f}s" '
        f'begin="{delay:.3f}s" fill="freeze"/>'
        f'</rect>'
    )
    parts.append('</clipPath>')
    parts.append(
        f'<text x="{art_left}" y="{y}" fill="{INK}" font-size="{font_sz}px" clip-path="url(#{clip_id})">'
        f'{esc}</text>'
    )

parts.append('</svg>')

svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"Wrote {OUT}: {CANVAS_W} x {CANVAS_H}, {len(svg)} bytes")
