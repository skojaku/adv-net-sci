# House style — how Sadamori's lecture decks look, read and move

> Repo copy of `~/.claude/skills/slide/HOUSE_STYLE.md` (the canonical one; edit there and
> copy here). The `house/` kit it names lives in that skill folder; its worked example is
> `slides/m06/` (figures/figlib.py, figures/figs_ui.py, network-science.css).

**Wording (2026-10-31, important; check it in every review):** write plainly, directly and briefly, with no ornament
(「もっと端的に、シンプルに、直接的かつ簡潔に、飾らずに」). A title states the claim or the question literally and names things by
their technical term: no thematic titles ("One walk, three worlds"), no verbs of life or war for mathematical objects
("dies", "forgets", "sets the clock"), no metaphorical nouns ("rooms" for communities), no commands ("Measure it"). Rule N9 in
`SLIDE_RUBRIC.md`; it holds from the first wireframe.

Every rule below comes from his own review of a deck. It was settled on the Module 06
centrality deck (adv-net-sci `slides/m06/`), rebuilt three times in October 2026; that deck
is the worked example. He signed off on the result: 「色使い、スライドのつなぎ方、構成図、
テキストの構成や文字量など、すべて良くなった」. Build every new lecture deck this way.
The reference implementation is bundled in `house/`; see "Files" at the end.

This guide takes precedence over the older defaults in `DECK_BUILD_GUIDE.md` and
`FIGURE_GUIDE.md` where they disagree. Examples: the old palette (#3959A6 / #B14434, black
ink), Caveat captions, GIFs, and two-graph questions are all replaced here.

---

## 1. Slide flow: small differences

**The principle, in his words:** the cognitive cost of a slide change grows like n², where n
is the amount of new information. Consecutive slides must differ by little. Split
information rather than delivering it at once.

**Base layout.**
- Put the figure in the right half (`<div class="cols">`, the right column is 537 px).
- Put two to four short bullets in the left half, revealed one at a time (`*` list items
  fragment in Marp).
- Keep this layout on as many slides as possible.
- The exceptions are full width:
  - a classification grid;
  - a wide equation row;
  - a gallery of panels;
  - a live interactive stage.

**The drawing stays; it grows.**
- When consecutive slides talk about the same network, they show the same drawing at the
  same pixel position.
- The next slide adds one thing: a value, a mark, a bullet, a highlighted node.
- Build such figures as a group on one canvas and one crop. In figlib that means
  `emit_group(..., box=)`; across functions, a shared `box`.
- Avoid a fresh figure on every slide. His example: Rome map → NY map → graph was "too many
  figures".

**Questions: one graph per slide.**
- A two-graph question is two questions: Q1 → A1 → Q2 → A2.
- Showing both graphs at once "feels like two steps at once".
- Q and A share the title and the left text; A adds one line.
- Q and A share the crop: A is Q plus the values and the winner's mark. figlib asserts that
  the answer's TikZ starts with the question's.

**Builds are separate slides. No slider, no GIF, no autoplay.**
- He explains the bullets first, then steps the figure. So a build is a run of slides with
  the same title:
  - Slide 0 shows the bullets (fragments) and frame 00. Frame 00 is pixel-identical to the
    previous slide's figure.
  - Each following slide shows the same bullets, all visible (`-`), and the next frame.
- Each step changes **one** thing and carries a **callout** (section 4) saying what changed.
- Keep 3–5 steps.
- Animate only a process: a sum being formed, an iteration, a parameter sweep, a walk.
  Where the change is obvious, show the result statically. Examples: map → network, a
  matrix sum written out.
- Tools:
  - author the build once as `<div class="fig scrub">` with frames from
    `figlib.emit_frames`;
  - then run `house/split_builds.py deck.md` to expand it;
  - put one line per step in `figures/frames/<name>/steps.txt`.
- A slider widget (scrub.js) was tried and rejected: it is hard to talk over.

**Pacing.**
- One minute per content slide, at most about 45 content slides per 90-minute session.
- Build-step slides are extra and take seconds each. Say so in the title slide's notes.

