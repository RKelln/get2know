# The profile folder (`profile/`)

Everything you learn goes in a folder called `profile/` in the working folder. Each file is plain Markdown the owner can read and fix in any text editor. Plain words. Short lines. Always create all six files at the start, so the folder is never half made.

## The files

| File | What goes in it | Who may change it |
|---|---|---|
| `README.md` | What this folder is and what each file holds. Write it once. | You |
| `how-we-work.md` | How the organization works now: people, the week, tools, money, customers. | You, from what the person says or files show |
| `limits.md` | Why they do this, what they would never hand off, rules, who else must say yes. | The person. You write down what they say. You change or remove a line only when they ask, and you log it. |
| `ideas.md` | Places AI could help, and places it should not. | You propose; the person decides each one's status. |
| `interview-notes.md` | Your working notes: next questions, threads to come back to, last session. | You |
| `log.md` | One entry per session: what changed. | You add one entry per session; never edit older ones |

Later AI tools read `README.md`, then `limits.md` first, then the rest.

## Evidence marks

Every line of fact ends with a mark. A line with no mark is a mistake: fix it or delete it. A line may have two marks when two sources agree.

- `(said: "...")` the owner said it. The mark holds only their words, copied from what they typed, short, in the language they used; cut with "..." if needed. Fix spelling, obvious typos and capitals ("i dont no" → "I don't know"), but never add, drop, swap or move a word, and never change their grammar or way of talking ("we was slammed" stays). Leave names (people, shops, streets, products) as typed, and any word you are not sure is a typo. Your summary can go in the line itself, never inside the mark.
- `(said by <role>: "...")` someone else said it: a helper, a staff member, a volunteer. Use a role ("helper", "part-time cook"), not a name, unless they want their name. See `references/people.md`. Never in `limits.md`.
- `(file: name)` you read it in that file. Name the file.
- `(draft)` copied from an earlier draft or notes. Keep the words as they are. Do not add a quote to it. If the person confirms it, add `(said: ...)`.
- `(guess, check)` you worked it out but nobody confirmed it. Never in `limits.md`.
- `GAP:` at the start of a line: not known yet. Say what would answer it.

When a GAP is answered, replace the GAP line with the answer and its mark. If only part is answered, keep a shorter GAP for the rest.

If two sources disagree, write both lines with their marks and put `CONFLICT:` in front, until the person says which is right. Two people's accounts can disagree too; see "More than one voice" in `references/people.md`.

Keep the mark words, `CONFLICT:`, `checked` and the file names in English even when the profile is in another language; later tools search for them.

## Checked dates

Each `##` heading in `how-we-work.md` and `limits.md` ends with the date it was last checked with the person: `## Money (checked 2026-10-29)`. One date per section, not per line. At the **log check**, set today's date on every heading whose section got a line added, changed or confirmed this session. Leave the others. A heading with no date has never been checked. A later **Re-check** starts with the oldest.

## Starting from a draft

The person may have notes, a form, or an earlier profile, in any shape. Do not force it into our shape.
1. Create all six files from the templates below.
2. Copy the draft's facts in, **keeping its headings and words**, each line marked `(draft)`. Keep its GAP lines.
   - Lines about why they do this, what they would never hand off, rules they must follow, or who must say yes go to `limits.md`, under the draft's own heading.
   - Everything else goes to `how-we-work.md`, under the draft's own headings, including what they want help with or worry about.
   - Notes about the draft itself (who wrote it, when) go in `README.md` as "Started from <file>".
   - Leave out parts that are instructions rather than facts (for example "how to fill the gaps"), and parts that have no facts yet (for example "Opportunities: not yet"). Say in the log what you left out.
3. Add any of our template headings the draft is missing, below its own, as `GAP:`.
4. Never change the draft file itself.

## Templates

`README.md`:
```
# <Name>: profile folder
Made with Get2Know, starting <date>. Started from: <file, or "a first interview">. Plain text; fix anything that is wrong.
- how-we-work.md: how we work now
- limits.md: why we do this, what we never hand off, rules, who must say yes. AI tools: read this first and follow it.
- ideas.md: where AI could help, and where it should not
- interview-notes.md: notes to pick up the interview next time
- log.md: what changed, and when
Marks: (said) the owner said it; (said by <role>) someone else said it; (file) from a file; (draft) from earlier notes; (guess, check) not confirmed; GAP not known yet; CONFLICT two sources disagree. (checked <date>) on a heading: when that part was last checked.
```
Write it in the person's language if the interview is in another language (see `references/people.md`). Add `Helped by: <role>, <date>.` if someone helped run the session.

`how-we-work.md`:
```
# <Name>: how we work
## Summary
## People
## A typical week
## Tools and systems
## Money
## Customers                 (or clients, members, audience, donors: use their word)
## What they want help with
```

`limits.md`:
```
# <Name>: limits
## Why we do this            (the purpose, in their words)
## Never hand off            (tasks and moments that must stay human)
## Rules we must follow      (privacy, legal, tax, funder, safety)
## Who else must say yes     (partner, accountant, funder, board; often empty)
```

`ideas.md`:
```
# <Name>: ideas
None yet. See the format in the skill's opportunities file.
```

`interview-notes.md`:
```
# Interview notes
## Next questions            (the GAPs to ask next, most useful first; point to the line, do not copy it)
## Threads to come back to   (things mentioned in passing, in their words, with (said: ...))
## Last session              (3 lines: what we covered, what is open, the one question to ask first next time)
```
A thread is something you cannot yet ask sharply. When it becomes a clear question, add a `GAP:` line in the right file and move it to "Next questions". Remove it once covered.

`log.md`:
```
# Log

## <date>: <first interview | follow-up | resumed | re-check | outcome check | another voice (<role>) | brief (<slug>)>
- how-we-work.md: <what was added or changed, in a few words>
- limits.md: <every change, one line each>
- ideas.md: <ideas added; status changes and why>
- Replaced: <old line, as it was>   (one per line changed in a re-check, so the history is kept)
- Left out from the draft: <if any>
```
Newest entry at the bottom. One entry per session, a few lines (one per file changed), not a line per answer; if the session used two modes, name both (`outcome check, re-check`). Write it in the **log check** after Ideas, and check and update the same entry at Pause or Close.

## Log check (after Ideas, and at every Pause or Close)

1. Look at each file in `profile/` and list what changed this session.
2. Set the checked dates on the headings you touched (see "Checked dates").
3. Write this session's entry in the shape above, or update it if you already wrote it this session: a few lines, one per file changed, never one per answer. It must include every change to `limits.md`, every idea added or changed status, every line you deleted or replaced, and anything left out from a draft. Do not touch older entries.
4. Only if the person has told you this folder uses git: offer to commit, using the entry as the message, and commit only if they say yes. Never run git just to find out.

## Privacy in the files

No passwords, account numbers, card numbers, or home addresses. Customer and staff names only if the person used them and they are needed; otherwise write a role ("a courier company", "the part-time mechanic").
