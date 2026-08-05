---
name: slide-review
description: Validate a Marp lecture deck against the course slide rubric (one point per slide, figure design standards, four-act narrative, milestone demos). Use when asked to review, validate, or QA lecture slides. Argument: path to the deck .md (default: the Marp deck in the current directory).
---

# Slide review

All substance lives in `docs/slide/new/SLIDE_RUBRIC.md` (repo root relative) so
that any agent — not just Claude — can run the same review. This skill is only a
dispatcher:

1. Resolve the target deck: the argument if given; otherwise the `.md` file with
   `marp: true` front matter in the current directory. If ambiguous, ask.
2. Read `docs/slide/new/SLIDE_RUBRIC.md` and follow its "How to run a review"
   procedure exactly — render every slide to PNG first; never review from source
   alone.
3. Deliver the findings report in the rubric's report format, ordered by severity.
   Report only — do not edit the deck unless the user explicitly asks for fixes
   afterward.
