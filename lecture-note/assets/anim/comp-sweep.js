/* ==========================================================================
   comp-sweep.js — Finding the connected components, one sweep at a time.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Mounted by slides/m01/m01-euler-tour.md. The stage's own layout CSS stays
   with the page that mounts it, because the note has a column to fill and the
   slide has a 1280x720 frame.

   The point the static figures cannot make: a component is not something you
   can see, it is something you *find*, and the finding is a process. Scene 5
   hands the graph to the room — pick any seed you like and the visit order
   changes while the partition does not.
   ========================================================================== */

(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     Twelve nodes, thirteen edges: an eight-node ladder, a triangle, and one
     lone node. The same graph and the same arrangement as
     figures/components-band.png and figures/sweep-1..3.png — make_figures.py's
     LADDER_POS + TRI_POS + PAIR_POS, mapped from its data units into a
     700 x 156 box by x -> 40 + 96.875x, y -> 122 - 96.875y. The extra 10 units
     of headroom are for the distance numbers, which sit outside the discs and
     would otherwise be clipped off the top row.
     ------------------------------------------------------------------------ */
  const NAME = ["L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "M0", "M1", "M2", "R0"];
  const POS = [
    [40, 122], [117.5, 122], [195, 122], [272.5, 122],
    [40, 34.8], [117.5, 34.8], [195, 34.8], [272.5, 34.8],
    [427.5, 122], [505, 122], [466.3, 39.7],
    [660, 92.9]
  ];
  const EDGES = [
    [0, 1], [1, 2], [2, 3], [4, 5], [5, 6], [6, 7],
    [0, 4], [1, 5], [2, 6], [3, 7],
    [8, 9], [9, 10], [10, 8]
  ];

  /* Which component each node belongs to, and how big each one is. Found once,
     by hand, and written down — nothing here runs a search at page load. */
  const COMP = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2];
  const SIZE = [8, 3, 1];

  /* Breadth-first layers from every one of the twelve possible seeds: layer k
     is the set of nodes at distance k. Twelve arrays rather than a BFS in the
     browser, because scene 5 lets the room choose the seed and the answer has
     to be the same one this file was checked against. Recipe: BFS over EDGES
     from each start in turn. */
  const LAYERS = [
    /* L0 */ [[0], [1, 4], [2, 5], [3, 6], [7]],
    /* L1 */ [[1], [0, 2, 5], [4, 3, 6], [7]],
    /* L2 */ [[2], [1, 3, 6], [0, 5, 7], [4]],
    /* L3 */ [[3], [2, 7], [1, 6], [0, 5], [4]],
    /* L4 */ [[4], [5, 0], [6, 1], [7, 2], [3]],
    /* L5 */ [[5], [4, 6, 1], [0, 7, 2], [3]],
    /* L6 */ [[6], [5, 7, 2], [4, 1, 3], [0]],
    /* L7 */ [[7], [6, 3], [5, 2], [4, 1], [0]],
    /* M0 */ [[8], [9, 10]],
    /* M1 */ [[9], [8, 10]],
    /* M2 */ [[10], [9, 8]],
    /* R0 */ [[11]]
  ];

  /* A dashed box around each component, drawn when its sweep finishes. Sized
     to clear the distance numbers and the names, not just the discs.
     [x, y, width, height] in the same 700 x 156 box. */
  const BOX = [
    [18, 4, 292, 150],
    [404, 9, 140, 145],
    [626, 60, 72, 68]
  ];

  /* The three seeds the playback uses, in order. Any three would do — that is
     scene 5's point — these are just the leftmost node of each component. */
  const SEEDS = [0, 8, 11];

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Twelve nodes, and no map",
      note: "Twelve nodes and thirteen edges, and nothing tells you how many pieces they form. You cannot read a component off the picture — a component is not drawn, it is found. So pick a node and start walking.",
      async run(ctx) {
        ctx.idle();
        ctx.draw();
        ctx.card();
        ctx.say("Nothing is marked yet. Every node is a node you have not visited.");
        await ctx.sleep(2600);
        ctx.tally("nodes", "12");
        await ctx.sleep(700);
        ctx.tally("edges", "13");
        await ctx.sleep(700);
        ctx.tally("components", "?");
        await ctx.sleep(2400);
      }
    },
    {
      label: "One sweep, ring by ring",
      note: "Start at L0. Visit its unvisited neighbours, then theirs, then theirs — the amber ring is the frontier, and the number on a node is how many edges from the seed it sits. When the frontier comes up empty, everything you touched is one component: eight nodes.",
      async run(ctx) {
        ctx.idle();
        ctx.reset();
        ctx.card();
        ctx.say("Pencil down on L0 and take the neighbours in rings.");
        await ctx.sleep(900);
        await ctx.sweep(0);
        await ctx.sleep(600);
        ctx.close(0, 0);
        ctx.say("Frontier empty. Everything reached from L0 is <b>component 1</b>.");
        await ctx.sleep(2800);
      }
    },
    {
      label: "Repeat until nothing is left",
      note: "Four nodes are still unmarked, so the graph is not done. Seed a second sweep at M0 — three nodes — and a third at R0, which reaches nobody at all. One node with no edges is still a component: there is no pair inside it left to fail the test.",
      async run(ctx) {
        ctx.idle();
        ctx.reset();
        ctx.card();
        await ctx.sweep(0, true);
        ctx.close(0, 0);
        ctx.say("Eight down, four to go. Seed the next sweep anywhere unmarked.");
        await ctx.sleep(1300);
        await ctx.sweep(8);
        ctx.close(1, 8);
        await ctx.sleep(1100);
        ctx.say("Two left? No — one. R0 has no edges, and reaches only itself.");
        await ctx.sweep(11);
        ctx.close(2, 11);
        await ctx.sleep(2800);
      }
    },
    {
      label: "What the sweep cost, and what it threw in",
      note: "Each node is entered once and each edge is looked at twice, once from either end, so the whole partition costs O(N + M) — thirteen edges, not seventy-eight pairs. And the ring number you watched grow is the shortest-path distance from the seed, free of charge. Module 2 spends it.",
      async run(ctx) {
        ctx.idle();
        ctx.reset();
        ctx.card();
        await ctx.sweep(0, true);
        ctx.close(0, 0);
        await ctx.sweep(8, true);
        ctx.close(1, 8);
        await ctx.sweep(11, true);
        ctx.close(2, 11);
        ctx.say("Three sweeps, twelve nodes, thirteen edges, nothing looked at twice over.");
        await ctx.sleep(1600);
        ctx.tally("nodes entered", "12, once each");
        await ctx.sleep(1000);
        ctx.tally("edges looked at", "13, twice each");
        await ctx.sleep(1000);
        ctx.tally("cost", "O(N + M)");
        await ctx.sleep(1200);
        ctx.quote("and the ring number is the distance from the seed — free.");
        await ctx.sleep(3000);
      }
    },
    {
      label: "Now you try — pick the seeds yourself",
      note: "Your turn. Click any unmarked node to sweep from there, then another, until the graph is used up. Whatever order you choose, you will need three sweeps and you will get the same three groups. The visit order is yours; the partition is the graph's.",
      async run(ctx) {
        ctx.reset();
        ctx.card();
        ctx.hand();
        ctx.say("Click any node to sweep from it.");
        if (ctx.fast()) return;
        await ctx.sleep(17000);
        ctx.idle();
      }
    }
  ];

  mountScenes(document.getElementById("comp-sweep"), scenes, {
    stepsLabel: "Sweep steps",

    helpers(ctx) {
      const mapBox = ctx.$("[data-cs-map]");
      const side = ctx.$("[data-cs-side]");
      const S = { seen: [], dist: [], live: false, busy: false, grabbed: false, sweeps: 0, done: [] };

      const at = (i) => POS[i][0] + " " + POS[i][1];

      /* Draw a path on and then let go of it — see kb-tracer's ink() for why
         the class has to come off again. */
      function ink(p, len, ms) {
        if (ctx.fast()) return p;
        p.classList.add("anim-draw");
        p.style.setProperty("--dash", Math.ceil(len) + 6);
        p.style.animationDuration = (ms / 1000) + "s";
        setTimeout(function () {
          p.classList.remove("anim-draw");
          p.style.removeProperty("--dash");
          p.style.removeProperty("animation-duration");
        }, ms + 150);
        return p;
      }

      /* ------------------------------------------------------------- the map */
      function draw() {
        mapBox.textContent = "";
        const svg = ctx.svgRoot("0 0 700 156");
        const g = () => svg.appendChild(ctx.svgEl("g"));
        const gBox = g(), gEdge = g(), gLit = g(), gNode = g(), gNum = g(), gHit = g();

        S.edges = EDGES.map(function (e) {
          return gEdge.appendChild(ctx.svgEl("line", {
            x1: POS[e[0]][0], y1: POS[e[0]][1], x2: POS[e[1]][0], y2: POS[e[1]][1],
            "class": "anim-edge"
          }));
        });

        S.nodes = POS.map(function (p, i) {
          const c = ctx.svgEl("circle", { cx: p[0], cy: p[1], r: 9, "class": "cs-node" });
          if (!ctx.fast()) {
            c.classList.add("anim-fade");
            c.style.animationDelay = (i * 0.05) + "s";
          }
          return gNode.appendChild(c);
        });

        /* Distance labels sit below the bottom row and above the top row, so a
           number never lands on the rung running through its own node. */
        S.nums = POS.map(function (p, i) {
          const below = p[1] > 70;
          const t = ctx.svgEl("text", {
            x: p[0], y: p[1] + (below ? 25 : -15),
            "text-anchor": "middle", "class": "cs-num anim-knockout"
          });
          return gNum.appendChild(t);
        });

        /* Names go beside the disc, not under it: centred on the node they sit
           exactly on top of the rung running through it, and a rung is the one
           thing in this drawing a label cannot dodge vertically. */
        POS.forEach(function (p, i) {
          const below = p[1] > 70;
          const t = ctx.svgEl("text", {
            x: p[0] + 14, y: p[1] + (below ? -10 : 18),
            "text-anchor": "start", "class": "cs-name anim-knockout"
          });
          t.textContent = NAME[i];
          gNum.appendChild(t);
        });

        S.hits = POS.map(function (p, i) {
          const e = ctx.svgEl("circle", { cx: p[0], cy: p[1], r: 20, "class": "cs-hit" });
          e.addEventListener("click", function () { onNode(i); });
          return gHit.appendChild(e);
        });

        S.svg = svg;
        S.gBox = gBox;
        S.gLit = gLit;
        mapBox.appendChild(svg);
        reset();
      }

      function paint() {
        S.nodes.forEach(function (c, i) {
          let cls = "cs-node";
          if (S.seen[i] === 2) cls += " cs-front";
          else if (S.seen[i] === 1) cls += " cs-seen";
          else if (S.live && !S.busy) cls += " cs-open";
          c.setAttribute("class", cls);
          S.nums[i].textContent = S.dist[i] == null ? "" : String(S.dist[i]);
        });
      }

      function reset() {
        if (!S.nodes) return;
        S.seen = POS.map(function () { return 0; });
        S.dist = POS.map(function () { return null; });
        S.sweeps = 0;
        S.busy = false;
        S.done = [];
        S.gBox.textContent = "";
        S.gLit.textContent = "";
        S.edges.forEach(function (l) { l.setAttribute("class", "anim-edge"); });
        paint();
      }

      /* A timer the sequencer's pause does not reach. Scene 5's first click
         pauses the run — that is the whole point of grab() — and a sweep that
         waited on ctx.sleep would then stall halfway through its own rings,
         with the room watching. A click-driven sweep waits on this instead. */
      const tick = (ms) => new Promise(function (r) { setTimeout(r, ms); });

      /* One breadth-first sweep from `seed`, layer by layer. Every edge from
         the layer just settled to the layer just found is lit — which is more
         than the search tree, and deliberately so: those are exactly the edges
         the sweep looks at, and the ones the O(N + M) count is about. */
      async function sweep(seed, quiet, waitFn) {
        const wait = waitFn || ctx.sleep;
        const layers = LAYERS[seed];
        let prev = [];
        for (let k = 0; k < layers.length; k++) {
          const now = layers[k];
          prev.forEach(function (i) { S.seen[i] = 1; });
          now.forEach(function (i) { S.seen[i] = 2; S.dist[i] = k; });
          EDGES.forEach(function (e, ei) {
            const a = prev.indexOf(e[0]) >= 0 && now.indexOf(e[1]) >= 0;
            const b = prev.indexOf(e[1]) >= 0 && now.indexOf(e[0]) >= 0;
            if (a || b) S.edges[ei].setAttribute("class", "anim-edge cs-tree");
          });
          paint();
          if (!quiet) {
            const total = S.seen.filter(function (v) { return v; }).length;
            say("Ring <b>" + k + "</b> — " + now.length +
              (now.length > 1 ? " nodes" : " node") + ", " + total + " marked of 12.");
          }
          prev = now;
          await wait(quiet ? 0 : 720);
        }
        prev.forEach(function (i) { S.seen[i] = 1; });
        paint();
      }

      /* The sweep is over: ring the component and write it down. */
      function close(c, seed) {
        const b = BOX[c];
        const r = ctx.svgEl("rect",
          { x: b[0], y: b[1], width: b[2], height: b[3], rx: 12, "class": "cs-box" });
        S.gBox.appendChild(ink(r, 2 * (b[2] + b[3]), 620));
        S.sweeps += 1;
        S.done.push(c);
        chip("component " + (c + 1), SIZE[c] + (SIZE[c] > 1 ? " nodes" : " node") +
          " · from " + NAME[seed]);
      }

      /* ------------------------------------------------------------ the card */
      /* Rebuilt by every scene, so nothing an earlier scene wrote can survive
         into a later one and read as this scene's own bookkeeping. */
      function card() {
        side.textContent = "";
        S.panel = ctx.el("div", "anim-panel anim-pop cs-card");
        S.msg = ctx.el("div", "cs-msg", "");
        S.rows = ctx.el("div", "cs-rows");
        S.panel.appendChild(S.msg);
        S.panel.appendChild(S.rows);
        side.appendChild(S.panel);
        return S.panel;
      }
      const say = (html) => { if (S.msg) S.msg.innerHTML = html; };
      function tally(k, v) {
        if (S.rows) S.rows.appendChild(ctx.el("div", "anim-tally anim-fade",
          "<span>" + k + "</span><b>" + v + "</b>"));
      }
      function chip(k, v) {
        if (S.rows) S.rows.appendChild(ctx.el("div", "cs-chip anim-pop",
          "<b>" + k + "</b><span>" + v + "</span>"));
      }
      function quote(t) {
        if (S.rows) S.rows.appendChild(ctx.el("div", "anim-quote anim-fade", t));
      }

      /* -------------------------------------------------------- the clicks */
      function hand() {
        S.live = true;
        S.busy = false;
        S.grabbed = false;
        S.svg.classList.add("cs-clickable");
        paint();
      }
      function idle() {
        S.live = false;
        if (S.svg) S.svg.classList.remove("cs-clickable");
        if (S.nodes) paint();
      }

      /* The first click is a grab: it pauses the sequence, so the graph stays
         yours until you press play. Same contract as the tracer's. */
      function grab() {
        if (S.grabbed) return;
        S.grabbed = true;
        ctx.pause();
      }

      async function onNode(i) {
        if (!S.live || S.busy) return;
        grab();
        if (S.seen[i]) {
          S.nodes[i].classList.remove("cs-nope");
          S.nodes[i].getBoundingClientRect();
          S.nodes[i].classList.add("cs-nope");
          say("<b>" + NAME[i] + "</b> is already marked. Seed somewhere unmarked.");
          return;
        }
        S.busy = true;                        /* no second click while one runs */
        await sweep(i, false, tick);
        S.busy = false;
        const c = COMP[i];
        close(c, i);
        const left = S.seen.filter(function (v) { return !v; }).length;
        if (left) {
          say("Sweep " + S.sweeps + " done — " + SIZE[c] + " nodes. <b>" + left +
            "</b> still unmarked.");
        } else {
          say("<b>" + S.sweeps + " sweeps, three components.</b> Your order, the graph's answer.");
          idle();
        }
      }

      return {
        draw: draw, reset: reset, sweep: sweep, close: close,
        card: card, say: say, tally: tally, chip: chip, quote: quote,
        hand: hand, idle: idle
      };
    }
  });
});
