# Firing artifact — `/prep`, section 2 session 3

**Date**: 2026-08-21
**Skill under test**: `skills/prep/SKILL.md`, driven from `commands/prep.md`
**Method**: the pass was run in-session against a real section — section 3, `resident-surface` —
immediately after the skill was written, following its own steps literally rather than in spirit.
The section is real rather than throwaway, so its output stays in the tree and the queue rows it
produces are the queue rows the verify asks for.

The artifact is the record that the skill *ran*, and of the one place where running it literally
refused.

---

## The run

**Step 1, declare the mode.** The skill's own `sed` line, then its own `git diff -U0` proof:

    @@ -3 +3 @@ active_work: docs/work/02-commands.md
    -mode: build
    +mode: prep

One line changed and six fields untouched, which is the narrow exception behaving as narrowly as
`FORMAT.md` rule 1 now says it does.

**Steps 2 to 4.** Section 3 scoped to one sentence, shape declared Build, broken into four sessions
that break by layer with the last one a measurement rather than a polish. Three plan-time calls
recorded with their reasons; two open calls written into the block that names the session that must
ask, rather than picked.

**Step 5, write the file.** `docs/work/03-resident-surface.md`: 193 lines, four sessions of 36-39
lines each against the 100-line cap, `subject` 111 bytes against the 120-byte cap.

**Step 6, hand back.** The generator was not called. The queue stayed stale until this session's
close, which is the decision the open call from section 2's plan settled.

---

## What the run found: the floor denies the skill's own check

The skill as first written told the pass to run `python tools/index.py --check` before handing
back, to confirm the new work file parses. Run literally, that was **denied by the safety floor**:

    ColdStart mode contract -- this session declared `mode: prep` on the pointer, and
    `python3 tools/index.py --check` is not provably read-only. A prep session reads freely
    and writes plan files only, so the shell is denied unless the whole command is a known read.

The refusal is correct. `--check` writes nothing, but the floor cannot prove that from the command
string, and a floor that took the tool's word for it would be a floor that any tool could talk past.
What was wrong was the step, not the floor.

Two consequences, both now written into the skill:

1. Step 5 no longer calls the generator. The work file is checked by eye against the six things the
   generator is strict about, and by `/done` minutes later — the close regenerates before it writes
   anything, so a malformed work file stops the close with a `FormatError` naming the file, before
   the pointer moves.
2. Step 1 now says the floor is live for the rest of the pass, and that an abandoned pass puts
   `mode` back with an editor rather than a `sed`, because the shell is denied by then.

This is the general lesson section 2 keeps re-learning: a step that cannot be followed literally is
a defect in the step. Session 2 found it with `head -40` on the pointer; session 3 found it here.

## The escape hatch the message names does not exist here

The floor's message ends *"Declare it with `python tools/done.py --set-mode build`."* That tool
belongs to the previous harness. This tree's close is a skill, and `tools/` holds `index.py` alone,
so the message points a stuck operator at a file that is not there. Filed in `docs/fixes/`.

## Verify, as run

1. **The generator accepts the file.** `python tools/index.py --check` after the pass, in `build`
   mode: no `FormatError`, exit 1 on staleness alone — `docs/PROGRESS.md is out of date`,
   `docs/DECISIONS.md is out of date`. Staleness is the expected state before the close; a format
   error would have named the file.
2. **Shape.** Four sessions, 36-39 lines each, every verify list naming a command with an exit code
   or a file plus the value it must hold. Grep for the generic forms (`test it works`,
   `works correctly`, `is well-formed`, `looks right`) returns nothing.
3. **The pointer.** `mode: prep` landed alone at the start; after the run was unwound,
   `git diff docs/PROGRESS.md` was empty against `HEAD` — the other six fields were never touched.
   The tree is back in `build`, and the close rewrites all seven fields from scratch.
4. **The queue.** Section 3's four rows enter `PROGRESS.md` at this session's close, through the
   close's own regeneration, and `python tools/index.py --check` exits 0 there.
