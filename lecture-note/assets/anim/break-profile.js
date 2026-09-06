/* The robustness profile, drawn one removal at a time. Markup above, scenes
   below, and nothing in between: the paper, the pen, the motion and the
   sequencer all come from assets/anim.css + assets/anim.js, and everything a
   scene calls arrives on `ctx`. The kit is loaded after this file, hence the
   animReady queue. */
(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     The eight Moravian towns and the seven cables of the 292 km minimum
     spanning tree, the same tree the deck's static figures draw. Every number
     below was computed once, offline, and pasted in; nothing here runs a graph
     algorithm at load. Reproduce with:

       import networkx as nx
       T = nx.Graph(); T.add_weighted_edges_from(MST_E)          # 292 km
       conn = lambda rm: max((len(c) for c in nx.connected_components(
                   nx.restricted_view(T, rm, []))), default=0) / 8
       R    = lambda order: sum(conn(order[:k]) for k in range(1, 8)) / 8

     which is the deck's own R-index: the mean of the seven intermediate
     connectivities, exactly as figures/make_figures.py computes it.

       random   Zlin, Znojmo, Jihlava, Hodonin, Prostejov, Trebic, Olomouc, Brno
                connectivity 8 7 6 5 4 2 1 1 0  (of 8)      R = 13/32 = 0.41
       attack   Brno, Prostejov, Trebic, Hodonin, Jihlava, Olomouc, Zlin, Znojmo
                connectivity 8 3 3 1 1 1 1 1 0  (of 8)      R = 11/64 = 0.17

     The attacker is ADAPTIVE: it recomputes the degrees after every removal and
     takes the largest town left, which is why it takes Prostejov second.
     ------------------------------------------------------------------------ */

  const SHORT = ["Jihlava", "Třebíč", "Znojmo", "Brno", "Hodonín", "Prostějov", "Olomouc", "Zlín"];
  const N = 8;

  /* A layout of its own, and deliberately so. The deck's map is 1100 x 300 —
     three times as wide as it is tall, which is what makes eight towns and
     thirteen cables legible across a slide. A stage has to hold that map AND a
     chart inside one 720px frame, so here the same tree is drawn square. Same
     towns, same seven cables, same left-to-right order; only the shape of the
     paper differs. */
  const POS = [
    [30, 42], [96, 96], [30, 152], [162, 150], [150, 238], [236, 94], [281, 44], [283, 162]
  ];
  /* At slide type a name is wider than the gap beside its town, so each one is
     placed clear of its own disc and of every cable, and anchored to the canvas
     where centring would run it off the edge. Centred labels clipped "Jihlava"
     to "ihlava" and sat on top of three discs. */
  const LAB = [
    [6, 16], [96, 70], [6, 188], [162, 124], [172, 244], [196, 68], [305, 18], [305, 198]
  ];
  const LAB_ANCHOR = ["start", "middle", "start", "middle", "start", "middle", "end", "end"];
  const E = [[0, 1], [1, 2], [1, 3], [3, 5], [5, 6], [5, 7], [3, 4]];

  /* Per step: which towns are in the largest surviving piece (g), alive but cut
     off (o), or gone (x), recovered from the tree, not typed by hand. */
  const RANDOM = ["gggggggg", "gggggggx", "ggxggggx", "xgxggggx", "xgxgxggx",
                  "xgxgxxox", "xxxgxxox", "xxxgxxxx", "xxxxxxxx"];
  const ATTACK = ["gggggggg", "gggxoooo", "gggxoxoo", "gxoxoxoo", "gxoxxxoo",
                  "xxgxxxoo", "xxgxxxxo", "xxgxxxxx", "xxxxxxxx"];
  const ORDER = { random: [7, 2, 0, 4, 5, 1, 6, 3], attack: [3, 5, 1, 4, 0, 6, 7, 2] };

  /* Connectivity read straight off the frames above, so the curve and the
     picture are the same fact stored once. */
  const conn = (frames) => frames.map((f) => {
    let g = 0;
    for (let i = 0; i < N; i++) if (f[i] === "g") g++;
    return g / N;
  });
  const Y = { random: conn(RANDOM), attack: conn(ATTACK) };
  const rindex = (a) => {
    let s = 0;
    for (let k = 1; k <= 7; k++) s += a[k];
    return s / 8;
  };
  const R = { random: rindex(Y.random), attack: rindex(Y.attack) };
  const RATIO = (R.random / R.attack).toFixed(1);

  /* chart geometry, in the chart's own viewBox units */
  const CX = (k) => 44 + (k / N) * 236;
  const CY = (v) => 112 - v * 92;

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "The 292 km grid, whole",
      note: "Connectivity is the number of towns in the largest connected component, divided by the eight the grid started with. Nothing is removed yet, so it is 1.",
      short: "Connectivity = largest component / 8.",
      async run(ctx) {
        ctx.build();
        ctx.frame(RANDOM[0]);
        ctx.readout('<span>towns removed <b>0</b></span><span>connectivity <b>1.00</b></span>');
        await ctx.sleep(2600);
      }
    },
    {
      label: "Random failure",
      note: "The towns are removed in an order that does not depend on the grid. Connectivity falls roughly in step with the number removed.",
      short: "Order independent of the grid.",
      async run(ctx) {
        const pl = ctx.line("bp-random");
        await ctx.sweep("random", RANDOM, pl);
        ctx.verdict("<span>random failure</span><b>R = " + R.random.toFixed(2) + "</b>");
        await ctx.sleep(2600);
      }
    },
    {
      label: "Targeted attack",
      note: "Same grid, same eight removals, but each step removes the town with the most cables, recounted after every removal. Brno goes first and the grid is already in thirds.",
      short: "Each step removes the largest town.",
      async run(ctx) {
        ctx.ghost();
        ctx.verdict("");
        const pl = ctx.line("bp-attack");
        await ctx.sweep("attack", ATTACK, pl);
        ctx.verdict("<span>targeted attack</span><b>R = " + R.attack.toFixed(2) + "</b>");
        await ctx.sleep(2800);
      }
    },
    {
      label: "The area under each curve",
      note: "The R-index is the mean of the connectivities after 1 to 7 removals, which is the area under the curve. The same grid and the same number of removals give " + RATIO + " times the loss under attack.",
      short: "R-index = area under the curve.",
      async run(ctx) {
        ctx.shade();
        ctx.frame(ATTACK[1]);
        ctx.readout(
          '<span style="color:var(--_gold)">random failure <b>R = ' + R.random.toFixed(2) + "</b></span>" +
          '<span style="color:var(--_amber)">targeted attack <b>R = ' + R.attack.toFixed(2) + "</b></span>");
        ctx.verdict("<span>the attack costs</span><b>" + RATIO + "&times; as much</b>");
        await ctx.sleep(3200);
      }
    }
  ];

  mountScenes(document.getElementById("break-profile"), scenes, {
    stepsLabel: "Removal steps",

    /* The two things only this animation has: one tree that persists across all
       four scenes, and one pair of axes under it that both removal orders draw
       into. Built once at mount, handed to every scene on ctx. */
    helpers(ctx) {
      const netBox = ctx.$("[data-bp-net]");
      const chartBox = ctx.$("[data-bp-chart]");
      const S = { nodes: [], edges: [], marks: null, c: null };

      function drawNet() {
        netBox.textContent = "";
        const wrap = ctx.el("div", "bp-net");
        const svg = ctx.svgRoot("0 0 311 268");
        const gEdge = svg.appendChild(ctx.svgEl("g"));
        const gNode = svg.appendChild(ctx.svgEl("g"));
        const gName = svg.appendChild(ctx.svgEl("g"));
        S.marks = svg.appendChild(ctx.svgEl("g"));
        const slow = !ctx.fast();

        S.edges = E.map((e, i) => {
          const a = POS[e[0]], b = POS[e[1]];
          const ln = ctx.svgEl("path", {
            d: "M " + a[0] + " " + a[1] + " L " + b[0] + " " + b[1],
            "class": "anim-edge" + (slow ? " anim-draw" : "")
          });
          if (slow) {
            ln.style.setProperty("--dash", Math.ceil(Math.hypot(a[0] - b[0], a[1] - b[1])) + 2);
            ln.style.animationDelay = (0.2 + i * 0.09) + "s";
          }
          return gEdge.appendChild(ln);
        });

        S.nodes = POS.map((p, i) => {
          const c = ctx.svgEl("circle", {
            cx: p[0], cy: p[1], r: 15.5, "class": "anim-node" + (slow ? " anim-fade" : "")
          });
          if (slow) c.style.animationDelay = (i * 0.06) + "s";
          return gNode.appendChild(c);
        });

        LAB.forEach((p, i) => {
          const t = ctx.svgEl("text", { x: p[0], y: p[1], "class": "bp-name",
                                        "text-anchor": LAB_ANCHOR[i] });
          t.textContent = SHORT[i];
          gName.appendChild(t);
        });

        wrap.appendChild(svg);
        netBox.appendChild(wrap);
      }

      function drawChart() {
        chartBox.textContent = "";
        const readSlot = ctx.el("div", "anim-readout bp-read");
        const svg = ctx.svgRoot("0 0 300 140");
        svg.innerHTML =
          '<line class="anim-axis" x1="44" y1="112" x2="288" y2="112"/>' +
          '<line class="anim-axis" x1="44" y1="16" x2="44" y2="112"/>' +
          '<text class="anim-label" x="39" y="24" text-anchor="end">1</text>' +
          '<text class="anim-label" x="39" y="115" text-anchor="end">0</text>' +
          '<text class="anim-label" x="15" y="64" text-anchor="middle" transform="rotate(-90 15 64)">connectivity</text>' +
          '<text class="anim-label" x="44" y="128">none gone</text>' +
          '<text class="anim-label" x="288" y="128" text-anchor="end">all eight gone</text>';
        const shade = svg.appendChild(ctx.svgEl("g"));
        const layer = svg.appendChild(ctx.svgEl("g"));
        const verdict = ctx.el("div", "anim-tally bp-verdict");
        chartBox.appendChild(readSlot);
        chartBox.appendChild(svg);
        chartBox.appendChild(verdict);
        S.c = { svg, layer, shade, verdict, readSlot, lines: [] };
      }

      function build() { drawNet(); drawChart(); }

      /* One snapshot. Pure lookup: a town is in the largest piece, cut off, or
         gone, and a cable is there unless one of its ends is. */
      function frame(str) {
        for (let i = 0; i < N; i++) {
          const c = str[i];
          S.nodes[i].setAttribute("class",
            c === "g" ? "anim-node" : c === "o" ? "anim-node-off" : "bp-out");
        }
        E.forEach((e, i) => {
          const dead = str[e[0]] === "x" || str[e[1]] === "x";
          S.edges[i].setAttribute("class", dead ? "anim-edge bp-cut" : "anim-edge");
        });
      }

      /* The town this step is about to remove, marked on the drawing before it
         goes, so the room can see which one the order picked. */
      function mark(i) {
        if (ctx.fast() || ctx.reduced || i < 0) return;
        S.nodes[i].setAttribute("class", "bp-next");
      }

      function line(cls) {
        const pl = ctx.svgEl("polyline", { "class": cls, points: "" });
        S.c.layer.appendChild(pl);
        S.c.lines.push(pl);
        return pl;
      }
      function setLine(pl, arr, upto) {
        let s = "";
        for (let k = 0; k <= upto; k++) s += (k ? " " : "") + CX(k) + "," + CY(arr[k]);
        pl.setAttribute("points", s);
      }
      function ghost() {
        S.c.lines.forEach((pl) => pl.setAttribute("class", pl.getAttribute("class") + " bp-ghost"));
      }
      /* The R-index is an area, so at the end it is drawn as one. */
      function shade() {
        S.c.shade.textContent = "";
        [["random", "bp-fill-random"], ["attack", "bp-fill-attack"]].forEach(([k, cls]) => {
          let d = "M " + CX(0) + " " + CY(0);
          for (let i = 0; i <= N; i++) d += " L " + CX(i) + " " + CY(Y[k][i]);
          d += " L " + CX(N) + " " + CY(0) + " Z";
          S.c.shade.appendChild(ctx.svgEl("path", { d: d, "class": cls }));
        });
      }

      function readout(html) { S.c.readSlot.innerHTML = html; return S.c.readSlot; }
      function verdict(html) { S.c.verdict.innerHTML = html; }

      /* One loop drives the grid, the curve and the readout from the same
         index, so nothing on screen can drift out of step with anything else. */
      async function sweep(key, frames, pl) {
        const read = readout(
          '<span>towns removed <b data-k>0 of 8</b></span>' +
          '<span>connectivity <b data-c>1.00</b></span>');
        const outK = read.querySelector("[data-k]");
        const outC = read.querySelector("[data-c]");
        frame(frames[0]);
        setLine(pl, Y[key], 0);
        for (let k = 1; k <= N; k++) {
          mark(ORDER[key][k - 1]);
          await ctx.sleep(340);
          frame(frames[k]);
          setLine(pl, Y[key], k);
          outK.textContent = k + " of 8";
          outC.textContent = Y[key][k].toFixed(2);
          await ctx.sleep(360);
        }
      }

      return { build, frame, line, setLine, ghost, shade, readout, verdict, sweep };
    }
  });
});
