#!/usr/bin/env python3
"""Generate every Module 06 slide figure (deck v3, 2026-10-13).

    python3 figures/make_figures.py            # all of them
    python3 figures/make_figures.py quiz       # only figures whose name contains "quiz"

Prerequisites, built once and kept in the gitignored figures/data/:

    uv run figures/make_ny.py          # the NY State highway network (OSM)
    uv run figures/make_basemap.py     # the Roman basemap (OSM tiles)

The pipeline and every gate live in `figlib.py`; every small-graph number lives in
`smallgraphs.py`; the Roman map geometry lives in `romelib.py`. One module per part of
the deck, so the parts could be authored in parallel:

    figs_ui.py       the brush underline the theme puts under key terms
    figs_intro.py    the Roman map and its turn into a network
    figs_ny.py       the New York State highway maps
    figs_defs.py     definition animations, the two ways to count, the classification grid
    figs_quiz.py     the one-graph questions and their answers, and the CA group
    figs_eigen.py    eigenvectors, localization, Katz
    figs_decomp.py   the eigendecomposition in circles and bars
    figs_dir.py      HITS and PageRank

Three figures are still built by v1 modules: roma-degree (figs_rome), sigma-answer
(figs_small), genealogy (figs_web).

v3 style (the lecturer's own): xelatex with MesloLGS NF, hand-drawn discs, brush strokes,
grain; every build is a set of frames in figures/frames/<name>/ that the lecturer steps with
slides/m06/scrub.js, and figures/<name>.png is its last frame.
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
import figs_ui
import figs_web
from figlib import run

KEPT_V1 = {"roma-degree", "sigma-answer", "genealogy"}

FIGURES = (figs_ui.FIGURES + figs_intro.FIGURES + figs_ny.FIGURES + figs_defs.FIGURES + figs_quiz.FIGURES
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
