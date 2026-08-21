# coldstart-standard — SPEC

> Written before the build, per the family contract (`../../CHARTER.md`).
> Status: **partly built** — 3 of 7 sections. 2026-08-19, amended 2026-08-21.
> The per-section state is at the bottom of this file, under Build state.

> **UNPARKED — 2026-08-21 (Tim).** The 2026-08-19 parking held because the program's one rule
> is that a harness is only interesting if it can be compared, and no comparator exists. That
> rule is set aside here by owner's call: `standard` and `minimal` are being built as harnesses
> for real use, not as arms of an experiment. The consequence is stated plainly so nobody
> rediscovers it later — **`standard` ships without a score, and its success condition below is
> restated in terms it can actually be judged by.** The parking card in the control tree
> (`/Users/macbook/coldstart/docs/deepseek-transfer/decisions/program-parked.md`) still says
> parked and is owed a superseding entry.

## The job

The general-purpose harness. What ColdStart v2 should have been if weight had been a
constraint from day one instead of an afterthought.

Explicitly **not** a fork of ColdStart with files deleted. Deleting from a mature tree
carries its assumptions along with its lessons, and produces something that is neither
lean nor coherent. This is a rebuild that *reads* ColdStart, treats it as a source of
answers, and re-earns each one.

## Who it is for

Tim's real projects. The default. If `standard` is not the thing you reach for on a normal
Tuesday, it has failed regardless of its score.

## The one thing it is for

**You should not have to re-prompt the project into the session.** Everything below serves
that. A harness that cannot tell the model what is next, what was already decided, and what
already bit, is a harness that makes you type those things again every morning, which is
the cost it exists to remove.

## Declared budget

- **Resident: under 12,000 B.** Roughly a third of ColdStart's 38,616 B. Provisional
  until the first `MEASURE.md`; it is a target to design against, not a lock.
- **Runtime dependencies:** Python stdlib permitted. No network on the hot path.
- **Install:** one command, reversible, idempotent.

## The inheritance question

Three sources, and they rank:

1. **`coldstart/design/00`–`15`** — the locked spec. This is where the *reasoning* lives.
   Read the design file before re-deciding anything it already settled.
2. **`coldstart-codex/`** — a prior clean-room *audit and decision set*, not a tree. It never
   shipped code; it is stalled in section 1 waiting on Tim to accept D-005..D-012. Its 12
   decisions and its measurements are the shortcut. Read before building.
3. **`coldstart/docs/`** — the warehouse. 364 documents of what was tried and what bit.
   Query it; do not port it.

The rule: **carry the decision, leave the implementation.** ColdStart's answer to "how do
you stop a component ref outliving its target" is 30 check-classes. The *decision* worth
carrying is that a rename must sweep its refs. Whether that needs 30 check-classes in a
lean harness is exactly what is being re-decided.

## What it must keep

These are the things ColdStart proved by having them break when absent. Non-negotiable in
some form, though not necessarily in ColdStart's form:

- **A safety floor that is enforced, not requested.** Secrets, destructive commands.
- **The memory model** (below). The resume pointer, the decision record and the interrupt
  queue. This is the harness.
- **A "verify the world, not the self-report" discipline**, wired into how work is closed.
- **Session scoping** — the one-sentence goal, the "and" test.

## The memory model

> Amended 2026-08-21 (Tim). Supersedes the original ledger line that dropped the warehouse
> outright. The drop was reasoning about the wrong cost: **stored knowledge is COLD and
> costs zero resident bytes.** What made ColdStart's warehouse expensive was the machinery
> around the storage, and the machinery is separable from the storage.

Three kinds of fact a session needs, and one uniform structure that holds all three.

| Fact | Without it |
|---|---|
| What is next | you re-scope every session |
| What was already decided | the model re-asks, or quietly decides differently |
| What is open but not now | unplanned work derails the active session |

### The shape

```
docs/
  PROGRESS.md    pointer + one line per session    ->  work/
  DECISIONS.md   one line per topic                ->  decisions/
  FIXES.md       one line per open item            ->  fixes/
  work/          one file per session
  decisions/     clustered by topic: auth.md, database.md, deploy.md, ...
  fixes/         clustered by topic, same rule
```

**One mechanic, applied three times.** An index file holds status and a pointer and
structurally cannot hold detail, so it cannot bloat. The folder beside it holds the
content, clustered by topic so no single file grows without bound. The uniformity is the
point: one rule for the model to follow, one script to write, no file that behaves
differently from its neighbours.

`PROGRESS.md` additionally carries the resume pointer at the top: active work, next action,
blockers, read list. That block is the only part of the memory model that is resident.

