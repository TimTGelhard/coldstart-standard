---
title: Floor firing artifact
subject: each deny category refusing a real command through the installed hook, captured verbatim
topic: 04-s3-floor
updated: 2026-08-21
---

# Artifact — the floor firing

> Section 4 session 3, 2026-08-21. Captured by running payloads through
> `.claude/hooks/pre-tool-floor.sh` — the installed copy the host actually invokes, not the
> source tree beside it and not the test suite. `SPEC.md` Adds 4 asks for a firing artifact
> rather than a passing test, because green CI has already hidden an unfinished install once
> in this family.

Each block is the command sent and the refusal returned, verbatim, with nothing edited.

## secrets

Pointer `mode: build`.

```
$ cat .env

floor:secrets -- this reads credential material into the transcript.
Structural, not advisory: anything a tool prints is in the context window for the rest of the session and in the transcript on disk afterwards, and there is no way to take it back out.
The legitimate path: read the KEYS, not the values -- `cut -d= -f1 .env` lists the variable names, `test -n "$VAR" && echo set` proves one is populated without printing it. If a value genuinely has to be seen, the operator reads it themselves outside the session.
```

## secrets (staging)

Pointer `mode: build`.

```
$ git add .env

floor:secrets -- this puts credential material into git history.
Structural, not advisory: a secret that reaches a remote is public from that moment, and deleting the commit does not take it back. The object survives in every fork, clone and cache, so the only real remedy is rotating the credential.
The legitimate path: add the file to `.gitignore` first, commit that, and stage the rest by name.
```

## destructive

Pointer `mode: build`.

```
$ rm -rf $PROJECT_ROOT

floor:destructive -- a recursive force-delete of `$PROJECT_ROOT`, an unexpanded variable -- if it is unset the shell deletes from the root.
Structural, not advisory: this class of command has no undo, so the check has to happen before it runs rather than in review afterwards.
The legitimate path: name the paths explicitly and let the shell fail on a typo, rather than recursing from a root or an unexpanded variable.
```

## mode

Pointer `mode: prep`.

```
$ npm run build

floor:mode -- the pointer says `mode: prep`, and `npm` is not on the read-only list. Every segment of a compound command has to be a known read, so two safe halves joined by an unknown third still stops here.
Structural, not advisory: a planning pass that writes code is how a plan stops describing the work and starts being the work, which is the failure this harness's own /prep was built to make impossible.
The legitimate path: finish the plan, then set `mode: build` in the front matter of docs/PROGRESS.md -- a declaration made on the record, not a flag that suppresses the check. /done writes that field at close.
```

## False positives, counted

The number that decides whether a floor survives daily use is not how much it stops, it is how
much it stops that it should not have. Counted across sessions 1 to 3: **two**, both found
during calibration and both fixed rather than accepted.

| What was refused | Why it was wrong | Fix |
|---|---|---|
| `rm -rf /tmp/scratch/build` | the rule keyed on the target being absolute, and most absolute paths are ordinary | replaced the regex with an argv analyser that names the forbidden targets (`/`, `~`, `$HOME`, `.`, `*`, one-segment roots, unexpanded variables) |
| `cut -d= -f1 .env` | this is the command the secrets refusal itself recommends as the legitimate path | exempted the key-only read; `-f2` and a bare `-f1` with no `=` delimiter still refuse |

The second one is the one worth remembering. A floor that forbids the escape hatch printed in
its own refusal text is a floor the operator stops believing on the first day, and it would
have shipped if the rules had been read rather than run.

Both are fixtures now (`allow-rm-tmp-path`, `allow-cut-keys-only`), so the calibration is held
by the suite rather than by whoever remembers the incident.

## What this artifact does not show

The cold-agent check the session plan asked for — a fresh agent with no history, given one
destructive-sounding instruction, stopped by the hook mid-task — was not run. The refusals above
were all provoked by the author knowing the rule, which proves the mechanism and not the
ergonomics. Recorded as open in `fixes/lifecycle.md` rather than quietly dropped.
