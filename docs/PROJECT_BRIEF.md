# PROJECT_BRIEF — coldstart-standard

> The brief. Derived from `../SPEC.md` (amended 2026-08-21), which stays the authority on the
> feature ledger and the byte budget. This file answers product shape; the SPEC answers scope.

## What is being built

A lean, general-purpose operating harness for Claude Code. Instructions, hooks, a small command
surface and a project-memory model, installed into a project so that a session can be opened and
continued without the operator re-explaining the project.

## Who it is for

Tim, on his real projects, as the default harness. Secondarily anyone who wants ColdStart's
discipline without ColdStart's 1,065-file tree.

## The one outcome

**Open a session with `/coldstart` and no prose, and get correctly scoped work that does not
contradict a decision already on file.** Everything else is subordinate to this.

## Where it lives

Inside a project repository, as files. No service, no daemon, no network on the hot path. The
model reads it; nothing else runs it.

## Primary journey in v1

`/prep` scopes the work and queues sessions. `/coldstart` resumes one. `/done` closes it, files
what was decided, and rewrites the indexes so the next `/coldstart` is correct.

## In v1, in order

1. The memory model: three index files, three folders, indexes derived by scanning.
2. The three commands: `/coldstart`, `/prep`, `/done`.
3. The resident surface: `CLAUDE.md`, a distilled profile, 4 routers, 3 agents.
4. The enforced safety floor.

## Explicitly NOT in v1

Capability library, facet-map, dock · lifecycle state and generated projections from a separate
state file · `registry.tsv` and the ownership manifest · rooms, boxes, caps and the split ritual ·
`bucket` · the soak gate · `adopt` (deferred, not dropped) · any cross-harness comparison score.

## Single or multi user

Single operator, single machine, local files. No auth, no sync, no server.

## Constraints

- Resident surface under 12,000 B, reported in `MEASURE.md`, treated as a design target rather
  than a gate.
- Python 3.12+ stdlib only. No runtime dependencies. No network after install.
- Install is one command, reversible, idempotent.
- Every hook and every skill needs a real firing artifact before it counts as shipped.

## Success

The operator stops re-prompting the project into the session, and stops hand-maintaining the
files that are supposed to maintain themselves. Failure is either of those returning.
