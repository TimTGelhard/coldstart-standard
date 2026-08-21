---
name: prep
description: Plan a section of this harness — declare prep mode on the pointer, scope the section to one sentence, break it into 2-5 sessions, and write one work file under docs/work/ that tools/index.py accepts. Plan files only, never code.
---

# prep — the planning pass

The third of the three commands. `/coldstart` opens a session, `/done` closes one, and this is
where a session comes from in the first place: a section of `docs/PROJECT_PLAN.md` becomes one file
under `docs/work/` holding 2-5 sessions, each startable cold by an agent that reads the pointer and
nothing else.

`docs/FORMAT.md` sections 2, 3 and 4 are the contract for what you write. This skill is the pass
that produces it. Run the steps in order.

**The pass writes plan files and nothing else.** No code, no config, no fixture. A planning session
that starts building has stopped planning, and the work file it was writing is now the thing nobody
finished. If the plan is obvious enough to just build, say so and let the operator run `/coldstart`
against it.

## 1. Declare the mode

    sed -i '' -e '1,/^---$/s/^mode: .*/mode: prep/' docs/PROGRESS.md

This is the one named exception to `FORMAT.md` section 1 rule 1, which makes `/done` the pointer's
single writer. `/prep` writes `mode` and **touches none of the other six fields**. The reason is
narrow and so is the exception: a safety floor reads `mode` off disk while the session runs, so a
planning pass has to be able to declare itself before it does anything.

If the front matter carries no `mode` line, add one directly beneath `active_work` — an absent
`mode` resolves to `build`, which is the thing you are declaring you are not.

Then prove you changed one line and not seven:

    git diff -U0 docs/PROGRESS.md

One `-mode:` and one `+mode:`, or one added line. Anything else is a pointer you have to put back
before continuing.

From here on the floor is reading that field, and it denies any shell it cannot prove read-only for
the rest of the pass. That constraint is why the rest of this skill is shaped the way it is: you
write plan files with an editor and you do not reach for a tool. If the pass finds itself needing to
run something, the work is a build session and this is not one.

At the end of the pass the tree is left in `prep`. `/done` writes `build` back when the planning
session closes, because the close is the pointer's whole writer and it composes all seven fields
from scratch. If a pass is abandoned rather than closed, the `mode` line is put back to `build` with
an editor — the shell is denied, so a `sed` will not do it.

## 2. Scope the section

Name the section, from `docs/PROJECT_PLAN.md` if it is already ordered there, or from what the
operator asked for. Then write two lines before anything else:

- **Goal**, one sentence. If it needs an "and", it is two sections; say so and pick one.
- **Done when**, one sentence naming the observable state that ends the section — a command that
  exits 0, a file that exists and parses, a behaviour that fires. Not "the section is complete".

Then read what the section builds on. The pointer's `reading` list is your ceiling here too, and a
read outside it is named out loud when it happens. `docs/DECISIONS.md` is the one index worth
walking during a prep pass, because planning against a decision already on file is the failure this
harness exists to prevent.

## 3. Settle what is settled, and surface what is not

Two blocks go into the work file, above the sessions.

**Settled at plan time** — calls the operator made before the plan was written, recorded so the
sessions build to them rather than re-opening them. Each one gets a sentence of *why*, because a
call without its reason gets re-litigated by the next cold session. The section's first or last
session files them into `docs/decisions/` at its close.

**Open, and owed a human answer** — questions the plan cannot settle alone. Name the session that
hits each one, and give your recommendation with its reason.

**Never silently pick.** An open call that the plan quietly resolves is a decision made by whoever
happened to be typing, filed nowhere, discovered later by the session it breaks. Ask the operator
when the pass reaches it, or write it into this block and name the session that must ask.

## 4. Break it into sessions

Two to five. One is a section that did not need planning; six is a section that is two sections.

Each session is one sitting for one agent with a fresh context: it has a single goal that survives
the "and" test, a read list of two to four files, build steps that land on named paths, and a verify
list it can run itself. Order them so each one leaves the tree working — a session that only makes
sense once the next one lands is half a session, and it should be merged with its other half.

