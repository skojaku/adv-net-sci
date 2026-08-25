---
name: pen-and-paper
description: >-
  Write or revise a pen-and-paper exercise sheet (LaTeX worksheet) for a module
  of the network science course, in Sadamori's discovery-first house style —
  students work the sheet IN CLASS, before the concept is named, and reconstruct
  it with their own hands. Use when asked to create, extend, review, or fix a
  pen-and-paper / worksheet / exercise sheet for any module m00-m09.
---

# Pen-and-paper exercise sheets

A pen-and-paper sheet is **not** a practice problem set, and it is **not
homework**. It is handed out in class and worked there, in the half hour before
the concept has a name. The sheet's job is to walk the room into the concept by
hand, so that the rest of the session only has to give a name to something they
have already built, and can start from what they actually found.

Two consequences for how a sheet is written. It has to be finishable in the
time the room has, by someone with no preparation — nobody has read ahead. And
its questions are discussed out loud a few minutes after they are answered, so
a question whose answers differ between neighbours is a feature: that
disagreement is the material the session is built on.

If the student could answer a question by recalling a definition, the question
is wrong. Every question must be answerable with a pencil, a small drawing, and
counting.

## Who it is written for

Sadamori's instruction, in his words: write it so that somebody **with no
background knowledge — assume high-school students — and who is not a native
English speaker** can understand it. That is the standard every sentence is
measured against, and it is the reason for most of the rules below: short
sentences, one ask per line, no clause the student has to hold in their head
while they read the next one. **Condense.** A question that needs a second
reading has already spent the minutes it had.

`lecture-note/m01-euler_tour/pen-and-paper/` and `m02-small-world/pen-and-paper/`
are the two sheets written to this standard and iterated on with Sadamori until
he was happy. Read them before anything else. `m03`-`m09` are the older shape —
they still hold good scenarios, but their form (blanks, ruled answer gaps,
titles, 12pt) is what m01 and m02 were rewritten *out of*.

## Before writing

1. Read `curriculum.yml` (repo root) for the target module: `big_question`,
   `hook`, `objectives`, and the full `concepts` list with IDs.
2. Read at least two existing sheets end to end to re-anchor the voice — m01 and
   m02 for the current form; `lecture-note/m05-clustering/pen-and-paper/exercise.tex`
   (compare-two-groups pattern) and `lecture-note/m06-centrality/pen-and-paper/exercise.tex`
   (guess-then-compute-then-revisit pattern) for the two purest arcs.
3. Read `references/house-style.md` in this skill — the full style rules with
   quoted examples.
4. Pick the concept set. Each sheet covers **one coherent cluster** of concept
   IDs, not a whole module. Two sheets per module means two disjoint clusters,
   each ending at its own "you just invented X" moment.
5. **For a new sheet, write `plan.md` beside where the sheet will go and stop.**
   Sadamori reviews the plan before a line of LaTeX is written — that is how m02
   was built. Write the plan **in Japanese**, in language that assumes no
   background, and say what each question asks, what the answer is, and which
   concept ID it covers. Ask him anything you are unsure of instead of choosing.
   A revision of an existing sheet does not need this.

## The shape of a sheet

Standard arc, 5-10 questions, **four pages maximum**:

1. **Concrete scenario, second person.** "You're new at a university and want to
   understand social dynamics of students." Real data on the page (a club
   roster, a cost table, a small drawn network) — never "consider a graph G".
2. **Naive attempt first.** Ask for a guess, a drawing, or a brute-force count
   *before* any machinery. Often literally: "Without doing any calculations,
   which student would you approach first? Explain your reasoning."
3. **Hand computation on scaffolded structures.** Pre-drawn tables and grids so
   the arithmetic is bounded and mechanical. Scaffolding is a table with its
   columns already named, or a box beside every node — not a blank at the end
   of a sentence.
4. **The discovery question.** After the student has measured two or three
   cases, name the object and ask them to state the rule:
   "Group B is called a 1-plex. Based on your observations, what do you think
   defines a k-plex?"
5. **Break it / stress it.** Change the data, add an adversary, add a budget
   constraint, and ask them to redo the reasoning. This is where the limitation
   concepts live.
6. **Lift to the general case.** Last question asks for the procedure, not the
   number: "You don't need to do the calculation, just describe the process
   using matrix multiplication."

Not every sheet needs all six, but a sheet with no step 4 is not a pen-and-paper
sheet.

## Hard rules

- **No definition before the student has produced the thing.** Names arrive
  after the counting, in the question that asks them to generalize.
