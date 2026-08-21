# FORMAT — the memory model, on disk

> Written at section 1 session 1, 2026-08-21, and implemented by `tools/index.py` at session 2.
> The contract came first and the tool followed it; where session 2 amended this file, the
> amendment is recorded in `decisions/memory-model.md`. Sections 8 and 9, the read protocol and
> the close protocol, were added at session 3.

The model is one mechanic applied three times: an **index file** that holds status and a pointer
and structurally cannot hold detail, and a **folder** beside it that holds the content, clustered
by topic. `PROGRESS.md` additionally carries the resume pointer at the top.

| Index | Folder | One index line is |
|---|---|---|
| `PROGRESS.md` | `work/` | one planned or completed session |
| `DECISIONS.md` | `decisions/` | one topic file |
| `FIXES.md` | `fixes/` | one open item |

Two of the three index at a finer grain than the file: a work file holds several sessions and a
fixes file holds several items, so the generator reads *inside* those files. `decisions/` indexes
at file grain, because a decision topic is the unit anyone looks things up by.

**The rule behind every cap below: structure, not discipline.** ColdStart v1 asked its entries to
be terse and they arrived three to six times over. So a field here is named, capped, and written
by a tool, and a recap has nowhere to go but git. The writer truncates at the cap and says so;
the verify check is a backstop, not the enforcement.

---

## 1. The pointer

The YAML front matter at the top of `docs/PROGRESS.md`, and the only part of this model that is
ever resident in a session. `/done` is its single writer.

```yaml
---
active_work: docs/work/01-memory-model.md
mode: build
next_action: section 1 session 1 — write docs/FORMAT.md, then seed the folders
blockers: []
reading: [SPEC.md, docs/ARCHITECTURE.md]
updated: 2026-08-21
resume_note: "planned but not started; the indexes are hand-written until tools/index.py exists"
---
```

| Field | Type | What it is for |
|---|---|---|
| `active_work` | repo-relative path | the one work file this session continues. Exactly one, or empty between sections |
| `mode` | `build` \| `prep` | what the session is allowed to do. Absent resolves to `build` |
| `next_action` | one line, <=120 chars | the next concrete step, specific enough to start on without reading anything else |
| `blockers` | list of one-liners | empty list when clear. A non-empty list is read as "do not start; resolve or re-scope" |
| `reading` | list of paths | the declared read list, and a **ceiling** on what the session reads, not a suggestion |
| `updated` | `YYYY-MM-DD` | when `/done` last wrote this block |
| `resume_note` | one sentence, quoted, <=160 chars | the human line a colleague would say out loud, which no field above carries. The only prose a human writes on the hot path |

Rules:

1. **One writer.** `/done` writes the pointer. A session may read it and may not edit it.
2. **Nothing below the pointer restates a field from it.** Duplication is how a pointer starts
   disagreeing with its own file. If a fact belongs to the pointer, the body does not repeat it.
   The queue's link column is not a restatement of `active_work`: it names every session's file
   because that is what an index does. What the body never carries is a row saying *this* is the
   active one, a copy of `next_action`, or a restated blocker.
3. **The pointer is rewritten whole, never appended to.** `/done` composes all seven fields
   from scratch every close. Nothing accumulates, so nothing has to be pruned later.
4. **There is no history field, and that is the point.** No `prior_section`, no recap, no
   "previously we". ColdStart v1's `PROGRESS.md` reached 26 KB of which 79% was dead recap while
   still passing its own checks. Removing the field is what makes that impossible rather than
   discouraged; git holds the history.
5. **Seven fields, and adding an eighth is a decision.** If something does not fit one of them,
   that is the signal it belongs in the active work file, not on the hot path.
6. **`tools/index.py` never touches this block.** It rewrites the queue section below it and
   leaves the front matter byte-identical. This is asserted by a test in session 2.
7. **Paths are repo-relative** and resolve from the repo root, so a check for link rot is a
   plain existence test. A reference may point outside the repo, either by escaping the root
   (`../../CHARTER.md`) or as an absolute path; such a target is machine-local, and `ghost-refs`
   reports it as unresolvable rather than failing, because a sibling tree's absence is not this
   repo's defect.

## 2. Content-file front matter

Every file in `work/`, `decisions/` and `fixes/` opens with the same four fields. This is what
the generator reads; a file missing any of them is a hard error, not a skip, because a file that
is silently absent from an index is invisible.

```yaml
---
title: Memory model
subject: three indexes, three folders, and why the indexes are derived rather than maintained
topic: memory-model
updated: 2026-08-21
---
```

- `title` — human, sentence case, no trailing punctuation.
- `subject` — **one line, at most 120 characters**, no line breaks. This is the text the index
  line carries, so it is written to be read out of context.
- `topic` — the kebab-case slug, and it **must equal the filename stem** (minus the `NN-` number
  prefix on work files). The generator checks this rather than trusting either side.
- `updated` — `YYYY-MM-DD`, the last substantive edit.

## 3. File naming

