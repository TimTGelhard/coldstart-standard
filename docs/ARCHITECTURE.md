# ARCHITECTURE — coldstart-standard

> Drafted at `/prep`, 2026-08-21. High-level only: layout, boundaries, and the decisions that
> later sections are not allowed to quietly re-open.

## Stack

Markdown (the instruction surface) · bash (hooks) · Python 3.12+ stdlib only (the one tool).
No datastore, no runtime dependencies, no network on the hot path. Same stack as ColdStart,
because the lesson that produced it (a harness with dependencies is a harness that breaks on a
fresh machine) is carried, not re-litigated.

## Installed layout

Everything lives inside the project. There is no parallel root and no `COLDSTART_ROOT`-style
environment variable to resolve.

```
<project>/
  .claude/
    CLAUDE.md            the resident surface, read every session
    settings.json        hook registration only
    commands/            coldstart.md · prep.md · done.md
    skills/              4 routers, read on demand
    agents/              3 definitions
  .coldstart/
    hooks/floor.sh       PreToolUse safety floor
    tools/index.py       regenerates the three indexes by scanning
    tools/verify.py      3 checks
    chapters/            12-15 files, read on demand
    VERSION
  docs/
    PROGRESS.md          pointer + one line per session   -> work/
    DECISIONS.md         one line per topic               -> decisions/
    FIXES.md             one line per open item           -> fixes/
    work/                one file per session
    decisions/           clustered by topic
    fixes/               clustered by topic
```

**Decision: in-project install, not a parallel root.** ColdStart resolves every path from
`COLDSTART_ROOT`, which buys one shared copy across projects and costs a resolution layer, an
installer that writes two trees, and a live-root hazard that broke its own hermetic test rig.
`standard` takes the opposite trade: one copy per project, updated by re-running install. The
harness becomes a normal part of the repo, versioned with it, and reversible by deleting two
directories. The cost is real and named: N projects means N copies to update.

**Decision: `.coldstart/` is separate from `.claude/`.** `.claude/` holds only what the host
reads. Everything the harness owns sits beside it, so uninstall is unambiguous and a host change
never lands in harness files.

## The memory model

The load-bearing part of the product. Full statement in `../SPEC.md`; the architectural facts:

- **One mechanic, applied three times.** An index file holds status plus a pointer and cannot
  hold detail. The folder beside it holds content, clustered by topic.
- **Indexes are derived, never maintained.** `tools/index.py` scans each folder, reads each
  file's title and one-line subject, and rewrites the index above it. An index cannot disagree
  with its folder because it is a function of it. This one choice removes the entire
  canonical-versus-projection problem and every check that would police it.
- **There is no separate state file.** The folders are canonical. ColdStart's `LIFECYCLE.json`
  is the thing being deliberately not built.
- **Storage is cold.** A session reads the pointer, then walks one index to one or two files.
  Nothing under `docs/` is ever loaded wholesale, which is why the memory model costs 0 B
  resident.

### The pointer

The top of `PROGRESS.md`, and the only resident part of the model. Fields: active work file,
next action, blockers, read list, one human line, updated date. Hand-written by `/done`, which
is the only writer.

## Boundaries

| Boundary | Rule |
|---|---|
| Who writes the indexes | `tools/index.py`, called by `/done`. Never a human, never the model directly |
| Who writes the pointer | `/done` only |
| Who writes content files | the model, during a session, under the active work file's scope |
| What the hook does | denies. It never injects and never edits |
| What `verify.py` checks | link rot, byte budgets, hooks-actually-fire. Nothing about content quality |

## Verify

Three checks, and each ships a test that makes it fail on an injected defect. A check that
cannot be made to fail is not a check (carried from ColdStart, cheaply).

1. `ghost-refs` — every path referenced in `docs/` resolves.
2. `byte-budgets` — the rendered resident surface against the declared budget.
3. `hooks-registered` — the floor hook is wired and has a real firing artifact.

## Self-hosting

`standard`'s own build uses `standard`'s memory model from session 1, not ColdStart's. This tree
therefore carries `PROGRESS.md` + `work/` + `decisions/` + `fixes/` and no `LIFECYCLE.json`.
Two reasons: a repo whose own docs contradict its spec is a repo nobody trusts, and dogfooding
is the cheapest way to find out whether the model actually works. Until `tools/index.py` exists
(section 1, session 2), the indexes are hand-written; after it, they are generated.

## Open, and deliberately deferred

- **`--weight minimal|standard` in the installer.** Specced as an add; it only becomes real once
  `minimal` exists. Section 6 builds the selector with one arm.
- **`adopt`.** A real facility, deferred until `standard` runs on a real project.
- **Chapter count.** "12-15, on demand" is an estimate. The actual cut happens in section 3 and
  is reported, not assumed.
