---
name: done
description: Close the active session in this harness — run its own Verify list, file the outcome into work/decisions/fixes, regenerate the three indexes, rewrite the seven-field pointer whole, and commit. Refuses to close over a red verify.
---

# done — the close

`docs/FORMAT.md` section 9 is the contract; this skill is its implementation, and the two do not
restate each other by accident. Run the steps in order. Nothing here is optional, and nothing here
is a judgement call except step 2's filing and step 6's nudge.

You are the single writer of the pointer and the single caller of `tools/index.py`. Both facts are
what let a reader trust an index line without opening the file behind it, so neither is delegated,
batched, or done twice in one close.

## 1. Verify before writing

Walk the active session's own **Verify** list, item by item, and report each one: passed, could not
run, or failed. Run the checks; do not reason about whether they would pass.

**Red or paused does not close.** On any failed or unrun check: say what failed, leave the session
`Status` as it is, leave the pointer pointing at this session, and stop. Do not fix the check by
weakening it, and do not close the session and file the failure as a fix. A session that cannot
pass its own verify list is not finished, and the pointer is the only thing standing between the
next cold session and that fact.

A pause is not a close either. When the work stops for the day mid-session, say what is left and
leave the session open.

## 2. Update the content files, not the indexes

- The session's `## Session N` block in its work file goes to `**Status**: done` and gains a
  `**Closed**: YYYY-MM-DD` line beneath it.
- New decisions are filed into the **existing** topic file under `docs/decisions/` that fits; a new
  topic file only when none does. One `##` heading per decision, with a `**Decided**:` date.
  Superseding never deletes: the old heading gains `(superseded YYYY-MM-DD)` and one line saying
  what replaced it.
- New known-open items are added to `docs/fixes/` with `Subject` / `Since` / `Closes when`, and
  anything shipped this session has its `##` block deleted from there. Presence is openness; there
  is no status field and no done section.
- An index file (`PROGRESS.md`'s generated region, `DECISIONS.md`, `FIXES.md`) is never hand-edited
  here. Every one-line field is written to be read out of context, at most 120 characters, no
  trailing full stop, because the generator carries it verbatim.

## 3. Regenerate

    python tools/index.py

It rewrites `PROGRESS.md`'s queue and log, `DECISIONS.md` and `FIXES.md` from the folders, and it
leaves the pointer front matter byte-identical.

## 4. Assert the regeneration is a no-op

    python tools/index.py --check

Exit 0 or the close does not continue. A non-zero exit means step 2 wrote something the format does
not describe: it names the file, and you fix the file. Never hand-edit a generated region to make
the check pass, and never commit past it.

## 5. Write the pointer, whole

Compose all seven fields from scratch in the front matter of `docs/PROGRESS.md`. Nothing is
appended, nothing is carried over unexamined, and a field that would repeat last close's value is
re-derived rather than left.

| Field | Cap | What you write |
|---|---|---|
| `active_work` | one repo-relative path | the work file the next session continues, or empty between sections |
| `mode` | `build` \| `prep` | see the rule below |
| `next_action` | <=120 chars, one line | the next concrete step, startable cold without reading anything else |
| `blockers` | list of one-liners | `[]` when clear. Non-empty reads as "do not start; resolve or re-scope" |
| `reading` | list of repo-relative paths | the next session's read ceiling, not a suggestion |
| `updated` | `YYYY-MM-DD` | today |
| `resume_note` | quoted, one sentence, <=160 chars | the line a colleague would say out loud that no field above carries |

There is no history field and no eighth field. If something does not fit one of the seven, it
belongs in the active work file, not on the hot path. Truncate at the cap and say that you did.

**The close never writes a restrictive `mode`.** `mode` says what the *running* session may do, and
a safety floor reads it the instant it lands on disk. Writing `mode: prep` here denies the close its
own remaining steps, because step 7 is a write. Leave `build`, or omit it, which resolves the same
way. The next session declares its own mode when it starts.

## 6. Nudge on clustering, do not gate

If a topic file under `decisions/` or `fixes/` has grown past roughly 200 lines, say so and propose
the split by sub-topic. Then continue. Nothing blocks on it: a clustering rule with teeth becomes a
filing ritual, which is the thing this model replaces.

## 7. Commit

Stage the changed files **by name** — never `git add -A` or `git add .`. The session's declared
`**Output**:` line is the commit message, unchanged. Git is the history, which is what lets the
pointer carry none.
