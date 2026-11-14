"""What Get2Know ships: the file list, hashes and version, shared by the build tools.

Standard library only. The shipped folder is `skill/` plus `tools/update.py`
(placed at the folder's top so an owner can run it from a new download).
The owner's own folders (`profile/`, `share/`) are never shipped, even if a
developer has them inside `skill/` while testing.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skill"
TOOLS = REPO / "tools"
DIST = REPO / "dist"

MANIFEST_NAME = "MANIFEST.sha256"
# Top-level folders that belong to the owner. Never shipped, never touched by update.py.
OWNER_DIRS = {"profile", "share", "drafts", "updates-to-review"}
SKIP_NAMES = {".DS_Store", "__pycache__", "Thumbs.db", MANIFEST_NAME}
SKIP_SUFFIXES = (".pyc", ".swp", "~")
# Extra files placed in the shipped folder: published path -> source.
EXTRAS = {"update.py": TOOLS / "update.py"}


def version() -> str:
    return (SKILL / "VERSION").read_text(encoding="utf-8").strip()


def _skipped(name: str) -> bool:
    return name in SKIP_NAMES or name.endswith(SKIP_SUFFIXES)


def shipped_files() -> list[tuple[str, Path]]:
    """(published posix path, source path) for every regular file shipped, sorted."""
    out: dict[str, Path] = {}
    for root, dirs, files in os.walk(SKILL, followlinks=False):
        rel_root = Path(root).relative_to(SKILL)
        # Never descend into owner folders or symlinked folders.
        dirs[:] = sorted(
            d for d in dirs
            if not _skipped(d)
            and not (rel_root == Path(".") and d in OWNER_DIRS)
            and not (Path(root) / d).is_symlink()
        )
        for name in files:
            src = Path(root) / name
            if _skipped(name) or src.is_symlink():
                continue
            out[PurePosixPath(*(rel_root / name).parts).as_posix()] = src
    for rel, src in EXTRAS.items():
        out[rel] = src
    return sorted(out.items())


def shipped_links() -> list[tuple[str, str]]:
    """(published posix path, link target) for symlinks inside skill/, sorted."""
    links = []
    for root, dirs, files in os.walk(SKILL, followlinks=False):
        rel_root = Path(root).relative_to(SKILL)
        if rel_root.parts and rel_root.parts[0] in OWNER_DIRS:
            continue
        for name in dirs + files:
            p = Path(root) / name
            if p.is_symlink():
                links.append((PurePosixPath(*(rel_root / name).parts).as_posix(), os.readlink(p)))
    return sorted(links)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_text() -> str:
    """Lines in `sha256sum` format, so `shasum -a 256 -c MANIFEST.sha256` works on a Mac."""
    return "".join(f"{sha256_file(src)}  {rel}\n" for rel, src in shipped_files())
