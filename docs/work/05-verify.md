---
title: Verify
subject: three checks, each with an inject-one-defect self-test, and the close gate that runs them
topic: verify
updated: 2026-08-21
---

# Section 5 — verify

> Built 2026-08-21, in the same pass as section 4. Two sessions, both closed.
> Goal: `/done` has something to run. Until this section there was a close protocol with a
> verify step and no verifier, which is a gate that always opens.

**Done when**: `python3 tools/verify.py --check` reports three checks, each one has been shown
going red on a planted defect, and the resident byte count is a measured number rather than the
SPEC's estimate.

### Settled at plan time

1. **Three checks, named in `SPEC.md`'s feature ledger**: `ghost-refs`, `byte-budgets`,
   `hooks-registered`. Not four. A fourth is a decision, and nothing in sections 4 or 5 asked
   for one.
2. **Each check ships with a self-test that plants one defect** (`SPEC.md`, Adds 4, applied to
   the checks themselves). "The check runs" is not evidence that "the check works".
3. **The tool is `tools/verify.py`**, beside `tools/index.py`, same argument idiom (`--check`
   for the exit-code form), because a second style in a two-file tools directory is how a
   convention dies.

---

## Session 1 — the three checks

**Status**: done

**Goal**: `tools/verify.py` implements the three checks named in the SPEC and prints a report a
human can act on without reading the source

**Build steps**
1. `ghost-refs`: every markdown link under `docs/` and in `SPEC.md` resolves. Out-of-repo and
   absolute targets are counted and reported, not failed, per `FORMAT.md` rule 7.
2. `byte-budgets`: measure the resident surface against the 12,000 B in `SPEC.md`. Front matter
   only for skills, whole file for the wrappers and the carrier, plus the pointer block the
   SessionStart hook injects.
3. `hooks-registered`: four separate properties — registered, installed, executable, and
   pointing at a script that exists — because each fails silently and identically.

**Verify**
1. `python3 tools/verify.py` reports all three, and `--check` exits non-zero when any is red.
2. The byte count is printed as a number and a percentage of the declared ceiling, so the
   report is publishable as-is into `MEASURE.md` at section 7.

**Output**: `feat: three checks, and the close has something to run`

---

## Session 2 — the self-tests

**Status**: done

**Goal**: each check is shown going red on a planted defect, in a copy of the real tree rather
than a fixture built to satisfy it

**Build steps**
1. `tests/test_verify.py`: copy the repo to a temp dir, break exactly one thing, assert the
   check names it.
2. One test per check minimum, plus the tolerance cases that prove the checks stay narrow: an
   out-of-repo link passes `ghost-refs`, and 5 KB added to a skill body does not move
   `byte-budgets`.
3. Assert the clean copy is green first, so a red from a planted defect is attributable.

**Verify**
1. `python3 -m unittest discover -s tests` exits 0.
2. Deleting a rule from `hooks/floor.py` turns `tests/test_floor.py` red naming the category.

**What it found**

The bar paid for itself immediately. `ghost-refs` compared a resolved link path against an
unresolved repo root; on macOS `/var` is a symlink to `/private/var`, so in the temp tree every
link resolved to a path that was not under the root, and the check classified all of them as
"points outside the repo" — a case it tolerates by design. It passed while watching nothing.

The same bug class had already appeared once that morning in the floor's plan-surface check,
which is why it was recognised rather than argued with. Both are one-line fixes and both are
now held by a test. Filed in `fixes/lifecycle.md`.

**Output**: `feat: each check has been shown going red, and one of them was watching nothing`