**Story shape per module.**
- **Opener:** a concrete, memorable story, carrying only the facts the lecture uses.
- **A real local network:** for Binghamton students, the NY State highways. Map on the
  right, bullets on the left. It returns after every measure.
- **Per concept:** concept → formula → a one-graph question → answer → the same measure on
  the real network.
- **Questions must be a little tricky.** The node that looks central (the hub, or the node
  drawn in the middle of the picture) must not win, or two candidates must need computing.
  Draw the loser at the centre of the picture, and assert it in code (see
  `smallgraphs.check()` in m06).
- **Close a part** with a figure that classifies everything so far (m06: the two-axes grid).

## 2. Text: little, plain, and pointing at the figure

- **Amount:**
  - As little as his reference slides: two to four bullets per slide, each one idea,
    telegraphic.
  - At MesloLGS NF 30 px a 537 px column holds about 29 characters per line. Two lines per
    bullet is the most.
  - No sentences inside figures, only numbers and two- to five-word labels.
- **Figures over text.** If the figure shows a number, the bullet states the takeaway, not
  the number list.
- **Cut every fact the lecture does not use.** His example: "by the Temple of Saturn". A
  fact that cannot be sourced is not claimed (m06: the Golden Milestone's lost inscription).
- **Key terms:**
  - `**Term**` renders orange with a brush underline. Use it once, where the term is
    defined.
  - `<strong class="cool">` is the sky-blue variant, for a term the figure colours blue (m06:
    HITS "Authority").
- **Show the quantity the slide names.** If a centrality is "higher is better", show the
  centrality value, with the winner highest. Do not show an intermediate quantity where
  smaller wins.
  - m06 mistake: a closeness build ended on "sum of distances = 10", underlined, which read
    as "closeness = 10".
  - Show the sums as a step, then convert to (N−1)/sum. The answer is the highest value.
  - Say "Highest closeness wins: the smallest sum of distances."
- **A number a reader can add must be an amount.**
  - m06 mistake: PageRank's links were labelled with the share of the sender's score (1/3, 1).
    The lecturer added the shares: C = 1/3 + 1 + 1 = 7/3, not the 3/11 shown.
  - Label what flows (score × share: 1/11 on each link). Show the balance (in = out at every
    page) as a build.
- **A concrete instance, not a claim about all.**
  - "true at every node: λ = 2.88" did not land.
  - A second worked case did: "C: 0.58 = 2.88 × 0.20, the same 2.88".
- **Pick an example where the effect is visible.**
  - Betweenness's 1/2 split needs two shortest routes that share no node (s–A–D–t,
    s–B–C–t).
  - A shared node gets 1 and hides the split.
- **Index order follows the edge.** $A_{ij} = 1$ means a link from $i$ to $j$. Write every
  formula in that order: $c_j = \sum_i A_{ij} c_i / d^{out}_i$ and $a_j = \sum_i A_{ij} h_i$.
  Never write $A_{ji}$.
- **Nothing that reads as vulgar on a slide.** m06: the fable title *The Ass and His
  Purchaser* went to the notes.
- **Questions:**
  - The question is the slide title.
  - The left column holds one line of instruction.
  - A near-white cue (`<div class="cue">`, e.g. *Take a minute.*) goes below the columns.
  - A question slide never shows its answer.
- **Notes:** speaker notes carry the sources, the exact numbers, and what to ask the room.
- **No paragraph after a fragmented list.**

## 3. Colour: saturation carries importance

| token | hex | use |
|---|---|---|
| ink | `#30323D` | text, node outlines, edges. **Never pure black.** |
| muted | `#8C847F` | what is not the point: context labels, axis titles, callouts, removed edges |
| pale / faint | `#D9D3CF` / `#EFEBE8` | de-emphasised fills; the low end of a value scale |
| hot | `#D9631E` | **the point of the slide**: the winner, the answer, the key term |
| cool | `#1E96DC` | the second emphasis; high values on a value scale |
| gold | `#C08A1F` | a route or a walk (brush) |
| teal, olive, deep | `#3F8A88`, `#9B9922`, `#2F6FB4` | extra categories, desaturated, sparingly |

