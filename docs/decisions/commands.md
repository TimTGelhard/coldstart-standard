---
title: Commands
subject: three commands, the payload layout they ship in, and the close's rules: refuse on red, never write a restrictive mode
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

## The repo root mirrors the payload, and only the installer knows the mapping

**Decided**: 2026-08-21

`commands/`, `skills/`, `agents/`, `hooks/` and `chapters/` sit at the repo root beside `tools/`.
Section 6's installer maps them into `.claude/` and `.coldstart/`.

The source tree therefore does not look like the installed tree, on purpose. The alternative is a
root that already looks installed, which puts the mapping in two places and makes a wrong copy the
default failure. One place owns it, and that place is the installer.

## The three lifecycle skills are counted on top of the SPEC census, not inside it

**Decided**: 2026-08-21

`/coldstart`, `/prep` and `/done` are separate skills from section 3's four routers, so resident
cost grows by three skill descriptions over what the SPEC census predicted. Each description is
written to a ~250 B target, and section 7 reports the measured number rather than the predicted
one. An estimate that is never checked is how the previous harness lost its floor.

## /prep may write the pointer's `mode` field, and nothing else

**Decided**: 2026-08-21

`FORMAT.md` section 1 rule 1 says `/done` is the pointer's single writer. This is the one named
exception: a planning pass sets `mode: prep` at its start and touches none of the other six fields.

The exception is narrow because the reason is narrow — the safety floor reads `mode` off disk while
the session runs, so a planning session has to be able to declare itself before it does anything.
Session 3 writes the exception into `FORMAT.md` itself rather than leaving this file as the only
place the contradiction is resolved.

## A red verify does not close, and the close never writes a restrictive mode

**Decided**: 2026-08-21

Two rules that could have been left implicit in `FORMAT.md` section 9 and are instead written into
`skills/done/SKILL.md` where the close can read them without opening a second file.

A failed or unrun check leaves the session's `Status` untouched and the pointer still pointing at
it. The close does not fix the check, and does not close-and-file-the-failure-as-a-fix: the pointer
is the only thing standing between the next cold session and the fact that the work is unfinished.

And the close writes `mode: build` or omits it. `mode` constrains the *running* session, and the
close's own last step is a commit, so a close that writes `mode: prep` denies itself its remaining
steps. The previous harness found this by locking its own tree before the commit and unblocking the
last two steps by hand.

## The command surface does not count against the four-file bound

**Decided**: 2026-08-21

The bound is four files under `docs/`: the pointer's file, the active work file, one index, and one
file that index names. The wrapper and the skill are the command being invoked, not tree reads, so
they sit outside it.

Two cold agents at session 2 derived this independently and unprompted, which is the signal it
belonged in the skill rather than in each reader's head. The distinction is not bookkeeping: the two
command reads are fixed, while the tree reads are what would grow with the project, and a bound that
mixed them would stop measuring the thing it exists to measure.

## The pointer is read by extraction, never by paging the top of the file

**Decided**: 2026-08-21

`sed -n '/^---$/,/^---$/p' docs/PROGRESS.md`, not `head -40`. Paging pulls the generated queue in
behind the front matter and silently turns the pointer read into an index read, which defeats step
1's own "and nothing else in that file yet".

Both cold runs at session 2 did exactly that before the skill named the extraction, and the run
after the amendment used it unprompted. The lesson generalises past this line: a step that cannot be
followed literally is a defect in the step, not in the reader, and the fix is to write the command
rather than to ask for more care.

## The four-file bound survives being wrapped in a command

**Decided**: 2026-08-21

Section 1 session 3 measured the bound on the bare files. Section 2 session 2 re-measured it through
`/coldstart` with three cold agents: four tree files for the full walk, three when the escape hatch
was used, one when a planted blocker stopped the resume.

Two properties held that were claimed rather than tested before. A resume can answer a question from
an index line without opening the file behind it, because the generator carries source fields
verbatim. And the `reading` list is a ceiling rather than a checklist: one run declined two files on
it as unnecessary, which is the correct reading and the less likely drift.

## /done stays the single caller of tools/index.py, and the queue is stale between prep and close

**Decided**: 2026-08-21

The open call from section 2's plan: whether `/prep` may regenerate the indexes when it writes a
new work file, so the new sessions appear in the queue immediately.

It may not. `/done` remains the only caller, and the queue in `PROGRESS.md` stays stale from the
moment a work file is written until the planning session closes — minutes later, by the same
operator, in the same sitting. The cost is a short window where the queue is behind its folder.
The alternative cost is permanent: two callers are two things that can disagree with the folders,
and the property that lets a reader trust an index line without opening the file behind it is that
exactly one writer produced it.

The same reasoning is why `/prep` writes `mode` and no other pointer field. A second writer is
admitted only where the floor forces it, and then only over the one field the floor reads.

## A prep pass has no shell, and `/prep` is written to that rather than around it

**Decided**: 2026-08-21

`/prep`'s first step writes `mode: prep`, and the safety floor reads that field the instant it
lands. From then on the floor denies any shell it cannot prove read-only — including
`python tools/index.py --check`, which writes nothing but cannot say so from its command string.

The skill as first written told the pass to run that check before handing back, and the floor
refused it on the first real firing. The step was wrong, not the floor: a floor that took a tool's
word for its own read-onlyness is a floor anything can talk past.

So the pass writes plan files with an editor and calls no tool. The work file is checked by eye
against the six things the generator is strict about, and by the close minutes later — `/done`
regenerates before it writes anything, so a malformed work file stops that close with a
`FormatError` naming the file, before the pointer moves. The check moved from the pass that cannot
run it to the close that must.

One consequence is written into the skill because an abandoned pass hits it: a `/prep` that stops
without closing puts `mode` back to `build` with an editor, because by then a `sed` is denied too.
