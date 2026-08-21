---
title: Section 6 session 1 — the minimal map, firing artifact
subject: what install.sh produced, and the measured collision that mapping into .claude/ did not fix on its own
topic: 06-s1-map
updated: 2026-08-21
---

# 06 s1 — the minimal map

Captured 2026-08-21, in the session that ran `/coldstart` on this tree.

## The red measurement, taken before anything was changed

`.claude/` was already correctly installed: three wrappers under `.claude/commands/`, three skill
directories under `.claude/skills/`. The operator typed `/coldstart` in this repo, and the payload
that loaded was:

    Base directory for this skill: /Users/macbook/.claude/skills/coldstart

That is ColdStart v1's dispatcher, read from outside this repo. The session only reached this
harness's own walk by opening `.claude/skills/coldstart/SKILL.md` by hand, which is exactly the
prose `SPEC.md`'s success condition forbids. The host's skill list carried one `coldstart`, and its
description was v1's.

Two things were narrowed from that. Mapping into `.claude/` is necessary and not sufficient,
because a user-level registration of the same name wins. And the surface that won was the *skill*,
not the command stub, so claiming `~/.claude/commands/` alone would have left the collision.

## What changed

`install.sh` gained a name-claiming step over both surfaces. Colliding entries are moved, never
deleted, into `~/.claude/commands-displaced-by-coldstart-standard/` and
`~/.claude/skills-displaced-by-coldstart-standard/`, with the reverse `mv` printed on every run
that displaces something. `--keep-user-commands` skips the step and warns instead. Recorded in
`decisions/install.md`.

Displaced on the first claiming run: `coldstart.md`, `prep.md`, `done.md` from the user commands
directory, and the `coldstart` skill symlink from the user skills directory.

## Verify

| # | Item | Result |
|---|---|---|
| 1 | `bash install.sh` exits 0; three files in `.claude/commands/`, three dirs in `.claude/skills/` | green |
| 2 | A second run exits 0 and `git status --short` reports nothing new | green |
| 3 | A fresh session's `/coldstart` loads this harness's skill, not v1's | **open** |
| 4 | Negative case: with `.claude/` deleted, `/coldstart` falls back to v1 | **stale** |

Item 3 cannot be closed from inside the session that made the change: the host registers commands
and skills at session start, so this session still holds the pre-change registry. It needs a new
terminal in this tree, typing `/coldstart`, and the artifact updated with the base directory that
prints. Until then session 1 stays `pending`.

Item 4 was written before the collision was understood. It assumed v1 was the fallback; v1's
`coldstart` skill is now displaced, so deleting `.claude/` leaves no `coldstart` at all rather than
v1's. The item should be rewritten to assert that, or dropped, at the session that closes this one.
