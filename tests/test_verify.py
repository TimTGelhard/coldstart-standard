"""Tests for tools/verify.py: each check is shown going red for its own reason.

SPEC.md's bar for this section is a self-test per check that plants one defect
and asserts the check finds it. The reason the bar is that and not "the check
runs" is the failure this family has already had: a check can pass because the
thing it watches is fine, or because it is watching nothing at all, and from the
outside those are the same green.

Every test copies the real repo into a temp dir and breaks one thing there, so
the checks are exercised against a tree with real content rather than a fixture
that happens to satisfy them.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import verify  # noqa: E402


class VerifyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="verify-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        for item in ("docs", "hooks", "commands", "skills", "SPEC.md", ".claude"):
            source = ROOT / item
            if not source.exists():
                continue
            target = self.tmp / item
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)

    # -- the tree is green before anything is broken ----------------------

    def test_all_three_pass_on_a_clean_copy(self) -> None:
        for name, check in verify.CHECKS.items():
            with self.subTest(check=name):
                result = check(self.tmp)
                self.assertTrue(result.ok, f"{name} is red on a clean tree:\n{result.report()}")

    # -- ghost-refs -------------------------------------------------------

    def test_ghost_refs_finds_a_dead_link(self) -> None:
        (self.tmp / "docs" / "PROGRESS.md").write_text(
            "# Progress\n\nSee [the plan](work/99-does-not-exist.md).\n", encoding="utf-8")
        result = verify.check_ghost_refs(self.tmp)
        self.assertFalse(result.ok)
        self.assertIn("99-does-not-exist.md", " ".join(result.failures))

    def test_ghost_refs_tolerates_a_link_out_of_the_repo(self) -> None:
        """FORMAT.md rule 7: a sibling tree's absence is not this repo's defect."""
        (self.tmp / "docs" / "PROGRESS.md").write_text(
            "# Progress\n\nSee [the charter](../../CHARTER.md) and [v1](/nowhere/x.md).\n",
            encoding="utf-8")
        result = verify.check_ghost_refs(self.tmp)
        self.assertTrue(result.ok, result.report())
        self.assertIn("point outside the repo", " ".join(result.notes))

    # -- byte-budgets -----------------------------------------------------

    def test_byte_budgets_goes_red_over_the_ceiling(self) -> None:
        (self.tmp / "CLAUDE.md").write_text("x" * (verify.RESIDENT_BUDGET + 1), encoding="utf-8")
        result = verify.check_byte_budgets(self.tmp)
        self.assertFalse(result.ok)
        self.assertIn("over the declared budget", " ".join(result.failures))

    def test_byte_budgets_counts_skill_front_matter_only(self) -> None:
        """A skill body loads on demand, so counting it would report a number
        four times the truth and make every later trim look ineffective."""
        before = verify.check_byte_budgets(self.tmp)
        skill = self.tmp / "skills" / "prep" / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\n" + "y" * 5000,
                         encoding="utf-8")
        after = verify.check_byte_budgets(self.tmp)
        self.assertEqual(
            [n for n in before.notes if "SKILL.md" in n],
            [n for n in after.notes if "SKILL.md" in n],
            "5 KB added to a skill body changed the resident measurement, so the "
            "check is measuring the file rather than the rendered surface")

    # -- hooks-registered -------------------------------------------------

    def test_hooks_registered_finds_an_unregistered_hook(self) -> None:
        script = self.tmp / "hooks" / "orphan.sh"
        script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
        result = verify.check_hooks_registered(self.tmp)
        self.assertFalse(result.ok)
        self.assertIn("orphan.sh", " ".join(result.failures))

    def test_hooks_registered_finds_a_non_executable_hook(self) -> None:
        script = self.tmp / "hooks" / "pre-tool-floor.sh"
        script.chmod(script.stat().st_mode & ~stat.S_IXUSR & ~stat.S_IXGRP & ~stat.S_IXOTH)
        result = verify.check_hooks_registered(self.tmp)
        self.assertFalse(result.ok)
        self.assertIn("not executable", " ".join(result.failures))

    def test_hooks_registered_finds_a_registration_with_no_script(self) -> None:
        fragment = self.tmp / "hooks" / "settings.json"
        data = json.loads(fragment.read_text(encoding="utf-8"))
        data["hooks"]["Stop"] = [{"hooks": [{"type": "command",
                                             "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/ghost.sh"}]}]
        fragment.write_text(json.dumps(data, indent=2), encoding="utf-8")
        result = verify.check_hooks_registered(self.tmp)
        self.assertFalse(result.ok)
        self.assertIn("ghost.sh", " ".join(result.failures))

    def test_hooks_registered_finds_a_stale_install(self) -> None:
        """The failure this check exists for: source says registered, the
        installed copy the host actually reads does not."""
        installed = self.tmp / ".claude" / "settings.json"
        if not installed.is_file():
            self.skipTest("no .claude/ in this tree; run install.sh first")
        installed.write_text(json.dumps({"hooks": {}}), encoding="utf-8")
        result = verify.check_hooks_registered(self.tmp)
        self.assertFalse(result.ok)
        self.assertIn("re-run install.sh", " ".join(result.failures))


if __name__ == "__main__":
    unittest.main()
