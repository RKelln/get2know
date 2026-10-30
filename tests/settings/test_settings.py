"""Tests for skill/SETTINGS.md, the owner-editable settings. Standard library only.

Run: python3 -m unittest tests/settings/test_settings.py

The skill states each setting's default where it uses it, for when the file is
missing. These tests keep those defaults and the file's numbers the same.
"""

import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

import export_prompt as ep  # noqa: E402

SETTINGS = REPO / "skill" / "SETTINGS.md"
REFS = REPO / "skill" / ".agents" / "skills" / "get2know" / "references"
SKILL_MD = REPO / "skill" / ".agents" / "skills" / "get2know" / "SKILL.md"
LINE = re.compile(r"^- ([^:\n]+): (\d+ days|yes|no)$", re.MULTILINE)
DAYS = {"Re-check after": 30, "Outcome check after": 14}
SAY_WRITTEN = "Say what was written after each answer"
EXPECTED = {**{name: f"{n} days" for name, n in DAYS.items()}, SAY_WRITTEN: "no"}


def raw_settings():
    return dict(LINE.findall(SETTINGS.read_text(encoding="utf-8")))


def settings():
    """The day settings, as numbers."""
    return {name: int(v.split()[0]) for name, v in raw_settings().items() if v.endswith(" days")}


class Settings(unittest.TestCase):
    def test_file_has_only_the_real_settings(self):
        self.assertEqual(raw_settings(), EXPECTED)

    def test_each_line_states_its_default(self):
        text = SETTINGS.read_text(encoding="utf-8")
        for name, value in raw_settings().items():
            block = text.split(f"- {name}: {value}", 1)[1].split("\n- ", 1)[0]
            self.assertIn(f"Default: {value}.", block, name)

    def test_skill_reads_say_written_with_quiet_default(self):
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn(f"**{SAY_WRITTEN}: yes**", skill)
        self.assertIn("Read `SETTINGS.md`", skill)
        self.assertIn("a missing file or line means the default", skill)
        # Quiet is the default: the skill must not tell the interviewer to report every write.
        self.assertNotIn("After writing in `profile/`, say in one short line", skill)

    def test_modes_fallback_matches_file(self):
        modes = (REFS / "returning.md").read_text(encoding="utf-8")
        for name in DAYS:
            self.assertIn(f"**{name}**", modes)
        s = settings()
        self.assertIn(f"use {s['Outcome check after']} days for the first and {s['Re-check after']} for the second", modes)
        # The order of "the first" and "the second" is the order they are named.
        self.assertLess(modes.index("**Outcome check after** and **Re-check after**"), modes.index("use "))

    def test_other_fallbacks_match_file(self):
        n = settings()["Outcome check after"]
        for name in ("opportunities.md", "next-steps.md"):
            text = (REFS / name).read_text(encoding="utf-8")
            self.assertIn("SETTINGS.md", text, name)
            self.assertIn(f"{n} if not set", text, name)

    def test_no_threshold_literals_left(self):
        # The old hard-coded thresholds must not come back into the skill text.
        for path in [SKILL_MD, *REFS.glob("*.md")]:
            text = path.read_text(encoding="utf-8")
            for phrase in ("30 days old", "about 2 weeks", "about two weeks"):
                self.assertNotIn(phrase, text, f"{path.name}: {phrase}")

    def test_chat_prompt_includes_settings(self):
        text = ep.build(warn=lambda m: None)
        self.assertIn("===== File: SETTINGS.md =====", text)
        self.assertIn("- Re-check after: 30 days", text)
        self.assertNotIn("at the top of this folder (next to", text)


if __name__ == "__main__":
    unittest.main()
