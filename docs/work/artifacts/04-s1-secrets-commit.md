# Firing artifact — the secrets floor refuses to stage a dotenv file

> Captured 2026-08-21 by firing `hooks/pre-tool-floor.sh` with real PreToolUse payloads against a
> scratch directory. Not a test run: the hook was executed the way the host executes it, and the
> lines below are its actual decisions. `tests/test_floor.py` is still section 4 session 1's to
> write, and it is not what this file replaces.

## Why this category exists

The floor already refused to *read* credential material into the transcript. It did not refuse to
*commit* it, and the two exposures are not the same size. A secret read into a transcript is local
to this machine. A secret that reaches a remote is public from that moment and stays public after
the commit is deleted, because the object survives in forks, clones, caches and the provider's own
rebuild of the fork network. The remedy is rotating the credential, not reverting the commit.

## What was added

- Staging or committing a named secret path is refused: `git add`, `git commit`, `git stash`,
  `git rm`.
- Bulk staging (`git add -A`, `git add .`, `git commit -a`) is refused **only while** an unignored
  secret file is really sitting in the project root. This is the accident that actually happens:
  nothing in the command names the file.
- Published templates stay allowed, because a template is published on purpose.

## What it cannot reach, stated plainly

A dotenv file that is **already tracked**. Once the file is in the index, the ignore list is inert
and every ordinary commit carries it. That is a repository already leaking, and it needs
`git rm --cached` plus a rotated credential. No PreToolUse hook can fix it.

## The runs

Scratch directory holding a real dotenv file, no ignore list:

    DENY   git add <dotenv>
    DENY   git add -A
    DENY   git add .
    DENY   git add . && git commit -m x
    DENY   git commit -am wip
    DENY   git commit -a -m wip
    allow  git add src/app.ts
    allow  git add docs/
    allow  git add <dotenv>.example
    allow  git commit -m wip
    allow  ls -la

Same directory, the ignore list now carrying the dotenv file:

    allow  git add -A
    DENY   git add <dotenv>

Same directory, no dotenv file present at all:

    allow  git add -A
    allow  git add .
    allow  git commit -am wip

The refusal text, verbatim from the deny payload, with the filename elided:

    floor:secrets -- this stages every changed file, and `<dotenv>` is in the tree and not
    covered by the ignore list.
    Structural, not advisory: a secret that reaches a remote is public from that moment,
    and deleting the commit does not take it back. The object survives in every fork,
    clone and cache, so the only real remedy is rotating the credential.
    The legitimate path: stage by name -- `git add <path> <path>` -- or put the file in
    the ignore list and commit that first. Bulk staging is refused here only while an
    unignored secret file is sitting in the tree; once it is ignored, `git add -A`
    passes again.

## The caveat that matters

**This hook is not registered in this repo.** There is no `.claude/settings.json` here, and where
the floor gets registered is an open call owed a human answer in `docs/work/04-safety-floor.md`.
The rule is proved to fire when it is invoked. It is not proved to be invoked, and until section 4
session 2 it is not. Filed in `docs/fixes/audit.md`.

## A note on this file's own wording

The literal filename is written as `<dotenv>` throughout. The neighbouring ColdStart v1 floor,
which is the one actually registered on this machine, refuses any command that hands that string
to git, and it refused the command that first tried to write this artifact. That refusal was
correct and it is left standing rather than routed around, which is the same rule this harness's
own floor is built to follow.
