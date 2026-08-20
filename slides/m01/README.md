# Module 01 — Marp deck

Königsberg bridges, Euler paths, and the vocabulary of networks.

## Files

    m01-euler-tour.md     the deck
    network-science.css   the theme — identical to slides/intro/theme.css
    figures/              make_figures.py, make_animations.py, and their output
    check_render.py       the pixel gate

## Figures note

Marp wraps each slide in an SVG `foreignObject`. Nested `<img src="*.svg">`
often renders blank in preview/HTML. Use PNG/JPG for slide assets. GIF animates.

## Build

    npm i -g @marp-team/marp-cli

    python3 figures/make_figures.py       # needs networkx + matplotlib
    python3 figures/make_animations.py

    marp m01-euler-tour.md --theme network-science.css --allow-local-files --html --no-stdin -o m01-euler-tour.html
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --html --no-stdin --pdf
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --html --no-stdin --images png -o review/slide.png
    python3 check_render.py

Or in VS Code with the Marp extension, add to settings.json:

    "markdown.marp.themes": ["./network-science.css"]

Math is KaTeX (`math: katex` in the front matter), so `$...$` and `$$...$$` work as written.

## `--html` is not optional, and it is not a front-matter directive

Five slides carry live HTML: the CSR widget on "Store only the nonzeros"
(`<input type="range">` plus a script) and four animation stages (`<button>`s
plus two `<script src>`s each) — `kb-tracer`, `euler-builder`, `comp-sweep`,
`dir-reach`. Without `--html`, Marp escapes all of it
to literal text and prints the source code on the slide, in **every** export,
images and PDF included.

`html: true` in the front matter does **not** do this. Marpit has no such
directive, so the line is silently inert; the flag is the only thing that works.
Pass it to every invocation above, including the one the gate measures — that is
also what makes the gate see the same slide the lecture does.

`--no-stdin` is not optional either. Without it marp waits on stdin and never
finishes when it is not attached to a terminal.

## Animation

No stage is written here. Each is a scene array under
`lecture-note/assets/anim/`, mounted against the shared kit in
`lecture-note/assets/anim.{css,js}`. The deck carries only the markup and two
`<script src>` tags pointing back at it. Six stages, in slide order:

    kb-tracer       05  cross the seven bridges yourself, then see why you cannot
    euler-builder   25  two odd corners: the trail built, and the same graph strand
    route-namer     35  click a route, get it named walk / trail / path / cycle
    comp-sweep      41  breadth-first sweeps finding the three components
    dir-reach       50  point a five-corner town 64 ways; six of them work
    walk-power      67  the two routes behind (A^2) at (1,4), then k on a knob

`kb-tracer` is also mounted by the lecture note
(`m01-euler_tour/01-concepts.qmd`); the other five are the deck's alone so far,
but they live in the same place so the note can pick them up with three lines.

The slide-sized port of the kit's stylesheet lives in `network-science.css`
under "animation stage" and "per-stage rules"; only sizes differ from the note's
`assets/anim.css`, because a slide's body type is 30px where the note's is 18px.

Verifying an animation needs a browser, not a render. What worked here: serve
the repo (`python3 -m http.server`), point headless Chrome at a page holding the
stage, and drive it with `--virtual-time-budget` plus a small script that
dispatches the clicks. Checking that the `<script>` survived the export is not
the same as checking that it runs.

Two things that page should report, because a screenshot cannot: whether the
section overflowed its own 720px frame, and whether anything threw. Both of the
layout bugs found while adding the five new stages were invisible in the picture
and obvious in that one line of text.

## Design tokens

    accent (purple)   #593196    structure: nodes, edges, rules, part label
    contrast (red)    #c2410c    emphasis: key terms, the thing pointed at
    accent, lighter   #7a51c0    a second route, a second highlight
    ink               #22212b
    annotation        #76757c
    rule              #e6e4e0
    formula panel     #f6f4f9
    sketch paper      #fffdf8    animation stages only

    body              Iowan Old Style / Palatino / Georgia (system serif)
    hand              Excalifont, embedded in the theme as a data: URI

Nothing is fetched from a CDN. The palette is the lecture note's
(`lecture-note/scss/minimal.scss`); change it there and here together.

## Conventions

    <!-- _class: lead -->     title slide (keep sub/credit on same slide)
    <!-- _class: part -->      part divider
    ## Title + <hr>           title and rule on the SAME slide as content
                              (do not use --- after titles — that splits slides)
    <div class="cols">         two-column body
    <div class="formula">      tinted formula panel
    <div class="note">         gray annotation copy
    <!-- ... -->               speaker notes
