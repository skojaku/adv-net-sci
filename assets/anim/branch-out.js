/* Why the node at the end of a random edge is not a typical node, and what that
   does to a search. Markup above, scenes below, and nothing in between: the
   paper, the pen, the motion and the sequencer all come from assets/anim.css +
   assets/anim.js, and everything a scene calls arrives on `ctx`. The kit is
   loaded after this file, hence the animReady queue. */
(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     One network, ten nodes and ten edges, with degrees 5 4 3 2 1 1 1 1 1 1.
     Every quantity this stage prints is then exact:

       <k>      = 20 / 10 = 2          mean degree
       <k^2>    = 60 / 10 = 6
       kappa    = <k^2> / <k> = 3      mean degree of the node an edge end
                                       belongs to
       kappa-1  = 2                    edges leading onward from that node
       f_c      = 1 - 1/(kappa-1)      = 0.5

     Its only cycle has length four, so the network contains no triangle and the
     branching argument's own assumption holds on the picture it is argued over.

     The draws in scenes 2 and 3 were generated once, offline, with the seed
     whose running means land exactly on 2.00 and 3.00:

       import random
       r = random.Random(1045)
       nodes = [r.randrange(10) for _ in range(40)]
       ends  = [E[r.randrange(10)][r.randrange(2)] for _ in range(40)]
     ------------------------------------------------------------------------ */

  const E = [[0, 1], [1, 3], [3, 2], [2, 0], [0, 4], [0, 5], [0, 6], [1, 7], [1, 8], [2, 9]];
  const N = 10;
  const DEG = [5, 4, 3, 2, 1, 1, 1, 1, 1, 1];
  const ENDS = 2 * E.length;
  const MEAN_K = 2, KAPPA = 3, BRANCH = KAPPA - 1, F_C = 1 - 1 / BRANCH;

  const NODE_DRAWS = [0, 6, 7, 7, 1, 7, 2, 5, 7, 7, 2, 8, 9, 2, 8, 1, 3, 0, 9, 9,
                      5, 9, 1, 5, 3, 9, 3, 1, 7, 4, 9, 1, 2, 8, 6, 9, 3, 9, 1, 2];
  const END_DRAWS = [1, 0, 4, 1, 0, 1, 5, 0, 8, 5, 8, 9, 4, 0, 1, 2, 0, 7, 0, 0,
                     1, 1, 0, 8, 2, 0, 1, 0, 0, 2, 1, 9, 6, 3, 4, 3, 4, 0, 7, 5];

  const POS = [[110, 120], [190, 60], [190, 185], [255, 122],
               [25, 48], [20, 125], [35, 203], [150, 20], [245, 26], [130, 230]];

  /* The twenty edge ends, as a column of ends under each node, nodes ordered by
     degree. This is the picture the whole first half rests on: a node owns
     exactly as many ends as it has edges, so drawing an end at random is not
     the same as drawing a node at random. */
  const COL = DEG.map((_, i) => i).sort((a, b) => DEG[b] - DEG[a] || a - b);
  const colX = (i) => 18 + i * 29.3;
  const HEAD_Y = 25, END_Y0 = 56, END_DY = 23;

  /* the fan: five levels, and (kappa-1) = 2 onward edges each */
  const LEV = 5;
  const ROW = [1, 2, 4, 8, 16];
  const ROW_Y = [16, 50, 84, 118, 152];
  /* Children sit under their parent, straddling it: x = centre + (i - (n-1)/2)
     * spread / n. Spacing the row evenly across the full width instead put a
     * node's two children at opposite edges of the drawing, and the surviving
     * path read as a zig-zag rather than as a path down a tree. */
  const SPREAD = 248;
  const fanX = (k, i) => 150 + (i - (ROW[k] - 1) / 2) * (SPREAD / ROW[k]);

  /* the dial: f from 0 to 0.75 in twentieths, so f_c = 0.50 is a detent */
  const DET = 16, DF = 0.05;
  const F_AT = (d) => d * DF;
  const CROSS = Math.round(F_C / DF);

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Ten edges, twenty edge ends",
      note: "Each of the ten edges has two ends, so there are twenty of them. Every end belongs to one node, and a node owns exactly as many ends as it has edges: the degree-5 node owns five of the twenty, and each degree-1 node owns one.",
      short: "A node owns one end per edge.",
      async run(ctx) {
        ctx.build();
        ctx.stubs();
        ctx.read("nodes <b>" + N + "</b>", "edge ends <b>" + ENDS + "</b>");
        await ctx.sleep(3000);
      }
    },
    {
      label: "Draw a node at random",
      note: "All ten nodes are equally likely. Over forty draws the mean degree of the node drawn is 2, which is the mean degree of the network.",
      short: "Each node has probability 1/10.",
      async run(ctx) {
        ctx.stubs();
        ctx.read("nodes <b>" + N + "</b>", "edge ends <b>" + ENDS + "</b>");
        await ctx.sample(NODE_DRAWS, "node", MEAN_K, "node drawn");
        await ctx.sleep(2200);
      }
    },
    {
      label: "Draw an edge end at random",
      note: "All twenty edge ends are equally likely, so a node is reached with probability proportional to its degree. The mean degree of the node an end belongs to is 3, not 2. That number is kappa.",
      short: "A node has probability degree / 20.",
      async run(ctx) {
        ctx.stubs();
        ctx.keepMean();
        ctx.read("nodes <b>" + N + "</b>", "edge ends <b>" + ENDS + "</b>");
        await ctx.sample(END_DRAWS, "end", KAPPA, "edge end drawn");
        ctx.verdict("<span>this is</span><b>&kappa; = " + KAPPA + "</b>");
        await ctx.sleep(2800);
      }
    },
    {
      label: "One edge in, kappa minus one out",
      note: "A search that arrives at a node along an edge finds kappa edges there on average, and one of them is the edge it arrived on. It continues along kappa - 1 = 2, so the number of nodes it reaches doubles at every step.",
      short: "One edge in, so kappa - 1 = 2 lead onward.",
      async run(ctx) {
        ctx.fan();
        ctx.read("&kappa; <b>" + KAPPA + "</b>", "arrival edge <b>1</b>",
                 "onward <b>&kappa; &minus; 1 = " + BRANCH + "</b>");
        ctx.verdict("");
        ctx.setF(0);
        if (ctx.fast()) { ctx.grow(LEV); }
        else for (let k = 0; k <= LEV; k++) { ctx.grow(k); await ctx.sleep(700); }
        await ctx.sleep(2400);
      }
    },
    {
      label: "Remove a fraction f of the nodes",
      note: "f is the fraction of nodes removed at random. An onward edge leads to a node that survives with probability 1 - f, so the branching factor is (1 - f)(kappa - 1). Above 1 the search keeps reaching new nodes; below 1 it stops. It equals 1 at f = 0.5.",
      short: "f = the fraction of nodes removed at random.",
      async run(ctx) {
        ctx.fan();
        ctx.grow(LEV);
        const dial = ctx.mountKnob(ctx.dial(), {
          min: 0, max: DET - 1, step: 1, value: 0,
          label: "Fraction of nodes removed",
          format: (d) => "f = " + F_AT(d).toFixed(2),
          onGrab: () => ctx.pause(),
          onInput: (d) => ctx.setF(F_AT(d))
        });
        if (ctx.fast()) { dial.set(CROSS); return; }
        dial.set(0);
        await ctx.sleep(1200);
        for (let d = 1; d <= CROSS + 3; d++) { dial.set(d); await ctx.sleep(620); }
        await ctx.sleep(900);
        dial.set(CROSS);
        await ctx.sleep(3000);
      }
    }
  ];

  mountScenes(document.getElementById("branch-out"), scenes, {
    stepsLabel: "Branching steps",

    helpers(ctx) {
      const netBox = ctx.$("[data-bo-net]");
      const sideBox = ctx.$("[data-bo-side]");
      const S = { nodes: [], edges: [], panel: null, stub: null, fan: null, c: null };

      /* ---- the network, drawn once and kept for every scene ---- */
      function drawNet() {
        netBox.textContent = "";
        const wrap = ctx.el("div", "bo-net");
        const svg = ctx.svgRoot("0 0 300 250");
        const gEdge = svg.appendChild(ctx.svgEl("g"));
        const gNode = svg.appendChild(ctx.svgEl("g"));
        const slow = !ctx.fast();

        S.edges = E.map((e, i) => {
          const a = POS[e[0]], b = POS[e[1]];
          const ln = ctx.svgEl("path", {
            d: "M " + a[0] + " " + a[1] + " L " + b[0] + " " + b[1],
            "class": "anim-edge" + (slow ? " anim-draw" : "")
          });
          if (slow) {
            ln.style.setProperty("--dash", Math.ceil(Math.hypot(a[0] - b[0], a[1] - b[1])) + 2);
            ln.style.animationDelay = (0.15 + i * 0.05) + "s";
          }
          return gEdge.appendChild(ln);
        });

        S.nodes = POS.map((p, i) => {
          const c = ctx.svgEl("circle", { cx: p[0], cy: p[1], r: 17, "class": "anim-node" });
          gNode.appendChild(c);
          const t = ctx.svgEl("text", {
            x: p[0], y: p[1] + 6, "class": "bo-deg", "text-anchor": "middle"
          });
          t.textContent = String(DEG[i]);
          gNode.appendChild(t);
          return c;
        });

        wrap.appendChild(svg);
        netBox.appendChild(wrap);
        netBox.appendChild(ctx.el("div", "anim-caption bo-netcap", "node label = degree"));
      }

      function drawSide() {
        sideBox.textContent = "";
        S.panel = sideBox.appendChild(ctx.el("div", "bo-panel"));
        const means = ctx.el("div", "bo-means");
        const readSlot = ctx.el("div", "anim-readout bo-read");
        const dialSlot = ctx.el("div", "anim-range");
        const verdict = ctx.el("div", "anim-tally bo-verdict");
        [means, readSlot, dialSlot, verdict].forEach((n) => sideBox.appendChild(n));
        S.c = { means, readSlot, dialSlot, verdict, kept: "" };
      }

      /* The kit empties every [data-anim-clear] before each run, so the cached
         panel handles are stale by the time scene 1 rebuilds. Dropping them here
         is what makes stubs() and fan() redraw instead of returning early into a
         panel that no longer exists. */
      function build() { S.stub = null; S.fan = null; drawNet(); drawSide(); }

      /* ---- panel A: the twenty edge ends ---- */
      function stubs() {
        if (S.stub) { resetHighlight(); return; }
        S.panel.textContent = "";
        S.panel.setAttribute("class", "bo-panel bo-panel--stubs");
        S.fan = null;
        const svg = ctx.svgRoot("0 0 300 170");
        const gHead = svg.appendChild(ctx.svgEl("g"));
        const gEnd = svg.appendChild(ctx.svgEl("g"));
        const heads = [], ends = [];
        COL.forEach((n, i) => {
          const x = colX(i);
          heads[n] = gHead.appendChild(ctx.svgEl("circle",
            { cx: x, cy: HEAD_Y, r: 14, "class": "anim-node" }));
          const t = gHead.appendChild(ctx.svgEl("text",
            { x: x, y: HEAD_Y + 5, "class": "bo-headdeg", "text-anchor": "middle" }));
          t.textContent = String(DEG[n]);
          ends[n] = [];
          for (let j = 0; j < DEG[n]; j++) {
            ends[n].push(gEnd.appendChild(ctx.svgEl("rect", {
              x: x - 9, y: END_Y0 + j * END_DY, width: 18, height: 18, rx: 3,
              "class": "bo-end"
            })));
          }
        });
        S.panel.appendChild(svg);
        S.stub = { heads, ends };
      }

      function resetHighlight() {
        if (S.stub) {
          S.stub.heads.forEach((h) => h.setAttribute("class", "anim-node"));
          S.stub.ends.forEach((row) => row.forEach((r) => r.setAttribute("class", "bo-end")));
        }
        S.nodes.forEach((n) => n.setAttribute("class", "anim-node"));
      }

      /* ---- panel B: the branching fan ---- */
      function fan() {
        if (S.fan) return;
        S.panel.textContent = "";
        S.panel.setAttribute("class", "bo-panel bo-panel--fan");
        S.stub = null;
        S.c.means.textContent = "";
        const svg = ctx.svgRoot("0 0 300 170");
        const gEdge = svg.appendChild(ctx.svgEl("g"));
        const gDot = svg.appendChild(ctx.svgEl("g"));
        const gNum = svg.appendChild(ctx.svgEl("g"));
        const rows = [];
        for (let k = 0; k < LEV; k++) {
          const dots = [];
          for (let i = 0; i < ROW[k]; i++) {
            dots.push(gDot.appendChild(ctx.svgEl("circle", {
              cx: fanX(k, i), cy: ROW_Y[k], r: k > 2 ? 4.6 : 6.6, "class": "bo-dead"
            })));
          }
          const num = gNum.appendChild(ctx.svgEl("text", {
            x: 298, y: ROW_Y[k] + 6, "class": "bo-count", "text-anchor": "end"
          }));
          rows.push({ dots, num, links: [] });
        }
        for (let k = 0; k + 1 < LEV; k++) {
          for (let i = 0; i < ROW[k + 1]; i++) {
            rows[k + 1].links.push(gEdge.appendChild(ctx.svgEl("path", {
              d: "M " + fanX(k, i >> 1) + " " + ROW_Y[k] +
                 " L " + fanX(k + 1, i) + " " + ROW_Y[k + 1],
              "class": "bo-link-dead"
            })));
          }
        }
        S.panel.appendChild(svg);
        S.fan = { rows, shown: -1, f: 0 };
      }

      function grow(k) { if (S.fan) { S.fan.shown = k; paint(); } }
      function setF(f) { if (S.fan) { S.fan.f = f; paint(); } }

      /* One dial setting. The survivors are taken from the middle of each row,
         so the branch that lives stays in the centre of the drawing instead of
         collapsing onto its left edge. The exact expected count is printed
         beside every row, because after two steps it stops being a whole number
         and a row of discs alone would misreport it. */
      function paint() {
        const { rows, shown, f } = S.fan;
        const b = (1 - f) * BRANCH;
        const live = [];
        let stopped = false;
        for (let k = 0; k < LEV; k++) {
          const exp = Math.pow(b, k);
          const n = k > shown ? 0 : (stopped ? 0 : Math.min(ROW[k], Math.round(exp)));
          if (n === 0 && k <= shown) stopped = true;
          const from = Math.floor((ROW[k] - n) / 2);
          live.push({ exp, n, from, to: from + n });
        }
        for (let k = 0; k < LEV; k++) {
          const L = live[k];
          const on = (i) => i >= L.from && i < L.to;
          rows[k].dots.forEach((d, i) => {
            d.setAttribute("class", k > shown ? "bo-hidden" : on(i) ? "bo-live" : "bo-dead");
          });
          rows[k].links.forEach((l, i) => {
            const up = live[k - 1];
            const alive = on(i) && (i >> 1) >= up.from && (i >> 1) < up.to;
            l.setAttribute("class", k > shown ? "bo-hidden"
              : alive ? "bo-link-live" : "bo-link-dead");
          });
          rows[k].num.textContent = k > shown ? ""
            : (L.exp >= 10 ? L.exp.toFixed(0)
                           : L.exp.toFixed(L.exp === Math.round(L.exp) ? 0 : 2));
          rows[k].num.setAttribute("class", "bo-count" + (L.n ? "" : " bo-count-dead"));
        }
        if (shown >= 0 && f > 0) {
          read("f <b>" + f.toFixed(2) + "</b>",
               "1 &minus; f <b>" + (1 - f).toFixed(2) + "</b>",
               "branching <b class=\"bo-hot\">" + b.toFixed(2) + "</b>");
          S.c.verdict.innerHTML = b > 1.001
            ? "<span>above 1</span><b>the search continues</b>"
            : b < 0.999
              ? "<span>below 1</span><b>the search stops</b>"
              : "<span>exactly 1</span><b>f = f<sub>c</sub> = " + F_C.toFixed(2) + "</b>";
        }
      }

      /* ---- readouts, captions, dial ---- */
      function read() {
        S.c.readSlot.innerHTML = Array.prototype.map
          .call(arguments, function (t) { return "<span>" + t + "</span>"; }).join("");
      }
      function verdict(html) { S.c.verdict.innerHTML = html; }
      function keepMean() { S.c.kept = S.c.means.innerHTML; }
      function dial() {
        S.c.dialSlot.textContent = "";
        const track = ctx.el("div", "anim-track");
        const tick = ctx.el("div", "bo-tick");
        tick.style.left = (100 * CROSS / (DET - 1)) + "%";
        track.appendChild(tick);
        const knob = ctx.el("div", "anim-knob");
        track.appendChild(knob);
        S.c.dialSlot.appendChild(track);
        return knob;
      }

      /* Forty draws. `kind` says what is drawn: a node (one of the ten column
         heads) or an edge end (one of the twenty squares). Both light the node
         in the network on the left as well, so the room can see that the second
         one lands on the degree-5 node far more often than the first. */
      async function sample(seq, kind, exact, label) {
        const cell = ctx.el("div", "bo-mean");
        cell.innerHTML = '<span class="bo-mean-n" data-m>&ndash;</span>' +
                         '<span class="bo-mean-l">' + label + "</span>";
        S.c.means.innerHTML = S.c.kept;
        S.c.means.appendChild(cell);
        const outM = cell.querySelector("[data-m]");
        let sum = 0;
        const counter = new Array(N).fill(0);
        for (let i = 0; i < seq.length; i++) {
          const v = seq[i];
          sum += DEG[v];
          counter[v]++;
          outM.textContent = (sum / (i + 1)).toFixed(2);
          if (!ctx.fast()) {
            resetHighlight();
            S.nodes[v].setAttribute("class", "bo-hit");
            S.stub.heads[v].setAttribute("class", "bo-hit");
            if (kind === "end") {
              const j = (counter[v] - 1) % DEG[v];
              S.stub.ends[v][j].setAttribute("class", "bo-end bo-end-hit");
            }
            await ctx.sleep(i < 6 ? 460 : i < 18 ? 200 : 90);
          }
        }
        resetHighlight();
        outM.textContent = exact.toFixed(2);
      }

      return { build, stubs, fan, grow, setF, read, verdict, dial, sample, keepMean };
    }
  });
});
