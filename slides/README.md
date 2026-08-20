# Slides

```
slides/
  m01/ … m06/       Marp decks — the current generation. One dir per module:
                      m0X-<topic>.md    the deck (source of truth)
                      network-science.css  theme
                      figures/*.py      figure + animation generators
                      check_render.py   render gate (thin wrapper around gatelib)
                      review/*.md       deck spec and fix logs
  intro/            Marp deck for the course intro (intro.md + theme.css)
  legacy/           The old Quarto revealjs decks (m01–m09 + intro), kept as
                    source for the modules not yet ported to Marp (m07–m09).
                    These need a `advnetsci` Jupyter kernel to render.
  gatelib -> ~/.claude/skills/slide-build/gatelib
  DECK_BUILD_GUIDE.md  SLIDE_RUBRIC.md  FIGURE_GUIDE.md  REVIEW_PLAYBOOK.md
  FILLER_PASS.md    the last stage: cut the padding out of a finished deck
```

Nothing generated is committed: figures, GIFs, review screenshots, HTML and PDF
are all rebuilt from the sources above.

## Building a deck

```sh
cd slides/m01
../../.venv-figs/bin/python figures/make_figures.py     # static figures
../../.venv-figs/bin/python figures/make_animations.py  # GIFs
marp m01-euler-tour.md --theme network-science.css --allow-local-files \
     --images png -o review/slide.png --no-stdin
python3 check_render.py                                 # render gate
```

## One-time setup

```sh
uv venv .venv-figs && uv pip install --python .venv-figs/bin/python \
    -r tools/figures-requirements.txt -r slides/requirements.txt
tlmgr --usermode install standalone     # the figure scripts shell out to LaTeX
brew install marp-cli
```
