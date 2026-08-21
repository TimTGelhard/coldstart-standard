---
active_work: docs/work/01-memory-model.md
mode: build
next_action: section 1 session 1 — write docs/FORMAT.md, then seed decisions/ and fixes/ and hand-write the three indexes once
blockers: []
reading: [SPEC.md, docs/ARCHITECTURE.md, docs/PROJECT_BRIEF.md, docs/work/01-memory-model.md]
updated: 2026-08-21
resume_note: "planned but not started; nothing is built yet, and the indexes below are hand-written until tools/index.py exists"
---

# Progress — coldstart-standard

<!-- The block above is the pointer, and it is the only resident part of this tree. It has one
     writer, /done. Nothing below it may restate a field from it. Everything below is an index:
     one line per session, detail in the file it points at. -->

## Queue — planned sessions

| # | Session | What it does | Status | File |
|---|---|---|---|---|
| 1.1 | memory-model s1 | Fix the on-disk format of the pointer, the three indexes and the three folders, and make this repo the first instance | pending | [work/01-memory-model.md](work/01-memory-model.md) |
| 1.2 | memory-model s2 | `tools/index.py` derives the three indexes by scanning the folders; idempotent, fails loudly | pending | [work/01-memory-model.md](work/01-memory-model.md) |
| 1.3 | memory-model s3 | Prove a cold session resumes from the pointer alone, and write the read + close protocols | pending | [work/01-memory-model.md](work/01-memory-model.md) |

Sections 2-7 are named and ordered in [PROJECT_PLAN.md](PROJECT_PLAN.md) and planned just in
time, one section at a time.

## Log — completed sessions

None yet.
