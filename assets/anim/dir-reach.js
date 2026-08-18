/* ==========================================================================
   dir-reach.js — Strong and weak, on a town you can re-point.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Mounted by slides/m01/m01-euler-tour.md. The deck shows strong and weak on
   two separate figures, which makes them look like two graphs. They are one
   graph and two questions, and the difference is one arrowhead — so the stage
   hands the arrowheads to the room.

   It began as the deck's own three-node triangle, where all eight orientations
   fit on one screen and every single flip kills the strong verdict. That is
   tidy and it is boring: there is nothing to discover. Five corners and six
   streets give 64 orientations, six of them strongly connected, and — the
   thing the triangle cannot show — one street whose direction does not matter
   at all while the other five each break it on their own.
   ========================================================================== */

(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     Five corners on a circle of radius 115 about (210, 175), in a 420 x 340
     box: A at the top, then B, C, D, E clockwise. Six streets — the pentagon
     A-B-C-D-E-A, plus the chord B-E.

     A configuration is a six-bit mask; bit i set means street i points the
     other way, so the 64 masks are the 64 ways to point this town. The base
     orientation (mask 0) runs the pentagon A->B->C->D->E->A and the chord
     B->E.

     `bow` is how far the arc bends away from the middle. The chord bends less
     than the sides do: it is the longest street and the same bow would run its
     apex up under corner A.
     ------------------------------------------------------------------------ */
  const NAME = ["A", "B", "C", "D", "E"];
  const POS = [[210, 60], [319.4, 139.5], [277.6, 268], [142.4, 268], [100.6, 139.5]];
  /* Where each corner's reach count sits — radially outward, on a circle of
     154, so no badge lands on a street. */
  const BADGE = [[210, 26, "middle"], [358, 134, "start"], [302, 306, "middle"],
                 [118, 306, "middle"], [62, 134, "end"]];
  const MID = [210, 175];
  const BASE = [
    { u: 0, v: 1, bow: 30 },   /* 0  A–B */
    { u: 1, v: 2, bow: 30 },   /* 1  B–C */
    { u: 2, v: 3, bow: 30 },   /* 2  C–D */
    { u: 3, v: 4, bow: 30 },   /* 3  D–E */
    { u: 4, v: 0, bow: 30 },   /* 4  E–A */
    { u: 1, v: 4, bow: 22 }    /* 5  B–E, the chord */
  ];
  const R = 24;

  /* For each of the 64 orientations, how many of the other four corners each
     corner can reach. Four means it reaches everything; the orientation is
     strongly connected exactly when all five read four. Computed once by a
     breadth-first search per source over all 64 x 5 cases and written down —
     nothing here searches at page load.

     Six of the 64 come out strongly connected, and every one of the six has
     each corner sitting on a directed cycle. */
  const REACH = [
    [4,4,4,4,4], [0,4,3,2,1], [2,2,4,3,2], [0,2,4,2,1],   /*  0- 3 */
    [3,3,0,4,3], [0,3,0,3,1], [2,2,3,4,2], [0,2,3,4,1],   /*  4- 7 */
    [4,4,1,0,4], [0,4,1,0,2], [3,3,4,0,3], [0,3,4,0,2],   /*  8-11 */
    [4,4,0,1,4], [0,4,0,1,3], [4,4,4,4,4], [0,4,4,4,4],   /* 12-15 */
    [4,3,2,1,0], [1,4,2,1,0], [2,1,3,1,0], [1,2,4,1,0],   /* 16-19 */
    [3,2,0,2,0], [1,3,0,2,0], [2,1,2,3,0], [1,2,3,4,0],   /* 20-23 */
    [4,3,1,0,1], [2,4,1,0,1], [3,2,3,0,1], [2,3,4,0,1],   /* 24-27 */
    [4,3,0,1,2], [3,4,0,1,2], [4,3,3,3,3], [4,4,4,4,4],   /* 28-31 */
    [4,4,4,4,4], [0,4,4,4,4], [1,0,4,3,2], [0,1,4,3,2],   /* 32-35 */
    [2,1,0,4,3], [0,2,0,4,3], [1,0,1,4,2], [0,1,2,4,2],   /* 36-39 */
    [3,2,1,0,4], [0,3,1,0,4], [1,0,2,0,3], [0,1,3,0,3],   /* 40-43 */
    [2,1,0,1,4], [0,2,0,1,4], [1,0,1,2,4], [0,1,2,3,4],   /* 44-47 */
    [4,3,3,3,3], [4,4,4,4,4], [2,0,3,2,1], [2,2,4,3,2],   /* 48-51 */
    [3,1,0,3,2], [3,3,0,4,3], [2,0,1,3,1], [2,2,3,4,2],   /* 52-55 */
    [4,2,1,0,3], [4,4,1,0,4], [3,0,2,0,2], [3,3,4,0,3],   /* 56-59 */
    [4,1,0,1,3], [4,4,0,1,4], [4,0,1,2,3], [4,4,4,4,4]    /* 60-63 */
  ];
  const STRONG_N = 6;
  const strongAt = (m) => REACH[m].every(function (c) { return c === 4; });

  /* The playback's two flips, and why these two. From the base orientation the
     chord is the ONLY street whose direction does not matter — flip it and all
     five counts stay at four — while each of the five pentagon sides breaks
     the graph on its own. Then A–B on top of it leaves both of A's streets
     pointing in, so A's count falls to zero and the collapse is one number. */
  const FLIP_SAFE = 5;
  const FLIP_FATAL = 0;

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Five corners, six one-way streets",
      note: "The number beside a corner is how many of the other four you can reach from it.",
      async run(ctx) {
        ctx.idle();
        ctx.draw(0);
        ctx.card("all four, from everywhere");
        await ctx.sleep(1400);
        await ctx.reveal();
        ctx.verdict();
        await ctx.sleep(3000);
      }
    },
    {
      label: "What the number means",
      note: "Four out of four: from A the arrows take you to all of B, C, D and E.",
      async run(ctx) {
        ctx.idle();
        ctx.set(0);
        ctx.card("follow the arrows");
        ctx.reveal(true);
        await ctx.sleep(700);
        await ctx.flood(0);
        await ctx.sleep(1200);
        await ctx.flood(2);
        await ctx.sleep(1000);
        ctx.clearFlood();
        ctx.verdict();
        await ctx.sleep(2600);
      }
    },
    {
      label: "One street that does not matter",
      note: "Turn the chord round and every count stays at four. Some arrows are free.",
      async run(ctx) {
        ctx.idle();
        ctx.set(0);
        ctx.card("flip the chord");
        ctx.reveal(true);
        await ctx.sleep(1300);
        ctx.flip(FLIP_SAFE);
        ctx.mark(FLIP_SAFE);
        ctx.reveal(true);
        await ctx.sleep(1600);
        ctx.verdict();
        await ctx.sleep(3200);
      }
    },
    {
      label: "And one that does",
      note: "Turn A–B round too and both of A's streets point in — A reaches nobody. Weak survives.",
      async run(ctx) {
        ctx.idle();
        ctx.set(1 << FLIP_SAFE);
        ctx.card("now flip A–B");
        ctx.reveal(true);
        await ctx.sleep(1200);
        ctx.flip(FLIP_FATAL);
        ctx.mark(FLIP_FATAL);
        ctx.reveal(true);
        await ctx.sleep(1600);
        ctx.verdict();
        await ctx.sleep(1400);
        /* One beat with the arrowheads rubbed out: the same six streets are
           still one piece, so weak survives what strong does not. */
        ctx.undirected(true);
        await ctx.sleep(1800);
        ctx.undirected(false);
        await ctx.sleep(2200);
      }
    },
    {
      label: "Now you try — find all six",
      note: "Your turn. Click any street to turn it round; six of the 64 orientations work.",
      async run(ctx) {
        ctx.set(0);
        ctx.card("your town");
        ctx.reveal(true);
        ctx.hand();
        if (ctx.fast()) return;
        await ctx.sleep(20000);
        ctx.idle();
      }
    }
  ];

  mountScenes(document.getElementById("dir-reach"), scenes, {
    stepsLabel: "Reachability steps",

    helpers(ctx) {
      const mapBox = ctx.$("[data-dr-map]");
      const side = ctx.$("[data-dr-side]");
      const S = { mask: 0, lit: 0, live: false, grabbed: false, shown: false,
                  seen: {}, found: {}, used: [] };

      /* Where street i actually runs, given the mask. */
      const arcOf = (i) => ((S.mask >> i) & 1)
        ? [BASE[i].v, BASE[i].u]
        : [BASE[i].u, BASE[i].v];

      /* A street bends away from the middle of the town, so the six of them
         make a ring rather than six chords through each other. */
      function geo(i) {
        const a = arcOf(i);
        const p = POS[a[0]], q = POS[a[1]];
        const mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2;
        const ox = mx - MID[0], oy = my - MID[1], om = Math.hypot(ox, oy) || 1;
        const cx = mx + (ox / om) * BASE[i].bow, cy = my + (oy / om) * BASE[i].bow;
        const trim = (f, pad) => {
          const ux = cx - f[0], uy = cy - f[1], m = Math.hypot(ux, uy) || 1;
          return [f[0] + (ux / m) * pad, f[1] + (uy / m) * pad];
        };
        return { s: trim(p, R + 4), t: trim(q, R + 15), c: [cx, cy] };
      }

      function headPoints(G) {
        const ax = G.t[0] - G.c[0], ay = G.t[1] - G.c[1], m = Math.hypot(ax, ay) || 1;
        const ux = ax / m, uy = ay / m;
        return [
          (G.t[0] + ux * 13) + "," + (G.t[1] + uy * 13),
          (G.t[0] - uy * 9) + "," + (G.t[1] + ux * 9),
          (G.t[0] + uy * 9) + "," + (G.t[1] - ux * 9)
        ].join(" ");
      }

      /* ------------------------------------------------------------- the map */
      function draw(mask) {
        S.mask = mask;
        mapBox.textContent = "";
        const svg = ctx.svgRoot("0 0 420 340");
        const g = () => svg.appendChild(ctx.svgEl("g"));
        const gArc = g(), gNode = g(), gText = g(), gHit = g();

        S.arcs = [];
        S.heads = [];
        for (let i = 0; i < 6; i++) {
          S.arcs.push(gArc.appendChild(ctx.svgEl("path", { "class": "dr-arc" })));
          S.heads.push(gArc.appendChild(ctx.svgEl("polygon", { "class": "dr-head" })));
        }

        S.nodes = POS.map(function (p) {
          return gNode.appendChild(ctx.svgEl("circle",
            { cx: p[0], cy: p[1], r: R, "class": "dr-node" }));
        });
        /* The letters live in their own group, so paint() has to recolour them
           itself — a flooded disc is dark and a dark letter on it disappears. */
        S.names = POS.map(function (p, i) {
          const t = ctx.svgEl("text",
            { x: p[0], y: p[1] + 8, "text-anchor": "middle", "class": "dr-name" });
          t.textContent = NAME[i];
          return gText.appendChild(t);
        });
        /* The reach counts. This is where the verdict lives: five fours and the
           town is strongly connected, and the card only has to agree. */
        S.counts = BADGE.map(function (b) {
          return gText.appendChild(ctx.svgEl("text",
            { x: b[0], y: b[1], "text-anchor": b[2], "class": "dr-count anim-knockout" }));
        });

        S.hits = [];
        for (let i = 0; i < 6; i++) {
          const h = ctx.svgEl("path", { "class": "dr-hit" });
          (function (k) {
            h.addEventListener("click", function () { onArc(k); });
          })(i);
          S.hits.push(gHit.appendChild(h));
        }

        S.svg = svg;
        S.shown = false;
        mapBox.appendChild(svg);
        shape();
        clearFlood();
      }

      /* Lay the six streets out for the current mask. Called on every flip. */
      function shape() {
        for (let i = 0; i < 6; i++) {
          const G = geo(i);
          const d = "M " + G.s[0] + " " + G.s[1] + " Q " + G.c[0] + " " + G.c[1] +
            " " + G.t[0] + " " + G.t[1];
          S.arcs[i].setAttribute("d", d);
          S.hits[i].setAttribute("d", d);
          S.heads[i].setAttribute("points", headPoints(G));
        }
      }

      /* Point the town a given way. Also drops whatever an earlier scene left
         on the streets — the flip highlight is scene-local, and a jump between
         steps must not carry it. */
      function set(mask) {
        S.mask = mask;
        for (let i = 0; i < 6; i++) {
          S.arcs[i].classList.remove("dr-flipped");
          S.heads[i].classList.remove("dr-flipped-fill");
        }
        if (S.svg) S.svg.classList.remove("dr-undirected");
        shape();
        clearFlood();
      }

      /* Hide every arrowhead: the same six streets, asked the weaker question. */
      function undirected(on) {
        if (S.svg) S.svg.classList.toggle("dr-undirected", !!on);
      }

      function flip(i) {
        S.mask ^= (1 << i);
        shape();
        clearFlood();
      }

      /* Point at the street just turned. */
      function mark(i) {
        S.arcs[i].classList.add("dr-flipped");
        S.heads[i].classList.add("dr-flipped-fill");
      }

      /* Write the five counts. `now` puts them up at once; without it they
         arrive one corner at a time, which is scene 1's whole beat. */
      async function reveal(now) {
        S.shown = true;
        if (now || ctx.fast()) {
          paint();
          return;
        }
        for (let i = 0; i < 5; i++) {
          S.upto = i + 1;
          paint();
          await ctx.sleep(420);
        }
        S.upto = null;
        paint();
      }

      function clearFlood() {
        S.lit = 0;
        S.src = null;
        S.used = [];
        paint();
      }

      function paint() {
        const counts = REACH[S.mask];
        const upto = (S.upto == null) ? 5 : S.upto;
        S.nodes.forEach(function (c, i) {
          const on = (i === S.src) || !!((S.lit >> i) & 1);
          let cls = "dr-node";
          if (i === S.src) cls += " dr-src";
          else if ((S.lit >> i) & 1) cls += " dr-lit";
          /* An amber rim on any corner that cannot reach the whole town, so a
             broken orientation is visible before you read a single number. */
          if (S.shown && i < upto && counts[i] < 4) cls += " dr-part";
          c.setAttribute("class", cls);
          S.names[i].setAttribute("class", "dr-name" + (on ? " dr-name-on" : ""));
          S.counts[i].textContent = (S.shown && i < upto) ? String(counts[i]) : "";
          S.counts[i].setAttribute("class", "dr-count anim-knockout" +
            (counts[i] < 4 ? " dr-count-low" : ""));
        });
        for (let i = 0; i < 6; i++) {
          const keep = S.arcs[i].classList.contains("dr-flipped");
          S.arcs[i].setAttribute("class", "dr-arc" +
            (S.used.indexOf(i) >= 0 ? " dr-on" : "") + (keep ? " dr-flipped" : ""));
        }
      }

      /* Light everything reachable from s, one round at a time. Six streets, so
         the frontier loop is bookkeeping rather than a search — and REACH,
         above, is what the counts and the verdict are read off. */
      async function flood(s) {
        S.src = s;
        S.lit = 1 << s;
        S.used = [];
        paint();
        await ctx.sleep(420);
        for (let round = 0; round < 5; round++) {
          let grew = false;
          for (let i = 0; i < 6; i++) {
            const a = arcOf(i);
            if (((S.lit >> a[0]) & 1) && !((S.lit >> a[1]) & 1)) {
              S.lit |= (1 << a[1]);
              S.used.push(i);
              grew = true;
            }
          }
          if (!grew) break;
          paint();
          await ctx.sleep(520);
        }
      }

      /* ------------------------------------------------------------ the card */
      function card(title) {
        side.textContent = "";
        S.panel = ctx.el("div", "anim-panel anim-pop dr-card");
        if (title) S.panel.appendChild(ctx.el("div", "anim-caption", title));
        side.appendChild(S.panel);
        S.vBox = null;
        S.msg = null;
        S.score = null;
        return S.panel;
      }

      function verdict() {
        const strong = strongAt(S.mask);
        if (!S.vBox) {
          S.vBox = ctx.el("div", "dr-verdict");
          S.panel.appendChild(S.vBox);
        }
        S.vBox.innerHTML = "";
        S.vBox.appendChild(ctx.el("div", "dr-flag anim-pop " + (strong ? "dr-yes" : "dr-no"),
          "<b>strongly connected</b><span>" + (strong ? "yes" : "no") + "</span>"));
        /* Weak never fails here: rubbing out the arrowheads leaves the same
           pentagon and chord whichever way the streets point. */
        S.vBox.appendChild(ctx.el("div", "dr-flag anim-pop dr-yes",
          "<b>weakly connected</b><span>yes</span>"));
      }

      /* -------------------------------------------------------- the clicks */
      function hand() {
        S.live = true;
        S.grabbed = false;
        S.seen = {};
        S.found = {};
        S.svg.classList.add("dr-clickable");
        verdict();
        S.msg = ctx.el("div", "dr-msg", "click any street to turn it round");
        S.panel.appendChild(S.msg);
        S.score = ctx.el("div", "anim-tally", "<span>strong ones found</span><b>1 of 6</b>");
        S.panel.appendChild(S.score);
        S.seen[S.mask] = 1;
        if (strongAt(S.mask)) S.found[S.mask] = 1;
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
        const was = strongAt(S.mask);
        flip(i);
        /* Purple on the street just turned, and only that one, so the room can
           see what its own last click did. flip() -> paint() preserves the
           class, so the previous pick has to be cleared by hand. */
        for (let k = 0; k < 6; k++) {
          S.arcs[k].classList.remove("dr-flipped");
          S.heads[k].classList.remove("dr-flipped-fill");
        }
        mark(i);
        verdict();
        S.seen[S.mask] = 1;
        const strong = strongAt(S.mask);
        if (strong) S.found[S.mask] = 1;
        const nFound = Object.keys(S.found).length;
        S.score.querySelector("b").textContent = nFound + " of 6";
        if (strong) {
          S.msg.className = "dr-msg";
          S.msg.innerHTML = nFound === STRONG_N
            ? "<b>all six</b> — in every one, each corner sits on a cycle"
            : (was ? "<b>still strong</b> — that street's direction was free"
                   : "<b>strong again</b> — " + nFound + " of the six");
        } else {
          S.msg.className = "dr-msg dr-msg-no";
          const dead = [];
          REACH[S.mask].forEach(function (c, k) { if (c === 0) dead.push(NAME[k]); });
          S.msg.innerHTML = dead.length
            ? "<b>" + dead.join(", ") + "</b> can reach nobody at all"
            : "not strongly connected — read the amber counts";
        }
      }

      return {
        draw: draw, set: set, flip: flip, mark: mark, reveal: reveal,
        flood: flood, clearFlood: clearFlood, undirected: undirected,
        card: card, verdict: verdict, hand: hand, idle: idle
      };
    }
  });
});
