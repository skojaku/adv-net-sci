#!/usr/bin/env python3
"""Extract executable code out of Quarto lecture notes.

The lecture note is prose + static figures only; all code lives in marimo
notebooks. This tool moves code out of .qmd files.

Subcommands
-----------
list       Show every python cell in a .qmd with its index and options.
to-ipynb   Write all python cells of a .qmd into a Jupyter notebook, which can
           then be converted with `marimo convert nb.ipynb -o nb.py`.
to-figs    Write all python cells into a single flat script that saves each
           figure to an SVG instead of displaying it. Cell order is preserved,
           so setup cells still run before the cells that depend on them.

Usage
-----
    python tools/qmd_code.py list lecture-note/m05-clustering/02-coding.qmd
    python tools/qmd_code.py to-ipynb <in.qmd> -o notebooks/m05-clustering/coding.ipynb
    python tools/qmd_code.py to-figs <in.qmd> -o lecture-note/figs/src/m05.py --prefix m05
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

# ```{python} ... ``` — the fence Quarto uses for executable python.
CELL_RE = re.compile(r"^```\{python\}\s*$(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
# `#| key: value` cell options at the top of a cell.
OPT_RE = re.compile(r"^#\|\s*([\w-]+)\s*:\s*(.*)$")


@dataclass
class Cell:
    index: int
    options: dict[str, str] = field(default_factory=dict)
    source: str = ""
    start: int = 0
    end: int = 0

    @property
    def label(self) -> str:
        return self.options.get("label", "").strip('"')

    @property
    def caption(self) -> str:
        return self.options.get("fig-cap", "").strip('"')

    @property
    def makes_figure(self) -> bool:
        """A cell is figure-producing if it is captioned or draws something.

        Cells marked `include: false` or `output: false` are setup cells: they
        run so later cells work, but they show nothing, so they get no SVG.
        """
        if self.options.get("include") == "false" or self.options.get("output") == "false":
            return False
        if "fig-cap" in self.options or "fig-width" in self.options:
            return True
        return bool(re.search(r"\b(plt|sns|ig)\.\w|\.plot\(|savefig", self.source))


def parse(path: Path) -> tuple[str, list[Cell]]:
    text = path.read_text()
    cells: list[Cell] = []
    for i, m in enumerate(CELL_RE.finditer(text)):
        body = m.group(1)
        options: dict[str, str] = {}
        code_lines: list[str] = []
        in_header = True  # cell options only appear before the first line of code
        for line in body.splitlines():
            om = OPT_RE.match(line)
            if in_header and om:
                options[om.group(1)] = om.group(2).strip()
                continue
            if in_header and not line.strip():
                continue  # blank lines before/among the options
            in_header = False
            code_lines.append(line)
        cells.append(
            Cell(
                index=i,
                options=options,
                source="\n".join(code_lines).strip("\n"),
                start=m.start(),
                end=m.end(),
            )
        )
    return text, cells


def cmd_list(args) -> None:
    _, cells = parse(Path(args.qmd))
    for c in cells:
        flag = "FIG" if c.makes_figure else "   "
        first = next((l for l in c.source.splitlines() if l.strip()), "")
        print(f"[{c.index:2d}] {flag} {len(c.source.splitlines()):3d} lines  {first[:60]}")
        if c.caption:
            print(f"          cap: {c.caption[:70]}")


def cmd_to_ipynb(args) -> None:
    _, cells = parse(Path(args.qmd))
    nb = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": (c.source + "\n").splitlines(keepends=True),
            }
            for c in cells
            if c.source.strip()
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(nb, indent=1))
    print(f"{out}: {len(nb['cells'])} cells")


def cmd_to_figs(args) -> None:
    _, cells = parse(Path(args.qmd))
    prefix = args.prefix
    lines = [
        '"""Regenerate the static figures for this module.',
        "",
        f"Extracted from {args.qmd}.",
        "Run from the repository root; writes SVGs into lecture-note/figs/.",
        '"""',
        "",
        "import matplotlib",
        "matplotlib.use('Agg')",
        "import matplotlib.pyplot as plt",
        "from pathlib import Path",
        "",
        "OUT = Path(__file__).resolve().parents[1]",
        "OUT.mkdir(parents=True, exist_ok=True)",
        "",
        "",
        "def _save(name):",
        "    plt.savefig(OUT / f'{name}.svg', bbox_inches='tight', transparent=True)",
        "    plt.close('all')",
        "    print('wrote', name + '.svg')",
        "",
    ]
    fig_n = 0
    for c in cells:
        if not c.source.strip():
            continue
        lines.append("")
        lines.append(f"# --- cell {c.index} " + "-" * 50)
        if c.caption:
            lines.append(f"# caption: {c.caption}")
        lines.append(c.source)
        if c.makes_figure:
            name = c.label or f"{prefix}-fig-{fig_n:02d}"
            name = name.replace("fig-", "", 1) if name.startswith("fig-") else name
            lines.append(f"_save({name!r})")
            fig_n += 1
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    print(f"{out}: {fig_n} figures from {len(cells)} cells")


def cmd_strip(args) -> None:
    """Replace every python cell with a static image include (or delete it)."""
    path = Path(args.qmd)
    text, cells = parse(path)
    prefix = args.prefix
    fig_n = 0
    pieces: list[str] = []
    cursor = 0
    replaced = deleted = 0
    for c in cells:
        pieces.append(text[cursor : c.start])
        cursor = c.end
        if c.makes_figure:
            name = c.label or f"{prefix}-fig-{fig_n:02d}"
            if name.startswith("fig-"):
                name = name[4:]
            fig_n += 1
            label = c.label or f"fig-{name}"
            if not label.startswith("fig-"):
                label = f"fig-{label}"
            cap = c.caption
            width = c.options.get("fig-width")
            attrs = f"{{#{label}"
            if width:
                attrs += f' width="{width}"'
            attrs += "}"
            # A markdown image needs a blank line on both sides, or Quarto
            # folds it into the neighbouring paragraph and the crossref breaks.
            before = "" if not pieces or pieces[-1].endswith("\n\n") else "\n"
            after = "" if text[cursor:].startswith("\n\n") else "\n"
            pieces.append(f"{before}![{cap}](../figs/{name}.svg){attrs}\n{after}")
            replaced += 1
        else:
            # A setup cell with no output: drop it, the figure script keeps it.
            deleted += 1
            if pieces and pieces[-1].endswith("\n\n"):
                pieces[-1] = pieces[-1][:-1]
    pieces.append(text[cursor:])
    out = Path(args.out) if args.out else path
    out.write_text("".join(pieces))
    print(f"{out}: {replaced} cells -> images, {deleted} setup cells removed")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list")
    pl.add_argument("qmd")
    pl.set_defaults(func=cmd_list)

    pi = sub.add_parser("to-ipynb")
    pi.add_argument("qmd")
    pi.add_argument("-o", "--out", required=True)
    pi.set_defaults(func=cmd_to_ipynb)

    pf = sub.add_parser("to-figs")
    pf.add_argument("qmd")
    pf.add_argument("-o", "--out", required=True)
    pf.add_argument("--prefix", required=True)
    pf.set_defaults(func=cmd_to_figs)

    ps = sub.add_parser("strip")
    ps.add_argument("qmd")
    ps.add_argument("-o", "--out", default=None, help="default: edit in place")
    ps.add_argument("--prefix", required=True)
    ps.set_defaults(func=cmd_strip)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
