# Module 03 — Marp deck

Borůvka's minimum spanning tree, breaking it, percolation, the Molloy–Reed
criterion, and robust-yet-fragile. Story plan and lecturer decisions: `plan.md`.

## Files

    m03-robustness.md     the deck
    network-science.css   the theme (from marp-samples)
    figures/              PNG/JPG assets (prefer PNG over SVG in Marp)

## Figures note

Marp wraps each slide in an SVG `foreignObject`. Nested `<img src="*.svg">`
often renders blank in preview/HTML. Use PNG/JPG for slide assets.

## Build

    npm i -g @marp-team/marp-cli

    marp m03-robustness.md --theme network-science.css --allow-local-files --html --no-stdin -o m03-robustness.html
    marp m03-robustness.md --theme network-science.css --allow-local-files --html --no-stdin --pdf
    marp m03-robustness.md --theme network-science.css --allow-local-files --html --no-stdin --pptx

`--html` is not optional: without it Marp's default safelist strips the `<script>`
and `<button>` tags the two animation stages are made of, and the slides print
their own source to the room instead.

Or in VS Code with the Marp extension, add to settings.json:

    "markdown.marp.themes": ["./network-science.css"]

Math is KaTeX (`math: katex` in the front matter), so `$...$` and `$$...$$` work as written.

## Design tokens

    accent          #3959A6
    accent 2        #B14434
    accent 3        #DAB167
    text            #000000
    annotation      #6b6b6b
    rule            #dddddd
    formula panel   #f7f4f1

    body            Libre Baskerville 400
    figure labels   Caveat

## Conventions

    <!-- _class: lead -->     title slide (keep sub/credit on same slide)
    <!-- _class: part -->      part divider
    ## Title + <hr>           title and rule on the SAME slide as content
                              (do not use --- after titles — that splits slides)
    <div class="cols">         two-column body
    <div class="formula">      tinted formula panel
    <div class="note">         gray annotation copy
    <!-- ... -->               speaker notes

## Animation stages

Two slides mount the lecture note's animation kit rather than a GIF: `mst-race`
(Kruskal and Prim on one grid) and `rf-attack` (random failure, then an
adversary). The scene arrays live in `lecture-note/assets/anim/<stage>.js` and
the note page mounts the same files, so the two can never drift. The kit's
slide-sized stylesheet is at the bottom of `network-science.css`.

`<script>window.animStepOnly = true;</script>` runs once, before the first
`anim.js`, and puts every stage in this deck into step mode: the Pause button is
removed and nothing advances until the lecturer presses ▶.

Regenerate diagrams:

    python figures/make_figures.py   # needs networkx + matplotlib
