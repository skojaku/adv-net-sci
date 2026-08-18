/* ==========================================================================
   route-namer.js — Walk, trail, path, circuit, cycle: one route, five names.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Mounted by slides/m01/m01-euler-tour.md, after the five definition slides.
   Those slides give the five names one at a time; this gives the room the
   graph and lets it produce a route the definitions then have to name. The
   three played routes are the same three the deck's GIFs draw, on the same
   graph, so the stage recaps rather than introduces.
   ========================================================================== */

(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     The campus graph, exactly as make_figures.py declares it (CAMPUS_POS /
     CAMPUS_EDGES) and as campus-base.png and the three campus GIFs draw it: a
     square with one diagonal. Degrees are Dorm 2, Cafe 3, Lib 2, Gym 3.

     Note for whoever extends this: every closed trail on this graph is also a
     cycle. Telling a circuit from a cycle needs two loops meeting at one
     corner, and a square with a diagonal has no such corner — the deck's own
     circuit.png and cycle.png carry that distinction. Checked exhaustively:
     zero closed trails here repeat a node.
     ------------------------------------------------------------------------ */
  const NAME = ["Dorm", "Cafe", "Lib", "Gym"];
  const POS = [[100, 80], [280, 80], [280, 200], [100, 200]];
  const LABEL = [[100, 56], [280, 56], [280, 236], [100, 236]];
  const EDGES = [[0, 1], [1, 2], [2, 3], [3, 0], [1, 3]];
  const R = 11;

  /* The three routes the deck's GIFs draw, as node indices. */
  const WALK = [0, 1, 3, 1, 2];       /* Dorm-Cafe-Gym-Cafe-Lib */
  const TRAIL = [2, 3, 0, 1, 3];      /* Lib-Gym-Dorm-Cafe-Gym  */
  const PATH = [2, 1, 0, 3];          /* Lib-Cafe-Dorm-Gym      */

  /* The ladder, widest first. `rule` is what the name costs you. */
  const LADDER = [
    { k: "walk", rule: "anything goes" },
    { k: "trail", rule: "no edge twice" },
    { k: "path", rule: "no node twice" },
    { k: "circuit", rule: "closed trail" },
    { k: "cycle", rule: "closed path" }
  ];

  const WHY = {
    walk: "an edge came round twice — every stricter name is out",
    trail: "no edge twice, but a node came round again",
    path: "nothing repeats at all",
    circuit: "back at the start, no edge twice",
    cycle: "back at the start, and nothing else repeated"
  };

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "One route, five names",
      note: "Two questions settle the name: does an edge come round twice, and does a node?",
      async run(ctx) {
        ctx.idle();
        ctx.drawGraph();
        /* The ladder's right-hand column already asks both questions, one word
           per name. Narrating them underneath was the same thing twice. */
        ctx.card("the two questions");
        ctx.ladder();
        await ctx.sleep(4000);
      }
    },
    {
      label: "Dorm → Cafe → Gym → Cafe → Lib",
      note: "The cafe–gym edge is walked in both directions. Only a walk, then.",
      async run(ctx) {
        ctx.idle();
        ctx.card("what is this?");
        ctx.ladder();
        await ctx.play(WALK);
        await ctx.sleep(2400);
      }
    },
    {
      label: "Lib → Gym → Dorm → Cafe → Gym",
      note: "No edge twice, but the gym twice. A trail, and not a path.",
      async run(ctx) {
        ctx.idle();
        ctx.card("and this one?");
        ctx.ladder();
        await ctx.play(TRAIL);
        await ctx.sleep(2400);
      }
    },
    {
      label: "Lib → Cafe → Dorm → Gym",
      note: "Nothing repeats at all — a path. And every path is a trail.",
      async run(ctx) {
        ctx.idle();
        ctx.card("and this?");
        ctx.ladder();
        await ctx.play(PATH);
        await ctx.sleep(2400);
      }
    },
    {
      label: "Now you try",
      note: "Your turn. Click a place, then a neighbour, and watch the name move.",
      async run(ctx) {
        /* No card title here: this is the only scene carrying a Reset button,
           and the caption's 34px is exactly what would push it off the slide. */
        ctx.card();
        ctx.ladder();
        ctx.hand();
        if (ctx.fast()) return;
        await ctx.sleep(17000);
        ctx.idle();
      }
    }
  ];

  mountScenes(document.getElementById("route-namer"), scenes, {
    stepsLabel: "Route steps",

    helpers(ctx) {
      const mapBox = ctx.$("[data-rn-map]");
      const side = ctx.$("[data-rn-side]");
      const S = { route: [], live: false, grabbed: false };

      const nb = (a, b) => EDGES.some(function (e) {
        return (e[0] === a && e[1] === b) || (e[1] === a && e[0] === b);
      });
      const eid = (a, b) => EDGES.findIndex(function (e) {
        return (e[0] === a && e[1] === b) || (e[1] === a && e[0] === b);
      });

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

      /* ------------------------------------------------------------- the map */
      function drawGraph() {
        mapBox.textContent = "";
        const svg = ctx.svgRoot("0 0 380 260");
        const g = () => svg.appendChild(ctx.svgEl("g"));
        const gEdge = g(), gLeg = g(), gNode = g(), gText = g(), gHit = g();

        EDGES.forEach(function (e) {
          gEdge.appendChild(ctx.svgEl("line", {
            x1: POS[e[0]][0], y1: POS[e[0]][1], x2: POS[e[1]][0], y2: POS[e[1]][1],
            "class": "anim-edge"
          }));
        });

        S.nodes = POS.map(function (p) {
          return gNode.appendChild(ctx.svgEl("circle",
            { cx: p[0], cy: p[1], r: R, "class": "rn-node" }));
        });
        LABEL.forEach(function (p, i) {
          const t = ctx.svgEl("text",
            { x: p[0], y: p[1], "text-anchor": "middle", "class": "rn-name" });
          t.textContent = NAME[i];
          gText.appendChild(t);
        });

        POS.forEach(function (p, i) {
          const e = ctx.svgEl("circle", { cx: p[0], cy: p[1], r: 26, "class": "rn-hit" });
          e.addEventListener("click", function () { onNode(i); });
          gHit.appendChild(e);
        });

        S.svg = svg;
        S.gLeg = gLeg;
        mapBox.appendChild(svg);
        clearRoute();
      }

      /* One leg of the route, bowed sideways by however many times this edge
         has already been walked, so a second crossing does not hide under the
         first. Numbered at its own midpoint. */
      function drawLeg(a, b, step, again) {
        const p = POS[a], q = POS[b];
        const dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy);
        const nx = -dy / L, ny = dx / L;
        const bow = again * 20;
        const cx = (p[0] + q[0]) / 2 + nx * bow * 2;
        const cy = (p[1] + q[1]) / 2 + ny * bow * 2;

        /* Trim both ends back to the rim of their node disc. */
        const trim = (from) => {
          const ux = cx - from[0], uy = cy - from[1], m = Math.hypot(ux, uy) || 1;
          return [from[0] + (ux / m) * (R + 4), from[1] + (uy / m) * (R + 4)];
        };
        const s = trim(p), t = trim(q);

        const path = ctx.svgEl("path", {
          d: "M " + s[0] + " " + s[1] + " Q " + cx + " " + cy + " " + t[0] + " " + t[1],
          "class": "anim-trail" + (again ? " rn-again" : "")
        });
        S.gLeg.appendChild(ink(path, L + Math.abs(bow) * 3, 380));

        /* Arrowhead: the tangent at the far end runs from the control point. */
        const ax = t[0] - cx, ay = t[1] - cy, am = Math.hypot(ax, ay) || 1;
        const ux = ax / am, uy = ay / am;
        const head = ctx.svgEl("polygon", {
          points: [
            (t[0] + ux * 3) + "," + (t[1] + uy * 3),
            (t[0] - ux * 11 - uy * 6) + "," + (t[1] - uy * 11 + ux * 6),
            (t[0] - ux * 11 + uy * 6) + "," + (t[1] - uy * 11 - ux * 6)
          ].join(" "),
          "class": "rn-head" + (again ? " rn-again-fill" : "")
        });
        if (!ctx.fast()) {
          head.classList.add("anim-fade");
          head.style.animationDelay = "0.32s";
        }
        S.gLeg.appendChild(head);

        /* The step number, pushed clear of its own leg. */
        const mx = 0.25 * s[0] + 0.5 * cx + 0.25 * t[0];
        const my = 0.25 * s[1] + 0.5 * cy + 0.25 * t[1];
        const n = ctx.svgEl("text", {
          x: mx + nx * 13, y: my + ny * 13 + 4,
          "text-anchor": "middle", "class": "rn-step anim-knockout"
        });
        n.textContent = String(step);
        if (!ctx.fast()) {
          n.classList.add("anim-fade");
          n.style.animationDelay = "0.36s";
        }
        S.gLeg.appendChild(n);
      }

      function paint() {
        const on = S.route.length ? S.route[S.route.length - 1] : null;
        S.nodes.forEach(function (c, i) {
          let cls = "rn-node";
          if (i === on) cls += " rn-here";
          else if (S.route.indexOf(i) >= 0) cls += " rn-been";
          else if (S.live && on != null && nb(i, on)) cls += " rn-open";
          else if (S.live && on == null) cls += " rn-open";
          c.setAttribute("class", cls);
        });
      }

      function clearRoute() {
        if (!S.gLeg) return;
        S.gLeg.textContent = "";
        S.route = [];
        paint();
        report();
      }

      /* Extend the route by one node. Synchronous, because a click has to
         answer at once; playback does its own waiting between calls. */
      function step(to) {
        const from = S.route[S.route.length - 1];
        const id = eid(from, to);
        const again = S.route.slice(0, -1).filter(function (x, k) {
          return eid(x, S.route[k + 1]) === id;
        }).length;
        drawLeg(from, to, S.route.length, again);
        S.route.push(to);
        paint();
        report();
      }

      async function play(route) {
        clearRoute();
        S.route = [route[0]];
        paint();
        report();
        await ctx.sleep(600);
        for (let i = 1; i < route.length; i++) {
          step(route[i]);
          await ctx.sleep(720);
        }
      }

      /* ---------------------------------------------------- naming the route */
      /* Two counts and a comparison — the definitions, spelled out, over a
         route that is never more than a handful of steps long. */
      function verdict() {
        if (S.route.length < 2) return null;
        const used = [];
        for (let i = 1; i < S.route.length; i++) used.push(eid(S.route[i - 1], S.route[i]));
        const edgeRep = used.some(function (v, i) { return used.indexOf(v) !== i; });
        const closed = S.route[0] === S.route[S.route.length - 1];
        const seen = closed ? S.route.slice(0, -1) : S.route;
        const nodeRep = seen.some(function (v, i) { return seen.indexOf(v) !== i; });
        let k;
        if (edgeRep) k = "walk";
        else if (closed) k = nodeRep ? "circuit" : "cycle";
        else k = nodeRep ? "trail" : "path";
        return { k: k, edgeRep: edgeRep, nodeRep: nodeRep, closed: closed };
      }

      /* ------------------------------------------------------------ the card */
      function card(title) {
        side.textContent = "";
        S.panel = ctx.el("div", "anim-panel anim-pop rn-card");
        if (title) S.panel.appendChild(ctx.el("div", "anim-caption", title));
        S.body = ctx.el("div", "rn-body");
        S.panel.appendChild(S.body);
        side.appendChild(S.panel);
        S.chips = null;
        return S.panel;
      }

      /* Narration and refusals share one reserved two-line box, so nothing a
         scene says can push the ladder or the reset button around. */
      function tell(html, bad) {
        if (!S.why) return;
        S.why.className = "rn-why" + (bad ? " rn-why-no" : "");
        S.why.innerHTML = html;
      }

      /* The five names, always in the same order, with the current one lit. */
      function ladder() {
        S.chips = ctx.el("div", "rn-ladder");
        LADDER.forEach(function (L) {
          S.chips.appendChild(ctx.el("div", "rn-chip",
            "<b>" + L.k + "</b><span>" + L.rule + "</span>"));
        });
        S.body.appendChild(S.chips);
        S.line = ctx.el("div", "rn-route", "—");
        S.body.appendChild(S.line);
        S.why = ctx.el("div", "rn-why", "");
        S.body.appendChild(S.why);
        report();
      }

      function report() {
        if (!S.chips) return;
        const v = verdict();
        Array.prototype.forEach.call(S.chips.children, function (c, i) {
          c.setAttribute("class", "rn-chip" + (v && LADDER[i].k === v.k ? " rn-on" : ""));
        });
        S.line.textContent = S.route.length
          ? S.route.map(function (i) { return NAME[i]; }).join(" → ")
          : "—";
        if (v) tell("<b>" + v.k + "</b> — " + WHY[v.k]);
        else if (S.route.length) tell("one place, no route yet");
      }

      /* -------------------------------------------------------- the clicks */
      function hand() {
        clearRoute();
        S.live = true;
        S.grabbed = false;
        S.svg.classList.add("rn-clickable");
        paint();
        tell("click a place to put your pencil down");

        const rst = ctx.el("button", "anim-btn", "↻ Reset");
        rst.type = "button";
        /* The canvas is aria-hidden, so a tabbable control inside it would be
           a focus trap announcing nothing — the scene note is the account. */
        rst.tabIndex = -1;
        rst.addEventListener("click", function () {
          grab();
          clearRoute();
          tell("click a place to put your pencil down");
        });
        S.body.appendChild(rst);
      }
      function idle() {
        S.live = false;
        if (S.svg) S.svg.classList.remove("rn-clickable");
        if (S.nodes) paint();
      }
      function grab() {
        if (S.grabbed) return;
        S.grabbed = true;
        ctx.pause();
      }

      function nope(i) {
        S.nodes[i].classList.remove("rn-nope");
        S.nodes[i].getBoundingClientRect();
        S.nodes[i].classList.add("rn-nope");
      }

      function onNode(i) {
        if (!S.live) return;
        grab();
        if (!S.route.length) {
          S.route = [i];
          paint();
          report();
          tell("pencil down on <b>" + NAME[i] + "</b> — now click a neighbour");
          return;
        }
        const on = S.route[S.route.length - 1];
        if (!nb(i, on)) {
          nope(i);
          tell("<b>" + NAME[i] + "</b> is not next to <b>" + NAME[on] + "</b>", true);
          return;
        }
        step(i);
      }

      return {
        drawGraph: drawGraph, play: play, card: card, tell: tell, ladder: ladder,
        hand: hand, idle: idle
      };
    }
  });
});
