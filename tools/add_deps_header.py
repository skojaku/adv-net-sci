#!/usr/bin/env python3
"""Add a PEP 723 dependency header to marimo notebooks.

molab and marimo's WASM runtime read the `# /// script` block at the top of a
notebook to know what to install. Without it a reader has to set up the
environment by hand, which defeats the point of a one-click notebook.

This scans each notebook's imports, maps them to distribution names, and writes
the header. Notebooks that already have one are left alone, so the hand-tuned
ones (with pinned versions and display settings) are never clobbered.

Usage:  python3 tools/add_deps_header.py notebooks/*/coding.py ...
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

# import name -> distribution name on PyPI
DIST = {
    # Pyodide ships the real package as "igraph"; "python-igraph" is only a shim.
    "igraph": "igraph",
    "sklearn": "scikit-learn",
    "PIL": "pillow",
    "cv2": "opencv-python-headless",
    "torch_geometric": "torch-geometric",
    "yaml": "pyyaml",
    "bs4": "beautifulsoup4",
    "umap": "umap-learn",
    "skimage": "scikit-image",
}
# modules in the standard library or provided by marimo itself
# Not installable from PyPI; conda-only. Left out of the header so the rest
# of the notebook still resolves, with a comment in the file instead.
CONDA_ONLY = {"graph_tool"}

SKIP = {
    "marimo", "math", "random", "os", "sys", "time", "json", "re", "io",
    "pathlib", "collections", "itertools", "functools", "typing", "dataclasses",
    "warnings", "copy", "string", "textwrap", "urllib", "csv", "gzip", "pickle",
    "subprocess", "shutil", "tempfile", "glob", "heapq", "abc", "enum",
}

HEADER = """# /// script
# dependencies = [
{deps}
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

"""


def imports_of(source: str) -> set[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                found.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                found.add(node.module.split(".")[0])
    return found


def main(paths: list[str]) -> None:
    for p in paths:
        path = Path(p)
        src = path.read_text()
        if src.lstrip().startswith("# /// script"):
            print(f"  skip (has header)  {path}")
            continue
        mods = {m for m in imports_of(src) if m not in SKIP}
        conda_only = sorted(mods & CONDA_ONLY)
        mods -= CONDA_ONLY
        deps = sorted({DIST.get(m, m) for m in mods} | {"marimo"})
        block = "\n".join(f'#     "{d}",' for d in deps)
        note = ""
        if conda_only:
            note = ("# NOTE: this notebook also imports " + ", ".join(conda_only) +
                    ", which is not\n# installable from PyPI. Install it with conda, or run that cell locally.\n\n")
        path.write_text(HEADER.format(deps=block) + note + src)
        print(f"  wrote header       {path}  ({', '.join(deps)})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
