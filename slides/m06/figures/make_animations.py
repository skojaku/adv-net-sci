#!/usr/bin/env python3
"""The Module 06 animations, as looping GIFs.

Why GIF: the lecture is given from Marp's HTML output and the deck is meant to get
its density from motion rather than more text. Marp's sanitiser strips inline
`<svg>`, and an `<img>` pointing at `.svg` renders blank inside Marp's own
`foreignObject`; a GIF referenced by relative path just animates.

Geometry, palette and the TeX pipeline come from `figlib` and `romelib`, and every
number comes from `verify_numbers`, so a frame cannot drift from the still figure
beside it. In particular the last frame of `power-iteration.gif` is drawn from the
same score vector as `roma-eigenvector.png`, and that is asserted rather than
intended -- the loop has to hand off to the slide that follows it.

    python3 figures/make_animations.py
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figlib as F                                          # noqa: E402
import romelib as R                                         # noqa: E402
from figlib import (CONTAINER, DESIGN, FIG_H, FONT, INK_FILL_MIN, NODE,  # noqa: E402
                    NODE_MAX_PX, NODE_MIN_PX, OUT, PAD, PXBP, TEXT_MIN_PX,
                    calibrate, render)
from verify_numbers import (POWER_SHOW, POWER_TRACE, ROMA, ROMA_C,  # noqa: E402
                            ROMA_CROWNS)

HOLD = 6            # frames of pause on the settled state
MS = 700            # ms per frame

_only = sys.argv[1:]
_built = []
_failures = []


def emit_gif(name, frames, container="full", h=None, hmod="", hold=HOLD, ms=MS):
    """Render every frame, crop them all to ONE box, and assert the same floors.

    Cropping each frame to its own ink would make the drawing jump between frames,
    which reads as a fault in the projector rather than as a build.
    """
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
    edge = 2
    assert not (box[0] <= edge or box[1] <= edge
                or box[2] >= ims[0].size[0] - 1 - edge
                or box[3] >= ims[0].size[1] - 1 - edge), (
        f"{name}: ink runs off the canvas in some frame -- it is being CLIPPED")

    pad = int(PAD * PXBP)
    lo = max(0, box[1] - pad)
    hi = min(ims[0].size[1], box[3] + pad)
    ims = [im.crop((0, lo, im.size[0], hi)) for im in ims]

    fw, fh = ims[0].size
    hcap = FIG_H[hmod]
    scale = min(CONTAINER[container] / fw, hcap / fh, 1.0)
    factor = scale * PXBP
    want = CONTAINER[container] / w
    assert abs(factor - want) < 1e-6, (
        f"{name}: the HEIGHT binds the scale -- the frames are {fh / PXBP:.0f}bp tall "
        f"and a '{hmod or 'plain'}' figure may be at most {hcap}bp")
    span = (box[2] - box[0] + 1) / fw
    assert span >= INK_FILL_MIN, f"{name}: ink spans {span:.0%} of the canvas width"
    node_px = NODE * factor
    assert NODE_MIN_PX <= node_px <= NODE_MAX_PX, f"{name}: node disc {node_px:.0f}px"
    x_px = FONT * calibrate() * factor
    assert x_px >= TEXT_MIN_PX, f"{name}: text x-height {x_px:.1f}px on the slide"

    seq = ims + [ims[-1]] * hold
    pal = [im.convert("P", palette=Image.ADAPTIVE) for im in seq]
    pal[0].save(OUT / f"{name}.gif", save_all=True, append_images=pal[1:],
                duration=ms, loop=0, optimize=True, disposal=2)
    _built.append(name)
    print(f"  {name}.gif  {len(seq)} frames  {fw // 4}x{fh // 4}bp  "
          f"node {node_px:.0f}px  x-h {x_px:.1f}px  ink {span:.0%}")


# --------------------------------------------------------------------------- power
def power_frames():
    """One frame per iteration, shading the map by the score at that step.

    The step counter is drawn where the note placer says there is room, and the
    crown appears from step 1 -- which is the fact the slide is about, since the
    first sum is just a count of neighbours and therefore the degree ranking.
    """
    # The map fills its own canvas edge to edge -- `romelib.note()` reports, and it
    # is right, that a note does not fit anywhere clear on it. So the map is lifted
    # into a shifted scope and the step counter gets a reserved strip underneath,
    # rather than being dropped on top of a city name.
    LIFT = 26
    frames = []
    for t in range(0, POWER_SHOW + 1):
        scores = POWER_TRACE[t]
        top = max(scores.values())
        crowned = sorted(k for k, v in scores.items() if v > top - 1e-9)
        inner = R.map_body(scores=scores, crown_cities=[] if t == 0 else crowned)
        body = f"\\begin{{scope}}[yshift={LIFT}bp]\n{inner}\\end{{scope}}\n"
        body += F.text(24, 20, f"step {t}", color="accenttwo",
                       anchor="west")
        frames.append(body)
    # The loop has to hand off to the still figure on the next slide.
    last = POWER_TRACE[POWER_SHOW]
    ev = ROMA_C["eigenvector"]
    worst = max(abs(last[c] / max(last.values()) - ev[c] / max(ev.values()))
                for c in ROMA)
    assert worst < 0.01, (
        f"the last frame differs from roma-eigenvector.png by {worst:.3f} -- the "
        f"animation must settle on the picture the deck shows next")
    assert sorted(k for k, v in last.items() if v > max(last.values()) - 1e-9) \
        == ROMA_CROWNS["eigenvector"]
    return frames


def main():
    calibrate()
    for name, fn, kw in [("power-iteration", power_frames,
                          dict(container="full", h=470, hmod="tall"))]:
        try:
            emit_gif(name, fn(), **kw)
        except (AssertionError, SystemExit) as e:
            _failures.append((name, str(e)))
            print(f"  FAIL {name}: {e}")
    print(f"\n{len(_built)} animation(s) written, {len(_failures)} failed")
    if _failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
