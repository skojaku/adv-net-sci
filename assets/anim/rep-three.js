/* ==========================================================================
   rep-three.js — One graph, three data structures.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Mounted by slides/m01/m01-euler-tour.md, after the slide that names the
   three. The names arrive first and the stage builds them, because the point
   is not what they are called but that they are the same six edges filed
   three ways — and that a degree falls out of each differently.

   The lecture note's "Three ways to write a network down" prints all three as
   static blocks; nothing here contradicts it, and either page may mount this.
   ========================================================================== */

(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     make_figures.py's graph5, at walk-power.js's coordinates — the same five
     nodes and six edges behind store-matrix.png, adjacency-squared.png, the
     walk-counting stage and the CSR knob. Three slides in a row show one
     picture, so it has to be one picture.
     ------------------------------------------------------------------------ */
  const POS = [[95, 45], [325, 45], [95, 160], [325, 160], [210, 264]];
  const EDGES = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 4], [3, 4]];
  const N = 5;
  const R = 17;

  /* The node the last beat reads a degree off. 1 is the only one whose three
     neighbours are three different-looking things in the three structures:
     three scattered pairs, one row of three, one row summing to three. */
  const FOCUS = 1;

  /* The adjacency list, derived from the edges rather than written out, so it
     cannot drift from them. Sorted, because a reader compares it to the row
     of the matrix directly underneath. */
  const ADJ = [];
  for (let i = 0; i < N; i++) ADJ.push([]);
  EDGES.forEach(function (e) { ADJ[e[0]].push(e[1]); ADJ[e[1]].push(e[0]); });
  ADJ.forEach(function (row) { row.sort(function (a, b) { return a - b; }); });

  const TITLE = {
    el: "edge list",
    al: "adjacency list",
    m: "adjacency matrix"
  };

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "One graph",
      note: "Five nodes, six edges. A computer cannot look at the picture — it needs one of the three below.",
      async run(ctx) {
        ctx.drawGraph();
        ctx.blocks([]);
        await ctx.sleep(2600);
      }
    },
    {
      label: "Edge list",
      note: "One pair per edge, six of them. Compact, and what a data file looks like — but a neighbour question costs a scan of everything.",
      async run(ctx) {
        ctx.drawGraph();
        ctx.blocks(["el"]);
        await ctx.fillEdges({ pause: 420 });
        await ctx.sleep(2200);
      }
    },
    {
      label: "Adjacency list",
      note: "The same six edges, filed twice — once under each endpoint. A node's neighbours are now in one place, which is what a traversal wants.",
      async run(ctx) {
        ctx.drawGraph();
        ctx.blocks(["al"]);
        await ctx.fillAdj({ pause: 520 });
        await ctx.sleep(2200);
      }
    },
    {
      label: "Adjacency matrix",
      note: "Every pair gets a cell now, including the thirteen that hold nothing. That is the price of one-lookup answers and of linear algebra.",
      async run(ctx) {
        ctx.drawGraph();
        ctx.blocks(["m"]);
        await ctx.fillMatrix({ pause: 420 });
        await ctx.sleep(2200);
      }
    },
    {
      label: "Degree, three ways",
      note: "Node 1 has degree 3 in all three — count its appearances, take the length of its row, sum its row.",
      async run(ctx) {
        ctx.drawGraph();
        ctx.focus(FOCUS);
        ctx.blocks(["el", "al", "m"], true);
        await ctx.fillEdges({ hi: FOCUS, pause: 0 });
        await ctx.fillAdj({ hi: FOCUS, pause: 0 });
        await ctx.fillMatrix({ hi: FOCUS, pause: 0 });
        await ctx.sleep(4000);
      }
    }
  ];

  mountScenes(document.getElementById("rep-three"), scenes, {
    stepsLabel: "Representation steps",

    helpers(ctx) {
      const mapBox = ctx.$("[data-rt-map]");
      const side = ctx.$("[data-rt-side]");
      const S = { nodes: [], edges: [], box: {} };

      /* Every beat redraws: the kit replays earlier scenes in fast mode to
         reach a step, so nothing may depend on what a previous beat left. */
      function drawGraph() {
        mapBox.textContent = "";
        const svg = ctx.svgRoot("0 0 420 300");
        const g = () => svg.appendChild(ctx.svgEl("g"));
        const gEdge = g(), gNode = g(), gText = g();

        S.edges = EDGES.map(function (e) {
          return gEdge.appendChild(ctx.svgEl("line", {
            x1: POS[e[0]][0], y1: POS[e[0]][1], x2: POS[e[1]][0], y2: POS[e[1]][1],
            "class": "anim-edge"
          }));
        });
        S.nodes = POS.map(function (p) {
          return gNode.appendChild(ctx.svgEl("circle",
            { cx: p[0], cy: p[1], r: R, "class": "rt-node" }));
        });
        POS.forEach(function (p, i) {
          const t = ctx.svgEl("text",
            { x: p[0], y: p[1] + 7, "text-anchor": "middle", "class": "rt-name" });
          t.textContent = String(i);
          gText.appendChild(t);
        });
        mapBox.appendChild(svg);
      }

      function focus(i) {
        S.nodes.forEach(function (n, k) { n.classList.toggle("rt-focus", k === i); });
      }

      /* The right column carries whichever structures the beat names, in the
         order given. `compact` is the last beat, where all three have to fit
         at once. */
      function blocks(kinds, compact) {
        side.textContent = "";
        S.box = {};
        /* The opening beat names no structure yet, and half a slide of white
           beside a small graph reads as something failing to load. Give the
           graph the whole frame until there is something to put next to it. */
        const canvas = ctx.$("[data-anim-canvas]");
        if (canvas) canvas.classList.toggle("rt-solo", !kinds.length);
        const stack = ctx.el("div", "rt-stack" + (compact ? " rt-compact" : ""));
        kinds.forEach(function (k) {
          const block = ctx.el("div", "rt-block");
          block.appendChild(ctx.el("div", "rt-h", TITLE[k]));
          const body = ctx.el("div", "rt-" + k);
          block.appendChild(body);
          stack.appendChild(block);
          S.box[k] = body;
        });
        side.appendChild(stack);
      }

      /* `pause` is 0 on the last beat, where three structures build in one
         breath; ctx.fast() zeroes it anyway while the kit is catching up to a
         step the room clicked to. */
      function beat(pause) {
        if (!pause || ctx.fast()) return Promise.resolve();
        return ctx.sleep(pause);
      }

      async function fillEdges(o) {
        o = o || {};
        const host = S.box.el;
        if (!host) return;
        for (let k = 0; k < EDGES.length; k++) {
          const e = EDGES[k];
          const cell = ctx.el("i", "rt-pair", "(" + e[0] + "," + e[1] + ")");
          if (o.hi != null && (e[0] === o.hi || e[1] === o.hi)) cell.classList.add("rt-hi");
          host.appendChild(cell);
          if (S.edges[k]) S.edges[k].classList.add("rt-lit");
          await beat(o.pause);
        }
      }

      async function fillAdj(o) {
        o = o || {};
        const host = S.box.al;
        if (!host) return;
        for (let i = 0; i < N; i++) {
          const row = ctx.el("div", "rt-alrow");
          row.appendChild(ctx.el("b", null, String(i)));
          ADJ[i].forEach(function (j) { row.appendChild(ctx.el("i", "rt-cell", String(j))); });
          if (o.hi != null && i === o.hi) row.classList.add("rt-hi");
          host.appendChild(row);
          /* Walking the highlight down the graph is what says the rows are
             the nodes, not just five lines of numbers. The edges light as they
             are filed, which is also how the graph stays one picture across
             the three beats rather than going dark in the middle one. */
          if (o.pause) focus(i);
          EDGES.forEach(function (e, k) {
            if ((e[0] === i || e[1] === i) && S.edges[k]) S.edges[k].classList.add("rt-lit");
          });
          await beat(o.pause);
        }
        focus(o.hi == null ? -1 : o.hi);
      }

      async function fillMatrix(o) {
        o = o || {};
        const host = S.box.m;
        if (!host) return;
        const cells = [];
        for (let i = 0; i < N; i++) {
          for (let j = 0; j < N; j++) {
            const c = ctx.el("i", null, "0");
            if (o.hi != null && i === o.hi) c.classList.add("rt-band");
            host.appendChild(c);
            cells.push(c);
          }
        }
        for (let k = 0; k < EDGES.length; k++) {
          const e = EDGES[k];
          /* One edge, two cells — the mirror is the whole point of the beat. */
          [[e[0], e[1]], [e[1], e[0]]].forEach(function (p) {
            const c = cells[p[0] * N + p[1]];
            c.textContent = "1";
            c.classList.add("rt-on");
          });
          if (S.edges[k]) S.edges[k].classList.add("rt-lit");
          await beat(o.pause);
        }
      }

      return {
        drawGraph: drawGraph,
        focus: focus,
        blocks: blocks,
        fillEdges: fillEdges,
        fillAdj: fillAdj,
        fillMatrix: fillMatrix
      };
    }
  });
});
