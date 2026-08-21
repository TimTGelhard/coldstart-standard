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
