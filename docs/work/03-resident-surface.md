---
title: Resident surface
subject: the always-loaded surface — CLAUDE.md, the distilled profile, four routers, three agents, and the chapter cut
topic: resident-surface
updated: 2026-08-21
---

# Section 3 — resident surface

> The section plan. Four sessions. Written at `/prep`, 2026-08-21.
> Goal: everything this harness makes resident exists, in the cheap form the SPEC's ledger
> committed to, with the chapters it routes into.

**Done when**: `CLAUDE.md`, one distilled profile, four routers, three agents and the surviving
chapters exist on disk, every router routes into a chapter that exists, and the rendered resident
byte count is measured and written down against the SPEC's ~9,340 B census.

**Shape**: Build. Sessions break by layer, and the last one is the proof rather than a polish.

### Settled at plan time

1. **Two dials, and the unturned one is length.** Four routers, each description written to a
   ~250 B target. ColdStart's 17 routers average 713 B; count is the obvious lever and length is
   the one nobody pulled. Both get pulled here (`SPEC.md`, the feature ledger).
2. **Payload layout.** `chapters/`, `skills/` and `agents/` sit at the repo root beside `tools/`,
   and section 6's installer maps them into `.claude/` and `.coldstart/`. Already decided at
   section 2 and recorded in `decisions/commands.md`; this section is its first big consumer.
3. **Personalization is one file, not a system.** ColdStart's six-chapter personalization collapses
   to a single distilled profile of roughly 1,200 B, shipped as a template the operator edits by
   hand. There is no onboarding command in this harness, because the command surface is frozen at
   three.

### Open, and owed a human answer

- **Which four routers.** The SPEC fixes the count and not the names. Session 2 hits this and must
  not silently pick. Recommendation: `workflow`, `recovery`, `brownfield`, `anti-patterns` — the
  four ColdStart clusters that fired on real work rather than on questions about Claude Code.
- **Whether the byte targets are re-checked against section 2 session 4's census.** Session 4 hits
  this. Recommendation: yes, and the delta is written down either way, because an estimate that is
  never checked is how the previous harness lost its floor.

---

## Session 1 — the chapter cut

**Status**: pending

**Goal**: ColdStart's 84 chapters become the 12-15 this harness carries, each one a file that a
router can name

**Files to read**
- `SPEC.md` (the inheritance question and the drops list)
- `/Users/macbook/coldstart/chapters/` (the source tree — inventory it, do not port it)
- `docs/PROJECT_PLAN.md` (the open question this session answers)

**Build steps**
1. **Delegate the inventory**: an agent walks ColdStart's chapter tree and reports one line per
   chapter — what it decides, and what breaks when it is absent. The main context keeps the table,
   not the files.
2. Cut to 12-15 against that table, and write the reason each survivor survived.
3. `chapters/*.md`: write the survivors. Each one carries the decision and leaves ColdStart's
   implementation, per the rule this project is under.
4. `docs/decisions/resident-surface.md`: the cut list, with what was dropped and why.

**Files to write**
- `chapters/*.md` (12-15 files)
- `docs/decisions/resident-surface.md`

**Verify**
1. `ls chapters/*.md | wc -l` is between 12 and 15.
2. Every chapter file is under 200 lines, and the total `wc -c` of `chapters/` is recorded in the
   decision file. Chapters are cold, so the number is a fact, not a budget.
3. `docs/decisions/resident-surface.md` names every dropped ColdStart cluster with its reason, and
   `python tools/index.py --check` accepts the file's front matter.
4. No chapter references a `chapters/` file that does not exist: grep the cross-references and
   resolve each one.

**Output**: `feat: the chapter cut is decided, and each survivor says what it decides`

---

## Session 2 — the four routers

**Status**: pending

**Goal**: four skills route into the chapters, at a quarter of ColdStart's per-router description
cost, and each one is proved to fire

