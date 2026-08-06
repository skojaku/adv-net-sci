#!/usr/bin/env python3
"""The Module 04 animation, as a looping GIF.

Why GIF: the lecture is given from Marp's HTML output, and the deck is meant to get its
density from motion rather than more text.  Marp's sanitiser strips inline `<svg>`, and
an `<img>` pointing at `.svg` renders blank inside Marp's own `foreignObject`; a GIF
referenced by relative path just animates.

Geometry, palette and the TeX pipeline are imported from `figlib.py`, and the growth
history itself from `figs_tail.py` -- the same `ba_frames()`, `growth_pos()` and
`draw_growth()` that `quiz.png` freezes.  So the animation and the still cannot drift:
the last frame here IS the picture on slide 73, mapped into a bigger box.

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
    CONTAINER, DESIGN, FIG_H, FONT, INK_FILL_MIN, NODE_MAX_PX, NODE_MIN_PX, OUT, PAD,
    PXBP, TEXT_MIN_PX, calibrate, render, text,
)
from figs_tail import (  # noqa: E402
    GROWTH_N, GROWTH_NODE, QUIZ_B, ba_frames, draw_growth, growth_edges, growth_pos,
)

MS = 200            # ms per frame; 43 frames runs a shade under nine seconds
HOLD = 10           # frames of pause on the finished state before the loop restarts

# The network sits in the middle at exactly the aspect `quiz.png` uses, with the two
# running counts at the canvas edges.  Those counts are what carry the ink across the
# full width -- a square drawing centred in a 1080bp canvas spans 31%, and the floor is
# 76%.  They are numbers, not prose: the sentence lives in the deck's figcaption.
BOX = (384, 24, 696, 338)
LEFT_X, RIGHT_X, LABEL_Y = 40, 1040, 181

_built = []


def emit_gif(name, frames, container="full", h=None, hmod="", hold=HOLD, ms=MS,
             node=GROWTH_NODE, lead=0):
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
    _built.append(name)
    print(f"  {name}.gif  {len(seq)} frames  {fw // 4}x{fh // 4}bp  node {node_px:.0f}px  "
          f"x-h {x_px:.1f}px  ink {span:.0%}")


def ba_growth_frames():
    """Preferential attachment, one frame per edge, ending on `quiz.png`'s right panel.

    Two colours, two meanings, both readable off the drawing: accent is a node that is
    already there, accent-2 is the arrival happening in THIS frame and the edges it
    brought.  The counts at the two edges of the canvas are recomputed from the frame,
    never carried along, so a mislabelled frame cannot happen.
    """
    frames = ba_frames()
    pos = growth_pos(True, BOX)
    quiz_pos = growth_pos(True, QUIZ_B)

    # The still and the animation share one relative layout by construction; this is the
    # assertion that says so, rather than a comment claiming it.
    def unit(p):
        xs, ys = [v[0] for v in p.values()], [v[1] for v in p.values()]
        w, hgt = max(xs) - min(xs), max(ys) - min(ys)
        return {k: ((v[0] - min(xs)) / w, (v[1] - min(ys)) / hgt) for k, v in p.items()}

    ua, ub = unit(pos), unit(quiz_pos)
    assert max(abs(ua[k][0] - ub[k][0]) + abs(ua[k][1] - ub[k][1]) for k in ua) < 1e-9, \
        "the GIF's layout has drifted from quiz.png's preferential panel"

    final = frames[-1]
    assert sorted(final["nodes"]) == list(range(GROWTH_N))
    assert ({frozenset(e) for e in final["edges"]}
            == {frozenset(e) for e in growth_edges(True)}), \
        "the last frame is not the graph quiz.png draws"

    out = []
    for fr in frames:
        deg = {}
        for a, b in fr["edges"]:
            deg[a] = deg.get(a, 0) + 1
            deg[b] = deg.get(b, 0) + 1
        assert sum(deg.values()) == 2 * len(fr["edges"])
        body = draw_growth(fr, pos, fill="accent", size=GROWTH_NODE)
        body += text(LEFT_X, LABEL_Y,
                     f"${len(fr['nodes'])}$ nodes\\\\${len(fr['edges'])}$ edges",
                     color="annot", anchor="west")
        body += text(RIGHT_X, LABEL_Y,
                     f"largest\\\\${max(deg.values())}$ edges",
                     color="accenttwo", anchor="east")
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