- **The whole palette is muted.** Only the point of the slide is saturated. A value scale
  runs faint → cool, so low values look unimportant. A live stage tops out at about 70%
  of cool, so that equal scores do not light everything up.
- **One meaning per colour across a run of slides.** If blue and orange mean
  positive/negative on one slide, they keep that meaning on the next slides too. m06 made
  the eigenvector bars neutral (`pale` fill, ink outline) for that reason, and put the step
  counter "t = 16" in ink, not orange.
- **The winner:**
  - its disc is filled hot;
  - its value is hot with a brush underline;
  - the other candidates' values are ink;
  - comparison tags ("best closeness") are muted.

## 4. Figures: hand-drawn, labelled at the node, every step annotated

He disliked clean vector figures and sent reference images from his own slides (a
random-walk tree; word2vec query/key diagrams). Match them as follows.

- **Font:**
  - labels in **MesloLGS NF** (`fontspec`, via xelatex), 30 pt at 1 bp = 1 slide px;
  - math in Latin Modern at ≥ 38 pt (its x-height is smaller);
  - numbers in Meslo ("27/4", "0.85"), not math.
- **Nodes:**
  - a white disc (default), with a dark pencil outline drawn twice slightly offset;
  - a letter in ink;
  - a grainy fill when coloured.
  - `F.disc(x, y, label, fill=...)`; fills are `white`, `pale`, `hot`, `cool`, or
    `F.shade(v)`.
- **Edges:** soft ink with a faint second pencil stroke, `F.seg`. Context edges are muted;
  a removed edge is dashed muted with a hot ×.
- **Routes and walks:** a brush stroke (`F.brush`), drawn **before** the discs so the nodes
  stay on top.
- **Underlines:** a thin tapered brush (`F.underline`) in the colour of what it marks.
- **Texture:** `figlib.grain()` mottles every coloured or grey pixel after rendering. It is
  keyed to pixel position, so two renders of the same drawing match.
- **Callouts (every build step, and every path):**
  - `F.callout(text, at, target)` draws muted text of at most ~5 words and a thin arrow to
    what changed.
  - Every highlighted path is named ("u → v: 2 steps", "s–A–C–t").
  - Reserve the callout room on the group's canvas so frames keep one crop.
- **Values sit directly above or below their own disc.**
  - Never put a value over an edge's midpoint: in a distance lecture it reads as an edge
    length.
  - Never put it level with a neighbour's disc.
  - Lay the graph out so this is possible (spread the drawing vertically, keep edges between
    discs ≥ ~45 bp).
  - On maps: leader lines, white halos behind labels, a muted "NYC"-style anchor on every
    map.
