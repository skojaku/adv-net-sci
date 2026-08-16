# SSIE 641 Advanced Topics on Network Science

- [Lecture note](https://skojaku.github.io/adv-net-sci)
- [Syllabus](syllabus/syllabus.pdf)
- [Slides](slides)
- [Exercises](notebooks)

## Repository layout

| Path | What it holds |
|------|---------------|
| `lecture-note/` | The Quarto website published to GitHub Pages. Module pages, worksheets (`m0X/pen-and-paper/`), figures. |
| `slides/` | Marp decks (`m01`–`m06`, `intro`) plus the old Quarto revealjs decks under `slides/legacy/`. See [slides/README.md](slides/README.md). |
| `notebooks/` | Marimo/Jupyter coding exercises. Linked from the lecture note by URL — do not move or rename. |
| `syllabus/` | `syllabus.tex` and the built PDF. |
| `exam/` | Quiz sources (`quiz.json`) and the Marp generator. |
| `tutor-references/` | Per-module concept and code reference extracts. |
| `tutor-prototype/` | **Studio** — the AI-guided notebook assignment: the `pi-studio` toolkit and the module folders, published to `sk-classroom`. |
| `tools/` | Figure build, hands-on page generation, grading helpers. |
| `data/` | Course datasets. |
| `curriculum.yml` | Hand-authored concept inventory. Source of truth, not generated. |

Nothing generated is committed — no `_site/`, no `_freeze/`, no rendered slides,
no script-built figures. Build them:

```sh
bash tools/build_figures.sh   # lecture-note/figs/*.svg
quarto render lecture-note    # the website
```

CI (`.github/workflows/quarto-publish.yml`) runs both on every push to `main`
and publishes to the `gh-pages` branch.

## Set up the environment

The course Python packages are listed in
[lecture-note/environment.yml](lecture-note/environment.yml), installable with
[Anaconda](https://www.anaconda.com/products/distribution) or
[Miniconda](https://docs.conda.io/en/latest/miniconda.html):

```sh
conda env create -f lecture-note/environment.yml && conda activate advnetsci
```

Building figures needs only a small subset — see `tools/figures-requirements.txt`
and `slides/requirements.txt`.
