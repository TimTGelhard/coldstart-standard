---
title: Install
subject: the minimal map that unblocks the loop, the full two-directory payload, settings merge, and an install that reverses
topic: install
updated: 2026-08-21
---

# Section 6 — install

> The section plan. Four sessions. Written at `/prep`, 2026-08-21.
> Goal: one command puts this harness into a project, updates it by re-running, and reverses by
> deleting two directories.

**Done when**: `install.sh` run twice in a row on a clean checkout leaves an identical tree, the
three commands are typeable in a fresh session in that tree, and the uninstall path returns the
project to its pre-install state with nothing of the harness left behind.

### Settled at plan time

The first three are already on file in `decisions/install.md` and are repeated here so the
sessions build to them rather than re-opening them. The fourth is what section 2 session 4
discovered today. Session 4 files anything new into the same topic file at its close.

1. **In-project install, not a parallel root.** Everything lives inside the project, with no
   `COLDSTART_ROOT`-style variable to resolve. One copy per project, updated by re-running install.
   The stated cost is that N projects means N copies to update.
2. **`.coldstart/` is separate from `.claude/`.** `.claude/` holds only what the host reads:
   `CLAUDE.md`, `settings.json`, `commands/`, `skills/`, `agents/`. Everything the harness owns
   sits beside it. Uninstall is then deleting two directories, and a change in what the host
   expects never lands inside harness files.
3. **`--weight` ships with one arm.** The selector is specced because ColdStart has no preset
   mechanism and every install therefore pays the full floor. It only becomes real once `minimal`
   exists, so this section builds it with a single arm rather than faking a second.
4. **Session 1 runs before section 2 can finish**, per the amendment in `PROJECT_PLAN.md`. A
   command that is not installed cannot be typed, and a lifecycle proved by reading its source
   files rather than by running them is not proved. Session 1 is therefore scoped to the map alone
   and depends only on section 2 sessions 1 to 3, which are closed.

### Open, and owed a human answer

- **Copy or symlink.** A copy makes the project self-contained and versioned with the repo, which
  is what settled call 1 asks for. A symlink would make this repo's own loop editable live, which
  matters only while `standard` is its own subject. Session 1 hits this and must not silently pick.
  Recommendation: copy, and re-run install after editing a command. A symlink here would mean the
  thing being tested and the thing being edited are the same file, which is how a green run stops
  meaning anything.
- **What install does when `.claude/settings.json` already exists.** Session 3 hits this.
  Recommendation: merge additively and refuse on a genuine conflict, naming the key. Overwriting a
  file the host also owns is how an install eats a setting the user put there by hand, and refusing
  loudly costs one message where overwriting costs a debugging session.

---

## Session 1 — the minimal map

**Status**: done

**Goal**: this harness's three commands become typeable in this repo, by mapping `commands/` and
`skills/` into `.claude/` and nothing else

**Files to read**
- `docs/decisions/install.md` (the in-project call and the `.claude` / `.coldstart` split)
- `docs/work/02-commands.md` (session 4, the verify list this session exists to unblock)
- `commands/coldstart.md` (the wrapper shape, to confirm what a mapped command must look like)

**Build steps**
1. `install.sh`: the map alone. `commands/*.md` into `.claude/commands/`, `skills/*/` into
   `.claude/skills/`, nothing else written and no other directory created. Later sessions grow it;
   this one keeps it small enough to read in one screen.
2. Settle the copy-or-symlink call above and record the answer in `decisions/install.md`.
3. Make it idempotent from the start: running it twice leaves the same tree, and it never appends
   to a file it already wrote.
4. `.gitignore`: decide whether `.claude/` is committed or ignored in this repo, and say why in the
   same session. Committing it means the loop resumes on a fresh clone; ignoring it means the
   source tree stays the only truth.
5. Capture the firing artifact under `docs/work/artifacts/06-s1-map.md`: a fresh session in this
   repo typing `/coldstart` and getting this harness's skill rather than v1's.

**Files to write**
- `install.sh`
- `.gitignore`
- `docs/decisions/install.md`
- `docs/work/artifacts/06-s1-map.md`

**Verify**
1. `bash install.sh` exits 0, and `.claude/commands/` holds three files while `.claude/skills/`
   holds three directories.
2. `bash install.sh` run a second time exits 0 and `git status --short` reports nothing new,
   proving idempotence rather than asserting it.
3. In a fresh session in this repo, `/coldstart` loads `skills/coldstart/SKILL.md` from this
   harness. The artifact names the file that was read, which is how v1's payload is ruled out.
4. The negative case: with `.claude/` deleted, a fresh session's `/coldstart` falls back to v1's
   skill again, confirming the map is what changed the answer and not something else.

**Output**: `feat: the three commands are installed, and typing one loads this harness rather than v1`

---

## Session 2 — the full payload

**Status**: pending

**Goal**: install writes everything the host reads and everything the harness owns, into the two
directories the split calls for

