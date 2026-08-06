#!/usr/bin/env python3
"""The Module 05 animations, as looping GIFs.

Why GIF: the lecture is given from Marp's HTML output, and the deck is meant to get its
density from motion rather than more text. Marp's sanitiser strips inline `<svg>`, and an
`<img>` pointing at `.svg` renders blank inside Marp's own `foreignObject`; a GIF
referenced by relative path just animates.

Geometry, palette, graph data and the TeX pipeline are imported from the figure modules,
so a frame cannot drift from the still beside it. Every frame of one GIF is cropped to
the *same* box -- the union of the ink across frames -- so the drawing never jumps, and
the size gates are then applied once to that box exactly as `emit()` applies them to a
still.

Each animation ends on the frame its neighbouring still shows, so the loop hands off
instead of resting somewhere arbitrary.

    python3 figures/make_animations.py            # all
    python3 figures/make_animations.py louvain    # one
"""

import sys
from pathlib import Path

import networkx as nx
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_numbers as V                                             # noqa: E402
from figlib import (                                                   # noqa: E402
    CONTAINER, DESIGN, FIG_H, FONT, INK_FILL_MIN, NODE_MAX_PX, NODE_MIN_PX, OUT, PAD,
    PXBP, TEXT_MIN_PX, calibrate, disc, render, seg, text,
)
from figs_chance import WS_E, WS_LEFT, WS_POS                          # noqa: E402
from kfig import CHI, COFF, KNODE, bag, club, karate, small, string    # noqa: E402

HOLD = 6            # frames of pause on the finished state
MS = 700            # ms per frame

_only = [a for a in sys.argv[1:] if not a.startswith("-")]
_built, _failures = [], []


def emit_gif(name, frames, container="full", h=380, hmod="", hold=HOLD, ms=MS):
    """Render every frame, crop them all to one box, and assert the same floors."""
    if _only and not any(k in name for k in _only):
        return
    try:
        w = DESIGN[container]
        ims = [render(body, w, h) for body in frames]
        box = None
        for im in ims:
            a = np.array(im.convert("L"))
            ys, xs = np.where(a < 200)
            assert len(ys), f"{name}: a frame is blank"
            b = (xs.min(), ys.min(), xs.max(), ys.max())
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]),
                                         max(box[2], b[2]), max(box[3], b[3]))
        edge = 2
        assert not (box[0] <= edge or box[2] >= ims[0].size[0] - 1 - edge
                    or box[1] <= edge or box[3] >= ims[0].size[1] - 1 - edge), (
            f"{name}: ink runs off the page in some frame -- CLIPPED, not cropped")

        pad = int(PAD * PXBP)
        lo = max(0, box[1] - pad)
        hi = min(ims[0].size[1], box[3] + pad)
        ims = [im.crop((0, lo, im.size[0], hi)) for im in ims]

        fw, fh = ims[0].size
        scale = min(CONTAINER[container] / fw, FIG_H[hmod] / fh, 1.0)
        factor = scale * PXBP
        assert abs(factor - CONTAINER[container] / w) < 1e-6, (
            f"{name}: the height binds the scale -- {fh / PXBP:.0f}bp over all frames, "
            f"and a '{hmod or 'plain'}' figure may be {FIG_H[hmod]}bp. Shorten it.")
        span = (box[2] - box[0] + 1) / fw
        assert span >= INK_FILL_MIN, f"{name}: ink spans {span:.0%} of the canvas width"
        node_px = KNODE * factor
        assert NODE_MIN_PX <= node_px <= NODE_MAX_PX, f"{name}: node disc {node_px:.0f}px"
        x_px = FONT * calibrate() * factor
        assert x_px >= TEXT_MIN_PX, f"{name}: text x-height {x_px:.1f}px on the slide"

        seq = ims + [ims[-1]] * hold
        pal = [im.convert("P", palette=Image.ADAPTIVE) for im in seq]
        pal[0].save(OUT / f"{name}.gif", save_all=True, append_images=pal[1:],
                    optimize=False, duration=ms, loop=0, disposal=2)
        _built.append(name)
        print(f"  {name}.gif  {len(seq)} frames  {fw // 4}x{fh // 4}bp  "
              f"node {node_px:.0f}px  ink {span:.0%}")
    except (AssertionError, SystemExit) as e:
        _failures.append((name, str(e)))
        print(f"  FAIL {name}: {e}")


# --------------------------------------------------------------------------- k-core
def kcore_frames():
    """Peel everyone with fewer than k friends inside, and watch it stop at four.

    Ends on the 4-core -- ten people, which is the number the answer slide states and
    `verify_numbers` asserts.
    """
    g = V.karate()
    cn = nx.core_number(g)

    def frame(k):
        core = {n for n, c in cn.items() if c >= k}
        assert core, f"the {k}-core came out empty"
        return karate(fill={n: CHI for n in core},
                      faint=[e for e in g.edges()
                             if e[0] not in core or e[1] not in core])

    final = {n for n, c in cn.items() if c >= 4}
    assert len(final) == 10 == len(V.facts()["max_core_nodes"])
    # The 4-core leads AND closes: leading with k=1 leads with the untouched club, which
    # is the slide-6 figure, so the static export repeated a picture and taught nothing.
    return [frame(4)] + [frame(k) for k in (1, 2, 3, 4)]