**Files to read**
- `docs/decisions/resident-surface.md` (session 1's cut list)
- `SPEC.md` (the two-dial argument in the feature ledger)
- `skills/coldstart/SKILL.md` (the shape a skill in this tree takes)

**Build steps**
1. Settle the open call above: name the four routers, and record the answer in
   `docs/decisions/resident-surface.md` with the reason.
2. `skills/<router>/SKILL.md` x4: each one a description written to ~250 B, and a body that routes
   to chapters by name rather than restating them.
3. Write the fire test for each: a prompt that should route to it and a prompt that should not.
4. Capture the firing artifact — a real run per router, not a claim that the file exists.

**Files to write**
- `skills/<router>/SKILL.md` x4
- `docs/decisions/resident-surface.md` (the router names and the reason)
- `docs/work/artifacts/03-s2-routers.md`

**Verify**
1. Each of the four descriptions measures at most 300 B, and the four together are under 1,200 B
   against ColdStart's 12,121 B for 17. Print the measured numbers.
2. Every chapter from session 1 is named by at least one router; print the unrouted list and
   confirm it is empty or deliberately empty.
3. Each router fires on its own prompt in a fresh session, and does not fire on the negative
   prompt. The artifact shows the run.
4. No router body restates a chapter: grep for duplicated sentences between a router and the
   chapters it names.

**Output**: `feat: four routers carry seventeen routers' job at a tenth of the description cost`

---

## Session 3 — CLAUDE.md and the distilled profile

**Status**: pending

**Goal**: the always-loaded prose exists — delegation, signaling, the safety line and the pointer
at the lifecycle — plus one profile file the operator edits by hand

**Files to read**
- `SPEC.md` (the census target table and the keeps table)
- `docs/decisions/resident-surface.md` (the router names, so the prose points at real skills)
- `/Users/macbook/.claude/CLAUDE.md` (the current always-loaded carrier — carry the decision)

**Build steps**
1. `CLAUDE.md`: the resident carrier, to a ~2,500 B target. Delegation in ~400 B, signaling in four
   lines, the safety floor named, and a pointer at the three commands.
2. `templates/PROFILE.md`: the distilled profile, ~1,200 B, replacing the six-chapter
   personalization system with one file and no interview.
3. Every path either file names is checked to exist, because a carrier that points at a missing
   file is the failure that is invisible until a cold session hits it.
4. Record the measured bytes of both files in `docs/decisions/resident-surface.md`.

**Files to write**
- `CLAUDE.md`
- `templates/PROFILE.md`
- `docs/decisions/resident-surface.md` (the two measurements)

**Verify**
1. `wc -c CLAUDE.md` is at most 3,000 and `wc -c templates/PROFILE.md` is at most 1,500. Print both.
2. Every repo-relative path named in either file resolves: extract them and test each for existence.
3. `CLAUDE.md` names all three commands and all four routers, and nothing that section 3 dropped.
4. The profile template carries no placeholder that a real operator would ship unfilled: grep for
   angle brackets and confirm each is inside a labelled example block.

**Output**: `feat: the resident carrier and the profile are one file each, and every path they name exists`

---

## Session 4 — the three agents, and the census

**Status**: pending

**Goal**: the three agents exist, and the whole resident surface is measured against the SPEC's
predicted census with the delta stated either way

**Files to read**
- `SPEC.md` (the census target table)
- `docs/decisions/resident-surface.md` (every measurement the section has taken so far)
- `docs/work/03-resident-surface.md` (this file)

**Build steps**
1. `agents/*.md` x3: the reviewer, the simplifier and the build-fixer, each a description plus the
   tools it is granted. Read-only unless the definition says otherwise.
2. Settle the second open call: re-check the byte targets against section 2 session 4's census.
3. Write the census script or the one-liner that measures the rendered resident surface — every
   description the host loads, plus `CLAUDE.md` and the profile — and record its output.
4. File the delta against the SPEC's ~9,340 B in `docs/decisions/resident-surface.md`, and anything
   that bit into `docs/fixes/`.

**Files to write**
- `agents/*.md` x3
- `docs/decisions/resident-surface.md` (the census and the delta)
- `docs/fixes/` (whatever the census surfaces)

**Verify**
1. The census prints one line per resident item with its byte count and a total, and the total is
   compared to 9,340 B in writing, over or under.
2. The three agent descriptions together measure at most 1,200 B against the SPEC's ~989 B line.
3. Each agent's granted tool list is stated in its file, and no agent grants write or exec tools
   without a sentence saying why.
4. `python tools/index.py --check` exits 0, and `docs/DECISIONS.md` carries the
   `resident-surface` line with the entry count the folder actually holds.

**Output**: `feat: the resident surface is three agents wide and measured, not estimated`
