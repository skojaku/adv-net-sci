# Slide Pipeline Improvement Plan (revised after review)

Derived from analysis of 7 Claude Code sessions (m01–m06 + root), totaling 148MB of
session data, 8,810 messages, 121 agent spawns, 207 inter-agent messages.

Revised per `IMPROVEMENT_PLAN_REVIEW.md`. Key corrections:

- **Gatelib shared before automating** — the copy-and-edit pattern was the root cause
  of lost checks, and adding a second per-module file would have doubled the decay
- **Markdown-source table/code/column detectors removed** — zero markdown table syntax
  in any shipped deck; surviving L1/L2/L3 violations live inside figure PNGs
- **Render hash for change detection** — not markdown diff; three regressions in the
  record are unchanged slides broken by a changed figure
- **Three missing rules added** — private helper ban, assertion independence, PNG
  delete-before-regenerate
- **Tier 1 scope set from measurement, not estimate** — record what fraction Tier 0
  catches on the next module's R1, then set scope

## What was implemented

### 1. gatelib shared gate library (`slides/gatelib/`)

Single source of truth for all automated checks. Each module has a thin wrapper
carrying only its constants. Recovered lost checks:

- `caption_colours` (m02 only, lost m03+)
- `em_dashes` (m03 only, lost m04+)
- `_flood_from_border` (m02, lost m03, rebuilt m04)

### 2. check_deck.py — source-level structural checks

Automated at zero token cost:
- Question slide answer leak (text scope; figure content not examined)
- Figure reuse across non-adjacent slides with different captions
- Fragmented list followed by paragraph (L5)
- Bullet count > 4 (L4)
- KaTeX in raw HTML blocks
- Demo link on slide vs speaker note only (S5a)
- Fragment syntax consistency
- Bold overuse
- Deck structure heuristic (S1)
- Stale render detection
- **Render hash change detection** for Tier 1 review scoping

### 3. REVIEW_PLAYBOOK.md — new rules

- Ban private helpers that bypass shared drawing primitives
- Ground-truth side of assertion must be independently wrong
- Delete figure PNG before regenerating
- Run check_deck.py before any LLM review
- Tiered review with render-hash change detection
- Token-efficient agent architecture

### 4. Skill updates (slide-build, slide-review)

- Tiered review protocol (Tier 0 automated → Tier 1 changed slides → Tier 2 full)
- Agent architecture: 3 agents max (lead + deck-fixer + figure-fixer)
- Guide injection into briefs instead of re-reads
- Checkpoint file for session durability

## What was NOT done (and why)

- **Markdown-source table/code/column detectors** — zero hits on any shipped deck.
  Surviving violations are inside figure PNGs; only render review catches them.
- **Full automation of F1/F4/N1–N4** — these are judgment criteria. The two largest
  finding families (F1: 75, F4: 83) require reading the rendered figure and
  understanding what it encodes. No regex catches "this node size means nothing."
- **Token budget as primary metric** — rounds-to-PASS and severity class of R1
  findings are the binding constraints. Token cost is worth measuring but not worth
  trading coverage for while round count is still the constraint.

## Measurement plan

On the next module's R1:
1. Record what fraction of findings Tier 0 caught
2. Set Tier 1's scope from that number
3. Track rounds-to-PASS and severity class per round
4. Compare token consumption against m06 baseline
