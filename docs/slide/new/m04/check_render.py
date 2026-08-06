#!/usr/bin/env python3
"""Check the *rendered* slides, not the source figures.

Nine review rounds kept finding the same defect from different angles — node
diameter, in-figure type size, canvas margin — because every fix was asserted in
figure space while the defect lives on the slide. The deck scales each image by
its own factor (`min(w_directive/src_w, max_height/src_h)`), so a figure that is
perfect at source resolution can land as a smudge.

This runs after marp and fails the build on what a student actually sees.

    python3 figures/make_figures.py
    marp m04-node-degree.md --theme network-science.css --allow-local-files \
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

# network-science.css caps figures three different ways, and using one number for all of
# them is how 13px type passed a green gate on sixteen slides. Measured on the render:
# discs the generator draws at a uniform 40bp land 38-40px in a plain full-width figure
# and 34-38px in a `fig tight` one.
#   section .fig img        { max-height: 380px }
#   section .fig.tight img  { max-height: 320px }   <- 16 slides use this
#   section .fig.stack img  { max-height: 190px }
FIG_H = {"": 380, "tight": 320, "stack": 190}
MAX_FIG_H = FIG_H[""]

# Content must stop before the frame does. The theme's bottom padding is 60px,
# and the page number sits in the bottom-right corner, so ink below this row is
# either overflowing or colliding with the pagination. Raising the body type
# from 25px to 30px pushed one slide's last line clean off the frame -- the
# deck's only notebook pointer -- and nothing caught it.
#
# m02 lowered this from 690 to the theme's actual content box (720 - 60 padding).
# 690 sits 60px BELOW the pagination row, so two slides shipped a last line that
# rendered underneath the page number and still passed the gate. Anything below
# 660 is outside the box the theme reserves for content, full stop.
CONTENT_BOTTOM = 660

# The `w:NNN` directive in the deck is INERT. The theme sets
# `section .fig img { width: auto !important }`, and an author !important
# declaration beats a non-important inline style, so Marp's inline width never
# applies. What actually bounds a figure is its container and the height cap:
#   content area  = 1280 - 2*80 padding          = 1120px
#   .cols column  = (1120 - 46 gap) / 2          =  537px
# Confirmed against getComputedStyle in a real browser: 536.98px measured.
COL_W = 537

# And the WIDTH cap for a full-width figure is not the content area. Marp wraps the image
# in a <p>, and `section p { max-width: 1080px }` binds first.
FULL_IMG_W = 1080

DARK = 60      # heavy ink
INK = 200      # any mark

# Node discs are found by COLOUR, not by darkness. The luminance test this file
# shipped with (`gray < 60`) is inert on this palette -- accent converts to L=88,
# accent-2 to L=99 -- so `node_discs()` returned [] on every slide of m02 and the
# 26-52px band went unenforced for a whole build. Two independent reviewers found
# the same thing, one of them after a 19px disc had passed a green gate.
#
# Masking on the fill colour also solves the problem that made a luminance test
# unworkable in the first place: edges are black, so they are not in the mask and
# cannot merge two discs into one component.
# Annotation gray belongs here too, and its absence was a silent hole. Two round-4 fixes
# recoloured discs to gray -- the quiz sketches, so a disc could be told from its edge,
# and the non-hub nodes on `assortativity` -- and both quietly left the size gate. The
# run still printed a confident "435 discs, 27-40px" while 28 discs on one slide and 15
# on another were not among them, including the ones whose clearance had been a Blocker
# two rounds earlier. Nothing was actually out of band, which is the point: the number
# was true and the coverage it implied was not.
#
# Black cannot be added -- the edges are black, and a graph would come back as one disc.
NODE_FILLS = [(0x39, 0x59, 0xA6), (0xB1, 0x44, 0x34), (0x6b, 0x6b, 0x6b)]
FILL_TOL = 46

# A disc at the bottom of the band covers ~530px2. A filled-in letter "o" at the type
# floor covers ~200. Below this, a component is a glyph the hole-filling closed up.
MIN_DISC_AREA = 380


def components(mask, min_px=120, step=2, with_origin=False):
    """Connected components of a boolean mask, as (h, w, area) triples.

    With `with_origin`, yields (h, w, area, y0, x0) so a caller can re-measure the same
    box against a different mask -- which is how a disc is told apart from a square (see
    node_discs).
    """
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
                bh, bw = max(ys) - min(ys) + 1, max(xs) - min(xs) + 1
                out.append((bh, bw, n, min(ys), min(xs)) if with_origin else (bh, bw, n))
    return out


def _flood_from_border(mask):
    """Everything in `mask` reachable from the image border, four-connected."""
    H, W = mask.shape
    out = np.zeros_like(mask)
    q = deque()
    for x in range(W):
        for y in (0, H - 1):
            if mask[y, x] and not out[y, x]:
                out[y, x] = True
                q.append((y, x))
    for y in range(H):
        for x in (0, W - 1):
            if mask[y, x] and not out[y, x]:
                out[y, x] = True
                q.append((y, x))
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not out[ny, nx]:
                out[ny, nx] = True
                q.append((ny, nx))
    return out


def node_discs(rgb):
    """Filled circles: near-square bounding box, fill ratio near pi/4.

    Takes an RGB array and masks on the theme's node fills (see NODE_FILLS), which
    is the only way this test fires at all on this palette.
    """
    a = np.asarray(rgb, dtype=np.int16)
    if a.ndim == 2:                       # tolerate a grayscale caller
        a = np.stack([a] * 3, axis=-1)
    mask = np.zeros(a.shape[:2], bool)
    for fill in NODE_FILLS:
        mask |= (np.abs(a - np.array(fill, dtype=np.int16)).max(axis=-1) <= FILL_TOL)
    # A part divider's band is a solid accent rectangle across the whole frame, and
    # the glyphs sitting in it read as small discs. Any row the mask fills more than
    # halfway across is a band, not a drawing.
    mask[(mask.mean(axis=1) > 0.5)] = False
    # Fill the holes. A disc carrying a white letter is an annulus in the colour mask,
    # and the letter cuts it into crescents -- which is how a 41px disc was reported as
    # a 12px one. Anything the background cannot reach from outside is interior.
    filled = ~_flood_from_border(~mask)
    out = []
    for h, w, area, y0, x0 in components(filled, min_px=MIN_DISC_AREA, with_origin=True):
        if h < 8 or w < 8:
            continue
        if not (0.82 < h / w < 1.22 and 0.70 < area / (h * w) < 0.92):
            continue
        # Hole-filling also turns a highlight RING into a solid blob, and an "o" in red
        # body text with it. Score the coverage BEFORE filling: a disc is ~60% covered
        # even with a letter punched out of it, an annulus or a glyph nowhere near that.
        if mask[y0:y0 + h, x0:x0 + w].mean() < 0.45:
            continue
        # A disc has empty corners; a square does not, and neither does a round
        # coloured glyph. Aspect and fill ratio alone could not tell them apart:
        # a 23px percolation cell and the letter "o" set in accent-2 both land
        # inside the aspect and fill windows, and m03 failed its node-size gate
        # on twelve glyphs of a caption and one wet paving stone before this
        # test existed. Sampling one pixel in from each corner costs nothing and
        # is exact for the shapes this deck actually draws.
        c = max(2, int(min(h, w) * 0.12))
        corners = [filled[y0 + c, x0 + c], filled[y0 + c, x0 + w - 1 - c],
                   filled[y0 + h - 1 - c, x0 + c], filled[y0 + h - 1 - c, x0 + w - 1 - c]]
        if any(corners):
            continue
        # ...and an ANNULUS survives all of the above: a highlight ring and a bold "o"
        # set in accent-2 are both round, both have empty corners, and hole-filling
        # turns both into solid blobs. What separates them from a disc is how much of
        # the blob the fill had to invent. Measured over all 457 candidates in this
        # deck: a real disc reaches 0.075 at worst (the white numeral punched out of
        # it), while the ring on the worksheet scored 0.303 and the "o" in the title
        # "Does it hold for you?" scored 0.283 -- with NOTHING between 0.15 and 0.25.
        # The threshold sits in that empty gap. This narrows what counts as a disc; it
        # does not soften the band, and the 23.5px marks it was meant to catch still
        # fail (they score 0.0).
        if (filled[y0:y0 + h, x0:x0 + w] & ~mask[y0:y0 + h, x0:x0 + w]).mean() > 0.15:
            continue
        out.append((h + w) / 2)
    return out


def figure_containers(deck="m04-node-degree.md"):
    """Which container each figure is USED in, per slide.

    A figure authored for the full content width and then dropped into a `cols`
    column renders at 48% of its intended scale -- 19px node discs on a slide whose
    twin, laid out full width, shows 39px. Two slides of m02 shipped that way. It is
    invisible in the source and obvious once the two numbers are put side by side,
    so the gate computes both.
    """
    with open(deck) as fh:
        parts = fh.read().split("\n---\n")
    out = []
    for i, chunk in enumerate(parts[1:], start=1):
        in_cols = 'class="cols"' in chunk
        mod = ""
        for m in ("tight", "stack"):
            if f'class="fig {m}"' in chunk:
                mod = m
        for f in re.findall(r"!\[[^\]]*\]\((figures/[^)]+)\)", chunk):
            out.append((i, f, COL_W if in_cols else FULL_IMG_W, FIG_H[mod], mod))
    return out


def figcaption_math(deck="m04-node-degree.md"):
    """KaTeX does not process <figcaption>, or any other raw HTML block.

    Nine captions and one roadmap item of m02 rendered `$\\sigma$` and
    `$C/C_{\\mathrm{rand}}$` to the room as literal source. FIGURE_GUIDE has recorded
    the trap since m01; recording it was not enough, so it is a build failure now.
    """
    with open(deck) as fh:
        text = fh.read()
    bad = []
    for m in re.finditer(r"<figcaption>(.*?)</figcaption>", text, re.S):
        if "$" in m.group(1):
            bad.append(("figcaption", m.group(1).strip()[:60]))
    # Non-greedy to the first `</div>` stopped at the end of ITEM 01, so items 02+
    # were never scanned and `$\kappa$` shipped in item 05 with this gate in place.
    # Scan every line of the block instead, to its closing blank line.
    for m in re.finditer(r'<div class="steps-list">\n(.*?)\n\n</div>', text, re.S):
        for line in m.group(1).splitlines():
            if "$" in line:
                bad.append(("steps-list", line.strip()[:60]))
    return bad


def smallest_text(src_path):
    """Smallest glyph x-height in a figure, in source pixels.

    Letters are small ink blobs. Take every component in a letter-like size and
    fill range, and report the smallest one that is actually part of the body
    of text in the figure -- not a lone artifact that happens to pass the
    shape filter.
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
    if not real:
        return None
    # Fix: a bare "seen >= 3 times" bar still let non-letter ink through as the
    # reported x-height -- confirmed directly (get_window_extent + colour
    # sampling, not guessed) on several figures: a dashed connector's own dash
    # segments, overlapping scatter dots, an arrowhead tip and a comma inside a
    # big number all recur 3+ times at one small size and clear the shape
    # filter, so the SMALLEST "real" height was a dash or a comma, not a
    # letter -- and the build failed over ink nobody was meant to read as text.
    # Genuine body text is the DOMINANT population of letter-shaped ink in a
    # figure (every word contributes several letters at the same height); an
    # artifact is a minority that happens to clear the bare 3-times bar next to
    # it. Requiring a count at least a fifth of the figure's own most common
    # letter-height discards that minority while still catching a real,
    # deliberately smaller secondary text style (axis ticks beside a title,
    # say) -- unlike a handful of dashes or commas, that has enough of its own
    # letters to clear this bar too.
    max_count = max(counts[h] for h in real)
    real = [h for h in real if counts[h] >= max(3, 0.2 * max_count)]
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


