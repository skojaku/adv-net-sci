/* ==========================================================================
   kb-tracer.js — The Konigsberg bridge tracer.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header
   of assets/anim.js for the contract, and the markup this expects.

   Loaded by lecture-note/m01-euler_tour/01-concepts.qmd and slides/m01/m01-euler-tour.md.
   It lives in a file rather than inline in either of them because those two
   would otherwise be two copies of the same 500 lines of hand-checked data,
   and the first fix to one of them would silently not reach the other.

   The stage's own layout CSS stays with each page: the note has a column to
   fill and the slide has a 1280x720 frame, so the sizes differ even though
   every colour, class and coordinate here is shared.
   ========================================================================== */

/* Scenes and nothing in between: the paper, the pen, the motion and the
   sequencer all come from assets/anim.css + assets/anim.js, and everything a
   scene calls arrives on `ctx`. The markup stays with whichever page mounts
   this. The kit may load after this file, hence the animReady queue. */
(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     Königsberg, transcribed by hand into a 320 x 200 box: the same four
     landmasses in the same arrangement as figs/konigsberg-graph.svg, the same
     seven bridges, the same letters. Landmass 0 = A, 1 = B, 2 = C, 3 = D.

       A  Kneiphof island   a b c d e   5 bridges
       B  south bank        a b f       3
       C  north bank        c d g       3
       D  east island       e f g       3

     5 + 3 + 3 + 3 = 14 = 2 x 7, because every bridge has two ends. Note the
     two parallel pairs: a and b both run A-B, c and d both run A-C.

     Nothing in this file runs a graph algorithm at page load. The one walk the
     animation plays was found by hand and checked by exhaustive search over
     all 4 starts x 7! orderings: the longest trail in this city is 6 bridges,
     from any starting landmass, and the walk below is one of them.
     ------------------------------------------------------------------------ */
  const LAND = [
    { id: "A", full: "A — Kneiphof island", hub: [105, 100], at: [48, 105] },
    { id: "B", full: "B — south bank",      hub: [170, 176], at: [14, 186] },
    { id: "C", full: "C — north bank",      hub: [170,  24], at: [14,  30] },
    { id: "D", full: "D — east island",     hub: [258, 100], at: [284, 105] }
  ];

  /* n letter · u,v the two landmasses · p,q the mouth on u and on v (where the
     bridge meets the shore) · d the segment actually drawn, run a little way
     inland at both ends so no hairline of water shows at the joint · l the
     letter's anchor. */
  const BR = [
    { n:"a", u:0, v:1, p:[ 60,120], q:[ 60,154], d:[[ 60,120],[ 60,164]], l:[ 52,141], la:"end" },
    { n:"b", u:0, v:1, p:[145,121], q:[145,154], d:[[145,121],[145,164]], l:[137,141], la:"end" },
    { n:"c", u:0, v:2, p:[ 60, 80], q:[ 60, 46], d:[[ 60, 80],[ 60, 36]], l:[ 52, 66], la:"end" },
    { n:"d", u:0, v:2, p:[145, 79], q:[145, 46], d:[[145, 79],[145, 36]], l:[137, 66], la:"end" },
    { n:"e", u:0, v:3, p:[173,100], q:[218,100], d:[[170,100],[221,100]], l:[195, 93], la:"middle" },
    { n:"f", u:1, v:3, p:[258,154], q:[258,122], d:[[258,164],[258,122]], l:[250,145], la:"end" },
    { n:"g", u:2, v:3, p:[258, 46], q:[258, 78], d:[[258, 36],[258, 78]], l:[250, 62], la:"end" }
  ];

  /* Which bridges touch each landmass — the degree, spelled out. */
  const INC = [[0, 1, 2, 3, 4], [0, 1, 5], [2, 3, 6], [4, 5, 6]];

  /* The attempt scene 2 plays: start on C, then c, a, b, d, g, e.
       C -c- A -a- B -b- A -d- C -g- D -e- A
     Six of the seven crossed; you finish on A, and the survivor is f, which
     joins B to D and so is nowhere near you. Six is the most this city
     allows — see the note above. */
  const SEED = { from: 2, seq: [2, 0, 1, 3, 6, 4] };

  /* One pairing of the bridge-ends at each landmass: every visit spends two,
     one arriving and one leaving. Which spokes get married is arbitrary — what
     is not arbitrary is that an odd number of them cannot all be married, so
     each of these four leaves exactly one over. The four leftovers here are
     four different bridges (e, a, g, f), which is a coincidence of this
     pairing, not a fact about the city. */
  const PAIRING = [
    { k: 0, pairs: [[2, 3], [0, 1]], left: 4 },   /* A: (c,d) and (a,b), e over */
    { k: 2, pairs: [[2, 3]],         left: 6 },   /* C: (c,d), g over */
    { k: 1, pairs: [[1, 5]],         left: 0 },   /* B: (b,f), a over */
    { k: 3, pairs: [[4, 6]],         left: 5 }    /* D: (e,g), f over */
  ];

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Seven bridges, one rule",
      note: "Königsberg: two banks, two islands, seven bridges. The rule is one line long — cross every bridge exactly once. Watch the two pairs: a and b both run from the island A to the south bank B, and c and d both run from A to the north bank C.",
      async run(ctx) {
        ctx.idle();
        ctx.drawCity();
        ctx.cap("the city as Euler found it — four landmasses, seven bridges");
        const c = ctx.card("the city");
        await ctx.sleep(2200);
        [["landmasses", "4"], ["bridges", "7"]].forEach((row, i) => {
          const t = ctx.el("div", "anim-tally anim-fade",
            "<span>" + row[0] + "</span><b>" + row[1] + "</b>");
          t.style.animationDelay = ctx.fast() ? "0s" : (i * 0.4) + "s";
          c.appendChild(t);
        });
        LAND.forEach((L, i) => {
          const t = ctx.el("div", "anim-caption anim-fade", L.full);
          t.style.animationDelay = ctx.fast() ? "0s" : (1 + i * 0.25) + "s";
          c.appendChild(t);
        });
        const q = ctx.el("div", "anim-quote anim-fade", "cross every bridge exactly once.");
        q.style.animationDelay = ctx.fast() ? "0s" : "2.2s";
        c.appendChild(q);
        await ctx.sleep(3400);
      }
    },
    {
      label: "Watch a good attempt fail",
      note: "One attempt, played out: start on the north bank C and take c, a, b, d, g, e. Six bridges crossed, and then it stops. You are standing on A; the bridge left over is f, which joins B to D.",
      async run(ctx) {
        ctx.idle();
        ctx.resetWalk();
        ctx.cap("start on C and cross six — then look where the seventh is");
        const c = ctx.card("someone tries");
        const big = ctx.el("div", "anim-big", "0");
        c.appendChild(big);
        c.appendChild(ctx.el("div", "anim-caption", "bridges crossed, out of 7"));
        const tally = ctx.el("div", "anim-tally", "<span>crossed</span><b>—</b>");
        c.appendChild(tally);
        const val = tally.querySelector("b");

        ctx.stand(SEED.from);
        await ctx.sleep(800);

        const done = [];
        for (let i = 0; i < SEED.seq.length; i++) {
          ctx.cross(SEED.seq[i]);
          done.push(BR[SEED.seq[i]].n);
          big.textContent = String(done.length);
          val.textContent = done.join(" ");
          await ctx.sleep(560);
        }

        await ctx.sleep(400);
        c.appendChild(ctx.el("div", "anim-tally anim-fade",
          "<span>stranded on</span><b>A</b>"));
        const q = ctx.el("div", "anim-quote anim-fade",
          "the bridge left over is f, and f joins B to D. You are on A.");
        q.style.animationDelay = ctx.fast() ? "0s" : "0.6s";
        c.appendChild(q);
        await ctx.sleep(2800);
      }
    },
    {
      label: "Now you try",
      note: "Your turn. Click a landmass to put your pencil down, then click bridges to cross them. A bridge you have already used is refused. Nobody gets seven — six is the most this city allows. Press ▶ when you want the reason.",
      async run(ctx) {
        ctx.resetWalk();
        ctx.cap("click a landmass, then click bridges");
        const c = ctx.card("your turn");

        const rAt = ctx.el("div", "anim-tally", "<span>standing on</span><b>—</b>");
        const rN = ctx.el("div", "anim-tally", "<span>bridges crossed</span><b>0 of 7</b>");
        c.appendChild(rAt);
        c.appendChild(rN);

        const msg = ctx.el("div", "kb-msg", "Click any landmass to start.");
        c.appendChild(msg);

        const rst = ctx.el("button", "anim-btn", "↻ Reset");
        rst.type = "button";
        /* The canvas is aria-hidden, so a tabbable control in it would be a
           focus trap announcing nothing — the same call the kit makes for its
           knob. The scene note carries the account instead. */
        rst.tabIndex = -1;
        rst.addEventListener("click", function () {
          ctx.grab();
          ctx.resetWalk();
          ctx.report();
        });
        c.appendChild(rst);

        ctx.hand({ at: rAt.querySelector("b"), n: rN.querySelector("b"), msg: msg });
        if (ctx.fast()) return;

        await ctx.sleep(17000);
        ctx.idle();
      }
    },
    {
      label: "Every visit uses two bridges",
      note: "Here is the reason. Draw the bridge-ends at each landmass as spokes — fourteen of them, two per bridge. Every visit spends exactly two: one to arrive, one to leave. So pair them up. At A, five spokes make two pairs and one spare; at B, C and D, three spokes make one pair and one spare.",
      async run(ctx) {
        ctx.idle();
        ctx.resetWalk();
        ctx.cap("dashed: the bridge-ends · purple: a pair, one in and one out");
        const c = ctx.card("one in, one out");
        c.appendChild(ctx.el("div", "anim-quote",
          "arriving costs a bridge, leaving costs another — so the bridge-ends at a landmass have to pair up."));

        ctx.spokes();
        await ctx.sleep(ctx.fast() ? 0 : 1500);
        c.appendChild(ctx.el("div", "anim-tally", "<span>bridge-ends</span><b>14</b>"));
        await ctx.sleep(1200);

        for (let i = 0; i < PAIRING.length; i++) {
          const P = PAIRING[i];
          ctx.pairAt(P);
          const n = INC[P.k].length;
          c.appendChild(ctx.el("div", "anim-tally",
            "<span>" + LAND[P.k].id + " — " + n + " ends</span><b>" +
            P.pairs.length + (P.pairs.length > 1 ? " pairs" : " pair") + ", 1 spare</b>"));
          await ctx.sleep(1500);
        }
        await ctx.sleep(1400);
      }
    },
    {
      label: "Four ends, and a walk has two",
      note: "Every landmass here has an odd number of bridges, so every one of them keeps a spare — a bridge-end with no partner, which can only be used on the way in at the very start or on the way out at the very end. Four landmasses need to be an end. A walk has two. No such walk exists.",
      async run(ctx) {
        ctx.idle();
        ctx.resetWalk();
        ctx.pairAll();
        ctx.cap("orange: the bridge-end with no partner — one at every landmass");
        const c = ctx.card("four ends, and a walk has two");

        for (let i = 0; i < PAIRING.length; i++) {
          const P = PAIRING[i];
          const t = ctx.el("div", "anim-tally anim-fade",
            "<span>" + LAND[P.k].id + "</span><b>" + INC[P.k].length +
            " bridges → 1 spare</b>");
          t.style.animationDelay = ctx.fast() ? "0s" : (i * 0.45) + "s";
          c.appendChild(t);
        }
        await ctx.sleep(2600);

        const big = ctx.el("div", "anim-big anim-fade", "4");
        c.appendChild(big);
        c.appendChild(ctx.el("div", "anim-caption anim-fade",
          "landmasses that must be a start or an end"));
        await ctx.sleep(1600);
        c.appendChild(ctx.el("div", "anim-tally anim-fade",
          "<span>a walk has</span><b>1 start, 1 end</b>"));
        await ctx.sleep(1400);
        c.appendChild(ctx.el("div", "anim-quote anim-fade",
          "four ends needed, two available. The walk cannot exist."));
        await ctx.sleep(3200);
      }
    }
  ];

  mountScenes(document.getElementById("kb-tracer"), scenes, {
    stepsLabel: "Tracer steps",

    /* The three things only this animation has: a city that persists across
       all five scenes, a tracer that takes clicks, and a card on the right
       that each scene rewrites. Built once at mount, handed to every scene. */
    helpers(ctx) {
      const mapBox = ctx.$("[data-kb-map]");
      const side = ctx.$("[data-kb-side]");
      const S = { used: [], count: 0, on: null, tip: null, live: false, grabbed: false, out: null };

      const at = (p) => p[0] + " " + p[1];
      const far = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]);

      /* Draw a path on, then let go of it. .anim-draw's resting state is
         "fully drawn", but only once the animation has actually run: until
         then the class pins stroke-dashoffset at --dash, i.e. invisible. A
         path built inside a click handler can miss its first frame and stay
         that way forever. So the class comes off again as soon as the draw is
         over, and the stroke is solid whether or not it was ever ticked. */
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
      const mouth = (b, k) => (BR[b].u === k ? BR[b].p : BR[b].q);
      const other = (b, k) => (BR[b].u === k ? BR[b].v : BR[b].u);
      const touches = (b, k) => BR[b].u === k || BR[b].v === k;

      /* ------------------------------------------------------------ the map */
      function drawCity() {
        mapBox.textContent = "";
        const svg = ctx.svgRoot("0 0 320 200");
        const g = () => svg.appendChild(ctx.svgEl("g"));
        const gWater = g(), gLand = g(), gBridge = g(), gTrail = g(),
              gSpoke = g(), gPair = g(), gText = g(), gMark = g(), gHit = g();
        const slow = !ctx.fast();

        gWater.appendChild(ctx.svgEl("rect",
          { x: 0, y: 0, width: 320, height: 200, "class": "kb-water" }));

        /* Two banks with a wavering shoreline, two islands. The shore only
           ever wanders between y = 40 and y = 50 (and 150 to 160 in the
           south), which is why every bridge is drawn from y = 36 or to
           y = 164 — a bridge always starts on dry land. */
        gLand.appendChild(ctx.svgEl("path",
          { d: "M -4 -4 H 324 V 44 C 268 49 232 40 176 45 C 120 50 58 41 -4 46 Z",
            "class": "kb-land" }));
        gLand.appendChild(ctx.svgEl("path",
          { d: "M -4 204 H 324 V 156 C 268 151 232 160 176 155 C 120 150 58 159 -4 154 Z",
            "class": "kb-land" }));
        gLand.appendChild(ctx.svgEl("ellipse",
          { cx: 105, cy: 100, rx: 68, ry: 26, "class": "kb-land" }));
        gLand.appendChild(ctx.svgEl("ellipse",
          { cx: 258, cy: 100, rx: 40, ry: 22, "class": "kb-land" }));

        S.bridges = BR.map(function (b, i) {
          const ln = ctx.svgEl("line", {
            x1: b.d[0][0], y1: b.d[0][1], x2: b.d[1][0], y2: b.d[1][1],
            "class": "kb-bridge" + (slow ? " anim-draw" : "")
          });
          if (slow) {
            /* --dash must clear the segment's own length; the longest bridge
               here is e at 51 units. */
            ln.style.setProperty("--dash", "70");
            ln.style.animationDelay = (0.8 + i * 0.16) + "s";
          }
          return gBridge.appendChild(ln);
        });

        BR.forEach(function (b, i) {
          const t = ctx.svgEl("text", {
            x: b.l[0], y: b.l[1], "text-anchor": b.la,
            "class": "kb-letter" + (slow ? " anim-fade" : "")
          });
          t.textContent = b.n;
          if (slow) t.style.animationDelay = (1.9 + i * 0.08) + "s";
          gText.appendChild(t);
        });
        LAND.forEach(function (L, i) {
          const t = ctx.svgEl("text", {
            x: L.at[0], y: L.at[1],
            "text-anchor": i === 0 || i === 3 ? "middle" : "start",
            "class": "kb-name" + (slow ? " anim-fade" : "")
          });
          t.textContent = L.id;
          if (slow) t.style.animationDelay = (0.3 + i * 0.12) + "s";
          gText.appendChild(t);
        });

        gText.appendChild(ctx.svgEl("rect",
          { x: 1.2, y: 1.2, width: 317.6, height: 197.6, rx: 5, "class": "kb-frame" }));

        S.mark = gMark.appendChild(ctx.svgEl("circle",
          { cx: 0, cy: 0, r: 5.5, "class": "kb-here" }));
        S.mark.style.opacity = 0;

        /* Hit areas, invisible and last: landmasses first, bridges over the
           top, so a bridge always wins where the two overlap. */
        [[0, "ellipse", { cx: 105, cy: 100, rx: 68, ry: 26 }],
         [1, "rect", { x: 0, y: 150, width: 320, height: 50 }],
         [2, "rect", { x: 0, y: 0, width: 320, height: 50 }],
         [3, "ellipse", { cx: 258, cy: 100, rx: 40, ry: 22 }]].forEach(function (h) {
          const e = ctx.svgEl(h[1], h[2]);
          e.setAttribute("class", "kb-hit");
          e.addEventListener("click", function () { onLand(h[0]); });
          gHit.appendChild(e);
        });
        S.hits = BR.map(function (b, i) {
          const e = ctx.svgEl("line", {
            x1: b.d[0][0], y1: b.d[0][1], x2: b.d[1][0], y2: b.d[1][1],
            "class": "kb-hit"
          });
          e.addEventListener("click", function () { onBridge(i); });
          return gHit.appendChild(e);
        });

        S.svg = svg;
        S.gTrail = gTrail;
        S.gSpoke = gSpoke;
        S.gPair = gPair;
        mapBox.appendChild(svg);
        S.capEl = ctx.el("div", "anim-caption", "");
        mapBox.appendChild(S.capEl);
        resetWalk();
      }

      const cap = (t) => { if (S.capEl) S.capEl.textContent = t; };

      /* ------------------------------------------------------------ walking */
      function paint() {
        S.bridges.forEach(function (ln, i) {
          let cls = "kb-bridge";
          if (S.used[i]) cls += " kb-used";
          else if (S.live && S.on != null && touches(i, S.on)) cls += " kb-open";
          ln.setAttribute("class", cls);
        });
        /* The marker is the pencil tip, not the landmass: it sits where the
           trail actually ends, so the route never dangles. */
        if (S.on == null) {
          S.mark.style.opacity = 0;
        } else {
          S.mark.setAttribute("cx", S.tip[0]);
          S.mark.setAttribute("cy", S.tip[1]);
          S.mark.style.opacity = 1;
        }
      }

      function resetWalk() {
        if (!S.gTrail) return;
        S.gTrail.textContent = "";
        S.used = [false, false, false, false, false, false, false];
        S.count = 0;
        S.on = null;
        S.tip = null;
        paint();
      }

      /* Pencil down: the tip starts in the middle of the landmass, and leaves
         a ring there, because once the tip moves on nothing else records where
         the walk began. Lives in the trail layer, so a reset takes it too. */
      function stand(k) {
        S.on = k;
        S.tip = LAND[k].hub;
        S.gTrail.appendChild(ctx.svgEl("circle",
          { cx: S.tip[0], cy: S.tip[1], r: 5.5, "class": "kb-start" }));
        paint();
      }

      /* One crossing. The bridge itself turns amber, so the only ink the trail
         has to lay is the leg *inside* the landmass you are standing on: from
         the pencil tip to the mouth of the bridge you are taking, bent through
         the middle of the landmass. Routing it to the hub and back out drew
         long diagonals that crossed other bridges; a single quadratic with the
         hub as its control point stays inside the shore, and — the reason it
         is worth the trouble — it is exactly the shape scene 4 calls a pair.
         Synchronous, because a click has to answer at once; scene 2 does its
         own waiting between calls. */
      function cross(b) {
        const from = S.on, to = other(b, from);
        const h = LAND[from].hub, m1 = mouth(b, from), m2 = mouth(b, to);
        const p = ctx.svgEl("path", {
          d: "M " + at(S.tip) + " Q " + at(h) + " " + at(m1), "class": "anim-trail"
        });
        S.gTrail.appendChild(ink(p, far(S.tip, h) + far(h, m1), 400));
        S.used[b] = true;
        S.count += 1;
        S.on = to;
        S.tip = m2;
        paint();
        return to;
      }

      /* -------------------------------------------------------- the clicks */
      /* Scene 3 hands over its three readouts; every other scene calls idle()
         and the map stops answering. */
      function hand(out) {
        S.out = out;
        S.live = true;
        S.grabbed = false;
        S.svg.classList.add("kb-live");
        paint();
      }
      function idle() {
        S.live = false;
        S.out = null;
        if (S.svg) S.svg.classList.remove("kb-live");
        if (S.bridges) paint();
      }

      /* The first click is a grab: it pauses the sequence, exactly as the
         knob does elsewhere, so the city stays yours until you press ▶. */
      function grab() {
        if (S.grabbed) return;
        S.grabbed = true;
        ctx.pause();
      }

      function say(kind, html) {
        if (!S.out) return;
        S.out.msg.className = "kb-msg" + (kind === "no" ? " kb-msg-no" : "");
        S.out.msg.innerHTML = html;
      }

      function report() {
        if (!S.out) return;
        S.out.at.textContent = S.on == null ? "—" : LAND[S.on].id;
        S.out.n.textContent = S.count + " of 7";
        if (S.on == null) say("ok", "Click any landmass to start.");
      }

      function nope(i) {
        const ln = S.bridges[i];
        ln.classList.remove("kb-nope");
        ln.getBoundingClientRect();          /* commit before re-arming */
        ln.classList.add("kb-nope");
      }

      function onLand(k) {
        if (!S.live) return;
        grab();
        if (S.on == null) {
          stand(k);
          report();
          say("ok", "Pencil down on <b>" + LAND[k].id + "</b>. Now click one of its bridges.");
        } else {
          say("no", "You are already walking. Click a <b>bridge</b>, not a landmass.");
        }
      }

      function onBridge(i) {
        if (!S.live) return;
        grab();
        if (S.on == null) {
          nope(i);
          say("no", "Put your pencil down first: click a landmass.");
          return;
        }
        if (S.used[i]) {
          nope(i);
          say("no", "Bridge <b>" + BR[i].n + "</b> is behind you. You may not cross it twice.");
          return;
        }
        if (!touches(i, S.on)) {
          nope(i);
          say("no", "Bridge <b>" + BR[i].n + "</b> does not touch <b>" +
            LAND[S.on].id + "</b>. You cannot reach it from here.");
          return;
        }
        const name = BR[i].n;
        cross(i);
        report();
        const stuck = !INC[S.on].some(function (b) { return !S.used[b]; });
        if (stuck) {
          say("no", "Stuck on <b>" + LAND[S.on].id + "</b> with <b>" + S.count +
            " of 7</b>. Every bridge here is behind you. ↻ Reset and open differently.");
        } else {
          say("ok", "Crossed <b>" + name + "</b>. You are on <b>" +
            LAND[S.on].id + "</b>, " + S.count + " of 7 done.");
        }
      }

      /* --------------------------------------------------- the bridge-ends */
      function spokes() {
        S.gSpoke.textContent = "";
        LAND.forEach(function (L, k) {
          INC[k].forEach(function (b) {
            S.gSpoke.appendChild(ctx.svgEl("path", {
              d: "M " + at(mouth(b, k)) + " L " + at(L.hub), "class": "kb-spoke"
            }));
          });
          S.gSpoke.appendChild(ctx.svgEl("circle",
            { cx: L.hub[0], cy: L.hub[1], r: 3.2, "class": "kb-hub" }));
        });
      }

      /* A pair is drawn as what it means: in over one bridge, through the
         landmass, out over the other. The leftover keeps its spoke and turns
         amber, with a dot on the shore end. */
      function pairAt(P) {
        const L = LAND[P.k];
        P.pairs.forEach(function (pr) {
          const a = mouth(pr[0], P.k), b = mouth(pr[1], P.k);
          S.gPair.appendChild(ink(ctx.svgEl("path", {
            d: "M " + at(a) + " Q " + at(L.hub) + " " + at(b), "class": "kb-pair"
          }), far(a, L.hub) + far(L.hub, b), 500));
        });
        const m = mouth(P.left, P.k);
        S.gPair.appendChild(ctx.svgEl("path",
          { d: "M " + at(m) + " L " + at(L.hub), "class": "kb-left" }));
        S.gPair.appendChild(ctx.svgEl("circle",
          { cx: m[0], cy: m[1], r: 4, "class": "kb-left-dot" }));
      }

      function pairAll() {
        spokes();
        S.gPair.textContent = "";
        PAIRING.forEach(pairAt);
      }

      /* pairAt appends, so scene 4 has to start from an empty group. */
      const spokesFresh = function () { spokes(); S.gPair.textContent = ""; };

      /* S is filled by drawCity(), i.e. after helpers() has already run, so
         everything that reaches into it has to be a function — the kit copies
         these onto ctx by value at mount time. */
      function card(title) {
        side.textContent = "";
        const c = ctx.el("div", "anim-panel anim-pop");
        if (title) c.appendChild(ctx.el("div", "anim-caption", title));
        side.appendChild(c);
        return c;
      }

      return {
        drawCity: drawCity, cap: cap, card: card,
        resetWalk: resetWalk, stand: stand, cross: cross,
        hand: hand, idle: idle, grab: grab, report: report,
        spokes: spokesFresh, pairAt: pairAt, pairAll: pairAll
      };
    }
  });
});
