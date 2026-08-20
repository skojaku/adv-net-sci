# Fonts vendored for the worksheets

One file, and it is here for a reason that only shows up in CI.

Every pen-and-paper sheet under `lecture-note/m0*/pen-and-paper/` loads
`fontspec` and asks for a hand-drawn face. **Naming a font that is not
installed is a hard error in fontspec, not a fallback** — so a sheet that says
`\setmainfont{Pretty Neat}` builds on exactly the machines where Pretty Neat is
installed, and nowhere else. Seven sheets were written that way, and by the
time this was noticed none of them built on the instructor's own Mac either.

Each sheet now resolves its face through a chain:

```
Pretty Neat  →  Humor Sans  →  Excalifont  →  Latin Modern Roman
```

The first two are the originals and are installed on almost nothing.
**Excalifont is the link that makes the chain terminate somewhere hand-drawn**,
which is why it is committed here rather than left to whoever runs the build.
`.github/workflows/quarto-publish.yml` copies it into the runner's font path
before `tools/build_worksheets.sh` runs.

`Excalifont-Regular.ttf` — the Excalidraw hand font, SIL Open Font License 1.1.
<https://plus.excalidraw.com/excalifont>

Module 1 is the exception: it is set in Charter, deliberately, and its chain is
`Charter → Iowan Old Style → Georgia → XCharter`. XCharter is Charter and ships
with TeX Live, so nothing needs vendoring for it.

## Building a sheet yourself

```sh
bash tools/build_worksheets.sh                     # all of them
bash tools/build_worksheets.sh lecture-note/m03-robustness/pen-and-paper
```

A full TeX Live has everything the sheets need. BasicTeX does not — it is
missing `adjustbox` and `tikz-3dplot`, and ten of the thirteen sheets stop on
one or the other:

```sh
sudo tlmgr install adjustbox tikz-3dplot
```
