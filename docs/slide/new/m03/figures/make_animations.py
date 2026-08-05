#!/usr/bin/env python3
"""The Module 03 animations, as looping GIFs.

Why GIF: the lecture is given from Marp's HTML output, and the deck is meant to get
its density from motion rather than more text.  Marp's sanitiser strips inline
`<svg>`, and an `<img>` pointing at `.svg` renders blank inside Marp's own
`foreignObject`; a GIF referenced by relative path just animates.

Geometry, palette, graph data and the TeX pipeline are imported from
`make_figures.py`, so a frame cannot drift from the static figure beside it.

Every frame of one GIF is cropped to the *same* box -- the union of the ink across
frames -- so the drawing never jumps, and the scale assertions are then applied once
to that box exactly as `emit()` applies them to a still.

    python3 figures/make_animations.py            # all
    python3 figures/make_animations.py kruskal    # one
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_figures import (  # noqa: E402
    km,
    ALL_CABLES, ATTACK_ORDER, ATTACK_PROFILE, BORUVKA_ROUNDS, CABLES, CONTAINER,
    DESIGN, FULL_H, KRUSKAL, MAX_FIG_H, MST_PAIRS, MST_TOTAL, NAME, NODE,
    NODE_MAX_PX, NODE_MIN_PX, OUT, PAD, PRIM, PUD_FIELD, PXBP, TEXT_MIN_PX,
    XHEIGHT_RATIO, FONT, INK_FILL_MIN, _XY, dot, moravia, note, polyline,
    profile_axes, profile_points, puddle_body, render, text,
)

HOLD = 5            # frames of pause on the finished state
MS = 620            # ms per frame

_only = sys.argv[1:]
_built = []


def emit_gif(name, frames, container="full", h=None, hold=HOLD, ms=MS):
    """Render every frame, crop them all to one box, and assert the same floors."""
    if _only and not any(k in name for k in _only):
        return
    w = DESIGN[container]
    hmax = h or int(w * 0.70)
    ims = [render(body, w, hmax) for body in frames]

    box = None
    for im in ims:
        a = np.array(im.convert("L"))
        ys, xs = np.where(a < 200)
        assert len(ys), f"{name}: a frame is blank"
        b = (xs.min(), ys.min(), xs.max(), ys.max())
        box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]),
                                     max(box[2], b[2]), max(box[3], b[3]))
    pad = int(PAD * PXBP)
    lo = max(0, box[1] - pad)
    hi = min(ims[0].size[1], box[3] + pad)
    ims = [im.crop((0, lo, im.size[0], hi)) for im in ims]

    fw, fh = ims[0].size
    scale = min(CONTAINER[container] / fw, MAX_FIG_H / fh, 1.0)
    factor = scale * PXBP
    want = CONTAINER[container] / w
    assert abs(factor - want) < 1e-6, (
        f"{name}: height binds the scale ({fh / PXBP:.0f}bp over all frames) -- "
        f"the drawing must be shorter than {w * MAX_FIG_H / CONTAINER[container]:.0f}bp")
    span = (box[2] - box[0] + 1) / fw
    assert span >= INK_FILL_MIN, f"{name}: ink spans {span:.0%} of the canvas width"
    node_px = NODE * factor
    assert NODE_MIN_PX <= node_px <= NODE_MAX_PX, f"{name}: node disc {node_px:.0f}px"
    x_px = FONT * XHEIGHT_RATIO * factor
    assert x_px >= TEXT_MIN_PX, f"{name}: text x-height {x_px:.1f}px on the slide"

    seq = ims + [ims[-1]] * hold
    pal = [im.convert("P", palette=Image.ADAPTIVE) for im in seq]
    pal[0].save(OUT / f"{name}.gif", save_all=True, append_images=pal[1:],
                optimize=False, duration=ms, loop=0, disposal=2)
    _built.append(name)
    print(f"  {name}.gif  {len(seq)} frames  {fw}x{fh}  node {node_px:.0f}px")


# --------------------------------------------------------------------------- MST runs
def kruskal_frames():
    """One frame per decision, including the refusal."""
    added, out = [], []
    out.append(moravia(faint=ALL_CABLES, weights=ALL_CABLES,
                       extra_text=note("0 km", color="annot")))
    for a, b, w, act in KRUSKAL:
        if act == "skip":
            out.append(moravia(
                faint=[e for e in ALL_CABLES if e not in added and e != (a, b)],
                edges=list(added), heavy={(a, b): "accenttwo"}, struck=[(a, b)],
                weights=list(added) + [(a, b)],
                extra_text=note(f"{w}: a loop")))
            continue
        added.append((a, b))
        out.append(moravia(
            faint=[e for e in ALL_CABLES if e not in added],
            edges=list(added), heavy={(a, b): "accenttwo"}, weights=list(added),
            extra_text=note(f"{sum(km(e) for e in added)} km")))
    total = sum(km(e) for e in added)
    assert total == MST_TOTAL and len(added) == 7, (total, len(added))
    return out


def prim_frames():
    grown, out = [], []
    out.append(moravia(faint=ALL_CABLES, weights=ALL_CABLES,
                       rings={"Brno": "accenttwo"},
                       extra_text=note("0 km", color="annot")))
    for u, v, w in PRIM:
        grown.append((u, v))
        reached = {"Brno"} | {n for e in grown for n in e}
        out.append(moravia(
            faint=[e for e in ALL_CABLES if e not in grown],
            edges=list(grown), heavy={(u, v): "accenttwo"}, weights=list(grown),
            rings={n: "accent" for n in reached},
            extra_text=note(f"{sum(km(e) for e in grown)} km")))
    assert sum(km(e) for e in grown) == MST_TOTAL
    return out


def boruvka_frames():
    """Every component picks its own cheapest cable at once -- two rounds, not seven."""
    out = [moravia(faint=ALL_CABLES, weights=ALL_CABLES,
                   extra_text=note("8 pieces", color="annot"))]
    picked = []
    for i, rnd in enumerate(BORUVKA_ROUNDS, 1):
        new = [(a, b) for a, b, _ in rnd]
        out.append(moravia(faint=[e for e in ALL_CABLES if e not in picked + new],
                           edges=list(picked),
                           heavy={e: "accenttwo" for e in new},
                           weights=picked + new,
                           extra_text=note(f"round {i}: {len(new)}")))
        picked += new
        out.append(moravia(faint=[e for e in ALL_CABLES if e not in picked],
                           edges=list(picked), weights=list(picked),
                           extra_text=note(f"{sum(km(e) for e in picked)} km")))
    assert sum(km(e) for e in picked) == MST_TOTAL
    return out


def profile_frames():
    """The curve appearing point by point as towns fall, in attack order."""
    X, Y = _XY()
    pts = profile_points(ATTACK_PROFILE)
    out = []
    for k in range(len(pts)):
        s = profile_axes()
        s += polyline(pts[:k + 1], color="accenttwo", w=4.0) if k else ""
        s += "".join(dot(x, y, "accenttwo") for x, y in pts[:k + 1])
        if k:
            gone = ATTACK_ORDER[k - 1]
            s += text(880, Y(0.62), NAME[gone] + "\\\\gone", color="accenttwo",
                      anchor="west")
            s += text(880, Y(0.28), f"${float(ATTACK_PROFILE[k - 1]):.3f}$",
                      color="black", anchor="west")
        else:
            s += text(880, Y(0.62), "all eight\\\\connected", color="annot",
                      anchor="west")
        out.append(s)
    return out


def puddle_frames():
    return [puddle_body(p, PUD_FIELD[:10], 80)[0]
            for p in (0.30, 0.40, 0.48, 0.54, 0.58, 0.62, 0.66, 0.72, 0.80)]


ANIMS = [
    ("kruskal", kruskal_frames, "full", FULL_H),
    ("prim", prim_frames, "full", FULL_H),
    ("boruvka", boruvka_frames, "full", FULL_H),
    ("profile-build", profile_frames, "full", 420),
    ("puddle-sweep", puddle_frames, "full", 440),
]


def main():
    for name, fn, cont, h in ANIMS:
        if _only and not any(k in name for k in _only):
            continue
        emit_gif(name, fn(), cont, h)
    print(f"\n{len(_built)} animations written")


if __name__ == "__main__":
    main()
