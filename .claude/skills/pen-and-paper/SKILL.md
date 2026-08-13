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
   `docs/lecture-note/m05-clustering/pen-and-paper/exercise.tex` (compare-two-
   groups pattern) and `docs/lecture-note/m06-centrality/pen-and-paper/exercise.tex`
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
  It is **not installed on this machine** — the guard in `assets/preamble.tex`
  falls back silently so the file still compiles. Do not remove the guard.
- The `xkcd` sketch decoration exists in the preamble but is fragile: applying
  it to many nodes (as m03 does) throws `Dimension too large` and produces no
  output. Prefer plain `\node[draw, circle]`; use `[xkcd]` only on a few plain
  `\draw` lines.
- Fill-in tables: `p{1cm}` columns, or `\\[0.5cm]` row stretch to leave writing
  room inside cells.
- Boxed background information the student genuinely cannot derive goes in a
  `tcolorbox` (see m04's CDF/CCDF box) — use sparingly, once per sheet at most.

## Where files go

New sheets: `docs/pen-and-papers/mNN/<slug>/exercise.tex`, where `<slug>` is a
short kebab-case name of the sheet's idea (e.g. `m02/counting-triangles`).
Existing legacy sheets stay under `docs/lecture-note/mNN-name/pen-and-paper/`.

Build with `xelatex -interaction=nonstopmode exercise.tex` run twice, from the
sheet's own directory. Commit the `.tex` and the `.pdf`; do not commit `.xdv`,
`.aux`, `.log`, `.out`. The repo `.gitignore` has a blanket `*.pdf`, so the PDF
needs `git add -f`.

Proofread by rendering: `pdftoppm -r 60 -png exercise.pdf out` and read the
images. Tables and their question text drift apart across page breaks — wrap
each question plus its table in `\begin{minipage}{\textwidth} ... \end{minipage}`.

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
