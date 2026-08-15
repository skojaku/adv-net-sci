# Module 02 — Marp deck

Milgram's small-world experiment, path length and clustering, the σ index, and
the Watts–Strogatz model. Story plan and lecturer decisions: `plan.md`.

## Files

    m02-small-world.md     the deck
    network-science.css   the theme (from marp-samples)
    figures/              PNG/JPG assets (prefer PNG over SVG in Marp)

## Figures note

Marp wraps each slide in an SVG `foreignObject`. Nested `<img src="*.svg">`
often renders blank in preview/HTML. Use PNG/JPG for slide assets.

## Build

    npm i -g @marp-team/marp-cli

    marp m02-small-world.md --theme network-science.css --allow-local-files -o m02-small-world.html
    marp m02-small-world.md --theme network-science.css --allow-local-files --pdf
    marp m02-small-world.md --theme network-science.css --allow-local-files --pptx

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

Regenerate diagrams:

    python figures/make_figures.py   # needs networkx + matplotlib
