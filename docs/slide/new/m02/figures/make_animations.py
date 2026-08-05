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

from PIL import Image

import make_figures as F

OUT = Path(__file__).resolve().parent
FRAME_MS = 620
HOLD = 5          # frames held at the end so the last state is readable


def _render(body, w, hmax):
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
        return im


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
    for edges, old, new in frames:
        s = ""
        for a, b in edges:
            fresh = (a, b) not in lattice
            s += F.curve_edge(a, b, F.RING_POS,
                              color="accenttwo" if fresh else "black",
                              w=F.HEAVY_W if fresh else F.EDGE_W, centroid=F.RING_C)
        if old:
            s += F.curve_edge(old[0], old[1], F.RING_POS, color="annot", w=2.2,
                              dash="dash pattern=on 8bp off 7bp", centroid=F.RING_C)
        for i in F.RING_POS:
            s += F.disc(F.RING_POS[i][0], F.RING_POS[i][1], "", fill="accent")
        n_new = sum(1 for e in edges if e not in lattice)
        s += F.text(260, 8, f"rewired so far: {n_new} of the {len(lattice)} lattice edges",
                    color="accenttwo", anchor="south")
        imgs.append(_render(s, F.DESIGN["col"], int(F.DESIGN["col"] * 0.70)))

    # crop every frame to the same box, so the ring does not jump between frames
    w, h = imgs[0].size
    box = (0, int(0.02 * h), w, int(0.99 * h))
    imgs = [im.crop(box).resize((im.size[0] // 2, (box[3] - box[1]) // 2), Image.LANCZOS)
            for im in imgs]
    imgs += [imgs[-1]] * HOLD
    imgs[0].save(OUT / "ws-rewire.gif", save_all=True, append_images=imgs[1:],
                 duration=FRAME_MS, loop=0, optimize=True)
    print(f"  ws-rewire.gif  {imgs[0].size[0]}x{imgs[0].size[1]}  {len(imgs)} frames")


if __name__ == "__main__":
    main()