### The rules that make it work unattended

1. **Indexes are derived, never maintained.** At `/done` a script scans each folder, reads
   each file's title and one-line subject, and rewrites the index above it. An index cannot
   go stale or disagree with its folder, because it is a function of it. This single choice
   is what deletes the canonical-versus-projection split and every check that polices it.
   ColdStart generates its indexes from a *separate state file* (`LIFECYCLE.json`), which is
   precisely why it needs `state-consistency` and `warehouse-maps`.
2. **Clustering follows a rule, not taste.** At close, a decision is filed into the existing
   topic file that fits; a new topic file is created only when none does. A long topic file
   splits by sub-topic (`auth.md` becomes `auth-sessions.md` + `auth-oauth.md`). This is a
   nudge at `/done`, never a gate.
3. **The queue is open-only.** A shipped fix is deleted, not archived; git is the archive.
   No done section, ever.
4. **Nothing in `docs/` is loaded wholesale.** A session reads the pointer, then walks one
   index to at most one or two files. Storage is cold by default.

### What this deliberately does NOT carry from ColdStart

Not because of bytes, but because each one exists only to police a split this model does
not have: `LIFECYCLE.json` and generated projections · `registry.tsv` and the ownership
manifest · rooms, boxes and the `plan`/`decisions`/`gotchas` taxonomy · nested per-room
`MAP.md` files · container caps, card caps and the room-split ritual · `done.py`'s 75-module
tool family · the check-classes whose subject is any of the above.

## What is on the table

Everything else. Named explicitly so the build cannot quietly assume them, and **ruled on
in the feature ledger below**:

generated projections · the capability library and facet-map · per-chapter routing skills ·
the check-class self-test bar · the 7-day soak gate · the ownership manifest

Each is a genuinely good idea that cost real bytes. Each has to argue for itself.

## Success condition

> Restated 2026-08-21. The original condition was "within noise of `coldstart` at a third of
> the resident cost", which is a score this harness cannot be given, because the comparator
> was dropped unbuilt. Keeping it would be specifying a gate nothing can open.

`standard` succeeds if, on a real project of Tim's, **a session can be opened with `/coldstart`
and no prose**, and the work that follows is correctly scoped, does not contradict a decision
already on file, and closes with the record updated. It fails if the operator finds themselves
re-explaining the project, or hand-maintaining the files that are supposed to maintain
themselves.

The resident budget stays as a design constraint and is reported in `MEASURE.md`. It is a
number to publish, not a gate to pass.

## Depends on

Nothing. Four other harnesses depend on it, so its memory model and command surface are
frozen before `coding` starts.

## The feature ledger

> Scoped 2026-08-19 against a live census of ColdStart's **rendered** surface, not its file
> list. Amended 2026-08-21. The byte table lives in `../coldstart-minimal/SPEC.md` and is not
> repeated here; the two numbers that drive this ledger are that the 17 `cs-*` router
> descriptions cost **12,121 B** (avg 713 B each) and the verbatim profile costs **5,222 B**.

Two dials, not one. Router *count* is the obvious lever; router *description length* is
the unturned one. The same 17 routers at 250 B each cost 4,250 B. `standard` turns both.

### Keeps — re-earned, in a cheaper form

Carrying the decision, leaving the implementation.

| Feature | ColdStart's form | `standard`'s form |
|---|---|---|
| Safety floor | `pre-tool-floor.sh` + deny rules | unchanged. It is the one thing that is a *defect* when skipped |
| Project memory | warehouse: 28 rooms, boxes, nested MAPs, `LIFECYCLE.json` + generator, 364 docs | **3 index files + 3 folders**, indexes derived by scanning. See the memory model above |
| Planning pass | 05h/05i/05j + `procedure.md` + the work-shape catalog + `/prep` | one skill, one template, work shapes as a compressed table inside it |
| Session close | the `done.py` tool family | one skill: file the decisions, regenerate the three indexes, run verify, write the pointer, stop |
| Delegation | chapters 16a/16b/16c + a router | ~400 B of `CLAUDE.md` prose |
| Signaling | chapter 11, 7 files + a router | 4 lines of `CLAUDE.md` |
| Verify | 30 check-classes, 65 test files | **3**: `ghost-refs` (link rot), `byte-budgets` (the floor guard), `hooks-registered` (proof it fires) |

### Commands — three, and why not fewer

> Amended 2026-08-21 (Tim). The original ledger cut 8 wrappers to `prep`, `done`,
> `orientate` and dropped `/coldstart`. That was arithmetic, not a decision: `/coldstart` is
> the resume door, the first thing typed in every session, and `/orientate` is only its
> read-only half. The whole wrapper set is 3,599 B against a 12,000 B ceiling, so bytes were
> never the constraint.

