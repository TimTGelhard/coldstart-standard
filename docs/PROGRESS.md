---
active_work: docs/work/01-memory-model.md
mode: build
next_action: section 1 session 2 — write tools/index.py so the three indexes are generated, not hand-written
blockers: []
reading: [docs/FORMAT.md, docs/PROGRESS.md]
updated: 2026-08-21
resume_note: "the format is written and this tree conforms to it by hand; session 2 is what makes the indexes stop being hand-written"
---

# Progress — coldstart-standard

<!-- The block above is the pointer, and it is the only resident part of this tree. It has one
     writer, /done. Nothing below it may restate a field from it. Everything below is an index:
     one line per session, detail in the file it points at. Grammar: docs/FORMAT.md section 5.
     Hand-written until tools/index.py exists (section 1 session 2); generated after it.
     GENERATED BELOW THIS LINE -->

## Queue — sessions not yet done

| # | Session | What it does | Status | File |
|---|---|---|---|---|
| 1.2 | memory-model s2 | the indexes stop being hand-written; one script scans each folder and rewrites the index above it | pending | [work/01-memory-model.md](work/01-memory-model.md) |
| 1.3 | memory-model s3 | prove the model does the job it exists for, which is that a session can start from the pointer and nothing else | pending | [work/01-memory-model.md](work/01-memory-model.md) |

Sections 2-7 are named and ordered in [PROJECT_PLAN.md](PROJECT_PLAN.md) and planned just in
time, one section at a time.

## Log — closed sections

None yet.
