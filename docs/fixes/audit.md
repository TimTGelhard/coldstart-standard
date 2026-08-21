---
title: Audit
subject: what an outside read found open on 2026-08-21: no measured floor, a borrowed hook, and proof that is self-report
topic: audit
updated: 2026-08-21
---

# Audit — the 2026-08-21 outside read

Findings from a read of this tree made from outside it, while scoping `coldstart-coding`. Nothing
here was found by a session that was building at the time, which is why it is filed as a queue
rather than as a decision. Each item is open; a shipped one has its block deleted.

## The harness has no measured floor

**Subject**: the family contract makes MEASURE.md mandatory and this tree has none, so every byte claim is still an estimate

**Since**: 2026-08-21

**Closes when**: MEASURE.md exists and carries a census of the rendered surface with the command that produced it

**Ref**: ../../CHARTER.md

The census is section 7 and it is gated on the resident surface existing at all, so this is not
late. It is recorded because two downstream things already lean on a number that does not exist:
the SPEC's ~9,340 B target, and `coldstart-coding`'s claim that its specialization layer costs
less than the general harness it sits on.

**Tag**: later

## The safety floor in this tree is borrowed

**Subject**: hooks/ is written but untracked and registered nowhere, so the floor that actually fires here is a neighbour's

**Since**: 2026-08-21

**Closes when**: hooks/ is committed, registered in this repo's own settings, and has a dated firing artifact per category

The prep skill tells the operator that a shell it cannot prove read-only is denied for the rest of
the pass. `hooks/pre-tool-floor.sh` and `hooks/floor.py` exist on disk and read well, 398 lines
between them, and git has never seen either. There is no `.claude/settings.json` in this tree, so
nothing registers them: the refusal that governed the last planning pass came from the global
ColdStart v1 install. The harness currently describes an enforcement it does not carry, which is
the exact failure the charter names, proved by reading rather than by firing. Related and already
filed: `fixes/lifecycle.md`, the escape hatch that names a tool this tree does not have.

## install.sh evicts entries from the global Claude surface

**Subject**: the installer moves ~/.claude commands and skills into backup directories, so a project script mutates the machine

**Since**: 2026-08-21

**Closes when**: the eviction is gated behind a dry-run and an explicit confirmation, or named as machine-wide in the installer's output

The eviction is correct in intent: a user-level command of the same name shadows the project copy,
and that was measured rather than assumed. The hazard is the blast radius. On this machine
`~/.claude` is ColdStart v1's live wiring and it is mid-soak, so running the installer against the
wrong tree moves files the operator is relying on that day. The reverse `mv` is printed, which is
the mitigation, not the fix.

## The payload is installed by copy with nothing checking for drift

**Subject**: commands/ and skills/ exist twice, at the root and under .claude/, and no check compares them

**Since**: 2026-08-21

**Closes when**: verify.py carries a check that the installed copy equals the source, or the check is ruled out in writing

Copy rather than symlink is a decision on file and it is a good one: the installed copy has to be a
different file or a passing run stops proving the install works. The consequence is a second copy
that can be edited, and section 5 is where the check for that belongs.

## Every proof in this tree is written by the session that produced it

**Subject**: the loop is evidenced by markdown artifacts authored by the run they describe, which is a self-report

**Since**: 2026-08-21

**Closes when**: at least one lifecycle claim is re-checked by something that is not the session that made it

The charter's standing rule is to verify the world, not the self-report. `docs/work/artifacts/`
holds the current evidence and it is a session's own account of itself. The cheapest honest fix is
an external re-read: a fresh agent given only the tree and one instruction, reporting what it did,
the way section 2 session 4's cold run was already done once.

**Tag**: later

## The committed indexes disagree with their folders at HEAD

**Subject**: index.py --check exits 1 on a clean checkout; the queue is missing all of section 4 and section 6

**Since**: 2026-08-21

**Closes when**: a /done regenerates the three indexes and `python tools/index.py --check` exits 0 on a clean tree

**Ref**: tools/index.py

Measured on a clean checkout with no working changes. `docs/PROGRESS.md` carries no rows for
sessions 4.1 to 4.3 or 6.1 to 6.4, and `docs/DECISIONS.md` reports the install topic as 3 entries
where the folder holds 7. Section 6 session 1 shipped `install.sh` and its work file still reads
`pending`, so the last piece of work was built without being closed.

This is not a defect in the generator, which produces the right answer the moment it is run. It is
the model's one exposed assumption: an index cannot go stale only while `/done` is the thing that
ends every session. A close skipped is a stale index, and nothing in the tree says so until
somebody runs the check by hand. Worth deciding whether section 5's verify carries it.

## Two sessions' worth of work sits outside the close protocol

**Subject**: install.sh shipped with its session still pending and hooks/ is untracked, so the record understates the tree

**Since**: 2026-08-21

**Closes when**: section 6 session 1 and section 4 session 1 are either closed through /done or explicitly marked unfinished

**Ref**: docs/PROGRESS.md

The pointer says the next thing is section 2 session 4. What is actually on disk is a working
installer (committed, session still `pending`) and a written safety floor (not committed at all).
A cold session that trusts the pointer will plan work that already exists.

This is the same root as the stale-index item above and it is worth stating separately, because the
cost is different. A stale index is a file that disagrees with a folder. This is the record
disagreeing with the tree, which is the one thing the memory model exists to prevent.

## The floor's secrets category outgrew the plan that describes it

**Subject**: the floor now refuses to stage a dotenv file as well as read one, and section 4's plan does not mention it

**Since**: 2026-08-21

**Closes when**: section 4 session 1's build steps and verify list name the commit rule, and install writes the ignore lines

**Ref**: docs/work/artifacts/04-s1-secrets-commit.md

Added and proved by firing on 2026-08-21, ahead of the session that plans it. Two consequences to
close rather than carry. The section 4 plan describes three deny categories and the secrets one is
now two rules, so its fixture list is short by the commit cases. And the durable half of this
protection is an ignore-list line rather than a hook, because a hook can be unregistered while an
ignore rule travels with the repo: `coldstart-minimal`'s installer writes those lines and this
harness's does not, which is a gap that belongs to section 6 session 2.