# --------------------------------------------------------------------------- the game
def balls_frames():
    """Pull a string, cut the strings, tip the balls into the bag, draw two.

    The graph is the worksheet -- the same six people the room scores Q on by hand two
    slides later, so the game and the arithmetic are about one picture.
    """
    g = nx.Graph(WS_E)
    m = g.number_of_edges()
    col = {n: (CHI if n in WS_LEFT else COFF) for n in WS_POS}
    pos = {n: (x * 0.44 + 60, y * 0.72 + 66) for n, (x, y) in WS_POS.items()}
    # The bag is on the page from frame one, empty. Marp renders a GIF's FIRST frame into
    # the static export, so a first frame that only fills the left third makes the gate --
    # correctly -- report 63% white margin on the slide.
    empty_bag = bag(830, 200, 400, 290)
    base = small(pos, list(WS_E), node=34, what="balls-1", fill=col) + empty_bag

    # 1: the network, as balls on strings, and an empty bag waiting
    f1 = base
    # 2: one string pulled out and inspected
    pulled = (1, 3)
    f2 = base + string((700, 250), (940, 250), color="accenttwo", w=5.0)
    f2 += disc(700, 250, fill=col[pulled[0]], size=48)
    f2 += disc(940, 250, fill=col[pulled[1]], size=48)
    f2 += text(820, 160, "same colour", color="accenttwo", anchor="north", size=FONT)
    # 3: every string cut, the balls in the bag
    f3 = small(pos, list(WS_E), node=34, what="balls-3", fill=col) + empty_bag
    rng = np.random.default_rng(2)
    slots = [(680 + (i % 5) * 76 + rng.uniform(-8, 8),
              110 + (i // 5) * 78 + rng.uniform(-7, 7)) for i in range(2 * m)]
    order = [n for n in sorted(WS_POS) for _ in range(g.degree(n))]
    assert len(order) == 2 * m == 14
    for (x, y), n in zip(slots, order):
        f3 += disc(x, y, fill=col[n], size=40)
    # 4: two of them drawn back out
    f4 = f3 + disc(1000, 250, fill=CHI, size=52) + disc(1000, 150, fill=COFF, size=52)
    return [f1, f2, f3, f4]


# --------------------------------------------------------------------------- Louvain
def louvain_frames(steps=9):
    """One local move at a time, ending on the four communities the still shows.

    The moves are a real greedy pass -- each node goes to whichever neighbouring group
    raises Q the most -- started from everybody in their own group. It converges on the
    partition `best-vs-real.png` draws, which is asserted rather than hoped for.
    """
    g = V.karate()
    target = V.facts()["louvain_parts"]
    lab = {n: i for i, c in enumerate(target) for n in c}
    cols = ["accent", "accenttwo", "accentthree", "annot"]

    cur = {n: n for n in g}
    order = sorted(g, key=lambda n: -g.degree(n))
    frames, moved = [], 0
    frames.append(karate(fill={n: "annot" for n in g}))
    for n in order:
        best, bq = cur[n], _q_of(g, cur)
        for nb in g[n]:
            trial = dict(cur)
            trial[n] = cur[nb]
            q = _q_of(g, trial)
            if q > bq + 1e-12:
                best, bq = cur[nb], q
        if best != cur[n]:
            cur[n] = best
            moved += 1
            if moved % max(1, len(order) // steps) == 0:
                frames.append(karate(fill=_colour(cur, cols)))
    frames.append(karate(fill={n: cols[lab[n] % len(cols)] for n in g}))
    assert len(frames) >= 4, f"only {len(frames)} frames -- the pass did nothing"
    return frames


def _colour(assign, cols):
    seen = {}
    out = {}
    for n, c in assign.items():
        seen.setdefault(c, len(seen))
        out[n] = cols[seen[c] % len(cols)]
    return out


def _q_of(g, assign):
    parts = {}
    for n, c in assign.items():
        parts.setdefault(c, []).append(n)
    return V.unweighted_Q(g, list(parts.values()))


ANIMS = [
    ("kcore-peel", kcore_frames, dict(h=380)),
    ("balls-strings", balls_frames, dict(h=360)),
    ("louvain", louvain_frames, dict(h=380)),
]

if __name__ == "__main__":
    calibrate()
    for name, fn, kw in ANIMS:
        if _only and not any(k in name for k in _only):
            continue
        try:
            emit_gif(name, fn(), **kw)
        except (AssertionError, SystemExit) as e:
            _failures.append((name, str(e)))
            print(f"  FAIL {name}: {e}")
    print(f"\n{len(_built)} animations written, {len(_failures)} failed")
    if _failures:
        sys.exit(1)
