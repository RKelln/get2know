#!/usr/bin/env python3
"""Check the capability commons records. Standard library only (Python 3.11+).

Usage:  python3 commons/check.py [records-folder]
Prints one line per problem and exits 1 if there are any.

Each record is a Markdown file with a TOML header between two `+++` lines.
The rules here are the ones in commons/README.md; change both together.
"""
from __future__ import annotations

import datetime as _dt
import re
import sys
import tomllib
from pathlib import Path

KINDS = {"capability", "recipe", "tool", "story", "gap"}
STATUSES = {"found", "listed", "listed-not-vetted", "vetted", "stale", "excluded"}
MOVES = {"read", "draft", "check", "sort", "watch", "connect", "build"}
OPENNESS = {"1", "2", "source-available"}
RUNS = {"offline", "local", "self-hosted", "hosted"}
COMMON_REQUIRED = ("id", "kind", "title", "status", "checked", "checked_by")
TOOL_REQUIRED = ("url", "licence", "osi", "openness", "open_core", "vetted",
                 "last_release", "last_release_date", "archived", "runs", "does")
LEVEL_BY_KIND = {"capability": {0, 1}, "recipe": {2}}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# SPDX ids or expressions: ids joined by OR / AND / WITH, or a LicenseRef-.
SPDX_EXPR = re.compile(
    r"^(LicenseRef-[A-Za-z0-9.-]+|[A-Za-z0-9.+-]+)"
    r"( (OR|AND|WITH) (LicenseRef-[A-Za-z0-9.-]+|[A-Za-z0-9.+-]+))*$")


def parse(path: Path) -> tuple[dict, str]:
    """Return (header, body). Raises ValueError on a malformed file."""
    text = path.read_text(encoding="utf-8")
    parts = text.split("+++\n", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError("must start with a TOML header between two '+++' lines")
    try:
        header = tomllib.loads(parts[1])
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"bad TOML header: {e}") from None
    return header, parts[2]


def _date_ok(value, today: _dt.date) -> str | None:
    if not isinstance(value, str) or not DATE.match(value):
        return "must be a date written YYYY-MM-DD, in quotes"
    try:
        d = _dt.date.fromisoformat(value)
    except ValueError:
        return "is not a real date"
    if d > today:
        return "is in the future"
    return None


def check_record(h: dict, body: str, path: Path, today: _dt.date) -> list[str]:
    errs: list[str] = []
    for f in COMMON_REQUIRED:
        if f not in h or h[f] in ("", None):
            errs.append(f"missing field '{f}'")
    if errs:
        return errs
    rid, kind = h["id"], h["kind"]
    if not ID.match(str(rid)):
        errs.append("id must be lowercase words joined by '-'")
    if not str(rid).startswith(f"{kind}-"):
        errs.append(f"id must start with '{kind}-'")
    if path.stem != rid:
        errs.append(f"file name must be '{rid}.md'")
    if kind not in KINDS:
        errs.append(f"kind must be one of {sorted(KINDS)}")
    if h["status"] not in STATUSES:
        errs.append(f"status must be one of {sorted(STATUSES)}")
    if (e := _date_ok(h["checked"], today)):
        errs.append(f"checked {e}")
    if not body.strip():
        errs.append("needs a plain-words body under the header")
    for m in h.get("moves", []):
        if m not in MOVES:
            errs.append(f"unknown move '{m}' (use {sorted(MOVES)})")
    if kind in LEVEL_BY_KIND:
        if h.get("level") not in LEVEL_BY_KIND[kind]:
            errs.append(f"{kind} level must be one of {sorted(LEVEL_BY_KIND[kind])}")
        if not h.get("moves"):
            errs.append("missing field 'moves'")
        if not h.get("hats"):
            errs.append("missing field 'hats'")
    if kind == "tool":
        errs += check_tool(h, today)
    return errs


def check_tool(h: dict, today: _dt.date) -> list[str]:
    errs = [f"missing field '{f}'" for f in TOOL_REQUIRED if f not in h]
    if errs:
        return errs
    if not str(h["url"]).startswith("https://"):
        errs.append("url must start with https://")
    if not isinstance(h["licence"], str) or not SPDX_EXPR.match(h["licence"]):
        errs.append("licence must be an SPDX id or expression (or LicenseRef-...)")
    if h["openness"] not in OPENNESS:
        errs.append(f"openness must be one of {sorted(OPENNESS)}")
    for f in ("osi", "open_core", "vetted", "archived"):
        if not isinstance(h[f], bool):
            errs.append(f"{f} must be true or false")
    if h["openness"] in ("1", "2") and h["osi"] is not True:
        errs.append("openness 1 or 2 needs an OSI-approved licence (osi = true)")
    if h["openness"] == "source-available" and h["status"] != "excluded":
        errs.append("a source-available tool must have status 'excluded'")
    if h["vetted"]:
        if h.get("level") != 3 or not h.get("vetting_report") or not h.get("pinned_version"):
            errs.append("a vetted tool needs level = 3, vetting_report and pinned_version")
    else:
        if "level" in h:
            errs.append("an unvetted tool must not claim a ladder level (level 3 means vetted)")
        if h["status"] == "vetted":
            errs.append("status 'vetted' needs vetted = true")
    if h["archived"] and h["status"] not in ("stale", "excluded"):
        errs.append("an archived project must be 'stale' or 'excluded'")
    if (e := _date_ok(h["last_release_date"], today)):
        errs.append(f"last_release_date {e}")
    for r in h["runs"]:
        if r not in RUNS:
            errs.append(f"unknown runs value '{r}' (use {sorted(RUNS)})")
    return errs


def check_folder(root: Path, today: _dt.date | None = None) -> list[str]:
    """Check every record under root. Returns a list of 'path: problem' lines."""
    today = today or _dt.date.today()
    problems: list[str] = []
    seen: dict[str, Path] = {}
    links: list[tuple[Path, str]] = []
    files = sorted(root.rglob("*.md"))
    if not files:
        return [f"{root}: no records found"]
    for path in files:
        try:
            h, body = parse(path)
        except ValueError as e:
            problems.append(f"{path}: {e}")
            continue
        for e in check_record(h, body, path, today):
            problems.append(f"{path}: {e}")
        rid = h.get("id")
        if rid in seen:
            problems.append(f"{path}: duplicate id '{rid}' (also in {seen[rid]})")
        elif rid:
            seen[rid] = path
        for target in h.get("related", []):
            links.append((path, target))
    for path, target in links:
        if target not in seen:
            problems.append(f"{path}: related id '{target}' does not exist")
    return problems


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).parent / "records"
    problems = check_folder(root)
    for p in problems:
        print(p)
    n = len(list(root.rglob("*.md")))
    print(f"{n} records checked, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
