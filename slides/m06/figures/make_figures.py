#!/usr/bin/env python3
"""Generate every Module 06 slide figure (deck v2, 2026-10).

    python3 figures/make_figures.py            # all of them
    python3 figures/make_figures.py quiz       # only figures whose name contains "quiz"

Prerequisites, built once and kept in the gitignored figures/data/:

    uv run figures/make_ny.py          # the NY State highway network (OSM)
    uv run figures/make_basemap.py     # the Roman basemap (OSM tiles)

The pipeline and every gate live in `figlib.py`; every small-graph number lives in
`smallgraphs.py`; the Roman map geometry lives in `romelib.py`. One module per part of
the deck, so the parts could be authored in parallel:

    figs_intro.py    the Roman map and its turn into a network
    figs_ny.py       the New York State highway maps
    figs_defs.py     definition animations, the two ways to count, the classification grid
    figs_quiz.py     the two-graph questions and their answers
    figs_eigen.py    eigenvectors, localization, Katz
    figs_decomp.py   the eigendecomposition in circles and bars
    figs_dir.py      HITS and PageRank

Five figures are kept from the v1 deck (2026-08) and still built by its modules:
roma-degree and two-roads-ahead (figs_rome), star-closeness and sigma-answer
(figs_small), genealogy (figs_web).
"""

import figs_decomp
import figs_defs
import figs_dir
import figs_eigen
import figs_intro
import figs_ny
import figs_quiz
import figs_rome
import figs_small
import figs_web
from figlib import run

KEPT_V1 = {"roma-degree", "two-roads-ahead", "star-closeness", "sigma-answer", "genealogy"}

FIGURES = (figs_intro.FIGURES + figs_ny.FIGURES + figs_defs.FIGURES + figs_quiz.FIGURES
           + figs_eigen.FIGURES + figs_decomp.FIGURES + figs_dir.FIGURES
           + [f for f in figs_rome.FIGURES + figs_small.FIGURES + figs_web.FIGURES
              if f[0] in KEPT_V1])

_names = [n for n, _ in FIGURES]
assert len(_names) == len(set(_names)), \
    f"duplicate figure name: {sorted({n for n in _names if _names.count(n) > 1})}"
assert KEPT_V1 <= set(_names), f"missing v1 figures: {KEPT_V1 - set(_names)}"

if __name__ == "__main__":
    print(f"building {len(FIGURES)} figures")
    run(FIGURES)
