# Course intro deck

The first session: the H1N1 story, three systems with one shape, and how the
course works.

## Build

```sh
cd slides/intro
python3 figures/prep_photos.py     # crop the photographs to their container's aspect
python3 figures/make_figures.py    # TikZ figures, 4 px per bp, gates included
marp intro.md --theme theme.css --allow-local-files --html --no-stdin \
     --images png -o review/slide.png
python3 check_render.py            # pixel-level gate; run it bare and read its exit status
```

Or the whole pipeline in one command, from `slides/`:

```sh
python3 -m gatelib review intro
```

## One file to carry

`marp -o intro.html` writes HTML that still points at `figures/` and at the
animation kit two directories up, so the file alone is blank on any other
machine. The bundler inlines every local reference — images as base64 `data:`
URIs, the two animation scripts as literal text:

```sh
python3 ../bundle_deck.py intro.md            # -> intro.standalone.html, 12 MB
python3 ../bundle_deck.py intro.md --max-width 1600   # -> 8 MB, resized first
```

It exits non-zero if anything in the output still points outside the file. The
figures are authored at 4320 px wide and no projector resolves that, so
`--max-width` costs nothing visible; without it the bundle is pixel-identical to
the ordinary render. Works on any deck in `slides/` — it finds `theme.css` or
`network-science.css` beside the deck.

## PDF, and the two flags that wreck it

```sh
python3 ../bundle_deck.py intro.md --pdf      # -> intro.pdf, 59 pages, 960x540
```

It is routed through the same script only to pin the flags. Drop
`--allow-local-files` and marp still writes a PDF and exits 0, with every figure
gone. Drop `--html` and slide 12 prints its own `<button>` and `<script src>`
source as body text. Both failures are silent at the console, so when a PDF comes
out wrecked, that is the first thing to check.

One thing no static export can fix: slide 12 is a running animation, so the PDF
freezes it mid-draw at scene 1 of 4 and the readout panel is two lines short. The
PNG gate captures the same half-finished frame. Show that slide from the HTML.

## Layout

- `intro.md` — the deck
- `theme.css` — the `network-science` theme, byte-identical to
  `slides/m01/network-science.css`. Change one, copy to the other.
- `figures/make_figures.py` — every generated figure, authored at 4 px per bp
- `figures/prep_photos.py` — deterministic crops of the photographs in `figures/src/`
- `figures/src/` — untouched originals; never referenced by the deck
- `review/` — `DECK_SPEC.md`, rendered slides, review notes

## `--html` is not optional, and it is not a front-matter directive

The "Drag the ruler yourself" slide carries a live stage: `<button>`s and two
`<script src>` tags. Without `--html`, Marp escapes them to literal text and
prints the source on the slide, in every export, images and PDF included.

`html: true` in the front matter does **not** do this — Marpit has no such
directive, so the line is silently inert. (An earlier version of this file
claimed otherwise; the `<div class="cols">` layout it credited to that line
survives on its own, which is what made the claim look true.) Pass the flag to
every invocation, including the one the gate measures.

## Animation

The ruler swap is a scene array in `lecture-note/assets/anim/h1n1-ruler.js`,
mounted against the shared kit in `lecture-note/assets/anim.{css,js}`. The
lecture note's own `intro/why-networks.qmd` mounts the same file; this deck
carries only the markup and two `<script src>` tags pointing back at it. The
slide-sized port of the kit's stylesheet lives in `theme.css`.

The two published Brockmann and Helbing panels stay on the two slides before it.
They are the evidence; the stage is the thing a student can put a hand on.

## Design tokens

    accent (purple)   #593196    structure: nodes, edges, rules, part label
    contrast (red)    #c2410c    emphasis: key terms, the thing pointed at
    accent, lighter   #7a51c0    where a drawing needs a third value
    contrast, lighter #e0a184    the same, for the contrast
    ink               #22212b
    annotation        #76757c
    rule              #e6e4e0

    body              Iowan Old Style / Palatino / Georgia (system serif)
    hand              Excalifont, embedded in the theme as a data: URI

Nothing is fetched from a CDN. The palette is the lecture note's
(`lecture-note/scss/minimal.scss`); change it there and here together.

## Conventions worth not relearning

- Figures are authored at **4 px per bp**: full width 4320 px, `cols` column 2148 px.
  The render gate reads a file under ~3000 px wide as authored for a column.
- A figure taller than 0.352 × width (full) or 0.708 × width (`cols`) is scaled down
  by the 380 px height cap, which shrinks its type. `prep_photos.py` crops for that.
- No em-dashes anywhere in the deck; the gate fails on them.
- Fragments use `*`; `-` lists do not fragment. Four items per list, no more.
- Imported images (journal figures, comics, screenshots) live in `figures/src/` and get a
  `prep_photos.py` entry. The gate's container check runs *before* `exempt_figures`, so an
  import still has to fit: aspect ≤ 0.352 full width, ≤ 0.708 in a column, and a file under
  ~3000 px wide is read as column-authored whatever the deck does with it.
- A portrait cannot meet either cap. Use `fit="pad"` rather than cropping through the subject.
- Do not embed an `<iframe>` in a slide that has to survive the PDF.