Fill `templates/SESSION.md` for each. The template holds the shape; this skill holds the judgement.

### Work shapes

The shape sets the default session break and the trap to plan around. Pick one and say which.

| Shape | Sessions usually break by | Hard rule | The trap |
|---|---|---|---|
| Build | layer, then the thing that proves the layer fires | the last session is a proof, not a polish | planning the happy path and discovering the wiring at session 4 |
| Audit | one dimension per session | the audit writes findings, never fixes | fixing as you find, so nothing is measured and the diff is unreviewable |
| Refactor | one seam per session, behaviour held constant | a green check before and after each session | changing behaviour under cover of a refactor |
| Migration | inventory, then transform, then the cutover | the old path stays live until the new one is proved | a cutover session with no rollback named |
| Investigation | one hypothesis per session | each session ends with the hypothesis killed or confirmed | open-ended reading with no session that ends |
| Research | source sweep, then a decision session | the last session decides, in writing | reading forever because no session was the deciding one |
| Cleanup | one category per session | delete, do not archive | tidying into a new structure nobody asked for |

### The no-generic-verify rule

A session entry whose verify list says "test it works", "confirm it is correct" or "check the file
is right" is **not finished**, and it is the thing that turns `/done` into a rubber stamp: the close
runs the list literally, so a list that cannot be run literally is a close that passes on reading.

Every verify item names either a command with an exit code, or a file plus the value it must hold.
At least one item is the negative case — plant the failure and confirm the thing refuses — because a
check that has only ever seen green does not know it can go red.

Good: `python tools/index.py --check` exits 0 · the pointer carries all seven fields and none is a
placeholder · with a failing check planted, `/done` leaves `Status` unchanged.

Bad: the skill works · the file is well-formed · the loop runs end to end.

## 5. Write the work file

`docs/work/NN-<section-slug>.md`, `NN` zero-padded and one file per **section**. The front matter is
the four fields every content file carries:

    ---
    title: <human, sentence case, no trailing punctuation>
    subject: <one line, at most 120 chars, no trailing full stop — the generator carries it verbatim
              into the index, so write it to be read out of context>
    topic: <the filename stem minus the NN- prefix, kebab-case, and the generator checks it>
    updated: <YYYY-MM-DD>
    ---

Then the section heading, the goal and done-when lines, the two blocks from step 3, and the session
entries. Every session block carries `**Status**: pending` and a one-line `**Goal**` — those two are
what `tools/index.py` parses, and a file missing either is a hard error, not a skip.

**You cannot run the generator to check this, and you do not need to.** With `mode: prep` on disk
the safety floor denies any shell it cannot prove read-only, and `python tools/index.py --check` is
not provably read-only even though it writes nothing. That is the floor working as designed, not an
obstacle to route around.

So the file is checked by reading it against the contract, and by the close minutes later. `/done`
regenerates before it writes anything, so a malformed work file stops that close with a
`FormatError` naming the file, before the pointer moves. What you check by eye here is the short
list the generator is strict about: four front-matter fields present, `topic` equal to the filename
stem minus the `NN-` prefix, `subject` one line of at most 120 characters, every session heading in
the form `## Session N — <name>`, session numbers unique within the file, and every session block
carrying both `**Status**` and `**Goal**`.

## 6. Hand back

**Do not run `python tools/index.py`.** `/done` is its single caller, and the queue in
`PROGRESS.md` stays stale until this planning session closes — minutes later. A second caller is a
second thing that can disagree with the folders, and the property that makes an index line
trustworthy without opening the file behind it is that exactly one writer produces it.

**Do not write the pointer's other six fields.** The next session's `active_work`, `next_action` and
`reading` are composed by `/done` from scratch at the close, against the file you just wrote.

Then say, in three or four lines: the section, its goal sentence, how many sessions and what each
one makes, and any open call still owed a human answer. Point at `/done` to close the planning
session, which is what puts the new sessions into the queue and the tree back into `build`.
