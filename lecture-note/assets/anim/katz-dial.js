/* ==========================================================================
   katz-dial.js — Turn the dial: Katz centrality as alpha grows.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Mounted by slides/m06/m06-centrality.md ("Turn the dial"). The graph is
   smallgraphs.clique_ring(RING_KATZ): cliques of 4, 4, 4 and 6 joined in a
   ring. The slider sets alpha from 0 to 1.2 / lambda_max; each node is shaded
   by its Katz score c = (I - alpha A)^-1 1, divided by the largest |c|. Near
   alpha = 0 every node scores about 1 and the big clique holds 6/18 = 33%. As
   alpha climbs toward 1 / lambda_max the big clique takes over; at that point
   the series 1 + alpha A + alpha^2 A^2 + ... stops converging, the scores
   blow up, and just past it they come back with the wrong sign.

   Scenes: alpha = 0 (all equal), then the dial.
   ========================================================================== */

(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     SIZES = smallgraphs.RING_KATZ. LAMBDA is the largest eigenvalue of that
     graph's adjacency matrix (smallgraphs prints 5.0841 for it; the full
     value, from numpy, is below). The graph is rebuilt here by the same rule
     as smallgraphs.clique_ring: every clique complete, and clique k's second
     node joined to clique k+1's first node. 37 edges, 18 nodes.

     The scores are NOT a pasted table: solve() below does Gaussian
     elimination on the 18 x 18 system (I - alpha A) c = 1 every time the dial
     moves. It was checked against smallgraphs.katz at k = 0, 20, 50, 90, 99, 100, 101,
     110 and 120 (k below: alpha = k * 0.01 / lambda_max): the normalised scores
     agree to 1e-15, the edge list is identical (37 edges), and the share of
     the total in the big clique agrees at every k. At k = 100, alpha is exactly the
     pole and the matrix is singular, so that one position is solved at
     0.999 / lambda_max and labelled as the blow-up it is.
     ------------------------------------------------------------------------ */
  const SIZES = [4, 4, 4, 6];
  const LAMBDA = 5.0840620328569655;
  const K_MAX = 120;      /* the track has 121 positions: alpha = k * 0.01 / LAMBDA */
  const K_POLE = 100;     /* k at which alpha = 1 / LAMBDA */
  const N = SIZES.reduce(function (a, b) { return a + b; }, 0);

  const EDGES = [];
  const BLOCK = [];       /* BLOCK[k] = [first node, last node + 1] */
  (function () {
    let off = 0;
    const ports = [];
    SIZES.forEach(function (s) {
      for (let i = 0; i < s; i++) {
        for (let j = i + 1; j < s; j++) EDGES.push([off + i, off + j]);
      }
      BLOCK.push([off, off + s]);
      ports.push([off, off + 1]);
      off += s;
    });
    SIZES.forEach(function (_, k) {
      EDGES.push([ports[k][1], ports[(k + 1) % SIZES.length][0]]);
    });
  })();
  const BIG = BLOCK[BLOCK.length - 1];    /* the clique of six */

  /* ------------------------------------------------------------ geometry ---
     The same drawing as the K = 6 frame of the lecture-note GIF ring-local
     (figs_eigen.ring_layout(sizes, 395, 105, radius), radius 42 for the three
     4-cliques, 53 for the 6-clique): four cliques on an ellipse, the clique of
     six at the right. Each 4-clique is a triangle with its fourth node in the
     middle, so no edge crosses another. Coordinates are that function's output
     with y flipped (SVG y runs down), origin at the ellipse's centre, pasted
     rather than recomputed. */
  const POS = [
    [36.4, -84.0], [-36.4, -84.0], [0.0, -147.0], [0.0, -105.0],
    [-374.0, -36.4], [-374.0, 36.4], [-437.0, -0.0], [-395.0, -0.0],
    [-36.4, 84.0], [36.4, 84.0], [-0.0, 147.0], [-0.0, 105.0],
    [349.1, 26.5], [349.1, -26.5], [395.0, -53.0], [440.9, -26.5],
    [440.9, 26.5], [395.0, 53.0]
  ];
  const CENTER_BIG = [395, 0];
  const RADIUS_BIG = 53;
  const VIEW = "-460 -165 940 330";
  const NODE_R = 17;

  /* ----------------------------------------------------------------- math --- */
  function solve(alpha) {
    /* (I - alpha A) c = 1, Gaussian elimination with partial pivoting. */
    const M = [];
    for (let i = 0; i < N; i++) {
      M.push(new Array(N + 1).fill(0));
      M[i][i] = 1;
      M[i][N] = 1;
    }
    EDGES.forEach(function (e) {
      M[e[0]][e[1]] -= alpha;
      M[e[1]][e[0]] -= alpha;
    });
    for (let c = 0; c < N; c++) {
      let p = c;
      for (let r = c + 1; r < N; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
      const t = M[c]; M[c] = M[p]; M[p] = t;
      for (let r = c + 1; r < N; r++) {
        const f = M[r][c] / M[c][c];
        if (f) for (let k = c; k <= N; k++) M[r][k] -= f * M[c][k];
      }
    }
    const x = new Array(N);
    for (let r = N - 1; r >= 0; r--) {
      let s = M[r][N];
      for (let k = r + 1; k < N; k++) s -= M[r][k] * x[k];
      x[r] = s / M[r][r];
    }
    return x;
  }

  function scores(k) {
    const kk = (k === K_POLE) ? K_POLE * 0.999 : k;
    const c = solve(kk * 0.01 / LAMBDA);
    const top = Math.max.apply(null, c.map(Math.abs));
    return { c: c, v: c.map(function (x) { return x / top; }) };
  }

  /* white -> blue for a positive score, white -> gold for a negative one. */
  function tint(v) {
    const base = v >= 0 ? [57, 89, 166] : [218, 177, 103];
    const a = 0.08 + 0.92 * Math.min(1, Math.abs(v));
    const m = function (c) { return Math.round(255 + (c - 255) * a); };
    return "rgb(" + m(base[0]) + "," + m(base[1]) + "," + m(base[2]) + ")";
  }

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "\u03B1 = 0",
      note: "\u03B1 = 0: only the baseline counts, so every node scores the same",
      async run(ctx) {
        ctx.build(false);
        ctx.set(0);
      }
    },
    {
      label: "the dial",
      note: "drag \u03B1 right: the big clique takes over, then the scores break",
      async run(ctx) {
        ctx.build(true);
        ctx.set(50);
        if (ctx.fast()) return;
        await ctx.sleep(30000);
      }
    }
  ];

  mountScenes(document.getElementById("katz-dial"), scenes, {
    stepsLabel: "Katz dial steps",

    helpers(ctx) {
      const drawBox = ctx.$("[data-kd-draw]");
      const sideBox = ctx.$("[data-kd-side]");
      const S = {};

      function build(live) {
        drawBox.textContent = "";
        sideBox.textContent = "";

        /* ------------------------------------------------------- the ring */
        const svg = ctx.svgRoot(VIEW);
        const gHull = svg.appendChild(ctx.svgEl("g"));
        const gEdge = svg.appendChild(ctx.svgEl("g"));
        const gNode = svg.appendChild(ctx.svgEl("g"));
        gHull.appendChild(ctx.svgEl("circle", {
          cx: CENTER_BIG[0], cy: CENTER_BIG[1], r: RADIUS_BIG + NODE_R + 10, "class": "kd-hull"
        }));
        EDGES.forEach(function (e) {
          gEdge.appendChild(ctx.svgEl("line", {
            x1: POS[e[0]][0], y1: POS[e[0]][1], x2: POS[e[1]][0], y2: POS[e[1]][1],
            "class": "anim-edge kd-edge"
          }));
        });
        S.node = POS.map(function (p) {
          return gNode.appendChild(ctx.svgEl("circle",
            { cx: p[0], cy: p[1], r: NODE_R, "class": "kd-node" }));
        });
        drawBox.appendChild(svg);

        /* ------------------------------------------------- the dial + card */
        const panel = ctx.el("div", "anim-panel kd-card");
        S.alpha = ctx.el("div", "kd-alpha", "");
        panel.appendChild(S.alpha);

        const wrap = ctx.el("div", "anim-range kd-range");
        const track = ctx.el("div", "anim-track");
        const mark = ctx.el("div", "kd-mark");
        mark.style.left = (K_POLE / K_MAX * 100) + "%";
        const kn = ctx.el("div", "anim-knob");
        track.appendChild(mark);
        track.appendChild(kn);
        const pole = ctx.el("div", "kd-pole", "1/&lambda;<sub>max</sub>");
        pole.style.left = "calc(7px + (100% - 14px) * " + (K_POLE / K_MAX) + ")";
        wrap.appendChild(pole);
        wrap.appendChild(track);
        const ends = ctx.el("div", "kd-ends");
        ends.appendChild(ctx.el("span", "kd-end0", "0"));
        ends.appendChild(ctx.el("span", "kd-end2", "1.2/&lambda;<sub>max</sub>"));
        wrap.appendChild(ends);
        panel.appendChild(wrap);

        S.share = ctx.el("div", "anim-big kd-share", "");
        panel.appendChild(S.share);
        S.warn = ctx.el("div", "kd-warn", "");
        panel.appendChild(S.warn);
        sideBox.appendChild(panel);

        S.kn = kn;
        S.knob = null;
        if (live) {
          S.knob = ctx.mountKnob(kn, {
            min: 0, max: K_MAX, step: 1, value: 0, track: track,
            label: "alpha, in hundredths of 1 over lambda max",
            format: function (k) { return "alpha = " + (k / 100).toFixed(2) + " over lambda max"; },
            onGrab: function () { ctx.pause(); },
            onInput: function (k) { show(k); }
          });
        } else {
          kn.classList.add("kd-still");
        }
      }

      function show(k) {
        const sc = scores(k);
        sc.v.forEach(function (v, i) { S.node[i].style.fill = tint(v); });
        S.alpha.innerHTML = "&alpha; = " + (k / 100).toFixed(2) + " / &lambda;<sub>max</sub>";
        S.alpha.setAttribute("data-k", String(k));
        if (k < K_POLE) {
          let big = 0, all = 0;
          sc.c.forEach(function (x, i) { all += x; if (i >= BIG[0] && i < BIG[1]) big += x; });
          S.share.textContent = "big clique: " + Math.round(100 * big / all) + "%";
          S.warn.innerHTML = "";
        } else if (k === K_POLE) {
          S.share.textContent = "";
          S.warn.innerHTML = "at 1/&lambda;<sub>max</sub>: scores blow up";
        } else {
          S.share.textContent = "";
          S.warn.innerHTML = "past 1/&lambda;<sub>max</sub>: negative scores";
        }
      }

      /* Put the dial at k, moving the knob if there is one. */
      function set(k) {
        if (S.knob) S.knob.set(k);
        else S.kn.style.left = (k / K_MAX * 100) + "%";
        show(k);
      }

      return { build: build, set: set, show: show };
    }
  });
});
