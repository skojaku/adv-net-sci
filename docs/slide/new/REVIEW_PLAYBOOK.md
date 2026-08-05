# Slide review playbook

How to run the review → fix → re-verify loop. `SLIDE_RUBRIC.md` says what to check;
`FIGURE_GUIDE.md` says how to author figures; this file says how to run the loop without
repeating mistakes that have already cost rounds.

Every rule below is here because it failed at least once during the Module 01 rebuild
(30 slides → 73, nine rounds). Add to it when something new goes wrong.

## The loop

1. **Render every slide to PNG.** Never review from source.
2. **Verify** — reviewers read every rendered PNG, one at a time, and measure rather than
   eyeball.
3. **Plan** — collect the findings into one `review/FIXES_Rn.md` spec.
4. **Fix** — dispatch against that spec; deck markdown and figure generator to *separate*
   agents, never both on one file.
5. **Regenerate figures, re-render, re-verify.** Go to 2.

## Rules that exist because they were broken

### Before trusting any verification, check the render is current

```sh
find figures -name '*.png' -newer review/slide.001.png | wc -l   # must be 0
[ deck.md -nt review/slide.001.png ] && echo STALE
```

This has happened **three times**: a figure agent finished one more fix after the render, so
reviewers spent their pass reading images that no longer matched disk. The first two cost a
full round each. The third was caught by running the check above and cost nothing — the
recovery works, so use it:

1. Message every reviewer: **hold, do not report, wait for the word RERENDERED.**
2. Regenerate figures, delete the old PNGs, re-render, confirm the check returns 0.
3. Message RERENDERED and tell them to re-read their range **from scratch**.

Their text and layout observations survive — the markdown did not change — but every figure
judgment must be redone.

The underlying cause is that fix agents keep working after reporting. Prefer to launch
reviewers only once every fix agent has gone idle, and re-run the check immediately before
you launch them.

### A gate that cannot fire is worse than no gate

`check_render.py`'s node-diameter band was inert for the whole of Module 02's first build.
It thresholds on `gray < 60`, and every colour in this palette is lighter than that — the
node blue converts to luminance 88 — so `node_discs()` returned `[]` on every slide and the
26–52px band went unenforced. A 19px disc passed a green run. Two reviewers found it
independently in the same round.

No gate at all would have been safer, because the green run was read as coverage. When you
add or inherit a gate, prove it fires: run its detector on a slide you know is bad and check
it says so. Then check the summary actually prints the measurement — the missing
`node diameter: …px across N discs` line was the visible symptom for a whole build and
nobody looked for it.

The generator had the same disease from the other end: it *computed* the property it was
asserting instead of measuring it (see `FIGURE_GUIDE.md`, "Measure the render"). Between
them, two independent checks on in-figure type size both passed while every label in the
deck was 17% under the floor.

### Measure on the rendered slide, not the source PNG

**Three consecutive rounds reported "node size is now uniform deck-wide" and were followed
by a verifier measuring an 8×, then a 16×, spread.** The assertion was true — every source
PNG carried a 150px disc — and irrelevant, because the deck scales each image by a different
factor (0.14×–0.34×) that the generator never sees. The defect lives on the slide, so the
measurement has to happen on the slide.

Same for text size. A figure whose type is comfortable at source resolution can land at 3px
on the slide.

### A fixer must re-read the rendered PNG before reporting done

**Every round contained at least one repair reported as landed that the render contradicted.**
Reading the source PNG is not enough (see above). Reading the code is not enough. Open the
slide.

### Fix at the generator, not at the figure

A defect class fixed on the named figure reappears on the next figure someone draws. Labels
sitting on filled discs were reported **five times on five different figures across four
rounds** before anyone wrote a placement helper with an assertion. The self-loop failed six
rounds under three different-looking explanations, all of which were the same missing
invariant.

When a finding is geometric, ask what invariant was violated, then assert it and let the
build fail. Assertions caught, before any human looked: four rings drawn inside the node they
were meant to encircle; an arrowhead standoff calibrated at the wrong linewidth; a traversal
whose numbered visit order jumped between non-adjacent nodes; a ring lattice whose chords
passed 0.005 units inside the discs they crossed.

### After changing a figure, check every slide that uses it — and every claim about it

Three separate regressions came from this:

- A matrix was added to a figure for one slide; the same file was already on a slide 41
  earlier, which then showed an adjacency matrix with unexplained colours before the matrix
  was defined.
- Making nodes a uniform size hid the ring-lattice edges on the small-world figure, so no
  triangle was visible — on the slide whose claim is high clustering.
- Fixing the badge overlap on a self-loop answer slide left the question slide correct and
  broke the answer.

**If two slides need different content, emit two files.** Reuse is only safe when both slides
explain the figure the same way.

### Verify the numbers before writing them into a spec

Two mathematical errors reached slides through specs written in this loop:

- A spec asked for "the concrete 12 vs 25 count" as evidence that CSR saves memory. That
  counts one of three arrays; CSR needs 30 against dense's 25 at that size, so the slide
  shipped a false claim that also contradicted its own neighbouring slide.
- A spec asserted that a sketch showed irregular landmasses. It showed rounded rectangles, so
  the fix built on it could not work.

Compute it, or read the file, before writing it down.

### Make the generator report every failure, not the first

A figure generator that stops at the first failed assertion hides the rest. Module 03's
geometry gates fire in clusters — raising the type size broke seven figures at once — and
stopping at figure 3 of 60 turns one round of fixes into seven. Catch per figure, print each
failure, and exit non-zero at the end:

    bad = []
    for name, fn, cont in FIGURES:
        try:
            emit(name, fn(), cont)
        except AssertionError as e:
            bad.append(str(e)); print(f"  FAIL {name}: {e}")
    if bad: sys.exit(1)

### Watch for a fix that moves an error rather than removing it

The directed Euler condition was wrong in two consecutive rounds: the first fix corrected the
degree rule and moved the error into the connectivity clause, where the deck then falsified
its own rule two slides later using its own figure. When a correctness fix lands, re-derive
the whole statement, not the clause you touched.

## Expectations

**The Blocker count will not fall monotonically, and that is not necessarily failure.**
Module 01 ran 29 → 7 → 4 → 7 → 9 → 3 → 4 → 11. Two things drive the bumps:

- The deck grows. 30 slides became 73, so there is 2.4× more surface, and every new slide and
  figure is reviewed for the first time.
- Reviewers get more forensic. Later rounds measured pixel positions and colour samples, so
  they found defects earlier rounds' coarser reads had passed over.

What *should* fall monotonically is the **severity class**. Round 1's blockers were structural
— tables, code blocks, three-column text, a missing act, no progressive disclosure. By round 8
they were figure geometry and one arithmetic slip. Track that, not the count.

## Roles

Review and planning want the stronger model; applying a written spec to markdown or a figure
generator does not. Run reviewers on Opus over disjoint slide ranges, write the fix spec
yourself, and dispatch the edits to cheaper agents — one for the deck, one for the figures,
never both on the same file.
