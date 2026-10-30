# What changed

Newest first. Your version number is in the file `VERSION`. To update, see `UPDATE.md`.

## Not released yet

- **Asks for your records early.** When talk turns to money, customers or prices, it asks early if you keep anything that shows how it works now (invoices, a spreadsheet, a price list), naming a file it can see in the folder. It reads only after you say yes, and if you say no, it carries on by asking.

## 0.2.1 (2026-10-30)

- **Short on time, still one idea.** If you confirm the summary and have to go right away, it still saves one idea and tells it to you in one sentence as you leave.

## 0.2.0 (2026-10-30)

- **Quieter while it writes.** It no longer says "I saved that in..." after every answer. It still says so when it makes a new file or changes something you said earlier, and it reads everything back to you after about 8 answers. To hear a line after every answer again, set **Say what was written after each answer: yes** in `SETTINGS.md`. It also stops thanking you after every answer.
- **More natural questions.** It asks about real events in more than one way (not always "the last time..."), asks about the example you gave instead of asking for another, and avoids stacked questions like "the one before that, the last time...".
- **Your words, spelled right.** Quotes in your profile keep your words, but now fix spelling and typos ("i dont no" becomes "I don't know"). It never changes your wording or the way you talk, and it leaves names as you typed them. If one word seems to say the opposite of what you meant ("can" for "can't", "left" for "right"), it asks once which you meant.
- **Asks how you do it now.** When you mention how you handle a task you want help with, it asks about that before moving on: what you use, how long it takes, how often. Each idea now says how you do the task today and builds on it, instead of suggesting something you already have. If you find it hard to describe, it may offer two or three choices and "or something else"; it never offers choices for what you want or for your limits.
- **Ideas that take work off you, safely.** Ideas first ask why the work comes in, and try to stop it at the source (tell customers before they ask, put the answer where they look) before speeding it up. They no longer assume you will read every message first. They start from a reliable source (an up-to-date price sheet, a list of which jobs are done) and, only as far as you say is okay, can answer simple questions on their own, marked as automatic, with everything else coming to you. Each such idea lists its guardrails: what it may answer, what it may never promise, how it is labelled, what it logs, and how to switch it off. It asks you before suggesting anything that would go out on its own.

## 0.1.0 (2026-10-29)

The first numbered version. What it has:

- **The interviewer (`get2know`).** Asks one short, plain question at a time about how your business or non-profit really works. It can start from nothing, from notes or a draft you already have, or pick up where you stopped last time.
- **Your `profile/` folder.** Six plain-text files you can open and fix in any text editor: how you work, your limits (what must stay human, rules you follow), ideas, interview notes, and a log of what changed. Every line says where it came from.
- **Ideas.** Before any ideas, it reads back what it heard so you can fix it. Then 3 to 5 ideas for where AI could help, each tied to something you said, and at least one thing AI should not do.
- **"Did you know I can...?" cards (`did-you-know`).** Short examples of what an AI helper can do, offered only when one fits something you said.
- **More ways to use the interviewer.** A helper (a volunteer, librarian or consultant) can sit with you. It can talk in your language. Months later it can ask "what changed?", and two weeks after ideas, "did you try it?". Staff or volunteers can be asked too; each line says whose account it is.
- **A brief for building (`builder-brief`).** Turns one idea you picked into a plain brief an AI coding tool can build from, with open-source options first and tests you approve in your own words.
- **Share safely (`share-safely`).** Makes a copy of your profile with names and private details taken out, in a `share/` folder, and shows you every change before anything leaves. It never sends anything.
- **Settings you can change (`SETTINGS.md`).** How many days it waits before it asks "did you try it?" or "what has changed?". Open it in any text editor. Updating keeps your changes.
- **Notes for whoever runs a session** (`FACILITATOR.md`).
- **A chat version.** One prompt to paste into any chat app (ChatGPT, Claude, Gemini and others). It gives you your profile files as text to save.
- **A chat version in three parts (experimental).** For chat apps that limit how much you can paste, or small AI models: paste part 1 to start; it asks for part 2 (ideas) or part 3 (coming back, helpers, other languages) only when it needs them. New and not yet tried with any AI model.
- **Updating.** Download the zip from the project's Releases page. This file, `VERSION`, `UPDATE.md`, `MANIFEST.sha256` and `update.py`. Updating never touches your `profile/` folder and keeps any changes you made to Get2Know's own files.

Not yet tried with a real owner: so far tested only with simulated interviews.
