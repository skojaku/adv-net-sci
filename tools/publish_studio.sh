#!/usr/bin/env bash
# Publish the Studio folders to the GitHub repos students clone.
#
#   tools/publish_studio.sh package        # tutor-prototype/pi-studio
#   tools/publish_studio.sh module         # tutor-prototype/m02-small-world
#   tools/publish_studio.sh all [-m "..."]
#
# Exports **HEAD**, not the working tree: what students get is always something
# that exists in this repo's history. Commit first.
#
# The published repos are exports, not forks. Each run wipes the checkout and
# re-exports, so a commit made directly on GitHub is lost on the next publish —
# which is the point: one source of truth, here.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

PKG_REPO="sk-classroom/pi-studio"
MODULE_REPO="sk-classroom/advnetsci-studio-m02-small-world"

MSG=""
DO_PKG=0
DO_MODULE=0
while [ $# -gt 0 ]; do
  case "$1" in
    -m)      MSG="$2"; shift 2 ;;
    package) DO_PKG=1; shift ;;
    module)  DO_MODULE=1; shift ;;
    all)     DO_PKG=1; DO_MODULE=1; shift ;;
    *) echo "usage: $0 [package|module|all] [-m message]" >&2; exit 1 ;;
  esac
done
[ $((DO_PKG + DO_MODULE)) -gt 0 ] || { DO_PKG=1; DO_MODULE=1; }

command -v gh >/dev/null || { echo "error: gh is required" >&2; exit 1; }

publish() { # publish <subdir> <owner/repo>
  local src="$1" repo="$2" work status
  git rev-parse --verify "HEAD:$src" >/dev/null 2>&1 ||
    { echo "error: $src is not in HEAD — commit it first" >&2; return 1; }

  echo "publishing $src -> $repo"
  work=$(mktemp -d "${TMPDIR:-/tmp}/publish-studio-XXXXXX")
  status=0
  if gh repo clone "$repo" "$work/repo" >/dev/null 2>&1; then
    # Wipe and re-export, so deletions here become deletions there.
    find "$work/repo" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
    git archive "HEAD:$src" | tar -x -C "$work/repo"
    # Authoring-only, and the golden is a FINISHED session — an answer key in
    # the repo the student clones. Neither is read at runtime.
    if [ "$src" != "tutor-prototype/pi-studio" ]; then
      rm -f "$work/repo/notebook.golden.py" "$work/repo/review_golden_sync.py"
    fi
    git -C "$work/repo" add -A
    if git -C "$work/repo" diff --cached --quiet; then
      echo "  already up to date"
    else
      git -C "$work/repo" commit --quiet \
        -m "${MSG:-Sync from adv-net-sci@$(git rev-parse --short HEAD)}"
      git -C "$work/repo" push --quiet
      echo "  pushed $(git -C "$work/repo" rev-parse --short HEAD)"
    fi
  else
    echo "error: cannot clone $repo — create it first (gh repo create $repo --public)" >&2
    status=1
  fi
  rm -rf "$work"
  return $status
}

[ "$DO_PKG" = 1 ] && publish tutor-prototype/pi-studio "$PKG_REPO"
[ "$DO_MODULE" = 1 ] && publish tutor-prototype/m02-small-world "$MODULE_REPO"
exit 0
