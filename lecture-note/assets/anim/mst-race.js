/* Kruskal and Prim on one grid. Markup above, scenes below, and nothing in
   between: the paper, the pen, the motion and the sequencer all come from
   assets/anim.css + assets/anim.js, and everything a scene calls arrives on
   `ctx`. The kit is loaded after this file, hence the animReady queue. */
(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     Six towns and the nine surveyed cables between them. The prices are
     1 through 9, all different, so this network has exactly one minimum
     spanning tree and the two algorithms are obliged to agree on it.

     Every number this figure prints was worked out once, offline, and pasted
     in. Nothing here runs a graph algorithm at load; the only arithmetic is
     the geometry that places the labels. Reproduce with:

       import itertools
       E = [("A","B",1),("B","E",2),("A","E",3),("A","D",4),("C","F",5),
            ("B","C",6),("D","E",7),("C","E",8),("E","F",9)]
       # 55 spanning trees in all; cheapest 18, next cheapest 19 — unique MST
       # Kruskal : 1 take, 2 take, 3 SKIP (loop), 4 take, 5 take, 6 take = 18
       # Prim(A) : 1, 2, 4, 6, 5                                          = 18
       # scene 4 : A-B,B-E,A-D,C-F,E-F = 21; cut the 9 -> {A,B,D,E} | {C,F};
       #           cheapest cable across that cut is B-C = 6; 21-9+6 = 18
     ------------------------------------------------------------------------ */
  const POS = { A: [28, 40], B: [100, 22], C: [174, 42], D: [30, 118], E: [104, 88], F: [172, 120] };
  const NAME = ["A", "B", "C", "D", "E", "F"];
  const E = [["A","B",1], ["B","E",2], ["A","E",3], ["A","D",4], ["C","F",5],
             ["B","C",6], ["D","E",7], ["C","E",8], ["E","F",9]];

  /* Kruskal walks the price list. `tot` is the running bill after this line. */
  const KRUSKAL = [
    { e: 0, take: true,  tot: 1,  log: "the 1-cable A–B: take it." },
    { e: 1, take: true,  tot: 3,  log: "the 2-cable B–E: take it." },
    { e: 2, take: false, tot: 3,  log: "the 3-cable A–E: refuse it — A and E are already joined through B, so this would only close a loop." },
    { e: 3, take: true,  tot: 7,  log: "the 4-cable A–D: take it." },
    { e: 4, take: true,  tot: 12, log: "the 5-cable C–F: two towns that were both on their own. take it." },
    { e: 5, take: true,  tot: 18, log: "the 6-cable B–C: the last two towns join the rest. take it." }
  ];

  /* Prim only ever looks at cables with exactly one end inside the grid. */
  const PRIM = [
    { e: 0, tot: 1,  log: "cables out of the grid: 1, 3, 4. cheapest is the 1-cable A–B." },
    { e: 1, tot: 3,  log: "now out of the grid: 2, 3, 4, 6. take the 2-cable B–E." },
    { e: 3, tot: 7,  log: "now out of the grid: 4, 6, 7, 8, 9. take the 4-cable A–D." },
    { e: 5, tot: 13, log: "now out of the grid: 6, 8, 9. the 5-cable is cheaper — but C and F are both still outside, so it is out of reach. take the 6-cable B–C." },
    { e: 4, tot: 18, log: "C is inside now, so the 5-cable finally reaches out. take it." }
  ];

  const ALT = [0, 1, 3, 4, 8];   /* a spanning tree costing 21 */
  const ALT_TOT = 21;
  const CUT = 8;                 /* the 9-cable E–F it reached the far side by */
  const FAR = ["C", "F"];        /* the piece left holding the far side */
  const FAR_EDGE = 4;            /* C–F, that piece's own cable */
  const BRIDGE = 5;              /* B–C, the cheapest cable across the cut */

  /* Label geometry, not analysis: each price sits nine units off its own
     cable, on the side away from the middle of the drawing. The town letters
     are hand-placed just outside their dots. */
  const MID = [101, 72];
  const WPOS = E.map(function (e) {
    const p = POS[e[0]], q = POS[e[1]];
    const mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2;
    let nx = p[1] - q[1], ny = q[0] - p[0];
    const m = Math.hypot(nx, ny) || 1;
    nx /= m; ny /= m;
    if ((mx - MID[0]) * nx + (my - MID[1]) * ny < 0) { nx = -nx; ny = -ny; }
    return [mx + 9 * nx, my + 9 * ny + 3.4];
  });
  const LPOS = { A: [16, 40], B: [100, 12], C: [186, 42], D: [19, 129], E: [94, 106], F: [184, 129] };

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Six towns, nine possible cables",
      note: "A power plant at A, five towns, and nine surveyed stretches of cable; the number on each is what that stretch costs. Any five cables that reach all six towns without closing a loop form a spanning tree. The question is which five are cheapest — and both algorithms work on this same grid.",
      async run(ctx) {
        ctx.build();
        ctx.head("left", "Kruskal");
        ctx.head("right", "Prim");
        ctx.log("left", "sort every cable by price, then walk down the list.");
        ctx.log("right", "start at the power plant and grow outward.");
        await ctx.sleep(3800);
      }
    },
    {
      label: "Kruskal: cheapest cable anywhere",
      note: "Walk down the price list and take each cable unless both of its towns are already joined — then it would buy a route that exists, which is what a loop is. The 3-cable is refused for exactly that reason. Five cables in, all six towns are joined and the bill is 18; the 7, 8 and 9-cables are never even considered.",
      async run(ctx) {
        ctx.wait("right", true);
        ctx.wait("left", false);
        ctx.head("left", "Kruskal: cheapest cable first");
        for (let i = 0; i < KRUSKAL.length; i++) {
          const s = KRUSKAL[i];
          ctx.edge("left", s.e, "look");
          ctx.log("left", s.log);
          await ctx.sleep(750);
          ctx.edge("left", s.e, s.take ? "take" : "skip");
          if (s.take) { ctx.join("left", s.e); ctx.bill("left", s.tot); }
          await ctx.sleep(s.take ? 650 : 1900);
        }
        ctx.log("left", "five cables, six towns, no loop. the 7, 8 and 9-cables were never even asked.");
        await ctx.sleep(2600);
      }
    },
    {
      label: "Prim: grow out from the power plant",
      note: "Same grid, opposite discipline. Prim only ever looks at cables with exactly one end inside the grid it has built so far. That is why it walks past the 5-cable while the 5-cable is the cheapest thing left on the map: both of its towns are still outside. Two steps later C is inside, the 5-cable is reachable, and Prim finishes on the same five cables and the same bill of 18.",
      async run(ctx) {
        ctx.wait("left", false);
        ctx.wait("right", false);
        ctx.head("right", "Prim: grow from A");
        ctx.log("right", "the grid starts as one town: the power plant A.");
        ctx.node("right", "A", "on");
        await ctx.sleep(1100);
        for (let i = 0; i < PRIM.length; i++) {
          const s = PRIM[i];
          ctx.edge("right", s.e, "look");
          ctx.log("right", s.log);
          await ctx.sleep(i === 3 ? 2200 : 950);
          ctx.edge("right", s.e, "take");
          ctx.join("right", s.e);
          ctx.bill("right", s.tot);
          await ctx.sleep(650);
        }
        ctx.log("right", "the same five cables Kruskal found, in a different order, for the same 18.");
        await ctx.sleep(3000);
      }
    },
    {
      label: "Why greedy could not have gone wrong",
      note: "On the left is a different spanning tree of the same towns, reaching the far side by the 9-cable, for 21. Cut that cable. A tree carries no spare route, so it falls into exactly two pieces: A, B, D, E on one side and C, F on the other. The cheapest cable joining those two pieces is the 6-cable. Put it in and everything is connected again with no loop, for 18 — the tree on the right. A tree you can improve by such a swap was never the minimum.",
      async run(ctx) {
        ctx.head("right", "the cheapest tree");
        ctx.head("left", "a tree that used the 9-cable");
        ctx.reset("left");
        for (let i = 0; i < ALT.length; i++) { ctx.edge("left", ALT[i], "take"); ctx.join("left", ALT[i]); }
        ctx.bill("left", ALT_TOT);
        ctx.log("left", "five cables, six towns, no loop — a perfectly good spanning tree, for 21.");
        await ctx.sleep(3000);

        ctx.edge("left", CUT, "look");
        ctx.log("left", "cut the 9-cable and watch what the tree does.");
        await ctx.sleep(1400);
        ctx.edge("left", CUT, "gone");
        ctx.edge("left", FAR_EDGE, "piece");
        for (let i = 0; i < FAR.length; i++) ctx.node("left", FAR[i], "two");
        ctx.bill("left", ALT_TOT - E[CUT][2]);
        ctx.log("left", "exactly two pieces: A, B, D, E — and C, F.");
        await ctx.sleep(2800);

        ctx.edge("left", BRIDGE, "look");
        ctx.log("left", "the cheapest cable joining those same two pieces is the 6-cable B–C.");
        await ctx.sleep(2000);
        ctx.edge("left", BRIDGE, "take");
        ctx.edge("left", FAR_EDGE, "take");
        for (let i = 0; i < FAR.length; i++) ctx.node("left", FAR[i], "on");
        ctx.head("left", "the same tree, three cheaper");
        ctx.bill("left", 18);
        ctx.log("left", "connected again, still no loop: 21 − 9 + 6 = 18. the tree on the right.");
        await ctx.sleep(3600);
      }
    }
  ];

  mountScenes(document.getElementById("mst-race"), scenes, {
    stepsLabel: "Minimum spanning tree steps",

    /* Two identical grids that persist across all four scenes, each with its
       own running bill and its own line of narration. Built once per run and
       handed to every scene on ctx, so a cable's colour, its price and the
       bill under it can never drift apart. */
    helpers(ctx) {
      const host = { left: ctx.$("[data-mst-left]"), right: ctx.$("[data-mst-right]") };
      const S = { left: null, right: null };

      function draw(which) {
        const h = host[which];
        h.textContent = "";
        const head = ctx.el("div", "mst-head", "");
        h.appendChild(head);

        const wrap = ctx.el("div", "mst-net");
        const svg = ctx.svgRoot("0 0 202 142");
        const gEdge = svg.appendChild(ctx.svgEl("g"));
        const gNode = svg.appendChild(ctx.svgEl("g"));
        const gText = svg.appendChild(ctx.svgEl("g"));

        const edges = E.map(function (e) {
          return gEdge.appendChild(ctx.svgEl("line", {
            x1: POS[e[0]][0], y1: POS[e[0]][1], x2: POS[e[1]][0], y2: POS[e[1]][1],
            "class": "anim-edge mst-idle"
          }));
        });
        const weights = E.map(function (e, i) {
          const t = ctx.svgEl("text", {
            x: WPOS[i][0], y: WPOS[i][1], "text-anchor": "middle",
            "class": "anim-label anim-knockout mst-w mst-w-off"
          });
          t.textContent = e[2];
          return gText.appendChild(t);
        });
        const nodes = {};
        NAME.forEach(function (n) {
          nodes[n] = gNode.appendChild(ctx.svgEl("circle",
            { cx: POS[n][0], cy: POS[n][1], r: 7, "class": "anim-node-off" }));
          const t = ctx.svgEl("text", {
            x: LPOS[n][0], y: LPOS[n][1], "text-anchor": "middle",
            "class": "anim-label anim-knockout mst-name"
          });
          t.textContent = n;
          gText.appendChild(t);
        });

        wrap.appendChild(svg);
        h.appendChild(wrap);
        const bill = ctx.el("div", "anim-tally mst-bill", "<span>cable bill</span><b>0</b>");
        h.appendChild(bill);
        const log = ctx.el("div", "anim-caption mst-log", "");
        h.appendChild(log);
        S[which] = { col: h, head: head, edges: edges, weights: weights,
                     nodes: nodes, bill: bill.querySelector("b"), log: log };
      }

      /* clear() empties the columns but leaves their classes alone, so the
         dimming has to be lifted here or a jump back to scene 1 inherits it. */
      function build() {
        draw("left");
        draw("right");
        wait("left", false);
        wait("right", false);
      }

      /* One cable, one of five states, price and ink moving together. */
      const WCLASS = { idle: "off", look: "look", take: "on", piece: "two", skip: "off", gone: "gone" };
      function edge(which, i, kind) {
        const s = S[which];
        s.edges[i].setAttribute("class", "anim-edge mst-" + kind);
        s.weights[i].setAttribute("class",
          "anim-label anim-knockout mst-w mst-w-" + WCLASS[kind]);
      }
      function node(which, n, kind) {
        S[which].nodes[n].setAttribute("class",
          kind === "on" ? "anim-node" : kind === "two" ? "mst-node-two" : "anim-node-off");
      }
      /* Taking a cable is also what puts its two towns in the grid. */
      function join(which, i) { node(which, E[i][0], "on"); node(which, E[i][1], "on"); }

      function bill(which, n) { S[which].bill.textContent = n; }
      function log(which, t) { S[which].log.textContent = t; }
      function head(which, t) { S[which].head.textContent = t; }
      function wait(which, on) { S[which].col.classList.toggle("mst-wait", !!on); }

      function reset(which) {
        for (let i = 0; i < E.length; i++) edge(which, i, "idle");
        NAME.forEach(function (n) { node(which, n, "off"); });
        bill(which, 0);
      }

      return { build: build, edge: edge, node: node, join: join,
               bill: bill, log: log, head: head, wait: wait, reset: reset };
    }
  });
});
