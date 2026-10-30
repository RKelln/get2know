# Handoff (updated 2026-10-29)

For the next working session. Read `docs/DESIGN.md` first; this file is only what is in flight.

## Where things stand

- `skill/` (version 0.1.0): four skills. `get2know` (first interview, follow-up, resume, re-check, outcome check, helper mode, other languages, more than one voice; D28–D31), `did-you-know` cards, `builder-brief` (D33) and `share-safely` (D34). `AGENTS.md`, `FACILITATOR.md` (with helper and train-the-helper notes), `SETTINGS.md` (owner-editable waits, D41), `VERSION`, `CHANGELOG.md`, `UPDATE.md`. `get2know/references/modes.md` is split into `returning.md` and `people.md` (D43).
- `tools/build_all.py` builds `dist/get2know-prompt.md` (one prompt for any chat app), the experimental three-part `dist/chat/` (D44), and the zip (a Release asset, not committed; `docs/RELEASING.md`, D43); `update.py` never touches `profile/` and keeps owner changes (D35). Run `python3 tools/build_all.py` after any skill change; tests fail if `dist/` is stale.
- `commons/`: 43 seed records (30 tools checked at source, none vetted), `check.py`. `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `docs/GOVERNANCE.md`: proposals (D37).
- `tests/`: unit tests (`python3 -m unittest tests/export/test_export_prompt.py tests/export/test_staged_parts.py tests/update/test_update.py tests/share_safely/test_check_share.py tests/commons/test_check.py tests/settings/test_settings.py`, 89 pass). `tests/rehearse/`: bike shop (six sims) plus a messy-draft bike-shop case (D42), a made-up non-profit with first-interview, cold-resume and injection cases; reading-level check (D36).
- A fresh review of the parallel builds found 11 cross-skill problems, all fixed (D38).

## Live runs (all codex since Ryan's steer, all assessed)

- Card fix (7fd1003), both bike-shop sims: D32. Fixes made to open questions, card step, keep-going once.
- Non-profit first interview and cold resume (295cce8): both pass, judge 11/11. Injection: not followed, owner told, but the session drifted into tasks and saved nothing: fixed in D39; rerun (359e816) better but still read `profile/` late: fixed in D40.
- Four harder bike-shop sims (359e816): guarded, hostile, hurried, low literacy: D40. New fast path for owners short on time.
- Fixture (D42, D54): the bike shop now lives in `tests/rehearse/fixture/` (CC BY 4.0) and is the master copy; the workshop's participant folder is copied from `fixture/shop/`. Clean draft (no "Made up." label or GAP instructions) and `shop-messy/`.
- **Never run with a model:** builder-brief (incl. the unvetted-tool question, D41), share-safely, the chat prompt and staged parts (and link fetching), helper/language/re-check/outcome/voices modes, `SETTINGS.md`, the messy draft, `update.py` on a Mac.

## Ryan's steer

- The workshop is the first deployment, not the main use case. Design for owners on their own business.
- Live tests on codex, not Claude. Use subagents for implementing and reviewing. Ryan tests the workshop Mac himself.
- Rehearse is new and can be changed to fit this case.

## Next

1. D51-D52 held over 7 codex runs (D53, D55): 1 assumed habit in 7. Open: log entries over the cap of 8 lines in 3 of 7; `three_problems_with_quotes` word lists too narrow (D55). Then the untested skills (item 2).
2. Rehearse cases for the untested skills: builder-brief (from a finished profile with a picked idea), share-safely (does anything private leak; run `check_share.py`), the chat prompt (a chat seat with no tools), re-check/outcome (an aged profile), helper and another-language sims, a staged-prompt chat case (part 1 only, then with part 2 pasted), a builder brief whose best option is an unvetted tool (owner says yes, and no).
3. A short human rating of a few transcripts, to compare with the judge.
4. After the workshop: what real owners did.
5. After the MVP, to consider (D56): a profile-only judge in rehearse; goldfish lenses between interview sessions that turn `profile/` into follow-up questions (D57: offline, goldfish questions reached missing items the interviewer's own plan did not; next, a live resume run with and without them); builder frameworks behind builder-brief (EGM is one example; compare others first); a plugin install once public.

## Open questions for Ryan

- Commons: who approves level 3? How many independent vetting reports make a tool `vetted`, and how to resist fake vetters (D41 open problem)? Code-of-conduct contact: likely the Human Feedback Foundation once they agree (placeholder stays in `CODE_OF_CONDUCT.md`).
- HFF's Agentic AI Design Exchange (cohorts from fall 2026; CC library "Agentic Commons" early 2027) overlaps the commons: see `docs/capability-commons.md` "Related". Ask HFF about its licence and whether outside projects can contribute.
- Fixture: check that none of the five stale values in the messy draft (listed in `rubric-messy.md` Q12) clashes with the answer key (no agent may read it).
- Re-check and outcome thresholds (30 days, 14 days) are guesses; now owner-editable in `skill/SETTINGS.md` (D41).

## For the workshop team: section to add to FACILITATOR.md in the bundle

> **Workshop: the bike shop.** Participants play **Sam**, owner of the made-up shop Spoke & Chain, using the shop files in the folder. When it asks about notes, they say yes and name `sam-profile-draft.md`. Where the files do not say, they decide what Sam would say. Real business details are not allowed on library machines. Before logging off, run the take-home script to copy `profile/`.

## Not yet read

Bano et al. 2019; W04 interviewer prompt and harness; Mom Test, JTBD, contextual inquiry, Anthropic's AI interviewer work.
