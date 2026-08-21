# PROJECT_PLAN — coldstart-standard

> Drafted at `/prep`, 2026-08-21. Seven sections. Only section 1 is planned in detail; the rest
> are named and ordered. Later sections are planned just in time, because earlier ones discover
> the real shape.

## Sections

| # | Section | Goal | Depends on | Status |
|---|---|---|---|---|
| 1 | `memory-model` | The three indexes, the three folders, and the tool that derives the indexes by scanning | — | done |
| 2 | `commands` | `/coldstart`, `/prep`, `/done` — the lifecycle loop, each one skill deep | 1 | pending |
| 3 | `resident-surface` | `CLAUDE.md`, the distilled profile, 4 routers, 3 agents, the chapter cut | 1, 2 | pending |
| 4 | `safety-floor` | The PreToolUse hook that denies, plus its firing artifact | 1 | pending |
| 5 | `verify` | The three checks, each with an inject-one-defect self-test | 1, 3, 4 | pending |
| 6 | `install` | One command, reversible, idempotent, `--weight` selector with one arm | 2, 3, 4, 5 | pending |
| 7 | `measure` | `MEASURE.md` census of the rendered surface + the containment test | 6 | pending |

## Why this order

Section 1 first because every other section reads or writes the memory model, and because four
other harnesses in the family inherit it. Commands second because they are the only interface to
it. The resident surface third, once there is something for it to point at, so the byte census
is measuring the real thing. The floor is independent and could move, but it sits after the
things it protects so its deny rules have real paths to name. Verify needs its subjects to exist.
Install packages what exists. Measure comes last because a census of a half-built surface is a
number that has to be taken twice.

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
