# Module 03 — Marp deck

Build it (the minimum spanning tree), break it (the robustness profile), predict it
(percolation, kappa, Molloy–Reed, f_c) and design it (robust-yet-fragile). 32 slides.
Slide-by-slide plan: `review/DECK_SPEC.md`; the original 78-slide story plan: `plan.md`.

The pen-and-paper sheet (`lecture-note/m03-robustness/pen-and-paper/exercise.tex`) runs
**before** the lecture, so the deck names what the students already built and broken by
hand rather than deriving it again. `review/DECK_SPEC.md` has the question-by-question
map of what that let us cut.

## Files

    m03-robustness.md     the deck
    network-science.css   the theme (from marp-samples) + the five stages' rules
    figures/              PNG assets (prefer PNG over SVG in Marp)

## Figures note

Marp wraps each slide in an SVG `foreignObject`. Nested `<img src="*.svg">`
often renders blank in preview/HTML. Use PNG/JPG for slide assets.

## Build

    npm i -g @marp-team/marp-cli

    marp m03-robustness.md --theme network-science.css --allow-local-files --html --no-stdin -o m03-robustness.html
    marp m03-robustness.md --theme network-science.css --allow-local-files --html --no-stdin --pdf
    marp m03-robustness.md --theme network-science.css --allow-local-files --html --no-stdin --pptx

`--html` is not optional: without it Marp's default safelist strips the `<script>`
and `<button>` tags the five animation stages are made of, and the slides print
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

**At most two lines of body text on a slide.** The room gets 1–2 minutes a slide and
cannot read a paragraph in that time; the title carries the claim, the figcaption carries
what the drawing does not say, and everything else is spoken. A third line is not a style
question: it pushed five slides past `check_render`'s CONTENT_BOTTOM here. Where a stage
exists it comes *before* the static figure that freezes its last frame.

**Every term is defined where it is first used, and used precisely after that.** No
analogy stands in for a definition — the percolation half is site percolation on a square
lattice with occupied cells and clusters, and the two removal orders are named random
failure and targeted attack. No rhetoric, and no sentence that carries no fact.

## Animation stages

Five slides mount the lecture note's animation kit rather than a GIF. The scene arrays
live in `lecture-note/assets/anim/<stage>.js`, so a stage the note page also mounts can
never drift from the deck's copy. The kit's slide-sized stylesheet, and one block per
stage, are at the bottom of `network-science.css`.

    mst-race        Kruskal, Prim, and the cut property (slide 6)
    break-profile   the robustness profile drawn one removal at a time (slide 10)
    percolation     site percolation on a square lattice, with p on a dial (slide 15)
    branch-out      edge ends, <k> against kappa, kappa-1, the dial for f (slide 18)
    rf-attack       random failure and targeted attack on two networks (slide 27)

A scene may carry **two** notes. `note` is the lecture note's account of a drawing its
reader cannot see and runs to a paragraph; `short` is the one line a slide shows instead.
`mountScenes` takes `short` whenever `window.animStepOnly` is set, which is every deck, so
the note page keeps its prose and the room gets a caption.

**Type inside a stage is 1.5x the lecture note's**, set once near the top of the per-stage
block: scene label 39px, note 31px, readout 30px, verdict 34px, and SVG labels 20 viewBox
units. That size is why each stage carries half the text it used to — a paragraph does not
fit at 31px, which is the point. Measured on the rendered slides: **1181 -> 634 characters
of visible text per scene, summed over the five stages**.

Two consequences to keep in mind when editing a stage:

- **A stage has at most four text slots per scene**: the label in the bar, the one-line
  note, the readout of numbers, and a two-part verdict. There is no caption any more —
  every caption in the three new stages was either the note said twice or something the
  drawing already showed. The two shared stages keep theirs for the note page and hide
  them on the slide (`.rf-cap`, `.mst-log` are `display: none` here).
- **A verdict is one phrase.** The kit's `.anim-tally` is `space-between`, written for the
  note's narrow column; on a slide that pushes the two halves to opposite ends of the row
  and they stop reading as a sentence, so the four verdicts are re-centred here.

`<script>window.animStepOnly = true;</script>` runs once, before the first
`anim.js`, and puts every stage in this deck into step mode: the Pause button is
removed and nothing advances until the lecturer presses ▶.

`break-profile`, `percolation` and `branch-out` all print numbers. Every one of them is
either pasted in from an offline computation (with the reproduction recipe in the file's
header comment) or computed in the browser **from the drawing on screen**, so the picture
and its number cannot disagree. `branch-out` and `figures/kappa-def.png` draw the same ten
nodes at the same positions, and `figures/fc-formula.png` is drawn for that network's
kappa = 3, so the dial the room turns and the line the next slide shows are the same fact.

Regenerate diagrams:

    python figures/make_figures.py   # needs networkx + matplotlib

## Gates

    python3 figures/make_figures.py
    python3 -c "import sys; sys.path.insert(0,'..'); from gatelib.check_deck import run; run('m03-robustness.md')"
    marp m03-robustness.md --theme network-science.css --allow-local-files --html \
         --no-stdin --images png -o review/slide.png
    python3 check_render.py

A render proves the stage markup survived, not that the stage works. To check that, export
the HTML, append a driver script that clicks each `[data-anim-next]` through every dot, and
read the result back out of the DOM:

    marp m03-robustness.md --theme network-science.css --allow-local-files --html \
         --no-stdin -o m03-robustness.html
    # append a <script> that steps every stage, writes errors and
    # (section.scrollHeight - section.clientHeight) into a #RESULT div, then:
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
        --allow-file-access-from-files --virtual-time-budget=120000 --dump-dom \
        "file://$PWD/_drive.html" | grep -A40 RESULT

The overflow number is the one that matters: a stage that runs off the bottom of the 720px
frame looks perfectly fine in a screenshot.
