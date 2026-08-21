---
title: Install
subject: in-project install rather than a parallel root, the .claude / .coldstart split, and the weight selector
topic: install
updated: 2026-08-21
---

# Decisions — install

## In-project install, not a parallel root

**Decided**: 2026-08-21

Everything lives inside the project. There is no parallel root and no `COLDSTART_ROOT`-style
environment variable to resolve.

ColdStart resolves every path from a shared root, which buys one copy across projects and costs a
resolution layer, an installer that writes two trees, and a live-root hazard that broke its own
hermetic test rig. `standard` takes the opposite trade: one copy per project, updated by
re-running install. The harness becomes a normal part of the repo, versioned with it, and
reversible by deleting two directories.

**The cost, stated rather than hidden**: N projects means N copies to update.

## `.coldstart/` is separate from `.claude/`

**Decided**: 2026-08-21

`.claude/` holds only what the host reads: `CLAUDE.md`, `settings.json`, `commands/`, `skills/`,
`agents/`. Everything the harness owns sits beside it in `.coldstart/`.

Two payoffs: uninstall is unambiguous, because it is deleting two directories, and a change in
what the host expects never lands inside harness files.

## The `--weight` selector is deferred to section 6, with one arm

**Decided**: 2026-08-21

`install.sh --weight minimal|standard` is specced as an add, because ColdStart has no preset
mechanism anywhere and every install therefore pays the full floor. It only becomes real once
`minimal` exists, so section 6 builds it with a single arm.

## Install copies, it does not symlink

**Decided**: 2026-08-21

`install.sh` duplicates `commands/` and `skills/` into `.claude/`. A symlink was the alternative,
and it is genuinely more convenient while `standard` is its own test subject, because editing a
skill would take effect with no re-run.

It was refused because the installed copy has to be a different file from the one being edited.
Under a symlink, the thing under test and the thing being changed are one file, so a green run
stops proving that what the installer produced works. The cost is stated rather than hidden: after
editing a command or skill in the source tree, `install.sh` runs again before the change takes
effect, and a session already open does not pick it up at all.

Consistent with the in-project call above, which already asks for one self-contained copy per
project updated by re-running install.

## `.claude/` is ignored by git, not committed

**Decided**: 2026-08-21

The source tree at the repo root is the single truth and the installed copy is a build output, so
`.gitignore` carries `.claude/`.

Committing it would put every command and skill in git twice with no way for a reader to tell which
copy is authoritative, and one edit would show up as a change in both places. The cost is that a
fresh clone has no typeable commands until someone runs `bash install.sh`, which is one command and
is named in the installer's own output.

## Idempotence is by replacement, not by merge

**Decided**: 2026-08-21

Each run removes `.claude/commands/` and `.claude/skills/` and rewrites them, rather than copying
over what is already there.

Replacement is what makes a deletion propagate: a command removed from the source tree disappears
from the install instead of lingering as a file nothing points at any more. Because the script
deletes before it writes, it first checks that it is standing in this harness's source tree and
exits 1 naming what was missing if it is not.

## Install claims its command and skill names from the user level

**Decided**: 2026-08-21

`install.sh` moves any same-named entry out of `~/.claude/commands/` and `~/.claude/skills/`
before declaring itself done, into two sibling `*-displaced-by-coldstart-standard/` directories.

Writing `.claude/` was necessary and not sufficient. A user-level registration of the same name
wins over the project one, and this repo measured it twice: with `.claude/` correctly installed, a
session that typed `/coldstart` loaded ColdStart v1's payload from outside the repo. The second
measurement narrowed it further — what loaded was v1's user-level *skill*, not its command stub,
so claiming only `commands/` would have left the collision in place. Both surfaces are claimed.

The alternative was renaming this harness's commands to something v1 does not own. It was refused
for the reason the section 2 amendment already gave: `SPEC.md`'s success condition is three command
names and no prose, and rewriting the condition to make it pass hides the gap it exists to find.

The cost is real and stated rather than hidden. This is the only part of the installer that writes
outside the repo, and it disables v1's `/coldstart`, `/prep` and `/done` machine-wide, not just in
this tree. Nothing is deleted: entries are moved, the reverse `mv` is printed at the end of every
run that displaces something, and `--keep-user-commands` skips the step and warns instead. A second
displacement that would overwrite an existing backup exits 1 rather than clobbering it.
