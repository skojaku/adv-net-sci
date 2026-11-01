#!/usr/bin/env python3
"""Module 07 summary figure: three claims, each with the thumbnail(s) of the figure that showed it.
Built last, from the other figures' PNGs (run figs_a/b/c first).  Text is MesloLGS at the same 4x scale as figlib."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
S = 4                                   # figlib rasterises at 4 px per slide px
W, H = 1080, 560
MESLO = "/Users/skojaku/Library/Fonts/MesloLGSNerdFontPropo-Regular.ttf"
HOT, INK, MUTED = "#B14434", "#000000", "#6B6B6B"
ROWS = [
    ("1", [("The eigenvalue ", INK), ("1", HOT), (" gives the ", INK), ("degree", HOT)], ["degree-share"]),
    ("2", [("The second eigenvalue gives the ", INK), ("communities", HOT), (" and the ", INK), ("mixing time", HOT)], ["relax-curve", "eigvec2"]),
    ("3", [("Short walks see ", INK), ("communities", HOT), (". Long walks see ", INK), ("degree", HOT), (".", INK)], ["comm-curve"]),
]


def runs(d, x, y, parts, font, maxw):
    """draw coloured runs, wrapping on spaces at maxw; returns the y after the last line"""
    line_h = int(font.size * 1.3)
    cx = x
    words = [(w, c) for t, c in parts for w in t.replace(" ", " \0").split("\0") if w]
    for w, c in words:
        ww = d.textlength(w, font=font)
        if cx + ww > x + maxw and w.strip():
            cx, y = x, y + line_h
        d.text((cx, y), w, font=font, fill=c)
        cx += ww
    return y + line_h


def main():
    im = Image.new("RGB", (W * S, H * S), "white")
    d = ImageDraw.Draw(im)
    big = ImageFont.truetype(MESLO, 34 * S)
    num = ImageFont.truetype(MESLO, 44 * S)
    row_h = H // 3
    for i, (n, parts, thumbs) in enumerate(ROWS):
        y0 = i * row_h
        d.text((14 * S, (y0 + 28) * S), n, font=num, fill=HOT)
        runs(d, 70 * S, (y0 + 30) * S, parts, big, 470 * S)
        x = 580
        avail = W - 12 - x
        gap = 14
        w_each = (avail - gap * (len(thumbs) - 1)) // len(thumbs)
        for t in thumbs:
            th = Image.open(HERE / f"{t}.png").convert("RGB")
            sc = min(w_each * S / th.width, (row_h - 22) * S / th.height)
            th = th.resize((int(th.width * sc), int(th.height * sc)), Image.LANCZOS)
            im.paste(th, (x * S, (y0 + (row_h - th.height // S) // 2) * S))
            d.rectangle([x * S - 4, (y0 + (row_h - th.height // S) // 2) * S - 4,
                         x * S + th.width + 4, (y0 + (row_h - th.height // S) // 2) * S + th.height + 4], outline="#D9D9D9", width=4)
            x += th.width // S + gap
        if i:
            d.line([(14 * S, y0 * S), ((W - 14) * S, y0 * S)], fill="#D9D9D9", width=3)
    im.save(HERE / "summary.png")
    print("summary.png", im.size)


if __name__ == "__main__":
    main()
