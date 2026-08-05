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

# In-figure text must be at least body size on the slide. Body is 30px type,
# which renders as ~15px of x-height ink. The page number is NOT the floor --
# that was tried and the lecturer rejected it as far too low.
MIN_TEXT_XHEIGHT = 15

# The drawing must be big enough in absolute terms, not just as a share of its
# box. A 353x149px figure scores 74% on ink fraction and still lands 61px tall.
MIN_DRAWING_PX = 150

# Margin has to be checked per axis. A bounding-box area ratio hides margin that
# is all on one axis: three figures scored 37% while 48% of their height was
# white, which is what stranded their captions 145px below the drawing.
MAX_AXIS_MARGIN = 0.30

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

# Content must stop before the frame does. The theme's bottom padding is 60px,
# and the page number sits in the bottom-right corner, so ink below this row is
# either overflowing or colliding with the pagination. Raising the body type
# from 25px to 30px pushed one slide's last line clean off the frame -- the
# deck's only notebook pointer -- and nothing caught it.
CONTENT_BOTTOM = 690

# The `w:NNN` directive in the deck is INERT. The theme sets
# `section .fig img { width: auto !important }`, and an author !important
# declaration beats a non-important inline style, so Marp's inline width never
# applies. What actually bounds a figure is its container and the height cap:
#   content area  = 1280 - 2*80 padding          = 1120px
#   .cols column  = (1120 - 46 gap) / 2          =  537px
# Confirmed against getComputedStyle in a real browser: 536.98px measured.
COL_W, FULL_W = 537, 1120

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


def smallest_text(src_path):
    """Smallest glyph x-height in a figure, in source pixels.

    Letters are small ink blobs. Take every component in a letter-like size and
    fill range, and report the 10th percentile of their heights -- the modal
    small glyph, rather than the single smallest speck, which would be a dot or
    an antialiasing artifact.
    """
    im = np.array(Image.open(src_path).convert("L"))
    heights = []
    for h, w, area in components(im < INK, min_px=12, step=1):
        # Aspect filter excludes dashes (wide and flat) and rules (long and thin);
        # a letterform is roughly as tall as it is wide, within a factor of a few.
        if 4 <= h <= 60 and 2 <= w <= 60 and 0.12 < area / (h * w) < 0.90 \
                and 0.45 <= h / w <= 4.0:
            heights.append(h)
    if len(heights) < 3:
        return None
    # A word has several letters of the same height, so a height that occurs
    # once is a dot, a dash or an antialiasing speck rather than text. Keep only
    # heights seen at least three times (within 1px), then take the smallest.
    counts = {}
    for h in heights:
        for k in (h - 1, h, h + 1):
            counts[k] = counts.get(k, 0) + 1
    real = [h for h in sorted(set(heights)) if counts.get(h, 0) >= 3]
    return float(real[0]) if real else None


def drawing_extent(src_path, container_w):
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
    scale = min(container_w / sw, MAX_FIG_H / sh, 1.0)
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
        # findall, not search: a slide may stack two images in one .fig, and
        # checking only the first leaves the second unexamined.
        hits = re.findall(r"!\[[^\]]*\]\((figures/[^)]+)\)", chunk)
        if hits:
            out[i] = (hits, 'class="cols"' in chunk)
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

        # Vertical overflow. Ignore the page-number corner, which lives below
        # this line by design.
        below = gray[CONTENT_BOTTOM:, :1080] < INK
        if below.sum() > 8:
            rows = np.where(below.any(axis=1))[0]
            fails.append(
                f"slide {n:03d}: content runs to y={CONTENT_BOTTOM + rows.max()} "
                f"in a 720px frame — the bottom of the slide is cut off"
            )

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
          srcs, in_cols = figs[n]
          for src in srcs:
            container = COL_W if in_cols else FULL_W
            ext = drawing_extent(src, container)
            if ext is None:
                fails.append(f"slide {n:03d}: {src} is blank")
                continue
            dw, dh, box_w, box_h, frac = ext
            ink_w, ink_h = dw, dh
            name = src.split("/")[-1]
            # The Konigsberg engraving is a historical photograph; its lettering
            # is not ours to size.
            if name == "konigsberg-map.png":
                continue
            im = np.array(Image.open(src).convert("L"))
            sh, sw = im.shape
            scale = min(container / sw, MAX_FIG_H / sh, 1.0)

            # In-figure text at body size on the slide.
            xh = smallest_text(src)
            if xh is not None and xh * scale < MIN_TEXT_XHEIGHT:
                fails.append(
                    f"slide {n:03d} ({name}): smallest text lands {xh * scale:.0f}px "
                    f"x-height, below the {MIN_TEXT_XHEIGHT}px body floor"
                )

            # Absolute size, not just share of box.
            if max(dw, dh) < MIN_DRAWING_PX:
                fails.append(
                    f"slide {n:03d} ({name}): drawing lands {dw:.0f}x{dh:.0f}px — "
                    f"too small to read regardless of how much of its box it fills"
                )

            # Margin per axis, since an area ratio hides one-sided padding.
            ys, xs = np.where(im < INK)
            mx = 1 - (xs.max() - xs.min() + 1) / sw
            my = 1 - (ys.max() - ys.min() + 1) / sh
            if max(mx, my) > MAX_AXIS_MARGIN:
                axis, val = ("horizontal", mx) if mx > my else ("vertical", my)
                warns.append(
                    f"slide {n:03d} ({name}): {val:.0%} {axis} white margin baked "
                    f"into the canvas"
                )
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
