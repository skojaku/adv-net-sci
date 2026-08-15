#!/usr/bin/env python3
"""Generate every Module 06 slide figure.

    python3 figures/make_figures.py            # all of them
    python3 figures/make_figures.py roma       # only figures whose name contains "roma"

The pipeline and every gate live in `figlib.py`; every number lives in
`verify_numbers.py`; the one Roman-map geometry that all seven metric figures share
lives in `romelib.py`. The figures are split four ways only so they can be authored
in parallel:

    figs_rome.py    Parts 1-4   the map, its crowns, and the story around it
    figs_small.py   the purpose-built small graphs (club, sigma, broker, star, path)
    figs_walk.py    Parts 5-6   eigenvector, power iteration, Katz
    figs_web.py     Parts 7-8   the directed web, and the closing figures
    figs_extra.py   three column-width figures the slides needed once written

Nothing here stops at the first failure: `figlib.run()` catches per figure, prints
every failure and exits non-zero at the end. These gates fire in clusters -- raising
the type size broke seven of m03's figures at once -- and stopping at figure 3 of 55
turns one round of fixes into seven.
"""

import figs_extra
import figs_rome
import figs_small
import figs_walk
import figs_web
from figlib import run

FIGURES = (figs_rome.FIGURES + figs_small.FIGURES + figs_extra.FIGURES
           + figs_walk.FIGURES + figs_web.FIGURES)

_names = [n for n, _ in FIGURES]
assert len(_names) == len(set(_names)), \
    f"duplicate figure name: {sorted({n for n in _names if _names.count(n) > 1})}"

if __name__ == "__main__":
    print(f"building {len(FIGURES)} figures")
    run(FIGURES)
