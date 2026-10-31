# House style — how Sadamori's lecture decks look, read and move

Every rule below comes from his own review of a deck. It was settled on the Module 06
centrality deck (adv-net-sci `slides/m06/`), rebuilt three times in October 2026; that deck
is the worked example. He signed off on the result: 「色使い、スライドのつなぎ方、構成図、
テキストの構成や文字量など、すべて良くなった」. Build every new deck this way, lecture or talk.
The reference implementation is bundled in `house/`; see "Files" at the end.

This guide takes precedence over the older defaults in `DECK_BUILD_GUIDE.md` and
`FIGURE_GUIDE.md` where they disagree. Examples: the old palette (#3959A6 / #B14434, black
ink), Caveat captions, GIFs, and two-graph questions are all replaced here.

**Second reference, 2026-10-14: his own CompleNet 2026 talk** (`~/Downloads/complenet-2026.pdf`,
130 slides, Keynote; a sheet of 20 typical pages is `house/reference/complenet-2026-patterns.jpg`).
He asked to align the skill with it in text amount, slide designs and when each is used, text
structure and position, annotations, and colour use, and to keep this guide's palette ("I like the
current colour usage"). Section 9 is that deck read as rules; sections 2, 4, 5 and 8 were changed to
match it. Where the m06 rules and section 9 disagree on type, layout or annotation, section 9 wins;
on colour, section 3 stands (fonts: section 5).
He approved the four changes this made to the m06 style (2026-10-14): Meslo bold centred titles in
place of Libre Baskerville; handwriting back, for asides only (captions stay Meslo); the part
opener as the paper (title, authors, faces) instead of the dark band; one emoji at most per
slide, as a reaction. Section 10 reads the same deck for how the story decides the design.

**Update 2026-10-17: the look is the CCS 2027 deck's (the lecturer: "the CCS one is correct and the latest").**
`house/theme-house.css` is now that deck's `theme.css` (`~/Documents/projects/talks-ccs-2027-disruption/`). Where this
guide still names the old look (Meslo type, ink `#30323D`, orange hot, sky-blue cool, breadcrumb, Excalifont), the lines below win:

- **Type:** Libre Baskerville for titles, body, labels and captions (bold titles, centred); **Caveat** for handwriting
  (asides, labels in drawings); Meslo and Excalifont are retired in slides. `figlib.py` (TikZ) still sets its labels in
  Meslo / Excalifont: use it only for figures that need LaTeX, or switch its fonts first; the CCS deck draws its
  figures as HTML boxes and SVG (`mm.py`) so that the slide and the figure share one typeface.
- **Colour:** ink **black `#000000`**; muted `#6B6B6B`; pale / faint `#D9D9D9` / `#EEEEEE`; **hot = brick red
  `#B14434`**; **cool = blue `#3959A6`**; light blue `#8FA3D6` (teal) and light red `#D98A7C` (olive) for a third and
  fourth category; deep blue `#22336B` for outlines. There is no orange and no gold any more; a route is red.
  Everything else of section 3 (saturation carries importance, one meaning per colour, the winner) stands.
- **No breadcrumb line at the top.** Do not use `<!-- header: ... -->`; the title is the topmost thing. Section 9.2's
  breadcrumb is retired.
- **The paper reference is a footer bar:** a black bar, 26 px high, white 13.5 px Baskerville, one line, at the foot of
  every slide of the part that reports that paper. Set it in the front matter (`footer: "Authors. Title. Venue Year."`)
  or per part with `<!-- footer: "..." -->`, and clear it on the title slide and openers with `<!-- _footer: "" -->`.
  Someone else's work is cited in this bar too; a photo credit stays small in `.ref` above it.
- **Emphasis:** `**term**` and the coloured word of a title are red with the brush underline; `<span class="hot">` is red
  without it; `<span class="cool">` is blue. Bullets are round blue dots (not `>` chevrons). Lists are 40-44 px.
- **Faces and logos:** the part opener's faces are 250 px (`faces big`), logos at the bottom left (`logos2`).
- **Pencil nodes and grain** as before (`.o.dc`, `.o.gr`, `figures/grain.png`); copy `grain.png`, `brush-hot.png`
  and `brush-cool.png` from the CCS deck's `figures/` (they are the reference files).