**Files to read**
- `install.sh` (session 1's output, the thing being grown)
- `docs/decisions/install.md` (the `.claude` / `.coldstart` split, in full)
- `SPEC.md` (the census target table, so what lands resident is what was budgeted)

**Build steps**
1. Extend `install.sh` to write the rest of `.claude/`: `CLAUDE.md`, `agents/`, and the resident
   profile, from their source locations at the repo root.
2. Write `.coldstart/` beside it: everything the harness owns and the host does not read, including
   the chapters section 3 cuts and `tools/`.
3. Handle a source directory that does not exist yet. Sections 3 and 4 have not landed, so the
   installer must skip a missing `agents/` or `hooks/` and say what it skipped, rather than failing
   or writing an empty directory.
4. Print a census line on completion: bytes written into `.claude/`, which is the resident surface
   section 7 measures. An installer that already knows the number should not make section 7 derive
   it a second way.

**Files to write**
- `install.sh`
- `docs/decisions/install.md`

**Verify**
1. After `bash install.sh` on a clean checkout, `.claude/` and `.coldstart/` both exist and no
   harness file sits outside them.
2. With `agents/` absent from the source tree, install exits 0 and names the skip in its output;
   with it present, the directory is written.
3. The printed census line matches `find .claude -type f | xargs wc -c` to the byte.
4. `python tools/index.py --check` exits 0, confirming the install wrote nothing into `docs/`.

**Output**: `feat: install writes the two directories, skips what does not exist yet, and reports the bytes`

---

## Session 3 — settings and registration

**Status**: pending

> **Partly landed early, 2026-08-21, pulled in by section 4.** The floor needed a registration
> to be a floor at all, so `install.sh` now copies `hooks/` into `.claude/hooks/` and merges
> `hooks/settings.json` into `.claude/settings.json`, replacing only entries that point at this
> harness's own script paths. Idempotence is asserted by hashing the file across two runs.
>
> What is still owed here, and why this session stays open: the registration is read from a
> tracked fragment rather than from whatever `hooks/` actually holds, so a new hook script needs
> a fragment edit — build step 2 asked for the opposite. There is no uninstall, so the merge is
> still a one-way door (step 3). There is no conflict refusal: a genuine disagreement on a key
> is overwritten rather than named (step 1). The self-install guard (step 4) is untested. The
> artifact (step 5) exists for the floor but not for the registration path itself.

**Goal**: install merges into `.claude/settings.json` without eating what is already there, and
registers whatever hooks the source tree actually holds

**Files to read**
- `install.sh` (session 2's output)
- `docs/work/04-safety-floor.md` (the registration open call, so the two sections settle it once)
- `~/.claude/settings.json` (the shape a real settings file has, read as a reference only)

**Build steps**
1. Settle the merge call above, then implement it: additive merge, refuse on a genuine conflict
   naming the key, never a blind overwrite.
2. Register hooks by reading `hooks/` at install time rather than from a hardcoded list, so the
   installer works before section 4 lands and needs no edit after it does.
3. Write the reverse: an uninstall that removes exactly the keys install added and leaves every
   other key untouched. A merge with no matching unmerge is a one-way door.
4. Guard the self-install case. This repo installs into itself, so the installer must not read a
   settings file it is in the middle of writing.
5. Capture the firing artifact: a hook registered by install firing in a real session.

**Files to write**
- `install.sh`
- `docs/decisions/install.md`
- `docs/work/artifacts/06-s3-settings.md`

**Verify**
1. With a `.claude/settings.json` holding an unrelated key, install preserves that key verbatim and
   adds its own alongside.
2. The negative case: with a settings file holding a conflicting value for a key install writes,
   install exits non-zero, names the key, and changes nothing on disk.
3. With `hooks/` empty or absent, install exits 0 and registers no hook; with one script present, it
   registers exactly that one.
4. The uninstall path restores the settings file byte-for-byte to its pre-install content.

**Output**: `feat: install merges settings additively, refuses on conflict, and registers what it finds`

---

## Session 4 — reverse and re-run

**Status**: pending

**Goal**: the install is proved reversible and idempotent against a real tree, and `--weight` ships
with its one arm

**Files to read**
- `install.sh` (sessions 1 to 3's output, whole)
- `docs/decisions/install.md` (the `--weight` deferral and its one-arm scope)
- `docs/work/artifacts/06-s1-map.md` (the artifact shape this section established)

**Build steps**
1. Add `--weight standard` as the only arm, with an explicit refusal for `minimal` naming the
   harness that does not exist yet. A selector whose second value silently does the same thing as
   the first is worse than no selector.
2. Add `--uninstall`: delete the two directories and unmerge the settings keys, and nothing else.
3. **Delegate the round trip**: an agent with no history runs install, uninstall and install again
   against a scratch clone, and reports the tree state at each boundary. The author of an installer
   is the worst person to test whether it left something behind.
4. Record what the install actually costs resident, against `SPEC.md`'s ~9,340 B census target, and
   state the delta either way. Section 7 measures the rendered surface; this is the installed one,
   and the two numbers being different is information rather than a contradiction.
5. File the result in `decisions/install.md`, and anything that bit into `fixes/`.

**Files to write**
- `install.sh`
- `docs/decisions/install.md`
- `docs/fixes/` (whatever the round trip surfaces)
- `docs/work/artifacts/06-s4-roundtrip.md`

**Verify**
1. On a scratch clone: install, then `git status --short` is empty except the two directories;
   uninstall, then `git status --short` is empty entirely.
2. Install run twice leaves an identical tree, compared with `diff -r` rather than by inspection.
3. `bash install.sh --weight minimal` exits non-zero and names the missing harness; `--weight
   standard` behaves as the bare command.
4. The delegated agent's report names the tree state at all three boundaries, and any file left
   behind by uninstall is listed by path.

**Output**: `feat: install reverses cleanly, re-runs to an identical tree, and ships one weight arm`
