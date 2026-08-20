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

## What counts as filler

Each rule below is a cut the lecturer made on the m01 deck himself.

**1. A tail that restates the sentence it hangs off.** Usually after an em-dash.

> Euler asked the same question. His answer: keep only what connects to what — geography,
> distance, shape, all gone.

→ *Euler answered: keep only what connects to what.*

**2. Emphasis that carries no fact.** "nothing more, nothing less", "in full",
"one last time", "Everything you need is still there", "if you got that far".

> Count every edge touching the node — nothing more, nothing less.

→ *Count every edge touching the node.*

**3. Repetition for rhythm.** The triad, the anaphora, the list of things being erased.

> Four landmasses. Four dots. A landmass's size, its shape, its area — all gone. Only a
> bare label remains.

→ *Four landmasses and dots. Only a label remains.*

**4. Narration of work the students already did.** Keep the pointer — `Question 3`,
`Question 5(a)` — cut the retelling of what they wrote and how it felt.

> Question 1 gave you two bridges between the same two cities, and the lab made you write
> that pair down **twice**. Both bridges count — merge them and you are solving a
> different puzzle with a different answer.
> * A pair that repeats is a **multi-edge**.
> * A graph that allows them is a **multigraph**.
> * Königsberg is one, twice over — which is why the doubling had to survive the abstraction.

→ *· **multi-edge**: multiple edges running between the same pair*
  *· **multigraph**: a graph with multi-edges*

**5. A body line that repeats the slide title.** The title already asked it.

> ## Which two bridges would you destroy?
> You want to make the walk possible. Which two bridges do you remove?

→ the second question goes; the title keeps it.

**6. A part-divider subtitle that asserts the punchline** instead of naming the part's
subject. `Parity is the whole argument` → cut. A subtitle that says what the part covers
stays.

**7. Announcing an object instead of naming it.**

> Every bridge becomes a line joining two dots — a new object: a **graph**.

→ *Every bridge becomes a line joining two dots: a **graph**.*

**8. Bridging sentences.** "You've just seen what one entry of $A^2$ counts." The previous
slide is still in the room's head; the transition is the lecturer's job, not the slide's.

## What is not filler

Do not cut these while you are in cutting mood:

- **Interaction cues** — *Turn to your neighbor — 30 seconds.* They are the use model
  (`SLIDE_RUBRIC.md`), not decoration.
- **figcaptions**, which by rule say what nothing else on the slide says.
- **Any clause carrying a fact, a cause, or a number**, however ornamental it sounds.
  "The 200-year impossible walk becomes possible — by accident of war" says *why*: keep it.
- **Cross-references that do work** — "Traversal is cheap, which is what the component
  sweep needed" tells the room where they met it.
- **A stated implication** — "never the same node twice — and so never the same edge
  either" is a second claim, not a restatement.

## How to run it

1. Top to bottom in the source, one slide at a time. For each sentence: *does deleting
   it remove a fact, a cause, a number, or an instruction?* If not, delete it.
2. Deletions and shortenings only. If you find yourself typing a new sentence, you have
   drifted into rewriting — that is a different pass, and it needs the lecturer.
3. A slide that ends up as bare bullets straight after the `<hr>` is a fine outcome.
4. **Re-render and re-run the gate.** Cutting changes slide fill: a `mid`-class slide can
   come out too empty, and any hand-edit made in the same sitting (an unbalanced `$$` will
   swallow the rest of the deck) shows up only in the render.
5. Read `git diff` before committing. Every hunk should be shorter on the right.
