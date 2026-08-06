#!/usr/bin/env python3
"""Generate every Module 04 slide figure.

    python3 figures/make_figures.py            # all of them
    python3 figures/make_figures.py feld       # only figures whose name contains "feld"

The pipeline and every gate live in `figlib.py`; every number lives in
`verify_numbers.py`; the shared layout of Feld's eight girls lives in `feld.py`. The
figures themselves are split three ways only so they can be authored in parallel:

    figs_story.py   Parts 1-4   the eight girls, the theorem, the applications
    figs_tail.py    Parts 5-6   degree distributions, CCDFs, where hubs come from
    figs_edge.py    Parts 7-8   edge cases, the straight line that proves nothing

Nothing here stops at the first failure: `figlib.run()` catches per figure, prints every
failure and exits non-zero at the end. These gates fire in clusters -- raising the type
size broke seven of m03's figures at once -- and stopping at figure 3 of 60 turns one
round of fixes into seven.
"""

import figs_edge
import figs_story
import figs_tail
from figlib import run

FIGURES = figs_story.FIGURES + figs_tail.FIGURES + figs_edge.FIGURES

_names = [n for n, _ in FIGURES]
assert len(_names) == len(set(_names)), \
    f"duplicate figure name: {[n for n in _names if _names.count(n) > 1]}"

if __name__ == "__main__":
    print(f"building {len(FIGURES)} figures")
    run(FIGURES)
