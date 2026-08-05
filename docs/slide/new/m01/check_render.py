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

MAX_FIG_H = 380  # network-science.css: section .fig img { max-height }

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


def drawing_extent(src_path, w_directive):
    """How big the drawing lands on the slide, and what share of its box it fills.

    Measured on the *source* PNG, not the render. The ink fraction is invariant
    under the deck's uniform downscale, so it is identical either way -- and on
    the source there is no figcaption to segment away. Trying to separate caption
    from drawing on the rendered slide by whitespace bands is fragile: a caption
    that wraps to two lines gets counted as drawing, and a figure whose own
    annotation sits far from its graph gets cut in half.

    Returns (drawn_w, drawn_h, box_w, box_h, fraction) in slide pixels.
    """
    im = np.array(Image.open(src_path).convert("L"))
    ys, xs = np.where(im < INK)
    if len(ys) == 0:
        return None
    ink_w = xs.max() - xs.min() + 1
    ink_h = ys.max() - ys.min() + 1
    sh, sw = im.shape
    # Whichever of the width directive and the CSS max-height binds first.
    scale = min(w_directive / sw, MAX_FIG_H / sh, 1.0)
    frac = (ink_w * ink_h) / float(sw * sh)
    return ink_w * scale, ink_h * scale, sw * scale, sh * scale, frac


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
        m = re.search(r"!\[([^\]]*)\]\((figures/[^)]+)\)", chunk)
        if m:
            w = re.search(r"w:(\d+)", m.group(1))
            out[i] = (m.group(2), int(w.group(1)) if w else 520,
                      'class="cols"' in chunk)
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
            src, w_directive, _ = figs[n]
            ext = drawing_extent(src, w_directive)
            if ext is None:
                fails.append(f"slide {n:03d}: {src} is blank")
                continue
            dw, dh, box_w, box_h, frac = ext
            ink_w, ink_h = dw, dh
            name = src.split("/")[-1]
            if frac < INK_FRACTION_FAIL:
                fails.append(
                    f"slide {n:03d} ({name}): drawing lands {ink_w:.0f}x{ink_h:.0f}px = "
                    f"{frac:.0%} of its {box_w:.0f}x{box_h:.0f} box — the deck is scaling "
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
