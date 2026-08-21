---
title: Self-hosting
subject: this repo runs its own memory model during its own build, and ships without a comparator score
topic: self-hosting
updated: 2026-08-21
---

# Decisions — self-hosting

## This repo runs its own memory model from section 1

**Decided**: 2026-08-21

`standard`'s own build uses `standard`'s memory model, not ColdStart's. This tree carries
`PROGRESS.md` plus `work/`, `decisions/` and `fixes/`, and no `LIFECYCLE.json`.

Two reasons: a repo whose own docs contradict its spec is a repo nobody trusts, and dogfooding is
the cheapest way to find out whether the model actually works.

**Interim**: the indexes are hand-written until `tools/index.py` lands in section 1 session 2.
This is the one deliberate violation of "derived, never maintained", and it has a closing date.

## The program is unparked, and `standard` ships without a score

**Decided**: 2026-08-21 (supersedes the 2026-08-19 parking)

Old position: no harness gets built, because the program's one rule is that a harness is only
interesting if it can be compared, and the extrinsic-tier comparator was dropped unbuilt.

New position, by owner's call: `standard` and `minimal` are built as harnesses for real use, not
as arms of an experiment. The consequence is stated plainly so nobody rediscovers it later —
`standard` ships without a score.

The parking card in the ColdStart control tree still says parked and is owed a superseding entry.
That is tracked in [../fixes/family.md](../fixes/family.md).

## The success condition is restated in terms this harness can be judged by

**Decided**: 2026-08-21 (supersedes the noise-band condition)

Old position: "within noise of `coldstart` at a third of the resident cost." That is a gate
nothing can open once the comparator is dropped unbuilt.

New position: `standard` succeeds if, on a real project, a session can be opened with
`/coldstart` and no prose, and the work that follows is correctly scoped, does not contradict a
decision already on file, and closes with the record updated. It fails if the operator finds
themselves re-explaining the project, or hand-maintaining the files that are supposed to maintain
themselves.

**Consequence**: the 12,000 B resident budget stays a design constraint, reported in `MEASURE.md`.
It is a number to publish, not a gate to pass.

## The self-report eval consumers are dropped

**Decided**: 2026-08-21

`eval-regression`'s three self-report consumers — routing, memory and skill-fire recall — are cut.
Selecting on a probe of the harness's own routing output picks the arm that routes well while
doing worse work.
