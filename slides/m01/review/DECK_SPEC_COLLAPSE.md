# m01 collapse spec — the deck after the sheet and the lab

## Why

The deck was built as the only place m01 was taught. It no longer is. Students
now do `lecture-note/m01-euler_tour/pen-and-paper/exercise.pdf` **before** the
lecture and the molab lab (`.../pen-and-paper/lab.py`) on their own, and
`01b-vocabulary.qmd` + `04-appendix.qmd` carry the written treatment — including
the two widgets this deck also mounts (route-namer, walk-power).

The budget decides the rest. **90-minute class: 50 to the sheet and the lab, 10
buffer, 30 for the deck.** 83 slides in 30 minutes is 21s each, which is not a
pace a dialogue deck can be given at.

## The rule this collapse follows

**Delete whole slides. Never merge two concepts onto one.** P1 (one slide, one
point) is the rubric's only Blocker in play, and merging is the one edit that
breaks it. Where the sheet, the lab or the note already teaches something, the
deck stops teaching it rather than compressing it — the material has a home.

Two consequences, both intended:

- No new tables, no slide carrying five definitions. DECK_SPEC non-negotiables
  survive intact.
- Surviving duplicates change **mode**, not size: a slide that derived a result
  now confirms one the room already has in pencil. Same figure, same one point,
  same fragments — 90 seconds becomes 15.

## Cuts — 26 slides

Indices are into the `\n---\n` split of the deck as of `c47fae31`.

| # | slide | why it goes |
|---|---|---|
| 12 | Two bridges, one pair | lab §1: "wherever two places are joined twice, the pair goes in twice" |
| 13 | An edge to itself | returns as the Act-4 question at 75/76 |
| 16 | Edges come in pairs | Q2 is this argument, drawn by hand; 18 becomes the callback |
| 17 | What if the degree is odd? | prompt for something Q2 already made them do |
| 20 | Your turn: count Königsberg | Q3 is the count |
| 23 | What if you must return...? | prompt; the lab's rule table carries the 0-odd row |
| 32 | Your turn: trail that is not a path | Q4(b) is literally this instruction |
| 35 | Name your own route | the route-namer now lives in 01b-vocabulary.qmd |
| 36 | Your turn: one trail, both triangles | third vocabulary activity in nine slides |
| 38 | Can you get from any node to any other? | prompt; lab §5 hands them `is_connected` |
| 40 | Finding components: the sweep | 41 is the same thing, animated |
| 46 | What breaks when edges have direction? | prompt |
| 51 | What replaces "odd" once edges point? | prompt |
| 52 | Total degree is the wrong quantity | now argued in 04-appendix; 53 states the rule |
| 57 | Edge list | lab §1 is the whole exercise |
| 58 | Adjacency list | note §Three ways to write a network down |
| 60 | Degree, three ways — the edge list | note §Three ways |
| 61 | Degree, three ways — the adjacency list | note §Three ways |
| 62 | Degree, three ways — the matrix | lab §3 makes them write `degrees(A)` |
| 63 | For a multigraph, count the edges | lab §3: add, do not set |
| 67 | Where the count comes from | walk-power animation now in 01b-vocabulary.qmd |
| 71 | The payoff: degree | 04-appendix §Storing a matrix that does not fit |
| 72 | The payoff: memory | same |
| 73 | Which format when? | same |
| 77 | Is a single node with no edges connected? | thinnest of Act 4's three pairs |
| 78 | Yes — vacuously | same pair |

83 → **57 slides**, 30 minutes, ~31s each.

Not cut, and why, since each looks cuttable:

- **64/65 — $A^2$ by hand, then predict $A^3$.** DECK_BUILD_GUIDE names this as
  the interaction the lecturer asked to strengthen: "Two slides, not one."
- **26/27 — destroy two bridges, then the epilogue.** Story, Act 1's payoff,
  and nowhere else in the course.
- **42/43 — giant component.** m01.c16 is core and has no in-class home but this.
- **5, 25, 41, 50 — the animations.** Density comes from motion; and S5 wants a
  demo per milestone.

## Rewrites — duplicates that become callbacks

| slide | becomes |
|---|---|
| 18 One edge left over | **You drew this already — Q2**: the dashed pairs, the road with no partner |
| 21 The verdict | confirms the Q3 table rather than deriving it |
| 22 Eulerian path | + the trail note: Q4(c) found their own drive revisits a city |
| 29/30/31 Walk / Trail / Path | Q4(a) named these; the slide confirms and moves |
| 39 Components | the `is_connected` they were handed in lab §5, opened up |
| 53 The directed Euler condition | absorbs 52's point: balance, not parity |
| 59 Adjacency matrix | their Q5(a) grid, and the lab's mirror rule |
| 79 Every node even, yet no circuit | "you built this" — the lab's early-finisher challenge |

Part dividers gain one line naming the lecture-note page that carries the
section, so "where do I review this" has an answer that is not the deck.

## Gate

    python3 figures/make_figures.py
    python3 figures/make_animations.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files \
         --html --no-stdin --images png -o review/slide.png
    python3 check_render.py

`--html` on every invocation: five slides still carry live HTML (the CSR widget
plus `kb-tracer`, `euler-builder`, `comp-sweep`, `dir-reach`). The two animation
stages that went with the cut slides — `route-namer` and `walk-power` — are both
mounted by `01b-vocabulary.qmd`, so nothing was lost, only moved.

### Result, measured against the same gate on the pre-collapse deck

|  | before | after |
|---|---|---|
| slides | 83 | **57** |
| gate findings | 173 | **129** |
| em-dash rule | 102 | 80 |
| figure taller than the 380px cap | 32 | 26 |
| drawing too small to read | 5 | 2 |
| everything else | 34 | 21 |

The gate exits 1 in both runs — it was already failing, and the em-dash rule is
most of why: it fires on the deck's own voice ("two edges per visit — one pair,
one leftover") 80 times, which is not something this collapse should decide.
Every remaining finding outside that rule names a **figure file**, and figure
dimensions are a property of `make_figures.py`, not of which slides survive.

One regression appeared and was fixed: an extra bullet on the review slide ran
content to y=719 in a 720px frame.

### Notes for the next pass

- **The em-dash rule.** 80 hits. Either the deck's voice changes or the rule is
  narrowed to em-dashes actually adjacent to `$…$`, which is what its own
  message claims to be about. Worth deciding once, deck-wide.
- **`slides/gatelib` is a symlink into `~/.claude/skills/slide-build/gatelib`,
  and that directory has lost its `.py` sources** — only `__pycache__` is left,
  so `check_render.py` cannot import. The numbers above came from the `.pyc`
  loaded sourceless off `PYTHONPATH`. The skill needs restoring or the gate is
  gone the next time a Python version rolls over.
- **`curriculum.yml`'s fifteen m01 slide anchors** all still point at
  `review/m01-euler-tour.OLD.md` headings. They were stale before this collapse
  and the collapse moved the targets again; rebuild them against this deck.
