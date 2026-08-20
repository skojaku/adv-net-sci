/* ==========================================================================
   anim.js — the scene sequencer behind every hand-drawn animation.

   Plain classic script. No module, no bundler, no network. Pair it with
   assets/anim.css.

   ---------------------------------------------------------------- markup ---
   Everything is found *inside* the root you hand to mountScenes, by data
   attribute. Nothing is looked up on `document`, so any number of stages can
   share one page without driving each other.

     <figure class="anim-stage">
       <div class="anim-bar">
         <div class="anim-step" data-anim-step></div>
         <div class="anim-dots" data-anim-dots></div>
         <button class="anim-btn" type="button" data-anim-prev>&#9664;</button>
         <button class="anim-btn" type="button" data-anim-play></button>
         <button class="anim-btn" type="button" data-anim-next>&#9654;</button>
         <button class="anim-btn" type="button" data-anim-replay>Replay</button>
       </div>
       <div class="anim-grid-2" data-anim-canvas>
         <div data-anim-clear data-anim-scroll></div>
       </div>
       <figcaption class="anim-note" data-anim-note></figcaption>
     </figure>

     data-anim-canvas  the drawing. Gets aria-hidden; the note speaks for it.
     data-anim-clear   emptied before every run.
     data-anim-scroll  the box type() keeps scrolled to the bottom.

   ------------------------------------------------------------------ boot ---
   The page's own script may run before or after this file, so queue it:

     (window.animReady = window.animReady || []).push(function () {
       mountScenes(document.currentScript.parentNode, scenes, opts);
     });

   ----------------------------------------------------------------- scenes ---
   scenes: [{ label, note, async run(ctx) }]

   ctx carries everything a scene needs, so a scene array is scenes and
   nothing else:
     ctx.el(tag, cls, html)          ctx.svgRoot(viewBox, cls)
     ctx.svgEl(tag, attrs)           ctx.attr(node, attrs)
     await ctx.sleep(ms)             await ctx.type(node, text, speed)
     ctx.bottom(box)                 ctx.$(sel) / ctx.$$(sel)   (scoped)
     ctx.fast()                      true while skipping to a step
     ctx.reduced                     the reader asked for no motion
     ctx.pause() / ctx.resume() / ctx.go(i)
   plus whatever opts.helpers(ctx) returns.

   opts: { helpers, clear, loop, endPause, autoplay, stepsLabel, threshold }
   ========================================================================== */

