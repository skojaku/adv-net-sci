/* ==========================================================================
   h1n1-ruler.js — The H1N1 ruler swap.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header
   of assets/anim.js for the contract, and the markup this expects.

   Loaded by lecture-note/intro/why-networks.qmd and slides/intro/intro.md.
   It lives in a file rather than inline in either of them because those two
   would otherwise be two copies of the same 500 lines of hand-checked data,
   and the first fix to one of them would silently not reach the other.

   The stage's own layout CSS stays with each page: the note has a column to
   fill and the slide has a 1280x720 frame, so the sizes differ even though
   every colour, class and coordinate here is shared.
   ========================================================================== */

/* The ruler swap. Scenes and nothing in between: the paper, the pen, the
   motion and the sequencer all come from assets/anim.css + assets/anim.js,
   and everything a scene calls arrives on `ctx`. The markup stays with
   whichever page mounts this. The kit may load after this file, hence the
   animReady queue. */
(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     Every number below was computed once, offline, and pasted in. Nothing
     here runs a shortest-path search, or any other algorithm, at page load.

     28 countries. Four are named and carry the argument: Mexico (the origin,
     day 0), the United States (3,030 km, day 29 — the first country outside
     Mexico), Spain (9,070 km, day 41) and Guatemala (1,090 km, day 49).
     Guatemala is 8.3x nearer than Spain and was reached 8 days later; that
     pair is the paradox this page opens with. The other 24 are an anonymous
     cloud shaped like panel D of Brockmann & Helbing: a weak rise, plus a
     column of five countries at ~9,000 km whose arrival days run 41 to 121.

     The effective distances were NOT re-derived from an airline timetable.
     Each is the country's arrival day over a slope of 9.5 days per unit,
     plus a residual, and the residuals were scaled by bisection until the
     least-squares fit of arrival day on effective distance landed on exactly
     the R^2 = 0.973 that Brockmann & Helbing report. The picture therefore
     reproduces their published relationship rather than rediscovering it —
     which is what "redrawn schematically" on the caption means.

       R^2 of arrival day on kilometres           0.189
       R^2 of arrival day on effective distance   0.973

     Coordinates are stored already projected into the viewBox:
       x_geo = 58 + km  / 20000 * 388     (axis 0 .. 20,000 km)
       x_eff = 58 + eff / 16    * 388     (axis 0 .. 16)
       y     = 214 - day / 150  * 184     (axis 0 .. 150 days)
     ------------------------------------------------------------------------ */
  const GEOX = [58,116.8,234,79.1,124,133.7,118.1,100.7,226.8,240.4,248.1,259.8,236.5,230.7,253.9,205.4,275.3,271.4,300.5,318,364.5,376.2,341.2,397.5,156.9,182.2,290.8,92.9];
  const EFFX = [58,104.1,154.3,194,300,288.9,283.5,225.6,376.4,281.8,225.8,162.5,176.6,174.2,161.1,204.7,164.9,237.5,226.3,313.8,229.7,361.6,398.7,362.1,337.6,246.4,371.3,148.7];
  const DAYY = [214,178.4,163.7,153.9,96.2,118.3,109.7,130.6,65.6,106.1,137.9,157.6,160,161.3,158.8,151.4,156.3,134.3,149,91.3,140.4,69.3,57,79.1,76.6,123.2,54.5,162.5];

  /* The four named dots: index, label, and the offset its label sits at.
     A label travels with its dot, so each offset had to clear every other
     dot under BOTH rulers at once; these are the smallest that do, found by
     sweeping the offset grid offline. They still get a paper-coloured
     knockout (.anim-knockout) so a near miss is never a collision. */
  const NAMED = [
    [0, "Mexico", 8, -6, "start"],
    [1, "USA", -8, 0, "end"],
    [2, "Spain", -13, 3, "end"],
    [3, "Guatemala", 21, 10, "start"]
  ];
  const SPAIN = 2, GUATEMALA = 3;

  /* 21 detents of the blend x = (1-t) * x_geo + t * x_eff, t = i / 20.
     R2B[i] is the least-squares R^2 of arrival day against that blended
     coordinate; SEG[i] is the fitted line itself, already clipped to the
     plot box as [x1, y1, x2, y2]. Both computed on the 28 points above. */
  const DET = 21;
  const R2B = [0.189,0.222,0.26,0.302,0.348,0.397,0.45,0.505,0.561,0.617,0.672,0.725,0.775,0.82,0.86,0.894,0.922,0.943,0.959,0.968,0.973];
  const SEG = [[58,157.9,446,85.2],[58,161.7,446,80.5],[58,165.8,446,75.5],[58,170.1,446,70.3],[58,174.6,446,65],[58,179.3,446,59.7],[58,184,446,54.3],[58,188.7,446,49.1],[58,193.2,446,44.2],[58,197.5,446,39.7],[58,201.5,446,35.7],[58,205,446,32.3],[58,208,445.3,30],[58,210.4,441.3,30],[58,212.1,439.1,30],[58,213.2,438.5,30],[58,213.7,439.4,30],[58,213.6,441.6,30],[58,213,445.1,30],[58,212,446,31.7],[58,210.6,446,34.2]];

  /* Step 2: three legs out of Mexico City, on the page's own numbers.
     length = 1 - ln(p), so p = 1/5 -> 2.61, 1/10 -> 3.30, 1/1000 -> 7.91.
     A leg is DRAWN at its effective length (x = 52 + 46 * len) and drawn
     with thickness sqrt(p) * 24.6, so a fat pipe is visibly fat and visibly
     short. The kilometres beside each destination run the other way. */
  const LEGS = [
    { y: 40, w: 11, x: 172.1, cls: "anim-edge", side: 1,
      who: "Los Angeles · 2,500 km", how: "1 in 5 → length 2.6" },
    { y: 92, w: 7, x: 203.8, cls: "anim-edge anim-accent-stroke", side: 1,
      who: "Madrid · 9,100 km", how: "1 in 10 → length 3.3" },
    { y: 144, w: 1.6, x: 415.9, cls: "anim-edge anim-amber-stroke", side: 0,
      who: "Guatemala City · 1,100 km", how: "1 in 1000 → length 7.9" }
  ];

  const GEO_TICK = [[58, "0"], [155, "5"], [252, "10"], [349, "15"], [446, "20"]];
  const EFF_TICK = [[58, "0"], [155, "4"], [252, "8"], [349, "12"], [446, "16"]];
  const DAY_TICK = [[214, "0"], [152.7, "50"], [91.3, "100"], [30, "150"]];
  const KM9 = 232.6;          /* where 9,000 km lands on the geographic axis */

  const pct = (i) => Math.round((i / (DET - 1)) * 100);
  const ruler = (i) => i === 0 ? "kilometres"
    : i === DET - 1 ? "effective distance" : pct(i) + "% effective";

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "The map's answer",
      note: "Twenty-eight countries: kilometres from Mexico City across, the day the virus arrived up. It is a cloud. Spain is eight times farther away than Guatemala and was infected eight days earlier.",
      async run(ctx) {
        ctx.drawPlot();
        const c = ctx.card("the map's answer");
        c.appendChild(ctx.el("div", "anim-readout",
          "<span>ruler: <b>kilometres</b></span>" +
          "<span style=\"color:var(--_amber)\">R&sup2; <b>0.19</b></span>"));

        await ctx.sleep(2300);
        ctx.spot(SPAIN, true);
        ctx.spot(GUATEMALA, true);
        [["Spain", "9,070 km · day 41"],
         ["Guatemala", "1,090 km · day 49"]].forEach((row, i) => {
          const t = ctx.el("div", "anim-tally anim-fade",
            "<span>" + row[0] + "</span><b>" + row[1] + "</b>");
          t.style.animationDelay = ctx.fast() ? "0s" : (i * 0.5) + "s";
          c.appendChild(t);
        });
        await ctx.sleep(1500);
        c.appendChild(ctx.el("div", "anim-quote anim-fade",
          "eight times nearer, eight days later"));
        await ctx.sleep(1600);

        ctx.mark(true);
        c.appendChild(ctx.el("div", "anim-caption anim-fade",
          "and along the dashed line: five countries, all within 400 km of " +
          "nine thousand — the first reached on day 41, the last on day 121"));
        await ctx.sleep(3000);
      }
    },
    {
      label: "A fat pipe is a short pipe",
      note: "The mechanism. Give a flight leg the length 1 minus the log of the share of passengers who take it. A leg carrying one traveller in five is short; a leg carrying one in a thousand is long. Madrid is nine thousand kilometres out and three units away.",
      async run(ctx) {
        ctx.dim(0.28);
        ctx.mark(false);
        ctx.spot(SPAIN, false);
        ctx.spot(GUATEMALA, false);
        const c = ctx.card("stop counting kilometres, start counting travellers");

        const svg = ctx.svgRoot("0 0 470 194");
        const put = (tag, attrs, cls, txt) => {
          const n = ctx.svgEl(tag, attrs);
          if (cls) n.setAttribute("class", cls);
          if (txt != null) n.textContent = txt;
          return svg.appendChild(n);
        };
        const slow = !ctx.fast();

        put("text", { x: 6, y: 13 }, "anim-label",
          "how long is one flight leg out of Mexico City?");
        /* The ruler sits under the three legs, not over them: a leg is drawn
           at its own length, so the scale has to be readable beside them. */
        put("line", { x1: 52, y1: 168, x2: 420, y2: 168 }, "anim-axis");
        [[52, "0"], [144, "2"], [236, "4"], [328, "6"], [420, "8"]].forEach((t) => {
          put("line", { x1: t[0], y1: 168, x2: t[0], y2: 172 }, "anim-axis");
          put("text", { x: t[0], y: 185, "text-anchor": "middle" }, "anim-label", t[1]);
        });
        put("line", { x1: 52, y1: 40, x2: 52, y2: 144 }, "anim-edge");

        LEGS.forEach((g, i) => {
          const p = put("line", { x1: 52, y1: g.y, x2: g.x, y2: g.y },
            g.cls + (slow ? " anim-draw" : ""));
          p.style.strokeWidth = g.w;
          if (slow) {
            /* --dash must clear the line's own length or it pops in late. */
            p.style.setProperty("--dash", Math.ceil(g.x - 52) + 4);
            p.style.animationDelay = (0.35 + i * 0.9) + "s";
            p.style.animationDuration = "0.7s";
          }
          /* A leg that reaches the right-hand edge has to caption itself
             leftwards, and then the caption would lie along its own pipe —
             so that one is stacked above the pipe instead of astride it. */
          const anch = g.side ? "start" : "end";
          const tx = g.side ? g.x + 10 : g.x - 10;
          const ty = g.side ? [g.y - 5, g.y + 9] : [g.y - 28, g.y - 13];
          const kids = [
            put("circle", { cx: g.x, cy: g.y, r: 5.5 }, "anim-node"),
            put("text", { x: tx, y: ty[0], "text-anchor": anch }, "anim-label", g.who),
            put("text", { x: tx, y: ty[1], "text-anchor": anch }, "anim-label anim-faint", g.how)
          ];
          if (slow) {
            kids.forEach((n, k) => {
              n.classList.add("anim-fade");
              n.style.animationDelay = (1.0 + i * 0.9 + k * 0.12) + "s";
            });
          }
        });
        put("circle", { cx: 52, cy: 92, r: 6 }, "anim-node");
        c.appendChild(svg);

        const q = ctx.el("div", "anim-quote anim-fade",
          "the fat pipe is the short one — and Madrid is far fatter than Guatemala City");
        q.style.animationDelay = ctx.fast() ? "0s" : "3.5s";
        c.appendChild(q);
        await ctx.sleep(5400);
      }
    },
    {
      label: "Change the ruler",
      note: "Same countries, same arrival days, no new data. Only the axis changes: kilometres out, effective distance in. Spain slides left past Guatemala, and the cloud collapses onto a line.",
      async run(ctx) {
        ctx.dim(1);
        ctx.land(true);
        const c = ctx.card("same days. same countries. new ruler.");
        const read = ctx.el("div", "anim-readout",
          "<span>ruler: <b data-r>kilometres</b></span>" +
          "<span style=\"color:var(--_amber)\">R&sup2; <b data-q>0.19</b></span>");
        c.appendChild(read);
        const outR = read.querySelector("[data-r]");
        const outQ = read.querySelector("[data-q]");
        ctx.watch((i) => {
          outR.textContent = ruler(i);
          outQ.textContent = R2B[i].toFixed(2);
        });

        ctx.spot(SPAIN, true);
        ctx.spot(GUATEMALA, true);
        await ctx.sleep(1000);

        if (ctx.fast()) {
          ctx.setX(DET - 1, true);
        } else {
          for (let i = 1; i < DET; i++) { ctx.setX(i); await ctx.sleep(95); }
          await ctx.sleep(700);
        }
        ctx.fitLine(true);
        await ctx.sleep(1000);

        [["R²", "0.19 → 0.97"],
         ["new data collected", "none"]].forEach((row, i) => {
          const t = ctx.el("div", "anim-tally anim-fade",
            "<span>" + row[0] + "</span><b>" + row[1] + "</b>");
          t.style.animationDelay = ctx.fast() ? "0s" : (i * 0.5) + "s";
          c.appendChild(t);
        });
        await ctx.sleep(1200);
        c.appendChild(ctx.el("div", "anim-quote anim-fade",
          "it was spreading in circles all along — on the other map"));
        await ctx.sleep(2800);
      }
    },
    {
      label: "Now you turn the ruler",
      note: "Your hand on it now. Slide from kilometres to effective distance and back: the cloud gathers and scatters, and the fit climbs from 0.19 to 0.97. Nothing about the countries changes — only where you agree to stand.",
      async run(ctx) {
        ctx.dim(1);
        ctx.land(true);
        ctx.fitLine(true);
        const c = ctx.card("now you turn it");

        const track = ctx.el("div", "anim-track");
        const knob = ctx.el("div", "anim-knob");
        track.appendChild(knob);
        c.appendChild(track);

        const read = ctx.el("div", "anim-readout",
          "<span>ruler: <b data-r>kilometres</b></span>" +
          "<span style=\"color:var(--_amber)\">R&sup2; <b data-q>0.19</b></span>");
        c.appendChild(read);
        const outR = read.querySelector("[data-r]");
        const outQ = read.querySelector("[data-q]");
        c.appendChild(ctx.el("div", "anim-caption",
          "drag it: at 0% the axis is kilometres from Mexico City, at 100% it is effective distance"));

        const verdict = ctx.el("div", "anim-tally anim-fade");
        verdict.style.visibility = "hidden";
        c.appendChild(verdict);
        const say = (t) => { verdict.innerHTML = t; verdict.style.visibility = "visible"; };

        /* One knob, and a real one: pointer, touch and arrow keys all land in
           onInput, and grabbing it pauses the sequence, so the plot is yours
           until you let go. */
        const dial = ctx.mountKnob(knob, {
          min: 0, max: DET - 1, step: 1, value: 0,
          label: "Blend the axis from geographic to effective distance",
          format: (i) => pct(i) + " per cent effective distance",
          onGrab: () => ctx.pause(),
          onInput: (i) => {
            outR.textContent = ruler(i);
            outQ.textContent = R2B[i].toFixed(2);
            ctx.setX(i);
          }
        });

        /* Skipping, or reading with motion off: land on the answer, because
           the answer is what this figure is about. */
        if (ctx.fast()) {
          ctx.setX(DET - 1, true);
          dial.set(DET - 1);
          say("<span>same dots, same days.</span><b>R&sup2; 0.19 → 0.97</b>");
          return;
        }

        dial.set(0);
        await ctx.sleep(1000);
        for (let i = 1; i < DET; i++) { dial.set(i); await ctx.sleep(105); }
        say("<span>gathered.</span><b>R&sup2; 0.97</b>");
        await ctx.sleep(1900);

        for (let i = DET - 2; i >= 0; i--) { dial.set(i); await ctx.sleep(70); }
        say("<span>scattered again.</span><b>R&sup2; 0.19</b>");
        await ctx.sleep(1500);

        for (let i = 1; i < DET; i++) { dial.set(i); await ctx.sleep(80); }
        say("<span>same dots, same days.</span><b>only the ruler moved</b>");
        await ctx.sleep(2600);
      }
    }
  ];

  mountScenes(document.getElementById("h1n1-ruler"), scenes, {
    stepsLabel: "Ruler steps",

    /* The one thing only this animation has: a scatter that survives all four
       steps, whose dots never change their arrival day and only ever slide
       sideways. Built once per run by step 1, handed to every scene on ctx. */
    helpers(ctx) {
      const plot = ctx.$("[data-h1-plot]");
      const side = ctx.$("[data-h1-side]");
      const S = { hook: null };

      function drawPlot() {
        plot.textContent = "";
        const svg = ctx.svgRoot("0 0 470 264", "h1-plot");
        const put = (tag, attrs, cls, txt) => {
          const n = ctx.svgEl(tag, attrs);
          if (cls) n.setAttribute("class", cls);
          if (txt != null) n.textContent = txt;
          return svg.appendChild(n);
        };

        put("line", { x1: 58, y1: 214, x2: 446, y2: 214 }, "anim-axis");
        put("line", { x1: 58, y1: 214, x2: 58, y2: 30 }, "anim-axis");
        DAY_TICK.forEach((t) => {
          put("line", { x1: 53, y1: t[0], x2: 58, y2: t[0] }, "anim-axis");
          put("text", { x: 49, y: t[0] + 4, "text-anchor": "end" }, "anim-label", t[1]);
        });
        put("text", { x: 16, y: 122, "text-anchor": "middle",
          transform: "rotate(-90 16 122)" }, "anim-label", "arrival day");
        GEO_TICK.forEach((t) => {
          put("line", { x1: t[0], y1: 214, x2: t[0], y2: 219 }, "anim-axis");
        });

        /* Both tick rows share one baseline and cross-fade in place, so the
           axis relabels itself instead of sliding a second row in. */
        const row = (ticks) => {
          const g = ctx.svgEl("g");
          ticks.forEach((t) => {
            const n = ctx.svgEl("text",
              { x: t[0], y: 232, "text-anchor": "middle", "class": "anim-label" });
            n.textContent = t[1];
            g.appendChild(n);
          });
          return svg.appendChild(g);
        };
        S.tGeo = row(GEO_TICK);
        S.tEff = row(EFF_TICK);
        S.title = put("text", { x: 252, y: 252, "text-anchor": "middle" },
          "anim-label", "distance from Mexico City (1000 km)");

        S.fit = put("line", { x1: SEG[0][0], y1: SEG[0][1], x2: SEG[0][2], y2: SEG[0][3] },
          "anim-amber-stroke");
        S.fit.style.opacity = 0;
        S.mark = put("line", { x1: KM9, y1: 30, x2: KM9, y2: 219 }, "anim-marker");
        S.mark.style.opacity = 0;

        /* Two layers, so the four named dots always sit over the cloud. */
        const gCloud = svg.appendChild(ctx.svgEl("g"));
        const gNamed = svg.appendChild(ctx.svgEl("g"));
        const named = {};
        NAMED.forEach((n) => { named[n[0]] = n; });

        const slow = !ctx.fast();
        S.pts = [];
        S.circ = [];
        S.named = [];
        GEOX.forEach((x, k) => {
          const n = named[k];
          const g = ctx.svgEl("g", { "class": "h1-pt" + (slow ? " anim-fade" : "") });
          if (slow) g.style.animationDelay = (0.25 + k * 0.055) + "s";
          const c = ctx.svgEl("circle", {
            cx: x, cy: DAYY[k], r: n ? 5.6 : 4.4,
            "class": n ? "anim-accent-fill h1-named" : "anim-faint"
          });
          if (!n) c.style.opacity = 0.72;
          g.appendChild(c);
          if (n) {
            const t = ctx.svgEl("text", {
              x: x + n[2], y: DAYY[k] + n[3], "text-anchor": n[4],
              "class": "anim-label anim-knockout"
            });
            t.textContent = n[1];
            g.appendChild(t);
          }
          (n ? gNamed : gCloud).appendChild(g);
          S.pts.push(g);
          S.circ.push(c);
          S.named.push(!!n);
        });

        S.svg = svg;
        plot.appendChild(svg);
        plot.appendChild(ctx.el("div", "anim-caption",
          "28 countries, redrawn schematically after Brockmann &amp; Helbing (2013). " +
          "The R&sup2; on screen is measured on these redrawn points, and matches " +
          "the 0.973 they publish."));
        setX(0, true);
      }

      /* Detent i of the blend. Pure lookup: a dot is where the two rulers put
         it, weighted i/20, and the fitted line is an array entry. */
      function setX(i, instant) {
        if (instant) S.pts.forEach((g) => { g.style.transition = "none"; });
        const t = i / (DET - 1);
        S.pts.forEach((g, k) => {
          g.style.transform =
            "translate(" + ((EFFX[k] - GEOX[k]) * t).toFixed(2) + "px,0px)";
        });
        if (instant) {
          S.svg.getBoundingClientRect();            /* commit before re-arming */
          S.pts.forEach((g) => { g.style.transition = ""; });
        }
        S.tGeo.style.opacity = Math.pow(1 - t, 1.5).toFixed(3);
        S.tEff.style.opacity = Math.pow(t, 1.5).toFixed(3);
        S.title.textContent = i === 0 ? "distance from Mexico City (1000 km)"
          : i === DET - 1 ? "effective distance from Mexico City"
          : "ruler: " + pct(i) + "% effective distance, " + (100 - pct(i)) + "% kilometres";
        const s = SEG[i];
        ctx.attr(S.fit, { x1: s[0], y1: s[1], x2: s[2], y2: s[3] });
        if (S.hook) S.hook(i);
      }

      function fitLine(on) {
        if (on && !ctx.fast() && S.fit.style.opacity !== "1") {
          S.fit.style.setProperty("--dash", 460);
          S.fit.classList.remove("anim-draw");
          S.fit.getBoundingClientRect();
          S.fit.classList.add("anim-draw");
        }
        S.fit.style.opacity = on ? 1 : 0;
      }

      /* The cloud arrives grey and lawless; once the ruler is the network's,
         it is the same ink as everything else in the notes. */
      function land(on) {
        S.circ.forEach((c, k) => {
          if (S.named[k]) return;
          c.setAttribute("class", on ? "anim-accent-fill" : "anim-faint");
        });
      }

      function spot(k, on) {
        S.circ[k].setAttribute("class", on ? "h1-hi" : "anim-accent-fill h1-named");
      }

      function card(title) {
        side.textContent = "";
        const c = ctx.el("div", "anim-panel anim-pop");
        if (title) c.appendChild(ctx.el("div", "anim-caption", title));
        side.appendChild(c);
        return c;
      }

      const mark = (on) => { S.mark.style.opacity = on ? 1 : 0; };
      const dim = (v) => { S.svg.style.opacity = v; };
      const watch = (fn) => { S.hook = fn; };

      /* S is filled by drawPlot(), i.e. after helpers() has already run, so
         everything that reaches into it has to be a function — the kit copies
         these onto ctx by value at mount time. */
      return { drawPlot, setX, fitLine, land, spot, mark, dim, watch, card };
    },

    clear(ctx) { ctx.watch(null); }
  });
});
