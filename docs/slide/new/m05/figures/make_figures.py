#!/usr/bin/env python3
"""Generate every Module 05 slide figure.

    python3 figures/make_figures.py              # all of them
    python3 figures/make_figures.py karate       # only figures whose name contains it

The pipeline and every gate live in `figlib.py`; the club's one cached layout lives in
`layout.py`; the drawing helpers specific to this deck live in `kfig.py`; every number
lives in `verify_numbers.py`. The figures are split three ways only so they stay
readable:

    figs_story.py    Parts 1-3   the club, the patterns, the cut
    figs_chance.py   Parts 4-6   modularity, Louvain, the SBM
    figs_doubt.py    Parts 7-9   the three lies, evaluation, the close

Nothing here stops at the first failure: `figlib.run()` catches per figure, prints every
failure and exits non-zero at the end. These gates fire in clusters -- raising the type
size broke seven of m03's figures at once -- and stopping at figure 3 of 70 turns one
round of fixes into seven.
"""

import figs_chance
import figs_doubt
import figs_story
from figlib import run

FIGURES = figs_story.FIGURES + figs_chance.FIGURES + figs_doubt.FIGURES

_names = [n for n, _ in FIGURES]
assert len(_names) == len(set(_names)), \
    f"duplicate figure name: {sorted({n for n in _names if _names.count(n) > 1})}"

if __name__ == "__main__":
    print(f"building {len(FIGURES)} figures")
    run(FIGURES)
