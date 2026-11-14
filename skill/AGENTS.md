# This folder

This folder holds **Get2Know**. It helps someone write down how their business, non-profit or work really runs, find a few places AI could help, and teach an AI assistant the jobs they do again and again.

**Before doing any job here, read `profile/limits.md` and `profile/assistant-brief.md` if they are there, and follow them.**

When the person says hello, asks what to do, or says anything like "start", "get to know", "interview", or "profile": use the `get2know` skill. If your tool does not load skills by itself, read `.agents/skills/get2know/SKILL.md` and follow it. The same skill handles: a helper (volunteer, librarian, consultant) running the session with the owner; another language; "things have changed" or "I tried it" when `profile/` already exists. Its `references/people.md` and `references/returning.md` say how.

If they ask what AI can do for them, use the `did-you-know` skill (`.agents/skills/did-you-know/SKILL.md`).

If they name a job for you to do, do it with the skill for that job. If they want to show you a job or teach you one, say "I'm going to show you how I do this", or want to change a skill they taught you, use the `teach-a-job` skill (`.agents/skills/teach-a-job/SKILL.md`), if its folder is there. Their own skills are in `profile/skills/`. If a skill there is not installed, read its `SKILL.md` and follow it. A named job does not start the interview, even when `profile/` exists.

If they want an AI to build something from one of their ideas, use the `builder-brief` skill (`.agents/skills/builder-brief/SKILL.md`). If they want to give their profile to someone else, use the `share-safely` skill (`.agents/skills/share-safely/SKILL.md`). Use either only if its folder is there.

Speak in short, plain sentences. Ask one question at a time. Ask before reading any of the person's files.

Write only inside the `profile/` folder, inside `drafts/` when doing a job (drafts are for the person to read and send; never send anything yourself), and inside `share/` when making a safe copy to share. Do not change any other file, unless the person asks you to copy `profile/` to a place they name, to add a card to the `did-you-know` cards, to change a number in `SETTINGS.md`, to install a skill they taught you (only with the `teach-a-job` install script, after they say yes to that skill), or to update Get2Know (then follow `UPDATE.md`: show the dry run first, and update only after they say yes).
