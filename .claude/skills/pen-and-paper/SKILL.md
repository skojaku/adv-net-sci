---
name: pen-and-paper
description: >-
  Write or revise a pen-and-paper exercise sheet (LaTeX worksheet) for a module
  of the network science course, in Sadamori's discovery-first house style —
  students do the exercise BEFORE the lecture and reconstruct the concept with
  their own hands. Use when asked to create, extend, review, or fix a
  pen-and-paper / worksheet / exercise sheet for any module m00-m09.
---

# Pen-and-paper exercise sheets

A pen-and-paper sheet is **not** a practice problem set. Students meet it
*before* they are taught the concept. The sheet's job is to walk them into the
concept by hand, so the lecture afterwards only has to give a name to something
they already built.

If the student could answer a question by recalling a definition, the question
is wrong. Every question must be answerable with a pencil, a small drawing, and
counting.

## Before writing

1. Read `curriculum.yml` (repo root) for the target module: `big_question`,
   `hook`, `objectives`, and the full `concepts` list with IDs.
2. Read at least two existing sheets end to end to re-anchor the voice —
   `lecture-note/m05-clustering/pen-and-paper/exercise.tex` (compare-two-
   groups pattern) and `lecture-note/m06-centrality/pen-and-paper/exercise.tex`
   (guess-then-compute-then-revisit pattern) are the two purest examples.
3. Read `references/house-style.md` in this skill — the full style rules with
   quoted examples.
4. Pick the concept set. Each sheet covers **one coherent cluster** of concept
   IDs, not a whole module. Two sheets per module means two disjoint clusters,
   each ending at its own "you just invented X" moment.

## The shape of a sheet

Standard arc, 5-10 questions, 1-4 pages:

1. **Concrete scenario, second person.** "You're new at a university and want to
   understand social dynamics of students." Real data on the page (a club
   roster, a cost table, a small drawn network) — never "consider a graph G".
2. **Naive attempt first.** Ask for a guess, a drawing, or a brute-force count
   *before* any machinery. Often literally: "Without doing any calculations,
   which student would you approach first? Explain your reasoning."
3. **Hand computation on scaffolded structures.** Pre-drawn tables, blanks, and
   fill-in grids so the arithmetic is bounded and mechanical.
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
- **Leave physical space to write.** `\vspace{3em}` for one-liners, `\vspace{8em}`
  to `\vspace{10em}` for reasoning, `\clearpage` between parts, `\underline{\hspace{2cm}}`
  for inline blanks and `\underline{\hspace{\textwidth}}` for a full-line answer.
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

If blanks really are the answer, count them against the answer: a 7-edge trail
is 8 places and 7 roads, so 15 tokens, and the first draft printed 13.

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

Second person, imperative, light. Titles are playful, not descriptive:
"Who's the Big Cheese in the University Clubs?", "Build it, Break it, and Build
it back!", "Discovering Friend Groups". Names in scenarios are ordinary student
names (Sarah, Noah, Emma). Pop-culture props are fine (hours spent watching
Game of Thrones). Never write in a textbook register.

Questions are labelled either `{\bf Question N}:` (running numbering across the
whole sheet) or an `enumerate` list with `[resume]` across sections. Pick one
per sheet and keep it.

## LaTeX mechanics

Copy `assets/preamble.tex` verbatim as the top of a new sheet. It is the
preamble used across all existing sheets, plus a font guard.

- Class: `\documentclass[a4paper, 14pt]{extarticle}` (17pt for very short,
  drawing-heavy sheets like m03), 1in margins, `\parindent=0pt`, `\parskip=0.5em`.
- Networks are drawn in TikZ by hand, nodes as `\node[draw, circle]`, either
  `node distance=1.5cm` relative placement or explicit polar coordinates
  (`at (90:1.3)`) for ring-shaped groups.
- The handwriting font is `Pretty Neat` (some older sheets use `Humor Sans`).
  Neither is installed on this machine, and **naming a missing font is a hard
  error in fontspec, not a fallback** — seven sheets named one outright and
  stopped building. `assets/preamble.tex` resolves the face once, through
  `Pretty Neat → Humor Sans → Excalifont → Latin Modern Roman`, into `\ppfont`
  and `\ppfontname`. Excalifont is vendored in `tools/fonts/` and is what the
  chain actually lands on, here and in CI. Use `\ppfont`; never write
  `\fontspec{<a name>}`, and do not remove the chain.
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
machine what they have just done in pencil — Module 1's Part 4 is the worked
example, and it is done **alone**, not in pairs. Read
`lecture-note/LAB_NOTEBOOK_GUIDE.md` before writing or editing one. The two
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

New sheets: `lecture-note/mNN/<slug>/exercise.tex`, where `<slug>` is a
short kebab-case name of the sheet's idea (e.g. `m02/counting-triangles`).
Existing legacy sheets stay under `lecture-note/mNN-name/pen-and-paper/`.

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

1. Compile and read the PDF page by page. Check that every question has room to
   answer and no question is orphaned across a page break.
2. Register coverage in `curriculum.yml`: add the sheet path to the `in_class`
   list of every concept ID the sheet touches.
3. Add a link from the module's lecture note (`01-concepts.qmd` or
   `03-exercises.*`), matching the existing line style:
   `- [✍️ Pen and paper exercises](pen-and-paper/exercise.pdf)`.
4. `git add`, commit, push.

## Self-check before declaring done

- [ ] Could a student who has never heard the term still answer Question 1?
- [ ] Is there a question that hands them a name and asks them to state the rule?
- [ ] Is every computation doable in under two minutes by hand?
- [ ] Does the sheet break or stress the idea, not just apply it?
- [ ] Is the last question about the general procedure, not a number?
- [ ] Does the PDF compile, and is there white space to write in?
- [ ] Have you *looked* at every page as an image, at the size it prints?
- [ ] Does every question name what it is asking about, without the sheet in the
      other hand?
- [ ] Does any question's wording give away its own answer?
- [ ] Where the answer is a drawing, does the sheet give somewhere on the
      drawing to put it?
- [ ] If there is a lab notebook: does it run clean with the blanks blank, does
      it carry its own stylesheet, and does it print nothing the student is
      being asked to work out?
- [ ] If there is an answer key: does it restate the questions, and does it
      answer the drawings by drawing?
