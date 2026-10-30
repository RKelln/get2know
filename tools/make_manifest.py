# /// script
# requires-python = ">=3.9"
# ///
"""Write skill/MANIFEST.sha256: the hash of every file this version ships.

    python3 tools/make_manifest.py           # write it
    python3 tools/make_manifest.py --check   # exit 1 if it is out of date

update.py compares an owner's files with this list to tell which ones the owner
changed (keep them) from which ones are as shipped (safe to replace). The format
is the one `sha256sum` and `shasum -a 256` use, so on a Mac
`shasum -a 256 -c MANIFEST.sha256` lists changed files with no Python needed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shipped import MANIFEST_NAME, SKILL, manifest_text  # noqa: E402

OUT = SKILL / MANIFEST_NAME


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    text = manifest_text()
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print(f"skill/{MANIFEST_NAME} is out of date: run python3 tools/build_all.py", file=sys.stderr)
            return 1
        print(f"skill/{MANIFEST_NAME} is up to date ({text.count(chr(10))} files)")
        return 0
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote skill/{MANIFEST_NAME}: {text.count(chr(10))} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
