---
name: slide-build
description: Build a new Marp lecture deck for a course module from scratch — scaffold from m01, spec first, figures with assertions, check_render gate, then the slide-review loop until PASS. Use when asked to create, build, or generate lecture slides for a module. Argument: the module (e.g. m02 or a module dir path).
---

# Slide build

All substance lives in four repo-root-relative files, so any agent — not just Claude —
can run the same build:

- `docs/slide/new/DECK_BUILD_GUIDE.md` — the use model (slides serve dialogue, not
  reading), the order of work, the module scaffold, and the Marp/theme facts
- `docs/slide/new/SLIDE_RUBRIC.md` — what the deck must satisfy (it is also the spec's
  non-negotiables list)
- `docs/slide/new/FIGURE_GUIDE.md` — tool choice, author-at-final-size, measured floors,
  assertions
- `docs/slide/new/REVIEW_PLAYBOOK.md` — how to run the review → fix → re-verify loop

This skill is only a dispatcher.

## Building

1. Resolve the module: the argument if given (e.g. `m02` →
   `docs/slide/new/m02/`). Content sources are the module's entry in `curriculum.yml`
   (big_question, hook, concept list with prereqs) and
   `docs/lecture-note/<module-slug>/`.
2. Read `DECK_BUILD_GUIDE.md` **before writing anything** and follow its "Order of
   work" exactly: scaffold from m01 (theme, `check_render.py`, README) → `review/DECK_SPEC.md`
   → `review/FIGURE_SPEC.md` → `figures/make_figures.py` (+ `make_animations.py`) →
   deck → render → `python3 check_render.py` exits 0.
3. The spec comes first and gets verified — compute every number in it; two arithmetic
   errors reached m01 slides through unverified specs.
4. Only after the checker is green, run `/slide-review` and drive the loop per
   `REVIEW_PLAYBOOK.md` until PASS. Deck edits and figure edits go to separate agents,
   never both on one file.
5. Commit every round with the round's lesson in the message.

## Keeping this current

When building a deck teaches something the four files above did not anticipate, **add
it** — authoring lessons to the build guide, drawing lessons to the figure guide, loop
lessons to the playbook, defect definitions to the rubric.
