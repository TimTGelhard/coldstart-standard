"""SessionStart: put the resume pointer in front of the model, unasked.

`SPEC.md` says the one thing this harness is for is that you should not have to
re-prompt the project into the session. `/coldstart` delivers that when it is
typed. This hook delivers it when it is not, which is the case that actually
costs the operator time: the session that starts with a question, gets answered
from a blank context, and quietly contradicts a decision made last Tuesday.

It is deliberately the pointer and nothing else. The seven fields plus the first
queued session is the smallest thing that makes a cold model correct rather than
confident, and every byte beyond it is resident cost on every session for the
life of the project. The budget is enforced below rather than intended: the
output is truncated at BUDGET and says so, because a payload that quietly grows
is how a lean harness stops being one.

Nothing here duplicates /coldstart. This says where you are; /coldstart is what
reads the work file and continues.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

BUDGET = 900   # bytes of additionalContext. Reported in MEASURE.md, section 7.

FIELDS = ("active_work", "mode", "next_action", "blockers", "reading", "resume_note")
SCHEMA_FIELDS = ("active_work", "next_action", "resume_note")


def find_root(start: str) -> Path | None:
    here = Path(start or ".").resolve()
    for candidate in (here, *here.parents):
        if (candidate / "docs" / "PROGRESS.md").is_file():
            return candidate
    return None


def pointer_block(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fields = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip("\"'")
    if not all(f in fields for f in SCHEMA_FIELDS):
        return None   # not this harness's pointer; say nothing at all
    return fields


def first_queued(text: str) -> str | None:
    """The top row of the generated queue table, which is the next session."""
    rows = re.findall(r"^\|\s*([\d.]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*pending\s*\|",
                      text, re.MULTILINE)
    if not rows:
        return None
    number, session, what = rows[0]
    return f"{number} {session} — {what}"


def compose(root: Path) -> str | None:
    text = (root / "docs" / "PROGRESS.md").read_text(encoding="utf-8")
    fields = pointer_block(text)
    if fields is None:
        return None
    lines = [f"Resume pointer for {root.name} (docs/PROGRESS.md, written by /done):"]
    for key in FIELDS:
        value = fields.get(key, "")
        if value and value not in ("[]", "''", '""'):
            lines.append(f"  {key}: {value}")
    queued = first_queued(text)
    if queued:
        lines.append(f"  next queued: {queued}")
    lines.append("Read the file named by active_work before changing anything in it. "
                 "`reading` is a ceiling, not a suggestion.")
    out = "\n".join(lines)
    if len(out.encode("utf-8")) > BUDGET:
        out = out.encode("utf-8")[:BUDGET].decode("utf-8", "ignore")
        out += f"\n  [truncated at {BUDGET} B: the pointer is over its resident budget]"
    return out


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    root = find_root(str(os.environ.get("CLAUDE_PROJECT_DIR")
                         or payload.get("cwd") or os.getcwd()))
    if root is None:
        return 0
    context = compose(root)
    if not context:
        return 0
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
