# Contributing to Get2Know

Thank you for helping. Get2Know helps small businesses and non-profits learn what AI can do for them, preferring open tools they can own. You can help with code, with the interview's words (skill text), or with the **capability commons**: the shared list of what AI can do and which open tools do it.

Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md). How decisions are made is in [docs/GOVERNANCE.md](docs/GOVERNANCE.md).

**Status:** the review roles below are **proposed** until Ryan decides them. Where a line says *(proposed)*, it is not yet a rule.

## What licence your work goes under

By sending a contribution you agree it is published under the licence for its kind. You keep your copyright except for commons records, which you give to the public domain.

| You send | Licence | Where |
|---|---|---|
| Code (Python, scripts, tests) | MIT | anywhere, including scripts inside `skill/` (`skill/**/*.py`) |
| Skill text, prompts, docs | CC BY 4.0 | `skill/` (except its scripts), `docs/`, Markdown files at the top |
| Commons records | CC0 1.0 (public domain) | `commons/records/` |

Write in your own words. Do not paste text you do not have the right to give, and never paste a tool's README into a commons record: besides the copyright problem, text from outside can carry instructions aimed at an AI.

## How to send a change

1. Open an issue first for anything bigger than a fix, so we can agree on the idea.
2. Make a branch, make the change, and open a pull request. Say what changed and why in plain words.
3. Run the checks that apply:
   - commons records: `python3 commons/check.py` and `python3 -m unittest discover -s tests/commons`
   - skill text: a dry run with the `rehearse` tool (see `tests/rehearse/README.md`). Live runs cost money; ask first.
4. Say what you did not test.

## Writing rules (short)

- Plain words, about grade 6 reading level. Explain any business or AI word the first time.
- One question at a time in anything the interviewer says.
- Plain text only (Markdown, CSV). A person must be able to read and fix every file in a text editor.
- No names of real people or organizations in examples. Never copy the test fixture's answer key anywhere an interviewer or simulated owner can read it.
- Decisions about the design go in `docs/DESIGN.md` with the reason.

## Commons records

Read `commons/README.md` for the format. One file per record.

### The review path by level

The commons has a ladder (see `docs/capability-commons.md`). The higher the level, the more third-party material it carries, and the more review it needs.

| Record | Who can write it | Review before it is shown to owners |
|---|---|---|
| **Level 0, possible** (capability) | anyone, or a maintenance agent | one reviewer skims it (the daily digest is enough) |
| **Level 1, shown** (capability with a sandbox example) | anyone, or the prover agent | one reviewer checks the example and its log |
| **Level 2, recipe** | anyone | one reviewer reads the steps and the checks a person must do |
| **Tool, listed, not vetted** | anyone, or the triage agent | one reviewer checks the licence and release facts at the source; shown with a warning, for use only by owners who help check it |
| **Level 3, vetted tool** | only after the vetter's automated checks pass | **a level-3 approver** approves the first listing of each tool *(proposed)* |
| **Story** | only from a session, with the owner's consent, anonymized | one reviewer checks nothing identifies the organization |
| **Gap** | anyone | one reviewer skims it |

Fact refreshes (a new release date, an archived flag) can merge on their own when `check.py` passes *(proposed)*. A changed licence never merges on its own: a person looks.

### Who can approve level-3 listings *(proposed)*

- **Level-3 approvers** are a short list kept in `docs/GOVERNANCE.md`. To start: Ryan, plus anyone he names.
- To join: at least three months of good reviews in the commons, a nomination by an approver, and no objection from the steering group within two weeks.
- An approver never approves a tool they make, are paid by, or have a stake in. They say so and pass it on.
- The first listing of each tool needs one approver. Removing a listing for safety needs only one approver and can happen at once; the reason is written in the record.
- Later version bumps that pass the same automated checks may merge without an approver.

## Gaps: turning needs into work

A **gap** is a need with no good open answer yet ("a booking page that texts customers, fully open, cheap to host"). Gaps are the commons' to-do list.

How a gap becomes work *(proposed)*:

1. **Collect.** Gaps come from sessions (with consent), from tier-2 tools with no open alternative, and from anyone who files one.
2. **Rank.** Once a month, the steering group puts the gaps in order: how many organizations asked, how much it would help, how small the first version can be.
3. **Pick a route.**
   - **Volunteer:** the gap gets a "good first project" label and a short brief (the builder-brief format when it exists).
   - **Hackathon:** the top few gaps become challenges, each with made-up test data and a definition of done.
   - **Workshop cohort:** a group of owners and helpers builds one gap together, which also teaches them to maintain it.
   - **Funded:** for gaps that need steady work, the host non-profit seeks a grant or a sponsor, and pays a maintainer, preferably by improving an existing open project rather than starting a new one.
4. **Close.** A gap closes when an open tool meets it and has a tool record. Prefer sending the work upstream to an existing project over a new fork.

## Questions

Open an issue. If something here is unclear, that is a bug in this file: tell us.
