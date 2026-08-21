---
title: Memory model
subject: three indexes over three folders, indexes derived by scanning, and the machinery deliberately not built
topic: memory-model
updated: 2026-08-21
---

# Decisions — memory model

## Three index files over three folders

**Decided**: 2026-08-19, amended 2026-08-21

`docs/` holds `PROGRESS.md`, `DECISIONS.md` and `FIXES.md` as indexes over `work/`, `decisions/`
and `fixes/`. One mechanic applied three times, so there is one rule for the model to follow and
one script to write, and no file behaves differently from its neighbours.

An index file holds status and a pointer and structurally cannot hold detail, so it cannot
bloat. The folder beside it holds the content, clustered by topic, so no single file grows
without bound. The on-disk contract is [../FORMAT.md](../FORMAT.md).

## The warehouse is kept, as cold storage (supersedes the outright drop)

**Decided**: 2026-08-21

Old position, 2026-08-19: the feature ledger dropped ColdStart's warehouse outright.

New position: stored knowledge is kept. It is cold and costs zero resident bytes. What made
ColdStart's warehouse expensive was the machinery around the storage, and the machinery is
separable from the storage. The drop was reasoning about the wrong cost.

## Indexes are derived, never maintained

**Decided**: 2026-08-21

At `/done` a script scans each folder, reads each file's title and one-line subject, and rewrites
the index above it. An index cannot go stale or disagree with its folder, because it is a
function of it.

This single choice removes the canonical-versus-projection split and every check that would
police it. ColdStart needed `state-consistency` and `warehouse-maps` precisely because it
generated its indexes from a separate state file rather than from the content.

## There is no separate state file

**Decided**: 2026-08-21

The folders are canonical. ColdStart's `LIFECYCLE.json` is the thing being deliberately not
built. Nothing derives from anything except the files themselves.

## Storage is cold by default

**Decided**: 2026-08-21

Nothing under `docs/` is ever loaded wholesale. A session reads the pointer, then walks one index
to at most one or two files. The consequence is that the whole memory model adds 0 B resident
beyond the pointer block that is already counted.

## Clustering follows a rule, and it is a nudge rather than a gate

**Decided**: 2026-08-21

At close, an item is filed into the existing topic file that fits; a new topic file is created
only when none does; a long topic file splits by sub-topic. Nothing blocks on this, because a
clustering rule with teeth becomes a filing ritual, which is the thing this model exists to
replace.

## The fixes queue is open-only

**Decided**: 2026-08-21

A shipped fix is deleted, not archived. Git is the archive. There is no done section, ever,
because a done section is where a queue goes to become a log nobody reads.

## The pointer has seven fields, one writer, and no history

**Decided**: 2026-08-21

Carried from ColdStart's own notation spec, whose lesson is structure over discipline: v1 asked
its entries to be terse and they arrived three to six times over cap. So each field is named and
capped, the close tool writes them, and a recap has nowhere to go but git. There is deliberately
no `prior_section` and no history field. ColdStart's `PROGRESS.md` reached 26 KB of which roughly
79% was dead recap while still passing its own checks; removing the field is what makes that
impossible rather than merely discouraged.

The pointer is rewritten whole at every close, never appended to.

## Deliberately not carried from ColdStart

**Decided**: 2026-08-21

`LIFECYCLE.json` and every generated projection · `registry.tsv` and the ownership manifest ·
rooms, boxes and the plan/decisions/gotchas taxonomy · nested per-room `MAP.md` files · container
caps, card caps and the room-split ritual · `done.py`'s 75-module tool family · the check-classes
whose subject is any of the above.

Each is dropped for the same reason: it exists only to police a split this model does not have.

## An index line carries its source field verbatim

**Decided**: 2026-08-21

`tools/index.py` renders the `subject`, `Goal` and `Subject` fields exactly as the content file
writes them. It does not re-punctuate, re-case or paraphrase. The alternative is a generator with
an editorial opinion, which makes an index line something you can no longer trace to a line in a
file, and makes two runs of the tool differ whenever the opinion changes.

The consequence lands on the author, not the tool: a one-line field is written to read as an
index line, which means no trailing full stop and one sentence rather than two. Session 1's
hand-written indexes had silently applied that style while the source files did not carry it, so
the first generated run differed from them in six lines. The resolution was to fix the source
fields, not to teach the tool to trim, and the indexes then matched the hand-written ones byte
for byte. That match is the evidence session 1's format was implementable as written.

## The generated region is bounded by a marker, so a hand-owned header can sit above it

**Decided**: 2026-08-21

Each index file preserves everything through the line containing `GENERATED BELOW THIS LINE` and
replaces everything after it. `PROGRESS.md` therefore preserves on both sides: the pointer front
matter and the header comment above, the queue and log below. Prose a human wants to keep in an
index file goes above the marker, which is where the "sections 2-7 are planned just in time"
paragraph moved at this session.

`index.py --check` writes nothing and exits non-zero when any index is out of date. That is the
form the `/done` no-op assertion takes, so the close does not have to diff files itself.
