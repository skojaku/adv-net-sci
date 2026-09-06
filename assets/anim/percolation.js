/* Site percolation on a square lattice, with the occupation probability in the
   room's hands. Markup above, scenes below, and nothing in between: the paper,
   the pen, the motion and the sequencer all come from assets/anim.css +
   assets/anim.js, and everything a scene calls arrives on `ctx`. The kit is
   loaded after this file, hence the animReady queue. */
(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     One 28 x 28 = 784 cell lattice, fixed once so the picture is the same in
     every lecture. FIELD[i] is the threshold of cell i times 1000: the cell is
     occupied exactly when FIELD[i] < 1000p. Nothing is re-drawn when the dial
     moves, so lowering p vacates exactly the cells that raising it occupied,
     which is what makes the third scene a demonstration and not a reshuffle.

     Reproduce the field and both curves with:

       import numpy as np
       field = (np.random.default_rng(11).random((28, 28)) * 1000).astype(int)
       # largest 4-connected cluster of (field < 1000p), as a share of 784

     LATTICE is that share for THIS lattice at each of the 23 dial settings, a
     deterministic function of FIELD, so the dot on the chart and the number in
     the readout are the same fact. BIG is the same measurement on a 220 x 220
     lattice averaged over four of them: the same transition, without the finite
     size of a 28 x 28 lattice rounding it off.

       p              0.575   0.600   0.625
       28 x 28        0.196   0.561   0.602
       220 x 220      0.093   0.289   0.540

     The percolation threshold of the square lattice is p_c = 0.5927 (Newman &
     Ziff 2000); the dial's mark sits there.
     ------------------------------------------------------------------------ */

  const G = 28;
  const CELLS = G * G;
  const FIELD = (
    "128,499,601,28,147,928,70,129,948,621,368,511,662,275,137,788,670,512,816,549,980,204,553,48" +
    "3,353,591,235,802,867,128,467,277,83,895,429,147,673,202,901,217,33,200,345,468,906,697,339," +
    "16,159,996,459,691,54,34,845,587,308,317,89,172,24,839,466,127,739,195,61,598,895,26,805,190" +
    ",92,17,292,727,493,852,217,315,258,978,941,340,436,314,746,40,67,404,245,845,741,545,661,692" +
    ",781,927,149,626,143,443,786,894,759,35,359,163,998,144,244,357,60,870,636,159,498,78,610,23" +
    "1,38,115,555,636,324,643,352,130,315,395,912,115,86,561,963,907,700,66,806,683,143,464,49,80" +
    "1,718,804,760,267,789,249,137,390,497,285,605,602,239,622,357,734,290,798,415,553,673,518,25" +
    "7,979,96,324,549,28,154,799,783,636,901,755,298,644,340,749,384,153,876,690,744,559,782,447," +
    "565,62,555,814,705,803,496,881,108,875,371,90,619,454,428,852,137,616,413,528,499,134,512,86" +
    "2,171,11,67,459,974,44,990,536,120,418,207,714,541,287,255,866,766,436,405,737,970,79,159,36" +
    "2,507,71,53,219,385,739,609,29,45,452,874,914,365,887,929,406,746,365,153,575,86,663,809,915" +
    ",448,117,902,870,967,593,673,373,183,291,720,324,691,502,448,967,166,487,159,937,488,331,168" +
    ",594,398,127,32,391,583,518,900,911,936,799,477,523,397,399,41,798,246,29,466,717,436,364,65" +
    "8,162,11,592,530,865,415,786,17,27,598,226,67,127,374,337,563,887,365,184,578,2,384,317,387," +
    "50,554,624,749,957,354,656,442,215,889,745,942,821,917,128,15,198,412,687,438,513,760,70,678" +
    ",48,248,722,683,405,294,828,274,31,247,21,810,122,973,212,306,585,308,379,104,389,25,223,909" +
    ",280,270,679,882,295,376,714,792,613,178,180,757,706,896,779,421,133,890,695,576,681,385,343" +
    ",575,482,708,936,847,387,372,926,394,800,92,451,516,808,877,152,617,629,151,833,553,961,186," +
    "524,323,642,608,512,324,503,372,890,461,475,258,253,953,314,868,594,980,164,941,772,568,708," +
    "722,448,634,228,21,676,474,905,264,817,986,898,964,159,165,228,361,115,150,18,933,361,626,45" +
    "4,743,806,382,535,97,285,222,308,324,575,332,326,831,12,5,57,865,633,727,957,218,920,242,518" +
    ",681,797,248,477,45,287,980,905,582,786,902,331,980,448,158,530,593,692,670,41,639,921,670,9" +
    "75,511,810,140,895,436,876,320,624,846,711,619,970,87,101,551,954,686,309,107,448,480,468,61" +
    "9,272,880,288,107,348,935,159,277,926,348,843,45,888,237,180,742,989,959,752,914,987,552,144" +
    ",849,395,312,500,34,18,264,595,749,957,818,941,636,733,587,81,61,760,202,789,464,6,561,443,7" +
    "3,261,306,345,706,167,443,606,946,114,79,191,220,162,75,209,223,479,647,363,168,94,263,170,4" +
    "81,871,716,203,35,67,435,363,682,83,254,685,568,516,901,113,195,565,565,980,977,587,758,697," +
    "132,602,305,358,156,8,853,717,752,288,417,176,602,839,778,933,260,701,126,536,110,540,542,34" +
    "6,349,711,481,407,112,282,847,971,373,870,873,218,273,696,306,955,365,730,707,213,865,328,11" +
    "0,50,451,632,271,841,267,847,33,262,159,447,350,394,851,579,605,390,808,501,746,914,612,435," +
    "263,912,764,799,221,436,883,245,813,538,218,375,76,673,726,28,301,768,200,536,805,569,122,90" +
    "9,746,564,332,582,391,118,122,45,170,245,635,580,590,822,95,388,79,418,78,66,104,389,763,281" +
    ",741,233,287,471,74,448,583,824,56,799,569,578,51,879,277,546,538,910,601,991,232,662,576,51" +
    "3,627,550"
  ).split(",").map(Number);

  const P0 = 0.30, DP = 0.025, DET = 23;
  const P_AT = (d) => P0 + d * DP;
  const LATTICE = [0.024,0.028,0.028,0.031,0.040,0.052,0.054,0.054,0.061,0.122,0.177,
                0.196,0.561,0.602,0.633,0.659,0.688,0.714,0.769,0.787,0.811,0.841,0.858];
  const BIG  = [0.001,0.001,0.001,0.001,0.002,0.003,0.004,0.005,0.007,0.012,0.020,
                0.093,0.289,0.540,0.609,0.652,0.686,0.716,0.744,0.771,0.797,0.823,0.848];
  const PC = 0.5927;
  const CROSS = 12;              /* the first detent above p_c */
  const CELL = 10;               /* drawing units per cell */

  /* chart geometry, in the chart's own viewBox units */
  const CX = (p) => 44 + ((p - P0) / (DET - 1) / DP) * 238;
  const CY = (v) => 112 - v * 92;

  /* The largest cluster of the lattice on screen, computed from the lattice on
     screen. 784 cells is nothing to walk, and computing it here rather than
     reading it off a table is what guarantees that the red cells and the
     printed number are the same fact. */
  function largestCluster(occupied) {
    const par = new Int16Array(CELLS);
    for (let i = 0; i < CELLS; i++) par[i] = i;
    const find = (x) => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; };
    const uni = (a, b) => { const ra = find(a), rb = find(b); if (ra !== rb) par[ra] = rb; };
    for (let y = 0; y < G; y++) {
      for (let x = 0; x < G; x++) {
        const i = y * G + x;
        if (!occupied[i]) continue;
        if (x + 1 < G && occupied[i + 1]) uni(i, i + 1);
        if (y + 1 < G && occupied[i + G]) uni(i, i + G);
      }
    }
    const size = new Int16Array(CELLS);
    let best = -1, bestN = 0;
    for (let i = 0; i < CELLS; i++) {
      if (!occupied[i]) continue;
      const r = find(i);
      if (++size[r] > bestN) { bestN = size[r]; best = r; }
    }
    const inBig = new Uint8Array(CELLS);
    if (best >= 0) for (let i = 0; i < CELLS; i++) if (occupied[i] && find(i) === best) inBig[i] = 1;
    return { inBig, share: bestN / CELLS };
  }

  const STATE = [];              /* one occupied/empty/in-largest map per dial setting */
  for (let d = 0; d < DET; d++) {
    const thr = P_AT(d) * 1000;
    const occupied = new Uint8Array(CELLS);
    for (let i = 0; i < CELLS; i++) occupied[i] = FIELD[i] < thr ? 1 : 0;
    const { inBig, share } = largestCluster(occupied);
    STATE.push({ occupied, inBig, share });
  }

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "A 28 x 28 square lattice",
      note: "Each cell is occupied with probability p, independently of the others. Occupied cells that share an edge belong to the same cluster.",
      short: "Each cell occupied with probability p.",
      async run(ctx) {
        ctx.build();
        ctx.show(0);
        ctx.verdict("");
        await ctx.sleep(2600);
      }
    },
    {
      label: "Raising p",
      note: "The number of occupied cells grows steadily with p. The largest cluster does not: it stays small, then within a few hundredths of p it spans the lattice.",
      short: "The largest cluster does not grow steadily.",
      async run(ctx) {
        ctx.trace(true);
        if (ctx.fast()) { ctx.show(CROSS + 1); return; }
        for (let d = 0; d < DET; d++) {
          ctx.show(d);
          await ctx.sleep(d >= 9 && d <= 14 ? 700 : 320);
        }
        ctx.verdict("<span>p 0.575 to 0.600</span><b>cluster 0.20 to 0.56</b>");
        await ctx.sleep(2400);
      }
    },
    {
      label: "Crossing the threshold by hand",
      note: "The dial moves p in steps of 0.025. Between p = 0.575 and p = 0.600 the largest cluster goes from a fifth of the lattice to more than half.",
      short: "One step of 0.025 across the threshold.",
      async run(ctx) {
        ctx.verdict("");
        const knob = ctx.dial();
        const dial = ctx.mountKnob(knob, {
          min: 0, max: DET - 1, step: 1, value: CROSS,
          label: "Occupation probability p",
          format: (d) => "p = " + P_AT(d).toFixed(3),
          onGrab: () => ctx.pause(),
          onInput: (d) => ctx.show(d)
        });
        if (ctx.fast()) { dial.set(CROSS); return; }
        dial.set(CROSS - 2);
        await ctx.sleep(1500);
        dial.set(CROSS - 1);
        await ctx.sleep(1500);
        dial.set(CROSS);
        await ctx.sleep(3000);
      }
    }
  ];

  mountScenes(document.getElementById("percolation"), scenes, {
    stepsLabel: "Percolation steps",

    helpers(ctx) {
      const latticeBox = ctx.$("[data-pc-lattice]");
      const chartBox = ctx.$("[data-pc-chart]");
      const S = { cells: [], c: null, tracing: false };

      function drawLattice() {
        latticeBox.textContent = "";
        const wrap = ctx.el("div", "pc-lattice");
        const svg = ctx.svgRoot("0 0 " + G * CELL + " " + G * CELL);
        const g = svg.appendChild(ctx.svgEl("g"));
        S.cells = [];
        for (let i = 0; i < CELLS; i++) {
          const r = ctx.svgEl("rect", {
            x: (i % G) * CELL + 0.7, y: Math.floor(i / G) * CELL + 0.7,
            width: CELL - 1.4, height: CELL - 1.4, rx: 1.4, "class": "pc-dry"
          });
          S.cells.push(g.appendChild(r));
        }
        wrap.appendChild(svg);
        latticeBox.appendChild(wrap);
      }

      function drawChart() {
        chartBox.textContent = "";
        const dialSlot = ctx.el("div", "anim-range");
        const readSlot = ctx.el("div", "anim-readout pc-read");
        const svg = ctx.svgRoot("0 0 300 140");
        svg.innerHTML =
          '<line class="anim-axis" x1="44" y1="112" x2="288" y2="112"/>' +
          '<line class="anim-axis" x1="44" y1="16" x2="44" y2="112"/>' +
          '<text class="anim-label" x="39" y="24" text-anchor="end">1</text>' +
          '<text class="anim-label" x="39" y="115" text-anchor="end">0</text>' +
          '<text class="anim-label" x="15" y="64" text-anchor="middle" transform="rotate(-90 15 64)">largest cluster</text>' +
          '<text class="anim-label" x="44" y="128">p = 0.30</text>' +
          '<text class="anim-label" x="288" y="128" text-anchor="end">p = 0.85</text>';
        const layer = svg.appendChild(ctx.svgEl("g"));
        /* the reference curve first, so this lattice's own trace sits on top */
        let d = "";
        for (let i = 0; i < DET; i++) d += (i ? " " : "") + CX(P_AT(i)) + "," + CY(BIG[i]);
        layer.appendChild(ctx.svgEl("polyline", { points: d, "class": "pc-big" }));
        layer.appendChild(ctx.svgEl("line", {
          x1: CX(PC), y1: 16, x2: CX(PC), y2: 112, "class": "anim-marker"
        }));
        layer.appendChild(ctx.svgEl("text", {
          x: CX(PC) + 4, y: 26, "class": "anim-label pc-pc"
        })).textContent = "0.59";
        const trace = layer.appendChild(ctx.svgEl("polyline", { points: "", "class": "pc-trace" }));
        const dot = layer.appendChild(ctx.svgEl("circle", { r: 4, "class": "pc-dot" }));
        const verdict = ctx.el("div", "anim-tally pc-verdict");
        chartBox.appendChild(readSlot);
        chartBox.appendChild(svg);
        chartBox.appendChild(dialSlot);
        chartBox.appendChild(verdict);
        S.c = { layer, trace, dot, verdict, readSlot, dialSlot, seen: [] };
      }

      function build() { drawLattice(); drawChart(); S.tracing = false; }

      /* One dial setting: the lattice, the dot, the trace and the readout, all
         driven from the one index. */
      function show(d) {
        const st = STATE[d];
        for (let i = 0; i < CELLS; i++) {
          S.cells[i].setAttribute("class",
            st.inBig[i] ? "pc-in-largest" : st.occupied[i] ? "pc-occupied" : "pc-empty");
        }
        const p = P_AT(d);
        S.c.dot.setAttribute("cx", CX(p));
        S.c.dot.setAttribute("cy", CY(st.share));
        if (S.tracing) {
          if (S.c.seen.indexOf(d) < 0) S.c.seen.push(d);
          S.c.seen.sort((a, b) => a - b);
          S.c.trace.setAttribute("points", S.c.seen
            .map((k) => CX(P_AT(k)) + "," + CY(LATTICE[k])).join(" "));
        }
        S.c.readSlot.innerHTML =
          "<span>p <b>" + p.toFixed(3) + "</b></span>" +
          "<span>cells occupied <b>" + Math.round(p * 100) + "%</b></span>" +
          '<span style="color:var(--_amber)">largest cluster <b>' +
          Math.round(st.share * 100) + "%</b></span>";
      }

      function trace(on) { S.tracing = on; S.c.seen = []; }
      function verdict(html) { S.c.verdict.innerHTML = html; }
      function dial() {
        S.c.dialSlot.textContent = "";
        const track = ctx.el("div", "anim-track");
        const knob = ctx.el("div", "anim-knob");
        track.appendChild(knob);
        S.c.dialSlot.appendChild(track);
        return knob;
      }

      return { build, show, trace, verdict, dial };
    }
  });
});
