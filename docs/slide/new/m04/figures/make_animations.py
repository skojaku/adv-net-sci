#!/usr/bin/env python3
"""The Module 04 animation, as a looping GIF.

Why GIF: the lecture is given from Marp's HTML output, and the deck is meant to get its
density from motion rather than more text.  Marp's sanitiser strips inline `<svg>`, and
an `<img>` pointing at `.svg` renders blank inside Marp's own `foreignObject`; a GIF
referenced by relative path just animates.

Geometry, palette and the TeX pipeline are imported from `figlib.py`, and the growth
history itself from `figs_tail.py` -- the same `ba_frames()` and `draw_growth()` that
`quiz.png` freezes.

The animation deliberately does NOT share the quiz's arrangement.  It used to: the
last frame was `quiz.png`'s preferential panel node for node, asserted equal to 1e-9,
and the result was that slide 076 showed the answer to slide 077's question two slides
early, ringed hub and all.  The room could answer by matching pictures.  `fig_quiz`'s
withholding check scans banned *strings*, so a graphical leak walked straight through
it -- an assertion tells you about the property it measures and nothing else.

So the drift guard is now split in two.  What must stay identical is the *graph*: same
generator, same m, same n, same edge set, asserted.  What must differ is the *drawing*:
the GIF takes a different one of `growth_layout`'s ranked spring solutions, and the
build asserts the two normalised layouts are far apart -- counting reflections of the
quiz's layout as near, since a flip is not a difference a room cannot undo.

Every frame is cropped to the *same* box -- the union of the ink across frames -- so the
drawing never jumps, and the floors are then asserted once against that box, exactly as
`figlib.emit()` asserts them for a still.

    python3 figures/make_animations.py
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from figlib import (  # noqa: E402
    CONTAINER, DESIGN, FIG_H, FONT, INK_FILL_MIN, NODE, NODE_MAX_PX, NODE_MIN_PX, OUT,
    PAD, PXBP, TEXT_MIN_PX, calibrate, render, ring, text,
)
from figs_tail import (  # noqa: E402
    GROWTH_N, QUIZ_B, ba_frames, draw_growth, growth_edges, growth_layout, growth_pos,
)

MS = 280            # ms per frame; 23 growth frames runs about six and a half seconds
HOLD = 10           # frames of pause on the finished state before the loop restarts

# The graph gets the width.  It used to sit in a 312bp box -- the size of a *quiz
# panel* -- with the two running counts pushed out to the canvas edges to carry the ink
# span, so 780bp of a 1080bp canvas was two short gray lines and the network drew at
# 28% of the slide while every other single-graph figure in the range spans 950-1070.
# The counts go under the drawing instead; the hub's fifteen spokes are the thing the
# room has to be able to see.
BOX = (50, 100, 1030, 340)
GIF_NODE = NODE                       # 40bp, as every other graph in the deck
LEFT_X, RIGHT_X, LABEL_Y = 50, 1030, 44

_built = []


def emit_gif(name, frames, container="full", h=None, hmod="", hold=HOLD, ms=MS,
             node=GIF_NODE, lead=0):
    """Render every frame, crop them all to one box, and assert the same floors.

    `lead` repeats the LAST frame at the front. A growth animation starts from a
    triangle, and the PNG/PDF export shows a GIF's first frame -- so the finished slide
    was three discs adrift in an empty box, which is what `check_render` reported as
    "60% vertical white margin". Leading with the finished network gives the static
    export the picture it should have and turns the loop into "the result, then how it
    got there". The frames themselves are untouched.
    """
    w = DESIGN[container]
    ims = [render(body, w, h or int(w * 0.70)) for body in frames]

    box = None
    for im in ims:
        a = np.array(im.convert("L"))
        ys, xs = np.where(a < 200)
        assert len(ys), f"{name}: a frame is blank"
        b = (xs.min(), ys.min(), xs.max(), ys.max())
        box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]),
                                     max(box[2], b[2]), max(box[3], b[3]))
    edge = 2
    touched = [s for s, hit in (("left", box[0] <= edge), ("top", box[1] <= edge),
                                ("right", box[2] >= ims[0].size[0] - 1 - edge),
                                ("bottom", box[3] >= ims[0].size[1] - 1 - edge)) if hit]
    assert not touched, f"{name}: ink runs off the {', '.join(touched)} edge -- CLIPPED"

    pad = int(PAD * PXBP)
    lo, hi = max(0, box[1] - pad), min(ims[0].size[1], box[3] + pad)
    ims = [im.crop((0, lo, im.size[0], hi)) for im in ims]

    fw, fh = ims[0].size
    hcap = FIG_H[hmod]
    factor = min(CONTAINER[container] / fw, hcap / fh, 1.0) * PXBP
    want = CONTAINER[container] / w
    assert abs(factor - want) < 1e-6, (
        f"{name}: the HEIGHT binds the scale -- {fh / PXBP:.0f}bp over all frames, and a "
        f"'{hmod or 'plain'}' figure may be at most {hcap}bp. Shorten it.")
    span = (box[2] - box[0] + 1) / fw
    assert span >= INK_FILL_MIN, f"{name}: ink spans {span:.0%} of the canvas width"
    node_px = node * factor
    assert NODE_MIN_PX <= node_px <= NODE_MAX_PX, f"{name}: node disc {node_px:.0f}px"
    x_px = FONT * calibrate() * factor
    assert x_px >= TEXT_MIN_PX, f"{name}: text x-height {x_px:.1f}px on the slide"

    seq = [ims[-1]] * lead + ims + [ims[-1]] * hold
    pal = [im.convert("P", palette=Image.ADAPTIVE) for im in seq]
    pal[0].save(OUT / f"{name}.gif", save_all=True, append_images=pal[1:],
                optimize=False, duration=ms, loop=0, disposal=2)
    # Report what the FILE holds, not what was handed to the encoder: PIL merges a run
    # of identical frames into one and lengthens its duration, so the lead and the hold
    # collapse and `len(seq)` overstates the count by fifteen.
    _built.append(name)
    with Image.open(OUT / f"{name}.gif") as g:
        n = g.n_frames
    print(f"  {name}.gif  {n} frames ({len(seq)} drawn)  {fw // 4}x{fh // 4}bp  "
          f"node {node_px:.0f}px  x-h {x_px:.1f}px  ink {span:.0%}")


def _unit(p):
    """Layout normalised to the unit square, so two drawings can be compared by shape."""
    xs, ys = [v[0] for v in p.values()], [v[1] for v in p.values()]
    w, hgt = max(xs) - min(xs), max(ys) - min(ys)
    return {k: ((v[0] - min(xs)) / w, (v[1] - min(ys)) / hgt) for k, v in p.items()}


def _apart_from_quiz(pos):
    """How far this arrangement is from `quiz.png`'s, counting reflections as near.

    A flip is not a difference a room cannot undo, so scoring only the identity lets a
    mirror image score 1.0 and pass. All four reflections of the square are compared and
    the smallest distance wins.
    """
    ua = _unit(pos)
    ub = _unit(growth_pos(True, QUIZ_B))
    best = None
    for fx in (False, True):
        for fy in (False, True):
            flip = {k: (1.0 - x if fx else x, 1.0 - y if fy else y)
                    for k, (x, y) in ub.items()}
            d = max(abs(ua[k][0] - flip[k][0]) + abs(ua[k][1] - flip[k][1]) for k in ua)
            best = d if best is None else min(best, d)
    return best


def gif_layout():
    """The GIF's own arrangement of the quiz's preferential graph.

    `pick=1` takes the second-best of `growth_layout`'s ranked spring solutions, so this
    is a genuinely different arrangement rather than the quiz's one rearranged.

    It used to be `stretch=True` plus a mirror, and figs-tail measured what that was
    really worth: stretching alone leaves the layout 0.049 from `QUIZ_B`'s in normalised
    coordinates -- the same picture, wider -- and mirroring it leaves a mirror image,
    which a room matches by eye without difficulty.  My own assertion passed anyway,
    because reflecting every x to 1 - x makes the numeric distance large while changing
    nothing a viewer cannot undo.  That is the round's lesson landing on my own code:
    the assertion measured its quantity faithfully and knew nothing about what the
    quantity was standing in for.  Hence `_apart_from_quiz` below, which now scores the
    quiz layout's reflections too.
    """
    return growth_layout(True, box=BOX, node=GIF_NODE, stretch=True, pick=1)


def ba_growth_frames():
    """Preferential attachment, one arrival's edges lit at a time.

    Two colours, two meanings, both readable off the drawing: accent is a node that is
    already there, accent-2 is the arrival happening in THIS frame and the edges it
    brought.  The counts under the drawing are recomputed from the frame, never carried
    along, so a mislabelled frame cannot happen.
    """
    frames = ba_frames()
    pos = gif_layout()

    # What must NOT differ: the graph. Same generator, same m, same n, same edges.
    final = frames[-1]
    assert sorted(final["nodes"]) == list(range(GROWTH_N))
    assert ({frozenset(e) for e in final["edges"]}
            == {frozenset(e) for e in growth_edges(True)}), \
        "the GIF is animating a different graph from the one the quiz freezes"

    # What MUST differ: the drawing. This assertion is the old equality one negated.
    # Slide 076 showed the quiz's answer node for node because the two were held equal;
    # a picture-matching student needs no tail to read.
    apart = _apart_from_quiz(pos)
    assert apart > 0.25, (
        f"the GIF's layout is within {apart:.3f} of quiz.png's preferential panel, or "
        f"of a reflection of it -- slide 076 would be giving away slide 077's answer")

    out = []
    for fr in frames:
        deg = {}
        for a, b in fr["edges"]:
            deg[a] = deg.get(a, 0) + 1
            deg[b] = deg.get(b, 0) + 1
        assert sum(deg.values()) == 2 * len(fr["edges"])
        top = max(deg, key=lambda v: (deg[v], -v))

        # C2-3 -- the arriving node's edges coming out in two colours -- is fixed inside
        # `ba_frames()` now, which asserts the last arrival keeps all GROWTH_M of them.
        # I had recomputed the highlight here as well; two mechanisms agreeing today is
        # how they disagree later, so this one is gone and figs_tail's is the only one.

        # Ring first: drawn after `draw_growth` it sat on top of the hub's fifteen
        # spokes and cut every one of them, leaving stubs between ring and disc.
        body = ring(pos[top][0], pos[top][1], size=GIF_NODE,
                    color="accentthree", w=5.0, grow=13)
        # The counter had no referent and its colour pointed at the wrong node: it was
        # set in accent-2, which in the drawing marks the node that just ARRIVED, so the
        # eye read "largest 15 edges" off a disc with one edge while the real hub sat
        # unmarked in plain accent. The count is annotation now, and the node it counts
        # carries an accent-3 ring -- legal as a ring, banned only as text and as a thin
        # stroke. So: accent-2 = arriving now, accent-3 ring = the current biggest.
        body += draw_growth(fr, pos, fill="accent", size=GIF_NODE)
        body += text(LEFT_X, LABEL_Y,
                     f"${len(fr['nodes'])}$ nodes, ${len(fr['edges'])}$ edges",
                     color="annot", anchor="west")
        body += text(RIGHT_X, LABEL_Y,
                     f"ringed: largest, ${deg[top]}$ edges",
                     color="annot", anchor="east")
        out.append(body)
    return out


ANIMS = [("ba-growth", ba_growth_frames, "full", 400, "", 6)]


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    calibrate()
    for name, fn, cont, h, hmod, lead in ANIMS:
        if only and not any(k in name for k in only):
            continue
        emit_gif(name, fn(), cont, h, hmod, lead=lead)
    print(f"\n{len(_built)} animations written")


if __name__ == "__main__":
    main()
