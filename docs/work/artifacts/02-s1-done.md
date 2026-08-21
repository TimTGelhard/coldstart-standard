# Firing artifact — `/done`, section 2 session 1

**Date**: 2026-08-21
**Skill under test**: `skills/done/SKILL.md`, driven from `commands/done.md`
**Target**: `docs/work/99-scratch-close.md`, a throwaway section created for this run and deleted
after it. Its session block is the thing the close acted on; the artifact is the record that the
close *ran*, not that the file exists.

The generator scans `docs/work/*.md` non-recursively, so this directory is invisible to
`tools/index.py` and needs no front matter.

---

## Run 1 — red verify, planted. The close refuses.

The scratch session's `Verify` list carried three checks, the third planted to fail:

    1. python tools/index.py --check          exit=0
    2. test -f skills/done/SKILL.md           exit=0
    3. test -f commands/DOES-NOT-EXIST.md     exit=1   <- planted

Step 1 of the skill stopped the close here. What was asserted afterwards:

- `docs/work/99-scratch-close.md` line 15 still read `**Status**: pending`. Unchanged.
- The pointer front matter (`docs/PROGRESS.md` lines 1-9) hashed
  `aaed847ed7658c9cab03bfb6ec6c761d8f42b320`, byte-identical to before the run.
- No index was regenerated, nothing was committed.

The planted check was then repaired at its source (`commands/DOES-NOT-EXIST.md` ->
`commands/done.md`), which is the only legitimate way past a red: fix the thing, not the check.

**Deviation, recorded rather than hidden**: the run left the pointer byte-identical instead of
re-pointing it at the scratch section first. Re-pointing by hand would have needed a writer other
than `/done` touching the pointer, which is the rule under test. Byte-identical is the stronger
assertion anyway: the refused close wrote nothing at all.

## Run 2 — green verify. The close completes.

    1. python tools/index.py --check          exit=0
    2. test -f skills/done/SKILL.md           exit=0
    3. test -f commands/done.md               exit=0

Steps 2 through 6 of the skill, in order, with what each one actually did:

- **Step 2, content files.** The scratch session block went to `**Status**: done` and gained
  `**Closed**: 2026-08-21`. Five decisions were filed into the existing `docs/decisions/commands.md`
  rather than a new topic file, which is the clustering rule doing its job at close time.
- **Step 3, regenerate.** `python tools/index.py` printed `index: rewrote docs/PROGRESS.md`. Session
  99.1 left the queue and section 99 appeared as one row in the log, dated `closed 2026-08-21` —
  the queue-is-open-only rule, observed rather than asserted.
- **Step 4, assert no-op.** `python tools/index.py --check` exit 0.
- **Step 5, pointer written whole.** All seven fields recomposed from scratch. `mode: build`, not
  `prep`. No field carried a placeholder, and `next_action` / `resume_note` / `reading` were each
  re-derived rather than copied from the previous close. A re-run of `--check` afterwards exited 0,
  which is also the standing assertion that the generator leaves the front matter alone.
- **Step 6, clustering nudge.** Largest topic file was `docs/decisions/memory-model.md` at 144
  lines, under the ~200-line split threshold. Nothing to propose, nothing gated.

**Step 7 was deliberately not run against the scratch section**, because a commit of a throwaway
section that is deleted moments later records nothing. Step 7 fired for real on this session's own
close instead, and that commit is the artifact for it.

## Teardown

`docs/work/99-scratch-close.md` was deleted and `tools/index.py` re-run, returning the queue and log
to the state the real work describes. `--check` exit 0 after teardown.