| Command | Job |
|---|---|
| `/coldstart` | resume: read the pointer, load the active work file, continue |
| `/prep` | plan: scope the work, write the session files into `work/`, queue them in `PROGRESS.md` |
| `/done` | close: file decisions, regenerate the three indexes, verify, rewrite the pointer |

Dropped, with the reason: `orientate` is `/coldstart`'s read-only half and not worth a second
wrapper · `cleanup` and `maintenance` sweep generated projections and check-classes that this
harness does not have, so their subject is gone · `bucket` is out · `adopt` is a real facility
and is **deferred, not dropped** — it lands once `standard` runs on a real project.

### Drops

Capability library, facet-map, dock · `LIFECYCLE.json` and every projection · 17 routers down
to **4** · 84 chapters down to **~12–15**, on demand · the 6-chapter personalization system
down to one distilled ~1,200 B profile · bucket · `registry.tsv` · the 7-day soak gate · the
`self-test-integrity` bar · `eval-regression`'s three self-report consumers (routing, memory
and skill-fire recall) — selecting on a probe of the harness's own routing output picks the
arm that *routes* well while doing worse work.

### Adds — none of these exist in ColdStart

1. **A weight selector in `install.sh`** (`--weight minimal|standard`). ColdStart has no
   preset mechanism anywhere, so every install pays the full floor. It is also the thing
   that lets the family converge to presets later instead of leaving six trees to maintain.
2. **A containment test.** Plant a sentinel string, assert it never reaches the model, pin
   the full system string and the tool list. A leanness claim held by a test, not by
   inspection (`dsh`'s `minimal-preset.snapshot.ts`).
3. **`MEASURE.md` as a census of the rendered surface**, including `CLAUDE.md` and the
   profile. ColdStart's floor guard covers 55% of the floor it is named for, which is why
   every trim in that tree today is estimated rather than proved.
4. **A firing-artifact requirement** for every hook and every skill. Green CI has already
   hidden an unfinished install once.

### Census target

| Item | Bytes |
|---|---|
| `CLAUDE.md` | ~2,500 |
| profile, distilled | ~1,200 |
| 4 routers | ~2,850 |
| 3 wrappers | ~1,000 |
| 3 agents | ~989 |
| pointer / orientation payload | ~800 |
| **Total** | **~9,340** |

The memory model adds **0 B** beyond the pointer already counted: the three index files and
their folders are cold, read on demand, never injected. Under the declared 12,000 B with
room, at roughly **a quarter** of ColdStart's 38,616 B. If the build lands at 12,000 B,
something on the drop list came back and the ledger should say which.

## Build state

> Updated 2026-08-21. The line below used to say "not started", which stopped being true the
> same day. It is kept current here rather than in a second status file, because a status file
> beside a spec is a status file that disagrees with it by the end of the week.

**Three of seven sections built**, and the repo is public.

| # | Section | State |
|---|---|---|
| 1 | `memory-model` | done — three indexes, three folders, `tools/index.py` derives the indexes by scanning |
| 2 | `commands` | sessions 1-3 done; session 4 blocked on displacing the user-level v1 skills |
| 3 | `resident-surface` | not started. **The largest remaining gap**: there is no `CLAUDE.md`, no routers, no agents |
| 4 | `safety-floor` | done — `hooks/pre-tool-floor.sh`, three deny categories, 46 fixtures, firing artifact on file |
| 5 | `verify` | done — `tools/verify.py`, three checks, each shown going red on a planted defect |
| 6 | `install` | session 1 done, session 3 partly done (hooks + settings merge, pulled in by section 4). No uninstall, no `--weight` |
| 7 | `measure` | not started |

Two things landed that this ledger did not predict, both recorded in `decisions/`:

- **A fourth secrets rule**: staging credential material into git, not only reading it. Reading
  leaks to a transcript on this machine; staging leaks to every fork and cache of the remote,
  permanently, and rotation is the only remedy.
- **A SessionStart hook** that injects the pointer unasked. The census already budgeted ~800 B
  for an "orientation payload"; this is that line item, measured at 862 B, and it is what makes
  the one thing this harness is for true when `/coldstart` is *not* typed.

The resident surface currently measures **2,540 B, 21% of the declared 12,000 B**, with the three
largest predicted items (`CLAUDE.md`, the profile, the routers) still unbuilt. `tools/verify.py`
prints the number; it is not a `MEASURE.md` census yet, which is section 7.
