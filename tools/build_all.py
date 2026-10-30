# /// script
# requires-python = ">=3.9"
# ///
"""Regenerate everything built from skill/, in order: manifest, chat prompts, zip.

    python3 tools/build_all.py           # (or: uv run tools/build_all.py)
    python3 tools/build_all.py --check   # exit 1 if a committed file is out of date
    python3 tools/build_all.py --base-url https://raw.githubusercontent.com/OWNER/REPO   # links in dist/chat/

The manifest and the chat prompts are committed; --check checks those. The zip
is built locally and published as a GitHub Release asset, not committed
(dist/*.zip is in .gitignore), so --check skips it. Releasing: docs/RELEASING.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_zip  # noqa: E402
import export_prompt  # noqa: E402
import make_manifest  # noqa: E402


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    flags = ["--check"] if "--check" in argv else []
    # --base-url URL goes to the chat prompt step only (links in the staged parts).
    base = argv[argv.index("--base-url"):argv.index("--base-url") + 2] if "--base-url" in argv else []
    rc = 0
    # The zip is not committed, so there is nothing to check it against.
    steps = (make_manifest, export_prompt) if flags else (make_manifest, export_prompt, build_zip)
    for step in steps:
        rc |= step.main(flags + (base if step is export_prompt else []))
        if rc and not flags:
            return rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
