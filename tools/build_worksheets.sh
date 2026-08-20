#!/usr/bin/env bash
#
# Compile every pen-and-paper worksheet from LaTeX to PDF.
#
# The PDFs are NOT in git — `.gitignore` has `*.pdf`, and the worksheets that
# used to sit beside their sources were force-added. They are built here
# instead: by CI before the lecture note is published (see
# .github/workflows/quarto-publish.yml), and by hand when you want to print
# one.
#
#   bash tools/build_worksheets.sh                    # all of them
#   bash tools/build_worksheets.sh lecture-note/m03-robustness/pen-and-paper
#   bash tools/build_worksheets.sh .../exercise.tex   # one sheet
#
# XeLaTeX, not pdflatex: every sheet loads `fontspec`. The house font is
# Excalifont, vendored in tools/fonts/ so that a CI runner produces the same
# sheet a laptop does — see the README there for why that matters.
#
# A .tex without \documentclass is an \input fragment (m01's mapkit.tex) and is
# skipped rather than compiled into a broken PDF.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ---------------------------------------------------------------------------
# Collect the sheets to build
# ---------------------------------------------------------------------------
sources=()
if [[ $# -gt 0 ]]; then
  for arg in "$@"; do
    if [[ -f "$arg" ]]; then
      sources+=("$arg")
    elif [[ -d "$arg" ]]; then
      while IFS= read -r f; do sources+=("$f"); done \
        < <(find "$arg" -maxdepth 1 -name '*.tex' | sort)
    else
      echo "build_worksheets: no such file or directory: $arg" >&2
      exit 1
    fi
  done
else
  while IFS= read -r f; do sources+=("$f"); done \
    < <(find "$repo_root/lecture-note" -path '*/pen-and-paper/*.tex' | sort)
fi

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
# latexmk decides how many passes a sheet needs; without it, two xelatex runs
# is the number that settles \label references and tcolorbox page breaks.
if command -v latexmk >/dev/null 2>&1; then
  compile() { latexmk -xelatex -interaction=nonstopmode -halt-on-error -quiet "$1"; }
else
  compile() {
    xelatex -interaction=nonstopmode -halt-on-error "$1" >/dev/null
    xelatex -interaction=nonstopmode -halt-on-error "$1" >/dev/null
  }
fi

built=0
skipped=0
failed=()

for src in "${sources[@]}"; do
  rel="${src#"$repo_root"/}"

  if ! grep -q '\\documentclass' "$src"; then
    echo "  skip   $rel  (\\input fragment, no \\documentclass)"
    skipped=$((skipped + 1))
    continue
  fi

  dir="$(dirname "$src")"
  base="$(basename "$src")"

  # Compile inside the sheet's own directory: sheets \input siblings and
  # \includegraphics siblings (m01's mapkit.tex, m01lab-qr.png) by bare name.
  if (cd "$dir" && compile "$base"); then
    echo "  built  ${rel%.tex}.pdf"
    built=$((built + 1))
  else
    echo "  FAILED $rel" >&2
    failed+=("$rel")
  fi

  # The aux/log litter is git-ignored, but leaving it behind makes a later
  # `latexmk` reuse a stale run. Sheets are cheap; clean every time.
  (cd "$dir" && rm -f "${base%.tex}".{aux,log,out,fls,fdb_latexmk,synctex.gz,toc,nav,snm})
done

echo "build_worksheets: ${built} built, ${skipped} skipped, ${#failed[@]} failed"

if [[ ${#failed[@]} -gt 0 ]]; then
  printf 'failed: %s\n' "${failed[@]}" >&2
  exit 1
fi
