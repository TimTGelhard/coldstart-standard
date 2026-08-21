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
