# /// script
# requires-python = ">=3.8"
# ///
"""Update your Get2Know folder to the version this file came with.

How to run it (see UPDATE.md for the steps in plain words):

    python3 update.py YOUR-GET2KNOW-FOLDER            # shows the plan, then asks
    python3 update.py YOUR-GET2KNOW-FOLDER --dry-run  # only shows the plan
    python3 update.py YOUR-GET2KNOW-FOLDER --yes      # no question (for helpers)

What it does, in your folder:
- Never touches profile/, share/, or any file Get2Know did not ship.
- Replaces Get2Know's own files that you have not changed.
- Keeps every Get2Know file you changed, as you left it, and puts the new
  version's copy in updates-to-review/<version>/ so you can compare.
- Adds new files, and removes old Get2Know files you never changed.

It knows which files you changed from MANIFEST.sha256, the list of files and
their fingerprints (hashes) that came with your version.
Standard library only; this file must not import anything from the repo.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath

MANIFEST = "MANIFEST.sha256"
OWNER_DIRS = {"profile", "share", "updates-to-review"}
REVIEW_DIR = "updates-to-review"


class Stop(Exception):
    """A plain-language reason to stop without changing anything."""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_rel(rel: str) -> bool:
    """A manifest path we are willing to write: relative, inside the folder, not the owner's."""
    if not rel or "\\" in rel or rel.startswith("/") or rel == MANIFEST:
        return False
    parts = PurePosixPath(rel).parts
    # Case-insensitive: on a Mac or Windows disk, Profile/ and profile/ are the same folder.
    return ".." not in parts and "." not in parts and parts[0].lower() not in OWNER_DIRS and ":" not in parts[0]


def read_manifest(folder: Path):
    path = folder / MANIFEST
    if not path.is_file():
        return None
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, sep, rel = line.partition("  ")
        if not sep or len(digest) != 64:
            continue
        rel = rel.lstrip("*")
        if safe_rel(rel):
            out[rel] = digest
    return out


VERSION_SHAPE = re.compile(r"^[0-9A-Za-z][0-9A-Za-z.+-]{0,31}$")


def read_version(folder: Path) -> str:
    """The folder's VERSION, or "unknown". It is used in a folder name
    (updates-to-review/<version>/), so anything but a plain version is refused."""
    p = folder / "VERSION"
    v = p.read_text(encoding="utf-8", errors="replace").strip() if p.is_file() else ""
    return v if VERSION_SHAPE.match(v) and ".." not in v else "unknown"


def version_tuple(v: str):
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return None


def inside(root: Path, path: Path) -> bool:
    """True if path (resolved through any links) stays inside root."""
    root_r = os.path.realpath(root)
    path_r = os.path.realpath(path)
    return path_r == root_r or path_r.startswith(root_r + os.sep)


def existing_ancestor(path: Path) -> Path:
    while not path.exists() and not path.is_symlink() and path != path.parent:
        path = path.parent
    return path


def find_links(folder: Path):
    """Symbolic links in the new folder (like .claude/skills), outside owner folders."""
    links = []
    for root, dirs, files in os.walk(folder, followlinks=False):
        rel_root = Path(root).relative_to(folder)
        if rel_root.parts and rel_root.parts[0].lower() in OWNER_DIRS:
            dirs[:] = []
            continue
        for name in dirs + files:
            p = Path(root) / name
            if p.is_symlink():
                links.append((PurePosixPath(*(rel_root / name).parts).as_posix(), os.readlink(p)))
    return sorted(links)


def make_plan(old: Path, new: Path):
    """Return (plan, notes). plan is a list of (action, rel). Nothing is changed."""
    if os.path.realpath(old) == os.path.realpath(new):
        raise Stop("That is the new folder itself. Give the path of your old Get2Know folder, the one with profile/ in it.")
    if not old.is_dir():
        raise Stop(f"There is no folder at {old}.")
    if not ((old / "AGENTS.md").is_file() or (old / ".agents" / "skills" / "get2know").is_dir()):
        raise Stop(f"{old} does not look like a Get2Know folder (no AGENTS.md). Nothing was changed.")
    new_m = read_manifest(new)
    if not new_m:
        raise Stop(f"The new version has no {MANIFEST}. Download it again. Nothing was changed.")
    for rel, digest in new_m.items():
        src = new / rel
        if not src.is_file() or sha256(src) != digest:
            raise Stop(f"The new download looks damaged ({rel}). Download it again. Nothing was changed.")
    old_m = read_manifest(old)
    notes = []
    if old_m is None:
        old_m = {}
        notes.append(f"Your folder has no {MANIFEST}, so any Get2Know file that differs from the new one is treated as changed by you and kept.")

    plan = []
    for rel, digest in sorted(new_m.items()):
        dst = old / rel
        if not inside(old, existing_ancestor(dst.parent)):
            plan.append(("skip-outside", rel))
        elif dst.is_symlink() or (dst.exists() and not dst.is_file()):
            plan.append(("skip-odd", rel))
        elif not dst.exists():
            plan.append(("restore" if rel in old_m else "add", rel))
        else:
            current = sha256(dst)
            if current == digest:
                plan.append(("same", rel))
            elif old_m.get(rel) == current:
                plan.append(("replace", rel))
            else:
                plan.append(("keep-changed", rel))
    for rel, digest in sorted(old_m.items()):
        if rel in new_m:
            continue
        dst = old / rel
        if dst.is_file() and not dst.is_symlink() and inside(old, dst.parent):
            plan.append(("remove" if sha256(dst) == digest else "keep-removed", rel))
    for rel, target in find_links(new):
        if not safe_rel(rel):
            continue
        dst = old / rel
        if not dst.exists() and not dst.is_symlink():
            plan.append(("link", rel))
        elif not dst.is_symlink():
            plan.append(("skip-link", rel))
    return plan, notes


