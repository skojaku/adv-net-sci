/* Where a random edge lands, what that costs you, and when the search dies.
   Markup above, scenes below, and nothing in between: the paper, the pen, the
   motion and the sequencer all come from assets/anim.css + assets/anim.js, and
   everything a scene calls arrives on `ctx`. The kit is loaded after this file,
   hence the animReady queue. */
(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     Ten towns, ten cables, chosen so every number this stage prints is exact:

       degrees   5, 4, 3, 2, 1, 1, 1, 1, 1, 1      sum 20, so ten cables
       <k>       20 / 10 = 2
       <k^2>     60 / 10 = 6
       kappa     6 / 2   = 3          the mean degree of the town you LAND on
       kappa-1   2                    so the search doubles at every step
       f_c       1 - 1/2 = 0.5        half the towns, exactly

     The one cycle is four towns long, so the network has no triangle and the
     branching argument's own assumption holds on the picture it is argued over.

     The forty draws in each scene were rolled once, offline, with the seed that
     lands both running means exactly on the theory (2.00 and 3.00) while the
     hub is still visibly the most-landed-on town. Reproduce with:

       import random
       r = random.Random(1045)
       nodes = [r.randrange(10) for _ in range(40)]
       ends  = [E[r.randrange(10)][r.randrange(2)] for _ in range(40)]
     ------------------------------------------------------------------------ */

  const E = [[0, 1], [1, 3], [3, 2], [2, 0], [0, 4], [0, 5], [0, 6], [1, 7], [1, 8], [2, 9]];
  const N = 10;
  const DEG = [5, 4, 3, 2, 1, 1, 1, 1, 1, 1];
  const MEAN_K = 2, KAPPA = 3, BRANCH = KAPPA - 1, F_C = 1 - 1 / BRANCH;

  const NODE_DRAWS = [0, 6, 7, 7, 1, 7, 2, 5, 7, 7, 2, 8, 9, 2, 8, 1, 3, 0, 9, 9,
                      5, 9, 1, 5, 3, 9, 3, 1, 7, 4, 9, 1, 2, 8, 6, 9, 3, 9, 1, 2];
  const EDGE_DRAWS = [1, 0, 4, 1, 0, 1, 5, 0, 8, 5, 8, 9, 4, 0, 1, 2, 0, 7, 0, 0,
                      1, 1, 0, 8, 2, 0, 1, 0, 0, 2, 1, 9, 6, 3, 4, 3, 4, 0, 7, 5];

  /* Which cable each landing came down, so the drawing can light it up. The
     first cable in E with that town as an end is close enough for one flash. */
  const CAME_BY = EDGE_DRAWS.map((n) => E.findIndex((e) => e[0] === n || e[1] === n));

  const POS = [[110, 120], [190, 60], [190, 185], [255, 122],
               [25, 48], [20, 125], [35, 203], [150, 20], [245, 26], [130, 230]];

  /* the fan: five levels, and (kappa-1) = 2 children each */
  const LEV = 5;
  const ROW = [1, 2, 4, 8, 16];
  const ROW_Y = [16, 50, 84, 118, 152];
  const fanX = (k, i) => (ROW[k] === 1 ? 150 : 22 + (i * 256) / (ROW[k] - 1));

  /* the dial: f from 0 to 0.75 in sixteenths, so f_c = 0.5 is a detent */
  const DET = 16, DF = 0.05;
  const F_AT = (d) => d * DF;
  const CROSS = Math.round(F_C / DF);            /* the detent that IS f_c */

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Pick a town at random",
      note: "Forty towns drawn out of a hat. Their degrees average 2, the network's own mean.",
      async run(ctx) {
        ctx.build();
        ctx.panel("counts");
        ctx.caption("every town is equally likely; the count beside each one is how often it came up.");
        await ctx.draw(NODE_DRAWS, null, "node", MEAN_K, "average degree drawn");
        ctx.verdict("<span>a town picked at random</span><b>has " + MEAN_K + " cables</b>");
        await ctx.sleep(2400);
      }
    },
    {
      label: "Pick a cable, and walk to its far end",
      note: "Same forty draws, but of cables. Twice the cables, twice the chance of being landed on.",
      async run(ctx) {
        ctx.reset();
        ctx.panel("counts");
        ctx.caption("each cable is equally likely, and each of its two ends; the hub owns five of the twenty ends.");
        await ctx.draw(EDGE_DRAWS, CAME_BY, "edge", KAPPA, "average degree landed on");
        ctx.verdict("<span>the town at the far end</span><b>has " + KAPPA +
                    " cables, and this is &kappa;</b>");
        await ctx.sleep(2600);
      }
    },
    {
      label: "Subtract the way you came in",
      note: "One of the κ cables is the one you arrived on, so " + BRANCH + " lead onward. Every step doubles.",
      async run(ctx) {
        ctx.reset();
        ctx.panel("fan");
        ctx.setFan(0);
        ctx.caption("one town, then everything it reaches, then everything those reach.");
        ctx.readout('<span>&kappa; <b>' + KAPPA + "</b></span>" +
                    "<span>onward cables <b>&kappa; &minus; 1 = " + BRANCH + "</b></span>");
        if (!ctx.fast()) for (let k = 0; k <= LEV; k++) { ctx.grow(k); await ctx.sleep(620); }
        else ctx.grow(LEV);
        ctx.verdict("<span>above one, the search</span><b>never runs out of towns</b>");
        await ctx.sleep(2600);
      }
    },
    {
      label: "Now remove a fraction f",
      note: "Each onward cable survives with probability 1 − f. Branching (1 − f)(κ − 1) is the whole story.",
      async run(ctx) {
        ctx.panel("fan");
        ctx.grow(LEV);
        ctx.caption("the mark on the dial is the critical fraction " + F_C.toFixed(2) +
                    ", where the branching is exactly 1.");
        const dial = ctx.mountKnob(ctx.dial(), {
          min: 0, max: DET - 1, step: 1, value: 0,
          label: "Fraction of towns removed",
          format: (d) => "f = " + F_AT(d).toFixed(2),
          onGrab: () => ctx.pause(),
          onInput: (d) => ctx.setFan(F_AT(d))
        });
        if (ctx.fast()) { dial.set(CROSS); return; }
        dial.set(0);
        await ctx.sleep(1100);
        for (let d = 1; d <= CROSS + 3; d++) { dial.set(d); await ctx.sleep(560); }
        await ctx.sleep(900);
        dial.set(CROSS);
        await ctx.sleep(3000);
      }
    }
  ];

  mountScenes(document.getElementById("branch-out"), scenes, {
    stepsLabel: "Branching steps",

    helpers(ctx) {
      const netBox = ctx.$("[data-bo-net]");
      const sideBox = ctx.$("[data-bo-side]");
      const S = { nodes: [], edges: [], badges: [], count: null,
                  panel: null, fan: null, c: null };

      function drawNet() {
        netBox.textContent = "";
        const wrap = ctx.el("div", "bo-net");
        const svg = ctx.svgRoot("0 0 300 250");
        const gEdge = svg.appendChild(ctx.svgEl("g"));
        const gNode = svg.appendChild(ctx.svgEl("g"));
        const gBadge = svg.appendChild(ctx.svgEl("g"));
        const slow = !ctx.fast();

        S.edges = E.map((e, i) => {
          const a = POS[e[0]], b = POS[e[1]];
          const ln = ctx.svgEl("path", {
            d: "M " + a[0] + " " + a[1] + " L " + b[0] + " " + b[1],
            "class": "anim-edge" + (slow ? " anim-draw" : "")
          });
          if (slow) {
            ln.style.setProperty("--dash", Math.ceil(Math.hypot(a[0] - b[0], a[1] - b[1])) + 2);
            ln.style.animationDelay = (0.15 + i * 0.05) + "s";
          }
          return gEdge.appendChild(ln);
        });

        S.nodes = [];
        S.badges = [];
        POS.forEach((p, i) => {
          const c = ctx.svgEl("circle", { cx: p[0], cy: p[1], r: 16, "class": "anim-node" });
          S.nodes.push(gNode.appendChild(c));
          const t = ctx.svgEl("text", {
            x: p[0], y: p[1] + 5.4, "class": "bo-deg", "text-anchor": "middle"
          });
          t.textContent = String(DEG[i]);
          gNode.appendChild(t);
          /* the count sits outside the disc, on the side away from the middle */
          const ox = p[0] < 150 ? -24 : 24;
          const b = ctx.svgEl("text", {
            x: p[0] + ox, y: p[1] + 5, "class": "bo-badge",
            "text-anchor": p[0] < 150 ? "end" : "start"
          });
          S.badges.push(gBadge.appendChild(b));
        });
        wrap.appendChild(svg);
        netBox.appendChild(wrap);
        S.count = new Array(N).fill(0);
      }

      function drawSide() {
        sideBox.textContent = "";
        S.panel = sideBox.appendChild(ctx.el("div", "bo-panel"));
        const readSlot = ctx.el("div", "anim-readout bo-read");
        const dialSlot = ctx.el("div", "anim-range");
        const cap = ctx.el("div", "anim-caption bo-cap");
        const verdict = ctx.el("div", "anim-tally bo-verdict");
        sideBox.appendChild(readSlot);
        sideBox.appendChild(dialSlot);
        sideBox.appendChild(cap);
        sideBox.appendChild(verdict);
        S.c = { readSlot, dialSlot, cap, verdict };
      }

      function build() { drawNet(); drawSide(); }

      function reset() {
        S.count = new Array(N).fill(0);
        S.badges.forEach((b) => { b.textContent = ""; });
        S.nodes.forEach((n) => n.setAttribute("class", "anim-node"));
        S.edges.forEach((e) => e.setAttribute("class", "anim-edge"));
      }

      /* Scenes 1-2 fill the side panel with the running tally; 3-4 with the fan.
         One slot, so the two never fight for the same pixels. */
      function panel(kind) {
        S.panel.textContent = "";
        S.panel.setAttribute("class", "bo-panel bo-panel--" + kind);
        if (kind !== "fan") { S.fan = null; return; }
        const svg = ctx.svgRoot("0 0 300 170");
        const gEdge = svg.appendChild(ctx.svgEl("g"));
        const gDot = svg.appendChild(ctx.svgEl("g"));
        const gNum = svg.appendChild(ctx.svgEl("g"));
        const rows = [];
        for (let k = 0; k < LEV; k++) {
          const dots = [];
          for (let i = 0; i < ROW[k]; i++) {
            dots.push(gDot.appendChild(ctx.svgEl("circle", {
              cx: fanX(k, i), cy: ROW_Y[k], r: k > 2 ? 4.4 : 6.4, "class": "bo-dead"
            })));
          }
          const num = gNum.appendChild(ctx.svgEl("text", {
            x: 296, y: ROW_Y[k] + 4, "class": "bo-count", "text-anchor": "end"
          }));
          rows.push({ dots, num, links: [] });
        }
        for (let k = 0; k + 1 < LEV; k++) {
          for (let i = 0; i < ROW[k + 1]; i++) {
            const par = i >> 1;
            rows[k + 1].links.push(gEdge.appendChild(ctx.svgEl("path", {
              d: "M " + fanX(k, par) + " " + ROW_Y[k] + " L " + fanX(k + 1, i) + " " + ROW_Y[k + 1],
              "class": "bo-link-dead"
            })));
          }
        }
        S.panel.appendChild(svg);
        S.fan = { rows, shown: -1, f: 0 };
      }

      /* How many levels are drawn at all (scene 3 grows them one at a time). */
      function grow(k) { if (S.fan) { S.fan.shown = k; paint(); } }

      /* One dial setting. The dots that survive at level k are the first
         round(b^k) of them, b = (1-f)(kappa-1); the exact expectation is
         printed beside the row, because after two levels it stops being a
         whole number and the row alone would lie about it. */
      function setFan(f) { if (S.fan) { S.fan.f = f; paint(); } }

      function paint() {
        const { rows, shown, f } = S.fan;
        const b = (1 - f) * BRANCH;
        /* The survivors are taken from the MIDDLE of each row, not the front:
           the first-k version left the whole surviving branch pinned to the
           left edge of the drawing with the dead fan hanging off it, and at
           branching 1 the picture read as a margin rather than as a search. */
        const live = [];
        let dead = false;
        for (let k = 0; k < LEV; k++) {
          const exp = Math.pow(b, k);
          const n = k > shown ? 0 : (dead ? 0 : Math.min(ROW[k], Math.round(exp)));
          if (n === 0 && k <= shown) dead = true;
          const from = Math.floor((ROW[k] - n) / 2);
          live.push({ exp, n, from, to: from + n });
        }
        for (let k = 0; k < LEV; k++) {
          const L = live[k];
          const on = (i) => i >= L.from && i < L.to;
          rows[k].dots.forEach((d, i) => {
            d.setAttribute("class", k > shown ? "bo-hidden" : on(i) ? "bo-live" : "bo-dead");
          });
          rows[k].links.forEach((l, i) => {
            const up = live[k - 1];
            const alive = on(i) && (i >> 1) >= up.from && (i >> 1) < up.to;
            l.setAttribute("class", k > shown ? "bo-hidden"
              : alive ? "bo-link-live" : "bo-link-dead");
          });
          rows[k].num.textContent = k > shown ? ""
            : (L.exp >= 10 ? L.exp.toFixed(0)
                           : L.exp.toFixed(L.exp === Math.round(L.exp) ? 0 : 2));
          rows[k].num.setAttribute("class", "bo-count" + (L.n ? "" : " bo-count-dead"));
        }
        if (shown >= 0) {
          S.c.readSlot.innerHTML =
            "<span>f <b>" + f.toFixed(2) + "</b></span>" +
            "<span>1 &minus; f <b>" + (1 - f).toFixed(2) + "</b></span>" +
            '<span style="color:var(--_amber)">branching <b>' + b.toFixed(2) + "</b></span>";
          S.c.verdict.innerHTML = b > 1.001
            ? "<span>branching above 1</span><b>the search never dies</b>"
            : b < 0.999
              ? "<span>branching below 1</span><b>the search dies out</b>"
              : "<span>branching exactly 1</span><b>f<sub>c</sub> = " + F_C.toFixed(2) + "</b>";
        }
      }

      function readout(html) { S.c.readSlot.innerHTML = html; }
      function caption(t) { S.c.cap.textContent = t; }
      function verdict(html) { S.c.verdict.innerHTML = html; }
      function dial() {
        S.c.dialSlot.textContent = "";
        const track = ctx.el("div", "anim-track");
        const tick = ctx.el("div", "bo-tick");
        tick.style.left = (100 * CROSS / (DET - 1)) + "%";
        track.appendChild(tick);
        const knob = ctx.el("div", "anim-knob");
        track.appendChild(knob);
        S.c.dialSlot.appendChild(track);
        return knob;
      }

      /* Forty draws, one at a time, with the count beside each town and the
         running mean in the readout. `by` lights the cable a landing came down;
         for the plain node draw there is none. */
      async function draw(seq, by, kind, exact, label) {
        S.panel.textContent = "";
        const big = S.panel.appendChild(ctx.el("div", "bo-big"));
        big.innerHTML = '<span class="bo-big-n" data-m>&mdash;</span>' +
                        '<span class="bo-big-l">' + label + "</span>";
        const outM = big.querySelector("[data-m]");
        const tail = S.panel.appendChild(ctx.el("div", "bo-tail"));
        let sum = 0;
        const n = ctx.fast() ? seq.length : seq.length;
        for (let i = 0; i < n; i++) {
          const v = seq[i];
          sum += DEG[v];
          S.count[v]++;
          S.badges[v].textContent = String(S.count[v]);
          outM.textContent = (sum / (i + 1)).toFixed(2);
          if (!ctx.fast()) {
            tail.textContent = "degree " + DEG[v] + ", draw " + (i + 1) + " of " + seq.length;
            S.nodes[v].setAttribute("class", "bo-hit");
            if (by) S.edges[by[i]].setAttribute("class", "anim-edge bo-along");
            await ctx.sleep(i < 8 ? 420 : i < 20 ? 170 : 80);
            S.nodes[v].setAttribute("class", "anim-node");
            if (by) S.edges[by[i]].setAttribute("class", "anim-edge");
          }
        }
        outM.textContent = exact.toFixed(2);
        tail.textContent = "forty draws, " + (kind === "node" ? "one town each" : "one cable end each");
      }

      return { build, reset, panel, grow, setFan, readout, caption, verdict, dial, draw };
    }
  });
});
