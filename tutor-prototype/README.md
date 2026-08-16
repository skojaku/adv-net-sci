# Studio — the AI-guided notebook assignment

A **Studio** is one module's worth of network science taught as a one-on-one
tutoring session: the student talks to an AI tutor in the terminal, and a
[marimo](https://marimo.io) notebook fills up beside it with figures, widgets,
photographs of their pen-and-paper work, and notes quoting their own answers.
The notebook they end up with is both their illustrated lecture note and the
graded artifact — **what is reviewed is their thinking, not their code.**

This directory is where Studios are authored. Two of its folders are published
to GitHub, where students get them from:

| here | published to | what it is |
|---|---|---|
| `pi-studio/` | [`sk-classroom/pi-studio`](https://github.com/sk-classroom/pi-studio) (public) | the pi package: the `nb_*` toolkit, chapter orchestration, checkpoint ceremony, verbatim logging, referee. Shared by every module |
| `m02-small-world/` | [`sk-classroom/advnetsci-studio-m02-small-world`](https://github.com/sk-classroom/advnetsci-studio-m02-small-world) (public) | one module: curriculum, premade cells, assets, launcher |
| `review/` | — | the E2E harness that drives a live session against scripted student personas |
| `TUTOR_REVIEW_RUBRIC.md` | — | what a review checks (Parts S, C, P, D) |

**Edit here, publish from here.** The GitHub copies are exports, not forks —
committing to them directly means the next publish overwrites it.

```bash
git commit -am "..."                 # publishing exports HEAD, not the working tree
tools/publish_studio.sh package      # -> sk-classroom/pi-studio
tools/publish_studio.sh module       # -> sk-classroom/advnetsci-studio-m02-small-world
tools/publish_studio.sh all
```

The module pins the toolkit **by tag** in `.pi/settings.json`
(`git:github.com/sk-classroom/pi-studio@v0.1.1`) — a module and its toolkit are
reviewed together, so nothing a student runs floats on `main`. Releasing a
toolkit change is therefore three steps: publish the package, tag it, bump the
tag in every module that should take it.

## Reviewing a module

```bash
python3 m02-small-world/review_golden_sync.py      # golden notebook still in step?
# then the rubric: Parts S, C, P statically, Part D live
STATE=$(review/e2e_setup.sh ../m02-small-world)
```

Part D runs against the **working tree** of `pi-studio/`, so a toolkit fix is
exercised before it is ever tagged. See `review/README.md`.

## Where the rest lives

Grading, distribution and the per-student model keys are not in here:

- **Distribution and submission** — Classroom 50, one repo per student
  (`COURSE_SYSTEM.md` §4).
- **Models and quotas** — the course LLM gateway (`llm-gateway/`), which
  publishes exactly three aliases: `tutor`, `vision`, `referee`.