SAY = {
    "add": "Add (new in this version)",
    "restore": "Put back (missing from your folder)",
    "replace": "Replace (you had not changed it)",
    "keep-changed": f"Keep yours (you changed it; the new copy goes in {REVIEW_DIR}/)",
    "remove": "Remove (no longer part of Get2Know; you had not changed it)",
    "keep-removed": "Keep yours (no longer part of Get2Know, but you changed it)",
    "link": "Add the link",
    "skip-link": "Leave as is (a folder or file where the new version has a link)",
    "skip-odd": "Leave as is (not a plain file in your folder)",
    "skip-outside": "Leave as is (it points outside your folder)",
}


def describe(plan, old_v: str, new_v: str, notes) -> str:
    lines = [f"Get2Know update: from version {old_v} to version {new_v}."]
    vt_old, vt_new = version_tuple(old_v), version_tuple(new_v)
    if vt_old and vt_new and vt_new < vt_old:
        lines.append("Careful: the new folder is an OLDER version than yours.")
    lines += notes
    lines.append("Your profile/ and share/ folders, and any files of your own, are not touched.")
    changes = [(a, r) for a, r in plan if a != "same"]
    if not changes:
        lines.append("Nothing to change: your Get2Know files already match.")
    for action in SAY:
        rels = [r for a, r in changes if a == action]
        if rels:
            lines.append(f"{SAY[action]}:")
            lines += [f"  {r}" for r in rels]
    return "\n".join(lines)


def copy_file(src: Path, dst: Path) -> None:
    """Copy safely: write a temporary file next to dst, then swap it in."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dst.parent, prefix=".g2k-")
    os.close(fd)
    try:
        shutil.copyfile(src, tmp)
        os.replace(tmp, dst)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def apply(plan, old: Path, new: Path, new_v: str) -> list[str]:
    review = old / REVIEW_DIR / new_v
    kept = []
    for action, rel in plan:
        src, dst = new / rel, old / rel
        if action in ("add", "restore", "replace"):
            if not inside(old, existing_ancestor(dst.parent)):
                continue
            copy_file(src, dst)
        elif action == "keep-changed":
            copy_file(src, review / rel)
            kept.append(rel)
        elif action == "remove":
            dst.unlink()
        elif action == "link":
            dst.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(os.readlink(src), dst)
    if kept:
        (review / "README.txt").write_text(
            f"These are Get2Know {new_v}'s copies of files you had changed.\n"
            "Your own versions were kept, in their usual places.\n"
            "Compare each one with yours, copy over any part you want, then delete this folder.\n",
            encoding="utf-8",
        )
    copy_file(new / MANIFEST, old / MANIFEST)
    return kept


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Update a Get2Know folder to the version this file came with.")
    ap.add_argument("folder", help="your Get2Know folder (the one with profile/ in it)")
    ap.add_argument("--dry-run", action="store_true", help="only show what would change")
    ap.add_argument("--yes", action="store_true", help="do not ask before changing files")
    ap.add_argument("--from", dest="new", default=None, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    new = Path(args.new).expanduser() if args.new else Path(__file__).resolve().parent
    old = Path(args.folder.strip().strip("'\"")).expanduser()
    try:
        plan, notes = make_plan(old, new)
    except Stop as e:
        print(e)
        return 1
    new_v, old_v = read_version(new), read_version(old)
    print(describe(plan, old_v, new_v, notes))
    if args.dry_run or all(a == "same" for a, _ in plan) and not notes:
        return 0
    if not args.yes:
        if not sys.stdin.isatty():
            print("Not changed: run again with --yes to go ahead.")
            return 0
        if input("Go ahead? Type y and press Return: ").strip().lower() not in ("y", "yes"):
            print("Stopped. Nothing was changed.")
            return 0
    kept = apply(plan, old, new, new_v)
    print(f"Done. Your folder is now version {new_v}.")
    if kept:
        print(f"You had changed {len(kept)} Get2Know file(s). Yours are kept; the new copies are in {REVIEW_DIR}/{new_v}/.")
    print("You can delete the folder you downloaded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
