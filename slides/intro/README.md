# Course intro deck

Marp rebuild of `slides/legacy/archive/intro/slide00.qmd`.

## Build

```sh
cd slides/legacy/intro
python3 figures/prep_photos.py     # crop the photographs to their container's aspect
python3 figures/make_figures.py    # TikZ figures, 4 px per bp, gates included
marp intro.md --theme theme.css --allow-local-files --images png \
     -o review/slide.png --no-stdin
python3 check_render.py            # pixel-level gate; run it bare and read its exit status
```

Or the whole pipeline in one command:

```sh
cd ~/.claude/skills/slide
python3 -m gatelib review /path/to/slides/legacy/intro
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
- Imported images (journal figures, comics, screenshots) live in `figures/src/` and get a
  `prep_photos.py` entry. The gate's container check runs *before* `exempt_figures`, so an
  import still has to fit: aspect ≤ 0.352 full width, ≤ 0.708 in a column, and a file under
  ~3000 px wide is read as column-authored whatever the deck does with it.
- A portrait cannot meet either cap. Use `fit="pad"` rather than cropping through the subject.
- `html: true` is set, so `marp --html` keeps raw HTML (including an `<iframe>`) in the HTML
  export. The `--images png` and PDF paths escape it to visible text, so do not embed an
  iframe in a slide that has to survive the PDF.
