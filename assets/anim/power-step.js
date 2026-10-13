/* ==========================================================================
   power-step.js — Power iteration, one press of the button at a time.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Mounted by slides/m06/m06-centrality.md ("Power iteration"). The slide
   before it shows A^t = sum_k lambda_k^t u_k u_k^T and says the largest circle
   wins. Here the room presses a button, applies x <- A x once, divides by the
   largest entry, and watches two things: the seven discs on the left settle
   into the eigenvector, and on the right one line per node (x = iteration t,
   y = that node's score) grows by one point and goes flat.

   Scenes: t = 0, 1, ..., 8, then t = 30 ("converged"). One scene per step.
   ========================================================================== */

(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     The graph is smallgraphs.EIG, laid out by smallgraphs.EIG_XY (grid units,
     y up; flipped and scaled in layout() below). The trace is
     smallgraphs.power_trace(A, 30) with A = EIG's adjacency matrix in
     EIG_ORDER = A..G: x_0 = 1, x_{t+1} = A x_t, each step divided by its
     largest entry. Rounded to four decimals, pasted for t = 0..8 and t = 30
     (30 is the eigenvector of the largest eigenvalue, 2.884, to four places;
     smallgraphs.check asserts the same). Nothing here multiplies a matrix.
     Step 1 is the degrees divided by 4: [4,2,1,3,2,3,3] / 4.
     ------------------------------------------------------------------------ */
  const NAMES = ["A", "B", "C", "D", "E", "F", "G"];
  const XY = {
    A: [2.0, 1.6], B: [1.0, 2.9], G: [2.6, 3.1], F: [3.6, 1.9],
    E: [3.2, 0.4], D: [1.6, 0.2], C: [0.3, 0.6]
  };
  const EDGES = [["A", "B"], ["A", "D"], ["A", "F"], ["A", "G"], ["B", "G"],
                 ["D", "C"], ["D", "E"], ["F", "E"], ["F", "G"]];
  const TRACE = {
    0: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    1: [1.0, 0.5, 0.25, 0.75, 0.5, 0.75, 0.75],
    2: [1.0, 0.6364, 0.2727, 0.6364, 0.5455, 0.8182, 0.8182],
    3: [1.0, 0.625, 0.2188, 0.625, 0.5, 0.8125, 0.8438],
    4: [1.0, 0.6344, 0.2151, 0.5914, 0.4946, 0.8065, 0.8387],
    5: [1.0, 0.6404, 0.206, 0.5955, 0.4869, 0.8127, 0.8502],
    6: [1.0, 0.6382, 0.2054, 0.584, 0.4858, 0.8062, 0.8463],
    7: [1.0, 0.6422, 0.2031, 0.5883, 0.4836, 0.8112, 0.8503],
    8: [1.0, 0.6398, 0.2034, 0.5832, 0.4839, 0.807, 0.8483],
    30: [1.0, 0.6413, 0.2027, 0.5845, 0.4831, 0.8088, 0.8495]
  };

  /* One line per step, at most 80 characters: what changed on the lines, and nothing
     the drawing already says. The prose goes in the slide's speaker notes.
     B and D are ringed (and their lines coloured) while they are the story: they
     tie at t = 2 and 3, and B passes D at t = 4. */
  const STEPS = [
    { t: 0, note: "one line per node; every line starts at 1" },
    { t: 1, note: "step 1: each score = degree \u00F7 4; the lines fan out" },
    { t: 2, note: "B's line rises to meet D's; F's and G's pull above", ring: ["B", "D"] },
    { t: 3, note: "G's line rises above F's; B's and D's are still tied", ring: ["B", "D"] },
    { t: 4, note: "B's line crosses D's; no other line crosses after",
      ring: ["B", "D"] },
    { t: 5, note: "no crossings; only the second decimal moves" },
    { t: 6, note: "D's line dips from 0.60 to 0.58; still no crossing" },
    { t: 7, note: "D's line is back at 0.59; still no crossing" },
    { t: 8, note: "D at 0.58 again; every line is almost flat" },
    { t: 30, note: "t = 30: flat. B (2 neighbours) ends above D (3)",
      label: "converged", ring: ["B", "D"] }
  ];

  /* ------------------------------------------------------------ geometry --- */
  const W = 440, H = 345, R = 23;
  /* The line chart (its own viewBox, same height as the graph). x: t = 0..8 at 44 px
     each, an axis break, then t = 30; y: score 0 (bottom) to 1 (top). */
  const CW = 600, CH = H, CL = 60, CT = 34, CB = 282, DX = 44, X30 = 520, XBREAK = 466;
  const PX = STEPS.map(function (S) { return S.t === 30 ? X30 : CL + DX * S.t; });
  const PY = function (v) { return CB - (CB - CT) * v; };
  const LABEL_GAP = 26;       /* least vertical distance between two end letters */
  const HOT = "#D9631E", COOL = "#1E96DC";
  const EMPH = { B: HOT, D: COOL };          /* the two lines the story is about */
  const POS = {};
  NAMES.forEach(function (n) {
    POS[n] = [62 + 88 * (XY[n][0] - 0.3), 296 - 78 * (XY[n][1] - 0.2)];
  });
  /* Where each printed value sits relative to its disc (28 px type), picked so that
     no label lies on an edge or outside the frame. */
  const OFF = {
    A: [-60, 9], B: [-62, 9], C: [0, 56], D: [36, 44],
    E: [58, 9], F: [58, 9], G: [0, -36]
  };

  /* near-paper warm grey -> saturated sky blue by the node's value (the m06 palette:
     saturation carries importance). The ink outline keeps a low score a disc. */
  function blue(v) {
    const a = 0.72 * Math.max(0, Math.min(1, v));      /* tops out below full saturation */
    const m = (lo, hi) => Math.round(lo + (hi - lo) * a);
    return "rgb(" + m(239, 30) + "," + m(235, 150) + "," + m(232, 220) + ")";
  }

  /* --------------------------------------------------------------- scenes */
  const scenes = STEPS.map(function (S, i) {
    return {
      label: S.label || ("step " + S.t),
      note: S.note,
      async run(ctx) {
        ctx.draw();
        ctx.show(Math.max(i - 1, 0), [], 1);
        /* One beat on the old values, then the new ones arrive: the colours and the
           numbers change, and each line grows by one segment. */
        if (!ctx.fast()) await ctx.sleep(80);
        ctx.show(i, S.ring || [], ctx.fast() ? 1 : 0);
        if (i > 0 && !ctx.fast()) ctx.grow(i, S.ring || []);
      }
    };
  });

  mountScenes(document.getElementById("power-step"), scenes, {
    stepsLabel: "Power iteration steps",

    helpers(ctx) {
      const drawBox = ctx.$("[data-ps-draw]");
      const sideBox = ctx.$("[data-ps-side]");
      const S = {};
      let token = 0;                            /* cancels a growth a newer step has replaced */

      function text(parent, cls, x, y, str, anchor) {
        const t = ctx.svgEl("text", { x: x, y: y, "text-anchor": anchor || "middle", "class": cls });
        t.textContent = str;
        return parent.appendChild(t);
      }

      function draw() {
        drawBox.textContent = "";
        sideBox.textContent = "";
        const svg = ctx.svgRoot("0 0 " + W + " " + H);
        const gEdge = svg.appendChild(ctx.svgEl("g"));
        const gRing = svg.appendChild(ctx.svgEl("g"));
        const gNode = svg.appendChild(ctx.svgEl("g"));
        S.node = {}; S.val = {}; S.ring = {}; S.name = {};
        EDGES.forEach(function (e) {
          gEdge.appendChild(ctx.svgEl("line", {
            x1: POS[e[0]][0], y1: POS[e[0]][1], x2: POS[e[1]][0], y2: POS[e[1]][1],
            "class": "anim-edge"
          }));
        });
        NAMES.forEach(function (n) {
          const p = POS[n];
          S.ring[n] = gRing.appendChild(ctx.svgEl("circle",
            { cx: p[0], cy: p[1], r: R + 8, "class": "ps-ring" }));
          if (EMPH[n]) S.ring[n].style.stroke = EMPH[n];     /* the ring wears its line's colour */
          S.node[n] = gNode.appendChild(ctx.svgEl("circle",
            { cx: p[0], cy: p[1], r: R, "class": "ps-node" }));
          const t = ctx.svgEl("text",
            { x: p[0], y: p[1] + 9, "text-anchor": "middle", "class": "ps-name" });
          t.textContent = n;
          S.name[n] = gNode.appendChild(t);
          S.val[n] = gNode.appendChild(ctx.svgEl("text", {
            x: p[0] + OFF[n][0], y: p[1] + OFF[n][1],
            "text-anchor": "middle", "class": "ps-val"
          }));
          S.val[n].setAttribute("data-ps-val", n);
        });
        drawBox.appendChild(svg);

        /* the line chart: axes first, then one path, end dot and end letter per node */
        const ch = ctx.svgRoot("0 0 " + CW + " " + CH, "ps-chart");
        [0, 0.5, 1].forEach(function (v) {
          ch.appendChild(ctx.svgEl("line", { x1: CL, x2: X30 + 14, y1: PY(v), y2: PY(v), "class": "ps-grid" }));
          text(ch, "ps-tick", CL - 12, PY(v) + 7, v === 0.5 ? "0.5" : String(v), "end");
        });
        ch.appendChild(ctx.svgEl("line", { x1: CL, x2: CL, y1: CT - 6, y2: CB, "class": "ps-axis" }));
        ch.appendChild(ctx.svgEl("line", { x1: CL, x2: XBREAK - 7, y1: CB, y2: CB, "class": "ps-axis" }));
        ch.appendChild(ctx.svgEl("line", { x1: XBREAK + 7, x2: X30 + 14, y1: CB, y2: CB, "class": "ps-axis" }));
        [-6, 6].forEach(function (d) {      /* the axis break: two slanted strokes */
          ch.appendChild(ctx.svgEl("line", {
            x1: XBREAK + d - 5, x2: XBREAK + d + 5, y1: CB + 9, y2: CB - 9, "class": "ps-axis"
          }));
        });
        for (let t = 0; t <= 8; t++) {
          ch.appendChild(ctx.svgEl("line", { x1: CL + DX * t, x2: CL + DX * t, y1: CB, y2: CB + 7, "class": "ps-axis" }));
          text(ch, "ps-tick", CL + DX * t, CB + 32, String(t));
        }
        ch.appendChild(ctx.svgEl("line", { x1: X30, x2: X30, y1: CB, y2: CB + 7, "class": "ps-axis" }));
        text(ch, "ps-tick", X30, CB + 32, "30");
        text(ch, "ps-cap", CL - 12, 18, "score", "start");
        text(ch, "ps-cap", (CL + X30) / 2, CH - 4, "iteration t");

        const gLine = ch.appendChild(ctx.svgEl("g"));
        const gDot = ch.appendChild(ctx.svgEl("g"));
        const gLab = ch.appendChild(ctx.svgEl("g"));
        S.line = {}; S.gap = {}; S.dot = {}; S.lab = {};
        NAMES.forEach(function (n) {
          S.line[n] = gLine.appendChild(ctx.svgEl("path", { "class": "ps-line" }));
          S.gap[n] = gLine.appendChild(ctx.svgEl("path", { "class": "ps-line ps-gap" }));
          S.dot[n] = gDot.appendChild(ctx.svgEl("circle", { r: 4.5, "class": "ps-dot" }));
          S.lab[n] = gLab.appendChild(ctx.svgEl("text", { x: 0, y: 8, "class": "ps-end" }));
          S.lab[n].textContent = n;
        });
        sideBox.appendChild(ch);
      }

      /* Spread the end letters so that none touches another: push overlapping neighbours
         apart by half the overlap each, then keep them inside the plot. */
      function spread(ys) {
        const o = ys.map(function (_, i) { return i; }).sort(function (i, j) { return ys[i] - ys[j] || i - j; });
        const y = o.map(function (i) { return ys[i]; });
        for (let k = 0; k < 80; k++) {
          for (let i = 1; i < y.length; i++) {
            const over = LABEL_GAP - (y[i] - y[i - 1]);
            if (over > 0) { y[i - 1] -= over / 2; y[i] += over / 2; }
          }
        }
        const lo = CT + 4, hi = CB - 4;
        const shift = Math.max(0, lo - y[0]) - Math.max(0, y[y.length - 1] - hi);
        const out = [];
        o.forEach(function (i, k) { out[i] = y[k] + shift; });
        return out;
      }

      /* Draw scenes 0..idx - 1 in full and scene idx at fraction f of the way from the
         previous scene's values and position. */
      function paintChart(idx, ring, f) {
        const cur = TRACE[STEPS[idx].t], prev = TRACE[STEPS[Math.max(idx - 1, 0)].t];
        const headX = PX[Math.max(idx - 1, 0)] + (PX[idx] - PX[Math.max(idx - 1, 0)]) * f;
        const ends = [];
        NAMES.forEach(function (n, i) {
          const head = prev[i] + (cur[i] - prev[i]) * f;
          const upto = Math.min(idx, 8);       /* t = 0..8 are one solid line; t = 30 is dotted on */
          let d = "";
          for (let k = 0; k < upto; k++) {
            d += (k ? "L" : "M") + PX[k] + " " + PY(TRACE[STEPS[k].t][i]) + " ";
          }
          const solidHead = idx <= 8;
          if (solidHead) d += (idx ? "L" : "M") + headX + " " + PY(head);
          else d += "L" + PX[8] + " " + PY(TRACE[8][i]);
          S.line[n].setAttribute("d", idx === 0 ? "" : d);
          S.gap[n].setAttribute("d", solidHead ? "" :
            "M" + PX[8] + " " + PY(TRACE[8][i]) + " L" + headX + " " + PY(head));
          const emph = ring.indexOf(n) >= 0 ? EMPH[n] : null;
          [S.line[n], S.gap[n]].forEach(function (p) {
            p.style.stroke = emph || "";
            p.style.opacity = emph ? "1" : "";
            p.style.strokeWidth = emph ? "4.6" : "";
          });
          S.dot[n].setAttribute("cx", headX);
          S.dot[n].setAttribute("cy", PY(head));
          S.dot[n].style.fill = emph || "";
          S.lab[n].style.fill = emph || "";
          ends.push(PY(head));
        });
        const ly = spread(ends);
        NAMES.forEach(function (n, i) {
          S.lab[n].setAttribute("x", headX + 13);
          S.lab[n].setAttribute("y", ly[i] + 8);
        });
      }

      function show(idx, ring, f) {
        const x = TRACE[STEPS[idx].t];
        NAMES.forEach(function (n, i) {
          S.node[n].style.fill = blue(x[i]);
          S.name[n].style.fill = "#30323D";
          S.val[n].textContent = x[i].toFixed(2);
          S.ring[n].style.opacity = ring.indexOf(n) >= 0 ? "1" : "0";
        });
        paintChart(idx, ring, f);
      }

      /* the new segment of every line, and the end letters, glide to their new places */
      function grow(idx, ring) {
        const my = ++token, t0 = performance.now(), ms = 450;
        (function frame(now) {
          if (my !== token) return;
          const u = Math.min(1, (now - t0) / ms);
          paintChart(idx, ring, 1 - Math.pow(1 - u, 3));
          if (u < 1) requestAnimationFrame(frame);
        })(t0);
      }

      return { draw: draw, show: show, grow: grow };
    }
  });
});
