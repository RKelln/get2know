"""Tests for commons/check.py. Run: python3 -m unittest discover -s tests/commons"""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("commons_check", REPO / "commons" / "check.py")
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)

TODAY = dt.date(2026, 10, 29)

TOOL = '''+++
id = "tool-demo"
kind = "tool"
title = "Demo"
status = "listed-not-vetted"
checked = "2026-10-29"
checked_by = "test"
url = "https://example.org/demo"
licence = "MIT"
osi = true
openness = "1"
open_core = false
vetted = false
last_release = "1.0"
last_release_date = "2026-10-01"
archived = false
runs = ["local"]
does = "Does a demo."
related = ["capability-demo"]
+++
Body.
'''

CAP = '''+++
id = "capability-demo"
kind = "capability"
title = "Demo capability"
level = 0
status = "listed"
checked = "2026-10-29"
checked_by = "test"
moves = ["read"]
hats = ["bookkeeper"]
+++
Body.
'''


class FolderCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def put(self, name, text):
        (self.root / name).write_text(text, encoding="utf-8")

    def problems(self):
        return check.check_folder(self.root, today=TODAY)

    def assertProblem(self, fragment):
        probs = self.problems()
        self.assertTrue(any(fragment in p for p in probs), f"{fragment!r} not in {probs}")


class TestRealRecords(unittest.TestCase):
    def test_seed_records_pass(self):
        self.assertEqual(check.check_folder(REPO / "commons" / "records"), [])


class TestShareSafelyShapes(FolderCase):
    """The story and gap shapes the share-safely skill writes must pass check.py."""

    def test_examples_pass(self):
        import re
        ref = REPO / "skill" / ".agents" / "skills" / "share-safely" / "references" / "commons-records.md"
        blocks = re.findall(r"```\n(\+\+\+\n.*?)```", ref.read_text(encoding="utf-8"), re.S)
        self.assertEqual(len(blocks), 2)
        for block in blocks:
            rid = re.search(r'^id = "(.+?)"', block, re.M).group(1)
            self.put(rid + ".md", block)
        self.assertEqual(check.check_folder(self.root, today=dt.date(2026, 11, 2)), [])


class TestRules(FolderCase):
    def test_valid_pair_passes(self):
        self.put("tool-demo.md", TOOL)
        self.put("capability-demo.md", CAP)
        self.assertEqual(self.problems(), [])

    def test_missing_licence(self):
        self.put("tool-demo.md", TOOL.replace('licence = "MIT"\n', ""))
        self.put("capability-demo.md", CAP)
        self.assertProblem("missing field 'licence'")

    def test_licence_not_spdx(self):
        self.put("tool-demo.md", TOOL.replace('"MIT"', '"open source, mostly"'))
        self.put("capability-demo.md", CAP)
        self.assertProblem("SPDX")

    def test_open_tier_needs_osi(self):
        self.put("tool-demo.md", TOOL.replace("osi = true", "osi = false"))
        self.put("capability-demo.md", CAP)
        self.assertProblem("OSI")

    def test_bad_date_format(self):
        self.put("tool-demo.md", TOOL.replace('checked = "2026-10-29"', 'checked = "29/10/2026"'))
        self.put("capability-demo.md", CAP)
        self.assertProblem("YYYY-MM-DD")

    def test_future_date(self):
        self.put("tool-demo.md", TOOL.replace('"2026-10-01"', '"2027-01-01"'))
        self.put("capability-demo.md", CAP)
        self.assertProblem("in the future")

    def test_duplicate_id(self):
        self.put("tool-demo.md", TOOL)
        sub = self.root / "copy"
        sub.mkdir()
        (sub / "tool-demo.md").write_text(TOOL, encoding="utf-8")
        self.put("capability-demo.md", CAP)
        self.assertProblem("duplicate id")

    def test_broken_link(self):
        self.put("tool-demo.md", TOOL)
        self.assertProblem("'capability-demo' does not exist")

    def test_unvetted_tool_cannot_claim_level_3(self):
        self.put("tool-demo.md", TOOL.replace("vetted = false", "vetted = false\nlevel = 3"))
        self.put("capability-demo.md", CAP)
        self.assertProblem("unvetted tool")

    def test_source_available_must_be_excluded(self):
        t = TOOL.replace('openness = "1"', 'openness = "source-available"').replace("osi = true", "osi = false")
        self.put("tool-demo.md", t)
        self.put("capability-demo.md", CAP)
        self.assertProblem("status 'excluded'")

    def test_capability_level_range(self):
        self.put("tool-demo.md", TOOL)
        self.put("capability-demo.md", CAP.replace("level = 0", "level = 3"))
        self.assertProblem("capability level")

    def test_unknown_move(self):
        self.put("tool-demo.md", TOOL)
        self.put("capability-demo.md", CAP.replace('["read"]', '["summarize"]'))
        self.assertProblem("unknown move")

    def test_file_name_matches_id(self):
        self.put("demo.md", TOOL)
        self.put("capability-demo.md", CAP)
        self.assertProblem("file name must be")

    def test_no_header(self):
        self.put("tool-demo.md", "# Just text\n")
        self.assertProblem("TOML header")


if __name__ == "__main__":
    unittest.main()