| Folder | Pattern | Example |
|---|---|---|
| `work/` | `NN-<section-slug>.md`, `NN` zero-padded, one file per **section** | `01-memory-model.md` |
| `decisions/` | `<topic-slug>.md` | `memory-model.md`, `commands.md` |
| `fixes/` | `<topic-slug>.md` | `family.md` |

Slugs are kebab-case ASCII. No dates, no author initials, no `v2` suffixes: a renamed topic is a
`git mv` plus a regenerate, and the index follows.

## 4. Item grammar inside a file

`work/` and `fixes/` are indexed per item, so their items carry a fixed shape the generator can
parse. `decisions/` is indexed per file and its internals are prose, with one convention.

### `work/` — one item per session

```markdown
## Session 2 — tools/index.py

**Status**: pending

**Goal**: the indexes stop being hand-written; one script scans each folder and rewrites the
index above it
```

`Status` is one of `pending`, `active`, `done`, `blocked`. `Goal` is one line and becomes the
index line's description. Everything else in the session block (files to read, build steps,
verify, output) is free-form and the generator ignores it.

### `fixes/` — one item per open thing

```markdown
## coldstart-minimal SPEC is stale

**Subject**: minimal's spec still carries the pre-amendment memory model

**Since**: 2026-08-21

**Closes when**: minimal's SPEC states the two-file version of this model, or records that it
diverges on purpose.

**Ref**: ../coldstart-minimal/SPEC.md

**Tag**: later
```

`Subject` and `Closes when` are one line each, at most 120 characters. `Ref` is optional and is a
repo-relative path in the **same addressing scheme as everything else here** — an item never gets
its own second way of naming where it lives. `Tag` is optional and is one of `blocked` or
`later`; its absence means plain open, so the common case carries no ceremony.

There is **no status field**, because the queue is open-only: presence is openness. A shipped fix
has its `##` block deleted, and when a topic file empties it is deleted too. Git is the archive.

### `decisions/` — one heading per decision

```markdown
## Indexes are derived, never maintained

**Decided**: 2026-08-21

The three index files are regenerated by scanning their folders ... (prose, as long as it needs)
```

A superseded decision is **not deleted**. Its heading gains `(superseded 2026-09-01)` and the
body keeps the old position plus one line saying what replaced it and why. The record exists so
nobody re-decides in the dark, and a deleted decision is exactly the one that gets re-made.

## 5. Index line grammar

Generated. Never hand-edited once `tools/index.py` exists.

**`PROGRESS.md` queue** — a table row per session, in file order then session order:

```
| 1.2 | memory-model s2 | tools/index.py derives the three indexes by scanning | pending | [work/01-memory-model.md](work/01-memory-model.md) |
```

Columns: `#` (section.session) · session name · the `Goal` line · `Status` · link to the work file.

The queue lists **only sessions that are not `done`**. Completed ones do not accumulate as rows:
when every session in a work file is `done`, the file contributes exactly one row to the `## Log`
section below the queue, naming the section and the date it closed. So the queue is bounded by
work remaining and the log by section count, and both are still a pure function of the folder.
The per-session detail of finished work stays in its work file, where it always was.

A log row is `| <NN> | <section slug> | <the work file's `subject`> | closed <YYYY-MM-DD> | <link> |`,
where the date is the file's `updated` at the moment its last session went `done`.

**`DECISIONS.md`** — one line per file in `decisions/`, sorted by topic slug:

```
- **Memory model** — three indexes, three folders, and why the indexes are derived · [decisions/memory-model.md](decisions/memory-model.md) · 4 entries · 2026-08-21
```

Fields in order: `title` · `subject` · link · count of `##` headings · `updated`.

**`FIXES.md`** — one line per open item, sorted by topic slug then order of appearance:

```
- **coldstart-minimal SPEC is stale** — minimal's spec still carries the pre-amendment memory model · [fixes/family.md](fixes/family.md) · since 2026-08-21 · later
```

Fields in order: item heading · `Subject` · link · `Since` · `Tag` if present.

Every rendered field is carried **verbatim** from its source line. The generator does not
re-punctuate or paraphrase, so a one-line field is authored to read as an index line: one
sentence, no trailing full stop. See `decisions/memory-model.md`.

**The generated region is marked.** Each index file ends its header comment with the literal line
`GENERATED BELOW THIS LINE`. Everything above that marker (the title and the comment) is preserved
verbatim; everything below it is replaced wholesale on every run. `PROGRESS.md` is the one file
with content the generator must preserve on *both* sides: the pointer front matter above, and the
marker's region below. Ordering is deterministic and sorting is by ASCII
slug, so a second run on an unchanged tree is byte-identical.

`python tools/index.py` rewrites the three files; `python tools/index.py --check` writes nothing
and exits non-zero when any of them is out of date, which is how `/done` asserts its regeneration
is a no-op. A content file that breaks any rule in sections 2 to 4 is a hard error naming the
file, and no index is written on that run.

## 6. Topic clustering

