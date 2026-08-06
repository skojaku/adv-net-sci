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

**And do not infer idleness from silence — look.** Module 04 held all three of its figure agents,
confirmed every one of them idle and every file committed, rendered, measured zero figures newer
than the render, and had a build running the whole time from a *fourth* session nobody had thought
to hold. It was found because one agent went looking rather than reporting itself clean:

    ps -o pid=,ppid=,command= -ax | grep -E 'make_figures|make_animations|pdflatex' | grep -v grep

That is cheap, gives a definite answer, and names the owning process, so it distinguishes "my
agents are done" from "nothing is writing to this directory" — which are different claims, and only
the second one is the one the render depends on. Run it immediately before rendering, not after.

**When you do find a race, resolve it on content, not on timestamps.** `find -newer` reports that a
build touched a file; it cannot tell you whether the file changed. A build re-run over unchanged
sources rewrites every PNG with a new mtime and identical bytes, and treating that as staleness
throws away a review round for nothing. `git status` on the figure paths answers the question that
actually matters.

The recovery, meanwhile, is narrower than it looks: tell the reviewers to keep reading and hold
their reports. Their images cannot change under them — only the lead re-renders — so their text,
layout, narrative and arithmetic observations are all safe. The single thing at risk is that a
defect correctly reported against the render has already been superseded on disk, which sends a
fixer after something that is no longer there.

### "A caveat on the answer" and "the answer cannot be computed yet" are different sentences

A fix agent, asked to write a number into a slide, sent back three candidate values with a
note that the sweep's sampling quantised all three. That read as a caveat, so the lead
picked one of the three. The right sentence was the second one — the sampling made *none*
of the three computable, and the fix was to resample, not to choose.

Writing the first when the second is true routes a decision to someone who then decides on
incomplete grounds, and it looks like diligence while doing it. If the work you are handing
back cannot answer the question as posed, say that in the first line, before the options.

(The agent that made this mistake is also the one that named it, after the fact, better than
the lead had.)

### Wait for the report, not for silence

Polling a fix agent's file mtimes until they go quiet does **not** tell you it has
finished. It tells you the agent is thinking, reading, or between two edits of a long
pass — and a half-applied generator fails in ways indistinguishable from a broken
hand-off. In Module 02 this cost three round-trips: the lead measured a mid-edit tree,
reported the build as abandoned, and was wrong twice in the same hour on the same file.

A fix agent's build is only meaningful **after it reports done**. Until then, whatever you
measure is a snapshot of work in progress. Ask for the report; do not infer it.

The corollary still holds and is not in tension with this: once the agent has reported,
re-measure before trusting the report, and re-run `find figures -newer review/slide.001.png`
immediately before launching reviewers.

### Read the gate's own exit status, not a pipeline's

Module 02's lead reported "gate exit=0" for several consecutive rounds from

    python3 check_render.py 2>&1 | grep -E "all checks|problem"

where `$?` is **grep's** status. The gate had been exiting 1. A verifier ran it unpiped
and found the failure in one line.

Every other entry in this file is about a check that measured the wrong thing. This one
is the same disease one level up — the check was right and the *reading* of it was wrong,
which is harder to notice because nothing looks broken. Run it bare, or capture properly:

    python3 check_render.py > /tmp/gate.txt 2>&1; echo "exit=$?"

and quote the exit status in the round's report, not the words "all checks pass" scraped
out of the middle of the output.

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

Module 03 inherited the same inert gate and it stayed inert for that whole build too. Once
it was masking on colour it found 19px, 25px, 52px and 20px discs across five figures in
one run. The line that proves it ran is the measurement, not the verdict:

    node diameter: 26-42px (spread 1.6x) across 351 discs

Corollary: a detector needs a discriminator, not just a filter. Aspect ratio and fill ratio
alone cannot tell a 23px percolation cell or an accent-2 "o" from a small node disc —
sampling the four bounding-box corners can, because a disc has empty corners and a square
does not.

### When a later round measures a fix as absent, believe the measurement

Round 1 of Module 02 specified "re-bow the ring lattice's chords to remove the crossings"
and the round reported it landed. Round 2 measured the same figure and found **16 crossings**
on a graph `nx.check_planarity` calls planar. Both were true: what landed was a *different*
fix — deepening the bow so each triangle had a visible interior — chosen for a good reason
(the zero-crossing drawing made every triangle unreadable) that was recorded only in a
docstring inside the generator.

Two rules from that. A fixer who substitutes a different fix must say so **in the report**,
not just in a comment; and a lead who reads "landed" without a measurement has learned
nothing. The round-2 reviewer then supplied the layout that dissolved the trade-off
altogether — the graph was an antiprism, which draws planar *and* keeps its triangles — so
the recorded disagreement was what made the third option findable.

