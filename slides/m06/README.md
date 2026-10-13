# Module 06 — Marp deck: centrality

Centrality, organised by two choices: which routes count (shortest paths or walks) and how
they become one number. Rome opens it, the New York State highways are the running real
network, and every measure gets a one-graph question where the central-looking node loses.
Lecturer decisions: `plan.md`. Slide list and figure groups: `review/DECK_SPEC.md`.

## Files

    m06-centrality.md     the deck (82 slides: day 1 is 1-41, day 2 is 42-82)
    network-science.css   the theme (this module's copy; MesloLGS NF body, brush underlines)
    scrub.js              steps a build's frames in the presentation (see below)
    figures/              generators; the PNGs and frames they write are not committed
    figures/photos/       the photographs (committed; credits in CREDITS.md)
    check_render.py       the render gate

## Build

Needs xelatex with `fontspec` and the font **MesloLGS NF** installed (the figures are set in
it), pdftoppm, Python with numpy, Pillow, networkx, and marp-cli.

    cd figures
    uv run make_ny.py          # once: the NY highway network (OSM, ~500 MB download)
    uv run make_basemap.py     # once: the Roman basemap (OSM tiles)
    python3 make_figures.py    # every figure; `python3 make_figures.py q-close` for some
    cd ..
    marp m06-centrality.md --theme network-science.css --html --allow-local-files --no-stdin -o m06-centrality.html
    marp m06-centrality.md --theme network-science.css --html --allow-local-files --no-stdin --images png -o review/slide.png
    python3 check_render.py && python3 ../gatelib/check_deck.py m06-centrality.md

`--html` on every invocation: the scrubber and the two live stages are scripts.

## Builds you step through

A figure in `<div class="fig scrub">` is a build: `figures/frames/<name>/00.png, 01.png, ...`.
In the presentation the figure starts at frame 0 and the right arrow (or a clicker) steps it;
a slider and ◀ ▶ appear under it for doing the same with the mouse. `data-at="k"` lets the
slide's first k bullets appear before the frames. The PDF/PNG export shows the last frame
(`figures/<name>.png`). Coming back to the slide from a later one shows the last frame.

## Design tokens (v3, the lecturer's own palette)

    ink             #30323D    text, outlines, edges (no pure black)
    muted           #8C847F    what is not the point
    pale / faint    #D9D3CF / #EFEBE8
    hot             #D9631E    the point of the slide; key terms (with a brush underline)
    cool            #1E96DC    second emphasis; high scores
    gold            #C08A1F    a route
    formula panel   #f7f4f1

    headings        Libre Baskerville
    body, labels    MesloLGS NF (fallback Menlo)
    math            KaTeX on the slides, Latin Modern in the figures
