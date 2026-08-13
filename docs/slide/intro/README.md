# Course intro deck

Marp rebuild of `docs/slide/archive/intro/slide00.qmd`.

## Build

```sh
cd docs/slide/intro
python3 figures/prep_photos.py     # crop the photographs to their container's aspect
python3 figures/make_figures.py    # TikZ figures, 4 px per bp, gates included
marp intro.md --theme theme.css --allow-local-files --images png \
     -o review/slide.png --no-stdin
python3 check_render.py            # pixel-level gate; run it bare and read its exit status
```

Or the whole pipeline in one command:

```sh
cd ~/.claude/skills/slide
python3 -m gatelib review /path/to/docs/slide/intro
```

## Layout

- `intro.md` — the deck
- `theme.css` — the bundled `network-science` theme
- `figures/make_figures.py` — every generated figure, authored at 4 px per bp
- `figures/prep_photos.py` — deterministic crops of the photographs in `figures/src/`
- `figures/src/` — untouched originals; never referenced by the deck
- `review/` — `DECK_SPEC.md`, rendered slides, review notes

## Conventions worth not relearning

- Figures are authored at **4 px per bp**: full width 4320 px, `cols` column 2148 px.
  The render gate reads a file under ~3000 px wide as authored for a column.
- A figure taller than 0.352 × width (full) or 0.708 × width (`cols`) is scaled down
  by the 380 px height cap, which shrinks its type. `prep_photos.py` crops for that.
- No em-dashes anywhere in the deck; the gate fails on them.
- Fragments use `*`; `-` lists do not fragment.
