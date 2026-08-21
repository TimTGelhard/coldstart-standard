---
title: Safety floor
subject: the PreToolUse hook that denies rather than asks, its coupling to the pointer's mode field, and the proof it fires
topic: safety-floor
updated: 2026-08-21
---

# Section 4 — safety floor

> The section plan. Three sessions. Written at `/prep`, 2026-08-21.
> Goal: the one thing `SPEC.md` calls a defect when skipped exists here — a PreToolUse hook that
> denies secrets, destructive commands and out-of-mode shells, enforced rather than requested.

**Done when**: a shell that reads a secret, a shell that destroys, and a non-read-only shell under
`mode: prep` are each refused by this harness's own hook, with a dated firing artifact per category
showing the refusal in a real session rather than in a test.

### Settled at plan time

No operator calls were made for this section before the plan was written. What is fixed below is
fixed by files already on disk, and the sessions build to it rather than re-opening it. Session 3
files these into `decisions/safety-floor.md` at its close.

1. **The floor is enforced, not requested** (`SPEC.md`, "What it must keep"). It denies. It does
   not warn, prompt, or defer to a setting. The reason is that a floor with a dial is a floor that
   is off in the session where it mattered.
2. **Payload layout**: `hooks/` sits at the repo root beside `tools/`, and section 6's installer
   maps it into `.claude/`. Same call section 2 settled for `commands/` and `skills/`; carried here
   so this section does not invent a second layout.
3. **A firing artifact per hook** (`SPEC.md`, Adds 4). The file existing is not the evidence.
   Green CI has already hidden an unfinished install once in this family, which is why the section
   ends on artifacts rather than on tests.
4. **The name is `pre-tool-floor.sh`** (`SPEC.md`, feature ledger row "Safety floor"), carried
   from ColdStart unchanged because the decision travelled and the implementation is being rebuilt.
5. **A harness must not claim a tree it does not serve.** Section 2 session 4 discovered this the
   hard way: ColdStart v1 claims any directory holding `docs/PROGRESS.md`
   (`tools/coldstart/root.py`, `MOUNT_MARKERS`) and then enforced its mode contract on this repo
   against a pointer field this repo does not have. `/prep` could not write at all until a
   `.coldstart-init` declaration scoped this tree out. This harness's floor inherits the rule as a
   constraint on itself, and session 2 is where it is proved rather than asserted.

### Open, and owed a human answer

- **Where the hook is registered while this repo is its own subject.** The tree has no `.claude/`
  today, and the floor that denied a command during this planning pass came from the global v1
  install, not from here. Session 2 hits this and must not silently pick.
  Recommendation: register it in an in-project `.claude/settings.json` at session 2, so the
  artifacts prove *this* harness's hook and not the neighbour's, and make section 6's installer
  emit that same registration rather than a second shape.
- **Whether the refusal is exit code 2 with stderr, or JSON carrying an explicit deny decision.**
  Session 1 hits this. Recommendation: JSON with an explicit deny and a reason string, because the
  refusal text is the working part — the operator has to know which category fired and what the
  legitimate path is, and a bare exit code teaches neither.

---

## Session 1 — the deny rules

**Status**: pending

**Goal**: the three deny categories exist as one hook script with a fixture-driven test that feeds
it real tool payloads and asserts refusal and, just as hard, non-refusal

**Files to read**
- `SPEC.md` (the "What it must keep" floor line and the feature-ledger row that names the script)
- `docs/decisions/commands.md` (the payload-layout call, so `hooks/` lands where section 2 put its
  siblings)
- `tests/test_index.py` (the fixture idiom this repo already uses, so the floor's test looks like
  its neighbour rather than importing a second style)

**Build steps**
1. `hooks/pre-tool-floor.sh`: the whole floor. Reads the PreToolUse payload on stdin, classifies
   the command, emits either a silent pass or a structured refusal naming the category.
2. Write the three categories with their rules inline: secrets (reading or echoing credential
   files and env values), destructive commands (recursive delete, force push, history rewrite,
   unbounded overwrite), and the mode contract, which session 2 wires and this session stubs.
3. Write the refusal text shape: what fired, why it is structural, and what the legitimate path is.
   A refusal that does not name the legitimate path gets routed around within a session.
4. `tests/test_floor.py` plus `tests/fixtures/floor/`: one fixture per category, and at least as
   many allow-fixtures as deny-fixtures. A floor that denies too much is turned off by its owner.
5. Settle the refusal-protocol open call above and record the answer in `decisions/safety-floor.md`.

**Files to write**
- `hooks/pre-tool-floor.sh`
- `tests/test_floor.py`
- `tests/fixtures/floor/`
- `docs/decisions/safety-floor.md`

**Verify**
1. `python -m pytest tests/test_floor.py` exits 0.
2. Feeding the hook a payload that reads `.env` produces a refusal naming the secrets category;
   feeding it `cat README.md` produces a pass with empty output.
