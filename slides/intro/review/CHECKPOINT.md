# Checkpoint

## Round 3 — instructor revision pass (Fall 2026)

Driven by the instructor's own slide-by-slide notes, not by a reviewer. Tier 0 gate
re-run after every batch. Deck grew 51 -> 53 slides.

### What changed

| Instructor note (old slide number) | What was done |
|---|---|
| cut slides 4, 5, 6 | the three EngiNet program slides are gone |
| office hours | Friday, roughly 13:00-15:00 (was 10:00-14:00); syllabus synced |
| slide 8 title too specific | Part 1 band and roadmap item 01 both read "Introduction" |
| slide 9 "Turn to your neighbour" | "Form a group and discuss" — applied to slide 14's prompt too |
| slides 11, 12 figures unclear, and drop the "ruler" wording | replaced with `flue-01.png` / `flue-02.png`, the two Brockmann-Helbing 2013 panels the archive deck used; titles are now "Kilometres predict nothing" / "Flights predict it exactly" |
| slide 13 subtitle | removed |
| slides 15, 16 network was wrong shape | `interbank_1/2` rebuilt as a five-layer lending web: "your bank" is four steps from Lehman and the cascade walks the layers one at a time |
| slide 17 wanted a figure | xkcd 2347 "Dependency" (the instructor supplied the image URL) |
| slide 23 question too broad | two concrete failures (home router vs. bank card processor) before the question |
| slides 24, 25 need more examples | new slide: power grid 2003, gut microbiome, Suez 2021, word co-occurrence |
| can YouTube be embedded? | see "YouTube" below — the deck now carries a linked thumbnail |
| slide 31 von Neumann, slide 33 Euler cropped through the face | `prep_photos.py` gained a `pad` fit: a portrait whose subject cannot survive a landscape crop is padded instead |
| slide 41 "coding assignment" | "an assignment. Some are code; some are not." Syllabus wording matched |
| exam week placeholder | 10-16 December 2026, from the Binghamton academic calendar |
| project dates | proposal Sun 27 Sep, presentations 1 and 3 Dec, paper Sun 6 Dec |
| "Three projects from previous years" | three slides, each with the figure from the archive deck (`sci-topic-net`, `ecog`, `super-charger`) |
| absence policy | new "Missing a class" slide: form plus email, and an absence not on the form is not counted |

### YouTube

`html: true` in the front matter plus `marp --html` does keep an `<iframe>` in the HTML
export, verified by rendering and grepping the output — so a real embed is possible if the
deck is presented from HTML. It is **not** usable in the shipped artifact: the `--images png`
and PDF paths escape the tag and print the raw HTML to the room, which is what the first
attempt did. The deck therefore uses a linked thumbnail (`xz_video_thumb.jpg`), which is
correct in every export.

### Figure-container arithmetic, re-learned

The render gate's container check runs *before* `exempt_figures`, so an imported image cannot
be waved through — it has to actually fit:

- A file under ~3000 px wide is read as authored for a 537 px column. A full-width imported
  figure must therefore be upscaled past 3000 px, not just cropped.
- Full width needs aspect <= 0.352, a column <= 0.708. The Science figures are 0.545 as
  published, so each was cropped to its bottom row of scatter panels (0.34) and doubled.
- A portrait image cannot satisfy either cap. Pad it to landscape (`fit="pad"`) rather than
  cropping through the subject.

## Round 2 — clean

- Deck: 51 slides. Tier 0 gate: **pass** (`python3 -m gatelib review .`, exit 0).
  Three 3px-ink warnings (slides 11, 19, 43) are arrowheads and square outlines, not glyphs.
- Tier 1/2 LLM review by three sonnet agents over slides 1-18, 19-35, 36-51:
  **0 blockers, 0 majors, 0 minors** in every range.
- Round 1 had 3 blockers-equivalent (1 blocker, 9 majors, 4 minors); all fixed and re-verified.

### Round 1 findings and what was done

| Finding | Fix |
|---|---|
| N4a — the pollinator figcaption answered the slide's own question | caption reduced to what a line means |
| N2 — xz detection slide, Part 2 payoff, "knowing the parts" all had no visual | three new figures: `xz_3`, `same_shape`, `parts_vs_relations` |
| F1/F3/F4 — the three past-project screenshots (unexplained node sizes, yellow callouts, an EEG head diagram, unreadable labels) | the three slides became one slide naming the projects in words |
| S4 — the last movement was pure logistics | new "Before you go" question slide reaching back to the Part 2 activity |
| FACT — Mexico City to Madrid is ~9,090 km | "nine thousand kilometres" |
| FACT — Descartes gave a method, not a substance | "four attempts to reduce the world to something simpler" |
| P3/F3 — thin EngiNet title slide, phone number wrapping mid-digits | title set as `lead`; numbers on their own bullet |
| naming — grading figure said "Homework", the slide says "Assignments" | figure relabelled |
| L6 — pen-and-paper slide hung with slack below | `_class: mid` |

Round 3 reversed the F1/F3/F4 fix at the instructor's request: the past-project figures are
back, one per slide, cropped and padded so they pass the gate this time.

### Still open, for the instructor

- The syllabus header still reads `Time: W16:40 -- 19:40` while the course outline is Tue/Thu.
  The outline was mapped onto Tue/Thu per the instructor; the header time is unverified.
- `syllabus.pdf` could not be recompiled here: `bbding.sty` is missing from this machine's
  TeX Live (`texlive-fonts-extra`). `syllabus.tex` is current; the PDF is not.

## Infrastructure notes

- `~/.claude/skills/slide/gatelib/cli.py` invoked `marp` without `--no-stdin`, so every render
  hung instead of finishing (25 minutes on the first run). Patched in place; the flag is what
  `REVIEW_PLAYBOOK.md` already prescribes.
- Delete `review/slide.*.png` before re-rendering a deck that lost slides: a round-2 render left
  `slide.052.png` behind from the 52-slide version and the gate happily checked the stale file.
- The render gate reads a figure narrower than ~3000px as authored for a `cols` column, and its
  scale arithmetic assumes 4 px per bp. Figures here are authored accordingly.
- `prep_photos.py` is the only writer of the deck-facing photograph copies. Anything imported
  from outside (a journal figure, a comic, a screenshot) goes through `figures/src/` and gets an
  entry there, so a re-run reproduces the deck exactly.
