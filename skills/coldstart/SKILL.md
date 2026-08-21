---
name: coldstart
description: Open a session in this harness cold — read the seven-field pointer, open the one work file it names, read the declared reading list in order, and stop. Treats that list as a ceiling and refuses to start work over a non-empty blockers field.
---

# coldstart — the resume

`docs/FORMAT.md` section 8 is the contract; this skill is its implementation. Run the steps in
order and stop where step 4 says to stop.

The whole point is that storage is cold. The folders under `docs/` are large and the resident cost
of a resume is one front-matter block, because a session walks to a file and never loads a folder.
Every rule below exists to keep that true under pressure.

## 1. Read the pointer

The YAML front matter at the top of `docs/PROGRESS.md`, and nothing else in that file yet. Seven
fields: `active_work`, `mode`, `next_action`, `blockers`, `reading`, `updated`, `resume_note`.

Read it by extracting the block, not by paging the top of the file:

    sed -n '/^---$/,/^---$/p' docs/PROGRESS.md

`head -40` or `sed -n '1,40p'` pulls the generated queue in behind the front matter, which turns
the pointer read into an unannounced index read. Two cold runs at session 2 both did exactly that.
The queue is the escape hatch below, entered deliberately when the question is "what else is
planned" — not absorbed by accident on the way past.

After reading them you already know what is being worked on, what to do next, and whether you may
start at all.

**A non-empty `blockers` stops the resume here.** Report what the blockers say, ask how to proceed,
and do not begin work, do not open `active_work`, do not start reading the list. A blocker is read
as "do not start; resolve or re-scope", and a resume that reads past its own blocker is how a
blocked session gets quietly worked on anyway.

An absent `mode` resolves to `build`. An empty `active_work` means the tree is between sections:
say so and point at `/prep`, which is where a section's work file is born. Never invent one.

## 2. Read `active_work`

One file, named by the pointer, opened directly. **No index is consulted to find it** — the pointer
already holds the path, and walking `PROGRESS.md`'s queue to rediscover a path you were handed is a
wasted file against the bound.

Inside it, the session being continued is the `## Session N` block whose `**Status**` is not `done`.
If several qualify, take the lowest-numbered one. If none does, the section is finished: say so and
point at `/prep` for the next one.

## 3. Read the declared read list

The pointer's `reading` field, in the order it is written.

**It is a ceiling, not a suggestion.** A read outside it is drift. Name it out loud at the moment it
happens — before the read, not confessed after it — with what you are opening and why the declared
list did not cover it. A silent overrun is the failure this rule exists to catch, and an overrun
that is announced is just a read.

The list is also an upper bound on what this context absorbs. A file on the list that the session
demonstrably does not need is not read for completeness.

## 4. Stop

Three steps, and the common case is two files plus the pointer. A session that has not answered its
question by here has a **pointer problem**, and the fix is to say so, not to keep reading.

Then announce, in three or four lines: the session goal in one sentence, the read list you
committed to, the blocker state, and the exit condition. If the goal sentence needs an "and", it is
two sessions — stop and say so rather than starting both.

## The escape hatch: one index, at most two files

When the session genuinely needs something the walk above did not reach, open **exactly one** of the
three index files, read the one or two lines that match, and open the files those lines name.

| Question | Index |
|---|---|
| why is it like this | `docs/DECISIONS.md` |
| what is known broken | `docs/FIXES.md` |
| what else is planned | the `PROGRESS.md` queue, below the marker |

**Never wholesale.** No `cat docs/decisions/*.md`, no glob read of a folder, no "load the docs tree
for context". A folder is storage, an index is the way in, and reading the folder to avoid reading
the index is the exact move this model exists to make unnecessary. Grep over a folder is fine,
because grep returns lines rather than files.

## The bound

The wrapper and this skill are the command being invoked, not tree reads, and they do not count
against the bound. What counts is what the walk opens under `docs/`.

A healthy resume respects **four files**: the pointer's file, the active work file, one index, and
one file that index names. Count them from your own reads and be able to say the number.

A resume that needs a fifth file is not a slow resume, it is a pointer defect — `next_action` too
vague, or `reading` naming the wrong file. Say which, and fix it in the session that finds it rather
than absorbing the cost every time.
