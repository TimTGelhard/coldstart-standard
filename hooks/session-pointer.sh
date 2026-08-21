#!/usr/bin/env sh
#
# session-pointer.sh -- the registered SessionStart entry point.
#
# Same shim shape as pre-tool-floor.sh, for the same reason: the rules are
# Python because the pointer is YAML, and the entry point is sh because that is
# what the host runs. If it cannot run, it says nothing and the session is
# exactly as it was before this hook existed.

set -eu

here=$( cd "$( dirname "$0" )" && pwd )

if [ -f "$here/pointer.py" ]; then
  rules="$here/pointer.py"
elif [ -n "${CLAUDE_PROJECT_DIR:-}" ] && [ -f "$CLAUDE_PROJECT_DIR/hooks/pointer.py" ]; then
  rules="$CLAUDE_PROJECT_DIR/hooks/pointer.py"
else
  exit 0
fi

command -v python3 >/dev/null 2>&1 || exit 0

exec python3 "$rules"