### An assertion tells you about the property it measures, and nothing else

Module 04 shipped a Blocker straight through a passing assertion, and the assertion was correct.

`make_animations.py` asserted that the GIF's node layout equalled the quiz figure's
preferential panel to 1e-9 — a guard so the animation and the still beside it could not drift
apart. It did exactly that. It also meant the "here is preferential attachment" slide drew, node
for node and ringed hub and all, the answer to the quiz two slides later. The room could answer
by matching pictures.

The withholding check that was supposed to catch this scans the figure's **banned strings**, and
round 1 certified "no leak" on its strength. A graphical leak walks through a textual assertion
without touching it.

Two rules out of that:

- **When an assertion passes, you have learned one fact, not a class of facts.** "Cannot drift"
  and "gives the answer away" were the same fact here, and nothing in the guard knew it.
- **Split a guard that is holding two properties at once.** The fix asserts the *graph* is
  identical (same generator, same m, same n, same edge set) and the *drawing* is not (normalised
  layouts far apart). Both halves were wanted; only their conjunction was the defect.

The same shape, from the other end, in the same deck: a node-size assertion computed
`NODE * factor` from the constant it already knew, so a figure that drew at `SMALLNODE` passed
it, and three markers shipped at 25.5px against a 26px floor. One guaranteed a real property of
the drawing and was blind to what it implied; the other guaranteed the author's intention and was
blind to the drawing.

### The ground-truth side of an assertion must be able to be wrong on its own

Module 04 shipped one defect through five rounds of review, and the thing that kept it alive was an
assertion whose job was to catch it. A figure drawing eight people coloured by whether their friends
have more friends than they do asserted:

    rel = 1 if friend_mean(g) > degree(g) else -1 if ... else 0     # derived from the data
    assert rel == {"accenttwo": 1, "accent": -1, "annot": 0}[fill]  # written two lines above

The data was right. The comparison was right. The **map from comparison to colour was inverted**,
and it sat inside the thing whose job was to catch inversions. The assertion passed every round and
reported the polarity verified.

"Do not assert against literals" is the wrong lesson — it would ban a lot of good assertions. The
invariant is structural:

> **The side of an assertion you are treating as ground truth must come from somewhere that can be
> wrong independently of the code under test.**

A dict written two lines above the thing it checks cannot be. Swap which side is derived and the
same line becomes a real test. In practice that means the expected side comes from a shared module,
a measurement of the render, or the source data — not from a constant the author wrote while writing
the thing it guards.

The corollary the same module paid for four times: **a shared constant binds only where someone
remembers to reach for it; a shared builder binds everywhere it is called.** Round 4 fixed an axis
mismatch by importing two constants, and the half of the axis those constants did not cover stayed
wrong. Round 5 fixed it by calling the shared axis *builder*. Same for the colour roles — declaring
them bound the two functions that were named, and the two that were not kept calling the primitive
directly.

### A green build line is not evidence about the file on disk

Late in module 04 a figure agent edited a generator, rebuilt, read `1 figures written, 0 failed`,
opened the PNG — and it was the previous image. It knew, because the drawing on screen could not
have passed the assertion the build had just reported passing, so it measured the file:

    accent-2 101536 px, accent 45423 px    <- on disk after a "successful" build
    accent-2  45409 px, accent     0 px    <- after rm + rebuild

The likely mechanism is mundane and worth naming: this build had, more than once, **two
`make_figures.py` processes writing into the same directory at the same time**, one of them from a
session nobody had thought to hold. A process reports success for the write it performed; the bytes
that survive can be the other one's.

The guard is cheap: **delete a figure's PNG before regenerating it.** Then "did it actually write"
cannot be answered by accident — if the file is absent and the build is green, the file on disk is
the file the code describes.

This is the render-staleness failure one level down. There, the render was stale relative to the
figures. Here, the figure was stale relative to its own generator, and nothing in the output said so.

### Assert on the numbers that describe the canvas, not the numbers that describe the content

Module 04 spent three rounds refining one rule, and this is where it ended up.

Round 3: **assert on the coordinates actually drawn.** A clearance gate passed at 46bp in a
canonical box, the layout was then scaled by 0.873 into a narrower panel, and six discs fused at
40.1bp against 40bp discs.

Round 4 found the narrower and more useful version. A figure teaching that a CCDF's slope is one
less than a PDF's drew the two panels at **0.4099 and 0.3915** — 4.5% apart, where the claim is 2.5
against 1.5 — because the panels spent six and four decades in boxes of identical height, so the
change of ruler cancelled the change of slope. The guard meant to catch it fit `xs ** -g` against
`xs ** -(g-1)` and asserted they differed by one: arithmetic on arrays the author had constructed.