**Update 2026-10-31 (wording; the lecturer's instruction, to be checked in every review):** write plainly, directly and
briefly, with no ornament. 「もっと端的に、シンプルに、直接的かつ簡潔に、飾らずに」 (about the M07 wireframe: "One walk, three worlds" is not
needed). A title says the claim or the question literally and names things by their technical term: no thematic titles
("One walk, three worlds", "Two rooms, one door"), no verbs of life or war for mathematical objects ("dies", "survives",
"forgets", "sets the clock"), no metaphorical nouns ("rooms" for communities), no commands ("Measure it"). The rule is N9 in
`SLIDE_RUBRIC.md`; it applies from the first wireframe; `gatelib` lists likely hits. Replace such a title with the plain
statement of what the figure shows ("Random walks appear in many fields").

**Update 2026-10-19 (the lecturer's red pen on the IPE seminar talk; these hold for every talk deck):**

- **The last slide is never "Thank you"** (his words: 「最悪」). It is the CCS 2027 deck's closing slide (`house/closing-slide.md`,
  rebuilt in `~/Documents/projects/talk-ipe-honkong-2027/review/make_wireframe.py`, the `END` block): at the top left the talk's title
  (bold, 46 px) and the venue and date (32 px); under it **one QR code per paper the talk reports** (165 px, black on white, made with
  `qrcode`, e.g. `figures/make_qr.py`) beside a bold lead (`Read the paper` / `Read the preprint`, 36 px) and two grey 23-26 px lines
  (the title in italics, the venue or `arXiv:ID`); at the bottom left the **contact block** exactly as in CCS (avatar 102 px, then
  `Web: <u>skojaku.github.io</u>`, the butterfly icon and `@skojaku.bsky.social`, `<u>skojaku@binghamton.edu</u>`, 36 px, black);
  at the right a picture from the talk (the map, the poster, a key figure) with a small italic caption; and the **footer bar with
  the paper reference** as on the CCS slide. Copy `avatar.jpg` and `butterfly.png` from the CCS deck's `assets/`. Get the URL of
  each paper from the lecturer; never guess a DOI. Use the lecturer's own lines of contact, not a thank-you sentence.
- **Figures as large as the slide allows** (「図はなるべく大きく。まだスライドに余白がある」). Do not cap a figure with a small
  inline `max-height`: leave the size to the layout CSS and raise its caps to what fits (the slide is 1280 x 720; the title, the
  take and the 26 px footer take the rest: about 560 px of figure under a B title, 640 px on G, 470 px on A, 450-480 px when a
  `.take` follows). **Trim the white margins of every placed figure** (`figures/trim.py` in the IPE deck) so that none of the
  allowed area is spent on blank pixels. When a figure needs more room, drop the subtitle or the take under it (move the sentence
  to the speaker note or into the title) before shrinking the figure. A wide figure (aspect over 2.5) is limited by width: crop it
  to the panels that carry the point, or build it in steps, rather than leaving a thin strip. Check every figure slide in a render.
- **Logos and faces.** The **title slide carries the speaker's school logo** (Binghamton: `logo_binghamton.png` in the CCS deck's
  `assets/`, bottom left, `logos2`) and the speaker's face (`face_sadamori.jpg`, `faces big`); add the host's logo when he supplies
  it. **Every part opener carries the photos of the co-authors of that part's paper, as many as can be had**: the old CompleNet /
  CCS decks hold them (crop them from `~/Downloads/OldDownloads/complenet-2026.pdf` page 52 or take `face_*.jpg` from the CCS
  `assets/`). Six faces: `faces` with `img` height 165 px (`faces big` overflows beyond four). Where no photo is on the machine,
  leave a dashed box with the name under it and tell him; **do not fetch photos of people from the web.** Read the author list from
  the paper's source (`\author`) rather than guess it.
- **Wireframe review sheets:** for the red-pen round give him the slides as contact sheets, 4 columns x 3 rows on a landscape A4
  page and 2 columns x 4 rows on a portrait page (`review/make_sheets.py` in the IPE deck), each slide numbered and captioned
  with its role; he marks them on a tablet.
- **Tooling:** `marp` needs `--html` (otherwise every inline `style=` is dropped), `--no-stdin < /dev/null` when it runs in the
  background (it waits for stdin otherwise and hangs), and an output path inside the working directory.

**Update 2026-10-21 (the IPE seminar talk, signed off: 「背景や色使い、文字の大きさ、添削と修正、図の作り方、アニメーションの作り方もすべて良かった」).**
The process and techniques are in `TALK_PLAYBOOK.md`; the look changes below hold for every deck.

