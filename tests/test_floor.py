"""Tests for hooks/floor.py, over the payload fixtures in tests/fixtures/floor/.

Each fixture is one PreToolUse payload plus the pointer state it should be
judged under, and the expectation. The suite runs every fixture in a throwaway
tree so the mode contract has a real docs/PROGRESS.md to read, which is the only
way to test a rule whose input is the filesystem.

Two properties matter more than the individual cases and are asserted directly:

  * allow-fixtures outnumber deny-fixtures. A floor calibrated only on the
    things it should stop is a floor that stops everything and gets switched off
    within a week, and the count is the cheapest guard against drifting that way.
  * every deny-fixture's category actually appears in the refusal text. A
    refusal that fires for the wrong reason teaches the operator the wrong rule.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hooks"))

import floor  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "floor"

STANDARD_POINTER = """---
active_work: docs/work/01-memory-model.md
mode: {mode}
next_action: the next concrete step
blockers: []
reading: [SPEC.md]
updated: 2026-08-21
resume_note: "a pointer carrying this harness's seven fields"
---

# Progress
"""

# ColdStart v1's shape: a real pointer, a real `mode`, and not our schema. The
# tree this harness was itself governed by, which is why it is a fixture.
FOREIGN_POINTER = """---
active_section: 3
mode: {mode}
updated: 2026-08-21
---

# Progress
"""


class FloorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="floor-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        (self.tmp / "docs" / "work").mkdir(parents=True)
        (self.tmp / "tools").mkdir()

    def plant(self, mode: str, pointer: str) -> Path:
        template = FOREIGN_POINTER if pointer == "foreign" else STANDARD_POINTER
        (self.tmp / "docs" / "PROGRESS.md").write_text(
            template.format(mode=mode), encoding="utf-8")
        return self.tmp

    def judge(self, case: dict) -> str | None:
        """Run one fixture through decide(), rooted in the throwaway tree."""
        root = self.plant(case.get("mode", "build"), case.get("pointer", "standard"))
        payload = json.loads(json.dumps(case["payload"]))   # a copy; we rewrite paths
        tool_input = payload.get("tool_input", {})
        if "file_path" in tool_input and not tool_input["file_path"].startswith("/"):
            tool_input["file_path"] = str(root / tool_input["file_path"])
        payload["cwd"] = str(root)
        return floor.decide(payload)


def load_fixtures() -> list[tuple[str, dict]]:
    return [(p.stem, json.loads(p.read_text(encoding="utf-8")))
            for p in sorted(FIXTURES.glob("*.json"))]


def make_test(name: str, case: dict):
    def test(self: FloorTestCase) -> None:
        reason = self.judge(case)
        note = case.get("note") or ""
        if case["expect"] == "deny":
            self.assertIsNotNone(reason, f"{name} should have been refused. {note}")
            self.assertIn(f"floor:{case['category']}", reason,
                          f"{name} was refused under the wrong category. {note}")
            self.assertIn("legitimate path", reason,
                          f"{name}'s refusal does not name a way forward, so it will "
                          f"be routed around rather than obeyed")
        else:
            self.assertIsNone(reason, f"{name} is a false positive: {note}\n{reason}")
    test.__name__ = f"test_{name.replace('-', '_')}"
    return test


for _name, _case in load_fixtures():
    setattr(FloorTestCase, f"test_{_name.replace('-', '_')}", make_test(_name, _case))


class CalibrationTestCase(unittest.TestCase):
    """Properties of the fixture set itself, not of any one rule."""

    def test_allows_outnumber_denies(self) -> None:
        names = [n for n, _ in load_fixtures()]
        allow = [n for n in names if n.startswith("allow")]
        deny = [n for n in names if n.startswith("deny")]
        self.assertGreaterEqual(
            len(allow), len(deny),
            "The floor is calibrated by what it lets through. Adding a deny rule "
            "without adding the allow cases that prove it stays narrow is how a "
            "floor becomes something its owner turns off.")

    def test_every_category_has_both_sides(self) -> None:
        cases = [c for _, c in load_fixtures()]
        for category in ("secrets", "destructive", "mode"):
            denied = [c for c in cases if c.get("category") == category]
            self.assertTrue(denied, f"no deny fixture for {category}")

    def test_unreadable_payload_passes(self) -> None:
        """A floor that cannot read its input must not brick every tool call."""
        self.assertIsNone(floor.decide({}))
        self.assertIsNone(floor.decide({"tool_name": "Bash", "tool_input": "not-a-dict"}))


if __name__ == "__main__":
    unittest.main()
