# Handing off: what the owner does next

Say this in your own short, plain sentences. Under 8 lines. Skip what does not fit.

1. **Check the brief.** It is in `profile/briefs/<slug>.md`, plain text. Fix anything wrong. "What it must never do" and the tests matter most.
2. **Start a new folder for the build.** Copy the whole `profile/` folder into a new, empty folder for this project, and start the AI there. (Started in this folder, it would start the interview again.)
3. **First, plan; then build.** Tell the AI there, in these words or close:
   > Read `profile/README.md`, `profile/limits.md` and `profile/briefs/<slug>.md`. Before building anything, help me settle the "Questions to settle", one question at a time, in plain words. Then build the simplest version on made-up data, and show me each acceptance test passing.
   If their AI has a planning skill (for example one called "grill-me" or "to-spec"), it can use it, but the owner should still get one plain question at a time.
4. **A helper can build it too.** If a friend, volunteer or local tech person will build it, give them the `profile/` folder or just the brief and `limits.md`. Check there are no private details in them first. If the `share-safely` skill is next to this one (`.agents/skills/share-safely/`), offer it: it makes a copy with private details taken out.
5. **Not checked yet?** If the suggested tool has not been checked for safety and the owner agreed to help check it, tell the AI there to check it before installing anything. No checking step yet? Then build the small version first.
6. **You decide when it is done.** It is done when every acceptance test passes in front of you. Try it on a copy of real work before the real thing.
7. **Write back.** When you try it, change the idea's status in `ideas.md` (trying, kept, dropped), with the date, as `Status: trying, 2026-11-12`. Change the brief's status too. If it fails, say why there; that helps the next try.

If nothing open did this job, say in one line: this is a gap other small organizations may share, and later they may be able to share it (anonymously, only if they want) so open-source builders can work on it.
