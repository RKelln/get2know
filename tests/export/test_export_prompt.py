"""Tests for the single-prompt chat export (tools/export_prompt.py). Standard library only.

Run: python3 -m unittest tests/export/test_export_prompt.py tests/update/test_update.py
"""

import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

import export_prompt as ep  # noqa: E402

SKILL_MD = REPO / "skill" / ".agents" / "skills" / "get2know" / "SKILL.md"
DYK_MD = REPO / "skill" / ".agents" / "skills" / "did-you-know" / "SKILL.md"
RULE = re.compile(r"^(\d+)\. \*\*(.+?)\*\*.*$", re.MULTILINE)


def section(text, heading):
    """Text under a '## heading' (by prefix) up to the next '## '."""
    m = re.search(r"^## " + re.escape(heading) + r".*?$(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return m.group(1) if m else ""


def rewritten(line):
    """The line as the export rewrites it."""
    for pattern, repl in ep.REWRITES:
        line = re.sub(pattern, repl, line, flags=re.MULTILINE)
    return line


class ExportPrompt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = ep.build(warn=lambda m: None)

    def test_every_rule_kept(self):
        for path, heading in ((SKILL_MD, "Rules"), (DYK_MD, "Rules")):
            src_rules = RULE.findall(section(path.read_text(encoding="utf-8"), heading))
            self.assertTrue(src_rules, f"no numbered rules found in {path.name}")
            for m in RULE.finditer(section(path.read_text(encoding="utf-8"), heading)):
                line = m.group(0)
                self.assertIn(rewritten(line).strip(), self.text, f"rule missing from prompt: {line[:70]}")

    def test_rule_numbering_intact(self):
        src = RULE.findall(section(SKILL_MD.read_text(encoding="utf-8"), "Rules"))
        out = self.text.split("===== File: SKILL.md (get2know) =====", 1)[1]
        out_rules = RULE.findall(section(out, "Rules"))
        self.assertEqual([n for n, _ in src], [n for n, _ in out_rules])

    def test_core_rules_named(self):
        # The adapter must not drop the rules that matter most in a chat.
        for phrase in ("One question per message", "Privacy"):
            self.assertIn(phrase, self.text)

    def test_every_included_file_present(self):
        for name, path in ep.included_files():
            self.assertIn(f"===== File: {name} =====", self.text)
            first_heading = next((l for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("# ")), None)
            if first_heading:
                self.assertIn(first_heading, self.text, name)

    def test_no_tool_specific_leftovers(self):
        self.assertEqual(ep.leftovers(self.text), [])
        for phrase in ("Read tool", "Write tool", "Edit tool", "write and edit tools", "file tools"):
            self.assertNotIn(phrase, self.text)

    def test_no_empty_inline_code(self):
        # A rewrite that removes a path must not leave `` behind (``` fences are fine).
        hits = [m.start() for m in re.finditer(r"(?<!`)``(?!`)", self.text)]
        self.assertEqual(hits, [], "empty inline code at " + ", ".join(
            f"line {self.text[:i].count(chr(10)) + 1}" for i in hits))

    def test_no_frontmatter(self):
        self.assertNotIn("\nname: get2know\n", self.text)
        self.assertNotIn("description: Interview the owner", self.text)

    def test_adapter_explains_chat(self):
        for phrase in ("Save as: profile/", "four backticks", "paste", "Resume", "Nothing is saved until"):
            self.assertIn(phrase, self.text)
        self.assertIn(ep.version(), self.text.splitlines()[0])
        self.assertNotIn(ep.SPLIT, self.text)
        self.assertNotIn("{version}", self.text)

    def test_code_fences_balanced(self):
        fences = [l for l in self.text.splitlines() if l.lstrip().startswith("```")]
        self.assertEqual(len(fences) % 2, 0)

    def test_size_under_limit(self):
        self.assertLess(len(self.text), ep.MAX_CHARS, ep.size_report(self.text))

    def test_deterministic(self):
        self.assertEqual(self.text, ep.build(warn=lambda m: None))

    def test_dist_up_to_date(self):
        self.assertTrue(ep.OUT.exists(), "dist/get2know-prompt.md missing: run python3 tools/build_all.py")
        self.assertEqual(ep.OUT.read_text(encoding="utf-8"), self.text,
                         "dist/get2know-prompt.md is out of date: run python3 tools/build_all.py")


if __name__ == "__main__":
    unittest.main()
