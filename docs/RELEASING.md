# Releasing a version

The chat prompts in `dist/` (`get2know-prompt.md` and `dist/chat/`) and `skill/MANIFEST.sha256` are committed, so each has a stable link and its changes show in a diff. The zip is not committed (`dist/*.zip` is in `.gitignore`). It is built here and uploaded to a GitHub Release.

1. **Bump the version.** Change `skill/VERSION` (for example `0.2.0`). Add a section at the top of `skill/CHANGELOG.md`, in plain words, with the date.
2. **Build.** `python3 tools/build_all.py`. This writes the manifest, the chat prompts and `dist/get2know-<version>.zip`. If the repo is public, set `BASE_URL` in `tools/export_prompt.py` (for example `https://raw.githubusercontent.com/OWNER/REPO`) so part 1 of the staged chat prompts links to the other parts, pinned to this version's tag. Setting it there, not only with `--base-url`, keeps `--check` and the tests in step with the committed files.
3. **Test.** Run the unit tests (the command is in `HANDOFF.md`) and `python3 tools/build_all.py --check`.
4. **Commit and tag.** Commit the version, changelog, manifest and prompts. Then tag that commit: `git tag v0.2.0` and `git push origin v0.2.0`. The staged prompts link to files under this tag, so tag the commit that holds them.
5. **Notes.** Copy the new CHANGELOG section into a file, for example `/tmp/notes-0.2.0.md`.
6. **Publish.** `gh release create v0.2.0 dist/get2know-0.2.0.zip --title "Get2Know 0.2.0" --notes-file /tmp/notes-0.2.0.md`
7. **Check.** Download the zip from the Release page, unzip it, and check that `.claude/skills` is still a link and that `update.py --dry-run` works on an older folder.

Never move a tag after you publish it: owners' links and the staged prompts point to it.