- **Background:** the real washi paper scan, `house/washi-scan.jpg`, on cream `#FDFBF7` (now in `theme-house.css`; copy the
  scan to the deck's `figures/`). Figures multiply into the paper; photos, faces and the dark full-bleed `L-d` slides do not,
  and `L-d` has no paper. Pure white `#ffffff` is retired as a slide colour.
- **Hand-drawn concept figures** are inline SVG with the `rough` wobble-and-grain filter (`house/sketch_kit.py`), Caveat labels,
  the palette tokens, red on the object of the slide and grey on the rest.
- **Real figures get grey ring call-outs** (ring, one to three Caveat lines, an arrow; `sketch_kit.callout` / `OVL`), red only
  for the slide's own claim. No frames or separator lines around panels and GIFs.
- **Builds are consecutive slides** with the hidden parts kept in place (`visibility: hidden`), not fragments: the text-only
  question slides, the Apoha exclusion, the summary (one claim per slide), the circle's second line.
- **Motion:** GIF for drifting dots, mp4 + poster for screen recordings (slide background = the video's own colour, sampled),
  transparent WebM when a sketch and a web page move together; export `deck.html` every round.
- **Wireframe first for a talk,** with dashed boxes saying what goes in them; the deck is generated from one Python slide list.

**Two kinds of deck.** A *lecture* (a course module, 90 minutes, with questions to the class and
often a worksheet) and a *talk* (a conference or seminar talk on his research; CompleNet 2026 was
70 minutes). Everything here applies to both, except where a rule says "lectures" or "talks": the
story shape of a lecture is section 1 plus SLIDE_RUBRIC S1-S6; the story shape of a talk is section 10.

---

## 1. Slide flow: small differences

**The principle, in his words:** the cognitive cost of a slide change grows like n², where n
is the amount of new information. Consecutive slides must differ by little. Split
information rather than delivering it at once.

**Base layout** (superseded twice: on 2026-10-13 by the six layouts, on 2026-10-14 by the CompleNet
reading of section 9). The default is now layout B, a title over a big figure; bullets beside a
figure (plain `cols`, the old base layout) is for the few slides whose text must be read to
understand the figure. Section 8 says which slide takes which layout.

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
- Q and A share the title and the text; A adds one line.
- Q and A share the crop: A is Q plus the values and the winner's mark. figlib asserts that
  the answer's TikZ starts with the question's.

**Builds are separate slides. No slider, no GIF, no autoplay.**
- A build is a run of slides with the same title (or, on G, none) and the same figure position:
  - Slide 0 shows frame 00, pixel-identical to the previous slide's figure. If the slide has
    bullets (C), he explains them first: they are fragments on slide 0.
  - Each following slide shows the next frame; bullets, if any, are all visible (`-`).
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
- Lectures: one minute per content slide, at most about 45 content slides per 90-minute
  session. Build-step slides are extra and take seconds each. Say so in the title slide's notes.
- Talks: plan minutes per part, not per slide (section 10.1). CompleNet: 130 slides in 70
  minutes, most of them build steps and pictures that take seconds.

**Story shape per module (lectures; talks follow section 10).**
- **Opener:** a concrete, memorable story, carrying only the facts the lecture uses.
- **A real local network:** for Binghamton students, the NY State highways. The map large
  (layout B), the point in its title. It returns after every measure.
- **Per concept:** concept → formula → a one-graph question → answer → the same measure on
  the real network.
- **Questions must be a little tricky.** The node that looks central (the hub, or the node
  drawn in the middle of the picture) must not win, or two candidates must need computing.
  Draw the loser at the centre of the picture, and assert it in code (see
  `smallgraphs.check()` in m06).
- **Close a part** with a figure that classifies everything so far (m06: the two-axes grid).

## 2. Text: little, plain, and pointing at the figure

- **Wording first (N9).** Literal, direct and short, no figure of speech, in every title, sub, take, cue, label and bullet.
  A title is never a theme, a metaphor or a command. See the update of 2026-10-31 at the top.
- **Amount (his rule of 2026-10-13, which replaces "two to four bullets"):**
  - **At most three bullets on any slide, never four.** Most slides have none: the title is the message and the figure explains.
  - **The text is a rescue for someone who missed the talk, not something to read during it.** The figure carries the explanation;
    a slide a listener has to read has failed. When a term needs a definition, put it in one short sentence (layout A's `.sub`) or in the figure's label; two or three terms defined beside one figure take plain `cols` (section 8, C).
  - Each bullet is one idea of at most eight words, telegraphic.
  - At MesloLGS NF 30 px a 537 px column holds about 29 characters per line. Two lines per
    bullet is the most.
  - No sentences inside figures, only numbers and two- to five-word labels. The one exception
    is an aside (section 9.3): at most about eight handwritten words the slide can lose.
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
  - The question is the slide title (or C's text, beside its picture).
  - One line of instruction at most: the `.sub`, or C's text.
  - A near-white cue (`<div class="cue">`, e.g. *Take a minute.*) goes at the bottom.
  - A question slide never shows its answer.
- **Notes:** speaker notes carry the sources, the exact numbers, and what to ask the room.
- **No paragraph after a fragmented list.**

## 3. Colour: saturation carries importance

| token | hex | use |
|---|---|---|
| ink | `#000000` | text, node outlines, edges |
| muted | `#6B6B6B` | what is not the point: context labels, axis titles, callouts, removed edges |
| pale / faint | `#D9D9D9` / `#EEEEEE` | de-emphasised fills; the low end of a value scale |
| hot | `#B14434` | **the point of the slide**: the winner, the answer, the key term (brick red) |
| cool | `#3959A6` | the second emphasis; high values on a value scale (blue) |
| light blue, light red | `#8FA3D6`, `#D98A7C` | third and fourth categories, sparingly |
| deep | `#22336B` | outlines of boxes and tree nodes |

(2026-10-17: replaces the older orange / sky-blue / gold / teal / olive palette and "never pure black".)

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
  - His spoken comments on a figure are asides, not callouts: `F.aside(text, at, target)`,
    handwritten (section 9, "Annotations").
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
  - authoring height cap 380 bp (400 with `fig tall`); how large each layout then shows it is
    in section 8;
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

`house/theme-house.css` (`theme: house`) is the m06 theme, aligned with CompleNet on
2026-10-14. It replaces the bundled `theme.css` (the older "network-science" theme, kept only for
decks already built with it). It sets:
- **Text** (2026-10-14, from CompleNet):
  - MesloLGS NF everywhere (Menlo fallback): titles bold, centred, 44 px; F statements 62 px;
    body 30–36 px;
  - Libre Baskerville only for quotations (layout Q);
  - Excalifont (`.aside`, `figlib.aside`) for handwritten asides; install it from Excalidraw,
    or the theme falls back to Caveat and figlib to a slanted Meslo;
  - ink `#30323D` everywhere;
  - no rule under titles: `<hr>` after a title is now an invisible spacer, kept so old decks
    render unchanged.
- **Small fixed pieces** (section 9): `header` breadcrumb, `.sub`, `.take`, `.ref`, `.paper`,
  `.thumb`, `.past`, `.aside`, `.hot`/`.cool`/… word colours, `.fig.photo` shadow.
- **Key terms:** `strong` is hot with a brush underline from `figures/brush-hot.png`, built
  by `house/figs_ui.py` into the deck's figures directory; `strong.cool` uses
  `brush-cool.png`.
- **Other elements:**
  - the title slide and the part opener (section 8);
  - figcaptions and credits in Meslo, muted, 24 px (a credit is the one text allowed under the
    type floor);
  - the photo row;
  - the animation-stage port, whose tokens come from the palette.
- **Live stages** (the lecture-note anim kit): load `house/stage-pencil.js` on the title
  slide. It injects the `#m06-pencil` SVG filter that the stage CSS applies to discs.

## 6. Order of work for a deck in this style

0. Write the story first (section 10.6): the spine of F sentences, the arc of each part, the
   motif table, the beat of every slide.
1. Write `review/DECK_SPEC.md`:
   - every slide: its beat (section 10.2), layout, title, text, figure, and what changes
     from the previous slide;
   - the **figure groups**, i.e. which figures share one canvas and box, and which frame 00
     equals which slide.
2. Put every graph, layout and quoted number in one `smallgraphs.py`, with `check()`
   asserting the quiz tricks.
3. Dispatch figure authors per module with this guide and the figlib API. Never two on one
   file.
4. Write the deck, then run `house/split_builds.py`.
5. Full clean rebuild, render with `marp --html --no-stdin --images png`, then gate
   (`check_render.py`, `check_deck.py`).
6. Review against the checklist below: changed slides by the lead each round (Tier 1), the
   whole deck in three parallel slide ranges once before shipping (Tier 2, REVIEW_PLAYBOOK).
   Write `FIXES_Rn.md`, fix, rebuild, re-gate, commit.

## 7. House review checklist (in addition to SLIDE_RUBRIC)

The one checklist for this style; sections 9 and 10 explain the items they come from.

**Story** (section 10)
- [ ] Do the F slides, read alone, give the talk's abstract (the spine test)?
- [ ] Does each part run its arc (talks: question, known, mystery, pivot, new view, test, result; lectures:
      section 1's story shape and SLIDE_RUBRIC S1-S6)?
- [ ] Does each slide take the layout its beat calls for (sections 8 and 10.2), with B and G the most common?
      Do more than three consecutive slides share a layout outside a build or a narrated run of pictures?
- [ ] Does every concept keep one picture and one colour, and does its picture return when it returns?
- [ ] Is every question answered on its own figure, and does the last slide answer the first picture?
- [ ] Is the last slide the CCS-style closing (QR code per paper, contact block, paper footer), not "Thank you"? Are the figures as large as the layout allows, with trimmed margins? Does the title slide carry the school logo, and each part opener its co-authors' photos?

**Slide flow** (section 1)
- [ ] Do consecutive slides on one drawing keep it at the same position and size? Does each add only one thing?
- [ ] Is every question one graph, Q1 A1 Q2 A2, with Q/A sharing title, text and crop?
- [ ] Is every build a run of slides? Does each step have a callout, with 3-5 steps and no slider or GIF?

**Text** (sections 2 and 9)
- [ ] Is every title, sub, take, cue and label literal (N9)? No thematic title, no "dies / forgets / sets the clock", no metaphorical noun, no command?
- [ ] Is there no fact the deck does not use? Is there no text beyond the title on about half the slides, at most
      one line (`.sub` or `.take`) on most others, and never more than three bullets?
- [ ] Is the vertical order breadcrumb, title, sub, figure, take, footer, with nothing out of order?
- [ ] Is every B title one line (at most 40 characters), with at most one coloured keyword?
- [ ] Is every number a reader might add an amount, not a share? Does $A_{ij}$ always read "$i$ → $j$"?

**Figures and annotation** (sections 4 and 9.3)
- [ ] Is every highlighted path named? Is every value directly above or below its own disc, not on an edge?
- [ ] Are labels at their things in Meslo, asides handwritten and dispensable, named equation terms in their colours?
- [ ] Does each callout show a concrete case rather than a claim about "every" case? Does the example make the
      effect visible (e.g. disjoint routes for a 1/2 split)?
- [ ] Is the previous step faded (`.past`), not deleted, when the next step builds on it?
- [ ] Lectures with quizzes: does the quiz trick hold, with the drawn-central node or the hub losing (asserted)?

**Colour and pictures** (sections 3 and 9.4)
- [ ] Is only the point saturated, with no pure black? Does each colour keep one meaning across the run, and every
      contrast its two colours across the talk?
- [ ] Is the winner hot and underlined, showing the measure itself (higher is better where that is the definition)?
- [ ] Does every photo slide use D, E, Q or C, with a credit? Do photographs on white carry the shadow; are
      portraits beside quotations black and white?

## 8. Slide layouts: one deck, not one layout

The lecturer's sketch (2026-10-13): "the design of the slides is monotonous; decide the layouts." On 2026-10-14
the set was aligned with his CompleNet 2026 deck: B became the default, G (figure alone) and Q (quotation) were
added, C became "text beside a picture" rather than "bullets beside a figure". Every slide takes one layout, and the
layout follows from what the slide has to do. CSS is in `house/theme-house.css` (the block "Slide layouts"),
markup for each in `house/layouts.md`.

| layout | class | what is on the slide | use it when | share in CompleNet |
|---|---|---|---|---|
| **B** | `L-b` | the title (the message) over a big figure | the default: the figure carries the point and the title says it; a plot, a diagram with callouts, the first step of a build | about 30% |
| **G** | `L-g` | the figure alone, no title | the later steps of a build whose drawing labels itself; a row of objects or an illustration he narrates; whenever a title would only repeat the previous slide's | about 20% |
| **A** | `L-a` | title, one line under it (`.sub`), figure, the conclusion under it (`.take`) | the figure needs a question or context above it, or its result stated in one bold line below it | about 12% |
| **F** | `L-f` | one statement, large and centred; at most two lines or one small picture under it | a part's question, a thesis, a turning point, "Summary"; `.num` ("#1", "#2") beside a claim that recurs | about 12% |
| **C** | `L-c` | a question, a term or at most three items, large, beside a picture (either side) | the text must be read with the picture: a question with options A and B, a term and its picture, a short headed list. Plain `cols` (bullets left, figure right) stays for definitions whose words the figure cannot show | about 10% |
| **E** | `L-e` | a short paragraph beside a photo | a photograph that needs two or three sentences of explanation | rare |
| **Q** | `L-q`, `L-q center` | a quotation in Baskerville, the phrase that matters in hot, the source muted under it; the speaker's portrait (black and white) on the right, or none and centred in italics | a quotation; a run of quotations from one person keeps the portrait and changes the words | about 4% |
| **D** | `L-d`, `L-d field` | a photograph full bleed with a box for the words; or a colour field with the title in white and the figure on a white card | a photograph or a collage that deserves the slide; a result shown per category when the categories have colours (Law / Science / Patents) | about 8% |
| title, part | `lead`, `part` | the title slide (title left in bold; venue, date, name; logos; QR); a part opener: the paper the part is about (title, authors, faces) or the part's question | the first slide; the start of each part | - |

The rules that made it work:

- **The layout belongs to a build, not to a step.** All steps of one build use the same layout, so the figure keeps its
  position. `house/split_builds.py` keeps the `_class` directive in every step (it used to strip it with the speaker notes).
  The exception CompleNet makes: a build may start on B and continue on G once the drawing labels itself, if the
  figure keeps its pixel position (give both the same container and crop).
- **The message is the title, set as on every other slide: no frame, no tinted box, no colour around it** (the lecturer,
  2026-10-13: "do not draw a box around the title; keep it minimal, title as title"). One keyword inside it may be
  coloured (section 9.4). There is no visible rule under a title any more; F centres its title.
- **A B title is one line: at most 40 characters** at 44 px (the generator should assert it). A two-line title takes
  50 px from the figure. What the short title drops goes into a speaker note, the `.sub` (then the slide is A) or the `.take`.
- **B moves the text into the title and the figure's labels.** When a line of text carries content the figure does not
  show (a definition, a number, the conclusion), add it as `.sub` or `.take` (layout A); when the text must be read with
  the picture, use C.
- **D, E, Q and C carry the pictures.** Photographs (history, people, a screenshot, a generated illustration) go in D, E,
  Q or in a C whose text is about them, never as a small thumbnail beside bullets. On white they carry a soft shadow
  (`.fig.photo`, `.shot`); drawings never do. Every one has its credit in the box (D), the caption (E, A), the `.who` (Q)
  or the sources slide. An image generated by a model says so in its credit.
- **F replaces a figure that only repeats words.** A framed quotation drawn as a figure became Q; a claim drawn as text in a
  figure becomes F.
- **A question slide is A, C or F, and never shows its answer.** The answer to one question is the same slide with
  the answer added: same layout, same figure, the answer as the `.take` or in place of the question. The results of
  several questions asked in a row (the room's A-or-B tests) get their own slide: a "Results" breadcrumb, the claim
  in bold with its keyword coloured, one muted line explaining it, thumbnails of the questions under it.
- **Never more than three slides in a row in one layout** unless they are the steps of one build or one narrated run
  of pictures (the hook's maps, the technology collage), which counts as a build.

Figures authored for the 537 px column are shown larger in A, B and G (up to 480 bp high in B, 600 in G). The gate compares
the container a figure is used in with the one it was authored for and fails the slide with "renders at 201% of its
intended scale". The enlargement is intended (type only gets bigger, the PNG is 4x), so put the figure in a single-child
`<div class="cols">` wrapper (CSS: `section.L-a .cols, section.L-b .cols, section.L-g .cols, section.L-d.field .cols` is a
centred flex box); the gate counts it as a column figure. Do not add `solo` or another class to that div: the gate looks
for the exact string `class="cols"`.

**The second rule of 2026-10-13: figure first, readable from the back row.**
- Explain with the figure; text only rescues. Prefer B and G to C: a figure authored for the 537 px column grows at most
  1.2 times in B, so draw the important ones (the lecturer: "the Snakemake figures are important") at full width
  (`container="full"`, `hmod="tall"`, up to 400 bp) and put them in A, B or G without the `cols` wrapper. The Snakemake
  build is the model: `snakefile-dag` (rule cards on the left, the graph that follows on the right, one hot arrow between
  them), then the rerun frames.
- A figure on a page with a caption (credit) may be at most 450 px high (B). An A slide with both a `.sub` and a `.take`
  takes `<div class="fig tight">` (320 px).
- **Keep the pictures the lecturer chose; they are part of the story, not decoration.** Never replace one with a drawing of
  your own. Before dropping or replacing a picture from an earlier deck (a character, a meme, a still
  from a film or a clip, a comic whose text he changed, logos, a QR code), look at what the old deck used (its imports, its last preview
  images) and carry each one over, with its credit. A GIF or a clip becomes a still. A QR code is decoded first (`opencv-python-headless`
  in a temporary venv: `cv2.QRCodeDetector().detectAndDecode`) and its target stated.
- The gate's hygiene step lists running processes that look like renderers: do not run `marp` in the same shell command line as `gatelib review`.

Known false positives of the gate: it reports "content runs to y=719" on every full-bleed slide (D, D field, and slides
with a full background colour), because ink reaches the last row. Check them by eye and leave them. Slides with a footer
element (`.ref`, `.paper`, `.logos`, `.qr`) are checked against the frame (y = 712), not the content box, because
that is where those elements belong; check by eye that the footer does not touch the figure.

## 9. The CompleNet 2026 deck, read as rules (2026-10-14)

What his own 130-slide talk does, in the terms of this skill. Look at `house/reference/complenet-2026-patterns.jpg`
before building: one picture of these rules is faster than the list.

### 9.1 How much text

- **Lines of text beyond the title:** none on about half the slides (B, G, D, most F); one line, a `.sub` or a `.take`,
  on most of the rest. A list appears on 6 of 130 slides, with at most three top-level items, each with at most two
  sub-items. The "at most three bullets, most slides none" rule of section 2 holds, and is the norm, not the limit.
- **The words that do appear are mostly in the figure:** node names, axis titles, labels and asides. pdftotext finds a
  median of 16 words per page, nearly all of them labels and references.
- **Two kinds of slide may carry more:** a derivation (a chain of equations, each line led by one plain phrase such as
  "So we linearize it using Taylor expansion.") and the summary (three `>` claims, each with one or two sub-points and a
  thumbnail of its figure).
- **Sentences are short and plain:** "Cut. Then glue." "There are two kinds of glues." "Let's measure!" A sentence that
  needs a comma is usually two slides.

### 9.2 How text is structured and where it sits

- **Vertical order, top to bottom:** breadcrumb (optional) → title → `.sub` → figure → `.take` → footer (`.ref`,
  `.paper`). Every slide uses a subset of this order and never another order.
- **Everything is centred** on the slide's vertical axis, except a paragraph (E) and a quotation with a portrait (Q).
  The title aligns left only above a left-aligned list (class `left`).
- **The title is the message as a sentence** ("word2vec can embed networks", "Learn by metonymy but captures metaphor.",
  "It's a growth model") **or, inside a long build, the topic** ("Perception bias", "Disruption index (Funk and
  Owen-Smith 2017)", "What's happening?"). A topic title in a long build may be set muted (`<span class="muted">`) so
  that the figure leads.
- **`.sub`** is the question, the context or the method in one line, in regular weight under the title ("How many
  colors in rainbow?", "without explicitly modeling aging"); `.sub muted` (italic, muted) for a method note ("Preserve
  degrees and time gap. Shuffle everything else.").
- **`.take`** is the conclusion in one bold line under the figure, its keyword coloured ("word2vec is a matrix
  factorization", "We preserve continuity by abandoning class rounding.").
- **Lists** use `>` chevrons in cool (the theme draws them). When items have sub-items, the top level is the claim in
  bold and the sub-items are the evidence in regular weight.
- **Text beside a picture (C)** is set large (36 px), centred in its column and level with the picture's middle; the
  picture may be on either side. A question with options writes them as lines: "A: Monkey and Pandas", "B: Monkey and
  Banana".
- **The breadcrumb (RETIRED 2026-10-17: do not use it)** (`<!-- header: Results -->`): a short line from the left edge, a dot, and a muted label naming
  the run's topic or source ("Results", "DeepWalk (Perozzi et al. 2014)", "How good is word2vec in community
  detection?"). Set it on the first slide of a run; Marp repeats it until `<!-- header: "" -->`. The theme hides it on
  `lead` and `L-d`.

### 9.3 Annotations

- **A label says what a thing is** and sits at it: Meslo, muted or in the thing's colour ("query vector", "random walk",
  "level of mixing", "average degree"). Where it cannot sit at it, a thin straight arrow. `F.text`, `F.callout`.
- **An aside says what he would say about it:** handwritten (Excalifont), muted, at most about eight words, with a thin
  curved arrow: "No analytical solution in general.", "Bayes optimal", "true for near-detectability threshold",
  "Milestone papers with the bottom-level D-index value". `F.aside(text, at, target)` in a figure; `.aside` on the
  page. An aside never carries a fact the slide needs; delete it and the slide still says its point.
- **Equation anatomy:** a term that matters gets a thin line in its colour under it (or over it, to keep neighbouring
  names apart) and its name in one to three words in the same colour: $\Pi_i(t)$ "Probability of a new citation",
  $\eta_i$ "Fitness", $c_i^t$ "Citation (PA)" (above), $P_i(t)$ "Aging". `F.eq_terms(x, y, parts)`. When the same
  equation returns, its terms keep their colours and names; a new term in the extended model gets a new colour
  ("Distance" in teal).
- **A value on a picture:** the number in hot (or in its series' colour), large, with an arrow to the person, node or
  bar it belongs to ("Δ = 1.002, Top 4.3 %"; "D = −0.27, Bottom 0.1 %" in the losing colour).
- **The past stays, faded.** When a step builds on the previous one, the previous content stays where it was at 30%
  (`.past`; in a figure, draw it `pale`) and the new part is at full ink: the old equation over the new one, the rows
  of a table already discussed, the word "prepared" once "favors" is the point.
- **A reminder of the subject:** a small picture of it in the top right corner (`.thumb`) when the talk returns to it
  after a digression (the Higgs photograph on "What's happening?").
- **A recap:** the summary pairs each claim with a thumbnail of the figure that showed it; a slide that resumes an
  earlier result may show that slide's figure small at the left.
- **References:** someone else's work as a full reference, 15 px, muted, bottom left (`.ref`); his own paper as
  "Kojaku et al. / Nat. Comm. 2023" with the venue's logo in a bottom or top corner (`.paper`, `.paper top`).
- **Emoji:** at most one on a slide, as a reaction that marks a turn of the story: 🤔 on a mystery or a test question,
  👉 before the results, 😎 on the winner. At the end of a line or beside a number; never inside a figure's labels,
  never in place of a word.

### 9.4 Colour use (the palette of section 3, applied the way CompleNet applies its own)

- **Titles are ink; one keyword in a title may be hot:** the concept the slide introduces ("**Culture** sets
  boundaries", "How do we humans accumulate **knowledge**?", "There are **two** kinds of glues", the last in italics as
  well). Write it `<span class="hot">…</span>`; `**term**` (hot with the brush underline) stays for a term where it is
  defined.
- **A contrast takes hot and cool, and keeps them for the whole talk:** query hot / key cool in every network drawing,
  table, matrix and equation; metaphorical hot / metonymical cool from the question slides to the summary. A third and
  fourth category take teal or olive, the same way (gold is for routes and fills, never text: 2:1 contrast on white).
- **A statement that names categories colours each word as its category** ("Perception, Culture & Language").
- **Muted is for what frames the point:** the breadcrumb, a topic title in a long build, labels of context, asides,
  references, method notes, the faded past.
- **The `.take` is ink and bold, with its keyword hot.**
- **Photographs keep their colours;** a portrait beside a quotation is black and white. A colour field (`L-d field`)
  is the category's colour at full size, with the title in white and the figure on a white card.

## 10. Story and design: the layout follows the beat (CompleNet 2026, 2026-10-14)

Section 9 says what each design looks like; this section says why a slide gets it. In the CompleNet deck the
design of a slide is decided by its place in the story, so a reader who sees only the layouts can tell where the
talk is. Page numbers below are the PDF's.

### 10.1 The shape of the talk

    hook (3-14)        a sensory, everyday puzzle: beer / wine / vodka belts of Europe, many maps of them
    thesis (10)        one F statement that names the talk's idea and its parts
    theory (15-24)     why it happens: an old theory, reduced to two icons, tested on the room
    part 1 (25-49)     the method: what it is, why it works (derivation), how far it goes (the limit)
    part 2 (50-83)     one paper: human question -> facts -> the mystery -> a new view -> the test
    part 3 (85-123)    one paper: the same arc
    close (125-129)    summary with thumbnails, then the hook's picture answered

- **Every part runs the same arc:** a human-scale question (F) → what is known (B, D field) → where it fails, a
  mystery (B with a black takeaway band, then an F question) → a pivot (a quotation, Q) → the new view (G builds) →
  the test (an A whose `.sub` is the question) → the result (B or A with a `.take`).
- **Concrete, abstract, concrete.** Each part opens and ends on things a non-specialist can see (maps, a clay tablet,
  a light bulb, phones; the Higgs photograph, sleeping papers "awake in 1994") and keeps the equations in the
  middle. Photographs live at the two ends; drawings and equations in the middle; a photograph in the middle
  appears only as a small anchor (`.thumb`).
- **One paper is one part.** Its opener names the paper (title, authors, faces). No clock on the slide (the
  lecturer, 2026-10-14: not needed); the part's planned minutes go in the opener's speaker note.
- **Slides are not minutes.** The talk was 70 minutes for 130 slides. Its time marks put about ten minutes on the
  16-slide hook, 8 on slides 17-34 (the glue, the room's tests, word2vec's first claims), 11 on slides 35-49 (how
  word2vec works, the derivation), 15 on part 2 (32 slides) and 26 on part 3 (about 40 slides): the hook's pictures
  and the build steps take seconds, a derivation takes minutes. Plan time per part, not per slide.

### 10.2 The beat decides the layout

| story beat | design | why it fits |
|---|---|---|
| hook, an everyday example | G (pictures alone) or C (a short statement beside one picture) | nothing to read, so the room looks and guesses |
| the thesis, a part's question, a turning point | F | the talk stops; one sentence fills the screen |
| a claim that recurs | F with `.num` (#1, #2) | the numbers tell the room how many to expect |
| evidence, data | B, or D field when the categories have colours | the figure is the evidence; the title says what it shows |
| mechanism, how it works | G builds with labels and asides | the drawing grows one element at a time; text would race ahead of it |
| derivation | the dense exception: equation lines, each led by one plain phrase | allowed, but always ends on a bold `.take` |
| a question to the room | C with options "A: … B: …" | the options are the text; the pictures are the stimuli |
| the answer to a question | the question's slide with the answer added | the figure stays; only the answer is new |
| exploring a case | B with a muted topic title ("What's happening?") | muted says "we are still looking" |
| a pivot to a new view | Q, a quotation | someone else's voice turns the story |
| the result | B or A with a `.take` (bold, keyword hot) | the conclusion is the last thing read |
| a part's start | `part`: the paper, its authors, their faces | the room learns whose work this is |
| summary | `>` claims with thumbnails of their figures | each claim points back to the picture that proved it |
| the end | one statement and the hook's picture, now answered | closes the loop opened on slide 3 |

**The spine test.** Read only the F slides in order and you get the talk's abstract: "We hallucinate boundaries due
to Perception, Culture & Language." → "Why do we build boundaries?" → "Cut. Then glue." → "There are two kinds of
glues." → "Surprising effectiveness of word2vec #1 … #2" → "Revisit the community detection problem" → "How do we
humans accumulate knowledge?" → "Citation: knowledge is individualized and can be built on top of each other." →
"Aging and sleeping beauties require counteractive mechanisms. How can they be explained?" → "Does our model explain
the citation dynamics…?" → "How do the aging & delayed recognition coappear?" → "Summary". Write these sentences
first (section 10.6); if they do not read as a story, no layout will fix the deck.

### 10.3 Text tracks the story's state

- **Title weight is the story's state.** Bold ink: a claim. Muted, regular: a topic under investigation ("Disruption
  index (Funk and Owen-Smith 2017)", "What's happening?"), kept for the whole run. F: the story stops to ask or to
  turn. A reader can see from the title alone whether the slide claims, explores or asks.
- **The title holds while the claim holds.** In a build the title does not change; the figure grows under it (four
  "Disruption index" slides, three "What's happening?"). A new title means a new claim.
- **Questions are titles; answers are takeaways.** "How wide is the gap for word2vec + random walks?" sits beside the
  plot; the next slide replaces it with "word2vec + random walks achieve the theoretical limit." on the same plot.
  "Does this identify the disruptive work better than the D-index? 🤔" is answered, three slides later, by "Our EDM
  better aligns with human judgment than the D-index."
- **A mystery ends on a band.** Before a new view, the failure is stated in one line on a dark band under the
  evidence (`<p class="take dark">`: "Neither LTCM nor Preferential Attachment reproduces the sleeping beauty
  phenomenon 🤔").
- **Three typefaces are three voices.** Meslo is the speaker stating; Excalifont is the speaker thinking aloud ("This
  was normal", "Innovative 🤯!", "Tested 10y> ago by myself"); Baskerville is someone else (Adams, Barabási). The voice
  changes exactly where the story's speaker does.
- **Emoji mark the story's turns,** never content (section 9.3).

### 10.4 Pictures and colours are the story's threads

- **One concept, one picture, one colour, for the whole talk.** The concept's picture returns whenever the concept
  returns, so the connection is made without a sentence:
  - the two glue bottles (type A red, type B blue) introduce the two ways of grouping, return on the results of the
    room's test, and are the colours of metaphorical / metonymical from then on;
  - the Apoha sculptures (stone → carved horse → horse) explain "concepts by negation" in the theory and return on
    "Trained by negation." when word2vec's negative sampling appears;
  - the word2vec network icon opens part 1 and returns in part 3 when the method is reused;
  - the Higgs photograph is the test case of part 3: D = −0.27 on it (the old measure fails), the same photograph as a
    reminder while diagnosing, Δ = 1.002 on it (the new measure works);
  - Law / Science / Patents keep brown / navy / green on every fact and every reproduced plot of part 2;
  - query / key keep orange / blue through part 1, in the network drawing, the table, the vectors and the matrices;
  - the hook's map is the summary's thumbnail for "the illusion of boundaries", and the scissors of "Cut. Then glue."
    return on the last slide, cutting a continuous strand.
  Keep a motif table in the spec (section 10.6) and reuse the same file for the same concept.
- **Transitions move the old picture aside instead of announcing a section.** The quotation slides off to the left as
  the paper-centric model comes in; the last results shrink to thumbnails at the left as "word2vec is a simple neural
  net" starts; the community-detection plot comes back as a thumbnail under "Revisit the community detection
  problem". The room sees where it came from and where it goes.
- **The last step stays in sight, faded** (`.past`, section 9.3), so the new part reads as a continuation.

### 10.5 Rhythm

- **Light and heavy alternate.** A dense stretch (the derivation, 46-48) is followed by a light one (a bold takeaway,
  a statement, a picture). Never two dense slides without a take or an F after them.
- **Fast runs are allowed where the story is a sequence of pictures** (the hook, the room's test, the technology
  collage, a build); a fast run has no text to read, so speed costs nothing.
- **The room takes part early.** Three A-or-B tests ("Count your A's.") in the first quarter turn the theory into the
  room's own result; the results slide reuses the tests' pictures as thumbnails.

### 10.6 Order of work (adds to section 6)

Before the slide list of `review/DECK_SPEC.md`, write:
1. **The spine:** the F sentences in order (10.2, the spine test). Read them aloud; fix the story here.
2. **The arc of each part:** question → known → mystery → pivot → new view → test → result, one line each, with the
   paper or source behind the part and its planned minutes (in the opener's speaker note).
3. **The motif table:** concept → its picture → its colour → the slides where it returns. One file per picture.
4. **The beat of every slide,** then its layout from the table of 10.2. A layout chosen for variety, against its beat,
   is wrong; the "no more than three in a row" rule of section 8 is a check, not the reason for a choice.

## Files (`house/`)

    figlib.py          the TikZ → xelatex → PNG pipeline with the house drawing API:
                       disc, seg, brush, underline, callout, aside (handwritten),
                       eq_terms (named equation terms), shade, mark, grain, the
                       label solver, emit / emit_group / emit_frames with a shared box
    figs_ui.py         builds brush-hot.png and brush-cool.png for the theme
    theme-house.css    the Marp theme (`theme: house`)
    stage-pencil.js    the SVG pencil filter for live stages; it also contains the
                       (retired) slider, which stays inert unless a `.scrub` remains
    split_builds.py    expands each `fig scrub` build into a run of slides (keeps `_class`)
    layouts.md         markup of every layout and fixed piece (sections 8 and 9); render
                       it to see them all
    washi-scan.jpg     the paper background (copy to the deck's figures/); grain.png is the pencil grain
    sketch_kit.py      hand-drawn SVG layer: rough filter, svg/t/arrow, and the grey ring call-outs (ring, callout, OVL)
    ipe-seminar-2026/  snapshot of the IPE talk's generator, sketches, sheet maker, worker briefs and video/GIF scripts
                       (code only, assets not copied); the worked example for TALK_PLAYBOOK.md
    closing-slide.md   the closing slide of a talk (QR code per paper, contact block, paper footer); never "Thank you"
    reference/         complenet-2026-patterns.jpg: 20 typical pages of the lecturer's
                       CompleNet 2026 deck (section 9)

Set a deck up with the commands in `template/README.md`. The one trap: `theme-house.css` must sit next to the deck
**named `theme.css`**, because the gate (`gatelib`) renders with `<deck dir>/theme.css` only, and a deck whose theme it
does not find is rendered in the default blue theme without a warning (the first full gate run of the CCS talk deck did).
