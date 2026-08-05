# Round-11 — the lecturer's own direction

This is not a defect list. Sadamori has said how he uses these slides, and the deck is
currently built for a different use. Read this first, because it changes what "good" means
for every remaining edit:

> These are not slides for the audience to read. They are an aid for me to teach *through
> dialogue with students*. So: keep the text short, highlight what matters, lower the
> complexity of each individual slide — and get the density back by animating instead.

Everything below follows from that.

## Already done in the theme

Body type 25 → 30px, notes 23 → 27px, formula panels and figcaptions → 30px. `strong` now
renders in accent-2 red — blue is structural here (rules, part bands, list markers), so red
is the accent that reads as emphasis; gold stays auxiliary. A new `section.mid` class
vertically centres a slide whose content does not fill the frame.

## 1. Never put a paragraph below a bullet list

The room reads it *before* the bullets have been revealed, which defeats the build. Confirmed
on the render: on "Back to Königsberg" the paragraph "One condition holds, one fails…" sits
under two fragmented bullets and is legible from the first beat.

Named instances: **"Back to Königsberg"**, **"Store only the nonzeros"**, **"Total degree is
the wrong quantity"** — and sweep the whole deck for the pattern, it is not only these three.

**Fix:** move the paragraph above the list, fold it into the last bullet, or make it a
fragment itself so it arrives in sequence.

## 2. Vertically centre shallow slides

Slides whose content does not fill the frame currently hang from the rule with all the slack
below. Named: **"Euler's move — each landmass becomes a node"**, **"Euler's move — each
bridge becomes an edge"**, **"An edge to itself"**. Add `<!-- _class: mid -->` to those and to
every other slide with the same shape — most question slides qualify.

## 3. Cut the text, hard

Long text spends the room's attention budget before you have said anything. Go through every
slide and shorten.

**Telegraphic is fine.** "Arrive by one edge, leave by another. Every time you pass through a
node, you spend two edges — one in, one out." becomes "Arrive by one edge, leave by another —
two edges per visit." Fragments, no verb, no article: all acceptable where the lecturer will
say the sentence out loud anyway.

**Keep real sentences where a real explanation is needed** — the theorem statements, the
definitions students will come back to, the parts that have to survive as a reference after
the lecture. Judgment call per slide: if the line exists so a student can reconstruct the
argument later, keep it whole; if it exists to prompt the lecturer, cut it to the bone.

## 4. Mark the key terms

Bold marks a term as key and now colours it red. Check that the deck bolds *the right things*
— the terms themselves: **graph**, **node**, **edge**, **degree**, **walk**, **trail**,
**path**, **circuit**, **cycle**, **connected**, **component**, **Euler's theorem**, **CSR**.
Unbold anything bolded merely for stress, or the red loses its meaning.

## 5. In-figure text is still too small to want to read

The lecturer named these directly, and "small text makes you not want to read it" is the
point — a label below a certain size is not merely hard, it is skipped:

| slide | figure text |
|---|---|
| Eulerian path | "start" / "end" — too small to see |
| Eulerian circuit | "start = end" — hard to see |
| A tragic epilogue | "destroyed" — very small |
| Circuit | in-figure text too small |
| Can you get from any node to any other? / Components | "connected" / "not connected" — too small |

Treat these as instances of a rule, not five one-offs: **every piece of text baked into a
figure must be at least the size of the deck's body text on the slide.** Not "at least the
page number" — that floor was too low, and it is the lecturer's own judgment that these are
unreadable. That is the figure agent's work; the deck side is to check the captions do not
duplicate what the figure now says legibly.

## 6. Animation

The deck should get its density from motion, not from more text on the slide.

**Start with the Walk / Trail / Path build** — the lecturer asked for the walk to visibly
*move*. Marp's HTML output is a browser, so an SVG with SMIL animation plays: emit the route
as an animated `<path>` with a `stroke-dasharray`/`stroke-dashoffset` animation so it draws
itself along the route, one edge at a time, and loops. Inline the SVG in the slide rather
than referencing it through `<img>` if that turns out to be more reliable — verify which
works in the actual render before building all three.

Static export degrades to a frame of the animation, which is acceptable; the lecture is given
from HTML.

Sliders and other interactivity are wanted too but need scripting, which Marp restricts.
Treat that as a follow-up: get the route animation working first and report what the render
supports.

## Standing rules — unchanged

No tables, no fenced code blocks, no inline backtick code, no `cols3`; `<div class="cols">` is
text + figure only; argument-revealing lists use `*` markers; question slides contain no
answer; exactly one plain-prose notebook pointer. `python3 check_render.py` must exit 0.
