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
| `quiz/` | In-class paper quizzes: the LaTeX source, the solutions, and the script that builds the Google Form. |
| `syllabus/` | `syllabus.tex` and the built PDF. |
| `tutor-references/` | Per-module concept and code reference extracts. |
| `tools/` | Figure build and page generation. See [tools/README.md](tools/README.md). |
| `data/` | Course datasets. |
| `curriculum.yml` | Hand-authored concept inventory: every concept the course teaches, and which activity covers it. Source of truth, not generated. |

Everything here is material a student may read. The exam bank, the Pair Notebook
authoring copies, the LLM gateway, the roster and the operational scripts live
in a separate private repository — if you are looking for one of those, that is
where it went. Nothing that names a student belongs in this tree.

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

Building figures needs only a small subset. `tools/figures-requirements.lock`
is the exact environment the committed figures were built in — install from it,
not from the unpinned `tools/figures-requirements.txt` and
`slides/requirements.txt` behind it:

```sh
uv venv .venv-figs --python 3.12
uv pip install --python .venv-figs/bin/python -r tools/figures-requirements.lock
```
