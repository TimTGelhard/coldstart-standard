# Session entry scaffold

One `## Session N` block per session inside `docs/work/NN-<section-slug>.md`. `/prep` fills this
shape rather than recomposing one each time, and `tools/index.py` parses the two bold fields it
requires (`Status`, `Goal`) out of it. Everything below `Goal` is free-form to the generator and
load-bearing to the human: it is what a cold session reads to start.

The whole entry stays under 100 lines. If it does not fit, the session is two sessions.

---

## Session N — <two or three words, the thing this session makes>

**Status**: pending

**Goal**: <one sentence, no "and". It becomes the queue's description line, so write it to be read
out of context: what this session makes true that was not true before>

**Files to read**
- `<repo-relative path>` (<which part, and why this session needs it>)
- <2-4 entries. This list becomes the next pointer's `reading` ceiling, so it is what the session
  may read, not everything that might be relevant>

**Build steps**
1. `<path to write>`: <what it holds and why it is a separate file>
2. <numbered, ordered, each one a thing that lands on disk>
3. <name the delegation where the step is a broad read, an independent parallel strand, an audit of
   the diff, or a noisy build/test loop>
4. Capture the firing artifact under `docs/work/artifacts/NN-sM-<slug>.md`, when the session builds
   something that fires.

**Files to write**
- `<every path the build steps land on, listed flat>`

**Verify**
1. <a command with an exit code, or an observation with a named file and a stated expected value>
2. <the negative case: plant the failure and confirm the thing refuses>
3. <2-4 checks. "test it works" is not a check; see the skill's no-generic-verify rule>

**Output**: <the commit message, in the imperative present, stating what became true>

---

## Filling notes

- `Status` is one of `pending`, `active`, `done`, `blocked`. `/prep` writes `pending`; only `/done`
  writes `done`, and it adds `**Closed**: YYYY-MM-DD` beneath the status line.
- The heading is `## Session N — <name>` with the em dash. The generator requires `Session N` and
  takes the name from what follows.
- Session numbers start at 1 within the file and never repeat.
- Delete the angle-bracket prompts. A shipped work file carries no placeholders.
