# coldstart-standard

A lean session harness for Claude Code. It exists to answer one question at the start of every
session — *where were we?* — without you typing the answer again.

**Status: in progress.** Three of seven sections are built. What is here works and is tested;
what is not here is named below rather than implied. See [SPEC.md](SPEC.md) for the full design
and [docs/PROGRESS.md](docs/PROGRESS.md) for what is next.

## The problem

A model starts every session with no memory of the last one. So you re-explain the project: what
you were doing, what you already decided, what already broke. That re-explanation is the cost,
and it is paid daily.

The usual fix is a big project document, which fails a different way: it grows, it goes stale
against the code, and it is too large to load, so it gets loaded anyway and eats the context it
was meant to save.

## The shape

One mechanic applied three times. An **index file** that holds status and a pointer and
structurally cannot hold detail, and a **folder** beside it holding the content, clustered by
topic.

```
docs/
  PROGRESS.md    pointer + one line per session   ->  work/
  DECISIONS.md   one line per topic               ->  decisions/
  FIXES.md       one line per open item           ->  fixes/
```

Three rules make it work without maintenance:

**The indexes are derived, never written.** `tools/index.py` scans each folder and rewrites the
index above it. An index cannot go stale or disagree with its folder, because it is a function
of it.

**Only the pointer is ever resident.** The seven-field block at the top of `PROGRESS.md` is the
one thing loaded into a session by default — currently 405 bytes. Everything else under `docs/`
is cold and read on demand.

**The queue is open-only.** A shipped fix is deleted, not archived. There is no done section and
no history field. Git is the archive, which is what git is.

## What is built

**Three commands.** `/prep` plans a section into `docs/work/`. `/coldstart` resumes from the
pointer. `/done` closes: files the decisions, regenerates the indexes, runs verify, rewrites the
pointer.

**A safety floor** (`hooks/pre-tool-floor.sh`), a PreToolUse hook that denies rather than asks.
Three categories: reading or staging credential material, destructive commands with no undo, and
anything not provably a read while the pointer says `mode: prep`. Every refusal names what fired,
why the rule is structural, and what the legitimate path is — a refusal without a way forward
gets routed around inside the same session.

It is calibrated on what it lets through, not on what it stops: 46 fixtures, 25 of them
allow-cases, and the suite fails if denies ever outnumber allows. `rm -rf node_modules` passes.
`git push --force-with-lease` passes. `rm -rf $BUILD_DIR` does not, because an unset variable
makes that `rm -rf /`.

**A session pointer hook** (`hooks/session-pointer.sh`), SessionStart, which puts the resume
pointer in front of the model whether or not you type anything.

**Three verify checks** (`tools/verify.py`): `ghost-refs` for link rot, `byte-budgets` for the
resident surface against the declared ceiling, and `hooks-registered`, which checks four separate
properties — registered, installed, executable, pointing at a script that exists — because each
fails silently and identically.

Every check ships with a test that plants one defect and asserts the check finds it. That bar
paid for itself on the first run: `ghost-refs` was passing while watching nothing.

## What is not built

Sections 3 and 7 of the plan. There is no `CLAUDE.md` carrier, no routing skills, no agents and
no chapter set, so the always-loaded prose layer does not exist yet. There is no `MEASURE.md`
census and no containment test. `install.sh` has no uninstall and no `--weight` selector.

Several documents cite a sibling ColdStart v1 tree by absolute path. Those citations are true and
machine-local, and `ghost-refs` counts them rather than failing them.

## Install

Requires `python3` and `sh`.

```sh
git clone https://github.com/TimTGelhard/coldstart-standard.git
cd coldstart-standard
sh install.sh
```

This copies `commands/`, `skills/` and `hooks/` into `.claude/` and merges the hook registration
into `.claude/settings.json`, keeping any keys already there. It is idempotent. Start a new
session afterwards for the host to register everything.

One thing it does that you should know about first: it claims its own command names. A
same-named command or skill already installed at the user level (`~/.claude/`) wins over the
project copy, so the installer **moves** those aside into `~/.claude/commands-displaced-by-coldstart-standard/`
and prints the `mv` that reverses it. Pass `--keep-user-commands` to skip that and get a warning
instead — the commands then stay shadowed and are not typeable.

```sh
python3 -m unittest discover -s tests   # 74 tests
python3 tools/verify.py                 # the three checks
```

## Licence

MIT. See [LICENSE](LICENSE).