def slides_with_figures(deck="m04-node-degree.md"):
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

    # Source-level gates. These do not need a render, and both of them shipped a
    # defect to the rendered deck of m02 before they existed.
    for kind, snippet in figcaption_math():
        fails.append(f"deck: math inside a {kind} — KaTeX will print it literally: {snippet!r}")
    for n, src, container, hcap, mod in figure_containers():
        try:
            sw, sh = Image.open(src).size
        except OSError:
            fails.append(f"slide {n:03d}: {src} is missing")
            continue
        # Figures are authored at 4px per bp: a column figure is 520bp -> 2080px
        # (the GIF is emitted at half that), a full-width one 1100bp -> 4400px.
        authored = COL_W if sw <= 3000 else FULL_IMG_W
        if authored != container:
            fails.append(
                f"slide {n:03d}: {src} is authored {sw}px wide (for a {authored}px "
                f"container) but used in a {container}px one — it renders at "
                f"{container / authored:.0%} of its intended scale")
        # The height cap the deck's own markup applies. When it binds before the width
        # does, every glyph in the figure shrinks with it -- which is how 13px type
        # passed this gate on sixteen `fig tight` slides.
        elif hcap / sh < container / sw:
            fails.append(
                f"slide {n:03d}: {src} is {sh}px tall, so the "
                f"{('`fig ' + mod + '`') if mod else '`fig`'} height cap of {hcap}px "
                f"binds before the width does — it lands "
                f"{min(container / sw, hcap / sh) * 4:.2f} slide px per bp instead of "
                f"{container * 4 / sw:.2f}, and the in-figure type shrinks with it")

    for path in files:
        n = int(re.search(r"(\d+)", path.split("/")[-1]).group(1))
        im = Image.open(path).convert("RGB")
        rgb = np.array(im)
        gray = np.array(im.convert("L"))

        # Vertical overflow. Ignore the page-number corner, which lives below
        # this line by design.
        below = gray[CONTENT_BOTTOM:, :1080] < INK
        if below.sum() > 8:
            rows = np.where(below.any(axis=1))[0]
            fails.append(
                f"slide {n:03d}: content runs to y={CONTENT_BOTTOM + rows.max()} "
                f"in a 720px frame — the bottom of the slide is cut off"
            )

        d = node_discs(rgb)
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
            container = COL_W if in_cols else FULL_IMG_W
            ext = drawing_extent(src, container)
            if ext is None:
                fails.append(f"slide {n:03d}: {src} is blank")
                continue
            dw, dh, box_w, box_h, frac = ext
            ink_w, ink_h = dw, dh
            name = src.split("/")[-1]
            # A historical photograph carries no lettering of ours to size, and its
            # tonal range is not a drawing.
            if name in ("boruvka-portrait.png", "konigsberg-map.png"):
                continue
            im = np.array(Image.open(src).convert("L"))
            sh, sw = im.shape
            scale = min(container / sw, MAX_FIG_H / sh, 1.0)

            # In-figure text at body size on the slide.
            # Text size. The generator computes this exactly -- it knows the
            # point size, the dpi and the scale -- so its assertion is the gate.
            # This is a pixel heuristic and it mistakes dashes, arrowheads and
            # scatter dots for glyphs, so it warns rather than fails. It still
            # earns its place: it reads what actually landed, which is how a
            # figure whose type was raised until it overflowed its own cells was
            # caught while the generator's size check passed.
            xh = smallest_text(src)
            if xh is not None and xh * scale < MIN_TEXT_XHEIGHT:
                warns.append(
                    f"slide {n:03d} ({name}): smallest ink measures {xh * scale:.0f}px "
                    f"x-height — check it is a glyph and not a dash before acting"
                )

            # Absolute size, not just share of box -- but only where the figure
            # has room to be bigger. A figure whose whole content is one node
            # cannot exceed the node band, so demanding 150px there would ask two
            # of this file's own constraints to contradict each other.
            has_nodes = bool(node_discs(np.array(Image.open(src).convert("RGB"))))
            if not has_nodes and max(dw, dh) < MIN_DRAWING_PX:
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
        # This header used to read "N figure(s) fill less than 35% of their box" while
        # printing len(warns) -- the count of EVERY warning, most of which are x-height
        # and margin notes. It reported 48 under-filled figures on a deck whose worst
        # figure fills 66% and whose median fills 81%. A gate that mislabels its own
        # output is the same failure as a gate that cannot fire: both are read as fact.
        print(f"\n{len(warns)} warning(s):")
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
