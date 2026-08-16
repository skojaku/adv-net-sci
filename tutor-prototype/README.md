# Pair Notebook — the AI-guided assignment

A **Pair Notebook** is one module's worth of network science taught as a
one-on-one tutoring session: the student talks to an AI tutor in the terminal,
and a
[marimo](https://marimo.io) notebook fills up beside them with figures,
widgets, photographs of their pen-and-paper work, and notes quoting their own
answers.
The notebook they end up with is both their illustrated lecture note and the
graded artifact — **what is reviewed is their thinking, not their code.**

This directory is where they are authored. Two of its folders are published to
GitHub, where students get them from:

| here | published to | what it is |
|---|---|---|
| `pi-pair-notebook/` | [`sk-classroom/pi-pair-notebook`](https://github.com/sk-classroom/pi-pair-notebook) (public) | the pi package: the `nb_*` toolkit, chapter orchestration, checkpoint ceremony, verbatim logging, referee. Shared by every module |
| `m02-small-world/` | [`sk-classroom/advnetsci-pair-notebook-m02-small-world`](https://github.com/sk-classroom/advnetsci-pair-notebook-m02-small-world) (public) | one module: curriculum, premade cells, assets, launcher |
| `review/` | — | the E2E harness that drives a live session against scripted student personas |
| `TUTOR_REVIEW_RUBRIC.md` | — | what a review checks (Parts S, C, P, D) |

**Edit here, publish from here.** The GitHub copies are exports, not forks —
committing to them directly means the next publish overwrites it.

Two files stay behind: `notebook.golden.py` (a *finished* session — an answer
key in the repo the student clones) and `review_golden_sync.py`, which checks
it. Nothing reads either at runtime, so the export drops them.

```bash
git commit -am "..."                 # publishing exports HEAD, not the working tree
tools/publish_pair_notebook.sh package   # -> sk-classroom/pi-pair-notebook
tools/publish_pair_notebook.sh module    # -> the m02 module repo
tools/publish_pair_notebook.sh all
```

The module pins the toolkit **by tag** in `.pi/settings.json`
(`git:github.com/sk-classroom/pi-pair-notebook@v0.2.0`) — a module and its
toolkit are reviewed together, so nothing a student runs floats on `main`.
Releasing a
toolkit change is therefore three steps: publish the package, tag it, bump the
tag in every module that should take it.

## Reviewing a module

```bash
python3 m02-small-world/review_golden_sync.py      # golden notebook still in step?
# then the rubric: Parts S, C, P statically, Part D live
STATE=$(review/e2e_setup.sh ../m02-small-world)
```

Part D runs against the **working tree** of `pi-pair-notebook/`, so a toolkit
fix is exercised before it is ever tagged. See `review/README.md`.

## Where the rest lives

Grading, distribution and the per-student model keys are not in here:

- **Distribution and submission** — Classroom 50, one repo per student
  (`COURSE_SYSTEM.md` §4).
- **Models and quotas** — the course LLM gateway (`llm-gateway/`), which
  publishes exactly three aliases: `tutor`, `vision`, `referee`.
