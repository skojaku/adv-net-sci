# Tutor E2E harness

Drives a **live tutor session** for Part D of `../TUTOR_REVIEW_RUBRIC.md`:
the reviewer plays the student against the real tutor agent (pi + the
`pi-pair-notebook` toolkit) in an isolated sandbox. Requires `herdr`, `uv`,
`pi`, `python3`, and credentials for whatever `TUTOR_MODEL` names.

## Scripts

```sh
STATE=$(./e2e_setup.sh ../m02-small-world)   # sandbox + marimo + browser + tutor
./screen.sh "$STATE"                          # peek at the tutor pane
./student_turn.sh "$STATE" "I don't code, sorry."   # one student message → reply
./dialog_choice.sh "$STATE" 0                 # answer a select dialog (0-based index)
./e2e_teardown.sh "$STATE"                    # stop; prints the kept sandbox path
```

- `e2e_setup.sh` copies the module (fresh notebook from the template), starts
  `marimo edit --sandbox --headless`, opens the notebook page in a browser
  (**required** — the kernel wakes only when a client connects; without it
  every `nb_*` call fails), then starts pi in a herdr pane with
  `--no-extensions -e <pi-pair-notebook>/extensions/notebook-tool.ts` so the
  machine's global pi extensions can't contaminate the run.
  The toolkit it loads is the **working tree** (`../pi-pair-notebook`), so a fix you
  just made is what gets tested; `PAIR_NOTEBOOK_EXTENSION` overrides that with any
  other checkout, and the module's installed copy is the fallback.
  Env overrides: `TUTOR_MODEL` (default `ollama/glm-5.2:cloud`),
  `TUTOR_VISION_MODEL`, `PAIR_NOTEBOOK_EXTENSION`.
- `student_turn.sh` / `dialog_choice.sh` block until the tutor goes idle
  (override wait with `TURN_TIMEOUT` seconds), then print the screen.
  If the screen shows an option list ("Where to next?"), the next call must
  be `dialog_choice.sh`, not `student_turn.sh`.
- `e2e_teardown.sh` closes the pane and marimo but **keeps the sandbox** —
  run rubric Parts S and P on its `notebook.py` and `session_artifacts/`
  afterward; the E2E gate passes only if that pass is clean too.

## Driving tips

- After `e2e_setup.sh`, wait for the greeting: poll `screen.sh` until the
  tutor asks its first question (~30–60 s for the first model turn).
- Play the persona honestly (rubric Part D lists them); type like a student,
  not like a grader. One message per turn.
- The pane text is the transcript evidence — quote it in findings.
- Resume test (D6): `herdr pane close` the tutor pane only, then re-run the
  `herdr agent start` line from `e2e_setup.sh` with the same sandbox (or
  simply run a new `e2e_setup.sh` against the *sandbox* dir) and check the
  continue/fresh dialog.
