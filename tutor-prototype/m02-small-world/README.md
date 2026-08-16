# Studio 02 — The Small-World Puzzle

**This is an assignment.** Instead of submitting code, you work through a
**one-on-one tutoring session**: an AI tutor builds a [marimo](https://marimo.io)
notebook with you, cell by cell — asking you to predict, explain, calculate, and
draw on paper — and keeps a log of the conversation. At the end you have a
notebook that is both your own illustrated lecture note and the thing that gets
graded.

**What is reviewed is your thinking, not your code.** No programming experience
is required. A session takes about 60–90 minutes, and you can stop and pick up
later.

---

## For students

### One-time setup (10 minutes)

**1. Install `uv`** — it runs the notebook.

- macOS: `brew install uv`
- otherwise: <https://docs.astral.sh/uv/getting-started/installation/>

**2. Install `pi`** — the agent your tutor runs on. It needs
[Node.js](https://nodejs.org) 24 or newer.

```bash
npm install -g @earendil-works/pi-coding-agent
pi --version
```

**3. Add the course model.** Your instructor issues you a key
(`sk-nsci-…`) and a base URL. Create `~/.pi/agent/models.json` — or merge the
`netsci` block into the one you already have — and paste both in:

```jsonc
{
  "providers": {
    "netsci": {
      "baseUrl": "https://PASTE-THE-COURSE-URL/v1",
      "api": "openai-completions",
      "apiKey": "PASTE-YOUR-COURSE-KEY",
      "compat": { "supportsDeveloperRole": false },
      "models": [
        { "id": "tutor",   "name": "Course Tutor",   "reasoning": true,
          "input": ["text"], "contextWindow": 131072, "maxTokens": 32768,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 } },
        { "id": "vision",  "name": "Course Vision",
          "input": ["text", "image"], "contextWindow": 1048576, "maxTokens": 8192,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 } },
        { "id": "referee", "name": "Course Referee", "reasoning": true,
          "input": ["text"], "contextWindow": 131072, "maxTokens": 8192,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 } }
      ]
    }
  }
}
```

Your key has a per-week allowance; `GET /v1/usage` on the same base URL tells
you what is left of it.

**4. Nothing else.** The tutor's own toolkit —
[`pi-studio`](https://github.com/sk-classroom/pi-studio) and its dialog
companion — is listed in `.pi/settings.json`, and `pi` fetches it the first time
you run. That first start takes a few seconds longer than the rest.

### Every session

```bash
./run_tutor.sh
```

Two windows appear:

| Window | What it is |
|---|---|
| **Terminal** (tutor) | Where you and your tutor talk — questions and answers happen here. |
| **Browser** (notebook) | The whiteboard: pictures, interactive experiments, and photo uploads appear here when needed. A drop box or a code box has a **📨 Send to my tutor** button under it — press it and your tutor sees your work. Anything else you explore, just tell your tutor about in the terminal. |

Say hello in the terminal and follow along. Have **pen and paper** ready: three
steps happen off-screen — a distance table, a drawing, and a derivation — and
you photograph each with your phone and drop it into the notebook.

If you and your tutor ever get properly stuck — you think an answer should
count, you want a fresh try, or you'd rather just move on — scroll to the
**⚖️ Stuck with your tutor?** box, always the last thing on the notebook page,
say so, and press the button. A second, stronger model reviews the whole
situation and makes a call your tutor has to follow. Using it is never held
against you.

### What gets turned in

The session produces everything automatically — you don't "write up" anything:

- `notebook.py` — the notebook you built together
- `session_artifacts/session_log.jsonl` — your answers, verbatim
- `session_artifacts/session_summary.md` — a summary for the instructor

**You submit by pushing them to your own GitHub repository** — the one the
course assignment link creates for you. Clone that repo, run the studio inside
it, and when you are done:

```bash
git add -A && git commit -m "Studio 02" && git push
```

The commit history is part of the picture: it shows when the work happened, and
a session finished in three sittings is exactly as good as one finished in one.

**Honesty note:** needing hints is *not* penalized. The log is reviewed for how
you reasoned, not for how few hints you used. Asking questions and taking
detours counts in your favor — it's the whole point.

---

## For the instructor / TA

### What's in this folder

| File | Role |
|---|---|
| `lesson/` | The curriculum, split into 5 chapters (`index.json` + `chN-*.yaml`): 12 checkpoints + 1 optional stretch, each with build spec, question, accept criteria, and starter hints. **The tutor holds only the current chapter in context** — the toolkit (the deterministic "lead agent") injects one CHAPTER SCRIPT at a time, and at each `chapter_done` builds a handoff brief (progress + verbatim quotes + the tutor's own notes), loads the next script, and trims the old conversation via pi compaction with the brief as the summary. Same session, same visible transcript, fresh LLM context per chapter (`.pi/settings.json` keeps only ~3k recent tokens on compaction). **Edit these files to change the lesson.** |
| `AGENTS.md` | The tutor's behavior contract (auto-loaded by pi). Pedagogy, logging schema, hard rules. Lesson-independent. |
| `cells/` | Premade, tested cell bodies the tutor inserts with `nb_add_template`. Each carries a `# describe:` line — one factual sentence about what the student sees. |
| `notebook.template.py` | Pristine starter: visually blank (only hidden import/helper cells). `notebook.py` is the working copy (gitignored until the student commits it), created from the template on first run. |
| `reset_session.sh` | Continue-or-fresh, decided **before anything loads**. `run_tutor.sh` asks at startup when a session exists; answering `f` runs this. It archives the notebook, the log, the summary and any uploads into `session_artifacts/` with a timestamp and drops in a clean notebook — nothing is ever deleted. Run it directly, or `./run_tutor.sh --fresh`, to skip the prompt. A file-level reset cannot half-succeed, which the in-session one can: `nb_fresh_start` deletes cells one at a time through a live kernel, and one failure there left a "clean slate" session opening on chapter 3. `nb_fresh_start` remains for a student who changes their mind mid-lesson. |
| `run_tutor.sh` | Launcher: asks continue-or-fresh, starts marimo (`--no-token`), starts pi (bash disabled). `--fresh` resets without asking. Model aliases (`netsci/tutor`, `netsci/vision`, `netsci/referee`) are overridable with `TUTOR_MODEL`, `TUTOR_VISION_MODEL`, `TUTOR_REFEREE_MODEL`. |
| `.pi/settings.json` | Thinking level, compaction budget, and the two packages pi installs on startup: the toolkit and the dialog extension. **Pinned by tag** — a module and its toolkit are tested together. |
| `notebook.golden.py` + `review_golden_sync.py` | A finished-notebook reference and the check that keeps its wording in step with `cells/` and the toolkit's emitted prose. |

The `nb_*` toolkit itself — tools, chapter orchestration, the checkpoint
ceremony, the verbatim capture, the referee, the improvised-cell review — lives
in [`sk-classroom/pi-studio`](https://github.com/sk-classroom/pi-studio) and is
shared by every module. Its README documents the module contract this folder
implements.

### Design decisions

- **The lesson script lives agent-side, not in the notebook.** An earlier idea
  was to pre-write all cells commented-out — but then any text editor reveals
  the answers. Here the notebook starts blank and `lesson/` is the source of
  truth. (For a graded deployment, serve the chapter scripts from the API proxy
  instead of shipping them in the repo.)
- **Channel discipline:** words live in the terminal (stories, questions,
  typed answers); the notebook is reserved for what the terminal can't do —
  figures, *interactive/animated* widgets (preferred over static images),
  photo uploads. A drop box or a code box carries a 📨 Send button whose press
  starts the tutor's turn; a slider or a radio has none — the student says so
  in the terminal and the tutor reads the values (an earlier Done button on
  every cell competed with the terminal for keyboard focus).
- **Interaction modalities on purpose:** prediction (cp1, cp6), calculation
  (cp2, cp3), three off-screen pen-and-paper steps with photo upload
  (cp2_paperwork, cp4, cp5_ring_formula), a real coded experiment at large N
  (cp6_large_n_experiment), concept articulation (cp3, cp5_tension, cp8),
  exploration with a widget (cp2, cp5, cp6), and a red-team critique of a
  flawed AI analysis (cp7) — the last one previews the course's
  process-over-product grading philosophy.
- **Templates are self-describing (notebook design principle).** Every
  template in `cells/` carries a `# describe:` line — one factual sentence
  about what the student sees. `nb_add_template` returns it on insert, and
  the tutor is told to describe the artifact *only* from that line (a tutor
  once called the 4-person network "5-person"). When authoring a new
  template, write the describe line first; keep titles/captions in the
  figures self-explanatory so the notebook stays truthful without the tutor.
- **Hints are logged, never penalized** — stated to the student up front, and
  binding on the grader. Otherwise students stop asking, and the log stops
  reflecting reality.
- **Grading artifact = the notebook itself** (plus the verbatim
  `session_log.jsonl` as the machine copy). Note cells quote the student's
  answers word for word, and a closing `session_record` cell summarizes every
  checkpoint. The tutor is required to record answers verbatim and never fake
  a pass.

The full set of notebook design principles — structure, note-cell rhythm,
naming conventions, theming — is in **[DESIGN.md](DESIGN.md)**.

### Adapting to another module

Copy this folder, rewrite the chapter scripts in `lesson/` (the checkpoint
schema is documented in each file's header comment) and `lesson/index.json`,
swap the premade cells in `cells/`, and update `notebook.template.py`'s
dependencies if needed. `AGENTS.md`, `DESIGN.md`, `run_tutor.sh` and
`.pi/settings.json` carry over unchanged.

### Known limitations

- The chapter scripts ship in the folder, so a determined student can read the
  accept criteria. Fine for formative use; move them server-side for grading.
- Per-student cost control lives in the course LLM gateway, not here.
- The marimo server runs with `--no-token` on localhost — fine on a laptop,
  not on a shared host.
