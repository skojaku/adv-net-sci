#!/bin/sh
# The slide skill (~/.claude/skills/slide) is canonical; slides/*.md are its copies, kept in the
# repo so that any agent can read them. Copy them over, or with --check only report differences.
SKILL="${SLIDE_SKILL:-$HOME/.claude/skills/slide}"
DEST="$(cd "$(dirname "$0")/.." && pwd)/slides"
FILES="HOUSE_STYLE.md SLIDE_RUBRIC.md REVIEW_PLAYBOOK.md DECK_BUILD_GUIDE.md FIGURE_GUIDE.md FILLER_PASS.md MAGIC_MOVE.md TALK_PLAYBOOK.md"
status=0
for f in $FILES; do
  if cmp -s "$SKILL/$f" "$DEST/$f"; then continue; fi
  if [ "$1" = "--check" ]; then echo "differs: $f"; status=1; else cp "$SKILL/$f" "$DEST/$f" && echo "copied:  $f"; fi
done
[ "$1" = "--check" ] && [ $status = 0 ] && echo "slides/*.md match the skill"
exit $status
