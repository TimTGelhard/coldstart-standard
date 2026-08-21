---
title: Commands
subject: the three commands one skill deep each, and the proof that the lifecycle loop closes itself unattended
topic: commands
updated: 2026-08-21
---

# Section 2 — commands

> The section plan. Four sessions. Written at `/prep`, 2026-08-21.
> Goal: `/coldstart`, `/prep` and `/done` exist as real files, each one skill deep, and the loop
> they form runs end to end on this tree.

**Done when**: a session on this tree can be opened with `/coldstart` and no prose, planned with
`/prep`, and closed with `/done`, with `python tools/index.py --check` clean at every boundary and
a dated firing artifact for each of the three skills.

### Settled at plan time

Three calls the user made before this plan was written. They are recorded here so the sessions
build to them rather than re-opening them, and session 1 files them into `decisions/commands.md`
at its close.

1. **Payload layout**: the repo root mirrors the payload. `commands/`, `skills/`, `agents/`,
   `hooks/` and `chapters/` sit at the root beside the existing `tools/`, and section 6's
   installer maps them into `.claude/` and `.coldstart/`. The source tree does not look like the
   installed tree, and the mapping lives in one place: the installer.
2. **Skill count**: the three lifecycle skills are separate from section 3's 4 routers. Resident
   cost therefore grows by three skill descriptions over the SPEC census, and section 7 reports
   the real number rather than the predicted one. Each description is written to a ~250 B target.
3. **Mode writer**: `/prep` may write the pointer's `mode` field and nothing else. This is a
   named exception to `FORMAT.md`'s one-writer rule, and session 3 writes the exception into
   `FORMAT.md` rather than leaving it as a contradiction for a later reader to find.

### Open, and owed a human answer

- Whether `/prep` may also call `tools/index.py` when it writes a new work file, or whether the
  queue stays stale until the prep session's own `/done`. Session 3 hits this and must not
  silently pick. Recommendation: it stays stale, because the prep session closes with `/done`
  minutes later and a second caller of the generator is a second thing that can disagree.

---

## Session 1 — `/done`, the close

**Status**: done

**Closed**: 2026-08-21

**Goal**: the close protocol stops being prose in `FORMAT.md` and becomes the command that every
other session in this project ends with

**Files to read**
- `docs/FORMAT.md` (sections 1, 2, 4 and 9 — the pointer, the content-file grammar, the item
  grammar and the close protocol)
- `docs/PROGRESS.md`
- `/Users/macbook/coldstart/skills/core/coldstart/close.md` (ColdStart's close — carry the
  decision, leave the implementation)

**Build steps**
1. `commands/done.md`: the wrapper. Name, one-line description, and a pointer at the skill.
   Nothing else, because the wrapper is resident and the skill is not.
2. `skills/done/SKILL.md`: the whole close, in the order `FORMAT.md` section 9 fixes it — verify
   first, update content files, regenerate, assert the regeneration is a no-op, write the pointer
   whole, nudge on clustering, commit. The skill carries the seven pointer fields and their caps
   inline, so the close never needs a second file open to write a valid pointer.
3. Write the red path explicitly: a red or paused verify does not close. The session stays open,
   the pointer keeps pointing at it, and the skill says what failed.
4. Write the mode rule explicitly: the close never writes a restrictive `mode`. This is the thing
   section 3 of the previous harness discovered by locking its own tree before the commit.
5. Capture the firing artifact: run `/done` for real against a scratch session block in this
   tree and keep the transcript under `docs/work/artifacts/`.

**Files to write**
- `commands/done.md`
- `skills/done/SKILL.md`
- `docs/decisions/commands.md` (the three plan-time calls above, filed at close)
- `docs/work/artifacts/02-s1-done.md`

**Verify**
1. Run `/done` against a scratch session block: its `Status` flips to `done` with a `Closed` date,
   the three indexes regenerate, and `python tools/index.py --check` exits 0.
2. The pointer after that close carries all seven fields, `mode` is not `prep`, and no field holds
   a placeholder or a value copied from the previous close.
3. Red verify does not close: plant a failing check in the scratch session's `Verify` list, run
   `/done`, and confirm `Status` is unchanged and the pointer still names that session.
4. The firing artifact exists, is dated, and shows the skill running rather than the file existing.

**Output**: `feat: the close protocol is a command, and a red verify refuses to close`

---

## Session 2 — `/coldstart`, the resume

**Status**: pending

**Goal**: the read protocol becomes the command that opens every session, and the four-file bound
is re-measured through it rather than by hand

**Files to read**
- `docs/FORMAT.md` (section 8, the read protocol)
- `docs/PROGRESS.md`
- `docs/decisions/memory-model.md` (the cold-resume measurement from section 1 session 3)

**Build steps**
1. `commands/coldstart.md`: the wrapper, same shape as session 1's.
2. `skills/coldstart/SKILL.md`: the four-step walk — pointer, `active_work`, the `reading` list,
   stop — plus the one-index-at-most-two-files escape hatch and the never-wholesale rule.