- **Every number small enough to do by hand.** 4-10 nodes. Degrees under 6.
  Two-step random walks, not ten-step.
- **Estimate over exactness where the point is the shape.** "No need to
  calculate the value of each pixel exactly but show your estimate by shading."
- **No answers, no solutions, no hints that give away the punchline.** Hints
  only explain *notation or mechanics* the student cannot guess (e.g. how the
  CSR `pointers` list is built, or the sum formula for a two-step walk).
- **No inline blanks, and no gap sized for an answer.** Sadamori took both out of
  the m01 sheet and then out of m02: an underline after a question turns it into
  a transcription, and a gap the answer has to fit in is a gap that says how long
  the answer should be. Ask the question in words and let it be answered on the
  back of the sheet. The space that used to go to ruled lines goes to 14pt text
  and to bigger drawings. The one exception is the answer that belongs to a
  place on a drawing — see *Where the answer goes* below — and there the
  affordance is a box on the drawing, drawn big enough to write a digit in.
- **One ask per line.** A question that runs "how many? \_\_ and the average? \_\_
  and the worst case? \_\_" as one paragraph is three questions wearing one
  number. Break them into three short paragraphs. The room reads the sheet once,
  in half an hour, and much of it does not read English at home.
- **Bookend it.** If the sheet opened with a guess, close by re-asking the same
  question after the machinery exists (m06 asks Q2/Q3 again as Q8/Q9). The
  student sees their own intuition confirmed or broken.
- **Discussion is part of the sheet.** "Discuss how your estimates compare to
  the actual ratios. Did you notice that it became harder ...?"
- **Name what a question refers to, inside that question.** "Your route in 1(a)
  is a \_\_\_\_", "the map has \_\_\_\_", "how many?" and "check it in the lab"
  all shipped in an m01 draft and all had to be rewritten: the student cannot
  see what you meant. Write "the drive you numbered in 1(a)", "the highway map",
  "how many 2-step routes", "the notebook in Part 4".
- **Point back by Part, never by page.** m02 said "go back to the circle on
  page 1" and the circle moved to page 2 the next time the sheet was reflowed.
  Parts are stable, pages are not. The same bullet applies to a demonstrative:
  "one of those two numbers" was printed under a question that produced three.
  Name them.
- **Ask a question whose phrasing does not answer it.** "Which highway is left
  over?" tells the student that one will be. "Can you drive every highway
  without lifting your pencil?" does not.
- **Never ask them to draw something they have no way of knowing.** The eighth
  road was once "draw US-11 yourself" — nobody knows where US-11 runs. Print it
  on a second copy of the map and let the drawing be given.
- **One symbol, one meaning, per sheet.** Rows labelled Map A / Map B beside a
  city called A is a table nobody can read. Rename one of them.
- **Merge questions that are a single act.** "Fill in the table" and "now write
  the right name in the last column" is one question with the name box printed
  above the table.

## Where the answer goes

If the question is about a drawing, the answer belongs **on the drawing**, and
the sheet has to carry the affordance. Module 1 first asked for the route as a
row of blanks — `I \_ S \_ I \_ \_ \_ ...` — which is a transcription exercise
wearing the costume of the real one. It became a small circle beside every road
on the map, with the first two filled in, and the student writes 1 to 7 into
them. The constraint the sheet is teaching (each road exactly once) is then
visible as one number per circle.

m02 does the same thing with a box printed outside the ring beside every one of
sixteen people: the sheet is teaching that a distance belongs to a *seat*, and a
column of fifteen numbers written underneath hides exactly that.

Size the affordance for a hand, not for the page. A box the student writes a
digit into wants ~6mm on paper, and the `\resizebox` around the figure is set
from that number.

## Prefer material that exists

The m01 map was an invented campus creek with seven footbridges until it became
Ithaca, Syracuse, Binghamton and Albany joined by NY-13, NY-34, NY-79, I-81,
I-90, I-88 and NY-7 — roads the students drive, whose degrees happen to be
3, 4, 4, 3, and where the eighth road that breaks it (US-11) really does run
beside I-81. Real material can be checked, argued with, and remembered, and it
picks itself: use the region the students live in.

Work the other way round when you do this. Fix the structure the argument needs
first (here: exactly two odd nodes, and one more edge that makes four), then go
looking for real objects with that structure, and verify the degrees by hand
before writing a word of the story.

## Voice

Second person, imperative, light. Names in scenarios are ordinary student names
(Sarah, Noah, Emma). Pop-culture props are fine (hours spent watching Game of
Thrones). Never write in a textbook register.

