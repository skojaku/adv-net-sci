# pi-studio

A [pi](https://pi.dev) package that turns a coding agent into a **Socratic
tutor teaching one student inside a [marimo](https://marimo.io) notebook**.

The student talks to the tutor in the terminal; the notebook beside it is the
shared whiteboard, and it fills up as the lesson goes — figures, widgets, photos
of their pen-and-paper work, and notes quoting their own answers. What the
session produces is a notebook the student keeps and an instructor grades.

This is the machinery. The lesson is not in here: a **module folder** supplies
the curriculum, the premade cells and the tutor's behaviour contract, and this
package supplies the tools that operate on them. See
[`sk-classroom/advnetsci-studio-m02-small-world`](https://github.com/sk-classroom/advnetsci-studio-m02-small-world)
for a complete module.

## Install

```bash
pi install git:github.com/sk-classroom/pi-studio@v0.1.1
pi install npm:@juicesharp/rpiv-ask-user-question@2.4.0   # required companion
```

A module folder normally declares both in its `.pi/settings.json`, and pi
installs them itself on startup — students run nothing by hand:

```json
{
  "packages": [
    "git:github.com/sk-classroom/pi-studio@v0.1.1",
    "npm:@juicesharp/rpiv-ask-user-question@2.4.0"
  ]
}
```

Requirements: pi ≥ 0.84 (Node ≥ 24), `uv` (runs marimo), and `bash` + `curl`
for the bridge. The tutor model may be text-only; a vision model is used
separately for photographs.

## What it gives the agent

One toolkit, `nb_*`, instead of raw bash and marimo code-mode boilerplate. The
model sends only cell bodies; the extension generates the plumbing, keeps the
student's terminal quiet (one friendly status line per call), and enforces the
things a prompt cannot.

| tool | does |
|---|---|
| `nb_add_template` | insert a premade, tested cell from the module's `cells/`. Refuses a build for a checkpoint that comes after the open one |
| `nb_add_cell` | an improvised cell — detours, fresh examples. Reviewed before insertion (see below) |
| `nb_add_exercise` | instructions + a pre-filled code box + ▶ Run, with a 📨 send button once it has run |
| `nb_edit_cell` / `nb_delete_cell` | fix or remove cells the tutor added |
| `nb_read` | read widget values out of the live notebook |
| `nb_view_image` | look at a student's uploaded photo through a vision model |
| `nb_run` | scratchpad Python — checking the student's arithmetic, never announcing it |
| `checkpoint_done` | the whole closing ceremony: append the log row, render the note cell from the script's skeleton with the student's verbatim words, ask what's next |
| `log_detour` | record an off-script question and the souvenir cell that answered it |
| `chapter_done` | gate the chapter transition on the student's own answer, write the handoff brief, load the next chapter |
| `nb_fresh_start` | clear the notebook when the student chooses to start over |

Four behaviours are worth knowing about, because they are what make the
artifact trustworthy rather than plausible:

- **Chapter-at-a-time context.** The tutor never holds the whole curriculum.
  The extension injects one `CHAPTER SCRIPT` at a time and, at `chapter_done`,
  builds a handoff brief (progress, verbatim quotes, the tutor's own notes) and
  compacts the conversation with that brief as the summary. Same session, same
  visible transcript, fresh model context per chapter.
- **The student's words are copied, not retold.** Typed answers are captured
  from the transcript, and the note cell's «verbatim» slots are filled from that
  capture — anything the model sends for those slots is discarded. Pairing
  answers with slots by hand failed five different ways in five live runs.
- **`checkpoint_done` refuses.** No build for the checkpoint, no photo on a
  pen-and-paper checkpoint, an empty answer, a note that quotes words the
  student never typed, a chapter that is not finished. Every refusal names its
  own fix, and every one gives up after one or two tries and logs anyway — a
  guard that can strand a student is worse than the fault it catches.
- **Improvised cells are reviewed** (`extensions/nb_review.py`, Python AST, run
  in the kernel before insertion): marimo renders only a cell's last expression,
  so displays that would silently vanish get wrapped in one `mo.vstack`,
  unrescuable cells are refused with an instruction, and ASCII-art diagrams are
  flagged.

There is also a **referee**: the notebook carries a ⚖️ box the student can press
to appeal over the tutor's head. The whole situation — their case, the log, the
script, the recent conversation — goes to a stronger model, and its ruling comes
back as a binding `REFEREE VERDICT` message. Appeals are logged as
participation, never as defiance.

## What a module folder must provide

The extension resolves everything from the **current working directory** — pi
runs in the module folder:

```
lesson/index.json          chapters, in order, each with a title + opening
lesson/ch*.yaml            checkpoints: goal, build, ask, accept, hints,
                           reveal_after, fresh_variants, note skeleton
cells/<name>.py            premade cell bodies, each with a `# describe:` line
                           that nb_add_template reads back to the tutor
assets/                    images the scripts refer to; uploads land here too
notebook.template.py       pristine starter notebook (imports + helpers only)
notebook.py                the working copy — the graded artifact
session_artifacts/         log, summary, archives, the student's signal file
AGENTS.md                  the tutor's behaviour contract, auto-loaded by pi
.pi/settings.json          packages, thinking level, compaction
```

Both `lesson/*.yaml` files and `cells/*.py` carry their schema in a header
comment. The one rule that is not obvious: **`cells/*.py` must be
self-describing.** `nb_add_template` returns the `# describe:` line and the
tutor is told to describe the artifact *only* from it — a tutor once called a
4-person network "5-person" because it was guessing.

## Environment

| variable | what |
|---|---|
| `MARIMO_URL` | the running marimo server. Set by the module's `run_tutor.sh`; defaults to `http://127.0.0.1:2718` |
| `TUTOR_VISION_MODEL` | `provider/model-id` for reading photographs. Unset → an image-capable model on the tutor's own provider, then any zero-cost one; none found → the tutor asks the student to describe the drawing in words, which is a valid pass |
| `TUTOR_REFEREE_MODEL` | `provider/model-id` for the ⚖️ appeal. Unreachable → the tutor resolves the appeal itself, generously |

## Local development

```bash
pi -e /path/to/pi-studio/extensions/notebook-tool.ts   # load the working tree
```

`-e` also works under `--no-extensions`, which is how the review harness pins a
run to exactly one copy of the toolkit. To iterate against a checkout instead of
a tag, point `.pi/settings.json` at the directory: a local path package
(`"../pi-studio"`, relative to the settings file) is loaded in place, without
copying.

Releases are pinned by tag. Bump `version` in `package.json`, tag `vX.Y.Z`, and
update the module folders that reference it — a module and its toolkit are
tested together, so nothing here floats on `main`.

## Credits

`bridge/scripts/` is [marimo-pair](https://github.com/marimo-team/marimo-pair),
vendored unmodified under Apache-2.0 — see [`bridge/README.md`](bridge/README.md).
Dialogs come from
[`@juicesharp/rpiv-ask-user-question`](https://github.com/juicesharp/rpiv-mono).
Everything else is MIT; see [`LICENSE`](LICENSE).

Built for **SSIE 641 Advanced Network Science** at Binghamton University.
