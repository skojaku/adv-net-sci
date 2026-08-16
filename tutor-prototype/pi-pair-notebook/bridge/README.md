# The notebook bridge (vendored)

`scripts/execute-code.sh` and `scripts/discover-servers.sh` are copied
**unmodified** from marimo-pair:

| | |
|---|---|
| upstream | https://github.com/marimo-team/marimo-pair |
| path | `skills/marimo-pair/scripts/` |
| commit | `6cecaff464479eaa2b9714572243da707c261d22` |
| license | Apache License 2.0 — full text in [`LICENSE`](LICENSE) |

`execute-code.sh` is the only way an `nb_*` tool reaches the notebook: it talks
to a running marimo server's HTTP API and runs code in its scratchpad, so
nothing here needs marimo installed on its own.

## Why vendored instead of fetched

The scripts ship inside a **skill**, and a pi tutor that can see that skill
reaches for it mid-hint — a bare `[skill] marimo-pair` line then lands in the
student's terminal, mid-lesson. So only the `scripts/` were ever wanted. Before
this package existed, `run_tutor.sh` did that surgery at every student's first
run: shallow-clone the repo into a cache, copy `scripts/` out, delete the rest.
That is a `git clone` of a third-party repository on 40 laptops in week one,
against a moving `main`, on a network the classroom does not control.

Vendoring pins the version, makes the package self-contained, and removes the
clone. The cost is that upstream fixes have to be pulled in by hand.

## Updating

```bash
git clone --depth 1 https://github.com/marimo-team/marimo-pair /tmp/mp
cp /tmp/mp/skills/marimo-pair/scripts/*.sh bridge/scripts/
git -C /tmp/mp rev-parse HEAD   # record the new commit in the table above
```

Then run a real session before tagging a release — this is the one file whose
breakage makes every `nb_*` call fail at once.
