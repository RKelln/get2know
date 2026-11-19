#!/usr/bin/env python3
"""Install a taught skill from profile/skills/<name>/ so a new chat can find it.

    python3 .agents/skills/teach-a-job/scripts/install_skill.py <name>
    python3 .agents/skills/teach-a-job/scripts/install_skill.py --all
    ... --target <folder>   install only into that skills folder (another AI tool's)
    ... --agents-only       install only into .agents/skills (the old behaviour)
    ... --link              make a link, not a copy
    ... --dry-run           say what would happen, change nothing

By default a skill goes into .agents/skills (OpenCode, Codex and others) and
.claude/skills (Claude Code). If .claude/skills is a link to .agents/skills, as
this kit ships it, that is one folder and it is installed once.

Run it only after the person says yes. profile/skills/ stays the master copy.
Standard library only. It never touches the network, or the skills this kit ships.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MANIFEST = "MANIFEST.sha256"


class Stop(Exception):
    """A plain message for the person. Nothing was changed."""


def kit_folder():
    """The folder holding AGENTS.md: scripts/ -> teach-a-job/ -> skills/ -> .agents/ -> here."""
    return Path(__file__).resolve().parents[4]


def shipped_names(kit):
    """Names of the skills this kit ships, from its manifest and from what is known."""
    names = {"get2know", "did-you-know", "builder-brief", "share-safely", "teach-a-job"}
    manifest = kit / MANIFEST
    if manifest.is_file():
        for match in re.finditer(r"\.agents/skills/([^/\s]+)/", manifest.read_text(encoding="utf-8")):
            names.add(match.group(1))
    return names


def read_frontmatter(path):
    """Return the frontmatter as a dict of top-level fields, or stop with a plain reason."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise Stop(f"{path} must start with a line of three dashes, then name and description.")
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        raise Stop(f"{path} has no closing line of three dashes after name and description.") from None
    fields = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    if not any(line.strip() for line in lines[end + 1:]):
        raise Stop(f"{path} has no steps after the name and description.")
    return fields


def check_skill(source, name):
    """Stop with a plain reason if this skill would not load, or is not safe to copy."""
    skill_md = source / "SKILL.md"
    if not skill_md.is_file():
        raise Stop(f"There is no {skill_md}.")
    fields = read_frontmatter(skill_md)
    if fields.get("name") != name:
        raise Stop(f"The name in {skill_md} must be '{name}', the same as its folder.")
    description = fields.get("description", "")
    if not description:
        raise Stop(f"{skill_md} has no description. A new chat would never find it.")
    if len(description) > MAX_DESCRIPTION:
        raise Stop(f"The description in {skill_md} is over {MAX_DESCRIPTION} characters. Shorten it.")
    quoted = len(description) > 1 and description[0] == description[-1] and description[0] in "\"'"
    if ": " in description and not quoted:
        raise Stop(f"The description in {skill_md} has a colon and a space, so some tools cannot load it. Use a dash.")
    for root, dirs, files in os.walk(source, followlinks=False):
        for entry in dirs + files:
            if (Path(root) / entry).is_symlink():
                raise Stop(f"{Path(root) / entry} is a link. A skill folder must hold only plain files.")


def remove(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def install_one(kit, target, name, link, dry_run):
    """Check and install one skill. Returns a line saying what happened."""
    if not NAME.match(name) or len(name) > MAX_NAME:
        raise Stop(f"'{name}' is not a usable name. Use lower case and dashes, like late-reminders.")
    if name in shipped_names(kit):
        raise Stop(f"'{name}' is one of this kit's own skills. Pick another name.")
    source = kit / "profile" / "skills" / name
    if not source.is_dir():
        raise Stop(f"There is no folder {source}.")
    check_skill(source, name)
    dest = target / name
    how = "link" if link else "copy"
    if dry_run:
        return f"Would {how} {source} to {dest}. Nothing was changed."
    target.mkdir(parents=True, exist_ok=True)
    if os.path.realpath(dest) == os.path.realpath(source):
        return f"{name} is already linked at {dest}."
    remove(dest)
    if link:
        try:
            os.symlink(os.path.relpath(source, target), dest, target_is_directory=True)
        except OSError as err:
            raise Stop(f"This computer would not make a link ({err}). Leave off --link to copy instead.") from None
    else:
        shutil.copytree(source, dest)
    return f"Installed {name} at {dest} ({how}). A new chat can find it now."


def main(argv=None):
    parser = argparse.ArgumentParser(description="Install a taught skill, after the person says yes.")
    parser.add_argument("name", nargs="?", help="the skill's folder name in profile/skills/")
    parser.add_argument("--all", action="store_true", help="install every skill in profile/skills/")
    parser.add_argument("--target", help="install only into this skills folder (default: .agents/skills and .claude/skills in this folder)")
    parser.add_argument("--agents-only", action="store_true", help="install only into .agents/skills, not .claude/skills")
    parser.add_argument("--link", action="store_true", help="make a link, not a copy")
    parser.add_argument("--dry-run", action="store_true", help="say what would happen, change nothing")
    parser.add_argument("--kit", help=argparse.SUPPRESS)  # tests only
    args = parser.parse_args(argv)

    kit = Path(args.kit).resolve() if args.kit else kit_folder()
    if args.target:
        targets = [Path(args.target).expanduser().resolve()]
    else:
        targets = [kit / ".agents" / "skills"]
        if not args.agents_only:
            targets.append(kit / ".claude" / "skills")
        seen, unique = set(), []
        for t in targets:  # .claude/skills may be a link to .agents/skills: one folder, install once
            real = os.path.realpath(t)
            if real not in seen:
                seen.add(real)
                unique.append(t)
        targets = unique
    try:
        if args.all == bool(args.name):
            raise Stop("Give one skill's name, or --all.")
        if args.all:
            folder = kit / "profile" / "skills"
            names = sorted(p.name for p in folder.iterdir() if p.is_dir()) if folder.is_dir() else []
            if not names:
                raise Stop(f"There are no skills in {folder}.")
        else:
            names = [args.name]
        # Check everything before changing anything.
        for target in targets:
            for name in names:
                install_one(kit, target, name, args.link, dry_run=True)
        for target in targets:
            for name in names:
                print(install_one(kit, target, name, args.link, args.dry_run))
    except Stop as stop:
        print(f"Not installed: {stop}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
