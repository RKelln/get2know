# Updating Get2Know

Your `profile/` folder is yours. Updating never changes it, or a `share/` folder, or any file of your own.

- Which version do you have? Open the file `VERSION` in your Get2Know folder.
- What is new? Open `CHANGELOG.md` in the new download.

There are two ways. Pick one.

## The easy way (no typing)

Use this if you have never changed Get2Know's own files (most people).

1. Download the new Get2Know zip file (from the project's Releases page on GitHub). Double-click it. You get a new folder called `get2know`.
2. Open your old Get2Know folder, the one with your `profile` folder in it.
3. Drag your `profile` folder into the new `get2know` folder. Do the same with a `share` folder, a `drafts` folder, and any files of your own you added, if you have them.
4. From now on, open the new folder in your AI tool, instead of the old one.
5. Check that your `profile` folder is there and has your files. Then you can delete the old folder.
6. If you taught it any jobs, they need installing again. Open the new folder in your AI tool and say "install my skills again". Your skills are safe in `profile/skills/`.

If you did change Get2Know's own files (for example, you changed a number in `SETTINGS.md`, or added your own cards to `cards.md`), the easy way loses those changes. Use the careful way.

## The careful way (keeps your changes)

This keeps your old folder where it is and updates it in place. It keeps any Get2Know file you changed. It needs the Terminal app once.

1. Download the new Get2Know zip file and double-click it, as above.
2. Open **Terminal** (on a Mac: in Applications, then Utilities).
3. Type `python3` and a space. Do not press Return yet.
4. Drag the file `update.py` from the new `get2know` folder into the Terminal window. Type a space.
5. Drag your old Get2Know folder into the Terminal window. Press Return.
6. It shows a list of what it will change, and asks. Type `y` and press Return.
7. Keep using your old folder as before. You can delete the new download.

The first time on a Mac, typing `python3` may ask to install "command line developer tools". Choose Install and wait a few minutes, then start again from step 3. On Windows, type `py` instead of `python3`.

What it does:
- Replaces Get2Know's own files that you have not changed.
- Keeps every Get2Know file you changed, just as you left it. The new version's copy goes in a folder called `updates-to-review`, so you can compare and copy over anything you want.
- Adds new files. Removes old Get2Know files that are no longer used, unless you changed them.
- Never touches `profile/`, `share/`, or files of your own.

## If an AI helper does it for you

You can ask your AI tool, in your Get2Know folder: "Update Get2Know from the new folder at <where you unzipped it>. Follow UPDATE.md." It should first run `update.py` with `--dry-run` and show you the list. Then, only if you say yes, run it again with `--yes`.

## Want to see which Get2Know files you changed?

In Terminal, in your Get2Know folder: `shasum -a 256 -c MANIFEST.sha256`. Lines that say `FAILED` are files that differ from the version you installed.
