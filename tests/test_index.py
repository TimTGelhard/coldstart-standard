"""Tests for tools/index.py, over the fixture tree in tests/fixtures/.

Each test copies the fixture tree to a temp dir, so a test may add, rename, delete
or corrupt files freely. The cases the section plan names are covered: a new file,
a renamed file, a deleted file, a malformed file — plus idempotence and the
pointer-is-untouched property, which are the two things that make the index
trustworthy rather than merely present.

Run: python -m unittest discover -s tests
"""

from __future__ import annotations

import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import index  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class IndexTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="index-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        shutil.copytree(FIXTURES, self.tmp, dirs_exist_ok=True)
        self.docs = self.tmp / "docs"

    # -- helpers ----------------------------------------------------------

    def run_index(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = index.main(["--root", str(self.tmp), *args])
        return code, out.getvalue(), err.getvalue()

    def generate(self, *args: str) -> None:
        code, _, err = self.run_index(*args)
        self.assertEqual(code, 0, err)

    def read(self, name: str) -> str:
        return (self.docs / name).read_text(encoding="utf-8")

    def write(self, relative: str, text: str) -> Path:
        path = self.docs / relative
        path.write_text(text, encoding="utf-8")
        return path

    def front_matter(self) -> str:
        return self.read("PROGRESS.md").split("---", 2)[1]

    # -- the generated content --------------------------------------------

    def test_queue_lists_only_open_sessions(self) -> None:
        self.generate()
        progress = self.read("PROGRESS.md")
        self.assertIn("| 1.2 | alpha s2 |", progress)
        self.assertNotIn("alpha s1", progress)
        self.assertNotIn("beta s1", progress)

    def test_a_fully_done_section_logs_instead_of_queueing(self) -> None:
        self.generate()
        progress = self.read("PROGRESS.md")
        self.assertIn("| 02 | beta | the second fixture section, entirely closed | closed 2026-01-02 |", progress)

    def test_a_wrapped_goal_becomes_one_index_line(self) -> None:
        self.generate()
        self.assertIn(
            "the goal of the second session, which wraps across two source lines", self.read("PROGRESS.md")
        )

    def test_the_stale_body_below_the_marker_is_replaced(self) -> None:
        self.generate()
        for name in ("PROGRESS.md", "DECISIONS.md", "FIXES.md"):
            self.assertNotIn("stale body", self.read(name))

    def test_decisions_count_headings_and_ignore_fenced_ones(self) -> None:
        self.generate()
        self.assertIn("· 2 entries · 2026-01-03", self.read("DECISIONS.md"))

    def test_fixes_carry_since_and_the_optional_tag(self) -> None:
        self.generate()
        fixes = self.read("FIXES.md")
        self.assertIn("- **An open thing** — it is open · [fixes/known.md](fixes/known.md) · since 2026-01-04", fixes)
        self.assertTrue(fixes.rstrip().endswith("· since 2026-01-05 · later"))

    # -- the properties ----------------------------------------------------

    def test_a_second_run_is_byte_identical(self) -> None:
        self.generate()
        first = {name: self.read(name) for name in ("PROGRESS.md", "DECISIONS.md", "FIXES.md")}
        code, out, err = self.run_index()
        self.assertEqual(code, 0, err)
        self.assertIn("already current", out)
        for name, text in first.items():
            self.assertEqual(text, self.read(name))

    def test_the_pointer_block_is_never_touched(self) -> None:
        before = self.front_matter()
        self.generate()
        self.assertEqual(before, self.front_matter())
        self.write("work/03-gamma.md", GAMMA)
        self.generate()
        self.assertEqual(before, self.front_matter())

    def test_check_reports_drift_and_writes_nothing(self) -> None:
        code, _, err = self.run_index("--check")
        self.assertEqual(code, 1)
        self.assertIn("PROGRESS.md is out of date", err)
        self.assertIn("stale body", self.read("PROGRESS.md"))
        self.generate()
        code, _, _ = self.run_index("--check")
        self.assertEqual(code, 0)

    # -- the four mutations the plan names ---------------------------------

    def test_a_new_file_appears(self) -> None:
        self.generate()
        self.assertNotIn("gamma", self.read("PROGRESS.md"))
        self.write("work/03-gamma.md", GAMMA)
        self.generate()
        self.assertIn("| 3.1 | gamma s1 | the goal of gamma |", self.read("PROGRESS.md"))

    def test_a_deleted_file_disappears(self) -> None:
        self.generate()
        self.assertIn("shapes", self.read("DECISIONS.md"))
        (self.docs / "decisions" / "shapes.md").unlink()
        self.generate()
        decisions = self.read("DECISIONS.md")
        self.assertNotIn("shapes", decisions)
        self.assertIn("None yet.", decisions)

    def test_a_renamed_file_moves_and_its_topic_must_follow(self) -> None:
        self.generate()
        source = self.docs / "decisions" / "shapes.md"
        renamed = self.docs / "decisions" / "forms.md"
        source.rename(renamed)

        code, _, err = self.run_index()
        self.assertEqual(code, 2)
        self.assertIn("does not match the filename stem", err)
        self.assertIn("forms.md", err)

        renamed.write_text(
            renamed.read_text(encoding="utf-8").replace("topic: shapes", "topic: forms"), encoding="utf-8"
        )
        self.generate()
        decisions = self.read("DECISIONS.md")
        self.assertIn("[decisions/forms.md](decisions/forms.md)", decisions)
        self.assertNotIn("shapes.md", decisions)

    def test_a_malformed_file_is_a_loud_failure_not_a_skip(self) -> None:
        self.generate()
        good = self.read("DECISIONS.md")
        broken = self.write("decisions/broken.md", "no front matter at all\n")

        code, _, err = self.run_index()
        self.assertEqual(code, 2)
        self.assertIn("broken.md", err)
        self.assertIn("no front matter", err)
        self.assertEqual(good, self.read("DECISIONS.md"))

        broken.unlink()
        self.generate()

    # -- the rest of the failure surface -----------------------------------

    def test_each_malformed_shape_names_its_file(self) -> None:
        cases = [
            ("decisions/half.md", "---\ntitle: Half\ntopic: half\nupdated: 2026-01-01\n---\n", "missing subject"),
            ("decisions/bad-date.md", "---\ntitle: B\nsubject: s\ntopic: bad-date\nupdated: yesterday\n---\n", "not YYYY-MM-DD"),
            ("work/04-delta.md", DELTA_BAD_STATUS, "is not one of"),
            ("work/05-epsilon.md", EPSILON_NO_GOAL, "missing **Goal**"),
            ("fixes/loose.md", LOOSE_FIX_NO_SINCE, "missing **Since**"),
            ("fixes/statused.md", STATUSED_FIX, "open-only"),
        ]
        for relative, text, expected in cases:
            with self.subTest(relative):
                path = self.write(relative, text)
                code, _, err = self.run_index()
                path.unlink()
                self.assertEqual(code, 2, f"{relative} should have failed")
                self.assertIn(Path(relative).name, err)
                self.assertIn(expected, err)

    def test_an_overlong_subject_is_truncated_with_a_warning(self) -> None:
        long_subject = "x" * 200
        self.write(
            "decisions/long.md",
            f"---\ntitle: Long\nsubject: {long_subject}\ntopic: long\nupdated: 2026-01-01\n---\n",
        )
        code, _, err = self.run_index()
        self.assertEqual(code, 0, err)
        self.assertIn("truncated to 120", err)
        line = next(l for l in self.read("DECISIONS.md").split("\n") if "**Long**" in l)
        self.assertIn("x" * 117 + "...", line)
        self.assertNotIn("x" * 121, line)

    def test_a_missing_marker_is_an_error(self) -> None:
        self.write("DECISIONS.md", "# Decisions — index\n\nno marker here\n")
        code, _, err = self.run_index()
        self.assertEqual(code, 2)
        self.assertIn("GENERATED BELOW THIS LINE", err)


GAMMA = """---
title: Gamma
subject: a third fixture section, added by a test
topic: gamma
updated: 2026-01-06
---

## Session 1 — the only one

**Status**: pending

**Goal**: the goal of gamma
"""

DELTA_BAD_STATUS = """---
title: Delta
subject: a section whose status is not in the vocabulary
topic: delta
updated: 2026-01-01
---

## Session 1 — one

**Status**: nearly

**Goal**: a goal
"""

EPSILON_NO_GOAL = """---
title: Epsilon
subject: a section whose session has no goal
topic: epsilon
updated: 2026-01-01
---

## Session 1 — one

**Status**: pending
"""

LOOSE_FIX_NO_SINCE = """---
title: Loose
subject: a fix item with no Since
topic: loose
updated: 2026-01-01
---

## Something

**Subject**: it is open

**Closes when**: it is not
"""

STATUSED_FIX = """---
title: Statused
subject: a fix item that tries to carry a status
topic: statused
updated: 2026-01-01
---

## Something

**Subject**: it is open

**Since**: 2026-01-01

**Closes when**: it is not

**Status**: open
"""


if __name__ == "__main__":
    unittest.main()
