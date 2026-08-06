# Slide Pipeline Improvement Plan

Derived from analysis of 7 Claude Code sessions (m01–m06 + root), totaling 148MB of session data, 8,810 messages, 121 agent spawns, 207 inter-agent messages.

> **Read `IMPROVEMENT_PLAN_REVIEW.md` before implementing sections A, B or C.** It checks
> this plan against the review records and the six copies of `check_render.py`, and finds
> one prerequisite the plan does not name (the gate is copied per module and has lost three
> checks across module boundaries), plus three Section A checks that are green by
> construction on every deck ever shipped.

## Mistake Taxonomy (from session history)

### Category 1: Process Failures (highest cost, most preventable)
| Mistake | Sessions | Cost | Automatable? |
|---------|----------|------|--------------|
| Stale render reviewed (figure agent still running) | m01, m03, m04 | 3+ full rounds | ✅ Pre-review staleness check |
| Fix reported landed but render contradicts | m01–m06 every round | 1+ round each | ✅ Post-fix render + gate |
| `str.replace` silent no-op | m04, m05 | 1 round each | ✅ Assert-match in edit script |
| Gate exit status read wrong (grep pipe) | m02 | Multiple rounds | ✅ Gate script wraps itself |
| Inert gate (never fires, read as coverage) | m02, m03 | 2 full builds | ✅ Gate self-test on known-bad input |

### Category 2: Token Waste (structural, recurring)
| Waste | Count | Est. tokens | Automatable? |
|-------|-------|------------|--------------|
| Guide re-reads by spawned agents | 49 reads | ~370K | ✅ Inject into agent brief |
| PNG review (image read per slide) | 224 reads | ~2.2M | ⚠️ Partially (see below) |
| Inter-agent message overhead | 207 msgs | ~414K | ✅ Reduce agent count |
| Session limit failures mid-build | 8 crashes | Lost work + restart | ✅ Checkpointing |
| File reads via bash (cat/head/tail) | 184 cmds | ~500K | ✅ Better context management |

### Category 3: Content Errors (reached slides)
| Error | Sessions | Root cause |
|-------|----------|------------|
| Arithmetic error in spec | m01, m05 | Numbers not computed before spec |
| Shared figure used with different explanations | m01, m04 | No cross-slide consistency check |
| Question slide leaks answer in note/gray text | m01, m02 | No automated leak check |
| Caption orphaned by figure regrouping | m04 | No caption-figure consistency check |
| Assertion ground truth not independent | m04 | Structural, needs rule |
| Container mismatch (figure authored for wrong width) | m02, m06 | Deck written after figures |

## Proposed Improvements

### A. Automate structural checks → `check_deck.py` (new)

Extends `check_render.py` with source-level checks that currently require LLM reviewers:

```
ALREADY AUTOMATED (check_render.py):
  ✅ Node disc size band (26–52px)
  ✅ In-figure text x-height ≥ 15px
  ✅ Content bottom overflow
  ✅ Drawing size / ink fraction / margin
  ✅ Container mismatch

NEW — add to check_deck.py:
  1. Question slide answer leak — scan question slides for answer text
  2. Figure reuse across slides with different captions
  3. Fragmented list followed by paragraph (L5 violation)
  4. Table detection (L2 violation)
  5. Code block detection (L3 violation)
  6. Multiple text columns (L1 violation)
  7. Bullet count > 4 (L4 violation)
  8. Missing figure for concept slides (N2 heuristic)
  9. Marp fragment syntax check (* not -)
 10. Stale caption detection (caption contains figure-specific numbers no longer in figure)
 11. Demo link on slide (S5a — grep export for href)
 12. KaTeX in raw HTML blocks (figcaption, steps-list)
 13. Deck structure: four-act arc detection (S1–S4 heuristic)
 14. Slide count per part balance
```

These are all **regex/structural checks on the markdown source** — zero LLM tokens.

### B. Tiered LLM review (replace full-deck review)

Current: every slide reviewed by LLM per round (~224 PNG reads, ~2.2M tokens).

Proposed 3-tier system:

