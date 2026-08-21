---
title: Safety floor
subject: the two open calls the plan left, the fourth rule the build added, and the one place the floor fails open
topic: safety-floor
updated: 2026-08-21
---

## The refusal is JSON with an explicit deny, not a bare exit code

**Decided**: 2026-08-21

The section plan left this open and recommended JSON. Built as recommended.

A `PreToolUse` hook can refuse two ways: exit 2 with text on stderr, or a JSON decision on
stdout. The bare exit code carries no structure, so the model sees "that was refused" and
nothing about which of three rules fired or what the allowed version of the command would
have been. The whole working part of a floor is the refusal text: a refusal that does not
name the legitimate path gets routed around inside the same session, and now the operator
believes there is a floor when what there is, is an obstacle.

The emitted object carries `hookSpecificOutput.permissionDecision: "deny"` with a reason,
and the older `decision`/`reason` pair beside it, so a host on either shape refuses rather
than silently allowing.

Every refusal has the same three parts, and the test asserts the third: what fired
(`floor:secrets`, `floor:destructive`, `floor:mode`), why the rule is structural rather
than advisory, and what the legitimate path is.

## Registered in the project's own .claude/settings.json, emitted by install.sh

**Decided**: 2026-08-21

Also as the plan recommended, and the reason is the one section 2 session 4 found the hard
way: with no registration of its own, this tree was governed by ColdStart v1's global
install, so any artifact showing a refusal would have been evidence about the neighbour's
floor rather than this one's.

The registration's source of truth is `hooks/settings.json`, tracked. `install.sh` merges it
into `.claude/settings.json`, which is gitignored as a build output. Committing both would
leave two files claiming to be the registration with no way to tell which one the host read
— the same canonical-versus-projection split the memory model was built to avoid, reappearing
in the install.

The merge is a merge, not an overwrite. A real project's `settings.json` carries permissions,
env and possibly another team's hooks, and an installer that replaces it wholesale eats
someone's work the first time it runs outside this repo. Only entries pointing at this
harness's own script paths are replaced, so a second run is a no-op rather than a duplicate,
which is asserted by hashing the file across two runs.

## A fourth rule: staging a secret into git

**Decided**: 2026-08-21

The plan named three categories. The build added a fourth check inside the secrets category,
because reading and staging are different exposures and staging is the worse one.

A secret read into the transcript is bad and local to this machine. A secret that reaches a
remote is public from that moment and stays public after the commit is deleted, because the
object survives in forks, clones, caches and the provider's own rebuild of the fork network.
Rotation is the only real remedy and it costs the operator an afternoon.

Two shapes are refused: naming a credential file in a `git add`/`commit`/`stash`/`rm`, and
bulk staging (`git add -A`, `git add .`) while an unignored credential file is sitting in the
project root. The second is the one that actually happens, because nothing in the command
names the file.

The bulk rule is scoped to the root and to one loose `.gitignore` pattern on purpose. A deeper
scan means walking the tree on every Bash call, and a floor that costs a directory walk per
command is a floor that gets removed for being slow. It is also where the accident lives:
`.env` sits at the root, and that is where `git add -A` picks it up.

## The floor fails open when it cannot run, loudly

**Decided**: 2026-08-21

If `python3` is not on PATH, or `floor.py` is not beside the shim, `pre-tool-floor.sh` prints
`THE FLOOR IS NOT RUNNING` to stderr and exits 0. The same applies to a payload that will not
parse as JSON.

This is the one place the floor is not enforced, and it is written down here rather than
discovered in the code during an incident. The argument for denying instead: a floor with any
open path is off in the session where it mattered. The argument that won: every other tool in
this harness is Python, so a machine without `python3` has a broken harness whatever the hook
does, and refusing every tool call is a worse first five minutes than a visible warning. The
cost is that the warning has to actually be visible, which is why the string is upper-case and
unmissable rather than a polite note.

The `hooks-registered` check exists to make the other silent-failure paths loud: registered but
not installed, installed but not executable, registered against a script that does not exist.
Each of those looks identical from the outside — nothing happens — and each is a separate
named failure.

## The mode contract does not govern a tree this harness does not serve

**Decided**: 2026-08-21

Carried unchanged from the plan's settled call 5, and now enforced rather than asserted.

The mode branch reads `docs/PROGRESS.md` and returns inert unless the front matter carries
`active_work`, `next_action` and `resume_note` — this schema's signature. ColdStart v1's
pointer carries `active_section` instead, which is exactly the mismatch that blocked `/prep`
in this repo until `.coldstart-init` scoped it out.

The scoping cuts one way only. In a foreign tree the mode contract goes quiet and the secrets
and destructive rules stay live, because a credential leak in someone else's repo is still a
credential leak. There is a fixture for each half.

## Under prep, provable beats plausible

**Decided**: 2026-08-21

The read-only test under `mode: prep` is a whitelist, and every segment of a compound command
has to be on it. Two safe halves joined by an unknown third still stops.

An unrecognised command may well be a read. "May well be" is the standard the whitelist exists
to refuse, and the refusal says so in those words, because an operator who thinks the rule is
about safety will argue with it and an operator who sees it is about provability will not.

The escape hatch is `mode: build` in the pointer's front matter, which `/done` writes at close
and `/prep` sets on entry. The section plan's text named `python tools/done.py --set-mode
build`; no such tool exists in this tree (`tools/` holds `index.py` and now `verify.py`), so the
refusal names the field and the file instead. Recorded here rather than silently diverging.
