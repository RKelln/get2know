# Design: the builder side

Owner of this file: the design agent. What happens between an approved brief and a tool the owner keeps. Read with `docs/DESIGN.md` (D33, D67), `skill/.agents/skills/builder-brief/references/brief-format.md`, `handoff.md`, `tests.md` and `docs/research/limits-and-trust.md`.

## What this covers

The chain is: interview → `profile/` → one picked idea → brief → **this** → a tool in use. This note designs the part in bold: the build-planning conversation, the build, the demonstration, the trial and the write-back.

Not covered: the interview (D19, D28–D31), writing the brief (D33), the commons (D25).

## Why this needs a design

The brief and `handoff.md` already give the owner a script: copy the folder, start an AI, read three files, settle the questions, build the simplest version, show the tests. Three things are still undefined, and each is where control is lost.

1. **How big.** "The simplest version" is one line in a brief. A coding agent that is good at its job will still reach for a database, a server and a login if nothing stops it, and the owner cannot tell a small tool from a platform until the maintenance or the bill arrives.
2. **Who says the tests stand.** A builder that cannot pass a test has an easy exit: change the test. The owner approved specific words. Nothing in the current files says those words are fixed.
3. **What comes back, and who can run it next year.** A tool the builder runs is not a tool the owner has.

So: three rules, one gate, one return contract.

## The boundary: what crosses, and what does not

Design: **the brief is a closed document.** A builder that is not the owner's own AI gets `profile/briefs/<slug>.md` and `profile/limits.md`, not `profile/`. Anything it needs from the profile is quoted into the brief, in the owner's words, with its mark.

Reason: `profile/` describes a business — staff, customers, money, the things the owner ruled out. Sending it to a friend, a volunteer, or a hosted agent that reads a whole folder is a consent event whose edges the owner cannot see. A brief is short enough to read in one go and say yes to.

- Inside the owner's own AI the folder is already there and no boundary is crossed: it may read `profile/` after a yes (D3).
- A helper gets the brief and `limits.md`. If those are not enough, that is a `GAP:` to add to the brief, not a reason to send the folder.
- If the owner does want to send the folder, `share-safely` (D34) makes a copy with names and money details taken out first.
- **Untested.** The failure to watch for is a brief whose "problem" section is too thin to build from, because its writer had the profile open and quoted too little.

## Three rules for the builder seat

**Rule 1 — plain words, one question at a time, until the questions are settled.**
The brief's `OPEN:` lines are the build-planning conversation, and no code is written until they are settled. This is grilling's confirmation gate at the second seam, for the same reason as D12, one step later. The owner is not a programmer; a builder that says "I'll use SQLite and a small Flask app" has already made three decisions the owner cannot weigh.

**Rule 2 — the acceptance tests are fixed before the build, not after.**
The tests are the owner's. A builder may not weaken, merge, reword or drop one, and may not add a test that replaces one. If a test cannot pass as written, the builder stops, says which test and why in plain words, and asks the owner. A changed test is a new approval, with a date and `(said: "...")`.

Reason: this is the one inversion that turns the whole method into theatre — tests written to match whatever got built. It is also what keeps the owner able to judge the tool later (`tests.md`, teaching loop in D33 §9).

**Rule 3 — the smallest build that passes the tests.**
Start from what the owner already has: their files, their spreadsheet, their existing tool. A new dependency, account, service or place to log in must be argued for in one line — what it buys, what it costs, who keeps it working — and the owner says yes before it is installed. In order: nothing new; an existing open tool; a small thing built here; only then something bigger.

The floor, never cut to stay small: validation of anything the owner types or pastes in, error handling that prevents losing their files, every `never` line in the brief, the log if a limit requires one, and a way to stop it. A tool that is small because it skips one of these is not small, it is unfinished.

**Why a floor and not just "keep it small":** every simplicity rule in the wild needs the same exception list, or "simple" quietly becomes "unsafe". The most-used version of this idea (ponytail, MIT) measures −53% lines at flat correctness and still publishes its never-cut list; the list is what keeps that number honest.

## The gate, before anything expensive

The simplest version is not always the whole job, and sometimes the honest answer is bigger: a weekly list becomes a small database, one shop's tool becomes something three staff use. Before starting that branch, the builder writes a **gate** in the build folder, and the owner decides:

1. the cheap check (their real files on made-up data, a 20-minute spike, one afternoon by hand);
2. the result that would make the bigger build worth it, as something you can look at;
3. a cost ceiling, much smaller than the build;
4. what happens if it fails, and what happens if it cannot be run at all.

Then: pass and no budget agreed → deliver the small version plus the gate result, and ask. Fail, or cannot tell → small version, and say what was learned. A gate never authorises the spend; it earns the right to ask.

**Untested.** No builder run has met a gate yet. The risk to watch for is a gate written after the fact to justify a build already started.

## What comes back

The build is done when the owner can run it, not when the tests are green in the builder's session. Hand back, in plain words, in the build folder:

