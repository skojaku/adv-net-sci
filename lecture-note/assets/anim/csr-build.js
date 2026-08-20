/* ==========================================================================
   csr-build.js — CSR, built out of the adjacency list.

   A scene array for the shared kit (assets/anim.css + assets/anim.js); it
   carries no sequencer and no copy of the kit's stylesheet. See the header of
   assets/anim.js for the contract, and the markup this expects.

   Loaded by lecture-note/m01-euler_tour/04-appendix.qmd and
   slides/m01/m01-euler-tour.md. Both used to carry a widget that showed the
   finished arrays beside the matrix and asked for them to be taken on trust.
   CSR is not a fact about matrices, it is what you get when you lay an
   adjacency list end to end: the neighbours survive as `indices`, and the only
   thing lost — where each row stopped — is what `indptr` writes down. So the
   stage does that, in that order, with one colour per row so a block in the
   strip can be traced back to the row it came from.

   The stage's own layout CSS stays with each page: the note has a column to
   fill and the slide has a 1280x720 frame, so the sizes differ even though
   every class here is shared.
   ========================================================================== */

(window.animReady = window.animReady || []).push(function () {

  /* ---------------------------------------------------------------- data ---
     make_figures.py's graph5 — the same five nodes behind store-matrix.png,
     the walk-counting stage and "One graph, three structures". indices and
     indptr are derived from the list rather than written out, so the three
     can never disagree.
     ------------------------------------------------------------------------ */
  const ADJ = [[1, 2], [0, 2, 3], [0, 1, 4], [1, 4], [2, 3]];
  const N = ADJ.length;

  const INDPTR = [0];
  ADJ.forEach(function (row) { INDPTR.push(INDPTR[INDPTR.length - 1] + row.length); });

  /* Each entry remembers which row it came from, which is the whole colour
     scheme and also what makes the cut points obvious. */
  const INDICES = [];
  ADJ.forEach(function (row, i) {
    row.forEach(function (j) { INDICES.push({ v: j, row: i }); });
  });

  /* --------------------------------------------------------------- scenes */
  const scenes = [
    {
      label: "Start from the adjacency list",
      note: "Five nodes, each with its neighbours. Twelve numbers in all — every edge filed twice, once at each end.",
      async run(ctx) {
        ctx.list();
        await ctx.sleep(2600);
      }
    },
    {
      label: "Lay the rows end to end",
      note: "Glue the rows into one line and the neighbours all survive. That line is indices — every node's neighbours, in node order, with nothing in between.",
      async run(ctx) {
        ctx.list();
        ctx.arrays(["indices"]);
        await ctx.fillIndices({ pause: 620 });
        await ctx.sleep(2200);
      }
    },
    {
      label: "Write down where each row started",
      note: "Gluing lost one thing: where a row stopped. So keep the cut points — indptr, one per node plus the total. data holds a value per entry: all 1s here, weights if the edges carry them.",
      async run(ctx) {
        ctx.list();
        ctx.arrays(["indices", "indptr", "data"]);
        await ctx.fillIndices({ pause: 0 });
        await ctx.fillIndptr({ pause: 560 });
        await ctx.sleep(2400);
      }
    },
    {
      label: "Read a row back",
      note: "Now cover the list. Degree is indptr[i+1] − indptr[i], a subtraction. The neighbours are indices[indptr[i] : indptr[i+1]], a slice that is already contiguous.",
      async run(ctx) {
        ctx.list();
        ctx.arrays(["indices", "indptr", "data"]);
        await ctx.fillIndices({ pause: 0 });
        await ctx.fillIndptr({ pause: 0 });
        ctx.reader();
        if (ctx.fast()) return;
        await ctx.sleep(14000);
      }
    }
  ];

  mountScenes(document.getElementById("csr-build"), scenes, {
    stepsLabel: "CSR steps",

    helpers(ctx) {
      const leftBox = ctx.$("[data-cb-left]");
      const rightBox = ctx.$("[data-cb-right]");
      const S = { rows: [], cells: {}, ptr: [] };

      function beat(pause) {
        if (!pause || ctx.fast()) return Promise.resolve();
        return ctx.sleep(pause);
      }

      /* ------------------------------------------------------- the list --- */
      function list() {
        leftBox.textContent = "";
        const wrap = ctx.el("div", "cb-list");
        wrap.appendChild(ctx.el("div", "cb-h", "adjacency list"));
        S.rows = ADJ.map(function (row, i) {
          const r = ctx.el("div", "cb-row");
          r.appendChild(ctx.el("b", null, String(i)));
          row.forEach(function (j) {
            r.appendChild(ctx.el("i", "cb-cell cb-r" + i, String(j)));
          });
          wrap.appendChild(r);
          return r;
        });
        leftBox.appendChild(wrap);
      }

      /* ----------------------------------------------------- the arrays --- */
      function arrays(kinds) {
        rightBox.textContent = "";
        S.cells = {};
        const wrap = ctx.el("div", "cb-arrays");
        kinds.forEach(function (k) {
          const r = ctx.el("div", "cb-arow");
          r.appendChild(ctx.el("b", null, k));
          const strip = ctx.el("div", "cb-strip");
          r.appendChild(strip);
          wrap.appendChild(r);
          S.cells[k] = strip;
        });
        rightBox.appendChild(wrap);
      }

      async function fillIndices(o) {
        o = o || {};
        const strip = S.cells.indices;
        if (!strip) return;
        strip.textContent = "";
        S.idx = [];
        /* Row by row, not entry by entry: the block is the unit that moves. */
        for (let i = 0; i < N; i++) {
          for (let k = INDPTR[i]; k < INDPTR[i + 1]; k++) {
            const c = ctx.el("i", "cb-cell cb-r" + INDICES[k].row, String(INDICES[k].v));
            strip.appendChild(c);
            S.idx.push(c);
          }
          if (S.rows[i]) S.rows[i].classList.add("cb-done");
          await beat(o.pause);
        }
        S.rows.forEach(function (r) { r.classList.remove("cb-done"); });
      }

      async function fillIndptr(o) {
        o = o || {};
        const strip = S.cells.indptr;
        if (!strip) return;
        strip.textContent = "";
        S.ptr = [];
        for (let i = 0; i < INDPTR.length; i++) {
          /* The last entry is the length of indices, not the start of a row,
             so it does not get a row's colour. */
          const cls = "cb-cell" + (i < N ? " cb-r" + i : " cb-total");
          const c = ctx.el("i", cls, String(INDPTR[i]));
          strip.appendChild(c);
          S.ptr.push(c);
          /* Mark the entry the cut point refers to, so indptr reads as an
             index into the strip rather than as five more numbers. */
          if (i < N && S.idx && S.idx[INDPTR[i]]) S.idx[INDPTR[i]].classList.add("cb-cut");
          await beat(o.pause);
        }

        const dat = S.cells.data;
        if (dat) {
          dat.textContent = "";
          INDICES.forEach(function () { dat.appendChild(ctx.el("i", "cb-cell cb-one", "1")); });
        }
      }

      /* ------------------------------------------------- the last beat --- */
      function reader() {
        const wrap = rightBox.querySelector(".cb-arrays");
        if (!wrap) return;

        const range = ctx.el("div", "anim-range");
        const track = ctx.el("div", "anim-track");
        const knobEl = ctx.el("div", "anim-knob");
        track.appendChild(knobEl);
        range.appendChild(track);
        wrap.appendChild(range);

        const out = ctx.el("div", "cb-read");
        wrap.appendChild(out);

        function draw(r) {
          S.rows.forEach(function (row, i) { row.classList.toggle("cb-on", i === r); });
          if (S.idx) {
            S.idx.forEach(function (c, k) {
              c.classList.toggle("cb-slice", k >= INDPTR[r] && k < INDPTR[r + 1]);
            });
          }
          S.ptr.forEach(function (c, i) {
            c.classList.toggle("cb-bound", i === r || i === r + 1);
          });
          out.innerHTML = "node " + r + " — indptr " + INDPTR[r] + " → " + INDPTR[r + 1] +
            ", so degree " + (INDPTR[r + 1] - INDPTR[r]) +
            " and neighbours " + ADJ[r].join(", ") + ".";
        }

        ctx.mountKnob(knobEl, {
          min: 0, max: N - 1, step: 1, value: 1,
          label: "which node's row",
          format: function (v) { return "node " + v; },
          onInput: draw
        }).set(1);
      }

      return {
        list: list,
        arrays: arrays,
        fillIndices: fillIndices,
        fillIndptr: fillIndptr,
        reader: reader
      };
    }
  });
});
