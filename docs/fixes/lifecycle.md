---
title: Lifecycle loop
subject: open items in the close and resume loop that sections 2 and 4 have to resolve together
topic: lifecycle
updated: 2026-08-21
---

# Fixes — lifecycle loop

Open items only. A shipped item's block is deleted rather than struck through, per
[../FORMAT.md](../FORMAT.md) section 4. Git is the archive.

## The close has no exemption from the mode floor it writes

**Subject**: the safety floor reads the pointer's mode the moment it lands, so a close can deny its own commit

**Since**: 2026-08-21

**Closes when**: `/done` writes the pointer and commits as one action the floor treats as the close, whatever mode the pointer carries

**Ref**: docs/FORMAT.md

**Tag**: later

## Testing the blocker path needs a pointer writer that is not `/done`

**Subject**: the resume's refusal path can only be exercised by planting a blocker the close has no reason to write

**Since**: 2026-08-21

**Closes when**: the blocker path is exercised without a second pointer writer, or the plant is a named FORMAT.md exception

**Ref**: docs/work/artifacts/02-s2-coldstart.md

**Tag**: later

## The floor's escape hatch names a tool this harness does not have

**Subject**: the mode-contract refusal tells the operator to run tools/done.py --set-mode build, and tools/ holds index.py alone

**Since**: 2026-08-21

**Closes when**: this tree ships a mode writer the message can name, or the message points at the editor path `/prep` documents

**Ref**: docs/work/artifacts/02-s3-prep.md

**Tag**: later

## `/prep`'s output is not resumable until an unrelated session closes

**Subject**: a freshly planned section is invisible to a cold resume: only `/done` repoints the pointer and regenerates the queue

**Since**: 2026-08-21

**Closes when**: a cold `/coldstart` run straight after `/prep` lands on the newly planned session with no intervening close

**Ref**: docs/work/02-commands.md

## The three commands are registered nowhere, so they cannot be typed

**Subject**: `commands/` and `skills/` sit unmapped at the repo root, so typing `/coldstart` here loads v1's skill instead

**Since**: 2026-08-21

**Closes when**: the installer maps the payload into `.claude/` and section 2 session 4's verify runs against installed commands

**Ref**: docs/work/02-commands.md