- **Each test, shown passing, one at a time**, with the thing the owner can look at: the list, the message, the file.
- **A one-page README for the owner:** what it does, how to start it, how to stop it, how to undo it, what to do when it breaks. `brief-format.md` already asks for it; this note makes it part of "done".
- **What it costs to keep:** any account, subscription, hosting or model use. If it needs a subscription, that is said before the trial, not discovered in month two.
- **Who can fix it next year:** a name, and the smallest description of how it is put together.
- **One real case:** the tool tried once on a copy of real work, with the owner watching.
- **The write-back, left ready:** `ideas.md` and the brief's status (`building` → `in use`, or `dropped` with the reason). `handoff.md` step 7 already gives this to the owner.

The builder explains what the tool does, shows the agreed checks on a real case using a copy, and leaves clear start, stop and undo steps. Clear explanation is the builder's job; do not require the owner to explain it back or pass a recall quiz (D68).

## Who the builder is

Three seats, the same rules:

- **The owner's own AI.** The common case. The folder is present, so it may read `profile/` after a yes; it still writes the build into its own folder, and still stops at `OPEN:`.
- **A helper who codes** (a friend, a volunteer, a library tech). Gets the brief and `limits.md`; the owner checks for private details first, or runs `share-safely`.
- **Us, or a workshop cohort.** Same contract; the difference is that we can prepare the gate template and the return template in advance.

Rejected for now: a Get2Know *builder* skill. It would be a fifth skill in a folder whose shape is four skills and plain text, and the builder is an agent that is not ours (Claude Code, Codex, a chat app). The brief's "For the builder" block already carries the contract. Revisit only if a live run shows a builder ignoring it — evidence first, as with D1.

## Failure modes to design against

1. **Scope drift.** The brief says the simplest version; the build grows a login, a queue and a settings screen. Guard: the gate, and "no new dependency without a yes".
2. **Test rewriting.** The build passes a test that was quietly reworded. Guard: Rule 2, and the owner hearing each test's plain words again at the demo.
3. **Real data too early.** The builder asks for the invoices to test with. Guard: made-up data or a copy first, always (`handoff.md` step 6).
4. **A tool only the builder can run.** It lives in a folder the owner does not know, started with a command they will not remember. Guard: the one-page README and "who can fix it next year".
5. **A silent subscription.** It needs an account or a paid key; the owner finds out in month two. Guard: cost stated before the trial.
6. **The owner loses the feel for the job.** The tool works and the owner stops being able to spot when it is wrong. Guard: approving the tests and seeing the agreed checks demonstrated on a real case. This is the failure the whole method exists to prevent.
7. **The builder over-promises.** "It could do X too" — a feature nobody approved, which then needs a test nobody wrote. Guard: unbriefed work goes to `Later, maybe` and is written down, not built.

## Open for Ryan

- **Where do the builder's rules live?** Today: seven lines under "For the builder" in `brief-format.md`, plus `handoff.md`. This note assumes they stay the carriers and no new skill is added. If a typed builder contract is wanted, it is one `references/builder-rules.md` that both files point at — one source, not two.
- **Is the gate a field in the brief or a file in the build folder?** This note puts it in the build folder: the builder writes it, after the owner says yes, and the brief stays the owner's document.
- **Does the builder have to state cost at all,** or is that too much for a workshop follow-up? The workshop path may need it as one line rather than a section.
- **Does a third-party seat ever get `profile/`?** Current answer: only through `share-safely`. Whether a helper may get the folder when the owner offers it is Ryan's call.

## Untested

Every rule here is a design, not a run. No builder seat has been rehearsed, no gate has been written, and no brief has been built from. The cheapest first evidence: one rehearse case where a builder agent gets only the brief plus `limits.md` for the bike-shop idea, settles the `OPEN:` lines, builds on made-up data, and is scored on three things — did it ask before installing anything, did every test's plain words survive unchanged, and does its README answer stop, undo and "what if it breaks".

## Sources

- The builder-brief seat and its prior art: `docs/research/builder-brief.md` (mattpocock/skills `grilling` and `to-spec`, spec-kit, snarktank/ai-dev-tasks, EGM).
- The simplicity floor and the measured case for it: `DietrichGebert/ponytail` (MIT, 2026-06), rules at `.agents/rules/ponytail.md`. Its published agentic benchmark reports −53% lines of code, −45% output tokens, −26% cost and −41% time against no skill, with correctness flat (hidden checks 96.7% vs 95.6%), over 39 tasks × 5 runs, alongside its harness and its own null results. Read 2026-11-01; a vendor-run benchmark, and its own README says the effect does not pay off under a day of work.
- The gate's attributes and outcomes: `alexpiar/be-ambitious-harness` README (MIT, 2026-10), which credits Felix Rieseberg, "How to be more ambitious: a tutorial for humans with models" (13 Oct 2026). Its own eval is two tasks, one pass each, so it is quoted as a design source, not as evidence.
- Limits as a starting stage, a bar to move up, a log and an off switch: `docs/research/limits-and-trust.md`; D66 for the three kinds of limit.
