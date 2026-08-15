# Module 01 — Marp deck

Königsberg bridges, Euler paths, and the vocabulary of networks.

## Files

    m01-euler-tour.md     the deck
    network-science.css   the theme (from marp-samples)
    figures/              PNG/JPG assets (prefer PNG over SVG in Marp)

## Figures note

Marp wraps each slide in an SVG `foreignObject`. Nested `<img src="*.svg">`
often renders blank in preview/HTML. Use PNG/JPG for slide assets.

## Build

    npm i -g @marp-team/marp-cli

    marp m01-euler-tour.md --theme network-science.css --allow-local-files --html --no-stdin -o m01-euler-tour.html
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --html --no-stdin --pdf
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --pptx

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

## Why `--html`

The "Store only the nonzeros" slide carries an interactive CSR widget — a slider
that steps through the matrix rows, highlighting each row's contiguous slice of
`indices`/`data` as you drag. It needs raw `<script>` and `<input>`, which only
survive the HTML export when `--html` is passed. The flag is deck-wide: without
it that export escapes *all* raw HTML, including the `cols` layout.

`--no-stdin` is not optional either. Without it marp waits on stdin and never
finishes when it is not attached to a terminal.
