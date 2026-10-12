---
marp: true
theme: network-science
paginate: true
math: katex
---

<!-- _class: lead -->

# Stage test

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
<script src="../../../lecture-note/assets/anim/power-step.js"></script>
<script src="../../../lecture-note/assets/anim.js"></script>

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

<script src="../../../lecture-note/assets/anim/katz-dial.js"></script>
<script src="../../../lecture-note/assets/anim.js"></script>
