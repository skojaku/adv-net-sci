# Stage markup for m06, ready to paste

Two stages, both mounted against `lecture-note/assets/anim.{css,js}` through
`slides/m06/network-science.css` (the per-stage rules are already at the end of that file,
scoped by `#power-step` and `#katz-dial`).

Paste each block where the spec puts it: `power-step` is slide 46 (after `decomp-power.gif`,
before `power-step1`), `katz-dial` is slide 55 (after `walks-discount.gif`, before `katz-why.gif`).

Rules that make the stage work in the export:

- The deck is rendered with `--html`, and with `--no-stdin` outside a terminal.
- Script order inside a stage block is fixed: the stage's scene file first, then `anim.js`.
  The scene file queues itself on `window.animReady`; `anim.js` drains the queue.
- `window.animStepOnly = true` must run before the first `anim.js`. It is deck-wide, so one
  copy is enough, but it is repeated in each block below so that either block pastes alone.
- Paths are relative to `slides/m06/`, where the deck lives.

## Slide 46: Power iteration (`power-step`)

````markdown
---

## Power iteration

<hr>

<figure class="anim-stage" id="power-step">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>

  <div class="anim-grid-2" data-anim-canvas>
    <div data-anim-clear data-ps-draw></div>
    <div data-anim-clear data-ps-side></div>
  </div>

  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script>window.animStepOnly = true;</script>
<script src="../../lecture-note/assets/anim/power-step.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Press the right arrow once per step. Each press applies x <- A x once and divides by the largest entry; the disc shade and the printed number are the entry.

Step 0: every node holds 1. Step 1: every node now holds its degree (A 4, D 3, F 3, G 3, B 2, E 2, C 1), divided by 4, so A is 1.00 and C is 0.25. So degree is the first guess, and each further step looks one step farther. Step 2: B has caught up with D (both 0.64) and F, G pull ahead of both (0.82). Step 3: G passes F; B and D are still exactly tied (0.625). Step 4: B passes D (0.63 against 0.59) and stays ahead; the order is now fixed. B has two neighbours and D has three, but B's two neighbours (A and G) are the strongest nodes. D's third neighbour is the leaf C. From step 4 the order A G F B D E C no longer changes; steps 5 to 8 only move the second decimal. Step 30 (the last dot): nothing moves; these seven numbers are the eigenvector of the largest eigenvalue, 2.884, with its largest entry set to 1.

Ask before step 3: which of B and D will end up higher? Most of the room says D (three neighbours).
-->
````

## Slide 55: Turn the dial (`katz-dial`)

````markdown
---

## Turn the dial

<hr>

<figure class="anim-stage" id="katz-dial">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>

  <div class="anim-grid-2" data-anim-canvas>
    <div data-anim-clear data-kd-draw></div>
    <div data-anim-clear data-kd-side></div>
  </div>

  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script>window.animStepOnly = true;</script>
<script src="../../lecture-note/assets/anim/katz-dial.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Four cliques, 4, 4, 4 and 6, joined in a ring; the six is the dashed circle. Shade = Katz score divided by the largest score.

First click shows alpha = 0: only the baseline counts, every node scores 1, and the big clique holds 6 of 18 = 33% of the total. The second click puts the dial at 0.5 / lambda_max; drag it. The red tick is 1/lambda_max, with lambda_max = 5.084 for this graph. As alpha rises the big clique's share climbs: 40% at 0.5, 63% at 0.9, 81% at 0.99. Walks of every length count, discounted by alpha per step, and the big clique has the most walks. At the tick the series 1 + alpha A + alpha^2 A^2 + ... stops converging and the scores blow up. Past the tick the formula still returns numbers, but many are negative (gold) and they mean nothing. Ask: what did alpha = 0 give, and what does the dial look like as alpha goes to 1/lambda_max? It approaches the eigenvector, which is the previous slides' localization.
-->
````
