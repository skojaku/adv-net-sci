/* ==========================================================================
   euler-builder.js — The other half of Euler's theorem, built edge by edge.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Mounted by slides/m01/m01-euler-tour.md. The deck proves the easy half —
   more than two odd nodes and no such walk exists — and then says the converse
   is used without proof. This shows the converse doing its work: on a graph
   with exactly two odd corners the trail is there, it starts on one odd corner
   and finishes on the other, and starting anywhere else strands you one edge
   short. Then one extra edge makes every degree even and the trail closes.
   ========================================================================== */

(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     make_figures.py's fig_euler_path_example graph, the one the deck already
     shows on the "Eulerian path" slide: a square with a lid. Its data units
     (BL 0,0 · BR 1,0 · TL 0,1 · TR 1,1 · T 0.5,1.7) mapped into a 360 x 240
     box by x -> 95 + 170x, y -> 190 - 90y.
     ------------------------------------------------------------------------ */
  const NAME = ["BL", "BR", "TL", "TR", "T"];
  const POS = [[95, 190], [265, 190], [95, 100], [265, 100], [180, 37]];
  /* Where the name sits, and which way it is anchored away from its disc. */
  const LABEL = [[95, 216, "middle"], [265, 216, "middle"],
                 [74, 96, "end"], [286, 96, "start"], [180, 22, "middle"]];
  const R = 13;

  /* Six edges, plus a seventh scene 4 adds: a second TL–TR, drawn bowed so the
     pair reads as two edges and not one. `bow` is the sideways offset of the
     control point; 0 is a straight line. */
  const EDGE = [
    { u: 0, v: 1, bow: 0 },    /* 0  BL–BR */
    { u: 1, v: 3, bow: 0 },    /* 1  BR–TR */
    { u: 3, v: 4, bow: 0 },    /* 2  TR–T  */
    { u: 4, v: 2, bow: 0 },    /* 3  T–TL  */
    { u: 2, v: 0, bow: 0 },    /* 4  TL–BL */
    { u: 2, v: 3, bow: 0 },    /* 5  TL–TR */
    { u: 2, v: 3, bow: 56 }    /* 6  TL–TR again — scene 4 only */
  ];

  /* Degrees, counted by hand from EDGE. Six edges: 2, 2, 3, 3, 2 — TL and TR
     odd, and nothing else. Seven edges: 2, 2, 4, 4, 2 — nothing odd at all. */
  const DEG6 = [2, 2, 3, 3, 2];
  const DEG7 = [2, 2, 4, 4, 2];
  const ODD6 = [2, 3];

  /* The three runs this plays, as edge indices, each checked by exhaustive
     search over every trail from its start:

       from TL (odd)  [4,0,1,2,3,5]  all six, finishing on TR — the other odd one
       from BL (even) [0,1,2,3,5]    five, stranded on TR with TL–BL untaken;
                                     no run from BL does better than five
       from TL on the seven-edge graph
                      [3,2,1,0,4,5,6]  all seven, finishing back on TL
     ------------------------------------------------------------------------ */
  const GOOD = { from: 2, seq: [4, 0, 1, 2, 3, 5] };
  const STRAND = { from: 0, seq: [0, 1, 2, 3, 5], left: 4 };
  const TOUR = { from: 2, seq: [3, 2, 1, 0, 4, 5, 6] };

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Exactly two odd corners",
      note: "A different city: a square with a lid. Count the edges at each corner and only two counts come out odd — the two on the middle row, in red. Königsberg had four and died on it. Two is the case Euler's theorem allows, so a trail across every edge should be sitting here. Where?",
      async run(ctx) {
        ctx.idle();
        ctx.draw(6);
        ctx.card("count the corners");
        await ctx.sleep(1600);
        ctx.marks();
        await ctx.sleep(900);
        ctx.tally("edges", "6");
        await ctx.sleep(700);
        ctx.tally("degrees", "2 · 2 · 3 · 3 · 2");
        await ctx.sleep(900);
        ctx.tally("odd corners", "2");
        await ctx.sleep(1200);
        ctx.quote("at most two odd — so nothing rules a trail out here.");
        await ctx.sleep(2800);
      }
    },
    {
      label: "Begin on an odd corner",
      note: "Put the pencil on TL, one of the two odd corners, and take the edges in the order shown. All six go, none twice, and the trail finishes on TR — the other odd corner. That is not luck. The spare edge-end at an odd corner has nowhere to go except the start or the finish of the walk.",
      async run(ctx) {
        ctx.idle();
        ctx.reset();
        ctx.card("from TL");
        const n = ctx.big("0");
        ctx.caption("edges crossed, out of 6");
        ctx.stand(GOOD.from);
        await ctx.sleep(900);
        for (let i = 0; i < GOOD.seq.length; i++) {
          ctx.cross(GOOD.seq[i]);
          n.textContent = String(i + 1);
          await ctx.sleep(620);
        }
        await ctx.sleep(500);
        ctx.tally("finished on", "TR — the other odd corner");
        await ctx.sleep(1000);
        ctx.quote("six of six. The trail the theorem promised.");
        await ctx.sleep(2800);
      }
    },
    {
      label: "Begin anywhere else and you strand",
      note: "Same graph, same rules, pencil down on BL instead — an even corner. Five edges go and then the walk is standing on TR with TL–BL still untaken and nowhere near. Two odd corners need to be the two ends of the walk, and a walk has only two ends; spend one of them on BL and there are not enough left.",
      async run(ctx) {
        ctx.idle();
        ctx.reset();
        ctx.card("from BL");
        const n = ctx.big("0");
        ctx.caption("edges crossed, out of 6");
        ctx.stand(STRAND.from);
        await ctx.sleep(900);
        for (let i = 0; i < STRAND.seq.length; i++) {
          ctx.cross(STRAND.seq[i]);
          n.textContent = String(i + 1);
          await ctx.sleep(620);
        }
        ctx.leftover(STRAND.left);
        await ctx.sleep(700);
        ctx.tally("stranded on", "TR");
        await ctx.sleep(800);
        ctx.tally("still untaken", "TL–BL");
        await ctx.sleep(1000);
        ctx.quote("two odd corners want both ends of the walk. BL took one.");
        await ctx.sleep(2800);
      }
    },
    {
      label: "One more edge, and the trail closes",
      note: "Lay a second edge between TL and TR. Both of them go from three to four, every degree in the graph is now even, and the two odd corners that had to be the ends are gone. With no end to be, the trail has to come home: seven edges, start and finish both on TL. That is an Eulerian circuit.",
      async run(ctx) {
        ctx.idle();
        ctx.draw(7);
        ctx.reset();
        ctx.card("every degree even");
        ctx.marks();
        ctx.tally("degrees", "2 · 2 · 4 · 4 · 2");
        await ctx.sleep(900);
        ctx.tally("odd corners", "0");
        await ctx.sleep(1200);
        const n = ctx.big("0");
        ctx.caption("edges crossed, out of 7");
        ctx.stand(TOUR.from);
        await ctx.sleep(700);
        for (let i = 0; i < TOUR.seq.length; i++) {
          ctx.cross(TOUR.seq[i]);
          n.textContent = String(i + 1);
          await ctx.sleep(560);
        }
        await ctx.sleep(500);
        ctx.quote("back on TL, seven of seven — a circuit, not just a trail.");
        await ctx.sleep(2800);
      }
    },
    {
      label: "Now you try",
      note: "Back to six edges. Click a corner to put your pencil down, then click edges to cross them; an edge you have already used is refused. Start on TL or TR and all six will go. Start anywhere else and you will get five, every time you try it.",
      async run(ctx) {
        ctx.draw(6);
        ctx.reset();
        ctx.card("your turn");
        ctx.hand();
        if (ctx.fast()) return;
        await ctx.sleep(17000);
        ctx.idle();
      }
    }
  ];

  mountScenes(document.getElementById("euler-builder"), scenes, {
    stepsLabel: "Builder steps",

    helpers(ctx) {
      const mapBox = ctx.$("[data-eb-map]");
      const side = ctx.$("[data-eb-side]");
      const S = { n: 6, used: [], count: 0, on: null, live: false, grabbed: false };

      const other = (e, k) => (EDGE[e].u === k ? EDGE[e].v : EDGE[e].u);
      const touches = (e, k) => EDGE[e].u === k || EDGE[e].v === k;
      const inc = (k) => {
        const r = [];
        for (let e = 0; e < S.n; e++) if (touches(e, k)) r.push(e);
        return r;
      };

      /* The control point of an edge's quadratic, and the two trimmed ends. A
         straight edge (bow 0) still goes through Q — with the control on the
         chord it draws the same line, so one code path covers both. */
      function geo(e) {
        const p = POS[EDGE[e].u], q = POS[EDGE[e].v];
        const dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy);
        const cx = (p[0] + q[0]) / 2 - (dy / L) * EDGE[e].bow;
        const cy = (p[1] + q[1]) / 2 + (dx / L) * EDGE[e].bow;
        const trim = (f) => {
          const ux = cx - f[0], uy = cy - f[1], m = Math.hypot(ux, uy) || 1;
          return [f[0] + (ux / m) * (R + 1), f[1] + (uy / m) * (R + 1)];
        };
        const s = trim(p), t = trim(q);
        return {
          d: "M " + s[0] + " " + s[1] + " Q " + cx + " " + cy + " " + t[0] + " " + t[1],
          mid: [0.25 * s[0] + 0.5 * cx + 0.25 * t[0], 0.25 * s[1] + 0.5 * cy + 0.25 * t[1]],
          len: L + Math.abs(EDGE[e].bow)
        };
      }

      /* ------------------------------------------------------------- the map */
      /* `n` is how many of EDGE to draw — six normally, seven in scene 4. */
      function draw(n) {
        S.n = n;
        mapBox.textContent = "";
        const svg = ctx.svgRoot("0 0 360 240");
        const g = () => svg.appendChild(ctx.svgEl("g"));
        const gEdge = g(), gNum = g(), gNode = g(), gText = g(), gMark = g(), gHit = g();
        const slow = !ctx.fast();

        S.edges = [];
        S.nums = [];
        for (let e = 0; e < n; e++) {
          const G = geo(e);
          const p = ctx.svgEl("path", { d: G.d, "class": "eb-edge" + (slow ? " anim-draw" : "") });
          if (slow) {
            p.style.setProperty("--dash", Math.ceil(G.len) + 8);
            p.style.animationDelay = (e * 0.13) + "s";
          }
          S.edges.push(gEdge.appendChild(p));
          const t = ctx.svgEl("text", {
            x: G.mid[0], y: G.mid[1] + 5, "text-anchor": "middle",
            "class": "eb-order anim-knockout"
          });
          S.nums.push(gNum.appendChild(t));
        }

        /* The degree lives inside the disc: five small numbers outside would
           have to dodge six edges, and there is no room to dodge into. */
        S.nodes = POS.map(function (p) {
          return gNode.appendChild(ctx.svgEl("circle",
            { cx: p[0], cy: p[1], r: R, "class": "eb-node" }));
        });
        S.degs = POS.map(function (p) {
          const t = ctx.svgEl("text",
            { x: p[0], y: p[1] + 5, "text-anchor": "middle", "class": "eb-deg" });
          return gText.appendChild(t);
        });
        LABEL.forEach(function (L, i) {
          const t = ctx.svgEl("text",
            { x: L[0], y: L[1], "text-anchor": L[2], "class": "eb-name" });
          t.textContent = NAME[i];
          gText.appendChild(t);
        });

        S.here = gMark.appendChild(ctx.svgEl("circle",
          { cx: 0, cy: 0, r: R + 7, "class": "eb-here" }));
        S.here.style.opacity = 0;

        /* Hit areas last and generous: nodes first, edges over the top, so an
           edge wins where the two overlap. */
        POS.forEach(function (p, i) {
          const h = ctx.svgEl("circle", { cx: p[0], cy: p[1], r: 24, "class": "eb-hit" });
          h.addEventListener("click", function () { onNode(i); });
          gHit.appendChild(h);
        });
        for (let e = 0; e < n; e++) {
          const h = ctx.svgEl("path", { d: geo(e).d, "class": "eb-hit eb-hit-edge" });
          (function (k) {
            h.addEventListener("click", function () { onEdge(k); });
          })(e);
          gHit.appendChild(h);
        }

        S.svg = svg;
        S.marked = false;      /* a fresh drawing starts bare; marks() fills it */
        mapBox.appendChild(svg);
        reset();
      }

      function paint() {
        const deg = S.n === 7 ? DEG7 : DEG6;
        for (let e = 0; e < S.n; e++) {
          let cls = "eb-edge";
          if (S.used[e]) cls += " eb-used";
          else if (S.live && S.on != null && touches(e, S.on)) cls += " eb-open";
          S.edges[e].setAttribute("class", cls);
          S.nums[e].textContent = S.used[e] ? String(S.used[e]) : "";
        }
        S.nodes.forEach(function (c, i) {
          let cls = "eb-node";
          if (S.n === 6 && ODD6.indexOf(i) >= 0) cls += " eb-odd";
          if (i === S.on) cls += " eb-on";
          c.setAttribute("class", cls);
          S.degs[i].textContent = S.marked ? String(deg[i]) : "";
        });
        if (S.on == null) {
          S.here.style.opacity = 0;
        } else {
          S.here.setAttribute("cx", POS[S.on][0]);
          S.here.setAttribute("cy", POS[S.on][1]);
          S.here.style.opacity = 1;
        }
      }

      function reset() {
        if (!S.edges) return;
        S.used = [];
        S.count = 0;
        S.on = null;
        paint();
      }

      /* Scene 1 only: show the degree inside every disc and redden the odd. */
      function marks() {
        S.marked = true;
        paint();
      }

      function stand(k) {
        S.on = k;
        S.marked = true;
        paint();
      }

      /* One crossing. The edge itself carries the record — it turns amber and
         takes the step number — so no separate trail has to be laid over it. */
      function cross(e) {
        S.count += 1;
        S.used[e] = S.count;
        S.on = other(e, S.on);
        paint();
        return S.on;
      }

      function leftover(e) {
        S.edges[e].classList.add("eb-left");
      }

      /* ------------------------------------------------------------ the card */
      function card(title) {
        side.textContent = "";
        S.panel = ctx.el("div", "anim-panel anim-pop eb-card");
        if (title) S.panel.appendChild(ctx.el("div", "anim-caption", title));
        side.appendChild(S.panel);
        S.msg = null;
        return S.panel;
      }
      function big(v) {
        const b = ctx.el("div", "anim-big", v);
        S.panel.appendChild(b);
        return b;
      }
      function caption(t) { S.panel.appendChild(ctx.el("div", "anim-caption", t)); }
      function tally(k, v) {
        S.panel.appendChild(ctx.el("div", "anim-tally anim-fade",
          "<span>" + k + "</span><b>" + v + "</b>"));
      }
      function quote(t) { S.panel.appendChild(ctx.el("div", "anim-quote anim-fade", t)); }

      /* -------------------------------------------------------- the clicks */
      function hand() {
        S.live = true;
        S.grabbed = false;
        S.marked = true;
        S.svg.classList.add("eb-clickable");

        S.at = ctx.el("div", "anim-tally", "<span>standing on</span><b>—</b>");
        S.n6 = ctx.el("div", "anim-tally", "<span>edges crossed</span><b>0 of 6</b>");
        S.msg = ctx.el("div", "eb-msg", "Click a corner to start. Try TL first.");
        S.panel.appendChild(S.at);
        S.panel.appendChild(S.n6);
        S.panel.appendChild(S.msg);

        const rst = ctx.el("button", "anim-btn", "↻ Reset");
        rst.type = "button";
        /* The canvas is aria-hidden, so a tabbable control inside it would be
           a focus trap announcing nothing — the scene note is the account. */
        rst.tabIndex = -1;
        rst.addEventListener("click", function () {
          grab();
          S.used = [];
          S.count = 0;
          S.on = null;
          S.edges.forEach(function (p) { p.classList.remove("eb-left"); });
          paint();
          report();
          say("ok", "Cleared. Click a corner to start.");
        });
        S.panel.appendChild(rst);
        paint();
      }
      function idle() {
        S.live = false;
        if (S.svg) S.svg.classList.remove("eb-clickable");
        if (S.edges) paint();
      }
      function grab() {
        if (S.grabbed) return;
        S.grabbed = true;
        ctx.pause();
      }
      function say(kind, html) {
        if (!S.msg) return;
        S.msg.className = "eb-msg" + (kind === "no" ? " eb-msg-no" : "");
        S.msg.innerHTML = html;
      }
      function report() {
        if (!S.at) return;
        S.at.querySelector("b").textContent = S.on == null ? "—" : NAME[S.on];
        S.n6.querySelector("b").textContent = S.count + " of 6";
      }
      function nope(e) {
        const p = S.edges[e];
        p.classList.remove("eb-nope");
        p.getBoundingClientRect();
        p.classList.add("eb-nope");
      }

      function onNode(k) {
        if (!S.live) return;
        grab();
        if (S.on == null) {
          stand(k);
          report();
          const odd = ODD6.indexOf(k) >= 0;
          say("ok", "Pencil down on <b>" + NAME[k] + "</b>" +
            (odd ? " — an odd corner. Good place to be." : " — an even corner. Watch what happens.") +
            " Now click an edge.");
        } else {
          say("no", "You are already walking. Click an <b>edge</b>, not a corner.");
        }
      }

      function onEdge(e) {
        if (!S.live) return;
        grab();
        if (S.on == null) {
          nope(e);
          say("no", "Put your pencil down first: click a corner.");
          return;
        }
        if (S.used[e]) {
          nope(e);
          say("no", "That edge is behind you. You may not cross it twice.");
          return;
        }
        if (!touches(e, S.on)) {
          nope(e);
          say("no", "That edge does not touch <b>" + NAME[S.on] +
            "</b>. You cannot reach it from here.");
          return;
        }
        cross(e);
        report();
        const stuck = !inc(S.on).some(function (k) { return !S.used[k]; });
        if (S.count === 6) {
          say("ok", "<b>Six of six.</b> You began on an odd corner and finished on the other one.");
        } else if (stuck) {
          say("no", "Stuck on <b>" + NAME[S.on] + "</b> with <b>" + S.count +
            " of 6</b>. Every edge here is behind you. ↻ Reset and open on TL or TR.");
        } else {
          say("ok", "You are on <b>" + NAME[S.on] + "</b>, " + S.count + " of 6 done.");
        }
      }

      return {
        draw: draw, reset: reset, marks: marks, stand: stand, cross: cross,
        leftover: leftover, card: card, big: big, caption: caption,
        tally: tally, quote: quote, hand: hand, idle: idle
      };
    }
  });
});
