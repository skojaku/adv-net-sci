#!/usr/bin/env python3
"""The Watts-Strogatz rewiring, animated.

Geometry, palette and the emit pipeline all come from `make_figures.py`, so the ring in
the GIF is pixel-identical to the ring on the static slides either side of it -- the m01
lesson that two files drawn from two sources drift apart within one review round.

    python3 figures/make_animations.py
"""

import random
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

import make_figures as F

OUT = Path(__file__).resolve().parent
FRAME_MS = 620
FINAL_MS = 6000   # the end state, held long enough to talk over


def _render(body, w, hmax, name="frame"):
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "f.tex").write_text(F._tex(body, w, hmax))
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"],
                           cwd=td, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("\n".join(r.stdout.splitlines()[-25:]))
        subprocess.run(["pdftoppm", "-png", "-r", str(F.DPI), "-singlefile", "f.pdf", "f"],
                       cwd=td, check=True)
        im = Image.open(td / "f.png").convert("RGB")
        im.load()
        _assert_inside(name, im, w, hmax)
        return im


def _assert_inside(name, im, w, hmax):
    """The page IS the bounding box, so ink at its edge is ink being cut off.

    `emit()` has had this check since the first build and `make_animations.py` did not,
    so the GIF's caption shipped clipped at BOTH ends on every frame -- it rendered as
    `ewired so far: 0 of the 32 lattice edge`, six ink pixels in column 0 and seven in
    the last, and nothing in the build said a word.
    """
    a = np.array(im.convert("L"))
    ys, xs = np.where(a < 200)
    assert len(ys), f"{name}: blank frame"
    for side, hit in (("top", ys.min() <= 1), ("bottom", ys.max() >= a.shape[0] - 2),
                      ("left", xs.min() <= 1), ("right", xs.max() >= a.shape[1] - 2)):
        assert not hit, (f"{name}: ink runs off the {side} of the {w}x{hmax}bp canvas -- "
                         f"it is being clipped, shorten the label or widen the drawing")


def rewire_frames():
    """One frame per rewiring, on the same ring as ws-rewire-step.png."""
    rng = random.Random(20260805)
    lattice = list(F.RING_EDGES)
    edges = list(lattice)
    frames = [(list(edges), None, None)]
    order = list(range(len(edges)))
    rng.shuffle(order)
    moved = 0
    for idx in order:
        if moved == 6:
            break
        a, b = edges[idx]
        if rng.random() < 0.55:
            continue
        cand = [c for c in range(F.RING_N)
                if c != a and (min(a, c), max(a, c)) not in edges and c != b]
        if not cand:
            continue
        c = rng.choice(cand)
        edges[idx] = (min(a, c), max(a, c))
        moved += 1
        frames.append((list(edges), (a, b), edges[idx]))
    assert moved >= 4, f"only {moved} edges rewired -- the build would show nothing"
    return frames


def main():
    frames = rewire_frames()
    lattice = set(F.RING_EDGES)
    imgs = []
    for k, (edges, old, new) in enumerate(frames):
        # the surviving lattice straight, on the same antiprism the static ring uses;
        # rewired ends bowed clear of whatever they now pass
        s = F._lattice_edges(edges=[e for e in edges if e in lattice],
                             name=f"ws-rewire frame {k}")
        for a, b in edges:
            if (a, b) in lattice:
                continue
            s += F.curve_edge(a, b, F.RING_POS, color="accenttwo", w=F.HEAVY_W,
                              centroid=F.RING_C, clear=F.NODE / 2 + 3)
        if old:
            s += F.curve_edge(old[0], old[1], F.RING_POS, color="annot", w=2.2,
                              dash="dash pattern=on 8bp off 7bp", centroid=F.RING_C,
                              clear=F.RING_CLEAR)
        for i in F.RING_POS:
            s += F.disc(F.RING_POS[i][0], F.RING_POS[i][1], "", fill="accent")
        n_new = sum(1 for e in edges if e not in lattice)
        # short enough to fit: the old label was ~6% wider than the canvas and the crop
        # is full-width, so it was clipped at both ends on every frame
        s += F.text(260, 8, f"rewired: {n_new} of {len(lattice)}",
                    color="accenttwo", anchor="south")
        imgs.append(_render(s, F.DESIGN["col"], int(F.DESIGN["col"] * 0.70),
                            name=f"ws-rewire frame {k}"))

    # crop every frame to the same box, so the ring does not jump between frames
    w, h = imgs[0].size
    box = (0, int(0.02 * h), w, int(0.99 * h))
    imgs = [im.crop(box).resize((im.size[0] // 2, (box[3] - box[1]) // 2), Image.LANCZOS)
            for im in imgs]
    # Plays once and stops on the end state.
    #
    # `loop=0` is GIF for "forever", so the slide never rested on the state its prose
    # describes -- the ring kept resetting to the lattice under a body claiming the
    # shortcuts are there now.  Omitting `loop` entirely writes no Netscape looping
    # extension, which is what makes a viewer play the frames once; passing `loop=1`
    # would not, because most viewers read that as "repeat once more", i.e. twice.
    # The last frame's own delay is long so the end state is also readable in any viewer
    # that ignores the absent extension and loops anyway.
    # Lead with the frame that carries the claim. A GIF's FIRST frame is what the PNG
    # export, the PDF and the printed handout show, and frame 0 was the untouched
    # lattice: the static slide showed zero rewired chords under a body reading "six
    # edges move ... a handful of long chords now cut across it", and was structurally
    # the same drawing as the ring-lattice figure six slides earlier. Put the end state
    # first, then replay the build.
    imgs = [imgs[-1]] + imgs
    durations = [FINAL_MS] + [FRAME_MS] * (len(imgs) - 2) + [FINAL_MS]
    imgs[0].save(OUT / "ws-rewire.gif", save_all=True, append_images=imgs[1:],
                 duration=durations, optimize=True)
    # The GIF is generated, so it belongs in the manifest the gate reads: it has
    # in-figure type whose size this build controls, and must be held to the same
    # height-cap reasoning as every other drawn figure.
    import json
    man = OUT / "_generated.json"
    names = set(json.loads(man.read_text())) if man.exists() else set()
    man.write_text(json.dumps(sorted(names | {"ws-rewire"})))
    print(f"  ws-rewire.gif  {imgs[0].size[0]}x{imgs[0].size[1]}  {len(imgs)} frames, "
          f"plays once, {FINAL_MS}ms on the last")


if __name__ == "__main__":
    main()
