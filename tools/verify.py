"""The three checks. `/done` runs this; a red result refuses the close.

SPEC.md cut ColdStart's 30 check-classes to three, and the cut is the point: a
check earns its place by watching something that has actually broken here, not
by covering a category.

  ghost-refs        a link in docs/ whose target does not exist
  byte-budgets      the resident surface against SPEC.md's declared ceiling
  hooks-registered  every hook script is registered, installed and executable

The third is the one ColdStart learned the hard way and this harness inherited
as a rule: green CI has already hidden an unfinished install once in this family,
so the check that a file EXISTS is worth nothing next to the check that the host
would actually run it.

Usage:
    python3 tools/verify.py            # all three, human output
    python3 tools/verify.py --check    # same, exit 1 on any failure
    python3 tools/verify.py ghost-refs # one check by name
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# SPEC.md, "Declared budget". A target to design against, reported either way,
# and NOT a gate: the SPEC says so in the same breath it names the number.
RESIDENT_BUDGET = 12_000

# What is actually resident in a session, as opposed to what is on disk. The
# whole memory model under docs/ is cold by design and is not counted, which is
# the claim this check exists to keep honest.
RESIDENT = (
    ("CLAUDE.md", "the always-loaded carrier"),
    ("PROFILE.md", "the distilled profile"),
    ("commands/*.md", "the command wrappers"),
    ("skills/*/SKILL.md", "router descriptions (front matter only)"),
    ("agents/*.md", "the agents"),
)

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


class Result:
    def __init__(self, name: str) -> None:
        self.name = name
        self.failures: list[str] = []
        self.notes: list[str] = []

    @property
    def ok(self) -> bool:
        return not self.failures

    def report(self) -> str:
        head = f"{'PASS' if self.ok else 'FAIL'}  {self.name}"
        lines = [head]
        lines += [f"        {n}" for n in self.notes]
        lines += [f"      ! {f}" for f in self.failures]
        return "\n".join(lines)


def check_ghost_refs(root: Path) -> Result:
    """Every repo-relative link in docs/ resolves to a file that exists.

    A reference that escapes the root or is absolute is machine-local, and
    docs/FORMAT.md rule 7 says it is reported as unresolvable rather than failed:
    a sibling tree's absence is not this repo's defect. This repo has six such
    references into ColdStart v1, and turning them into failures would mean
    either deleting a true citation or carrying a permanently red check.
    """
    result = Result("ghost-refs")
    # Resolved, because on macOS /var is a symlink to /private/var and a resolved
    # link compared against an unresolved root reads as "outside the repo" -- which
    # this check tolerates, so the bug would have shown up as a silent green.
    root = root.resolve()
    outside = 0
    checked = 0
    for path in sorted(root.glob("docs/**/*.md")) + [root / "SPEC.md"]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for target in MD_LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            checked += 1
            if target.startswith("/") or target.startswith(".."):
                outside += 1
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                outside += 1
                continue
            if not resolved.exists():
                rel = path.relative_to(root)
                result.failures.append(f"{rel} -> {target} does not exist")
    result.notes.append(f"{checked} links checked, {outside} point outside the repo "
                        f"(reported, not failed)")
    return result


def check_byte_budgets(root: Path) -> Result:
    """The resident surface, measured, against the declared ceiling.

    Measures the rendered surface rather than the file list: for a skill, only
    the front matter is resident, because the body loads on demand. Counting the
    body would report a number four times the truth and make every later trim
    look like it did nothing.
    """
    result = Result("byte-budgets")
    total = 0
    for pattern, label in RESIDENT:
        size = 0
        found = 0
        for path in sorted(root.glob(pattern)):
            if not path.is_file():
                continue
            found += 1
            text = path.read_text(encoding="utf-8")
            if path.name == "SKILL.md":
                end = text.find("\n---", 3) if text.startswith("---") else -1
                text = text[:end] if end != -1 else text
            size += len(text.encode("utf-8"))
        total += size
        state = f"{size:>6,} B" if found else "     -- not built yet"
        result.notes.append(f"{state}  {pattern:<20} {label}")

    pointer = root / "docs" / "PROGRESS.md"
    if pointer.is_file():
        text = pointer.read_text(encoding="utf-8")
        end = text.find("\n---", 3)
        block = len(text[:end + 4].encode("utf-8")) if end != -1 else 0
        total += block
        result.notes.append(f"{block:>6,} B  {'pointer':<20} injected at SessionStart")

    pct = round(100 * total / RESIDENT_BUDGET)
    result.notes.append(f"{total:>6,} B  TOTAL, {pct}% of the {RESIDENT_BUDGET:,} B "
                        f"declared in SPEC.md")
    if total > RESIDENT_BUDGET:
        result.failures.append(
            f"over the declared budget by {total - RESIDENT_BUDGET:,} B. SPEC.md calls "
            f"this a number to publish rather than a gate, so this is a red that says "
            f"'amend the ledger or trim', not 'the build is broken'.")
    return result


def check_hooks_registered(root: Path) -> Result:
    """Every hook is registered, installed, executable, and points at the copy that runs.

    The four properties are separate failures on purpose. A hook can exist and
    not be registered, be registered and not installed, be installed and not
    executable, or be registered against a path that does not exist -- and every
    one of those looks identical from the outside: nothing happens, silently.
    """
    result = Result("hooks-registered")
    fragment_path = root / "hooks" / "settings.json"
    if not fragment_path.is_file():
        result.failures.append("hooks/settings.json is missing, so nothing is registered")
        return result

    fragment = json.loads(fragment_path.read_text(encoding="utf-8"))
    registered: dict[str, str] = {}
    for event, entries in fragment.get("hooks", {}).items():
        for entry in entries:
            for hook in entry.get("hooks", []):
                registered[Path(hook.get("command", "")).name] = event

    scripts = sorted(p for p in (root / "hooks").glob("*.sh"))
    for script in scripts:
        if script.name not in registered:
            result.failures.append(
                f"hooks/{script.name} exists but no event in hooks/settings.json runs it")
        if not os.access(script, os.X_OK):
            result.failures.append(f"hooks/{script.name} is not executable")
    for name, event in registered.items():
        if not (root / "hooks" / name).is_file():
            result.failures.append(
                f"{event} is registered against hooks/{name}, which does not exist")

    installed = root / ".claude" / "settings.json"
    if not installed.is_file():
        result.notes.append("not installed here yet: run `sh install.sh`, and note that "
                            "an uninstalled floor does not fire")
    else:
        live = json.loads(installed.read_text(encoding="utf-8")).get("hooks", {})
        live_names = {Path(h.get("command", "")).name
                      for entries in live.values() for e in entries for h in e.get("hooks", [])}
        for name in registered:
            if name not in live_names:
                result.failures.append(
                    f"hooks/{name} is registered in source but missing from the installed "
                    f".claude/settings.json -- re-run install.sh")
            target = root / ".claude" / "hooks" / name
            if not target.is_file():
                result.failures.append(f".claude/settings.json points at {name}, "
                                       f"which is not in .claude/hooks/")
            elif not os.access(target, os.X_OK):
                result.failures.append(f".claude/hooks/{name} is not executable, so the "
                                       f"host cannot run it")
        result.notes.append(f"{len(registered)} hook(s) registered and installed: "
                            f"{', '.join(sorted(registered))}")
    return result


CHECKS = {
    "ghost-refs": check_ghost_refs,
    "byte-budgets": check_byte_budgets,
    "hooks-registered": check_hooks_registered,
}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    strict = "--check" in argv
    argv = [a for a in argv if not a.startswith("-")]
    names = argv or list(CHECKS)
    unknown = [n for n in names if n not in CHECKS]
    if unknown:
        print(f"verify: unknown check(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"        known: {', '.join(CHECKS)}", file=sys.stderr)
        return 2

    results = [CHECKS[name](ROOT) for name in names]
    for result in results:
        print(result.report())
    failed = [r for r in results if not r.ok]
    print()
    print(f"{len(results) - len(failed)}/{len(results)} checks pass")
    return 1 if (failed and strict) else 0


if __name__ == "__main__":
    sys.exit(main())