- **Matrix pictures** (m06 `figs_decomp.py`, the lecturer's notation):
  - Notation: a circle for an eigenvalue, a tall bar for $u_k$, a wide bar for $u_k^\top$.
  - Show at most three terms (1, 2, …, last), so each matrix is about 100 bp.
  - Colour each eigenvector by its index: $u_1$ blue, $u_2$ gold, the rest pale. Bars of
    one colour meeting give 1; bars of two colours give 0. Circles keep the sign colours.
  - Draw a product such as $A^2$ as two bracketed sums side by side. An arc joins the facing
    bars ($u_k^\top$ of the left term, $u_l$ of the right). Show one pair per step:
    different colours, then the same colour, then the result.
- **A parameter is a gauge on the left of the figure:**
  - a track with a knob;
  - the critical value as a tick;
  - the part past it shaded hot.
- **Plot the scalar function a formula applies to the eigenvalues.** For $1/(1-\alpha x)$,
  mark the eigenvalues as dots on the curve and the wall at $1/\alpha$. The blow-up and the
  sign flip are then visible, not just stated.
- **Convergence is a line chart:**
  - x = iteration, y = value;
  - one line per node, labelled at its end.
- **Containers:**
  - author at final size: col 537 bp, full 1080 bp;
  - height cap 380 bp (400 with `fig tall`);
  - discs land 26–52 px on the slide.
- **Assertions:**
  - every quoted number is asserted against the data;
  - frame 00 equals the previous slide's figure, checked with numpy `array_equal`;
  - a group shares one pixel size.
- **TikZ traps:**
  - `random steps` combined with `rounded corners` dies with "Dimension too large" on
    rectangles and short paths.
  - Use `pencil` (no rounded corners) for boxes and lines, and `pencilround` only for
    circles.
  - Brush jitter is computed in Python.

## 5. Theme

`house/theme-house.css` (`theme: house`) is the m06 theme. Over the bundled `theme.css` it
adds:
- **Text:**
  - MesloLGS NF body text (Menlo fallback);
  - Libre Baskerville headings;
  - ink `#30323D` everywhere.
- **Key terms:** `strong` is hot with a brush underline from `figures/brush-hot.png`, built
  by `house/figs_ui.py` into the deck's figures directory; `strong.cool` uses
  `brush-cool.png`.
- **Other elements:**
  - an ink part band;
  - a brush rule on the title slide;
  - figcaptions in Meslo, muted, 24 px;
  - the photo row;
  - the animation-stage port, whose tokens come from the palette.
- **Live stages** (the lecture-note anim kit): load `house/stage-pencil.js` on the title
  slide. It injects the `#m06-pencil` SVG filter that the stage CSS applies to discs.

## 6. Order of work for a deck in this style

1. Write `review/DECK_SPEC.md`:
   - every slide (title, left bullets, right figure, and what changes from the previous
     slide);
   - the **figure groups**, i.e. which figures share one canvas and box, and which frame 00
     equals which slide.
2. Put every graph, layout and quoted number in one `smallgraphs.py`, with `check()`
   asserting the quiz tricks.
3. Dispatch figure authors per module with this guide and the figlib API. Never two on one
   file.
4. Write the deck, then run `house/split_builds.py`.
5. Full clean rebuild, render with `marp --html --no-stdin --images png`, then gate
   (`check_render.py`, `check_deck.py`).
6. Review in three parallel slide ranges against the checklist below. Write
   `FIXES_Rn.md`, fix, rebuild, re-gate, commit.

## 7. House review checklist (in addition to SLIDE_RUBRIC)

- [ ] Do consecutive slides on one drawing keep it at the same position and size? Does each
      add only one thing?
- [ ] Is the figure on the right and the bullets on the left, except for the full-width
      exceptions?
- [ ] Is every question one graph, Q1 A1 Q2 A2, with Q/A sharing title, text and crop?
- [ ] Is every build a run of slides? Does each step have a callout, with 3–5 steps and no
      slider or GIF?
- [ ] Is every highlighted path named?
- [ ] Is every value directly above or below its own disc, not on an edge?
- [ ] Is only the point saturated, with no pure black? Does each colour keep one meaning
      across the run?
- [ ] Is the winner hot and underlined, showing the measure itself (higher is better where
      that is the definition)?
- [ ] Is there no fact the lecture does not use? Are bullets telegraphic, at most 4, at most
      2 lines each?
- [ ] Does the quiz trick hold, with the drawn-central node or the hub losing (asserted)?
- [ ] Is every number a reader might add an amount, not a share? Does $A_{ij}$ always read
      "$i$ → $j$"?
- [ ] Does each callout show a concrete case rather than a claim about "every" case?
- [ ] Does the example make the effect visible (e.g. disjoint routes for a 1/2 split)?

## Files (`house/`)

    figlib.py          the TikZ → xelatex → PNG pipeline with the house drawing API:
                       disc, seg, brush, underline, callout, shade, mark, grain, the
                       label solver, emit / emit_group / emit_frames with a shared box
    figs_ui.py         builds brush-hot.png and brush-cool.png for the theme
    theme-house.css    the Marp theme (`theme: house`)
    stage-pencil.js    the SVG pencil filter for live stages; it also contains the
                       (retired) slider, which stays inert unless a `.scrub` remains
    split_builds.py    expands each `fig scrub` build into a run of slides

Copy `figlib.py` and `figs_ui.py` into a deck's `figures/`. Copy `theme-house.css` next to
the deck, or point marp at it.
