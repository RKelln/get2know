# /// script
# requires-python = ">=3.9"
# ///
"""Build dist/get2know-<version>.zip: the one download an owner needs.

Not committed: it is uploaded as a GitHub Release asset (docs/RELEASING.md).

    python3 tools/build_zip.py           # write it (and remove older get2know-*.zip in dist/)
    python3 tools/build_zip.py --check   # exit 1 if its contents are out of date

The zip holds one folder, `get2know/`: everything in skill/ (with
MANIFEST.sha256, VERSION, CHANGELOG.md, UPDATE.md) plus update.py at the top.
No tests, no repo docs, no profile/ or share/. The `.claude/skills` link is
stored as a link (Unix mode), as in skill/. Entries are sorted and dated
2020-01-01, so the same files give the same zip contents.
Run tools/make_manifest.py first (tools/build_all.py does both).
"""

from __future__ import annotations

import argparse
import stat
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shipped import DIST, MANIFEST_NAME, SKILL, shipped_files, shipped_links, version  # noqa: E402

TOP = "get2know"
DATE = (2020, 1, 1, 0, 0, 0)


def zip_path() -> Path:
    return DIST / f"get2know-{version()}.zip"


def entries() -> list[tuple[str, bytes, int]]:
    """(name in zip, data, unix mode) for every entry, sorted by name."""
    out = [(f"{TOP}/{rel}", src.read_bytes(), 0o100644) for rel, src in shipped_files()]
    manifest = SKILL / MANIFEST_NAME
    if not manifest.exists():
        raise SystemExit(f"skill/{MANIFEST_NAME} is missing: run python3 tools/make_manifest.py")
    out.append((f"{TOP}/{MANIFEST_NAME}", manifest.read_bytes(), 0o100644))
    for rel, target in shipped_links():
        out.append((f"{TOP}/{rel}", target.encode("utf-8"), stat.S_IFLNK | 0o777))
    return sorted(out)


def write_zip(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data, mode in entries():
            info = zipfile.ZipInfo(name, date_time=DATE)
            info.create_system = 3  # Unix, so the modes and the link are kept
            info.external_attr = mode << 16
            info.compress_type = zipfile.ZIP_STORED if stat.S_ISLNK(mode) else zipfile.ZIP_DEFLATED
            zf.writestr(info, data)


def read_zip(path: Path) -> list[tuple[str, bytes, int]]:
    with zipfile.ZipFile(path) as zf:
        return sorted((i.filename, zf.read(i), i.external_attr >> 16) for i in zf.infolist())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    path = zip_path()
    rel = path.relative_to(DIST.parent)
    if args.check:
        if not path.exists() or read_zip(path) != entries():
            print(f"{rel} is out of date: run python3 tools/build_all.py", file=sys.stderr)
            return 1
        print(f"{rel} is up to date")
        return 0
    DIST.mkdir(exist_ok=True)
    for old in DIST.glob("get2know-*.zip"):
        if old != path:
            old.unlink()
    write_zip(path)
    print(f"wrote {rel}: {len(entries())} entries, {path.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
