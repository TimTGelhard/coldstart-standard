# PROJECT_PLAN — coldstart-standard

> Drafted at `/prep`, 2026-08-21. Seven sections. Only section 1 is planned in detail; the rest
> are named and ordered. Later sections are planned just in time, because earlier ones discover
> the real shape.

## Sections

> Amended 2026-08-21, at section 2 session 4. The section numbers are identity, not order: they
> name the work file (`docs/work/NN-<slug>.md`) and do not move. What moved is section 6's first
> session, which now runs before section 2 can finish. See the amendment note below.

| # | Section | Goal | Depends on | Status |
|---|---|---|---|---|
| 1 | `memory-model` | The three indexes, the three folders, and the tool that derives the indexes by scanning | — | done |
| 2 | `commands` | `/coldstart`, `/prep`, `/done` — the lifecycle loop, each one skill deep | 1, and 6 s1 for its own session 4 | pending |
| 3 | `resident-surface` | `CLAUDE.md`, the distilled profile, 4 routers, 3 agents, the chapter cut | 1, 2 | pending |
| 4 | `safety-floor` | The PreToolUse hook that denies, plus its firing artifact | 1 | done |
| 5 | `verify` | The three checks, each with an inject-one-defect self-test | 1, 3, 4 | done |
| 6 | `install` | One command, reversible, idempotent, `--weight` selector with one arm | 2 s1-s3 for its own session 1; 2, 3, 4, 5 for the rest | pending |
| 7 | `measure` | `MEASURE.md` census of the rendered surface + the containment test | 6 | pending |

### Amendment — the minimal install moves ahead of section 2's proof

Section 2 session 4's first verify item is that a whole section runs `/prep` to `/coldstart` to
`/done` on typed command names with no prose. That cannot be met in the order originally written,
and the reason is not a defect in section 2. This repo's `commands/` and `skills/` sit unmapped at
the repo root, registered nowhere, so typing `/coldstart` here loads the neighbouring v1 install's
skill instead of this harness's. Mapping the payload into `.claude/` is section 6, and section 6 sat
after section 2. Section 2 was verifying a property section 6 delivers.

Measured rather than argued: a fresh agent given this tree and the single instruction to run
`/coldstart` read v1's payload from outside the repo, resumed section 2 session 4 rather than the
section `/prep` had just planned, and never learned that section 4 was planned at all.

So section 6 splits. **Session 1 is the minimal map**: `commands/` and `skills/` into `.claude/`,
reversible and idempotent, and nothing else — no `--weight` selector, no packaging, no uninstall
story. It depends only on section 2 sessions 1 to 3, which are done, so the cycle breaks cleanly:
the command files exist, and mapping them needs nothing section 6's later sessions provide. The
rest of section 6 keeps its original dependencies and its original place.

This does not weaken section 2 session 4's verify list. The condition stands as written, because
"three command names and no prose" is the SPEC's own success condition, and rewriting it to pass
would have hidden the gap the session was built to find.

## Why this order

Section 1 first because every other section reads or writes the memory model, and because four
other harnesses in the family inherit it. Commands second because they are the only interface to
it. The resident surface third, once there is something for it to point at, so the byte census
is measuring the real thing. The floor is independent and could move, but it sits after the
things it protects so its deny rules have real paths to name. Verify needs its subjects to exist.
Install packages what exists. Measure comes last because a census of a half-built surface is a
number that has to be taken twice.

The one exception is the minimal map, section 6 session 1, which runs early. A command that is not
installed cannot be typed, and a lifecycle proved by reading its source files rather than by running
them is not proved. Installing is therefore upstream of proving, even though packaging stays
downstream of everything. The amendment above records what forced the split.

## The rule this plan is under

`standard` is a rebuild that reads ColdStart, not a fork with files deleted. For every component:
read the `design/NN` file that settled it, carry the decision, leave the implementation. When a
ColdStart mechanism looks necessary, the question is what it was defending against, and whether
the lean shape still has that exposure.

## Open questions

- The chapter cut (which 12-15 of ColdStart's 84 survive) is unanswered and belongs to section 3.
- The 4 routers are a count, not a list. Section 3 names them, and the description-length dial
  matters more than the count: ColdStart's 17 routers average 713 B each, and 250 B each is the
  target.
- `minimal` is being built alongside. If its two-file model diverges from this one, they get
  reconciled at section 6, not before.
