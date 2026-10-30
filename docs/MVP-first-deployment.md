# MVP for the first deployment (hard date: usable by Fri 2026-10-30)

## Where it will be used

A two-hour public-library workshop, "AI for Small Business", first run Monday 2026-11-02 at 2pm in a room of ten library MacBooks, with a repeat on 2026-11-30. About 10 beginners, each at one machine, using Claude Code on a library account. A facilitator (Ryan) runs the room.

In the workshop, participants **interview as a made-up owner** (Sam, who runs a bike repair shop), not about their own business, because real business details are not allowed on library machines. They keep the interview prompt to run on their own business at home.

## Design change 2026-10-28: the room does a follow-up, not a cold interview

Beginners cannot invent a whole business from nothing in 25 minutes, so the room will not start from a blank page. The first interview is treated as **already done**: the fixture holds a draft profile with marked gaps (`sam-profile-draft.md`, below). The participant, playing Sam, runs the skill in **follow-up mode**: it reads the draft profile, lists the gaps in plain words, picks the most useful ones, and asks one question at a time. Most gaps can be answered by looking at Sam's files; a few need the participant to decide what Sam would say. The agent then updates the profile and moves on to the opportunity step.

So the MVP is **follow-up mode first**; the cold first interview ("mini" mode below) is a second priority but must exist in the design and, if time allows, in the skill. The follow-up mode is also exactly the re-check interview in `REQUIREMENTS.md` 4.5, promoted to MVP, and a real use case: pick up where an earlier conversation left off.

## The constraint set the MVP must live inside

- **Delivery: a folder of plain files** put in the participant's home folder by an installer. An `AGENTS.md` at the top (was `CLAUDE.md`; changed 2026-10-29, DESIGN D23) plus skills in `.agents/skills/` (linked as `.claude/skills/`) with references. No installs.
- **The machines:** macOS, standard accounts (no admin). `python3`, `node` and `git` are installer stubs; do not need them. BSD command-line tools, bash 3.2. Finder adds `.DS_Store` files. Everything is wiped at reboot, so the profile must be copied out at the end by the participant's take-home script (the workshop team provides it) or by asking the agent to save it where told.
- **Participants are beginners.** The agent talks in short plain sentences, one question at a time, and says what it is about to do before it does it. It should not use jargon.
- **The interview slice in the workshop is about 20 to 25 minutes.** The MVP interview is therefore short: a "mini" mode that covers the core (what the business does, a typical week, the money, the customers, the dreaded task) and finishes with a profile and 3 to 5 opportunities. A "full" mode can exist but is not required for the MVP.
- **The interviewee is a person playing Sam**, reading from a shared folder of made-up files. The agent may read those files if the participant says so, but the interview is mainly asking the person. Sam's facts are in `shop-card.md` and the other files in the fixture below.

## Fixture (made-up bike shop)

`tests/rehearse/fixture/shop/` (made up, CC BY 4.0). The workshop's participant folder is copied from it.
Files: `shop-card.md`, `sam-profile-draft.md` (the draft profile with GAPs, input to follow-up mode), `price-sheet.md`, `invoices-q3.csv`, `bank-export.csv`, `receipts/`, `customer-emails.md`. Four stated problems: money (late payer, suspected mismatches), customers (repeat emails at night), market (e-bikes, pickup), time (60-hour weeks). The planted discoveries are in `.../seed_src/answer-key.md`. **That answer key is for the test checks only; never expose it to the interviewer or the simulated owner.**

## MVP scope

Must have:
1. The skill in **follow-up mode** (reads a draft profile, finds gaps, asks one question at a time, updates the profile), plain language. "Mini" cold-start mode second priority.
2. The profile written during the interview into the participant's folder, as a fixed folder `profile/` of plain-text files (changed from "a clear fixed filename" 2026-10-29, see DESIGN D16), readable and editable.
3. The opportunity step: 3 to 5 ranked, each citing something the person said, with a "try first this week" and an honest "not for AI" entry where fitting.
4. A closing handoff note: how to run this on your own business at home, in plain steps.
5. A rehearse case with at least two simulated Sams (cooperative, vague) and checks for the principles in `REQUIREMENTS.md` section 3 and the profile in section 4.2.
6. A short facilitator note: how to start it, what good looks like, what to do if it goes wrong.

Nice to have: a generated context file and one coding-agent brief from the top opportunity (for a hands-on follow-on); a single-prompt version for any chat app.

Out of scope for the MVP: full-length mode, nonprofit branch, re-check interview, web or voice delivery, anything needing network services beyond the model.

## Success criteria

- A beginner can run it start to finish in 25 minutes without help beyond one sentence from the facilitator.
- Across the rehearse sims: one question per turn at least 95% of the time; no invented facts about Sam; at least three of Sam's four stated problems appear in the profile with a quote; at least one opportunity touches money/admin and one customer service; no flattery; no requests for passwords or real customer data.
- The profile alone, handed to a fresh coding agent, is enough for it to propose a sensible first tool for Sam.
- Clear note of what was not tested.

## Hand-back

Put the finished skill folder where the workshop team can copy it, and tell Ryan the path. The workshop team then bundles it with the shop fixture. The fixture in this repo is the master copy: change it only with Ryan's say-so, and record why in `docs/DESIGN.md`.

## Timeline

- By Thu 2026-10-29: plan, first working interview, first rehearse dry-run.
- By Fri 2026-10-30: tested enough, handed back with a list of known weaknesses.
- The room test is the real test; the run on 2026-11-02 is the first use, and the second run (2026-11-30) is the chance to fix what it shows.
