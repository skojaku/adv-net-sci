/* Robust yet fragile. Markup above, scenes below, and nothing in between: the
   paper, the pen, the motion and the sequencer all come from assets/anim.css +
   assets/anim.js, and everything a scene calls arrives on `ctx`. The kit is
   loaded after this file, hence the animReady queue. */
(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     Every number below was computed once, offline, and pasted in. Nothing in
     this file runs a graph algorithm; the only arithmetic at load is the
     trigonometry that puts thirty dots on a circle.

     TWO GRIDS, both N = 30 towns and E = 60 cables, average degree 4.00.

       RING  every town cabled to its four nearest neighbours round a ring
             (the circulant C30(1,2)). Every degree is exactly 4.
             <k^2>/<k> = 4.00.
       HUBS  three hubs joined in a triangle; the other 27 towns sit in three
             arcs of nine, each cabled to the two hubs bounding its arc; the
             middle town of each arc gets a third cable to the remaining hub.
             Degrees: 21, 21, 21, then three 3s and twenty-four 2s.
             <k^2>/<k> = 12.05.

     Connectivity is the module's own measure: size of the largest connected
     component / 30. Targeted removal is ADAPTIVE — every degree is recomputed
     after every removal, ties broken at random.

     Headline results, and what the widget claims:
       random failure    R = 0.36 (ring)  R = 0.42 (hubs)   hubs ahead
       targeted attack   R = 0.34 (ring)  R = 0.08 (hubs)   hubs annihilated,
                                                            three removals in
       they change places when about one removal in ten is chosen on purpose.
     ------------------------------------------------------------------------ */

  const N = 30;

  const RING_E = [[0,1],[0,2],[0,28],[0,29],[1,2],[1,3],[1,29],[2,3],[2,4],[3,4],[3,5],[4,5],[4,6],[5,6],[5,7],[6,7],[6,8],[7,8],[7,9],[8,9],[8,10],[9,10],[9,11],[10,11],[10,12],[11,12],[11,13],[12,13],[12,14],[13,14],[13,15],[14,15],[14,16],[15,16],[15,17],[16,17],[16,18],[17,18],[17,19],[18,19],[18,20],[19,20],[19,21],[20,21],[20,22],[21,22],[21,23],[22,23],[22,24],[23,24],[23,25],[24,25],[24,26],[25,26],[25,27],[26,27],[26,28],[27,28],[27,29],[28,29]];
  const HUBS_E = [[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,16],[0,21],[0,22],[0,23],[0,24],[0,25],[0,26],[0,27],[0,28],[0,29],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],[1,25],[2,7],[2,12],[2,13],[2,14],[2,15],[2,16],[2,17],[2,18],[2,19],[2,20],[2,21],[2,22],[2,23],[2,24],[2,25],[2,26],[2,27],[2,28],[2,29]];

  /* One removal order per grid per threat, drawn with a fixed seed and frozen
     here as thirty snapshots: g = in the largest component, o = alive but cut
     off, x = removed. Of ten thousand seeds these are the two whose realised
     profiles sit closest to the averages plotted below. */
  const RAND_RING = ["gggggggggggggggggggggggggggggg","ggggggxggggggggggggggggggggggg","ggggggxgggggggggggggggxggggggg","ggggggxgggggggggggggggxxgggggg","gggxggxgggggggggggggggxxgggggg","gggxggxggggggggxggggggxxgggggg","gggxggxggggggggxggggggxxggggxg","gggxggxgxggggggxggggggxxggggxg","gxgxggxgxggggggxggggggxxggggxg","gxgxggxgxggggggxggggggxxooooxx","oxoxooxoxxgggggxggggggxxooooxx","oxoxooxoxxgggggxggggggxxoxooxx","oxoxooxoxxgggggxgxggggxxoxooxx","oxoxooxoxxgggxgxgxggggxxoxooxx","oxoxooxoxxgxgxgxgxggggxxoxooxx","oxoxooxoxxgxgxgxgxggggxxxxooxx","oxoxooxoxxgxgxgxgxgggxxxxxooxx","oxoxooxoxxgxgxgxgxgggxxxxxoxxx","oxoxooxxxxgxgxgxgxgggxxxxxoxxx","gxgxggxxxxoxoxxxoxoooxxxxxoxxx","gxgxggxxxxoxoxxxoxoooxxxxxxxxx","gxgxggxxxxoxoxxxxxoooxxxxxxxxx","xxgxggxxxxoxoxxxxxoooxxxxxxxxx","xxgxggxxxxoxoxxxxxoxoxxxxxxxxx","xxgxggxxxxoxoxxxxxxxoxxxxxxxxx","xxxxggxxxxoxoxxxxxxxoxxxxxxxxx","xxxxggxxxxxxoxxxxxxxoxxxxxxxxx","xxxxggxxxxxxoxxxxxxxxxxxxxxxxx","xxxxgxxxxxxxoxxxxxxxxxxxxxxxxx","xxxxxxxxxxxxgxxxxxxxxxxxxxxxxx"];
  const RAND_HUBS = ["gggggggggggggggggggggggggggggg","gggggggggggggxgggggggggggggggg","gggggggggggggxggggggggggxggggg","gggggggxgggggxggggggggggxggggg","gggggggxgggggxgggxggggggxggggg","gggggggxgggggxgggxggggggxxgggg","xggggggxgggggxgggxggggggxxgggg","xgggxggxgggggxgggxggggggxxgggg","xgggxggxxggggxgggxggggggxxgggg","xgggxxgxxggggxgggxggggggxxgggg","xggxxxgxxggggxgggxggggggxxgggg","xggxxxgxxggggxgggxggggggxxxggg","xxgxxxoxxooogxgggxggggggxxxggg","xxgxxxoxxooogxgxgxggggggxxxggg","xxgxxxoxxooogxgxxxggggggxxxggg","xxgxxxoxxooogxgxxxggggggxxxggx","xxgxxxoxxxoogxgxxxggggggxxxggx","xxgxxxoxxxoogxgxxxgggxggxxxggx","xxgxxxoxxxoogxgxxxgggxxgxxxggx","xxgxxxoxxxoogxgxxxgggxxgxxxxgx","xxgxxxoxxxoogxgxxxgxgxxgxxxxgx","xxgxxxoxxxooxxgxxxgxgxxgxxxxgx","xxgxxxoxxxooxxgxxxgxgxxgxxxxxx","xxgxxxoxxxooxxgxxxgxgxxxxxxxxx","xxgxxxoxxxoxxxgxxxgxgxxxxxxxxx","xxgxxxoxxxoxxxgxxxxxgxxxxxxxxx","xxgxxxxxxxoxxxgxxxxxgxxxxxxxxx","xxgxxxxxxxoxxxxxxxxxgxxxxxxxxx","xxxxxxxxxxgxxxxxxxxxoxxxxxxxxx","xxxxxxxxxxxxxxxxxxxxgxxxxxxxxx"];
  const TARG_RING = ["gggggggggggggggggggggggggggggg","ggggggggggggggggxggggggggggggg","gggggggggggggxggxggggggggggggg","gggggggggxgggxggxggggggggggggg","xggggggggxgggxggxggggggggggggg","xggggggggxgggxggxggggggggxgggg","xgggxggggxgggxggxggggggggxgggg","xgggxggggxgggxggxggxgggggxgggg","xgggxggggxgggxggxggxggxggxgggg","xggxxggggxgggxggxggxggxggxgggg","xooxxggggxgggxggxggxggxggxgggx","xooxxoooxxgggxggxggxggxggxgggx","xooxxoooxxooxxggxggxggxggxgggx","xooxxoooxxooxxggxggxggxggxxoox","xooxxoooxxooxxggxggxggxxoxxoox","xooxxoooxxooxxoxxggxggxxoxxoox","xooxxooxxxooxxoxxggxggxxoxxoox","xggxxooxxxooxxoxxooxxoxxoxxoox","xggxxooxxxooxxoxxoxxxoxxoxxoox","xggxxooxxxooxxoxxoxxxoxxoxxxox","xggxxooxxxxoxxoxxoxxxoxxoxxxox","xoxxxggxxxxoxxoxxoxxxoxxoxxxox","xgxxxoxxxxxoxxoxxoxxxoxxoxxxox","xgxxxoxxxxxoxxoxxxxxxoxxoxxxox","xgxxxoxxxxxxxxoxxxxxxoxxoxxxox","xgxxxoxxxxxxxxxxxxxxxoxxoxxxox","xgxxxoxxxxxxxxxxxxxxxoxxxxxxox","xgxxxoxxxxxxxxxxxxxxxxxxxxxxox","xgxxxxxxxxxxxxxxxxxxxxxxxxxxox","xgxxxxxxxxxxxxxxxxxxxxxxxxxxxx"];
  const TARG_HUBS = ["gggggggggggggggggggggggggggggg","ggxggggggggggggggggggggggggggg","gxxgggggggggoooogooooggggggggg","xxxgoooooooooooooooooooooooooo","xxxgooooooooxooooooooooooooooo","xxxgooooxoooxooooooooooooooooo","xxxgooooxoooxoooooooooooooxooo","xxxgooooxxooxoooooooooooooxooo","xxxgooooxxooxooxooooooooooxooo","xxxgooooxxooxxoxooooooooooxooo","xxxgooooxxooxxoxoooooooxooxooo","xxxgooooxxooxxoxoooooooxoxxooo","xxxgoxooxxooxxoxoooooooxoxxooo","xxxgoxooxxooxxoxooooooxxoxxooo","xxxxgxooxxooxxoxooooooxxoxxooo","xxxxgxooxxoxxxoxooooooxxoxxooo","xxxxgxxoxxoxxxoxooooooxxoxxooo","xxxxgxxoxxoxxxoxoooooxxxoxxooo","xxxxgxxoxxoxxxoxoooooxxxoxxxoo","xxxxgxxoxxoxxxoxoooooxxxoxxxxo","xxxxgxxoxxoxxxoxoxoooxxxoxxxxo","xxxxgxxoxxoxxxoxoxoooxxxxxxxxo","xxxxgxxoxxoxxxoxoxoooxxxxxxxxx","xxxxxxxgxxoxxxoxoxoooxxxxxxxxx","xxxxxxxgxxxxxxoxoxoooxxxxxxxxx","xxxxxxxgxxxxxxoxxxoooxxxxxxxxx","xxxxxxxgxxxxxxoxxxooxxxxxxxxxx","xxxxxxxgxxxxxxoxxxxoxxxxxxxxxx","xxxxxxxxxxxxxxgxxxxoxxxxxxxxxx","xxxxxxxxxxxxxxxxxxxgxxxxxxxxxx"];

  /* Connectivity x 100 after k = 0…29 removals, averaged over 4,000 removal
     orders, at 21 settings of the dial: what fraction of the removals are
     chosen (highest degree first) rather than drawn at random. Row 0 is pure
     chance, row 20 is a perfect attacker, and the widget reads its random and
     targeted curves out of exactly those two rows. */
  const KNOB_RING = [
    [100,97,93,90,86,82,76,70,63,55,49,42,37,33,29,25,22,20,18,16,14,12,11,9,8,7,6,5,4,3],
    [100,97,93,90,86,82,77,70,63,56,49,43,37,32,28,25,22,19,17,15,13,12,10,9,8,7,5,4,4,3],
    [100,97,93,90,86,82,77,71,64,57,50,43,37,32,28,25,22,19,17,14,13,11,10,8,7,6,5,4,4,3],
    [100,97,93,90,86,82,77,71,64,57,50,44,38,32,28,24,21,18,16,14,12,10,9,8,7,6,5,4,4,3],
    [100,97,93,90,86,82,77,72,65,58,51,44,38,33,28,24,21,18,15,13,11,10,9,7,6,5,4,4,3,3],
    [100,97,93,90,87,83,78,72,66,59,52,44,38,32,28,24,20,17,15,13,11,9,8,7,6,5,4,4,3,3],
    [100,97,93,90,87,83,78,73,66,60,52,45,38,32,27,23,20,17,14,12,10,9,8,7,6,5,4,4,3,3],
    [100,97,93,90,87,83,78,73,67,60,53,45,38,32,27,23,19,16,14,12,10,8,7,6,5,4,4,3,3,3],
    [100,97,93,90,87,83,78,73,68,61,54,46,38,32,26,22,19,16,13,11,9,8,7,6,5,4,4,3,3,3],
    [100,97,93,90,87,83,79,74,68,62,54,46,38,31,26,22,18,15,13,10,9,8,7,6,5,4,4,3,3,3],
    [100,97,93,90,87,83,79,74,69,63,55,47,38,31,26,21,18,15,12,10,8,7,6,5,4,4,3,3,3,3],
    [100,97,93,90,87,83,79,75,70,64,56,47,38,31,25,21,17,14,12,9,8,7,6,5,4,4,3,3,3,3],
    [100,97,93,90,87,83,79,75,70,64,56,46,37,30,25,20,17,13,11,9,8,7,6,5,4,4,3,3,3,3],
    [100,97,93,90,87,83,79,75,71,65,57,47,37,30,24,20,16,13,10,8,7,7,6,4,4,3,3,3,3,3],
    [100,97,93,90,87,83,80,76,72,66,58,47,37,30,24,19,16,13,10,8,7,6,5,4,4,3,3,3,3,3],
    [100,97,93,90,87,83,80,76,72,67,58,47,37,29,24,19,15,12,9,8,7,6,5,4,3,3,3,3,3,3],
    [100,97,93,90,87,83,80,76,73,68,59,47,37,29,23,18,15,11,9,7,7,6,5,4,3,3,3,3,3,3],
    [100,97,93,90,87,83,80,76,73,68,59,47,36,29,23,18,14,11,9,7,7,6,4,4,3,3,3,3,3,3],
    [100,97,93,90,87,83,80,76,73,69,60,47,36,28,22,18,14,11,8,7,7,6,4,3,3,3,3,3,3,3],
    [100,97,93,90,87,83,80,77,73,69,60,47,36,28,22,17,13,10,8,7,7,6,4,3,3,3,3,3,3,3],
    [100,97,93,90,87,83,80,77,73,69,59,46,36,28,21,17,13,9,7,7,7,5,3,3,3,3,3,3,3,3]
  ];
  const KNOB_HUBS = [
    [100,97,93,89,86,82,78,74,69,65,61,56,52,48,43,39,35,31,28,24,21,18,15,12,10,8,6,5,4,3],
    [100,97,93,89,84,79,74,69,64,59,54,49,44,39,35,30,27,23,20,17,14,12,10,8,7,6,5,4,4,3],
    [100,97,93,88,82,76,70,64,58,52,46,40,35,30,25,22,18,15,13,11,9,8,6,5,5,4,4,4,3,3],
    [100,97,92,86,79,72,64,57,49,43,36,31,26,21,18,15,12,10,8,7,6,5,5,4,4,4,3,3,3,3],
    [100,97,91,84,76,67,58,49,41,34,28,23,18,15,12,10,8,7,6,5,5,4,4,4,4,3,3,3,3,3],
    [100,97,91,82,72,61,51,42,34,27,21,17,13,10,8,7,6,5,4,4,4,4,3,3,3,3,3,3,3,3],
    [100,97,90,80,68,55,44,34,27,20,15,12,9,8,6,5,5,4,4,4,3,3,3,3,3,3,3,3,3,3],
    [100,97,89,77,62,49,37,27,20,15,11,8,6,5,5,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,88,73,58,44,31,22,16,11,8,6,5,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,87,70,52,37,26,17,12,8,6,5,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,86,66,47,31,20,13,9,6,5,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,84,62,40,25,15,9,6,5,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,83,57,35,20,11,7,5,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,81,52,29,15,8,5,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,80,47,24,11,6,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,78,41,18,8,5,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,76,33,13,6,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,74,26,9,5,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,71,19,6,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,69,11,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [100,97,67,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
  ];

  /* The picture beside each dial setting: one removal order at that setting,
     stopped after six removals — a fifth of the towns — chosen as the run whose
     connectivity lands closest to the average above. It cannot always get
     there: with three hubs, six removals leave the hub grid holding 24, 18, 16
     or 1 town and nothing in between, so in the middle of the dial the picture
     sits on one side of an average no single run can land on. The caption says
     so; no number on screen is read off the picture. */
  const SNAP_AT = 6;
  const SNAP_RING = ["ggggxgxggxxoxxgggggggggggggggg","gggggggxgggxxoxxgggggggggggxgg","ggggxgggxggggggggggggggxxoxxgg","xxoxxgggxgggggggxggggggggggggg","gggxgggggggxxoxxgggggggggggggx","ggggggggggggxxoxxgggggggxggggx","gggggggggggggggxxxxoxxgggggggg","xgxgxxoxxggggggggggggggggggggg","ggggxgggggxgggxgggxgggggxgggxg","gxgggggggxggggxgggxggxgggggxgg","gxggxggxgggggggggggxggxgggxggg","xgggxggxggggggxgggggxggxgggggg","ggxxggggxggggxggggggggxgggggxg","ggggxggxggggxggxggggggggxggggx","ggggggxxggggxgxggggggggxgggggx","ggggxggxgggxggxgggggggxgggggxg","xgggggggxggxggxggxgggxgggggggg","ggggggxgggxgggggxgggxggggxggxg","xgggggxggggggxgggxggggxgggxggg","ggxggxggxgggggggxgggxgggggggxg","xggxggggggxggxgggggxggggggxggg"];
  const SNAP_HUBS = ["xggxgxgxxggggxgggggggggggggggg","gggxxgggggggggggggggggxgxgxggx","gxxggggggggxxoxogooxoggggggggg","gxxgggggggggoxoxgoxoogggggxggg","gxxggxggggxgxooogooooggggxgggg","xxgooooxooooggggxggxgggggxgggg","xxgoooogoooogggxxxggggxggggggg","xxgoooogoooogggggggxgxgxggxggg","xxgoooogooooxgggggggxgggxxgggg","xxxgoxoooooooooxooooooooooooxo","xxxgooooooooooooxoooooxoxooooo","xxxxgooooooooooooxxooooooooooo","xxxgoooxooooxooooooxoooooooooo","xxxgooooooooooooxxooxooooooooo","xxxgooooxooooxoooxoooooooooooo","xxxgooooooooooooxooooooooxxooo","xxxgxooxoooooooooooooooooooxoo","xxxgooooxxoooooxoooooooooooooo","xxxgoooooooooooxoooooooooxoxoo","xxxgoooooooooxooooxoooooooxooo","xxxgxooooooooooooooooooooxooxo"];

  const DET = KNOB_RING.length;      /* 21 detents, 5 percentage points apart */
  const CROSS = 2;                   /* the first detent at which R(hubs) < R(ring) */

  /* The module's own R-index, read straight off the curve the reader is
     looking at, so the number and the picture can never disagree. */
  const rindex = (a) => {
    let s = 0;
    for (let k = 1; k < N; k++) s += a[k] / 100;
    return s / N;
  };
  const R_RING = KNOB_RING.map(rindex);
  const R_HUBS = KNOB_HUBS.map(rindex);

  /* Which town each step took, recovered from the snapshots themselves — the
     order and the pictures are then the same fact, stored once. */
  const removals = (fr) => fr.slice(1).map((f, i) => {
    for (let n = 0; n < N; n++) if (f[n] === "x" && fr[i][n] !== "x") return n;
    return -1;
  });
  const ORDER = {
    randring: removals(RAND_RING), randhubs: removals(RAND_HUBS),
    targring: removals(TARG_RING), targhubs: removals(TARG_HUBS)
  };

  /* Layout, not analysis: thirty dots on a circle of radius 60, and for the
     hub grid three hubs pulled in to radius 26 with their arcs outside them. */
  const RAD = Math.PI / 180;
  const at = (r, deg) => [75 + r * Math.cos(deg * RAD), 75 + r * Math.sin(deg * RAD)];
  const POS = { ring: [], hubs: [] };
  for (let i = 0; i < N; i++) POS.ring.push(at(60, -90 + 12 * i));
  for (let h = 0; h < 3; h++) POS.hubs[h] = at(26, -90 + 120 * h);
  for (let arc = 0; arc < 3; arc++) {
    for (let j = 0; j < 9; j++) POS.hubs[3 + arc * 9 + j] = at(60, -90 + 120 * arc + 12 * (j + 1));
  }
  /* Town size is degree: 4 everywhere on the ring; 21, 3 or 2 on the hub grid. */
  const SIZE = {
    ring: POS.ring.map(() => 4.8),
    hubs: POS.hubs.map((p, i) => (i < 3 ? 8.4 : ((i - 3) % 9 === 4 ? 5.0 : 4.3)))
  };
  const EDGES = { ring: RING_E, hubs: HUBS_E };
  const TITLE = { ring: "the even ring", hubs: "the hub grid" };

  /* chart geometry */
  const CX = (k) => 40 + (k / (N - 1)) * 252;
  const CY = (v) => 108 - v * 90;

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Same money, two ways to spend it",
      note: "Thirty towns and sixty cables on each side — four cables a town, the same bill. The left grid gives every town the same four neighbours. The right pools them into three hubs. Nothing else differs.",
      async run(ctx) {
        ctx.build();
        ctx.caption("the axes below stay put for the rest of the figure: connectivity down the side, towns removed along the bottom.");
        await ctx.sleep(2000);
        ctx.tally("ring", [["towns", "30"], ["cables", "60"], ["busiest town", "4 cables"]]);
        ctx.tally("hubs", [["towns", "30"], ["cables", "60"], ["busiest town", "21 cables"]]);
        await ctx.sleep(3000);
      }
    },
    {
      label: "Random failure: the dice choose",
      note: "Storms and worn-out bearings pick nobody in particular. Both grids shed towns at the same rate at first — then the ring starts breaking into pieces and the hub grid does not. A die almost never lands on a hub.",
      async run(ctx) {
        ctx.untally();
        ctx.caption("connectivity, averaged over 4,000 random removal orders. the grids above show one of those orders.");
        const curve = { ring: ctx.line("anim-amber-stroke"), hubs: ctx.line("anim-accent-stroke") };
        await ctx.run(0, RAND_RING, RAND_HUBS, ORDER.randring, ORDER.randhubs, curve, "die", 15);
        ctx.verdict("<span>same bill, same dice</span><b>the hub grid holds more</b>");
        await ctx.sleep(2800);
      }
    },
    {
      label: "Targeted attack: a hand chooses",
      note: "Same grids, same removal budget — but now each removal takes the largest town left. The even ring has no largest town, so almost nothing changes. The hub grid is gone in three.",
      async run(ctx) {
        ctx.ghost();
        ctx.reset();
        ctx.verdict("");
        ctx.caption("solid: the attacker chooses · faint dashed: the dice chose · every curve an average of 4,000 orders.");
        const curve = { ring: ctx.line("anim-amber-stroke"), hubs: ctx.line("anim-accent-stroke") };
        await ctx.run(DET - 1, TARG_RING, TARG_HUBS, ORDER.targring, ORDER.targhubs, curve, "cross", 3);
        ctx.verdict("<span>hub grid: three towns gone</span><b>and it is dust</b>");
        await ctx.sleep(3000);
      }
    },
    {
      label: "Now you choose who gets removed",
      note: "One dial: what share of the removals are chosen on purpose rather than left to chance. The even ring barely moves. The hub grid slides from the sturdier grid to the ruined one, and the two change places at about one removal in ten.",
      async run(ctx) {
        ctx.wipe();
        ctx.reset();

        const track = ctx.el("div", "anim-track");
        track.appendChild(ctx.el("div", "rf-tick"));
        const knob = ctx.el("div", "anim-knob");
        track.appendChild(knob);
        ctx.dialSlot(track);

        const read = ctx.readout(
          '<span>chosen on purpose <b data-m>0%</b></span>' +
          '<span style="color:var(--_amber)">R even ring <b data-r>0.36</b></span>' +
          '<span style="color:var(--_accent)">R hub grid <b data-h>0.42</b></span>');
        ctx.caption("curves: the average of 4,000 removal orders at that setting; the grids above are one such order, six towns in. the mark on the dial is where the two change places.");

        const guide = ctx.svgEl("line", {
          x1: CX(SNAP_AT), y1: 16, x2: CX(SNAP_AT), y2: 110, "class": "anim-marker anim-marker--faint"
        });
        ctx.chartLayer().appendChild(guide);
        const lr = ctx.line("anim-amber-stroke");
        const lh = ctx.line("anim-accent-stroke");

        const outM = read.querySelector("[data-m]");
        const outR = read.querySelector("[data-r]");
        const outH = read.querySelector("[data-h]");

        /* One knob, and a real one: pointer, touch and arrow keys all land in
           onInput, and grabbing it pauses the sequence so the dial is yours. */
        const dial = ctx.mountKnob(knob, {
          min: 0, max: DET - 1, step: 1, value: 0,
          label: "Share of removals chosen on purpose",
          format: (d) => (d * 5) + "% chosen on purpose",
          onGrab: () => ctx.pause(),
          onInput: (d) => {
            outM.textContent = (d * 5) + "%";
            outR.textContent = R_RING[d].toFixed(2);
            outH.textContent = R_HUBS[d].toFixed(2);
            ctx.setLine(lr, KNOB_RING[d], N - 1);
            ctx.setLine(lh, KNOB_HUBS[d], N - 1);
            ctx.frame("ring", SNAP_RING[d]);
            ctx.frame("hubs", SNAP_HUBS[d]);
            ctx.verdict(d < CROSS
              ? "<span>the hub grid</span><b>still the sturdier one</b>"
              : "<span>the hub grid</span><b>now the fragile one</b>");
          }
        });

        /* Skipping or reading without motion: land past the crossing, because
           the crossing is the thing this figure is about. */
        if (ctx.fast()) { dial.set(6); return; }

        dial.set(0);
        await ctx.sleep(1200);
        for (let d = 1; d < DET; d++) {
          dial.set(d);
          await ctx.sleep(d <= 4 ? 460 : 210);
        }
        await ctx.sleep(1400);
        dial.set(6);
        await ctx.sleep(2600);
      }
    }
  ];

  mountScenes(document.getElementById("rf-attack"), scenes, {
    stepsLabel: "Robustness steps",

    /* The three things only this animation has: two grids that persist across
       all four scenes, one pair of axes underneath them, and a removal loop
       that drives both grids and both curves from the same index. Built once
       at mount, handed to every scene on ctx. */
    helpers(ctx) {
      const box = { ring: ctx.$("[data-rf-ring]"), hubs: ctx.$("[data-rf-hubs]") };
      const chart = ctx.$("[data-rf-chart]");
      const S = { ring: null, hubs: null, c: null };

      function drawGrid(which) {
        const host = box[which];
        host.textContent = "";
        host.appendChild(ctx.el("div", "rf-head", TITLE[which]));

        const wrap = ctx.el("div", "rf-net");
        const svg = ctx.svgRoot("0 0 150 150");
        const g = () => svg.appendChild(ctx.svgEl("g"));
        const gEdge = g(), gNode = g(), gMark = g();
        const pts = POS[which], eds = EDGES[which], rad = SIZE[which];
        const slow = !ctx.fast();

        const edges = eds.map((e, i) => {
          const a = pts[e[0]], b = pts[e[1]];
          let len = Math.hypot(a[0] - b[0], a[1] - b[1]);
          let d = "M " + a[0] + " " + a[1] + " L " + b[0] + " " + b[1];
          /* Thirty towns on one circle put a straight i–(i+2) cable barely a
             unit inside the rim, so the even grid drew as a plain hoop and its
             four-cables-a-town were invisible. Every skip cable is therefore
             bowed into the disc, one control point each, and the ring becomes
             the braid it actually is. */
          if (which === "ring" && Math.min((e[1] - e[0] + N) % N, (e[0] - e[1] + N) % N) === 2) {
            const ux = (a[0] - 75) + (b[0] - 75), uy = (a[1] - 75) + (b[1] - 75);
            const m = Math.hypot(ux, uy) || 1;
            d = "M " + a[0] + " " + a[1] + " Q " + (75 + 40 * ux / m).toFixed(1) + " " +
                (75 + 40 * uy / m).toFixed(1) + " " + b[0] + " " + b[1];
            len *= 1.7;
          }
          const ln = ctx.svgEl("path", {
            d: d, "class": "anim-edge" + (slow ? " anim-draw" : "")
          });
          if (slow) {
            /* --dash must clear the path's own length or it pops in late
               instead of drawing; a bow is longer than its chord. */
            ln.style.setProperty("--dash", Math.ceil(len) + 2);
            ln.style.animationDelay = (0.3 + i * 0.016) + "s";
          }
          return gEdge.appendChild(ln);
        });

        const nodes = pts.map((p, i) => {
          const c = ctx.svgEl("circle", {
            cx: p[0], cy: p[1], r: rad[i],
            "class": "anim-node" + (slow ? " anim-fade" : "")
          });
          if (slow) c.style.animationDelay = (i * 0.028) + "s";
          return gNode.appendChild(c);
        });

        wrap.appendChild(svg);
        host.appendChild(wrap);
        const tally = ctx.el("div", "rf-tally");
        host.appendChild(tally);
        S[which] = { edges, nodes, marks: gMark, eds, pts, tally };
      }

      function drawChart() {
        chart.textContent = "";
        const dialSlot = ctx.el("div", "anim-range");
        const readSlot = ctx.el("div", "anim-readout rf-read");
        const svg = ctx.svgRoot("0 0 300 136");
        svg.innerHTML =
          '<line class="anim-axis" x1="40" y1="108" x2="292" y2="108"/>' +
          '<line class="anim-axis" x1="40" y1="14" x2="40" y2="108"/>' +
          '<text class="anim-label" x="36" y="22" text-anchor="end">1</text>' +
          '<text class="anim-label" x="36" y="111" text-anchor="end">0</text>' +
          '<text class="anim-label" x="13" y="61" text-anchor="middle" transform="rotate(-90 13 61)">connectivity</text>' +
          '<text class="anim-label" x="40" y="124">none removed</text>' +
          '<text class="anim-label" x="292" y="124" text-anchor="end">29 of the 30 gone</text>';
        const layer = svg.appendChild(ctx.svgEl("g"));
        const cap = ctx.el("div", "anim-caption rf-cap");
        const verdict = ctx.el("div", "anim-tally rf-verdict");
        chart.appendChild(dialSlot);
        chart.appendChild(readSlot);
        chart.appendChild(svg);
        chart.appendChild(cap);
        chart.appendChild(verdict);
        S.c = { svg, layer, cap, verdict, readSlot, dialSlot, lines: [] };
      }

      function build() {
        drawGrid("ring");
        drawGrid("hubs");
        drawChart();
      }

      /* A grid at one snapshot. Pure lookup: a town is in the giant component,
         cut off, or gone, and a cable is there unless one of its ends is. */
      function frame(which, str) {
        const s = S[which];
        for (let i = 0; i < N; i++) {
          const c = str[i];
          s.nodes[i].setAttribute("class",
            c === "g" ? "anim-node" : c === "o" ? "anim-node-off" : "rf-out");
        }
        s.eds.forEach((e, i) => {
          const dead = str[e[0]] === "x" || str[e[1]] === "x";
          s.edges[i].setAttribute("class", dead ? "anim-edge rf-cut" : "anim-edge");
        });
      }

      const WHOLE = new Array(N + 1).join("g");
      function reset() { frame("ring", WHOLE); frame("hubs", WHOLE); }

      /* The die that falls on a random town, and the crosshair that closes on
         a chosen one. Decoration, so they never run when we are catching up. */
      function mark(which, node, kind) {
        if (ctx.fast() || ctx.reduced || node < 0) return;
        const s = S[which], p = s.pts[node];
        const g = ctx.svgEl("g");
        g.style.transform = "translate(" + p[0] + "px," + p[1] + "px)";
        const inner = ctx.svgEl("g", { "class": kind === "die" ? "rf-drop" : "rf-snap" });
        if (kind === "die") {
          inner.appendChild(ctx.svgEl("rect",
            { x: -7, y: -7, width: 14, height: 14, rx: 3.5, "class": "rf-die" }));
          [[-3.4, -3.4], [0, 0], [3.4, 3.4]].forEach((q) => {
            inner.appendChild(ctx.svgEl("circle",
              { cx: q[0], cy: q[1], r: 1.5, "class": "rf-pip" }));
          });
        } else {
          inner.appendChild(ctx.svgEl("circle", { r: 13, "class": "rf-cross" }));
          inner.appendChild(ctx.svgEl("path", {
            d: "M -19 0 H -9 M 9 0 H 19 M 0 -19 V -9 M 0 9 V 19", "class": "rf-cross"
          }));
        }
        g.appendChild(inner);
        s.marks.appendChild(g);
        setTimeout(function () { if (g.parentNode) g.parentNode.removeChild(g); }, 950);
      }

      function line(cls) {
        const pl = ctx.svgEl("polyline", { "class": cls, points: "" });
        S.c.layer.appendChild(pl);
        S.c.lines.push(pl);
        return pl;
      }
      function setLine(pl, arr, upto) {
        let s = "";
        for (let k = 0; k <= upto; k++) s += (k ? " " : "") + CX(k) + "," + CY(arr[k] / 100);
        pl.setAttribute("points", s);
      }
      function ghost() {
        S.c.lines.forEach((pl) => {
          pl.setAttribute("class", pl.getAttribute("class") + " rf-ghost");
        });
      }
      function wipe() {
        S.c.layer.textContent = "";
        S.c.lines = [];
      }
      const chartLayer = () => S.c.layer;

      function readout(html) {
        S.c.readSlot.innerHTML = html;
        return S.c.readSlot;
      }
      function caption(t) { S.c.cap.textContent = t; }
      function verdict(html) { S.c.verdict.innerHTML = html; }
      function dialSlot(node) {
        S.c.dialSlot.textContent = "";
        S.c.dialSlot.appendChild(node);
      }

      function tally(which, rows) {
        const t = S[which].tally;
        t.textContent = "";
        rows.forEach((row, i) => {
          const d = ctx.el("div", "anim-tally anim-fade",
            "<span>" + row[0] + "</span><b>" + row[1] + "</b>");
          d.style.animationDelay = ctx.fast() ? "0s" : (i * 0.4) + "s";
          t.appendChild(d);
        });
      }
      function untally() { S.ring.tally.textContent = ""; S.hubs.tally.textContent = ""; }

      /* One removal loop drives both grids, both curves and all three
         readouts, so nothing on screen can drift out of step with anything
         else. `det` says which averaged curve this threat corresponds to. */
      async function run(det, frRing, frHubs, ordRing, ordHubs, pl, kind, freeze) {
        const read = readout(
          '<span>towns removed <b data-k>0 of 30</b></span>' +
          '<span style="color:var(--_amber)">even ring <b data-r>100%</b></span>' +
          '<span style="color:var(--_accent)">hub grid <b data-h>100%</b></span>');
        const outK = read.querySelector("[data-k]");
        const outR = read.querySelector("[data-r]");
        const outH = read.querySelector("[data-h]");

        const show = (k) => {
          outK.textContent = k + " of 30";
          outR.textContent = KNOB_RING[det][k] + "%";
          outH.textContent = KNOB_HUBS[det][k] + "%";
        };

        /* The curve always runs to the end; the two grids are left at the
           snapshot this threat is about, so the pictures and the numbers under
           them are the same moment. */
        if (ctx.fast()) {
          setLine(pl.ring, KNOB_RING[det], N - 1);
          setLine(pl.hubs, KNOB_HUBS[det], N - 1);
          frame("ring", frRing[freeze]);
          frame("hubs", frHubs[freeze]);
          show(freeze);
          return;
        }

        frame("ring", frRing[0]);
        frame("hubs", frHubs[0]);
        setLine(pl.ring, KNOB_RING[det], 0);
        setLine(pl.hubs, KNOB_HUBS[det], 0);
        await ctx.sleep(500);

        for (let k = 1; k < N; k++) {
          mark("ring", ordRing[k - 1], kind);
          mark("hubs", ordHubs[k - 1], kind);
          frame("ring", frRing[k]);
          frame("hubs", frHubs[k]);
          setLine(pl.ring, KNOB_RING[det], k);
          setLine(pl.hubs, KNOB_HUBS[det], k);
          show(k);
          await ctx.sleep(k <= 6 ? 330 : k <= 14 ? 190 : 85);
        }
        await ctx.sleep(900);
        frame("ring", frRing[freeze]);
        frame("hubs", frHubs[freeze]);
        show(freeze);
        await ctx.sleep(500);
      }

      return {
        build, frame, reset, mark, line, setLine, ghost, wipe, chartLayer,
        readout, caption, verdict, dialSlot, tally, untally, run
      };
    }
  });
});
