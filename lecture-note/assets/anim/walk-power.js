/* ==========================================================================
   walk-power.js — Why a matrix power counts walks.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Mounted by slides/m01/m01-euler-tour.md. The static figure shows two routes
   landing in one cell and the formula asserts the rest. Here the routes are
   drawn one at a time while the cell counts them, the row-times-column that
   produces the number is walked term by term, and the last scene puts k on a
   knob so the room can watch the entry move.
   ========================================================================== */

(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     make_figures.py's graph5 — the same five nodes and six edges behind
     store-matrix.png, adjacency-squared.png and the CSR slider on "Store only
     the nonzeros". Its data units (0,1 · 1,1 · 0,0 · 1,0 · 0.5,-0.9) mapped
     into a 420 x 300 box by x -> 95 + 230x, y -> 160 - 115y.
     ------------------------------------------------------------------------ */
  const POS = [[95, 45], [325, 45], [95, 160], [325, 160], [210, 264]];
  const EDGES = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 4], [3, 4]];
  const R = 17;

  /* A and its powers, k = 1..5, multiplied out once with numpy and written
     down. Nothing here multiplies a matrix at page load. */
  const POW = [
    [[0, 1, 1, 0, 0], [1, 0, 1, 1, 0], [1, 1, 0, 0, 1], [0, 1, 0, 0, 1], [0, 0, 1, 1, 0]],
    [[2, 1, 1, 1, 1], [1, 3, 1, 0, 2], [1, 1, 3, 2, 0], [1, 0, 2, 2, 0], [1, 2, 0, 0, 2]],
    [[2, 4, 4, 2, 2], [4, 2, 6, 5, 1], [4, 6, 2, 1, 5], [2, 5, 1, 0, 4], [2, 1, 5, 4, 0]],
    [[8, 8, 8, 6, 6], [8, 15, 7, 3, 11], [8, 7, 15, 11, 3], [6, 3, 11, 9, 1], [6, 11, 3, 1, 9]],
    [[16, 22, 22, 14, 14], [22, 18, 34, 26, 10], [22, 34, 18, 10, 26],
     [14, 26, 10, 4, 20], [14, 10, 26, 20, 4]]
  ];

  /* The cell the whole stage watches, and the walks that land in it. Found by
     enumerating every walk of the given length from 1 to 4 — two of length
     two, exactly one of length three. Colours match the deck's own
     adjacency-squared.png: 1-2-4 red, 1-3-4 purple. */
  const CELL = [1, 4];
  const TWO = [{ p: [1, 2, 4], c: "wp-red" }, { p: [1, 3, 4], c: "wp-purple" }];
  const THREE = [{ p: [1, 0, 2, 4], c: "wp-red" }];

  /* Three walks of length two that leave node 1 and come straight back — one
     per neighbour. They are the diagonal entry (A^2)(1,1) = 3, and the reason
     the word is walks and not paths. */
  const BACK = [
    { p: [1, 0, 1], c: "wp-red" },
    { p: [1, 2, 1], c: "wp-purple" },
    { p: [1, 3, 1], c: "wp-red" }
  ];

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "One empty cell",
      note: "No single edge joins 1 to 4, so entry (1,4) is zero. Now square the matrix.",
      async run(ctx) {
        ctx.idle();
        ctx.draw();
        ctx.card("A, and one empty cell");
        ctx.matrix(1, { hi: CELL });
        await ctx.sleep(2000);
        ctx.tally("entry (1, 4) of A", "0");
        await ctx.sleep(3000);
      }
    },
    {
      label: "Two steps, two routes",
      note: "Two two-step routes from 1 to 4 — and A squared puts a 2 in that cell.",
      async run(ctx) {
        ctx.idle();
        ctx.draw();
        ctx.card("count them by hand");
        ctx.matrix(1, { hi: CELL });
        const big = ctx.big("0");
        ctx.caption("walks of length 2 from 1 to 4");
        await ctx.sleep(700);
        /* keep from the second one on: the count is two, so both routes have to
           be on the graph at the end. Letting each clear the last left the card
           saying 2 over a drawing showing 1. */
        for (let i = 0; i < TWO.length; i++) {
          await ctx.route(TWO[i], i > 0);
          big.textContent = String(i + 1);
          ctx.tally("route " + (i + 1), TWO[i].p.join(" – "));
          await ctx.sleep(900);
        }
        await ctx.sleep(500);
        ctx.matrix(2, { hi: CELL });
        await ctx.sleep(3200);
      }
    },
    {
      label: "Where the two comes from",
      note: "Row 1 against column 4: a term counts only where both factors are 1.",
      async run(ctx) {
        ctx.idle();
        ctx.draw();
        ctx.card("row 1 against column 4");
        ctx.matrix(1, { row: 1, col: 4 });
        ctx.formula("(A<sup>2</sup>)<sub>1,4</sub> &nbsp;=&nbsp; &Sigma;<sub>m</sub> &nbsp;A<sub>1,m</sub> &middot; A<sub>m,4</sub>");
        await ctx.sleep(1800);
        let sum = 0;
        for (let m = 0; m < 5; m++) {
          const a = POW[0][1][m], b = POW[0][m][4];
          sum += a * b;
          ctx.term(m, a, b, sum);
          if (a && b) await ctx.route({ p: [1, m, 4], c: m === 2 ? "wp-red" : "wp-purple" }, true);
          await ctx.sleep(700);
        }
        await ctx.sleep(3000);
      }
    },
    {
      label: "Walks, not paths",
      note: "Out and straight back is a walk too, so the diagonal of A squared is the degree.",
      async run(ctx) {
        ctx.idle();
        ctx.draw();
        ctx.card("out and straight back");
        ctx.matrix(2, { hi: [1, 1] });
        const big = ctx.big("0");
        ctx.caption("walks of length 2 from 1 back to 1");
        await ctx.sleep(700);
        /* All three stay up — one lens per neighbour is the picture of the 3. */
        for (let i = 0; i < BACK.length; i++) {
          await ctx.route(BACK[i], i > 0);
          big.textContent = String(i + 1);
          await ctx.sleep(700);
        }
        await ctx.sleep(500);
        ctx.tally("degree of node 1", "3");
        await ctx.sleep(3200);
      }
    },
    {
      label: "Turn the crank",
      note: "Drag k. The counts climb because a walk is allowed to repeat itself.",
      async run(ctx) {
        ctx.idle();
        ctx.draw();
        ctx.card("k on a knob");
        ctx.knob();
        if (ctx.fast()) return;
        await ctx.sleep(17000);
      }
    }
  ];

  mountScenes(document.getElementById("walk-power"), scenes, {
    stepsLabel: "Walk-counting steps",

    helpers(ctx) {
      const mapBox = ctx.$("[data-wp-map]");
      const side = ctx.$("[data-wp-side]");
      const S = { k: 1 };

      function ink(p, len, ms) {
        if (ctx.fast()) return p;
        p.classList.add("anim-draw");
        p.style.setProperty("--dash", Math.ceil(len) + 8);
        p.style.animationDuration = (ms / 1000) + "s";
        setTimeout(function () {
          p.classList.remove("anim-draw");
          p.style.removeProperty("--dash");
          p.style.removeProperty("animation-duration");
        }, ms + 150);
        return p;
      }

      /* ----------------------------------------------------------- the graph */
      function draw() {
        mapBox.textContent = "";
        const svg = ctx.svgRoot("0 0 420 300");
        const g = () => svg.appendChild(ctx.svgEl("g"));
        const gEdge = g(), gLeg = g(), gNode = g(), gText = g();

        EDGES.forEach(function (e) {
          gEdge.appendChild(ctx.svgEl("line", {
            x1: POS[e[0]][0], y1: POS[e[0]][1], x2: POS[e[1]][0], y2: POS[e[1]][1],
            "class": "anim-edge"
          }));
        });
        S.nodes = POS.map(function (p) {
          return gNode.appendChild(ctx.svgEl("circle",
            { cx: p[0], cy: p[1], r: R, "class": "wp-node" }));
        });
        POS.forEach(function (p, i) {
          const t = ctx.svgEl("text",
            { x: p[0], y: p[1] + 7, "text-anchor": "middle", "class": "wp-name" });
          t.textContent = String(i);
          gText.appendChild(t);
        });

        S.svg = svg;
        S.gLeg = gLeg;
        mapBox.appendChild(svg);
      }

      /* One hop of a route, bowed clear of the edge it rides on. One fixed bow
         is enough for an out-and-back too: the perpendicular flips sign when
         the endpoints swap, so the return leg mirrors the outward one and the
         pair reads as a lens instead of one invisible overstrike. */
      function hop(a, b, cls, bow) {
        const p = POS[a], q = POS[b];
        const dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy);
        const cx = (p[0] + q[0]) / 2 - (dy / L) * bow;
        const cy = (p[1] + q[1]) / 2 + (dx / L) * bow;
        const trim = (f) => {
          const ux = cx - f[0], uy = cy - f[1], m = Math.hypot(ux, uy) || 1;
          return [f[0] + (ux / m) * (R + 3), f[1] + (uy / m) * (R + 3)];
        };
        const s = trim(p), t = trim(q);
        const path = ctx.svgEl("path", {
          d: "M " + s[0] + " " + s[1] + " Q " + cx + " " + cy + " " + t[0] + " " + t[1],
          "class": "wp-leg " + cls
        });
        S.gLeg.appendChild(ink(path, L + Math.abs(bow), 340));
      }

      /* Draw a whole route, hop by hop. `keep` leaves whatever is already on
         the graph in place — scene 3 stacks its two contributing routes. */
      async function route(r, keep) {
        if (!keep) S.gLeg.textContent = "";
        for (let i = 1; i < r.p.length; i++) {
          hop(r.p[i - 1], r.p[i], r.c, 26);
          await ctx.sleep(360);
        }
      }

      /* ---------------------------------------------------------- the matrix */
      /* Five by five plus a header row and column, built as cells rather than
         drawn, so the highlighted row, column and cell are one class each. */
      function matrix(k, opts) {
        const o = opts || {};
        S.k = k;
        if (!S.mBox) return;
        const M = POW[k - 1];
        S.mBox.innerHTML = "";
        const head = (txt, cls) => {
          const c = ctx.el("i", "wp-h " + (cls || ""));
          c.textContent = txt;
          return c;
        };
        /* Superscript digits are not contiguous in Unicode, so they are a
           lookup and not arithmetic. */
        S.mBox.appendChild(head("A" + ["", "²", "³", "⁴", "⁵"][k - 1]));
        for (let j = 0; j < 5; j++) {
          S.mBox.appendChild(head(String(j), o.col === j ? "wp-h-on" : ""));
        }
        for (let i = 0; i < 5; i++) {
          S.mBox.appendChild(head(String(i), o.row === i ? "wp-h-on" : ""));
          for (let j = 0; j < 5; j++) {
            const c = ctx.el("i", "wp-c" + (M[i][j] ? " wp-on" : ""));
            if (o.row === i || o.col === j) c.className += " wp-band";
            if (o.hi && o.hi[0] === i && o.hi[1] === j) c.className += " wp-hi";
            c.textContent = String(M[i][j]);
            S.mBox.appendChild(c);
          }
        }
      }

      /* ------------------------------------------------------------ the card */
      function card(title) {
        side.textContent = "";
        S.mBox = ctx.el("div", "wp-m");
        side.appendChild(S.mBox);
        S.panel = ctx.el("div", "anim-panel anim-pop wp-card");
        if (title) S.panel.appendChild(ctx.el("div", "anim-caption", title));
        side.appendChild(S.panel);
        /* Both belong to the panel this call just replaced; a stale reference
           would append the next scene's numbers into a detached node. */
        S.sum = null;
        S.total = null;
        return S.panel;
      }
      function big(v) {
        const b = ctx.el("div", "anim-big", v);
        S.panel.appendChild(b);
        return b;
      }
      function caption(t) { S.panel.appendChild(ctx.el("div", "anim-caption", t)); }
      function tally(k, v) {
        S.panel.appendChild(ctx.el("div", "anim-tally anim-fade",
          "<span>" + k + "</span><b>" + v + "</b>"));
      }
      function quote(t) { S.panel.appendChild(ctx.el("div", "anim-quote anim-fade", t)); }
      function formula(html) {
        S.panel.appendChild(ctx.el("div", "wp-formula", html));
      }

      /* One term of the row-times-column sum, and the running total. */
      function term(m, a, b, sum) {
        if (!S.sum) {
          S.sum = ctx.el("div", "wp-terms");
          S.panel.appendChild(S.sum);
        }
        S.sum.appendChild(ctx.el("span",
          "wp-term anim-fade" + (a && b ? " wp-term-on" : ""),
          a + "&middot;" + b));
        if (!S.total) {
          S.total = ctx.el("div", "anim-tally", "<span>running sum</span><b>0</b>");
          S.panel.appendChild(S.total);
        }
        S.total.querySelector("b").textContent = String(sum);
      }

      /* -------------------------------------------------------------- the knob */
      function knob() {
        const wrap = ctx.el("div", "anim-range");
        const track = ctx.el("div", "anim-track");
        const kn = ctx.el("div", "anim-knob");
        track.appendChild(kn);
        wrap.appendChild(track);
        S.panel.appendChild(wrap);

        const read = ctx.el("div", "wp-read", "");
        S.panel.appendChild(read);

        const show = (k) => {
          matrix(k, { hi: CELL });
          const v = POW[k - 1][CELL[0]][CELL[1]];
          read.innerHTML = "<b>k = " + k + "</b> &nbsp; walks of length " + k +
            " from 1 to 4: <b>" + v + "</b>";
          S.gLeg.textContent = "";
          if (k === 2) TWO.forEach(function (r) { drawNow(r); });
          if (k === 3) THREE.forEach(function (r) { drawNow(r); });
        };
        const drawNow = (r) => {
          for (let i = 1; i < r.p.length; i++) hop(r.p[i - 1], r.p[i], r.c, 26);
        };

        ctx.mountKnob(kn, {
          min: 1, max: 5, step: 1, value: 2, track: track,
          label: "the power k",
          format: function (v) { return "k = " + v; },
          onGrab: function () { ctx.pause(); },
          onInput: function (v) { show(v); }
        });
        show(2);
      }

      function idle() { }

      return {
        draw: draw, route: route, matrix: matrix, card: card, big: big,
        caption: caption, tally: tally, quote: quote, formula: formula,
        term: term, knob: knob, idle: idle
      };
    }
  });
});
