---
title: Harness family
subject: open items that sit between coldstart-standard and the rest of the harness family
topic: family
updated: 2026-08-21
---

# Fixes — harness family

Open items only. A shipped item's block is deleted rather than struck through, per
[../FORMAT.md](../FORMAT.md) section 4. Git is the archive.

## The ColdStart parking card still says parked

**Subject**: the control tree records the program as parked, which the 2026-08-21 unparking contradicts

**Since**: 2026-08-21

**Closes when**: a superseding entry lands beside the parking card saying the program is unparked by owner's call.

**Ref**: /Users/macbook/coldstart/docs/deepseek-transfer/decisions/program-parked.md

## coldstart-minimal SPEC has not been amended to this memory model

**Subject**: confirmed stale: still stamped parked, still lists the warehouse under abandons, has no three-index model

**Since**: 2026-08-21

**Closes when**: minimal's SPEC either carries its version of this model or records that it diverges on purpose.

**Ref**: ../coldstart-minimal/SPEC.md

**Tag**: later

## CHARTER.md is stale on the unparking

**Subject**: the charter still carries the 2026-08-19 parked banner and gates the downstream harnesses on a score

**Since**: 2026-08-21

**Closes when**: the charter records the unparking and restates the build-order gate in score-free terms.

**Ref**: ../../CHARTER.md

## The ColdStart control tree has not moved into claude-harnesses/

**Subject**: the charter says the tree moves once the 7-day soak closes on 2026-08-22; until then a symlink stands

**Since**: 2026-08-21

**Closes when**: the move happens and the charter's layout section is updated to match.

**Ref**: ../../CHARTER.md

**Tag**: later

## The v1 install claims any tree holding `docs/PROGRESS.md`

**Subject**: v1's floor governed this repo against a pointer schema it cannot read, and the workaround leans on a foreign error path

**Since**: 2026-08-21

**Closes when**: this harness's floor scopes itself to trees it serves, and `.coldstart-init` is no longer load-bearing here

**Ref**: docs/work/04-safety-floor.md

## coldstart-coding's unblock condition cannot be met as written

**Subject**: coding gates itself on standard having an eval score, and the comparator that would supply one was dropped unbuilt

**Since**: 2026-08-21

**Closes when**: coding's SPEC restates its gate in terms this family can actually satisfy, the way standard's success condition was

**Ref**: ../coldstart-coding/SPEC.md

The same set-aside that unparked `standard` applies here, and it should be written down rather
than assumed: `coding` starts without a score, because the extrinsic tier never existed. What is
still owed is the honest half of the trade, which is that `coding` has to be judged by whether its
own layer is separable and enforced rather than by beating `standard` on a number.
