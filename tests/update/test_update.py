"""Tests for tools/update.py, the manifest and the zip. Standard library only.

Run: python3 -m unittest tests/export/test_export_prompt.py tests/update/test_update.py
"""

import hashlib
import io
import os
import stat
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

import build_zip  # noqa: E402
import make_manifest  # noqa: E402
import shipped  # noqa: E402
import update  # noqa: E402


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_release(folder: Path, version: str, files: dict) -> Path:
    """A fake Get2Know version: files plus VERSION and a manifest."""
    files = dict(files, VERSION=version + "\n")
    for rel, text in files.items():
        p = folder / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    manifest = "".join(f"{sha(t.encode())}  {r}\n" for r, t in sorted(files.items()))
    (folder / update.MANIFEST).write_text(manifest, encoding="utf-8")
    return folder


V1 = {
    "AGENTS.md": "agents v1\n",
    ".agents/skills/get2know/SKILL.md": "skill v1\n",
    ".agents/skills/did-you-know/cards.md": "cards v1\n",
    ".agents/skills/get2know/references/old.md": "old ref\n",
    ".agents/skills/get2know/references/old-edited.md": "old ref 2\n",
}
V2 = {
    "AGENTS.md": "agents v2\n",
    ".agents/skills/get2know/SKILL.md": "skill v2\n",
    ".agents/skills/did-you-know/cards.md": "cards v2\n",
    ".agents/skills/get2know/references/new.md": "new ref\n",
}


