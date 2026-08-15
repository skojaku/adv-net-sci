#!/usr/bin/env bash
# Regenerate every static figure used by the lecture note.
#
# The lecture note contains no executable code, so its figures are plain SVGs
# built ahead of the render. They are NOT committed — CI runs this script
# before `quarto render`, and so should you after a fresh clone.
# Everything else in lecture-note/figs/ is hand-made art with no generator.
#
# Usage:  bash tools/build_figures.sh
#
# Requires the course environment (igraph, matplotlib, seaborn, numpy, pandas,
# scipy, altair). If you use conda:
#     conda env create -f environment.yml && conda activate advnetsci

set -euo pipefail
cd "$(dirname "$0")/.."

SRC=lecture-note/figs/src
OUT=lecture-note/figs

# Prefer the local figure venv when it exists; CI installs the deps into the
# ambient interpreter instead.
if [ -x .venv-figs/bin/python ]; then
  PY=.venv-figs/bin/python
else
  PY=python3
fi

if [ ! -d "$SRC" ]; then
  echo "no figure sources at $SRC" >&2
  exit 1
fi

fail=0
for f in "$SRC"/*.py; do
  [ -e "$f" ] || continue
  echo "=== $f"
  if ! "$PY" "$f"; then
    echo "!!! FAILED: $f" >&2
    fail=1
  fi
done

echo
echo "SVGs now in $OUT:"
ls -1 "$OUT"/*.svg 2>/dev/null | sed 's|.*/|  |' || echo "  (none)"

if [ "$fail" -ne 0 ]; then
  echo
  echo "Some figure scripts failed. The lecture note will render with broken" >&2
  echo "image links until they are fixed." >&2
  exit 1
fi
