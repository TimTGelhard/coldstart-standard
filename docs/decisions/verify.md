---
title: Verify
subject: why three checks rather than thirty, what each one watches, and the self-test bar each had to clear
topic: verify
updated: 2026-08-21
---

## Three checks, and a check earns its place by having caught something

**Decided**: 2026-08-21

`SPEC.md` cut ColdStart's 30 check-classes to three: `ghost-refs`, `byte-budgets`,
`hooks-registered`. Built as specified, and the cut held — nothing during section 4 or 5
wanted a fourth.

Most of ColdStart's 30 exist to police a split this harness does not have. `state-consistency`
and `warehouse-maps` watch `LIFECYCLE.json` against its generated projections; there is no
`LIFECYCLE.json` here, because the indexes are a function of their folders rather than of a
separate state file, so the class of defect is absent rather than unchecked.

What survives is the three things that can still go wrong here: a reference can outlive its
target, the resident surface can grow without anyone noticing, and a hook can be present
without being run.

## Each check had to go red on a planted defect before it counted

**Decided**: 2026-08-21

`tests/test_verify.py` copies the real repo, breaks exactly one thing, and asserts the check
finds it. This is the SPEC's Adds-4 bar applied to the checks themselves.

The bar is not ceremony. It caught a real defect the moment it was applied: `ghost-refs`
compared a resolved link path against an unresolved repo root, and on macOS `/var` is a
symlink to `/private/var`, so every link in the temp tree read as "points outside the repo" —
a case the check tolerates by design. It passed. It would have gone on passing while watching
nothing, which is the exact failure the self-test bar exists to catch, and it is the reason
"the check runs" is not evidence that "the check works".

## byte-budgets measures the rendered surface, not the file list

**Decided**: 2026-08-21

For a skill, only the front matter is resident: the body loads on demand. So the check counts
front matter for `SKILL.md` and the whole file for `CLAUDE.md`, the profile and the wrappers,
plus the pointer block that the SessionStart hook injects.

Counting whole skill files would report a number several times the truth and make every later
trim look like it did nothing — which is `SPEC.md`'s stated complaint about ColdStart's own
floor guard covering 55% of the floor it is named for. A test adds 5 KB to a skill body and
asserts the measurement does not move.

Over the ceiling is a red that means "amend the ledger or trim", not "the build is broken".
`SPEC.md` calls the 12,000 B a number to publish rather than a gate, and the failure text says
so, because a check whose meaning is not in its own output gets misread the first time it fires
at 3pm on a Friday.

## ghost-refs reports out-of-repo references rather than failing them

**Decided**: 2026-08-21

`docs/FORMAT.md` rule 7 already settled this and the check implements it: a reference that
escapes the root or is absolute is machine-local, and a sibling tree's absence is not this
repo's defect.

It is load-bearing here rather than theoretical. This repo carries several true citations into
ColdStart v1 at `/Users/macbook/coldstart/...`, and the alternatives were deleting a true
citation or carrying a permanently red check. Both are worse than a counted, reported number.