1. At close, a new decision or fix is filed into the **existing topic file that fits**. A new
   topic file is created only when none does.
2. A topic file that grows past roughly 200 lines splits by sub-topic: `auth.md` becomes
   `auth-sessions.md` + `auth-oauth.md`. The old file is removed by the split, not left as a
   stub.
3. This is a **nudge at `/done`, never a gate**. Nothing blocks on clustering, because a
   clustering rule with teeth becomes a filing ritual, which is the thing this model replaces.

## 7. What this format deliberately has no room for

There is no separate state file. The folders are canonical and the indexes are a function of
them, which is why there is no canonical-versus-projection split here and no check that polices
one. There is no `done` section in `FIXES.md`, no per-folder `MAP.md`, no ownership manifest, and
no cap on container size beyond the split nudge above.

## 8. The read protocol

What a session reads at start, in what order, and where it stops. This is the whole of what makes
storage cold: the folders are large and the resident cost is one front-matter block, because a
session walks to a file and never loads a folder.

1. **Read the pointer.** The front matter of `docs/PROGRESS.md`, and nothing else in that file
   yet. Seven fields, and after them the session already knows what it is working on, what to do
   next and whether it may start at all. A non-empty `blockers` stops here: report and ask, do not
   begin.
2. **Read `active_work`.** One file, named by the pointer, opened directly. No index is consulted
   to find it, because the pointer already holds the path. Inside it, the session block whose
   `Status` is not `done` is the session being continued.
3. **Read the declared read list.** The `reading` field, in the order it is written. It is a
   **ceiling**, not a suggestion: a read outside it is drift, and the session names it out loud
   when it happens rather than after.
4. **Stop.** Three steps, and the common case is two files plus the pointer. A session that has
   not answered its question by here has a pointer problem, and the fix is to say so, not to keep
   reading.

**One index, at most two files.** When the session genuinely needs something the walk above did
not reach, it opens exactly one of the three index files, reads the one or two lines that match,
and opens the files those lines name. `DECISIONS.md` when the question is "why is it like this",
`FIXES.md` when the question is "what is known broken", the `PROGRESS.md` queue when the question
is "what else is planned".

**Never wholesale.** No `cat docs/decisions/*.md`, no glob read of a folder, no "load the docs
tree for context". A folder is storage, an index is the way in, and reading the folder to avoid
reading the index is the exact move this model exists to make unnecessary. Grep over a folder is
fine, because grep returns lines rather than files.

The upper bound a healthy resume respects is **four files**: the pointer's file, the active work
file, one index, and one file that index names. Session 3's cold-resume proof counts them from the
resuming agent's own report, which is what makes the bound a measured property rather than a wish.

## 9. The close protocol

What `/done` does to the memory model, in order. This is the contract section 2 implements; it is
written here first so that section builds to a spec rather than inventing one.

1. **Verify before writing.** Run the active session's own `Verify` list and report the result.
   Red or paused does not close: the session stays open and the pointer keeps pointing at it.
2. **Update the content files, not the indexes.** The session's block in its work file goes to
   `Status: done` and gains a `Closed:` date. New decisions are filed into the existing topic file
   under `decisions/` that fits, or a new one when none does. New known-open items are added to
   `fixes/`, and anything shipped this session has its `##` block deleted from there.
3. **Regenerate.** `python tools/index.py` rewrites `PROGRESS.md`'s queue and log, `DECISIONS.md`
   and `FIXES.md` from the folders. The session never hand-edits an index, and the pointer block
   is untouched by this step.
4. **Assert the regeneration is a no-op.** `python tools/index.py --check` exits zero. A non-zero
   exit here means step 2 wrote something the format does not describe, and it is fixed before the
   close continues rather than committed and noticed later.
5. **Write the pointer, whole.** All seven fields composed from scratch: `active_work` for the
   next session (or empty between sections), `mode`, a `next_action` specific enough to start on
   cold, current `blockers`, the `reading` ceiling for the next session, today's `updated`, and one
   sentence of `resume_note`. Nothing is appended and nothing is carried over unexamined.

   **The close never writes a restrictive `mode`.** `mode` says what the *running* session may do,
   and the safety floor reads it the instant it lands on disk. A close that writes `mode: prep`
   here has therefore just denied its own remaining steps, because step 7's commit is a write and
   the tree is now a planning tree. So the close leaves `mode: build` (or omits it, which resolves
   the same way) and the next session declares its own mode when it starts. Section 3 discovered
   this the hard way: the pointer it wrote locked the tree before the commit, and the last two
   steps had to be unblocked by hand.
6. **Nudge on clustering, do not gate.** If a topic file has grown past roughly 200 lines, say so
   and propose the split. The close does not block on it.
7. **Commit.** The session's declared `Output:` line is the commit message. Git is the history,
   which is what lets the pointer carry none.

`/done` is the single writer of the pointer and the single caller of `tools/index.py`. Both
statements are what let a reader trust an index line without opening the file behind it.