**The sheet has no title.** It opens on Part 1 and its first sentence. A title
line, an author line and a "do this before the lecture" line were all on the m01
draft and all came off: the first costs three centimetres of paper for something
nobody reads, and the last is wrong anyway — the sheet is worked **in class**.
The playful title still exists, in the lecture note's link text
("Six Handshakes to a Stranger"), where it is doing a job.

Part headings carry the playfulness instead — "A letter from Omaha", "Ringville",
"Do your friends know each other?", "Back to Omaha". They also give every
question a name to point at: *the circle in Part 2*, *the whole drawing in
Part 3*.

Questions are labelled either `{\bf Question N}:` (running numbering across the
whole sheet) or an `enumerate` list with `[resume]` across sections. Pick one
per sheet and keep it.

**Verbs.** The student *writes*, *counts*, *traces*, *darkens*, *draws*. They do
not *fill in* — that verb belongs to the form of sheet this one is not.

## The paper budget

Four pages, 14pt, and no answer space is a tight budget, and it is meant to be:
what does not fit is a question that was not earning its place. Where to find
the room, in the order these were used:

- **Put two related figures side by side** rather than a page apart. m01's seven
  highways and the eight-highway version are one `tabular` of two `\resizebox`es
  with captions under them, which halves their height *and* lets 1(a) and 1(b)
  be compared without turning the sheet over.
- **Do not draw a second figure when the first will do.** m01's Part 3 works on
  the network from Part 2 and says so. Two drawings of the same object cost a
  quarter of a page and start to disagree with each other.
- **Approximate geometry is fine.** The map does not have to be to scale — "大体で
  良い". Four cities in roughly the right relative positions read better than
  four cities at true latitude and longitude squeezed into 7cm.
- **Scale the drawing to the affordance, not the other way round.** If the
  student writes a digit into a box on the figure, that box has to be ~6mm on
  paper. Set the `\resizebox` width from that and let the text find room
  elsewhere.
- **Then cut a question.** m01 dropped its Königsberg question to buy a page.

Measure the result rather than eyeballing it — a half-empty page is invisible
until you count it, and a *fully* empty one gets missed entirely:

```bash
pdftoppm -r 60 -png exercise.pdf p
for f in p-*.png; do echo -n "$f "; magick "$f" -crop x660+0+0 +repage \
  -fuzz 5% -trim -format "slack_px=%[fx:660-(page.y+h)]\n" info:; done
```

`660` is the bottom of the text block at 60dpi for the usual margins; anything
over ~60 is a page with a hole in it, and the crop keeps the page number from
making every page look full.

## LaTeX mechanics

Copy `assets/preamble.tex` verbatim as the top of a new sheet. It is m01's and
m02's preamble: 14pt Charter, tight margins, `\needroom`, `\parthead`, the `C`
column, the QR short-link macros, and the font guards. The older sheets
(`m03`-`m09`) each carry their own, earlier preamble; do not copy from those.

- Class: `\documentclass[a4paper, 14pt]{extarticle}` (17pt for very short,
  drawing-heavy sheets like m03). `extarticle` has no 13pt — the valid sizes are
  8, 9, 10, 11, 12, 14, 17, 20.
- Networks are drawn in TikZ by hand, nodes as `\node[draw, circle]`, either
  `node distance=1.5cm` relative placement or explicit polar coordinates
  (`at (90:1.3)`) for ring-shaped groups.
