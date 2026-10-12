/* ==========================================================================
   power-step.js — Power iteration, one press of the button at a time.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Mounted by slides/m06/m06-centrality.md ("Power iteration"). The slide
   before it shows A^t = sum_k lambda_k^t u_k u_k^T and says the largest circle
   wins. Here the room presses a button, applies x <- A x once, divides by the
   largest entry, and watches the seven discs settle into the eigenvector.

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

  /* One line per step, at most 80 characters: what changed, and nothing the
     drawing already says. The prose goes in the slide's speaker notes.
     B and D are ringed while they are the story (they tie at t = 2 and 3, and
     B passes D at t = 4). */
  const STEPS = [
    { t: 0, note: "x: one score per node. Start: every node holds 1" },
    { t: 1, note: "step 1: x = A\u00B71, every node holds its degree (\u00F7 4)" },
    { t: 2, note: "B has caught up with D; F and G pull ahead of both", ring: ["B", "D"] },
    { t: 3, note: "G passes F; B and D are still tied", ring: ["B", "D"] },
    { t: 4, note: "B passes D: the order A G F B D E C is fixed from here", ring: ["B", "D"] },
    { t: 5, note: "same order; only the second decimal moves" },
    { t: 6, note: "D goes from 0.60 to 0.58; the order stays" },
    { t: 7, note: "D is back at 0.59; the order stays" },
    { t: 8, note: "D at 0.58 again; no node changes rank" },
    { t: 30, note: "converged: eigenvector centrality. B (2 neighbours) ends above D (3)",
      label: "converged", ring: ["B", "D"] }
  ];

  /* ------------------------------------------------------------ geometry --- */
  const W = 440, H = 345, R = 23;
  const POS = {};
  NAMES.forEach(function (n) {
    POS[n] = [62 + 88 * (XY[n][0] - 0.3), 296 - 78 * (XY[n][1] - 0.2)];
  });
  /* Where each printed value sits relative to its disc (28 px type), picked so that
     no label lies on an edge or outside the frame. */
  const OFF = {
    A: [-60, 9], B: [-62, 9], C: [0, 56], D: [-48, 46],
    E: [58, 9], F: [58, 9], G: [0, -36]
  };

  /* white -> deck blue by the node's value. The floor keeps a score of 0.2
     visibly a disc; the ink outline keeps it a disc on white paper. */
  function blue(v) {
    const a = 0.08 + 0.92 * Math.max(0, Math.min(1, v));
    const m = (c, k) => Math.round(255 + (c - 255) * k);
    return "rgb(" + m(57, a) + "," + m(89, a) + "," + m(166, a) + ")";
  }

  /* The ranking, largest first, with "=" where two values agree to four places. */
  function ranking(x) {
    const idx = NAMES.map(function (_, i) { return i; })
      .sort(function (i, j) { return x[j] - x[i] || i - j; });
    let s = "";
    idx.forEach(function (i, k) {
      if (k) s += (x[idx[k - 1]] === x[i]) ? " = " : " ";
      s += NAMES[i];
    });
    return s;
  }

  /* --------------------------------------------------------------- scenes */
  const scenes = STEPS.map(function (S, i) {
    const prev = TRACE[i ? STEPS[i - 1].t : 0];
    return {
      label: S.label || ("step " + S.t),
      note: S.note,
      async run(ctx) {
        ctx.draw();
        ctx.show(prev, []);
        /* One beat on the old values, then the new ones fade in: the colours
           and numbers move, so the room sees what the step did. */
        if (!ctx.fast()) await ctx.sleep(80);
        ctx.show(TRACE[S.t], S.ring || []);
      }
    };
  });

  mountScenes(document.getElementById("power-step"), scenes, {
    stepsLabel: "Power iteration steps",

    helpers(ctx) {
      const drawBox = ctx.$("[data-ps-draw]");
      const sideBox = ctx.$("[data-ps-side]");
      const S = {};

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

        const panel = ctx.el("div", "anim-panel ps-card");
        panel.appendChild(ctx.el("div", "anim-caption", "ranking"));
        S.rank = ctx.el("div", "ps-rank", "");
        panel.appendChild(S.rank);
        panel.appendChild(ctx.el("div", "anim-caption",
          "x &larr; A x, then divide by the largest entry"));
        sideBox.appendChild(panel);
      }

      function show(x, ring) {
        NAMES.forEach(function (n, i) {
          S.node[n].style.fill = blue(x[i]);
          /* white lettering once the disc is dark enough to need it */
          S.name[n].style.fill = x[i] > 0.55 ? "#fff" : "#000";
          S.val[n].textContent = x[i].toFixed(2);
          S.ring[n].style.opacity = ring.indexOf(n) >= 0 ? "1" : "0";
        });
        S.rank.textContent = ranking(x);
      }

      return { draw: draw, show: show };
    }
  });
});
