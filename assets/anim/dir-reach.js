/* ==========================================================================
   dir-reach.js — Strong and weak, on a triangle you can re-point.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Mounted by slides/m01/m01-euler-tour.md. The deck shows strong and weak on
   two separate figures, which makes them look like two graphs. They are one
   graph and two questions, and the difference is one arrowhead — so the stage
   hands the arrowheads to the room. Flip any of the three and watch which
   verdict moves.
   ========================================================================== */

(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     The same three nodes as figures/directed-strong.png and directed-weak.png
     (make_figures.py's DIR_POS), mapped from its data units into a 360 x 240
     box by x -> 180 + 120x, y -> 140 - 120y.

     BASE is the cycle the deck draws: A->B, B->C, C->A. A configuration is a
     three-bit mask; bit i set means arc i points the other way, so the eight
     masks are the eight ways to orient this triangle.
     ------------------------------------------------------------------------ */
  const NAME = ["A", "B", "C"];
  const POS = [[180, 50], [284, 185], [76, 185]];
  const MID = [180, 140];
  const BASE = [[0, 1], [1, 2], [2, 0]];
  const R = 18;

  /* For each of the eight orientations: which nodes each node can reach, as a
     bitmask (bit 0 = A, 1 = B, 2 = C; the node itself is not counted), and
     whether the orientation is strongly connected. Computed once by a
     breadth-first search per source over all 8 x 3 cases and written down —
     nothing here searches at page load.

     The number worth keeping: 2 of the 8. Only the two orientations that run
     all the way round are strongly connected. Every one of the eight is weakly
     connected, because ignoring direction leaves the same triangle. */
  const REACH = [
    [6, 5, 3],   /* 0  A->B B->C C->A   the deck's cycle */
    [0, 5, 1],   /* 1 */
    [2, 0, 3],   /* 2 */
    [0, 1, 3],   /* 3 */
    [6, 4, 0],   /* 4  A->B B->C A->C   scene 3's flip */
    [4, 5, 0],   /* 5 */
    [6, 0, 2],   /* 6 */
    [6, 5, 3]    /* 7  the other cycle, the deck's run backwards */
  ];
  const STRONG = [1, 0, 0, 0, 0, 0, 0, 1];
  const STRONG_N = 2;

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Three nodes, three arrows",
      note: "Point the edges one way and the one question becomes two.",
      async run(ctx) {
        ctx.idle();
        ctx.draw(0);
        ctx.card("two questions now");
        await ctx.sleep(1700);
        ctx.tally("with the arrows", "strongly connected?");
        await ctx.sleep(1400);
        ctx.tally("without them", "weakly connected?");
        await ctx.sleep(2600);
      }
    },
    {
      label: "Every node reaches every node",
      note: "Every node reaches every node. This orientation is strongly connected.",
      async run(ctx) {
        ctx.idle();
        ctx.set(0);
        ctx.card("follow the arrows");
        for (let s = 0; s < 3; s++) {
          await ctx.flood(s);
          ctx.row(s);
          await ctx.sleep(800);
        }
        ctx.clearFlood();
        ctx.verdict();
        await ctx.sleep(3000);
      }
    },
    {
      label: "Turn one arrow round",
      note: "Turn C→A round, and nothing else. Now C reaches nobody, and strong is gone.",
      async run(ctx) {
        ctx.idle();
        ctx.set(0);
        ctx.card("one arrowhead");
        await ctx.sleep(900);
        ctx.flip(2);
        ctx.mark(2);
        await ctx.sleep(1400);
        for (let s = 0; s < 3; s++) {
          await ctx.flood(s);
          ctx.row(s);
          await ctx.sleep(700);
        }
        ctx.clearFlood();
        ctx.verdict();
        await ctx.sleep(3200);
      }
    },
    {
      label: "Now rub the arrowheads out",
      note: "Arrowheads off, still one piece — weakly connected either way.",
      async run(ctx) {
        ctx.idle();
        ctx.set(4);
        ctx.card("ignore direction");
        await ctx.sleep(900);
        ctx.undirected(true);
        await ctx.sleep(1500);
        ctx.tally("one piece?", "yes — weakly connected");
        await ctx.sleep(1200);
        ctx.undirected(false);
        ctx.tally("arrows back", "still not strongly connected");
        await ctx.sleep(3200);
      }
    },
    {
      label: "Now you try — flip any arrow",
      note: "Your turn — flip any arrow. Only two of the eight orientations survive.",
      async run(ctx) {
        ctx.set(0);
        ctx.card("your orientation");
        ctx.hand();
        if (ctx.fast()) return;
        await ctx.sleep(17000);
        ctx.idle();
      }
    }
  ];

  mountScenes(document.getElementById("dir-reach"), scenes, {
    stepsLabel: "Reachability steps",

    helpers(ctx) {
      const mapBox = ctx.$("[data-dr-map]");
      const side = ctx.$("[data-dr-side]");
      const S = { mask: 0, lit: 0, live: false, grabbed: false, seen: {}, found: {} };

      /* Where arc i actually runs, given the mask. */
      const arcOf = (i) => ((S.mask >> i) & 1)
        ? [BASE[i][1], BASE[i][0]]
        : [BASE[i][0], BASE[i][1]];

      /* An arc bows away from the middle of the triangle, so the three of them
         make a ring rather than three chords through each other. */
      function geo(i) {
        const a = arcOf(i);
        const p = POS[a[0]], q = POS[a[1]];
        const mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2;
        const ox = mx - MID[0], oy = my - MID[1], om = Math.hypot(ox, oy) || 1;
        const cx = mx + (ox / om) * 34, cy = my + (oy / om) * 34;
        const trim = (f, pad) => {
          const ux = cx - f[0], uy = cy - f[1], m = Math.hypot(ux, uy) || 1;
          return [f[0] + (ux / m) * pad, f[1] + (uy / m) * pad];
        };
        const s = trim(p, R + 3), t = trim(q, R + 11);
        return { s: s, t: t, c: [cx, cy] };
      }

      function headPoints(G) {
        const ax = G.t[0] - G.c[0], ay = G.t[1] - G.c[1], m = Math.hypot(ax, ay) || 1;
        const ux = ax / m, uy = ay / m;
        return [
          (G.t[0] + ux * 10) + "," + (G.t[1] + uy * 10),
          (G.t[0] - uy * 8) + "," + (G.t[1] + ux * 8),
          (G.t[0] + uy * 8) + "," + (G.t[1] - ux * 8)
        ].join(" ");
      }

      /* ------------------------------------------------------------- the map */
      function draw(mask) {
        S.mask = mask;
        mapBox.textContent = "";
        const svg = ctx.svgRoot("0 0 360 240");
        const g = () => svg.appendChild(ctx.svgEl("g"));
        const gArc = g(), gNode = g(), gText = g(), gHit = g();

        S.arcs = [];
        S.heads = [];
        for (let i = 0; i < 3; i++) {
          S.arcs.push(gArc.appendChild(ctx.svgEl("path", { "class": "dr-arc" })));
          S.heads.push(gArc.appendChild(ctx.svgEl("polygon", { "class": "dr-head" })));
        }

        S.nodes = POS.map(function (p) {
          return gNode.appendChild(ctx.svgEl("circle",
            { cx: p[0], cy: p[1], r: R, "class": "dr-node" }));
        });
        /* The letters live in their own group, so paint() has to recolour them
           itself — a lit disc is dark and a dark letter on it disappears. */
        S.names = POS.map(function (p, i) {
          const t = ctx.svgEl("text",
            { x: p[0], y: p[1] + 7, "text-anchor": "middle", "class": "dr-name" });
          t.textContent = NAME[i];
          return gText.appendChild(t);
        });

        S.hits = [];
        for (let i = 0; i < 3; i++) {
          const h = ctx.svgEl("path", { "class": "dr-hit" });
          (function (k) {
            h.addEventListener("click", function () { onArc(k); });
          })(i);
          S.hits.push(gHit.appendChild(h));
        }

        S.svg = svg;
        mapBox.appendChild(svg);
        shape();
        clearFlood();
      }

      /* Lay the three arcs out for the current mask. Called on every flip. */
      function shape() {
        for (let i = 0; i < 3; i++) {
          const G = geo(i);
          const d = "M " + G.s[0] + " " + G.s[1] + " Q " + G.c[0] + " " + G.c[1] +
            " " + G.t[0] + " " + G.t[1];
          S.arcs[i].setAttribute("d", d);
          S.hits[i].setAttribute("d", d);
          S.heads[i].setAttribute("points", headPoints(G));
        }
      }

      /* Point the triangle a given way. Also drops whatever an earlier scene
         left on the arcs — the flip highlight and the arrowheads-off view are
         both scene-local, and a jump between steps must not carry them. */
      function set(mask) {
        S.mask = mask;
        for (let i = 0; i < 3; i++) {
          S.arcs[i].classList.remove("dr-flipped");
          S.heads[i].classList.remove("dr-flipped-fill");
        }
        if (S.svg) S.svg.classList.remove("dr-undirected");
        shape();
        clearFlood();
      }

      function flip(i) {
        S.mask ^= (1 << i);
        shape();
        clearFlood();
      }

      /* Scene 3 points at the arrow it just turned. */
      function mark(i) {
        S.arcs[i].classList.add("dr-flipped");
        S.heads[i].classList.add("dr-flipped-fill");
      }

      function clearFlood() {
        S.lit = 0;
        S.src = null;
        S.used = [];
        paint();
      }

      function paint() {
        S.nodes.forEach(function (c, i) {
          let cls = "dr-node";
          const on = (i === S.src) || !!((S.lit >> i) & 1);
          if (i === S.src) cls += " dr-src";
          else if ((S.lit >> i) & 1) cls += " dr-lit";
          c.setAttribute("class", cls);
          S.names[i].setAttribute("class", "dr-name" + (on ? " dr-name-on" : ""));
        });
        for (let i = 0; i < 3; i++) {
          const keep = S.arcs[i].classList.contains("dr-flipped");
          S.arcs[i].setAttribute("class", "dr-arc" +
            (S.used && S.used.indexOf(i) >= 0 ? " dr-on" : "") + (keep ? " dr-flipped" : ""));
        }
      }

      /* Light everything reachable from s, one round at a time. Three arcs, so
         the frontier loop is bookkeeping rather than a search — and REACH,
         above, is what the verdict is actually read off. */
      async function flood(s) {
        S.src = s;
        S.lit = 1 << s;
        S.used = [];
        paint();
        await ctx.sleep(420);
        for (let round = 0; round < 3; round++) {
          let grew = false;
          for (let i = 0; i < 3; i++) {
            const a = arcOf(i);
            if (((S.lit >> a[0]) & 1) && !((S.lit >> a[1]) & 1)) {
              S.lit |= (1 << a[1]);
              S.used.push(i);
              grew = true;
            }
          }
          if (!grew) break;
          paint();
          await ctx.sleep(560);
        }
      }

      /* ------------------------------------------------------------ the card */
      function card(title) {
        side.textContent = "";
        S.panel = ctx.el("div", "anim-panel anim-pop dr-card");
        if (title) S.panel.appendChild(ctx.el("div", "anim-caption", title));
        S.rows = ctx.el("div", "dr-rows");
        S.panel.appendChild(S.rows);
        side.appendChild(S.panel);
        S.said = {};
        S.vBox = null;
        return S.panel;
      }

      const bits = (m) => ((m & 1) + ((m >> 1) & 1) + ((m >> 2) & 1));
      const listOf = (m) => {
        const r = [];
        for (let i = 0; i < 3; i++) if ((m >> i) & 1) r.push(NAME[i]);
        return r.length ? r.join(", ") : "nobody";
      };

      /* One "X reaches ..." line, written once per source per scene and
         rewritten in place on every flip. */
      function row(s) {
        const m = REACH[S.mask][s];
        const line = S.said[s] || ctx.el("div", "dr-row anim-fade");
        line.innerHTML = "<b>" + NAME[s] + "</b> reaches <span>" + listOf(m) + "</span>";
        line.className = "dr-row anim-fade" + (bits(m) === 2 ? " dr-full" : " dr-short");
        if (!S.said[s]) {
          S.rows.appendChild(line);
          S.said[s] = line;
        }
      }

      function verdict() {
        const strong = !!STRONG[S.mask];
        if (!S.vBox) {
          S.vBox = ctx.el("div", "dr-verdict");
          S.panel.appendChild(S.vBox);
        }
        S.vBox.innerHTML = "";
        S.vBox.appendChild(ctx.el("div", "dr-flag anim-pop " + (strong ? "dr-yes" : "dr-no"),
          "<b>strongly connected</b><span>" + (strong ? "yes" : "no") + "</span>"));
        /* Weak never fails here: rubbing out the arrowheads leaves the same
           triangle whichever way the arcs point. */
        S.vBox.appendChild(ctx.el("div", "dr-flag anim-pop dr-yes",
          "<b>weakly connected</b><span>yes</span>"));
      }

      function tally(k, v) {
        S.rows.appendChild(ctx.el("div", "anim-tally anim-fade",
          "<span>" + k + "</span><b>" + v + "</b>"));
      }
      function quote(t) { S.panel.appendChild(ctx.el("div", "anim-quote anim-fade", t)); }

      function undirected(on) {
        if (!S.svg) return;
        S.svg.classList.toggle("dr-undirected", !!on);
      }

      /* -------------------------------------------------------- the clicks */
      function hand() {
        S.live = true;
        S.grabbed = false;
        S.seen = {};
        S.found = {};
        S.svg.classList.add("dr-clickable");
        for (let s = 0; s < 3; s++) row(s);
        verdict();
        S.msg = ctx.el("div", "dr-msg", "click any arrow to turn it round");
        S.panel.appendChild(S.msg);
        S.score = ctx.el("div", "anim-tally",
          "<span>orientations seen</span><b>1 of 8</b>");
        S.panel.appendChild(S.score);
        S.seen[S.mask] = 1;
        if (STRONG[S.mask]) S.found[S.mask] = 1;
        paint();
      }
      function idle() {
        S.live = false;
        if (S.svg) S.svg.classList.remove("dr-clickable");
      }
      function grab() {
        if (S.grabbed) return;
        S.grabbed = true;
        ctx.pause();
      }

      function onArc(i) {
        if (!S.live) return;
        grab();
        flip(i);
        for (let s = 0; s < 3; s++) row(s);
        verdict();
        S.seen[S.mask] = 1;
        if (STRONG[S.mask]) S.found[S.mask] = 1;
        const nSeen = Object.keys(S.seen).length;
        const nFound = Object.keys(S.found).length;
        S.score.querySelector("b").textContent = nSeen + " of 8";
        if (STRONG[S.mask]) {
          S.msg.className = "dr-msg";
          S.msg.innerHTML = nFound === STRONG_N
            ? "<b>both of them</b> — and both go all the way round"
            : "<b>strongly connected</b> — the arrows agree on one direction";
        } else {
          S.msg.className = "dr-msg dr-msg-no";
          S.msg.innerHTML = "not strongly connected — a node has no way out, or none in";
        }
      }

      return {
        draw: draw, set: set, flip: flip, mark: mark, flood: flood,
        clearFlood: clearFlood, card: card, row: row, verdict: verdict,
        tally: tally, quote: quote, undirected: undirected,
        hand: hand, idle: idle
      };
    }
  });
});