3. Write the blocker path: a non-empty `blockers` stops the resume. Report and ask, do not begin.
4. Write the ceiling rule so it is audible: a read outside `reading` is named out loud when it
   happens, not confessed afterwards.
5. **Delegate the proof**: give an agent this tree and the single instruction to run `/coldstart`,
   with no conversation history and no paths. Take back what it named and how many files it read.
6. Capture the firing artifact from that run.

**Files to write**
- `commands/coldstart.md`
- `skills/coldstart/SKILL.md`
- `docs/work/artifacts/02-s2-coldstart.md`

**Verify**
1. The cold agent names the active work file, the next action and the blocker state correctly,
   from `/coldstart` alone.
2. It reads at most four files getting there, counted from its own report.
3. With a blocker planted in the pointer, a second cold run reports it and does not start work.
4. With a file deliberately outside the `reading` list needed, the agent names the overrun rather
   than reading silently.

**Output**: `feat: the resume is a command, and the four-file bound survives going through it`

---

## Session 3 — `/prep`, the plan

**Status**: pending

**Goal**: planning stops being borrowed from ColdStart and becomes this harness's own one-skill
pass, writing work files that `tools/index.py` accepts

**Files to read**
- `docs/FORMAT.md` (sections 2, 3, 4 — the front matter, the naming, the session item grammar)
- `docs/work/02-commands.md` (this file, as the worked example of the output shape)
- `SPEC.md` (the feature ledger's planning-pass row)

**Build steps**
1. `commands/prep.md`: the wrapper.
2. `skills/prep/SKILL.md`: the pass — declare mode, scope the section, break it into 2-5 sessions,
   write the work file, hand back. The work-shape catalog rides inside it as a compressed table,
   not as a chapter tree.
3. `templates/SESSION.md`: the session entry scaffold, so the skill fills a shape rather than
   recomposing one each time.
4. Wire the mode exception: `/prep` sets `mode: prep` at start and touches no other pointer field.
   Amend `FORMAT.md` section 1 rule 1 to name the exception in the same session that creates it.
5. Settle the open call above (whether `/prep` may call `tools/index.py`) and record the answer in
   `decisions/commands.md`.
6. Write the no-generic-verify rule into the skill: a session entry whose verify list says "test
   it works" is not finished, because that is what turns `/done` into a rubber stamp.
7. Capture the firing artifact.

**Files to write**
- `commands/prep.md`
- `skills/prep/SKILL.md`
- `templates/SESSION.md`
- `docs/FORMAT.md` (the mode exception)
- `docs/decisions/commands.md`
- `docs/work/artifacts/02-s3-prep.md`

**Verify**
1. `/prep` on a named scratch section writes `docs/work/NN-<slug>.md` that `python tools/index.py`
   accepts with no error: front matter complete, `topic` equal to the stem, item grammar parsed.
2. The file it writes holds 2-5 sessions, each under the 100-line entry cap, each with a verify
   list naming concrete checks rather than a generic one.
3. `mode: prep` lands on the pointer at start, the other six fields are byte-identical afterwards,
   and the tree is back to `build` once the session closes.
4. The scratch section's rows appear in the `PROGRESS.md` queue after the close, and
   `python tools/index.py --check` exits 0.

**Output**: `feat: planning is one skill and one template, and it writes files the generator accepts`

---

## Session 4 — the loop closes on itself

**Status**: pending

**Goal**: prove the three commands are a loop rather than three files, by running a whole section
through them with no prose, and count what they cost resident

**Files to read**
- `docs/PROGRESS.md`
- `docs/work/02-commands.md`
- `SPEC.md` (the census target table)

**Build steps**
1. Pick a scratch section that is real but small, and run `/prep` on it with nothing but the
   section name.
2. **Delegate the run**: a fresh agent with no history opens `/coldstart`, does the one session,
   and closes with `/done`. The operator types three command names and no prose, which is the
   success condition the SPEC states.
3. Check the tree at every boundary: pointer valid, `index.py --check` clean, no index hand-edited.
4. Census what section 2 made resident: the three wrapper descriptions and the three skill
   descriptions, in bytes, against the SPEC's ~1,000 B wrapper line. Record the number even when
   it is over, because an estimate that is never checked is how the previous harness lost its
   floor.
5. File the result in `decisions/commands.md`, and anything that bit into `fixes/`.

**Files to write**
- `docs/decisions/commands.md`
- `docs/fixes/` (whatever the run surfaces)
- `docs/work/artifacts/02-s4-loop.md`

**Verify**
1. The whole scratch section runs `/prep` to `/coldstart` to `/done` with no prose from the
   operator beyond the section name.
2. `python tools/index.py --check` exits 0 after each of the three commands.
3. The pointer is valid and non-placeholder at each boundary, and its seven fields never disagree
   with the file they point at.
4. The resident byte count for section 2's surface is measured and written down, with the delta
   against the SPEC census stated either way.

**Output**: `feat: the lifecycle loop runs a section end to end with three command names and no prose`
