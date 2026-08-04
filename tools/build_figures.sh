#!/usr/bin/env bash
# Regenerate every static figure used by the lecture note.
#
# The lecture note contains no executable code, so its figures are committed
# SVGs. This script rebuilds them from the scripts in
# docs/lecture-note/figs/src/. Run it whenever one of those scripts changes;
# the note itself never needs a Python environment.
#
# Usage:  bash tools/build_figures.sh
#
# Requires the course environment (igraph, matplotlib, seaborn, numpy, pandas,
# scipy, altair). If you use conda:
#     conda env create -f environment.yml && conda activate advnetsci

set -euo pipefail
cd "$(dirname "$0")/.."

SRC=docs/lecture-note/figs/src
OUT=docs/lecture-note/figs

if [ ! -d "$SRC" ]; then
  echo "no figure sources at $SRC" >&2
  exit 1
fi

fail=0
for f in "$SRC"/*.py; do
  [ -e "$f" ] || continue
  echo "=== $f"
  if ! python3 "$f"; then
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