What found it was **bp per decade, measured off the box dimensions** — the only quantity in that
figure that neither the data nor the author's intention can reach.

> A slope is content. Bp per decade is canvas. Assert the canvas.

The same test retires a whole family: a label's position is content, its ink box is canvas; a
node's degree is content, its drawn diameter is canvas; "the two states differ by one line" is
content, "the two PNGs are pixel-identical above row 313" is canvas.

### A gate is blind to whatever the drawing primitives do not tell it about

Three of module 04's gate gaps were the same gap. The collision gate could not see a **fill**,
because `fill_poly` reported nothing. It could not see a **frame border**, because a rectangle is
one TikZ path and the gate only knew `seg()`. And the node-size gate could not see a **gray or
hollow disc**, because `NODE_FILLS` listed two colours.

Each was found by a reviewer measuring the render, months of rounds apart, and each was one line to
close once someone looked at the primitive rather than at the check. So when a gate passes on a
figure you can see is wrong, ask what the drawing *told* it — not what it examined.

The corollary bites: **a private helper that bypasses the shared primitive is a hole in every gate
built on it.** `figs_story.py` kept its own `rect()` after `figlib`'s learned to record, so the
frame blockers were live and that file's frames were still invisible.

### A mechanical edit must assert that it matched

A fixer applying twenty wording changes reaches for `str.replace`, and a `str.replace` whose
pattern was never in the file returns the file unchanged and reports success. That is
indistinguishable from a landed fix, and it is one of the ways this project has twice reported a
repair the render contradicted.

Module 04's deck agent ran its edits as one script that **asserts each pattern matched exactly
once** and aborts otherwise, printing "all 23 replacements applied, each matched exactly once".
Exactly once, not at least once: a pattern that matches twice has found something the author did
not know was there, which is worth stopping for.

### An assertion that is never called is not a check

`assert_planar()` sat in Module 02's generator with a docstring reading "a figure whose claim
is 'count the triangles' must not draw phantom ones", wired into exactly one figure. The
figure that shipped 34 crossings under a caption asserting there were none was not one of
them. Grep for every guard the codebase defines and check where it is *called*, not where it
is defined.

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

### A patch that reports success but never matched looks exactly like a landed fix

Applying fixes with a scripted `str.replace` is fast and it fails silently: if the search
string is off by one escaped backslash, the script prints "patched", exits 0, and changes
nothing. Module 05 lost a round that way — the "draw two balls" figure was reported fixed,
the build was green, and the render still showed five overlapping discs.

Two defences, both cheap. Make the replacement **assert** it matched (`assert old in s`)
rather than trusting `str.replace` to no-op quietly; and re-read the rendered slide before
reporting, which is the rule below and is the one that actually caught it.

### ### A scripted replacement can eat the fix you just applied

Two edits in one script, both matching on the same URL: the first inserted a link on the
slide, the second rewrote "the URL in the speaker note" — and hit the copy inside the link
it had just created, producing `href="https://The link is on the slide..."`. The script
printed success. Order the replacements so later patterns cannot match earlier insertions,
or make each one match on enough surrounding context to be unambiguous — and then grep the
export for what you claimed to add.

### ### After changing a figure, check every slide that uses it — and every claim about it

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

### If a subagent review does not arrive, say so in the report

Four reviewers were launched for m03 round 1 and none returned. The rounds that followed
were driven by the checker plus a single read, which is weaker coverage than this playbook
intends. Record that in the fix spec rather than letting the round read as a full pass —
the next person needs to know which slides no one looked at.

### Give a fix agent the container list, not the intention

Three figure agents were briefed from the figure spec while the deck was still
being written. Each was told a container per figure; the deck then put several of
them somewhere else, and the build gate failed twenty figures for scale. The brief
was not wrong when it was written — it was written too early.

Dispatch figure work **after** the slide that uses it exists, and paste the
container for each figure into the brief as a list. Ask the agent to report the
emitted line for every figure (`name  WxH bp  node NNpx  x-h NN.Npx  [container]`)
rather than "done": that line is the only evidence that the figure is the size the
deck needs, and it costs the agent nothing to paste.

### A missing figure must fail the gate, not crash it

`check_render.py` opened every figure the deck references and died with a
traceback on the first one that did not exist, which reads as "the checker is
broken" rather than "the deck references a file nobody generated". While a deck is
mid-build that is the normal state and the gate has to survive it: report the
missing file as a failure and carry on, so one run tells you about all of them.

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
