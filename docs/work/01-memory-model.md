---
title: Memory model
subject: the three indexes, the three folders, and the tool that derives the indexes by scanning
topic: memory-model
updated: 2026-08-21
---

# Section 1 — memory-model

> The section plan. Three sessions. Written at `/prep`, 2026-08-21.
> Goal: the three indexes, the three folders, and the tool that derives the indexes by scanning.

**Done when**: a fresh session that has read nothing but `docs/PROGRESS.md` can name what it is
working on, what was decided, and what is open, and `/done`'s index regeneration is a no-op on a
clean tree.

---

## Session 1 — the shapes, and this tree adopts them

**Status**: done

**Closed**: 2026-08-21

**Goal**: fix the exact on-disk format of the three index files, the three folders and the
pointer, and prove it by making this repo's own `docs/` the first instance.

**Files to read**
- `SPEC.md` (the memory model section)
- `docs/ARCHITECTURE.md`
- `docs/PROJECT_BRIEF.md`
- `/Users/macbook/coldstart/design/02-*.md` (ColdStart's pointer + queue spec — carry the
  decision, leave the implementation)

**Build steps**
1. Write `docs/FORMAT.md`: the field list for the pointer, the one-line grammar for each of the
   three index files, the front-matter each content file carries (title, one-line subject, topic,
   date), and the topic-clustering rule. This is the contract `tools/index.py` implements in
   session 2, so it is written before the tool, not after it.
2. Seed `docs/decisions/` from this build's own history: the memory model, the three commands,
   in-project install, self-hosting. Four topic files or fewer. **Delegate the source read** to an
   agent over `SPEC.md`, `../../CHARTER.md` and the ColdStart parking card, and take back the
   decisions, not the file contents.
3. Seed `docs/fixes/` with what is already known-open (the ColdStart parking card still says
   parked; `minimal`'s spec has not been amended to match this model).
4. Hand-write `DECISIONS.md` and `FIXES.md` to the grammar from step 1, and add the queue index to
   `PROGRESS.md`. Hand-written this once only, because the tool does not exist yet.

**Files to write**
- `docs/FORMAT.md`
- `docs/DECISIONS.md`, `docs/decisions/*.md`
- `docs/FIXES.md`, `docs/fixes/*.md`
- `docs/PROGRESS.md` (queue index section)

**Verify**
1. Every line in each of the three index files resolves to a file that exists.
2. Every file in the three folders is named by exactly one index line, and no index line names a
   missing file. Both directions, because the tool in session 2 has to hold both.
3. `docs/FORMAT.md` describes the files that were actually written, checked by re-reading one
   file of each kind against it.
4. The pointer alone names the active work file, the next action and the read list, with nothing
   in it that also appears below it.

**Output**: `feat: the memory model has a written format, and this tree is its first instance`

---

## Session 2 — `tools/index.py`

**Status**: pending

**Goal**: the indexes stop being hand-written. One script scans each folder and rewrites the
index above it.

**Files to read**
- `docs/FORMAT.md`
- `docs/PROGRESS.md`

**Build steps**
1. `tools/index.py`: scan `work/`, `decisions/`, `fixes/`; read each file's front matter; rewrite
   the three index files. Python stdlib only.
2. Idempotence: a second run on an unchanged tree produces a byte-identical file. This is the
   property that makes the index trustworthy, so it is asserted, not assumed.
3. Preserve the pointer block. `index.py` rewrites the queue section of `PROGRESS.md` and must
   never touch the fields above it.
4. Fail loudly on a malformed file rather than silently skipping it. A file missing from an index
   is invisible, which is the failure mode that matters.
5. A test file with a fixture tree covering: a new file, a renamed file, a deleted file, a
   malformed file.

**Files to write**
- `tools/index.py`
- `tests/test_index.py`, `tests/fixtures/`

**Verify**
1. Run on this tree, diff against the hand-written indexes from session 1. Any difference is
   either a tool bug or a session-1 error, and the resolution is recorded either way.
2. Second run is byte-identical to the first.
3. Delete a file, re-run, confirm its index line is gone. Add one, re-run, confirm it appears.
4. Corrupt a file's front matter, re-run, confirm a non-zero exit and a message naming the file.
5. The pointer block is byte-identical before and after every run above.

**Output**: `feat: the indexes are derived from the folders, not maintained beside them`

---

## Session 3 — the cold-resume proof

**Status**: pending

**Goal**: prove the model does the job it exists for, which is that a session can start from the
pointer and nothing else.

**Files to read**
- `docs/PROGRESS.md`
- `docs/FORMAT.md`

**Build steps**
1. Write the read protocol: what a session reads at start, in what order, and where it stops.
   The rule is one index walked to at most two files, never a folder loaded wholesale.
2. Write the close protocol: what `/done` does to the memory model, in order. This is the
   contract section 2 implements, so it is written here and not invented there.
3. **Delegate the proof**: give an agent nothing but `docs/PROGRESS.md` and ask it to state the
   active work, the next action, and one decision already on file. It has this tree available but
   no conversation history, which is exactly the cold-start condition.
4. Record the result in `docs/decisions/`. If the agent cannot answer, the pointer is wrong and
   the fix lands in this session, not later.

**Files to write**
- `docs/FORMAT.md` (read + close protocols)
- `docs/decisions/memory-model.md`
- `docs/PROGRESS.md`

**Verify**
1. The cold agent names the active work file, the next action and one filed decision, correctly.
2. It reaches all three from the pointer without being told any path.
3. It reads at most four files getting there, counted from its own report.
4. `tools/index.py` still runs clean and idempotent after this session's writes.

**Output**: `feat: a cold session resumes from the pointer alone, and it is proved rather than claimed`