- **The body face is Charter, and the drawings are set in it too.** The
  handwriting font is for a heading (the answer key's "Answers") and nothing
  else: figure labels are read closely and want the text face.
- The handwriting font is `Pretty Neat` (some older sheets use `Humor Sans`).
  Neither is installed on this machine, and **naming a missing font is a hard
  error in fontspec, not a fallback** — seven sheets named one outright and
  stopped building. The preamble resolves the face once, through
  `Pretty Neat → Humor Sans → Excalifont → nothing`, into `\ppfont`. Excalifont
  is vendored in `tools/fonts/` and is what the chain actually lands on, here
  and in CI. Use `\ppfont`; never write `\fontspec{<a name>}`, and do not remove
  the chain. Charter has the same trap and the same guard: ask for
  `XCharter-Roman.otf` **by file**, because a CI runner says yes to
  `\IfFontExistsTF{Charter}` and then cannot typeset it.
- The `xkcd` sketch decoration exists in the preamble but is fragile: applying
  it to many nodes (as m03 does) throws `Dimension too large` and produces no
  output. Prefer plain `\node[draw, circle]`; use `[xkcd]` only on a few plain
  `\draw` lines.
- Fill-in tables: `p{1cm}` columns, or `\\[0.5cm]` row stretch to leave writing
  room inside cells.
- Boxed background information the student genuinely cannot derive goes in a
  `tcolorbox` (see m04's CDF/CCDF box) — use sparingly, once per sheet at most.
- **A bare `\color` at the start of a `p`-column cell costs that cell its first
  line**, so the entry sits a line below every other cell in its row. Wrap
  instead: `\textbf{\textcolor{...}{...}}`.
- **Labels on a TikZ path go in a second pass.** A `postaction` re-draws the
  path *over* the nodes placed on it, so a road drawn that way is drawn through
  its own label. Draw all the edges with `\draw`, then place the labels with
  `\path (a) to[same bend] node[...] (b);` — same bend spec, so keep them next
  to each other or they drift.
- **A fill-in box attached to a label** is a `label` on that node:
  `node[shield, label={[ord, name=o13]180:{}}] {NY-13}` gives a named empty
  circle touching the shield, on whichever side is free of other lines, and
  something else can write into `(o13)` later.
- `to[out=m, in=m, looseness=1.35]` where `m` is the bisector of two directions
  draws a loop that goes *round* a node rather than across it. `bend left/right`
  between two points on a circle will cut through the middle.
- **Never keep a question off a page break by comparing `\pagegoal` with
  `\pagetotal`.** It is the obvious way to write a "break unless N lines are
  left" macro and it is wrong: the page builder has not necessarily run when the
  macro expands, so the numbers it reads can still be the *previous* page's. The
  test then says "no room" on a page that is empty and the `\newpage` throws that
  page away — m02 shipped a blank page 3 this way, and it is invisible in the
  source. Use needspace's glue trick instead, which needs no `needspace.sty`:
  `\vskip 0pt plus <N>` then `\penalty -100` then `\vskip 0pt plus -<N>`.
- **Figures shared by the sheet and its answer key live in one file**
  (`mapkit.tex`), `\input` by both. Two copies of a 100-line TikZ picture drift
  within a day.
- Long URLs on a printed sheet are a QR code plus a short link, never the raw
  address — see `lecture-note/LAB_NOTEBOOK_GUIDE.md`. Load `hyperref` with
  `[hidelinks]` or the print carries coloured boxes.

## The answer key

`solutions.tex` beside the sheet, sharing its figures through the same
`\input`. Two things make it usable:

- **It carries the questions as well as the answers.** A key that reads "8 and
  4" next to a question number can only be read with the sheet in the other
  hand.
- **A map question is answered with a map.** m01's key draws the same map with
  the circles filled 1 to 7, and the eight-road copy with a cross on the road
  that goes undriven. Answers in running text are `\textbf{\textcolor{...}{}}`
  blue so the eye can skip between them.

Answers to the lab go in the key too, and the notebook's own worked copy is
generated, never hand-edited. Sadamori's call on m01 was that the key ships in
the public repo; ask before assuming that for another sheet.

## The lab notebook, if the sheet has one

A sheet may end by handing the student to a marimo notebook that does by
machine what they have just done in pencil — Module 1's Part 4 and Module 2's
Part 6 are the worked examples, and both are done **alone**, not in pairs. The
sheet's last part is a `tcolorbox` with a QR code and a `go.skojaku.com/mNNlab`
short link, and nothing else.

**The notebook teaches the mechanism, so interactivity is the whole point.**
Three beats, in this order:

1. **An interactive visualisation that prepares them** — a slider, a step
   button, something they turn with their hands before any code. It runs on a
   *different, smaller* network than the one the sheet made them work out.
2. **Then they write some code** — two or three `✍️` cells, small functions,
   the rules the rest of the notebook runs on (`ring_edges`, `distances_from`,
   `local_clustering` in m02).
3. **Then a demo driven by their own code**, so they can see whether it does
   what they expected. This is where the notebook earns its place: the student
   watches their own three lines reproduce, or fail to reproduce, the number
   they got in pencil.

**Finished early** gets a fourth beat, and it is the best part of the m02
notebook: something their correct code gets *wrong*. Ask them to explain why
with algebra, give a hint rather than the derivation, ask them how they would
repair the measure, and name the published repairs so the answer has somewhere
to go. In m02 that is $\sigma$ scoring a plain ring with no shortcuts as a
strong small world, and getting more confident as $n$ grows.

Read `lecture-note/LAB_NOTEBOOK_GUIDE.md` before writing or editing one. The two
things that will otherwise cost an afternoon:

- **molab ignores a notebook's `css_file`**
  ([marimo-team/marimo#8467](https://github.com/marimo-team/marimo/issues/8467)),
  so the stylesheet has to travel inside the file and go up as a `<style>` tag
  from the first cell. It styles correctly on your machine either way, which is
  how this gets shipped broken.
- **The animation must not walk the map the student is being asked to write
  down.** Teach on a different, smaller network; leave their own as a picture
  with nothing printed from it.

## Where files go

`lecture-note/mNN-name/pen-and-paper/`, beside the module's `.qmd` files —
that is where every sheet actually lives, m01 and m02 included. A module with
two sheets puts them in one directory as `exercise.tex` and a second file named
for its idea. Inside it:

| file | what it is |
|---|---|
| `exercise.tex` | the sheet, four pages |
| `solutions.tex` | the answer key, published alongside |
| `<name>kit.tex` | the TikZ figures, `\input` by both |
| `lab.py` | the marimo notebook, if there is one |
| `lab-solutions.py` | generated from `lab.py`, never hand-edited |
| `lecture-hall.css` | the notebook's stylesheet, embedded into it at build |
| `mNNlab-qr.png` | the QR square for the short link |

Build with `bash tools/build_worksheets.sh <the sheet's directory>`, or
`xelatex -interaction=nonstopmode exercise.tex` run twice from the sheet's own
directory. A full TeX Live is needed; BasicTeX lacks `adjustbox` and
`tikz-3dplot` (`sudo tlmgr install adjustbox tikz-3dplot`).

**Commit the `.tex` only. The PDF is not committed** — `.gitignore` has a
blanket `*.pdf`, and it is meant. Every sheet is rebuilt from source by
`.github/workflows/quarto-publish.yml` before the lecture note is published, so
the link on the site always matches the `.tex` that was pushed. Do not
`git add -f` a PDF back in; a rewritten binary on every edit is what makes a
repository heavy.

`solutions.pdf` is built and **published alongside the exercise**, and linked
from the table on the lecture note's front page. Write it for a reader who has
already tried the sheet — it is not hidden, so it should read as the worked
answer rather than as a key.

Proofread by rendering: `pdftoppm -r 60 -png exercise.pdf out` and read the
images. Tables and their question text drift apart across page breaks — wrap
each question plus its table in `\begin{minipage}{\textwidth} ... \end{minipage}`.

**Look at the pictures, do not reason about the source.** Nearly every fix in
the m01 rebuild came from rendering the page and seeing it: a city name running
off the drawing, two route shields overlapping, a pairing arc drawn straight
through the node it was pairing, a label sitting one line below its row. None
of those are visible in the `.tex`. Render at 150 dpi or crop and magnify
(`pdftoppm -r 300` + `magick -crop`) when a figure is dense, and re-render after
every geometry change rather than at the end.

## After writing

1. Compile and read the PDF page by page. Check that no question is orphaned
   across a page break, no question is separated from its table or drawing, and
   no page is left with a hole in it (measure it — see *The paper budget*).
2. Register coverage in `curriculum.yml`: add the sheet path to the `in_class`
   list of every concept ID the sheet touches.
3. Add a link from the module's lecture note (`01-concepts.qmd` or
   `03-exercises.*`), matching the existing line style:
   `- [✍️ Pen and paper exercises](pen-and-paper/exercise.pdf)`.
4. `git add`, commit, push.

## Self-check before declaring done

- [ ] Could a student who has never heard the term still answer Question 1?
- [ ] Would a first-year reading English as a second language get every question
      on one pass? Is any question three questions in one paragraph?
- [ ] Is there a question that hands them a name and asks them to state the rule?
- [ ] Is every computation doable in under two minutes by hand?
- [ ] Does the sheet break or stress the idea, not just apply it?
- [ ] Is the last question about the general procedure, not a number?
- [ ] Does the PDF compile, is it four pages or fewer, and is every page full?
- [ ] Have you *looked* at every page as an image, at the size it prints?
- [ ] Are there any blanks, ruled answer gaps, or a title left on it?
- [ ] Does every question name what it is asking about, without the sheet in the
      other hand?
- [ ] Does any question's wording give away its own answer?
- [ ] Where the answer is a drawing, does the sheet give somewhere on the
      drawing to put it, big enough to write in?
- [ ] If there is a lab notebook: does it run clean with the blanks blank, does
      it carry its own stylesheet, and does it print nothing the student is
      being asked to work out?
- [ ] If there is an answer key: does it restate the questions, and does it
      answer the drawings by drawing?
