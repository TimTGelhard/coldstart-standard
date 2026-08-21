---
title: Commands
subject: three commands (coldstart, prep, done), why /coldstart was restored, and what each dropped wrapper cost
topic: commands
updated: 2026-08-21
---

# Decisions — commands

## Three commands, and no more

**Decided**: 2026-08-21

`/coldstart` resumes: read the pointer, load the active work file, continue. `/prep` plans: scope
the work, write the session files into `work/`, queue them in `PROGRESS.md`. `/done` closes: file
the decisions, regenerate the three indexes, verify, rewrite the pointer.

These three are the whole lifecycle loop, and they are the only interface to the memory model.

## /coldstart is restored (supersedes cutting it)

**Decided**: 2026-08-21

Old position: the feature ledger cut eight wrappers down to `prep`, `done` and `orientate`, and
dropped `/coldstart`.

New position: that was arithmetic, not a decision. `/coldstart` is the resume door and the first
thing typed in every session, and `/orientate` is only its read-only half. The whole wrapper set
is 3,599 B against a 12,000 B ceiling, so bytes were never the constraint here.

## What each dropped wrapper cost, and why it went

**Decided**: 2026-08-21

- `orientate` — it is `/coldstart`'s read-only half and not worth a second wrapper.
- `cleanup` and `maintenance` — they sweep generated projections and check-classes that this
  harness does not have, so their subject is gone rather than merely cheap.
- `bucket` — out.
- `adopt` — **deferred, not dropped**. It is a real facility and it lands once `standard` runs on
  a real project.
