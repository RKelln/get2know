# Returning owners: resume, re-check, outcome check

Every rule in `SKILL.md` still holds here: one question per message, short and plain, ask about real past events, never invent, show conflicts, write only in `profile/`. Evidence marks and checked dates are in `references/profile-folder.md`.

## Telling Resume, Re-check and Outcome check apart

When `profile/` exists, read `profile/log.md` and `profile/interview-notes.md` first. Then:
1. **Their words win.** "Carry on", "where were we?" → **Resume**. "Things have changed", "update it", "it's been a while" → **Re-check**. "I tried it" → **Outcome check**.
2. **Otherwise, the dates.** Read `SETTINGS.md` at the top of this folder (next to `profile/`; no need to ask) for two numbers of days: **Outcome check after** and **Re-check after**. If the file is missing, or a number is missing or unclear, use 14 days for the first and 30 for the second. Use today's date and the newest entry in `log.md` that is not a `brief` (a `brief` entry is a builder-brief session, not an interview). No such entry yet means the first session was cut short: Resume.
   - An idea in `ideas.md` is `picked` or `trying`, and its status date is **Outcome check after** days ago or more → **Outcome check** first, then go on below.
   - That entry is **Re-check after** days old or more → **Re-check**.
   - Otherwise → **Resume** (in `SKILL.md`).
3. If you still cannot tell, ask one question: "Shall we carry on where we stopped, or catch up on what has changed?"

One session gets one log entry, even if it used two modes. Name both in its title, for example `## 2026-11-12: outcome check, re-check`.

## Outcome check ("did you try it?")

The real test of an idea is whether it helped. Say hello and the date of the last session, then do this before anything else, one idea at a time, most recent first. At most two ideas per session.
1. "Last time you picked <idea, in their words>. Did you try it?"
2. If yes, ask what happened the last time they used it (a real event). If no, ask what got in the way. One follow-up is enough.
3. Ask what they want to do with it now: keep it, keep trying, or drop it. Only they decide.
4. In `ideas.md`, under that idea, set `Status:` to their choice with today's date, and add a `Tried:` line with what happened and their words: `- Tried: used it twice, missed one invoice (said: "...")`. If dropped, the reason goes on the `Status:` line.
5. Log it: `- ideas.md: <idea> trying → kept, because "..."`.
Never argue them out of dropping an idea. "It didn't help" is a useful answer.

## Re-check ("what changed?")

For a profile made weeks or months ago. The aim is a current profile, not a new interview. About 6 to 8 answers.
1. Say hello and the date of the last session (from `log.md`), unless an outcome check already did. Say what you will do: "I'll ask what has changed, then check the oldest parts." Say the privacy note again if months have passed or it may be a different person.
2. Ask one open question: "What has changed since <month>?" Follow their thread, as in any interview.
3. Then check what is oldest. Each heading carries a checked date (see `references/profile-folder.md`). Pick the 3 or 4 sections with the oldest dates, `limits.md` first, then money and people. For each, sum up the section in one plain line and ask: "Is that still true?" Do not read out every line.
4. Update as you go:
   - **Still true:** leave the lines; set that heading's date to today.
   - **Changed:** replace the line, with the new mark. Copy the old line into the log, so the history is kept.
   - **Not sure:** keep the line and add a `GAP:` line under it saying what would settle it.
   - `limits.md`: change a line only when they say so (as always), and log it.
5. Sections you did not check keep their old dates. That is how the next re-check knows where to start.
6. If something new came up, it may need new ideas: follow **Ideas** in `SKILL.md`. Never rewrite `ideas.md`; add or update.
7. A short **Check back**, then **Close**. Log title: `re-check`.