(function () {
  "use strict";

  var SVG_NS = "http://www.w3.org/2000/svg";
  var ABORT = (typeof Symbol === "function") ? Symbol("abort") : "__anim_abort__";

  /* ---------------------------------------------------------------- builders */

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function attr(node, attrs) {
    if (attrs) {
      for (var k in attrs) {
        if (Object.prototype.hasOwnProperty.call(attrs, k) && attrs[k] != null) {
          node.setAttribute(k, attrs[k]);
        }
      }
    }
    return node;
  }

  function svgEl(tag, attrs) {
    return attr(document.createElementNS(SVG_NS, tag), attrs);
  }

  function svgRoot(viewBox, cls) {
    return svgEl("svg", {
      viewBox: viewBox,
      "class": "anim-svg" + (cls ? " " + cls : ""),
      focusable: "false"
    });
  }

  function bottom(box) {
    if (box) box.scrollTop = box.scrollHeight;
  }

  /* ------------------------------------------------------------- mountKnob */
  /* A draggable knob. Pointer, touch and keyboard all drive one set(), so the
     caption "drag it" is finally true. Give it the .anim-knob element; its
     parent is the track unless you pass one. */

  function mountKnob(knob, opts) {
    if (!knob) return null;
    var o = opts || {};
    var track = o.track || knob.parentNode;
    var min = (o.min == null) ? 0 : o.min;
    var max = (o.max == null) ? 100 : o.max;
    var step = o.step || 1;
    var value = (o.value == null) ? min : o.value;
    var dragging = false;

    knob.setAttribute("role", "slider");
    knob.setAttribute("aria-valuemin", String(min));
    knob.setAttribute("aria-valuemax", String(max));
    if (o.label) knob.setAttribute("aria-label", o.label);
    /* If the knob sits inside the aria-hidden canvas, a tabbable control there
       would be a focus trap announcing nothing. Pointer and arrow keys still
       work once it is clicked; the scene's note carries the account. */
    knob.tabIndex = knob.closest && knob.closest('[aria-hidden="true"]') ? -1 : 0;

    function snap(v) {
      v = Math.round((v - min) / step) * step + min;
      return Math.max(min, Math.min(max, v));
    }

    function render() {
      var t = (max === min) ? 0 : (value - min) / (max - min);
      knob.style.left = (t * 100) + "%";
      knob.setAttribute("aria-valuenow", String(value));
      if (o.format) knob.setAttribute("aria-valuetext", o.format(value));
    }

    function set(v, fromUser) {
      value = snap(v);
      render();
      if (o.onInput) o.onInput(value, !!fromUser);
    }

    function fromX(clientX) {
      var r = track.getBoundingClientRect();
      if (!r.width) return;
      set(min + ((clientX - r.left) / r.width) * (max - min), true);
    }

    function grab() { if (o.onGrab) o.onGrab(); }

    function down(ev) {
      dragging = true;
      knob.classList.add("anim-knob-live");
      grab();
      /* Focus even at tabindex -1: that is what makes the arrow keys live
         for a reader who reached the knob by clicking it. */
      if (knob.focus) knob.focus({ preventScroll: true });
      fromX(ev.clientX);
      ev.preventDefault();
    }
    function move(ev) {
      if (!dragging) return;
      fromX(ev.clientX);
      ev.preventDefault();
    }
    function up() {
      if (!dragging) return;
      dragging = false;
      knob.classList.remove("anim-knob-live");
    }

    track.addEventListener("pointerdown", down);
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
    window.addEventListener("pointercancel", up);

    knob.addEventListener("keydown", function (ev) {
      var k = ev.key, d = null;
      if (k === "ArrowRight" || k === "ArrowUp") d = step;
      else if (k === "ArrowLeft" || k === "ArrowDown") d = -step;
      else if (k === "PageUp") d = step * 4;
      else if (k === "PageDown") d = -step * 4;
      else if (k === "Home") d = "min";
      else if (k === "End") d = "max";
      else return;
      grab();
      set(d === "min" ? min : d === "max" ? max : value + d, true);
      ev.preventDefault();
    });

    render();

    return {
      el: knob,
      get: function () { return value; },
      set: function (v) { set(v, false); },
      destroy: function () {
        track.removeEventListener("pointerdown", down);
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", up);
        window.removeEventListener("pointercancel", up);
      }
    };
  }

  /* ----------------------------------------------------------- mountScenes */

  function mountScenes(root, scenes, opts) {
    if (typeof root === "string") root = document.querySelector(root);
    if (!root || !scenes || !scenes.length) return null;
    if (root.getAttribute("data-anim-mounted")) return null;
    root.setAttribute("data-anim-mounted", "1");

    var o = opts || {};
    var loop = o.loop !== false;
    var endPause = (o.endPause == null) ? 2400 : o.endPause;

    /* Step mode: the stage never advances itself. It builds one step, stops,
       and waits for a click. A slide deck sets window.animStepOnly, because a
       lecturer drives the beats by hand; the lecture note leaves it off, where
       a reader wants the thing to play. */
    var stepOnly = (o.step == null) ? !!window.animStepOnly : !!o.step;
    if (stepOnly) loop = false;

    /* Every lookup is scoped to root. Two stages on one page stay strangers. */
    function $(sel) { return root.querySelector(sel); }
    function $$(sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }

    var stepBox = $("[data-anim-step]");
    var dotsBox = $("[data-anim-dots]");
    var noteBox = $("[data-anim-note]");
    var btnPlay = $("[data-anim-play]");
    var btnPrev = $("[data-anim-prev]");
    var btnNext = $("[data-anim-next]");
    var btnReplay = $("[data-anim-replay]");

    /* Nothing plays on its own in step mode, so the pause control would be a
       dead button. Drop it rather than leave it there to be clicked. */
    if (stepOnly && btnPlay) {
      btnPlay.parentNode.removeChild(btnPlay);
      btnPlay = null;
    }

    /* ---- ARIA, once, for every animation that uses the kit ---- */
    if (dotsBox) {
      dotsBox.setAttribute("role", "group");
      dotsBox.setAttribute("aria-label", o.stepsLabel || "Steps");
    }
    if (noteBox) {
      noteBox.setAttribute("aria-live", "polite");
      noteBox.setAttribute("aria-atomic", "true");
    }
    /* The canvas is rebuilt character by character; narrating it would be
       noise. It is hidden, and the per-scene note is the account instead. */
    $$("[data-anim-canvas]").forEach(function (c) {
      c.setAttribute("aria-hidden", "true");
    });

    var reduced = !!(window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches);

    /* ---- sequencer: abortable, pausable, fast-forwardable ---- */
    var gen = 0;          // bumped on every restart/jump; stale scenes abort
    var paused = false;   // = userPaused || offscreen
    var userPaused = false;
    var offscreen = false;
    var fast = false;     // true while fast-forwarding to a step
    var current = 0;

    function syncPause() { paused = userPaused || offscreen; }

    function sleep(ms) {
      if (fast) return Promise.resolve();
      var g = gen;
      return new Promise(function (resolve, reject) {
        var left = ms;
        var slice = 40;
        var tick = function () {
          if (g !== gen) return reject(ABORT);
          if (paused) return setTimeout(tick, 90);
          left -= slice;
          if (left <= 0) resolve(); else setTimeout(tick, slice);
        };
        setTimeout(tick, slice);
      });
    }

    async function type(target, text, speed) {
      var box = target.closest("[data-anim-scroll]");
      if (fast) {
        target.textContent = text;
        bottom(box);
        return;
      }
      var caret = el("span", "anim-caret");
      target.after(caret);
      try {
        /* Array.from, not split — one emoji is one keystroke, not two. */
        var chars = Array.from(String(text));
        for (var i = 0; i < chars.length; i++) {
          target.textContent += chars[i];
          bottom(box);
          await sleep(speed || 26);
        }
      } finally {
        caret.remove();
      }
      bottom(box);
    }

    function setPlayUI() {
      if (!btnPlay) return;
      btnPlay.textContent = userPaused ? "▶ Play" : "⏸ Pause";
      /* The visible text was the only signal of state; now it is announced. */
      btnPlay.setAttribute("aria-pressed", userPaused ? "false" : "true");
      btnPlay.setAttribute("aria-label",
        userPaused ? "Play the animation" : "Pause the animation");
    }

    /* ---- dots ---- */
    var dots = [];
    if (dotsBox) {
      scenes.forEach(function (s, i) {
        var d = el("button", "anim-dot");
        d.type = "button";
        d.title = (i + 1) + ". " + (s.label || "");
        d.setAttribute("aria-label", "Step " + (i + 1) + ": " + (s.label || ""));
        d.setAttribute("aria-current", "false");
        d.addEventListener("click", function () { go(i); });
        dotsBox.appendChild(d);
        dots.push(d);
      });
    }

    function mark(i) {
      if (stepBox) {
        stepBox.textContent = "";
        var n = el("span", "anim-num");
        n.textContent = String(i + 1);
        stepBox.appendChild(n);
        stepBox.appendChild(document.createTextNode(scenes[i].label || ""));
      }
      if (noteBox) noteBox.textContent = scenes[i].note || "";
      dots.forEach(function (d, k) {
        d.setAttribute("aria-current", k === i ? "true" : "false");
      });
    }

    /* Knobs built inside a scene are rebuilt on every loop; their window-level
       pointer listeners would pile up forever, so the kit owns their lives. */
    var knobs = [];

    function clear() {
      knobs.forEach(function (k) { k.destroy(); });
      knobs = [];
      $$("[data-anim-clear]").forEach(function (n) { n.textContent = ""; });
      if (typeof o.clear === "function") o.clear(ctx);
    }

    /* ---- the context every scene is handed ---- */
    var ctx = {
      root: root,
      $: $,
      $$: $$,
      el: el,
      attr: attr,
      svgEl: svgEl,
      svgRoot: svgRoot,
      bottom: bottom,
      sleep: sleep,
      type: type,
      mountKnob: function (knob, kopts) {
        var k = mountKnob(knob, kopts);
        if (k) knobs.push(k);
        return k;
      },
      reduced: reduced,
      fast: function () { return fast; },
      pause: function () { userPaused = true; syncPause(); setPlayUI(); },
      resume: function () { userPaused = false; syncPause(); setPlayUI(); },
      go: function (i) { go(i); }
    };

    if (typeof o.helpers === "function") {
      var extra = o.helpers(ctx) || {};
      for (var k in extra) {
        if (Object.prototype.hasOwnProperty.call(extra, k)) ctx[k] = extra[k];
      }
    }

    function play(from, stopAfter) {
      var g = ++gen;
      clear();
      return (async function () {
        try {
          for (var i = 0; i < scenes.length; i++) {
            if (g !== gen) return;
            fast = i < from;
            current = i;
            if (!fast) mark(i);
            await scenes[i].run(ctx);
            if (stopAfter != null && i >= stopAfter) {
              fast = false;
              userPaused = true;
              syncPause();
              setPlayUI();
              return;
            }
          }
          fast = false;
          if (!loop) return;
          await sleep(endPause);
          if (g === gen) play(0);
        } catch (e) {
          if (e !== ABORT) throw e;
        }
      })();
    }

    function go(i) {
      var target = Math.max(0, Math.min(scenes.length - 1, i));
      userPaused = false;
      syncPause();
      setPlayUI();
      /* In step mode the target is also the terminus: build it, then stop. */
      play(target, stepOnly ? target : null);
    }

    if (btnReplay) btnReplay.addEventListener("click", function () { go(0); });
    if (btnPrev) btnPrev.addEventListener("click", function () { go(current - 1); });
    if (btnNext) btnNext.addEventListener("click", function () { go(current + 1); });
    if (btnPlay) {
      btnPlay.addEventListener("click", function () {
        userPaused = !userPaused;
        syncPause();
        setPlayUI();
      });
    }
    setPlayUI();

    if (reduced) {
      /* No motion: build the whole thing at once and leave it there. */
      (async function () {
        var g = ++gen;
        clear();
        fast = true;
        for (var i = 0; i < scenes.length; i++) {
          if (g !== gen) return;
          await scenes[i].run(ctx);
        }
        fast = false;
        current = scenes.length - 1;
        mark(current);
        userPaused = true;
        syncPause();
        setPlayUI();
      })();
    } else if (stepOnly) {
      /* Build the first beat so the slide is never a blank stage, then wait. */
      go(0);
    } else if (o.autoplay === false) {
      mark(0);
      userPaused = true;
      syncPause();
      setPlayUI();
    } else {
      /* Idle while scrolled out of view, so nothing plays to an empty room. */
      if (window.IntersectionObserver) {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            offscreen = !en.isIntersecting;
            syncPause();
          });
        }, { threshold: (o.threshold == null ? 0.2 : o.threshold) }).observe(root);
      }
      go(0);
    }

    return {
      root: root,
      go: go,
      next: function () { go(current + 1); },
      prev: function () { go(current - 1); },
      replay: function () { go(0); },
      pause: ctx.pause,
      resume: ctx.resume,
      index: function () { return current; }
    };
  }

  /* -------------------------------------------------------------- exports */

  window.mountScenes = mountScenes;
  window.mountKnob = mountKnob;
  window.animHelpers = { el: el, attr: attr, svgEl: svgEl, svgRoot: svgRoot, bottom: bottom };

  /* Drain whatever the pages queued, then run later pushes immediately — so
     this file may be loaded before or after them. */
  var queued = window.animReady;
  window.animReady = {
    push: function (fn) {
      try { fn(); } catch (e) { console.error(e); }
    }
  };
  if (queued && queued.length) {
    for (var i = 0; i < queued.length; i++) {
      try { queued[i](); } catch (e) { console.error(e); }
    }
  }
})();