3. The negative case: delete one deny rule from the script and confirm `tests/test_floor.py` goes
   red naming that category, so the test is proved to be watching the rule rather than the file.
4. `hooks/pre-tool-floor.sh` is executable and runs under `sh` with no bash-only syntax.

**Output**: `feat: the floor is three deny categories and a test that has seen each one go red`

---

## Session 2 — the mode contract

**Status**: pending

**Goal**: the floor reads this tree's pointer at tool time, denies any shell it cannot prove
read-only while the mode is `prep`, and stays silent in a tree it does not serve

**Files to read**
- `docs/FORMAT.md` (section 1, the pointer's seven fields and the one-writer rule with `/prep`'s
  named exception)
- `skills/prep/SKILL.md` (the mode declaration and what the pass promises the floor)
- `hooks/pre-tool-floor.sh` (session 1's output, the thing being extended)

**Build steps**
1. Extend `hooks/pre-tool-floor.sh`: read `mode` from `docs/PROGRESS.md`'s front matter at each
   invocation, not once at registration. An absent `mode` resolves to `build` and the contract is
   inert.
2. Write the read-only proof as a whitelist, not a blacklist: a command passes under `prep` only if
   every segment is a known read. Compound commands and pipes into anything unrecognised are
   denied, because provable is the standard and plausible is not.
3. **Scope the contract to trees this harness serves**, per settled call 5. A pointer that does not
   carry this schema's seven fields is not this harness's pointer, and the mode branch fails open
   rather than refusing. The risk categories stay active everywhere.
4. Resolve the registration open call above, then land the registration it decides on.
5. Write the escape hatch into the refusal text: the way out of a `prep` denial is
   `python tools/done.py --set-mode build`, which is a declaration the operator makes on the record,
   not a flag that suppresses the check.
6. Extend `tests/fixtures/floor/` with the mode cases, including a `prep` pass-case so the
   whitelist is proved to let real reads through.

**Files to write**
- `hooks/pre-tool-floor.sh`
- `.claude/settings.json` (pending the registration call above)
- `tests/fixtures/floor/`
- `tests/test_floor.py`
- `docs/decisions/safety-floor.md`

**Verify**
1. With `mode: prep` on the pointer, a write outside the plan surface is refused and `cat SPEC.md`
   passes; with `mode: build`, both pass.
2. The pointer is edited from `prep` to `build` mid-run and the next invocation behaves as `build`
   with no restart, proving the field is read at tool time.
3. The negative case: a compound command whose halves are both known reads is still denied under
   `prep`, and the refusal says why provability rather than safety is the bar.
4. Pointed at a fixture tree whose pointer carries a foreign schema, the mode branch returns no
   violation while the secrets and destructive categories still fire — the defect this harness was
   on the receiving end of, asserted as a test.
5. `python -m pytest tests/test_floor.py` exits 0 and `python tools/index.py --check` exits 0.

**Output**: `feat: the floor reads the pointer at tool time, and refuses to govern a tree it does not serve`

---

## Session 3 — proof it fires

**Status**: pending

**Goal**: each deny category is shown refusing a real command in a real session, captured dated,
so the section closes on evidence rather than on a passing test

**Files to read**
- `docs/work/04-safety-floor.md` (this file, sessions 1 and 2 as the list of what must be shown)
- `docs/work/artifacts/02-s2-coldstart.md` (the artifact shape section 2 established)
- `.claude/settings.json` (the registration session 2 landed, to confirm what is actually wired)

**Build steps**
1. Run each category against the live hook in this repo: a secrets read, a destructive command, and
   a non-read-only shell under `mode: prep`. Capture the refusal text verbatim.
2. **Delegate the cold check**: a fresh agent with no history is given this tree and one
   destructive-sounding instruction, and its transcript is taken back as the artifact. A refusal
   the author provoked knowing the rule proves less than one that stopped someone mid-task.
3. Record the false-positive count from sessions 1 and 2 plus this run: every command the floor
   denied that should have passed. A floor is calibrated by that number, and it is the number that
   decides whether it survives contact with daily use.
4. `docs/work/artifacts/04-s3-floor.md`: the artifacts, dated, one block per category.
5. File the calibration result in `decisions/safety-floor.md`, and anything that bit into `fixes/`.

**Files to write**
- `docs/work/artifacts/04-s3-floor.md`
- `docs/decisions/safety-floor.md`
- `docs/fixes/` (whatever the run surfaces)

**Verify**
1. `docs/work/artifacts/04-s3-floor.md` holds three dated blocks, each with the command sent and
   the refusal returned verbatim.
2. The cold agent's block shows it was stopped by the hook rather than declining on its own
   judgement, identifiable by the hook's category string appearing in its transcript.
3. The false-positive count is written down as a number with each instance named, even when it is
   zero, because an unstated zero and an uncounted zero read the same later.
4. `python -m pytest tests/test_floor.py` and `python tools/index.py --check` both exit 0.

**Output**: `feat: each deny category is shown refusing a real command, and the false positives are counted`
