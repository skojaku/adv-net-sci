#!/usr/bin/env python3
"""Check the *rendered* slides, not the source figures.

Nine review rounds kept finding the same defect from different angles — node
diameter, in-figure type size, canvas margin — because every fix was asserted in
figure space while the defect lives on the slide. The deck scales each image by
its own factor (`min(w_directive/src_w, max_height/src_h)`), so a figure that is
perfect at source resolution can land as a smudge.

This runs after marp and fails the build on what a student actually sees.

    python3 figures/make_figures.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files \
         --images png -o review/slide.png
    python3 check_render.py
"""

import glob
import re
import sys
from collections import deque

import numpy as np
from PIL import Image

SLIDES = "review/slide.*.png"

# What a student can actually read, in slide pixels. The page number renders at
# 13px of ink and is the floor everyone agreed on; body text is 21px.
MIN_TEXT_PX = 13

# Node discs. Uniform enough that the same graph does not change size between
# consecutive slides, wide enough to allow a genuinely denser figure to be
# smaller. Measured band when this was written: 26-51px.
NODE_MIN_PX, NODE_MAX_PX = 26, 52

# How much of its allotted box a figure's drawing actually fills. Below FAIL the
# deck is scaling white margin, not the drawing: the diagram collapses to a
# smudge and its caption drifts a couple of hundred px away from it. Between
# FAIL and WANT it is merely modest — reported so the trend stays visible, not
# failed, because a sparse figure legitimately needs less room than a dense one.
INK_FRACTION_FAIL = 0.15
INK_FRACTION_WANT = 0.35

DARK = 60      # node fill / heavy ink
INK = 200      # any mark


def components(mask, min_px=120, step=2):
    """Connected components of a boolean mask, as (h, w, area) triples."""
    H, W = mask.shape
    seen = np.zeros_like(mask, bool)
    out = []
    for y in range(0, H, step):
        for x in range(0, W, step):
            if not mask[y, x] or seen[y, x]:
                continue
            q = deque([(y, x)])
            seen[y, x] = True
            ys, xs, n = [], [], 0
            while q:
                cy, cx = q.popleft()
                ys.append(cy)
                xs.append(cx)
                n += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            if n >= min_px:
                out.append((max(ys) - min(ys) + 1, max(xs) - min(xs) + 1, n))
    return out


def node_discs(gray):
    """Filled circles: near-square bounding box, fill ratio near pi/4."""
    out = []
    for h, w, area in components(gray < DARK):
        if h < 8 or w < 8:
            continue
        if 0.82 < h / w < 1.22 and 0.70 < area / (h * w) < 0.92:
            out.append((h + w) / 2)
    return out


def figure_region(gray):
    """The right-hand figure column: ink right of the text column, below the rule.

    Returns (ink_h, ink_w) of the drawing, or None if the slide has no figure.
    """
    sub = gray[120:610, 640:1210]
    rows = (sub < INK).sum(axis=1)
    if rows.sum() < 60:
        return None
    # The figcaption sits below the drawing with clear white between them, and a
    # naive ink bbox would union the two — the caption is wide, so a collapsed
    # drawing would still look like it fills its box. Split into bands separated
    # by whitespace so the caption can be dropped below.
    bands, start = [], None
    gap = 0
    for i, r in enumerate(rows):
        if r > 0:
            if start is None:
                start = i
            gap = 0
        elif start is not None:
            gap += 1
            if gap >= 8:
                bands.append((start, i - gap))
                start = None
    if start is not None:
        bands.append((start, len(rows) - 1))
    if not bands:
        return None
    # The figcaption is always the bottom-most band. Drop it and keep the rest:
    # picking the *largest* band instead would select the caption whenever the
    # drawing has collapsed, which is exactly the case we need to catch.
    drawing = bands[:-1] if len(bands) > 1 else bands
    y0, y1 = drawing[0][0], drawing[-1][1]
    xs = np.where((sub[y0:y1 + 1] < INK).any(axis=0))[0]
    return y1 - y0 + 1, xs.max() - xs.min() + 1


def slides_with_figures(deck="m01-euler-tour.md"):
    """Map slide number -> figure filename, from the deck itself.

    The deck is the only reliable source: a part divider or a question slide has
    text in the right half of the frame, which an ink scan cannot tell from a
    drawing.
    """
    with open(deck) as fh:
        text = fh.read()
    # parts[0] is the YAML front matter (the file opens with `---`), so the
    # slides are everything after it — parts[1] is slide 1.
    parts = text.split("\n---\n")
    out = {}
    for i, chunk in enumerate(parts[1:], start=1):
        m = re.search(r"!\[[^\]]*\]\((figures/[^)]+)\)", chunk)
        if m:
            out[i] = m.group(1)
    return out


def main():
    files = sorted(glob.glob(SLIDES))
    if not files:
        sys.exit("no rendered slides found — run marp first")
    figs = slides_with_figures()

    fails = []
    warns = []
    diams = []
    for path in files:
        n = int(re.search(r"(\d+)", path.split("/")[-1]).group(1))
        gray = np.array(Image.open(path).convert("L"))

        d = node_discs(gray)
        if d:
            diams += d
            lo, hi = min(d), max(d)
            if lo < NODE_MIN_PX or hi > NODE_MAX_PX:
                fails.append(
                    f"slide {n:03d}: node diameter {lo:.0f}-{hi:.0f}px "
                    f"outside {NODE_MIN_PX}-{NODE_MAX_PX}px"
                )

        if n in figs:
            reg = figure_region(gray)
            if reg is None:
                fails.append(f"slide {n:03d}: references {figs[n]} but nothing rendered")
                continue
            ink_h, ink_w = reg
            # The figure box is the column width, capped at the CSS max-height.
            box_h, box_w = 380, 520
            frac = (ink_h * ink_w) / float(box_h * box_w)
            name = figs[n].split("/")[-1]
            if frac < INK_FRACTION_FAIL:
                fails.append(
                    f"slide {n:03d} ({name}): drawing is {ink_w}x{ink_h}px = "
                    f"{frac:.0%} of its {box_w}x{box_h} box — the deck is scaling "
                    f"white margin; crop the canvas to its ink"
                )
            elif frac < INK_FRACTION_WANT:
                warns.append(f"slide {n:03d} ({name}): drawing fills {frac:.0%} of its box")

    print(f"checked {len(files)} rendered slides")
    if diams:
        print(
            f"node diameter: {min(diams):.0f}-{max(diams):.0f}px "
            f"(spread {max(diams)/min(diams):.1f}x) across {len(diams)} discs"
        )
    if warns:
        print(f"\n{len(warns)} figure(s) fill less than {INK_FRACTION_WANT:.0%} of their box:")
        for w in warns:
            print("  " + w)
    if fails:
        print(f"\n{len(fails)} problem(s) on the rendered slides:\n")
        for f in fails:
            print("  " + f)
        sys.exit(1)
    print("\nall checks pass")


if __name__ == "__main__":
    main()
