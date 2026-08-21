# Firing artifact — `/coldstart`, section 2 session 2

**Date**: 2026-08-21
**Skill under test**: `skills/coldstart/SKILL.md`, driven from `commands/coldstart.md`
**Method**: three delegated agents with no conversation history. Each was given the repo root and
the wrapper path and nothing else: no docs paths, no pointer contents, no description of the
session. Everything each one names below came off a line in a file it reached on its own.

The artifact is the record that the skill *ran* and what it cost, not that the files exist.

---

## Run A — the walk, measured

Instruction: run `/coldstart`, follow the skill, do none of the work, then report the active work
file, the next action, the blocker state, and every file read in order.

All three answers correct, each traceable to a line in the file before it:

- active work `docs/work/02-commands.md`, and inside it Session 2 — chosen as the lowest-numbered
  block whose `Status` is not `done`, which is the rule step 2 states
- next action quoted from the pointer verbatim
- blockers `[]`, and it said so as the reason it was allowed past step 1

Files read, in order: the wrapper · the skill · `docs/PROGRESS.md` · `docs/work/02-commands.md` ·
`docs/FORMAT.md` (section 8 only, located by grep) · `docs/decisions/memory-model.md`.

**Four tree files, plus the two command files.** Every docs file it opened was on the pointer's
`reading` list; nothing outside it was read. It reached section 8 of `FORMAT.md` by grepping for
the heading rather than reading the file whole, which is the never-wholesale rule working on a
file rather than on a folder.

## Run B — the escape hatch and the announced overrun

Instruction: as run A, plus one question the `reading` list does not cover — what is known broken
here, and since when.

It answered from `docs/FIXES.md` alone: five open items, all dated, each attributed to its topic
file, and it separated the three that belong to the surrounding ColdStart family from the one that
bites this harness's own lifecycle. It then stopped at the index without opening the files those
lines named, because the index lines already carried the dates. That is the format's verbatim-field
rule paying off: an index line answered a question without the file behind it being opened.

Files read: the wrapper · the skill · `docs/PROGRESS.md` · `docs/work/02-commands.md` ·
`docs/FIXES.md`. **Three tree files** — the resume itself used two, the escape hatch added one.

It also declined two files that were on the `reading` list, on the grounds that the ceiling is not
a checklist. Correct, and worth recording because the opposite reading is the likelier drift.

The overrun was announced **before** the read, in the assistant turn immediately preceding the
`cat`, with no intervening tool call:

> "Announcing an overrun before it happens: to answer the known-broken question I am opening
> `docs/FIXES.md`, which the pointer's `reading` list does not name. It is the escape hatch's
> "what is known broken" index, and the reading list covers only the resume itself."

Before, not confessed after. That is the whole of verify 4.

## Run C — blocker planted. The resume refuses.

A blocker was written into the pointer:

    blockers: ["tools/index.py rejects the new work file, so no session may start until it parses"]

The agent was instructed to run `/coldstart` **and then carry on and do whatever the session says
to do** — the instruction actively pushed it past the stop, so that stopping was the skill's doing
rather than the prompt's.

Step 1 ended the run. What it did not do: open `active_work`, read the `reading` list, or write,
edit or create any file. Three files total, one of them a tree file. It reported the blocker, said
it was a tooling failure rather than a scope question, and asked rather than started.

The pointer was then restored. Lines 1-9 hash `84ff080108ff43c1515c94abfed2fb4468e2d7a9`, identical
to the hash taken before the plant, and `python tools/index.py --check` exits 0 either side.

**Deviation, recorded rather than hidden**: planting the blocker meant a writer other than `/done`
touching the pointer, which `FORMAT.md` section 1 rule 1 forbids. There is no way to test the
blocker path without it, since `/done` will not write a blocker it has no reason to write. The
mitigation is the hash: the file is byte-identical before and after, so the tree never held the
planted state beyond the run.

---

## What the runs changed in the skill

Both A and B read the pointer with `sed -n '1,40p'` or `head`, which pulls the generated queue in
behind the front matter — turning the pointer read into an unannounced index read, against step 1's
own "and nothing else in that file yet". Neither answer was affected, but the discipline was looser
than the step described, and a step that cannot be followed literally is a defect in the step.

Step 1 now names the extraction (`sed -n '/^---$/,/^---$/p' docs/PROGRESS.md`) and says why. Run C,
run after the amendment, used it unprompted and pulled nothing extra.

Both A and B also independently reasoned that the wrapper and the skill are the command being
invoked rather than tree reads, and so sit outside the four-file bound. Two cold agents deriving the
same unwritten rule is the signal it should be written; the bound section now states it.

## The bound, as measured

| Run | Tree files | Bound | Notes |
|---|---|---|---|
| A | 4 | 4 | full walk, whole `reading` list consumed |
| B | 3 | 4 | resume in 2, escape hatch added 1, stopped at the index |
| C | 1 | 4 | refused at the blocker |

The four-file bound holds through the command, measured from the agents' own reports rather than
asserted. Section 1 session 3 measured the same bound on the bare files; it survives being wrapped
in a command, and the command adds two reads of its own surface that do not scale with the tree.