def run(*args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = update.main([str(a) for a in args])
    return rc, buf.getvalue()


class UpdateFolder(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.old = make_release(base / "mine", "0.1.0", V1)
        self.new = make_release(base / "download", "0.2.0", V2)
        # The owner's own things.
        (self.old / "profile").mkdir()
        (self.old / "profile" / "limits.md").write_text("never hand off: the phone\n")
        (self.old / "share").mkdir()
        (self.old / "share" / "brief.md").write_text("shared\n")
        (self.old / "my-notes.txt").write_text("mine\n")
        # The owner edited two shipped files.
        (self.old / ".agents/skills/did-you-know/cards.md").write_text("cards v1 plus my own card\n")
        (self.old / ".agents/skills/get2know/references/old-edited.md").write_text("my edits\n")

    def tearDown(self):
        self.tmp.cleanup()

    def read(self, rel):
        return (self.old / rel).read_text()

    def test_dry_run_changes_nothing(self):
        before = {p: p.read_bytes() for p in self.old.rglob("*") if p.is_file()}
        rc, out = run(self.old, "--dry-run", "--from", self.new)
        self.assertEqual(rc, 0)
        self.assertIn("from version 0.1.0 to version 0.2.0", out)
        after = {p: p.read_bytes() for p in self.old.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_update(self):
        rc, out = run(self.old, "--yes", "--from", self.new)
        self.assertEqual(rc, 0, out)
        # Unchanged shipped files are replaced; new files added; old unchanged removed.
        self.assertEqual(self.read("AGENTS.md"), "agents v2\n")
        self.assertEqual(self.read(".agents/skills/get2know/SKILL.md"), "skill v2\n")
        self.assertEqual(self.read(".agents/skills/get2know/references/new.md"), "new ref\n")
        self.assertFalse((self.old / ".agents/skills/get2know/references/old.md").exists())
        self.assertEqual(self.read("VERSION"), "0.2.0\n")
        # Owner edits kept, new copy put aside for review.
        self.assertEqual(self.read(".agents/skills/did-you-know/cards.md"), "cards v1 plus my own card\n")
        self.assertEqual(self.read("updates-to-review/0.2.0/.agents/skills/did-you-know/cards.md"), "cards v2\n")
        self.assertEqual(self.read(".agents/skills/get2know/references/old-edited.md"), "my edits\n")
        # The owner's folders and files untouched.
        self.assertEqual(self.read("profile/limits.md"), "never hand off: the phone\n")
        self.assertEqual(self.read("share/brief.md"), "shared\n")
        self.assertEqual(self.read("my-notes.txt"), "mine\n")
        # The new manifest is in place.
        self.assertEqual(self.read(update.MANIFEST), (self.new / update.MANIFEST).read_text())

    def test_second_run_is_stable(self):
        run(self.old, "--yes", "--from", self.new)
        rc, out = run(self.old, "--dry-run", "--from", self.new)
        self.assertEqual(rc, 0)
        self.assertNotIn("Replace", out)
        self.assertIn("Keep yours", out)  # the owner's edit stays theirs

    def test_never_writes_owner_folders_even_if_listed(self):
        # A tampered or buggy manifest naming profile/ or ../ must be ignored.
        (self.new / "profile").mkdir()
        (self.new / "profile" / "limits.md").write_text("overwritten!\n")
        m = self.new / update.MANIFEST
        m.write_text(m.read_text()
                     + f"{sha(b'overwritten!' + bytes([10]))}  profile/limits.md\n"
                     + f"{sha(b'x')}  ../escape.md\n"
                     + f"{sha(b'x')}  /etc/passwd\n")
        rc, out = run(self.old, "--yes", "--from", self.new)
        self.assertEqual(rc, 0, out)
        self.assertEqual(self.read("profile/limits.md"), "never hand off: the phone\n")
        self.assertFalse((self.old.parent / "escape.md").exists())

    def test_owner_folders_any_case(self):
        for rel in ("Profile/limits.md", "SHARE/x.md", "Updates-To-Review/a.md"):
            self.assertFalse(update.safe_rel(rel), rel)

    def test_odd_version_not_used_in_a_path(self):
        (self.new / "VERSION").write_text("../../evil\n")
        self.assertEqual(update.read_version(self.new), "unknown")
        (self.new / "VERSION").write_text("0.2.0\n")
        self.assertEqual(update.read_version(self.new), "0.2.0")

    def test_refuses_damaged_download(self):
        (self.new / "AGENTS.md").write_text("corrupt\n")
        rc, out = run(self.old, "--yes", "--from", self.new)
        self.assertEqual(rc, 1)
        self.assertIn("damaged", out)
        self.assertEqual(self.read("AGENTS.md"), "agents v1\n")

    def test_refuses_non_get2know_folder(self):
        other = Path(self.tmp.name) / "photos"
        other.mkdir()
        rc, out = run(other, "--yes", "--from", self.new)
        self.assertEqual(rc, 1)
        self.assertEqual(list(other.iterdir()), [])

    def test_refuses_same_folder(self):
        rc, _ = run(self.new, "--yes", "--from", self.new)
        self.assertEqual(rc, 1)

    def test_no_old_manifest_keeps_differences(self):
        (self.old / update.MANIFEST).unlink()
        rc, out = run(self.old, "--yes", "--from", self.new)
        self.assertEqual(rc, 0, out)
        self.assertEqual(self.read("AGENTS.md"), "agents v1\n")  # cannot tell; kept
        self.assertEqual(self.read("updates-to-review/0.2.0/AGENTS.md"), "agents v2\n")

    def test_restores_link(self):
        (self.new / ".claude").mkdir()
        os.symlink("../.agents/skills", self.new / ".claude" / "skills")
        rc, out = run(self.old, "--yes", "--from", self.new)
        self.assertEqual(rc, 0, out)
        link = self.old / ".claude" / "skills"
        self.assertTrue(link.is_symlink())
        self.assertTrue((link / "get2know" / "SKILL.md").is_file())

    def test_no_tty_without_yes_changes_nothing(self):
        rc, out = run(self.old, "--from", self.new)  # stdin is not a terminal under unittest
        if sys.stdin.isatty():
            self.skipTest("stdin is a terminal")
        self.assertIn("--yes", out)
        self.assertEqual(self.read("AGENTS.md"), "agents v1\n")


def extract_with_links(zpath: Path, dest: Path):
    """Unzip, recreating symbolic links the way macOS Archive Utility does."""
    with zipfile.ZipFile(zpath) as zf:
        for info in zf.infolist():
            target = dest / info.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            if stat.S_ISLNK(info.external_attr >> 16):
                os.symlink(zf.read(info).decode(), target)
            else:
                target.write_bytes(zf.read(info))


class SettingsFile(unittest.TestCase):
    """SETTINGS.md is the file owners are told to edit: an update must keep their numbers."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.old = make_release(base / "mine", "0.1.0", dict(V1, **{"SETTINGS.md": "- Re-check after: 30 days\n"}))
        self.new = make_release(base / "download", "0.2.0", dict(
            V2, **{"SETTINGS.md": "- Re-check after: 30 days\n- Outcome check after: 14 days\n"}))

    def tearDown(self):
        self.tmp.cleanup()

    def test_owner_numbers_kept_new_copy_for_review(self):
        (self.old / "SETTINGS.md").write_text("- Re-check after: 60 days\n")
        rc, out = run(self.old, "--yes", "--from", self.new)
        self.assertEqual(rc, 0, out)
        self.assertEqual((self.old / "SETTINGS.md").read_text(), "- Re-check after: 60 days\n")
        self.assertEqual((self.old / "updates-to-review/0.2.0/SETTINGS.md").read_text(),
                         (self.new / "SETTINGS.md").read_text())

    def test_unchanged_settings_replaced(self):
        rc, out = run(self.old, "--yes", "--from", self.new)
        self.assertEqual(rc, 0, out)
        self.assertEqual((self.old / "SETTINGS.md").read_text(), (self.new / "SETTINGS.md").read_text())
        self.assertFalse((self.old / "updates-to-review/0.2.0/SETTINGS.md").exists())

    def test_added_when_old_version_had_none(self):
        (self.old / "SETTINGS.md").unlink()
        # An older version without the file: drop it from the old manifest too.
        m = self.old / update.MANIFEST
        m.write_text("".join(l for l in m.read_text().splitlines(True) if not l.endswith("  SETTINGS.md\n")))
        rc, out = run(self.old, "--yes", "--from", self.new)
        self.assertEqual(rc, 0, out)
        self.assertEqual((self.old / "SETTINGS.md").read_text(), (self.new / "SETTINGS.md").read_text())


class ShippedBuild(unittest.TestCase):
    def test_manifest_up_to_date(self):
        path = shipped.SKILL / shipped.MANIFEST_NAME
        self.assertTrue(path.exists(), "run python3 tools/build_all.py")
        self.assertEqual(path.read_text(encoding="utf-8"), shipped.manifest_text(),
                         "skill/MANIFEST.sha256 is out of date: run python3 tools/build_all.py")

    def test_shipped_files(self):
        rels = [r for r, _ in shipped.shipped_files()]
        for must in ("AGENTS.md", "VERSION", "CHANGELOG.md", "UPDATE.md", "SETTINGS.md", "update.py",
                     ".agents/skills/get2know/SKILL.md"):
            self.assertIn(must, rels)
        for rel in rels:
            self.assertFalse(rel.startswith(("profile/", "share/", "tests/", "updates-to-review/")), rel)
            self.assertNotIn("__pycache__", rel)
            self.assertTrue(update.safe_rel(rel), rel)
        self.assertNotIn(shipped.MANIFEST_NAME, rels)

    def test_zip_not_committed(self):
        # The zip is a Release asset, built at release time (docs/RELEASING.md).
        ignore = (shipped.REPO / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("dist/*.zip", ignore)

    def test_zip_deterministic_and_installable(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            a, b = tmp / "a.zip", tmp / "b.zip"
            build_zip.write_zip(a)
            build_zip.write_zip(b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            names = [i.filename for i in zipfile.ZipFile(a).infolist()]
            self.assertTrue(all(n.startswith("get2know/") for n in names))
            self.assertFalse(any("/tests/" in n or "/profile/" in n for n in names))
            # Unzip as an owner would, then update an older install from it.
            extract_with_links(a, tmp / "new")
            new = tmp / "new" / "get2know"
            self.assertTrue((new / ".claude" / "skills" / "get2know" / "SKILL.md").is_file())
            old = make_release(tmp / "old", "0.0.1", {"AGENTS.md": "old agents\n"})
            (old / "profile").mkdir()
            (old / "profile" / "log.md").write_text("# Log\n")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = update.main([str(old), "--yes", "--from", str(new)])
            self.assertEqual(rc, 0, buf.getvalue())
            self.assertEqual((old / "profile" / "log.md").read_text(), "# Log\n")
            self.assertEqual((old / "VERSION").read_text().strip(), shipped.version())
            self.assertEqual((old / "AGENTS.md").read_bytes(), (shipped.SKILL / "AGENTS.md").read_bytes())
            self.assertTrue((old / ".claude" / "skills").is_symlink())


if __name__ == "__main__":
    unittest.main()
