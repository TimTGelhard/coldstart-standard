#!/usr/bin/env sh
#
# pre-tool-floor.sh -- the registered PreToolUse entry point.
#
# The rules live in floor.py beside this file; this is the shim that finds it
# and feeds it the payload. Kept in sh with no bash-only syntax because the host
# runs hooks under /bin/sh and a floor that silently fails to start is worse than
# no floor: the session looks protected and is not.
#
# Resolution order for the rules file: next to this script (the installed copy in
# .claude/hooks/), then $CLAUDE_PROJECT_DIR/hooks/ (running from a source tree
# that has not been installed).
#
# If python3 is absent the floor cannot run. It passes, loudly, on stderr rather
# than denying: a harness whose every other tool is Python is already broken
# without it, and bricking every tool call is a worse first five minutes than a
# visible warning. The tradeoff is written down in docs/decisions/safety-floor.md
# so that nobody discovers it by reading the code during an incident.

set -eu

here=$( cd "$( dirname "$0" )" && pwd )

if [ -f "$here/floor.py" ]; then
  rules="$here/floor.py"
elif [ -n "${CLAUDE_PROJECT_DIR:-}" ] && [ -f "$CLAUDE_PROJECT_DIR/hooks/floor.py" ]; then
  rules="$CLAUDE_PROJECT_DIR/hooks/floor.py"
else
  echo "pre-tool-floor: floor.py not found beside $here -- THE FLOOR IS NOT RUNNING" >&2
  exit 0
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "pre-tool-floor: python3 not on PATH -- THE FLOOR IS NOT RUNNING" >&2
  exit 0
fi

exec python3 "$rules"
