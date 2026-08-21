#!/usr/bin/env sh
#
# install.sh — the minimal map (section 6 session 1).
#
# Copies this harness's commands and skills into `.claude/`, which is the only
# place the host looks for them. Without this, `commands/` and `skills/` sit at
# the repo root registered nowhere, and typing `/coldstart` in this tree loads
# whatever other install happens to own the name.
#
# It writes `.claude/commands/`, `.claude/skills/`, `.claude/hooks/` and the hook
# registration inside `.claude/settings.json`. Nothing else: no `.coldstart/`, no
# uninstall, no `--weight` selector. Those are sessions 2 to 4.
#
# The hooks arrived at section 4. They are installed the same way as their
# siblings and for the same reason -- a floor that is only in the source tree is
# registered nowhere, so it never fires, and a floor that never fires is the most
# expensive kind of missing: the session looks protected and is not.
#
# Copy, not symlink (decisions/install.md): the installed copy has to be a
# different file from the one being edited, or a passing run stops proving that
# the installed copy works.
#
# Idempotent by replacement: the two target directories are removed and rewritten
# on every run, so a command deleted from the source tree does not linger in the
# install, and running twice leaves an identical tree.
#
# It also claims its own command names. A same-named command already registered
# at the user level (~/.claude/commands/) wins over the project copy, so writing
# `.claude/` is necessary but not sufficient: measured in this repo, typing
# `/coldstart` still loaded ColdStart v1's user-level SKILL, not even its command
# stub, so both surfaces have to be claimed. Displaced entries are MOVED, never
# deleted, into sibling backup directories, and the reverse is the `mv` printed
# at the end. `--keep-user-commands` skips the step and warns instead.

set -eu

claim_names=1
for arg in "$@"; do
  case "$arg" in
    --keep-user-commands) claim_names=0 ;;
    *) echo "install.sh: unknown argument: $arg" >&2; exit 1 ;;
  esac
done

root=$( cd "$( dirname "$0" )" && pwd )
target="$root/.claude"
cfg="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
user_dir="$cfg/commands"
displaced="$cfg/commands-displaced-by-coldstart-standard"
user_skills="$cfg/skills"
displaced_skills="$cfg/skills-displaced-by-coldstart-standard"

# Refuse to run against a tree that is not this harness, because the first thing
# this script does is delete two directories.
if [ ! -f "$root/SPEC.md" ] || [ ! -d "$root/commands" ] || [ ! -d "$root/skills" ] \
   || [ ! -d "$root/hooks" ]; then
  echo "install.sh: $root does not look like the coldstart-standard source tree" >&2
  echo "  (expected SPEC.md, commands/, skills/ and hooks/ beside this script)" >&2
  exit 1
fi

rm -rf "$target/commands" "$target/skills" "$target/hooks"
mkdir -p "$target/commands" "$target/skills" "$target/hooks"

commands=0
for f in "$root"/commands/*.md; do
  [ -f "$f" ] || continue
  cp "$f" "$target/commands/"
  commands=$(( commands + 1 ))
done

skills=0
for d in "$root"/skills/*/; do
  [ -d "$d" ] || continue
  name=$( basename "$d" )
  mkdir -p "$target/skills/$name"
  cp "$d"*.md "$target/skills/$name/"
  skills=$(( skills + 1 ))
done

hooks=0
for f in "$root"/hooks/*.sh "$root"/hooks/*.py; do
  [ -f "$f" ] || continue
  cp "$f" "$target/hooks/"
  case "$f" in *.sh) chmod +x "$target/hooks/$( basename "$f" )" ;; esac
  hooks=$(( hooks + 1 ))
done

# Merge the registration rather than overwrite it. A project settings.json may
# already carry permissions, env or another team's hooks, and an installer that
# replaces the file wholesale eats someone's work the first time it runs in a
# real repo. Only this harness's own entries are replaced, matched by the script
# path they point at, so a second run is a no-op rather than a duplicate.
if [ -f "$root/hooks/settings.json" ]; then
  python3 - "$root/hooks/settings.json" "$target/settings.json" <<'MERGE'
import json, sys
from pathlib import Path

fragment_path, target_path = Path(sys.argv[1]), Path(sys.argv[2])
fragment = json.loads(fragment_path.read_text(encoding="utf-8"))
try:
    settings = json.loads(target_path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    settings = {}

live = settings.setdefault("hooks", {})
for event, entries in fragment.get("hooks", {}).items():
    ours = {h.get("command") for e in entries for h in e.get("hooks", [])}
    kept = [e for e in live.get(event, [])
            if not any(h.get("command") in ours for h in e.get("hooks", []))]
    live[event] = kept + entries

target_path.parent.mkdir(parents=True, exist_ok=True)
target_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
MERGE
  echo "registered the floor and the session pointer in .claude/settings.json"
fi

moved=0
kept=0
for f in "$root"/commands/*.md; do
  [ -f "$f" ] || continue
  name=$( basename "$f" )
  live="$user_dir/$name"
  [ -f "$live" ] || continue

  if [ "$claim_names" -eq 0 ]; then
    echo "install.sh: WARNING $live shadows this harness's /$( basename "$name" .md )" >&2
    kept=$(( kept + 1 ))
    continue
  fi

  mkdir -p "$displaced"
  if [ -f "$displaced/$name" ]; then
    # Already displaced once and the user-level file came back. Only safe to
    # drop the live copy if it is byte-identical to what is already saved;
    # otherwise stop and let a human decide which one is wanted.
    if cmp -s "$live" "$displaced/$name"; then
      rm "$live"
    else
      echo "install.sh: $live differs from the copy already in $displaced" >&2
      echo "  refusing to overwrite a backup; move or delete one of them by hand" >&2
      exit 1
    fi
  else
    mv "$live" "$displaced/$name"
  fi
  moved=$(( moved + 1 ))
done

# Same claim over the skills surface. A user-level skill directory of the same
# name wins too, and in this repo it was the skill -- not the command stub --
# that actually loaded. Entries here are often symlinks; mv moves the link.
for d in "$root"/skills/*/; do
  [ -d "$d" ] || continue
  name=$( basename "$d" )
  live="$user_skills/$name"
  [ -e "$live" ] || continue

  if [ "$claim_names" -eq 0 ]; then
    echo "install.sh: WARNING $live shadows this harness's $name skill" >&2
    kept=$(( kept + 1 ))
    continue
  fi

  mkdir -p "$displaced_skills"
  if [ -e "$displaced_skills/$name" ]; then
    echo "install.sh: $displaced_skills/$name already exists" >&2
    echo "  refusing to overwrite a backup; move or delete it by hand" >&2
    exit 1
  fi
  mv "$live" "$displaced_skills/$name"
  moved=$(( moved + 1 ))
done

echo "installed $commands command(s), $skills skill(s) and $hooks hook file(s) into .claude/"
if [ "$moved" -gt 0 ]; then
  echo "displaced $moved user-level entr(ies) that shadowed them, into:"
  echo "  $displaced"
  echo "  $displaced_skills"
  echo "reverse with: mv $displaced/*.md $user_dir/"
  echo "         and: mv $displaced_skills/* $user_skills/"
fi
if [ "$kept" -gt 0 ]; then
  echo "$kept user-level entr(ies) left in place and still shadowing this harness"
  echo "  (--keep-user-commands was passed); the loop is not typeable until they move"
fi
echo "start a NEW session in this tree for the host to register them"
