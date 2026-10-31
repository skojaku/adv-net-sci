# The filler pass

A finished deck is not a tight deck. This is the second stage: one pass over a
**complete, gate-green** deck whose only job is to delete padding. Nothing is added,
nothing is restructured, nothing is reworded for taste.

## Why it is a separate stage

While drafting you are chasing coverage and the argument, and the padding helps you get
there — a restatement is how you check you meant it, a triad is how you feel the rhythm
of a beat. Cut it as you write and you cut content with it, because at that moment you
cannot tell scaffolding from load-bearing wall. Once every slide exists and the gate is
green, the two are easy to tell apart, and the deletion is mechanical.

So: **build, gate, review, ship-ready — then filler pass.** Never interleave them.

Run it as an explicit, announced stage. If the user asks to "tighten", "cut the padding",
"remove the filler", or 埋め草を消す, this is the pass they mean — not a rewrite.

## What counts as filler

**1. A tail that restates the sentence it hangs off.** Usually after an em-dash.

> She asked the same question. Her answer: keep only what connects to what — geography,
> distance, shape, all gone.

→ *Her answer: keep only what connects to what.*

**2. Emphasis that carries no fact.** "nothing more, nothing less", "in full",
"one last time", "Everything you need is still there", "if you got that far".

> Count every request that reaches the queue — nothing more, nothing less.

→ *Count every request that reaches the queue.*

**3. Repetition for rhythm.** The triad, the anaphora, the list of things being erased.

> Four regions. Four dots. A region's size, its shape, its area — all gone. Only a bare
> label remains.

→ *Four regions and dots. Only a label remains.*

**4. Narration of work the audience already did.** Keep the pointer — `Exercise 3`,
`the worksheet's Q5(a)` — cut the retelling of what they wrote and how it felt.

> Exercise 1 gave you two links between the same pair, and the worksheet made you write
> that pair down **twice**. Both count — merge them and you are answering a different
> question with a different answer.
> * A pair that repeats is a **multi-edge**.
> * A structure that allows them is a **multigraph**.
> * This example is one, twice over — which is why the doubling had to survive.

→ *· **multi-edge**: multiple links running between the same pair*
  *· **multigraph**: a structure with multi-edges*

**5. A body line that repeats the slide title.** The title already asked it.

> ## Which two would you remove?
> You want to make it possible. Which two do you remove?

→ the second question goes; the title keeps it.

**6. A section-divider subtitle that asserts the punchline** instead of naming the
section's subject. `Parity is the whole argument` → cut. A subtitle that says what the
section covers stays.

**7. Announcing an object instead of naming it.**

> Every link becomes a line joining two dots — a new object: a **graph**.

→ *Every link becomes a line joining two dots: a **graph**.*

**8. Bridging sentences.** "You've just seen what one entry of $A^2$ counts." The previous
slide is still in the room's head; the transition is the presenter's job, not the slide's.

## What is not filler

Do not cut these while you are in cutting mood:

- **Interaction cues** — the near-white `.cue` (*Take a minute.*), the instruction of a test
  to the room (*Count your A's.*). They are the use model (`SLIDE_RUBRIC.md` N4), not
  decoration. (Whether a prompt earns its place at all is a build decision, `DECK_BUILD_GUIDE.md`,
  not the filler pass's.)
- **figcaptions**, which by rule say what nothing else on the slide says.
- **Any clause carrying a fact, a cause, or a number**, however ornamental it sounds.
  "The 200-year impossible walk becomes possible — by accident of war" says *why*: keep it.
- **Cross-references that do work** — "Traversal is cheap, which is what the sweep on
  slide 31 needed" tells the room where they met it.
- **A stated implication** — "never the same node twice — and so never the same edge
  either" is a second claim, not a restatement.

## The diction pass is a different pass

Deleting padding is not the same job as fixing the register. A metaphorical verb, an
"A, not B" antithesis and an em-dash all survive a filler pass untouched, because removing
any of them means typing a new sentence — which rule 2 below forbids. Those are
`SLIDE_RUBRIC.md` **N7 and N8**, and they run as their own top-to-bottom sweep after this
one, with the same re-render and re-gate at the end.

## How to run it

1. Top to bottom in the source, one slide at a time. For each sentence: *does deleting
   it remove a fact, a cause, a number, or an instruction?* If not, delete it.
2. Deletions and shortenings only. If you find yourself typing a new sentence, you have
   drifted into rewriting — that is a different pass, and it needs the author.
3. A slide that ends up as a title over its figure, with no other text, is a fine outcome.
4. **Re-render and re-gate** (`python3 -m gatelib review <deck_dir>`). Cutting changes
   slide fill: a `mid`-class slide can come out too empty, and any hand-edit made in the
   same sitting (an unbalanced `$$` will swallow the rest of the deck) shows up only in
   the render.
5. Read `git diff` before committing. Every hunk should be shorter on the right.
