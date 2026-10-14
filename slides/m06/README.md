# Module 06 — Marp deck: centrality

Centrality, organised by two choices: which routes count (shortest paths or walks) and how
they become one number. Rome opens it, the New York State highways are the running real
network, and every measure gets a one-graph question where the central-looking node loses.
Lecturer decisions: `plan.md`. Slide list and figure groups: `review/DECK_SPEC.md`.

## Files

    m06-centrality.md     the deck (131 slides: day 1 is 1-61, day 2 is 62-131)
    theme.css             the house theme (slide skill, house/theme-house.css) plus an m06
                          appendix: the power-iteration chart and a fixed figure box (below)
    scrub.js              injects the pencil filter the two live stages use
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
    marp m06-centrality.md --theme-set theme.css --html --allow-local-files --no-stdin -o m06-centrality.html
    cd ~/.claude/skills/slide && python3 -m gatelib review <this directory>   # render, check, review images

`--html` on every invocation: the two live stages are scripts. The theme must be passed as
`--theme-set theme.css`; without it marp falls back to its default theme without a warning.

## Layouts (2026-10-14, the slide skill's HOUSE_STYLE sections 8 to 10)

Every slide takes one layout class. The title is the message; most slides have no other text.

    L-a     title, one line under it (.sub: a formula or a question's rule), the figure,
            one line at the bottom (.take: the answer or the result)
    L-b     title over a big figure (the New York maps, the grid)
    left    plain two columns, text beside the figure: only where two or three terms are
            defined beside one figure (paths and walks, betweenness, HITS)
    L-e     the Golden Milestone photographs;  L-q  Aesop;  L-f  the closing quiz
    part    each part opens on its question

A question and its answer are the same slide with the answer added as the .take; the figure
does not move. The m06 appendix of theme.css makes that hold: in L-a and L-b the figure sits in
a box of fixed height, so a .take or a cue under it, or a formula in the .sub, cannot push it.
A figure drawn for the 537 px column is shown at 1.0 to 1.25 times its authored size.

## Builds

A build is a run of slides with the same title, one per frame
(`figures/frames/<name>/00.png, 01.png, ...`): the first slide shows frame 00 (equal to the
previous slide's figure) and carries the speaker notes; each later slide changes one thing and
its note says what. No slider, no GIF, no autoplay.

## Design tokens (the lecturer's own palette)

    ink             #30323D    text, outlines, edges (no pure black)
    muted           #8C847F    what is not the point
    pale / faint    #D9D3CF / #EFEBE8
    hot             #D9631E    the point of the slide; key terms (with a brush underline)
    cool            #1E96DC    second emphasis; high scores
    gold            #C08A1F    a route
    formula panel   #f7f4f1

    titles          MesloLGS NF bold, centred, 44 px (one line: at most 40 characters)
    body, labels    MesloLGS NF (fallback Menlo); Libre Baskerville only for the quotation
    math            KaTeX on the slides, Latin Modern in the figures
