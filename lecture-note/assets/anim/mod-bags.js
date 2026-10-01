/* The two bags (m05). Mounted by the lecture note (m05-clustering/01-concepts.qmd)
   and by the m05 deck (slides/m05/m05-clustering.md), which is why it lives here
   rather than inline in the page. Markup is in each of those two files; the
   paper, the pen, the motion and the sequencer come from assets/anim.css +
   assets/anim.js, and everything a scene calls arrives on `ctx`. The kit is
   loaded after this file, hence the animReady queue.

   On a slide (window.animStepOnly) the stage says less: each scene's `short`
   note replaces the paragraph, and the few on-canvas strings that name the
   note's purple/orange, or carry an em-dash, take their deck wording from T().
   The deck's theme maps the kit's accent/amber to its own blue/red. */
(window.animReady = window.animReady || []).push(function () {

  /* On a slide the stage is driven by hand and names the deck's colours. */
  const DECK = !!window.animStepOnly;
  const T = (note, deck) => (DECK ? deck : note);

  /* ---------------------------------------------------------------- data ---
     Every number below was computed once, offline, and pasted in. Nothing
     here runs a graph algorithm; the only arithmetic at run time is score(),
     which re-adds twenty edges and twelve degrees whenever the reader
     recolours a node.

     The network: 12 nodes, 20 edges. Group A (0–5) is a hub with five spokes,
     a 4-cycle around it and one leaf; group B (6–11) is the triangular prism,
     every node degree 3. Two edges cross between the groups.

       degrees   [5,3,4,4,3,1, 4,3,4,3,3,3]  — hub k=5, leaf k=1, sum 40 = 2m
       m = 20, 2m = 40
       internal edges 18, volumes 20 and 20
       observed = 18/20                        = 0.900
       by luck  = (20/40)² + (20/40)²          = 0.500
       Q        = 0.900 − 0.500                = 0.400
     and 0.400 is what Q = (1/2m) Σ_ij (A_ij − k_i k_j/2m) δ(c_i,c_j) returns
     for this partition — checked term by term, not by eye. Paint every node
     one colour and the same two sums give 1.000 and 1.000, so Q = 0.000.
     Every one of the 4096 colourings a reader can click their way to was
     checked as well: three decimals never disagree with the subtraction.
     ------------------------------------------------------------------------ */
  const NODE = [
    [48,78],[15,20],[83,10],[88,132],[12,140],[48,42],
    [138,34],[216,84],[143,128],[153,60],[156,103],[189,83]];
  const EDGE = [
    [0,1],[0,2],[0,3],[0,4],[0,5],[1,2],[2,3],[3,4],
    [4,1],[6,7],[7,8],[8,6],[9,10],[10,11],[11,9],[6,9],
    [7,11],[8,10],[2,6],[3,8]];
  /* One control point per edge, pushed off the midpoint: strings, not wires. */
  const WOB = [
    [26.1,52.1],[71.6,47.1],[73.1,101.3],[24.3,105.7],[43.4,60.0],[48.1,8.7],
    [76.2,71.4],[49.3,129.2],[4.3,79.8],[181.2,52.5],[183.3,112.2],[148.3,80.6],
    [149.5,81.8],[174.9,97.0],[173.7,67.3],[149.2,44.9],[202.3,87.6],[153.2,117.4],
    [108.1,27.4],[115.9,135.6]];
  const DEG  = [5,3,4,4,3,1,4,3,4,3,3,3];
  const HOME = [0,0,0,0,0,0,1,1,1,1,1,1];
  const HUB = 0, LEAF = 5;

  /* Where the 20 strings lie in the real bag: x, y and a tumble angle. A
     jittered grid clipped to the pouch, so the pile looks poured. */
  const SLOT = [
    [29.5,190.2,-42.7],[49.6,189.8,-58.7],[67.4,191.3,23.0],[83.3,192.0,12.4],[28.6,209.7,19.4],
    [46.8,207.9,-20.9],[66.6,211.7,-7.0],[83.0,208.6,55.9],[33.0,230.3,45.8],[49.8,227.5,-33.9],
    [69.0,225.6,-32.7],[85.6,226.9,-61.3],[32.2,243.0,33.3],[49.0,246.6,-66.1],[64.3,245.4,25.8],
    [82.7,244.3,65.1],[36.1,256.7,49.9],[48.3,257.5,-18.3],[66.3,258.6,44.5],[79.2,259.4,-53.1]];
  /* …and where the 40 loose balls lie in the shuffled bag. */
  const BALL = [
    [136.1,193.2],[148.2,192.9],[156.7,193.3],[165.6,193.0],[177.6,194.2],[185.7,192.2],[195.9,194.2],
    [208.5,191.2],[139.0,211.9],[147.7,210.5],[155.7,208.1],[167.1,208.2],[175.8,209.0],[185.1,209.9],
    [196.7,211.4],[207.0,210.6],[138.4,227.6],[147.8,226.1],[159.6,229.0],[168.6,227.8],[176.1,225.9],
    [185.5,225.3],[197.0,226.6],[207.0,226.5],[142.2,245.4],[147.4,242.8],[160.1,243.9],[169.4,243.6],
    [174.8,244.5],[186.7,243.1],[192.9,243.3],[205.5,245.0],[141.1,258.0],[149.4,257.2],[160.6,257.7],
    [168.0,258.8],[175.0,259.9],[183.1,259.6],[191.5,258.7],[200.2,258.1]];
  /* Which node each ball fell out of — node i owns DEG[i] of them, and they
     are scattered through the pile, because mixing them is the whole point. */
  const OWNER = [1,3,4,0,7,9,8,10,3,2,0,0,2,9,2,6,4,5,8,9,6,3,7,7,8,11,6,1,1,4,10,11,0,0,8,6,2,10,11,3];
  /* The order scene 2 empties the real bag in: the two mismatched strings come
     out 7th and 15th rather than last. */
  const ORDER = [4,9,6,5,14,17,18,1,2,15,10,3,12,7,19,13,0,16,11,8];
  /* Scene 4's twenty draws from the shuffled bag, with replacement, drawn once
     with a fixed seed. They give 11 matches — 0.550, not the exact 0.500, and
     the widget says so rather than pretending a sample is an expectation. */
  const DRAW = [
    [14,23],[24,8],[12,2],[5,8],[15,32],[13,25],[1,29],
    [31,29],[24,31],[36,12],[25,5],[31,14],[1,17],[33,26],
    [30,24],[7,16],[6,4],[24,39],[24,6],[3,21]];
  const DRAW_HITS = 11;

  const N = NODE.length, M = EDGE.length, TWOM = 2 * M;
  const col = HOME.slice();          /* the live partition */

  /* The two bars, for whatever the colours currently are. */
  function score() {
    let hit = 0;
    for (let e = 0; e < M; e++) if (col[EDGE[e][0]] === col[EDGE[e][1]]) hit++;
    const v = [0, 0];
    for (let i = 0; i < N; i++) v[col[i]] += DEG[i];
    const obs = hit / M;
    const luck = (v[0] / TWOM) * (v[0] / TWOM) + (v[1] / TWOM) * (v[1] / TWOM);
    return { hit: hit, v: v, obs: obs, luck: luck, q: obs - luck };
  }
  const d3 = (x) => x.toFixed(3);
  const EMPTY = T("—", "&nbsp;");     /* a value not yet shown */

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Every edge is two balls on a string",
      short: "Every edge is a string with two balls. All 20 go into the first bag.",
      note: "Twelve people, twenty friendships, and a guess at the two groups. Every edge is two coloured balls joined by a string — the colour is the group its node is in. Peel all twenty off and drop them in the first bag. The network does not move: the bag is a copy.",
      async run(ctx) {
        ctx.build();
        const c = ctx.card("the real bag");
        [["nodes", "12"], ["edges = strings", "20"], [T("colours", "colors"), "2"]].forEach((row, i) => {
          const t = ctx.el("div", "anim-tally anim-fade",
            "<span>" + row[0] + "</span><b>" + row[1] + "</b>");
          t.style.animationDelay = ctx.fast() ? "0s" : (1.4 + i * 0.35) + "s";
          c.appendChild(t);
        });
        await ctx.sleep(2600);
        await ctx.tumble();
        const last = ctx.el("div", "anim-caption anim-fade",
          "twenty strings in the bag, still tied");
        c.appendChild(last);
        await ctx.sleep(1400);
      }
    },
    {
      label: "Do the two ends match?",
      short: "Draw every string: 18 of the 20 have matching ends. Observed: 0.900.",
      note: "Empty the real bag one string at a time — there are only twenty, so take them all rather than sampling — and ask the one question modularity asks of an edge: are the two ends the same colour? Eighteen of the twenty are. Observed = 18/20 = 0.900.",
      async run(ctx) {
        const c = ctx.card("draw all twenty strings");
        const tal = ctx.tally(c, "✓ ends match", "✗ ends differ");
        const show = { obs: false, luck: false, q: false };
        const sync = ctx.bars(c, show);
        sync();

        for (let k = 0; k < M; k++) {
          const e = ORDER[k];
          ctx.pingSlot(e);
          tal.add(col[EDGE[e][0]] === col[EDGE[e][1]]);
          await ctx.sleep(215);
        }
        await ctx.sleep(500);
        show.obs = true;
        sync();
        await ctx.sleep(2000);
      }
    },
    {
      label: "Cut the strings: k edges, k balls",
      short: "Cut the strings. A node with k edges drops k balls: 40 in all.",
      note: "Now cut every string — but watch it happen node by node. The hub has five edges, so it leaves five balls. The leaf has one, so it leaves one. Forty ball-ends in the second bag, twenty of each colour: the degrees survive the shuffle and nothing else does.",
      async run(ctx) {
        const c = ctx.card("the shuffled bag");
        c.appendChild(ctx.el("div", "anim-quote", "a node with k edges leaves k balls"));
        const live = ctx.el("div", "anim-tally", "<span>balls in the bag</span><b>0</b>");
        c.appendChild(live);
        const count = live.querySelector("b");
        let n = 0;
        const drop = (node, hold) => ctx.rain(node, hold, () => { count.textContent = ++n; });

        await ctx.snip();
        await ctx.sleep(300);

        const row = (k, v) => {
          const t = ctx.el("div", "anim-tally anim-fade",
            "<span>" + k + "</span><b>" + v + "</b>");
          c.appendChild(t);
          return t;
        };

        await drop(HUB, 250);
        row("the hub, k = 5", "5 balls");
        await ctx.sleep(900);

        await drop(LEAF, 250);
        row("the leaf, k = 1", "1 ball");
        await ctx.sleep(900);

        for (let i = 0; i < N; i++) {
          if (i === HUB || i === LEAF) continue;
          await drop(i, 60);
          await ctx.sleep(110);
        }
        await ctx.sleep(400);
        row("12 nodes", "40 balls");
        await ctx.sleep(500);
        c.appendChild(ctx.el("div", "anim-caption anim-fade",
          T("20 purple, 20 orange — one ball per edge-end", "20 blue, 20 red: one ball per edge end")));
        await ctx.sleep(1800);
      }
    },
    {
      label: "Draw two balls, put them back",
      short: "Draw two balls and put them back. The exact chance of a match: 0.500.",
      note: "Reach into the shuffled bag, take two balls, note the colours, put them back. Twenty draws gave 11 matches here — but keep drawing forever and the answer settles at (20/40)² + (20/40)² = 0.500. That is what your own degrees hand you with the groups blindfolded.",
      async run(ctx) {
        const c = ctx.card("draw pairs from the shuffled bag");
        const tal = ctx.tally(c, T("✓ same colour", "✓ same color"), "✗ different");
        const show = { obs: true, luck: false, q: false };
        const sync = ctx.bars(c, show);
        sync();

        for (let k = 0; k < DRAW.length; k++) {
          const p = DRAW[k];
          ctx.pingBall(p[0]);
          ctx.pingBall(p[1]);
          tal.add(col[OWNER[p[0]]] === col[OWNER[p[1]]]);
          await ctx.sleep(240);
        }
        await ctx.sleep(400);
        c.appendChild(ctx.el("div", "anim-caption anim-fade",
          "this sample: " + DRAW_HITS + " of " + DRAW.length + " = " +
          d3(DRAW_HITS / DRAW.length) +
          T(". Keep drawing and it settles on the exact chance — and the exact chance is what the bar shows.",
            ". The bar shows the exact chance, 0.500.")));
        await ctx.sleep(1100);
        show.luck = true;
        sync();
        await ctx.sleep(2200);
      }
    },
    {
      label: "Q is the gap between the bars",
      short: "Q is the gap: 0.900 − 0.500 = 0.400.",
      note: "Slide the two bars together. Modularity is the hatched gap: what you observed, minus what luck would have given you. Q = 0.900 − 0.500 = 0.400. The cut was imaginary — the network still has every string it started with.",
      async run(ctx) {
        ctx.mend();
        const c = ctx.card("observed minus luck");
        const show = { obs: true, luck: true, q: false };
        const sync = ctx.bars(c, show);
        sync();
        await ctx.sleep(1200);
        show.q = true;
        sync();
        await ctx.sleep(900);
        c.appendChild(ctx.el("div", "anim-quote anim-fade",
          "Q = 0.900 − 0.500 = 0.400"));
        await ctx.sleep(700);
        c.appendChild(ctx.el("div", "anim-caption anim-fade",
          "the same number the formula gives: Q = (1/2m) Σ (A<sub>ij</sub> − k<sub>i</sub>k<sub>j</sub>/2m) δ(c<sub>i</sub>,c<sub>j</sub>)"));
        await ctx.sleep(2600);
      }
    },
    {
      label: T("Now you move the colours", "Now you move the colors"),
      short: "Click a node to change its color, and watch both bars.",
      note: "Your turn. Click any node in the drawing to change its colour and watch which bar moves. Paint everything one colour and the observed bar goes to 1.000 — every string matches — but the luck bar goes to 1.000 too, and Q collapses to 0.000. Clicking one node and watching Q move is Louvain's local-moving step, run by hand.",
      async run(ctx) {
        const c = ctx.card("your turn");
        const show = { obs: true, luck: true, q: true };
        const sync = ctx.bars(c, show);
        ctx.setLive(sync);
        sync();

        c.appendChild(ctx.el("div", "anim-caption",
          T("click any node to change its colour — both bars recount", "click a node to change its color; both bars recount")));
        const act = ctx.el("div", "mb-act");
        const ONE = T("paint everything one colour", "paint everything one color");
        const btn = ctx.el("button", "anim-btn", ONE);
        btn.type = "button";
        /* Inside the aria-hidden canvas, exactly like the kit's knob: a
           tabbable control here would announce nothing. The scene note says
           what the button does. */
        btn.tabIndex = -1;
        let saved = null;
        btn.addEventListener("click", function () {
          ctx.touched();
          if (saved) {
            for (let i = 0; i < N; i++) col[i] = saved[i];
            saved = null;
            btn.textContent = ONE;
          } else {
            saved = col.slice();
            for (let i = 0; i < N; i++) col[i] = 0;
            btn.textContent = T("put the colours back", "put the colors back");
          }
          ctx.repaint();
          sync();
        });
        act.appendChild(btn);
        c.appendChild(act);

        if (ctx.fast()) return;

        /* One demonstration move, then the widget belongs to the reader. */
        await ctx.sleep(1500);
        if (ctx.was()) return;
        const say = ctx.el("div", "anim-caption anim-fade",
          "watch: send the hub across on its own →");
        c.appendChild(say);
        await ctx.sleep(1200);
        if (ctx.was()) return;
        ctx.flip(HUB);
        sync();
        await ctx.sleep(2400);
        if (ctx.was()) return;
        say.innerHTML = T("five strings broken, and the luck bar barely noticed: Q fell to 0.119",
                          "five strings broken: Q fell to 0.119");
        await ctx.sleep(2600);
        if (ctx.was()) return;
        ctx.flip(HUB);
        sync();
        say.innerHTML = "put it back, and Q returns to 0.400. Your turn.";
      }
    }
  ];

  mountScenes(document.getElementById("mod-bags"), scenes, {
    stepsLabel: "Modularity steps",
    /* The last scene hands the widget to the reader; looping back to scene 1
       would take it away again mid-click. Replay restarts it. */
    loop: false,

    /* The things only this animation has: one drawing that survives all six
       scenes — network on top, two bags underneath — and a card on the right
       that each scene rewrites. Built once at mount, handed to every scene. */
    helpers(ctx) {
      const draw = ctx.$("[data-mb-draw]");
      const side = ctx.$("[data-mb-side]");
      const S = {};
      let live = null;        /* the live scene's sync(), or null */
      let touched = false;    /* the reader has taken over */

      const at = (n) => NODE[n][0] + " " + NODE[n][1];
      const edgeD = (e) => "M " + at(EDGE[e][0]) + " Q " + WOB[e][0] + " " + WOB[e][1] +
        " " + at(EDGE[e][1]);
      const mid = (e) => [(NODE[EDGE[e][0]][0] + NODE[EDGE[e][1]][0]) / 2,
                          (NODE[EDGE[e][0]][1] + NODE[EDGE[e][1]][1]) / 2];
      const tr = (x, y, rot, sc) => "translate(" + x + "px," + y + "px) rotate(" +
        (rot || 0) + "deg) scale(" + (sc == null ? 1 : sc) + ")";

      /* Set a transform now or set it with motion, depending on whether the
         reader is watching or has skipped ahead. */
      function pose(el, transform, opacity) {
        if (ctx.fast()) el.classList.add("mb-now");
        el.style.transform = transform;
        el.style.opacity = opacity;
        if (ctx.fast()) {
          el.getBoundingClientRect();          /* commit before re-arming */
          el.classList.remove("mb-now");
        }
      }

      /* A hand-drawn pouch, twice: x0 is its left edge. */
      const pouch = (x0) =>
        "M " + (x0 + 2) + ",174 C " + (x0 + 20) + ",166 " + (x0 + 42) + ",180 " + (x0 + 62) + ",172" +
        " C " + (x0 + 78) + ",166 " + (x0 + 94) + ",176 " + (x0 + 102) + ",174" +
        " C " + (x0 + 107) + ",212 " + (x0 + 102) + ",254 " + (x0 + 94) + ",270" +
        " C " + (x0 + 68) + ",278 " + (x0 + 36) + ",278 " + (x0 + 10) + ",270" +
        " C " + (x0 + 2) + ",254 " + (x0 - 3) + ",212 " + (x0 + 2) + ",174 Z";

      /* Scene 1 builds the drawing; scenes 2–6 only ever mutate it. Separate
         <g>s so the balls land inside the bags and the network keeps its own
         stacking without any z fiddling. */
      function build() {
        draw.textContent = "";
        for (let i = 0; i < N; i++) col[i] = HOME[i];
        live = null;
        touched = false;

        const svg = ctx.svgRoot("0 0 230 286");
        const g = () => svg.appendChild(ctx.svgEl("g"));
        const gBag = g(), gStr = g(), gBall = g(), gEdge = g(), gNode = g(), gTop = g();
        const slow = !ctx.fast();

        [[6, "the real bag"], [120, "the shuffled bag"]].forEach(function (b) {
          gBag.appendChild(ctx.svgEl("path", { d: pouch(b[0]), "class": "mb-pouch" }));
          gBag.appendChild(ctx.svgEl("path", {
            d: "M " + (b[0] + 8) + ",186 C " + (b[0] + 34) + ",194 " + (b[0] + 70) + ",194 " +
               (b[0] + 96) + ",186",
            "class": "mb-seam"
          }));
          const t = ctx.svgEl("text", {
            x: b[0] + 52, y: 166, "class": "anim-label", "text-anchor": "middle"
          });
          t.textContent = b[1];
          gBag.appendChild(t);
        });

        S.edge = EDGE.map(function (e, i) {
          const p = ctx.svgEl("path", {
            d: edgeD(i), "class": "anim-edge" + (slow ? " anim-draw" : "")
          });
          if (slow) {
            /* --dash must clear the path's own length or the line pops in
               late instead of drawing; a bowed string is longer than its
               chord, hence the 1.25. */
            const L = Math.hypot(NODE[e[0]][0] - NODE[e[1]][0], NODE[e[0]][1] - NODE[e[1]][1]);
            p.style.setProperty("--dash", Math.ceil(L * 1.25) + 4);
            p.style.animationDelay = (0.15 + i * 0.045) + "s";
          }
          return gEdge.appendChild(p);
        });

        S.node = NODE.map(function (q, i) {
          const n = ctx.svgEl("circle", { cx: q[0], cy: q[1], r: 6.5, "class": "anim-node" });
          n.addEventListener("click", function () {
            if (!live) return;
            touched = true;
            flip(i);
            live();
          });
          return gNode.appendChild(n);
        });

        /* One string per edge, parked at its edge's midpoint and invisible,
           waiting for scene 1 to tumble it into the bag. */
        S.str = EDGE.map(function (e, s) {
          const grp = ctx.svgEl("g", { "class": "mb-fly" });
          grp.appendChild(ctx.svgEl("path", { d: "M -7.5,0 Q 0,-3.6 7.5,0", "class": "mb-string" }));
          const ba = ctx.svgEl("circle", { cx: -7.5, cy: 0, r: 3.6, "class": "mb-ball" });
          const bb = ctx.svgEl("circle", { cx: 7.5, cy: 0, r: 3.6, "class": "mb-ball" });
          grp.appendChild(ba);
          grp.appendChild(bb);
          const m = mid(s);
          grp.style.transform = tr(m[0], m[1], 0, 0.45);
          grp.style.opacity = 0;
          gStr.appendChild(grp);
          return { g: grp, a: ba, b: bb };
        });

        /* …and one ball per edge-end, parked on the node it belongs to. */
        S.ball = BALL.map(function (p, b) {
          const c = ctx.svgEl("circle", { cx: 0, cy: 0, r: 4.1, "class": "mb-ball mb-fly" });
          c.style.transform = tr(NODE[OWNER[b]][0], NODE[OWNER[b]][1], 0, 0.5);
          c.style.opacity = 0;
          return gBall.appendChild(c);
        });

        S.svg = svg;
        S.top = gTop;
        /* repaint() owns the class attribute of every coloured thing, so the
           nodes are coloured first and only then decorated with the fade —
           otherwise the first repaint strips the animation before it runs. */
        repaint();
        if (slow) {
          S.node.forEach(function (n, i) {
            n.classList.add("anim-fade");
            n.style.animationDelay = (0.9 + i * 0.05) + "s";
          });
        }
        draw.appendChild(svg);
        draw.appendChild(ctx.el("div", "anim-caption",
          "12 nodes · 20 edges · m = 20, so 2m = 40 ball-ends"));
      }

      /* Colour is state, so every colour-carrying element is repainted from
         one place: nodes, the balls on the strings, and the loose balls. */
      function repaint() {
        for (let i = 0; i < N; i++) S.node[i].setAttribute("class", "anim-node mb-c" + col[i]);
        for (let b = 0; b < TWOM; b++) {
          S.ball[b].setAttribute("class", "mb-ball mb-fly mb-c" + col[OWNER[b]]);
        }
        for (let s = 0; s < M; s++) {
          S.str[s].a.setAttribute("class", "mb-ball mb-c" + col[EDGE[s][0]]);
          S.str[s].b.setAttribute("class", "mb-ball mb-c" + col[EDGE[s][1]]);
        }
      }

      function flip(i) {
        col[i] = 1 - col[i];
        repaint();
        ping(NODE[i][0], NODE[i][1], 9);
      }

      /* A ring that blinks once and removes itself. It goes straight into
         gTop, which carries no transform of its own, so --px/--py land in
         plain viewBox units. */
      function ping(x, y, r) {
        if (ctx.fast()) return;
        const c = ctx.svgEl("circle", { r: r || 5, "class": "mb-ping" });
        c.style.setProperty("--px", x + "px");
        c.style.setProperty("--py", y + "px");
        S.top.appendChild(c);
        setTimeout(function () { c.remove(); }, 700);
      }

      const pingSlot = (e) => ping(SLOT[e][0], SLOT[e][1], 10);
      const pingBall = (b) => ping(BALL[b][0], BALL[b][1], 5.5);

      /* Scene 1: the strings peel off the network and tumble into the bag. */
      async function tumble() {
        for (let k = 0; k < M; k++) {
          const s = ORDER[k];
          pose(S.str[s].g, tr(SLOT[s][0], SLOT[s][1], SLOT[s][2], 1), 1);
          await ctx.sleep(150);
        }
        await ctx.sleep(500);
      }

      /* Scene 3: scissors cross the drawing, and every string they pass goes
         slack. Nothing is destroyed — mend() puts them all back. */
      async function snip() {
        const g = ctx.svgEl("g");
        g.appendChild(ctx.svgEl("path", { d: "M -1,0 L 12,-5.5", "class": "mb-tool" }));
        g.appendChild(ctx.svgEl("path", { d: "M -1,0 L 12,5.5", "class": "mb-tool" }));
        g.appendChild(ctx.svgEl("path", { d: "M -1,0 L -4.5,-3.5", "class": "mb-tool" }));
        g.appendChild(ctx.svgEl("path", { d: "M -1,0 L -4.5,3.5", "class": "mb-tool" }));
        g.appendChild(ctx.svgEl("circle", { cx: -7, cy: -5, r: 3.4, "class": "mb-tool" }));
        g.appendChild(ctx.svgEl("circle", { cx: -7, cy: 5, r: 3.4, "class": "mb-tool" }));
        S.top.appendChild(g);
        const cut = (x) => S.edge.forEach(function (p, e) {
          if (mid(e)[0] <= x) p.setAttribute("class", "anim-edge mb-cut");
        });
        if (ctx.fast()) {
          cut(999);
          g.remove();
          return;
        }
        for (let k = 0; k <= 24; k++) {
          const x = -14 + (250 * k) / 24;
          g.style.transform = tr(x, 74 + 5 * Math.sin(k / 2));
          cut(x);
          await ctx.sleep(70);
        }
        g.remove();
      }

      function mend() {
        S.edge.forEach(function (p) { p.setAttribute("class", "anim-edge"); });
      }

      /* Scene 3, the fact everything downstream rests on: node i lets go of
         exactly DEG[i] balls. */
      async function rain(node, hold, each) {
        ping(NODE[node][0], NODE[node][1], 11);
        for (let b = 0; b < TWOM; b++) {
          if (OWNER[b] !== node) continue;
          pose(S.ball[b], tr(BALL[b][0], BALL[b][1]), 1);
          if (each) each();
          await ctx.sleep(hold);
        }
      }

      function card(title) {
        side.textContent = "";
        const c = ctx.el("div", "anim-panel anim-pop");
        if (title) c.appendChild(ctx.el("div", "anim-caption", title));
        side.appendChild(c);
        return c;
      }

      /* A two-column tally board: ticks on the left, crosses on the right. */
      function tally(c, yes, no) {
        const w = ctx.el("div", "mb-tal",
          '<div class="mb-tal-col"><div class="mb-tal-h">' + yes + '</div>' +
          '<div class="mb-tal-m" data-y></div><div class="mb-tal-n" data-yn>0</div></div>' +
          '<div class="mb-tal-col"><div class="mb-tal-h">' + no + '</div>' +
          '<div class="mb-tal-m" data-n></div><div class="mb-tal-n" data-nn>0</div></div>');
        c.appendChild(w);
        const box = [w.querySelector("[data-y]"), w.querySelector("[data-n]")];
        const num = [w.querySelector("[data-yn]"), w.querySelector("[data-nn]")];
        const seen = [0, 0];
        return {
          add: function (isYes) {
            const k = isYes ? 0 : 1;
            const m = ctx.el("i", isYes ? "anim-pop" : "anim-pop mb-x", isYes ? "✓" : "✗");
            box[k].appendChild(m);
            num[k].textContent = ++seen[k];
          }
        };
      }

      /* The two bars and the hatched gap. `show` is read on every sync, so a
         scene can reveal one bar, then the other, then the gap. */
      function bars(c, show) {
        const w = ctx.el("div", "mb-bars",
          '<div class="mb-row"><span>observed</span>' +
            '<span class="mb-track"><i class="mb-obs" data-obs></i></span>' +
            '<b class="mb-val" data-obsv>' + EMPTY + '</b></div>' +
          '<div class="mb-sub"><span></span><em data-obsx>&nbsp;</em><span></span></div>' +
          '<div class="mb-row"><span>Q</span>' +
            '<span class="mb-gap"><i class="mb-hatch" data-hatch></i></span>' +
            '<b class="mb-val" data-qv>&nbsp;</b></div>' +
          '<div class="mb-row"><span>' + T("by luck", "by chance") + '</span>' +
            '<span class="mb-track"><i class="mb-luck" data-luck></i></span>' +
            '<b class="mb-val" data-luckv>' + EMPTY + '</b></div>' +
          '<div class="mb-sub"><span></span><em data-luckx>&nbsp;</em><span></span></div>');
        c.appendChild(w);
        const q = (sel) => w.querySelector(sel);
        const obs = q("[data-obs]"), obsv = q("[data-obsv]"), obsx = q("[data-obsx]");
        const lck = q("[data-luck]"), lckv = q("[data-luckv]"), lckx = q("[data-luckx]");
        const hat = q("[data-hatch]"), qv = q("[data-qv]");

        return function sync() {
          const s = score();
          if (show.obs) {
            obs.style.width = (s.obs * 100) + "%";
            obsv.textContent = d3(s.obs);
            obsx.innerHTML = s.hit + " of 20 strings match";
          }
          if (show.luck) {
            lck.style.width = (s.luck * 100) + "%";
            lckv.textContent = d3(s.luck);
            lckx.innerHTML = "(" + s.v[0] + "/40)² + (" + s.v[1] + "/40)²";
          }
          if (show.q) {
            hat.style.opacity = 1;
            hat.style.left = (Math.min(s.obs, s.luck) * 100) + "%";
            hat.style.width = (Math.abs(s.obs - s.luck) * 100) + "%";
            qv.textContent = d3(s.q);
          }
          return s;
        };
      }

      return {
        build: build, repaint: repaint, flip: flip, tumble: tumble, snip: snip,
        mend: mend, rain: rain, card: card, tally: tally, bars: bars,
        pingSlot: pingSlot, pingBall: pingBall,
        setLive: function (sync) { live = sync; S.svg.classList.add("mb-live"); },
        touched: function () { touched = true; },
        was: function () { return touched; }
      };
    }
  });
});
