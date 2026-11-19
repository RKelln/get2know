"""Tests for skill/.agents/skills/teach-a-job/scripts/install_skill.py. Standard library only.

Run: python3 -m unittest tests/teach_a_job/test_install_skill.py
"""

import contextlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "skill" / ".agents" / "skills" / "teach-a-job" / "scripts" / "install_skill.py"
spec = importlib.util.spec_from_file_location("install_skill", SCRIPT)
install_skill = importlib.util.module_from_spec(spec)
spec.loader.exec_module(install_skill)

GOOD = "---\nname: {name}\ndescription: Chase late payers. Use when someone has not paid.\n---\n\n# Job\n\n**Do:** it.\n"


class InstallSkill(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.kit = Path(self._tmp.name) / "kit"
        (self.kit / ".agents" / "skills" / "get2know").mkdir(parents=True)
        (self.kit / ".agents" / "skills" / "get2know" / "SKILL.md").write_text("kit skill\n")
        (self.kit / "MANIFEST.sha256").write_text("abc  .agents/skills/some-new-kit-skill/SKILL.md\n")

    def add(self, name="late-reminders", text=None, folder=None):
        path = self.kit / "profile" / "skills" / (folder or name)
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text(GOOD.format(name=name) if text is None else text)
        return path

    def run_it(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = install_skill.main(["--kit", str(self.kit), *args])
        return code, out.getvalue(), err.getvalue()

    def installed(self, name="late-reminders"):
        return self.kit / ".agents" / "skills" / name

    def test_copy_is_the_default_and_keeps_scripts(self):
        source = self.add()
        (source / "count.py").write_text("print(1)\n")
        code, out, _ = self.run_it("late-reminders")
        self.assertEqual(code, 0)
        self.assertIn("A new chat can find it", out)
        self.assertFalse(self.installed().is_symlink())
        self.assertEqual((self.installed() / "count.py").read_text(), "print(1)\n")

    def test_installs_into_claude_skills_too_unless_agents_only(self):
        self.add()
        code, out, _ = self.run_it("late-reminders")
        self.assertEqual(code, 0)
        self.assertTrue((self.kit / ".claude" / "skills" / "late-reminders" / "SKILL.md").is_file())
        self.add(name="other-job")
        self.run_it("other-job", "--agents-only")
        self.assertTrue(self.installed("other-job").is_dir())
        self.assertFalse((self.kit / ".claude" / "skills" / "other-job").exists())

    def test_claude_skills_link_to_agents_skills_installs_once(self):
        self.add()
        (self.kit / ".claude").mkdir()
        os.symlink("../.agents/skills", self.kit / ".claude" / "skills")
        code, out, _ = self.run_it("late-reminders")
        self.assertEqual(code, 0)
        self.assertEqual(out.count("Installed"), 1)

    def test_copy_does_not_follow_later_changes_until_reinstalled(self):
        source = self.add()
        self.run_it("late-reminders")
        (source / "SKILL.md").write_text(GOOD.format(name="late-reminders") + "\nNew rule.\n")
        self.assertNotIn("New rule", (self.installed() / "SKILL.md").read_text())
        self.assertEqual(self.run_it("late-reminders")[0], 0)
        self.assertIn("New rule", (self.installed() / "SKILL.md").read_text())

    def test_link_is_relative_and_follows_changes(self):
        source = self.add()
        self.assertEqual(self.run_it("late-reminders", "--link")[0], 0)
        self.assertTrue(self.installed().is_symlink())
        self.assertFalse(os.path.isabs(os.readlink(self.installed())))
        (source / "SKILL.md").write_text(GOOD.format(name="late-reminders") + "\nNew rule.\n")
        self.assertIn("New rule", (self.installed() / "SKILL.md").read_text())

    def test_link_again_leaves_the_source_alone(self):
        source = self.add()
        self.run_it("late-reminders", "--link")
        self.assertEqual(self.run_it("late-reminders", "--link")[0], 0)
        self.assertTrue((source / "SKILL.md").is_file())

    def test_target_installs_elsewhere(self):
        self.add()
        other = Path(self._tmp.name) / "other-tool" / "skills"
        self.assertEqual(self.run_it("late-reminders", "--target", str(other))[0], 0)
        self.assertTrue((other / "late-reminders" / "SKILL.md").is_file())
        self.assertFalse(self.installed().exists())

    def test_dry_run_changes_nothing(self):
        self.add()
        code, out, _ = self.run_it("late-reminders", "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("Nothing was changed", out)
        self.assertFalse(self.installed().exists())

    def test_refuses_the_kits_own_skills(self):
        for name in ("get2know", "teach-a-job", "some-new-kit-skill"):
            self.add(name=name)
            code, _, err = self.run_it(name)
            self.assertEqual(code, 1, name)
            self.assertIn("kit's own", err)
        self.assertEqual((self.installed("get2know") / "SKILL.md").read_text(), "kit skill\n")

    def test_refuses_names_that_leave_the_folder(self):
        for name in ("../evil", "a/b", "Bad Name", ".hidden", "-x", "x" * 65):
            code, _, err = self.run_it("--", name)
            self.assertEqual(code, 1, name)
            self.assertIn("not a usable name", err)

    def test_refuses_a_skill_that_would_not_load(self):
        cases = {
            "no frontmatter": "# Just a heading\n",
            "not closed": "---\nname: late-reminders\ndescription: x\n",
            "wrong name": GOOD.format(name="other"),
            "no description": "---\nname: late-reminders\n---\n\nBody\n",
            "long description": f"---\nname: late-reminders\ndescription: {'x' * 1025}\n---\n\nBody\n",
            "colon": "---\nname: late-reminders\ndescription: Use when: late\n---\n\nBody\n",
            "no body": "---\nname: late-reminders\ndescription: fine\n---\n",
        }
        for why, text in cases.items():
            source = self.add(text=text)
            code, _, err = self.run_it("late-reminders")
            self.assertEqual(code, 1, why)
            self.assertTrue(err.startswith("Not installed:"), why)
            self.assertFalse(self.installed().exists(), why)
            (source / "SKILL.md").unlink()
            source.rmdir()

    def test_a_quoted_colon_is_fine(self):
        self.add(text='---\nname: late-reminders\ndescription: "Use when: late"\n---\n\nBody\n')
        self.assertEqual(self.run_it("late-reminders")[0], 0)

    def test_refuses_a_link_inside_the_skill(self):
        source = self.add()
        (source / "sneaky").symlink_to("/etc/hostname")
        code, _, err = self.run_it("late-reminders")
        self.assertEqual(code, 1)
        self.assertIn("is a link", err)

    def test_all_installs_every_skill(self):
        self.add("late-reminders")
        self.add("weekly-note")
        code, out, _ = self.run_it("--all")
        self.assertEqual(code, 0)
        self.assertTrue(self.installed("late-reminders").is_dir())
        self.assertTrue(self.installed("weekly-note").is_dir())
        self.assertEqual(out.count("Installed"), 4)  # two skills, two skill folders

    def test_all_changes_nothing_if_one_is_bad(self):
        self.add("late-reminders")
        self.add("weekly-note", text="# broken\n")
        self.assertEqual(self.run_it("--all")[0], 1)
        self.assertFalse(self.installed("late-reminders").exists())

    def test_needs_exactly_one_of_name_or_all(self):
        self.add()
        self.assertEqual(self.run_it()[0], 1)
        self.assertEqual(self.run_it("late-reminders", "--all")[0], 1)
        self.assertEqual(self.run_it("--all", "--dry-run")[0], 0)

    def test_missing_skill_says_so(self):
        code, _, err = self.run_it("nothing-here")
        self.assertEqual(code, 1)
        self.assertIn("There is no folder", err)


if __name__ == "__main__":
    unittest.main()