```
Tier 0: Automated gate (check_render.py + check_deck.py)
  → Runs in seconds, zero tokens
  → Catches ~60% of historical findings

Tier 1: Targeted LLM review (only what Tier 0 cannot check)
  → Only review slides that CHANGED since last PASS
  → Only check criteria that need judgment:
    - P1 (one point per slide)
    - F1 (unexplained encodings)
    - F4 (figure carries the point)
    - N1–N4 (narrative quality)
    - S1–S5 (four-act structure)
  → Skip: layout, sizes, colors, overflow (Tier 0 handles)

Tier 2: Full deck review (milestone only)
  → Once per module, before shipping
  → Full rubric, all slides
```

Estimated savings: 224 PNG reads → ~40 per round (only changed slides + judgment criteria).

### C. Agent architecture redesign

Current: 4–8 agents (reviewers A–D, fix-deck, fix-figs, fig-builder, verify-A/B/C)
Each re-reads guides + rubric. 121 agent spawns, 207 messages.

Proposed: 3 agents maximum per round.

```
Lead (1 agent, expensive model)
  ├── Reads all guides ONCE
  ├── Runs Tier 0 gate
  ├── Reviews ONLY judgment-criteria slides (Tier 1)
  ├── Writes FIXES_Rn.md
  └── Dispatches fixes

Deck-fixer (1 agent, cheap model)
  ├── Gets: FIXES_Rn.md + deck file + relevant guide EXCERPTS in brief
  ├── Applies markdown edits only
  └── Reports: "N replacements applied, each matched exactly once"

Figure-fixer (1 agent, cheap model)
  ├── Gets: FIXES_Rn.md + generator file + FIGURE_GUIDE excerpts in brief
  ├── Applies generator edits
  ├── Runs make_figures.py
  └── Reports: per-figure emit lines (name WxH node-px x-height)
```

Key changes:
1. **Guides injected into brief** — no agent re-reads SLIDE_RUBRIC.md
2. **Cheap model for fixers** — applying a spec ≠ judgment
3. **Fewer agents** — 3 per round instead of 8+
4. **Structured handoff** — fix spec contains exact old→new strings, not intentions

### D. Session durability

8 session-limit failures mid-build. Mitigations:

1. **Checkpoint file**: after each round, write `review/CHECKPOINT.md` with:
   - Current round number
   - Gate status (pass/fail output)
   - Pending fixes
   - Which agents were running
2. **Atomic commits**: commit after every successful gate pass, not just at round end
3. **Idempotent re-entry**: `slide-build` skill can resume from checkpoint if session crashes

### E. Preventive rules to add to existing files

New entries for REVIEW_PLAYBOOK.md:

1. **"Run the pre-review staleness check as a script, not a command"** — wrap in shell script that also checks for running generator processes
2. **"Every fix script must assert each replacement matched"** — codify in the fixer agent brief template
3. **"Gate scripts must exit with their own status, never piped through grep"** — add self-test to check_render.py
4. **"New gates must prove they fire on known-bad input"** — gate self-test requirement

New entries for DECK_BUILD_GUIDE.md:

5. **"Write the deck before commissioning figures"** (already there, but violated in m06 — make it a hard gate: no figure work until deck markdown exists)
6. **"Numbers in spec must be computed, not estimated"** — add verification step to spec review

New entries for SLIDE_RUBRIC.md:

7. **F6: No shared figures with different explanations** — codify as Blocker
8. **N5: No answer leak on question slides** — codify as Blocker with automated check

## Token Budget Estimate

| Phase | Current (per module) | Proposed | Savings |
|-------|---------------------|----------|---------|
| Guide reads | 49 reads × 7.5K = 370K | 6 reads × 7.5K = 45K | 88% |
| PNG review | 224 reads × 10K = 2.2M | 40 reads × 10K = 400K | 82% |
| Inter-agent msgs | 207 × 2K = 414K | 30 × 2K = 60K | 86% |
| File reads via bash | 184 × 3K = 552K | 30 × 3K = 90K | 84% |
| **Total** | **~3.5M tokens/module** | **~600K tokens/module** | **83%** |
