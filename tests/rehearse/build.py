"""Prepare the cases: copy the current skill in as a variant.

    uv run --project path/to/rehearse python tests/rehearse/build.py

The bike-shop fixture lives in `fixture/` (made up; CC BY 4.0). `case.toml` gives the agent only
`fixture/shop` (or `fixture/shop-messy`); `fixture/answer-key.md` sits outside those folders and goes
to the judge only. To test a different shop, point a case's `folder` and `answer_key` at it.
Each skill version becomes its own variant folder, named by git commit, so old runs stay explained,
and is listed in every non-mock case*.toml (bike shop and the collective cases alike).
"""
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def main():
    rev = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True, check=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "skill"],
                           capture_output=True, text=True, check=True).stdout.strip()
    name = f"skill-{rev}" + ("-dirty" if dirty else "")
    dest = HERE / "variants" / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(REPO / "skill", dest, symlinks=True, ignore=shutil.ignore_patterns(".DS_Store"))   # keep .claude/skills a link, as in the bundle

    line = f'{name} = "variants/{name}"'
    for case in sorted(HERE.glob("case*.toml")):
        text = case.read_text()
        if "[variants]\n" in text and "seat = \"mock\"" not in text and line not in text:
            case.write_text(text.replace("[variants]\n", f"[variants]\n{line}\n", 1))
    print(f"variant {name} (from skill/ at {rev}{', uncommitted changes' if dirty else ''})")


if __name__ == "__main__":
    main()
