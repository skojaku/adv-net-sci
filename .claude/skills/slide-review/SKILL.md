---
name: slide-review
description: Validate a Marp lecture deck against the course slide rubric (one point per slide, figure design standards, four-act narrative, milestone demos), and drive the fix/re-verify loop. Use when asked to review, validate, or QA lecture slides. Argument: path to the deck .md (default: the Marp deck in the current directory).
---

# Slide review

All substance lives in three repo-root-relative files, so any agent — not just Claude — can
run the same review:

- `docs/slide/new/SLIDE_RUBRIC.md` — what to check, severities, report format
- `docs/slide/new/FIGURE_GUIDE.md` — how to author figures: tool choice, sizing, palette,
  and the traps found the hard way
- `docs/slide/new/REVIEW_PLAYBOOK.md` — how to run the review → fix → re-verify loop
  without repeating known process failures

This skill is only a dispatcher.

## Reviewing

1. Resolve the target deck: the argument if given; otherwise the `.md` file with
   `marp: true` front matter in the current directory. If ambiguous, ask.
2. Read `SLIDE_RUBRIC.md` and follow its "How to run a review" procedure exactly — render
   every slide to PNG first; never review from source alone.
3. **Before trusting any review, confirm the render is current.** Figures regenerated after
   a render silently invalidate every figure finding, and this has cost whole rounds:

   ```sh
   find figures -name '*.png' -newer review/slide.001.png | wc -l   # must be 0
   ```

4. Deliver the findings in the rubric's report format, ordered by severity. Report only —
   do not edit the deck unless the user asks for fixes afterward.

## Fixing, if asked

Read `REVIEW_PLAYBOOK.md` first. Its rules are the ones that were broken during the Module 01
rebuild; the four that cost the most:

- **Measure on the rendered slide, not the source PNG.** Three rounds reported a figure
  property as fixed, correctly, in the wrong coordinate space.
- **Re-read the rendered PNG before reporting a fix done.** Every round contained at least
  one repair reported as landed that the render contradicted.
- **Fix at the generator, with an assertion — not at the individual figure.** A defect class
  patched per-figure reappears on the next figure drawn.
- **After changing a figure, check every slide that uses it.** A shared asset leaked a
  concept 41 slides early; a global sizing change hid the edges on one figure entirely.

## Keeping this current

When something goes wrong in a way the three files above did not anticipate, **add it** —
to the playbook if it is about running the loop, to the figure guide if it is about drawing,
to the rubric if it is about what counts as a defect. That is what keeps the next deck from
paying for the same lesson.
