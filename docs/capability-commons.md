# The capability commons (proposal, 2026-10-29)

**Status: proposal, not built.** Ryan asked for something that scales beyond hand-written cards: a database of things AI can do, open source only, kept current by regular agent maintenance, and searched cheaply against a person's profile. This is the design agent's proposal, revised the same day with Ryan's answers and his tiered-records idea (below). The did-you-know cards (DESIGN D21) are step 0 of it.

**Decided with Ryan (2026-10-29):** hosted under a non-profit; records are **CC0**; open-source connectors to closed services are allowed as a second tier, after fully open solutions (commercial open source counts as fully open: paying someone to improve open tooling is fine); scheduled agents run about **once a day on cheap models** (such as DeepSeek).

## The idea in one paragraph

A public, plain-text index of **what an AI helper can do for a small organization, and which open-source tools and skills do it**. Agents tend it on a schedule: they find candidates (GitHub, skill and MCP registries, awesome-lists), check them, describe them in plain words, and open pull requests that a person reviews. Each organization downloads the index and searches it **on its own machine** against its own `profile/` folder, so the profile never leaves home. What the matches surface: a couple of "did you know" cards in the interview, and open-source options attached to each idea. What flows back, with consent: anonymous stories ("this worked for a bike shop") and **gaps** ("nobody has a tool for X"). Over time the gaps list becomes a shared to-do list for open-source builders, hackathons and workshop cohorts. That is the "collectively craft the foundations, keep your own customizations" loop.

## Why not just search GitHub live

A quick probe (2026-10-29): a code search for skill files mentioning "invoice" returns about 67,000 hits, mostly irrelevant; a keyword search for bookkeeping MCP servers returns generic popular projects first. Topic search is far better (see Scout below): `mcp-server` + `accounting` gave 121 repos, with an open-source accounting project and a tax-filing MCP server at the top. Finding is cheap; **judging is the work**: is it relevant to a five-person shop, is it alive, is the licence open, will a beginner get it running, what does it touch, who fixes it in month thirteen? An agent doing that live in every interview would be slow, costly, inconsistent, and would read untrusted text mid-session. Doing it once, centrally, reviewed, and sharing the result is the scalable shape.

## What is in the index: knowledge first, tools when vetted

**Ryan's key idea (2026-10-29):** knowing that something is possible is already useful, and it is safe. "An AI matched a month of invoices to a bank export and found the unpaid ones" contains no code and no third-party text, so it cannot carry an attack, and the owner's own AI can build a safe version from that description alone. So the index is built in two layers, and records climb a ladder:

| Level | A record says | Contains | Risk | Automation |
|---|---|---|---|---|
| **0. Possible** | "An AI can do X" | a short plain description and the evidence | almost none: no code, no instructions from outside | high: most records start and can stay here |
| **1. Shown** | "...and here is a verified example" | a worked example on made-up data: inputs, what the AI did, the result, how it was checked | low: written by our own agents, not copied from a source | high: a prover agent runs it in a sandbox |
| **2. Recipe** | "...and here is a way to do it" | the approach, the inputs, the checks a person should do | low to medium: still our own words | medium: needs review |
| **3. Vetted tool** | "...and this existing open-source tool or skill does it, and passed our checks" | a link pinned to a tested version, plus the vetting report | the real attack surface: third-party code and text | only after automated safety checks pass; a person approves the first listing |

**Preference when matching**, because less work and better tested wins once safety is established: a vetted, fully open tool > a vetted open connector to a closed service > a recipe > a shown possibility > a bare possibility. A lower level is always available: if no vetted tool fits, "this is possible, here is how it was shown" is enough for the owner's AI to build its own.

**Openness tiers** for tools (separate from the ladder):
1. **Fully open**: an OSI-approved licence, runs without a closed service. Includes commercial open source.
2. **Open connector, closed service**: open code that talks to a commercial product (for example an MCP server for a commercial accounting app). Listed after tier 1. A tier-2 record that has no tier-1 alternative also files a **gap**: a candidate for a community-built open replacement ("vibe code the alternative").

Kinds of record, all plain Markdown with a front-matter header, linked to each other:

| Kind | One record is... | Example |
|---|---|---|
| **capability** | a job a helper can do, in the person's words, at level 0 or 1 | "Match payments to invoices" (the cards, generalized) |
| **recipe** | a way to do that job with an agent (level 2) | "Monthly invoice/bank match from two CSV files" |
| **tool** | an open-source project or skill, with its vetting report (level 3) | a bookkeeping app, an MCP server, a skill folder on GitHub |
| **story** | a real use, anonymized, with consent | "6-person repair shop: found 3 unpaid invoices in the first month" |
| **gap** | a need with no good open answer yet | "Booking page that texts customers, fully open, runs on a cheap host" |

Fields that make matching work (in the header, so code can filter without a model):
- **moves** (read, draft, check, sort, watch, connect, build) and **hats** (bookkeeper, front desk, ...): the vocabulary Get2Know already uses.
- **inputs**: what the person must have (a bank CSV export, a shared inbox, photos of paper, nothing).
- **org types** it suits; **language**; **runs**: offline / local / needs a hosted service.
- **data**: what leaves the machine, if anything. **touches**: money, customers, staff. **undo**.
- **level** (0 to 3) and, for tools, **openness tier** (1 or 2) and **licence** (SPDX id).
- **effort** to start, and **upkeep**: who maintains the tool, last release, number of maintainers. The "month thirteen" question as data.
- **evidence**: for level 1, the sandbox run log; for level 3, the vetting report; for stories, the consent note.
- **checked**: the date an agent or person last confirmed the record is true.

## The maintenance agents (the part that scales)

A small crew of scheduled jobs, each a plain skill so any agent harness can run it, each with a spending cap. They run about **once a day on cheap models** (DeepSeek or similar); only the vetter's final step and human review need more.

1. **Scout** (daily, mostly no model). The main source is **GitHub topics**, which is how agent skills are shared (Hermes agent skills, Claude skills, Agent Skills, MCP servers; Ryan, 2026-10-29). Crossing a *skill topic* with a *domain topic* gives small, relevant sets. Counts on 2026-10-29:

   | skill topic (all repos) | + bookkeeping | + accounting | + invoicing | + crm | + small-business | + nonprofit |
   |---|---|---|---|---|---|---|
   | `agent-skills` (38,515) | 42 | 73 | 15 | 64 | 66 | 7 |
   | `claude-skills` (13,245) | 21 | 40 | 10 | 32 | 57 | 5 |
   | `mcp-server` (40,574) | 40 | 121 | 78 | 157 | 34 | 8 |
   | `hermes-skill` (456), `hermes-agent` (4,740) | | | | | 1 | |

   Tens to low hundreds per pair: a daily diff (new or updated since the last run) is a handful, which triage can afford. Other sources: code search for `SKILL.md` files (noisy: a query for "invoice" gave about 67,000 hits), skill and MCP registries, curated awesome-lists, and the **gaps list** (search for what people asked for). The domain-topic list is itself maintained: it grows from the hats and from gaps. GitHub's search API allows about 30 queries a minute (hit during this probe), so the scout batches, caches, and only asks for repos pushed since its last run. Writes *found* candidates to a queue.
2. **Triage** (cheap model). For each candidate: licence check (from the GitHub API, not the README), openness tier, alive check (last commit, archived?), relevance to small organizations, duplicate of an existing record? Most candidates stop here. A promising candidate first yields a **level-0 capability record** ("this is possible"), written in our words from the README's claims, before anyone trusts its code.
3. **Prover** (cheap model plus a sandbox). Takes a level-0 capability and tries to show it: makes up realistic data (like the bike-shop fixture), has an agent do the task **without any third-party code**, checks the result, and saves the log. Success makes it **level 1, shown**. This is where rehearse fits: a capability is a tiny test case with a checker. Failure is recorded too ("tried, could not show"), which is honest and useful.
4. **Vetter** (for level 3 only). Runs automated safety checks on a specific tool or skill version before it can be listed: licence and dependency audit; known-vulnerability scan; a scan of every skill, prompt and README for instructions aimed at agents (prompt injection), hidden network calls, credential access or obfuscated code; then installs it in an isolated sandbox with no secrets and watches what it touches while it runs its own tests and the matching level-1 example. The report is attached; the version is pinned. A person approves the first listing of each tool; later version bumps that pass the same checks can auto-merge.
5. **Describer** (cheap model). Writes every record in plain words (grade 6) from our own evidence, never pasting source text, and opens the pull request.
6. **Gardener** (daily slice, so the whole index is re-checked monthly). Archived, licence changed, no release in 18 months, broken links, a vetted version superseded. Marks records stale rather than deleting them, and lists what needs a human.

**Review is the bottleneck, by design** (design-considerations §12). Levels 0 and 1 are our own words plus our own evidence, so they can merge with light review (a person skims a daily digest). Metadata refreshes merge automatically. Level-3 listings need a person the first time. The crew is throttled to what reviewers can read each week: a review queue with a cap, not an ever-growing pile. A record with no reviewer stays *found* and is never shown to an owner.

**Unvetted tools (decided with Ryan, 2026-10-29).** A `listed-not-vetted` tool may be named to an owner, with a one-line warning that nobody has checked its code. It is offered for use only if the owner agrees to help check it: the cost of using it is spending some of their own AI usage on the checks, and, with their consent, sending the result back. If they say no, they get the level-0 knowledge ("this is possible, here is how") or another option. Rules in `builder-brief/references/options.md` and `get2know/references/opportunities.md`. A check never asks the owner for passwords, keys, or bank or card numbers.

**Security.** Skills and READMEs are untrusted text that will reach agents. The ladder is the main defence: most of the index (levels 0 to 2) is our own words and our own evidence, so a malicious README can at most cause a level-0 record to exist. Third-party code reaches an owner only at level 3, after the vetter, pinned to a checked version, and never auto-installed. Every level-3 record says what to check before installing.

## Decision models for the narrow steps (Ryan, 2026-10-29)

Many steps in the crew are not writing; they are **narrow decisions with a fixed set of answers**: is this repo relevant to small organizations, which hats and moves does it fit, does this README contain instructions aimed at an agent, does this code read credentials, does this record still match the tool? A **decision model** answers exactly that: given an input and typed questions (true/false, one of a list, a score), it returns calibrated probabilities instead of prose. Example: Jev, from TypeSafe AI (limited early access since 2026-09-15; proprietary, no weights or paper; its maker claims 70 to 500 ms and 40 to 400 times cheaper than frontier models, on its own workflows; read on Wikipedia 2026-10-29, not tested).

Where they fit:
- **Search:** a deterministic semantic search makes the first pass (same query, same results, cacheable, testable); a decision model then curates the top results against the profile ("does this fit, given these limits?"). Replaces the general-model rerank in the matching steps.
- **Discovery and metadata:** triage and labelling (moves, hats, inputs, touches, openness tier, relevance) as typed questions over a fixed vocabulary.
- **Audits:** the vetter's safety checks as many narrow yes/no questions, each testable against known-good and known-bad examples, rather than one big model's opinion.
- **Routing review by confidence:** high-confidence decisions merge, low-confidence ones go to a person. Review time is the scarce resource; calibrated confidence is how to spend it well.

Rules: the decision model is a **role**, not a vendor. Every question gets a hand-labelled test set and is scored on it before its answers are trusted; a proprietary model can serve while open alternatives (small open classifiers, or a cheap open model constrained to the answer set) are tested on the same sets. General models stay for the one thing they are for: writing records in plain words.

**Two axes on the test set, not one (added 2026-10-29).** Accuracy is the obvious one. The second is **presentation invariance**: ask the same question three ways — options reordered, wording rephrased, the recommendation named in one framing and not another — and the distribution should stay put. A model whose answer moves when only the frame moves is not a candidate for any question where the surface must not lean: the audits, "does this fit", routing review by confidence. The reason a decision model needs this test and a prose model does not is that its lean is unreadable — there is no argument to inspect, only a number. It is also the one capture property that can be measured on a model without a human subject (randomise the frame, hold the question), which makes it cheap enough to run on every candidate and every model change. Evidence and the argument: `docs/research/agent-lean.md`.

**Read distributions, never a single probability.** Per-option probabilities are relative to the option set, not absolute: in the published worked example a correct answer scored at raw probability 0.36 becomes 0.98 once normalised across ten options. So compare the distribution across framings and across models, and treat "confidence" as how concentrated an answer is, not as a correctness claim — the vendor's own documentation says the same.

## Later: converging builds as safety evidence (Ryan, 2026-10-29)

When something is known to be possible, different people's agents will build their own versions. If several **independent** builds behave the same, that is evidence they are all safe: the ways to solve a problem converge, while the ways to be malicious differ. Design notes for a full-scale system:
- **Compare behaviour, not code.** Run each build in the sandbox on the same made-up data and compare outputs and everything it touches (files, network, processes). Agreement on the task is the signal; anything one build does that the others do not (an extra network call, reading a credentials file) is the red flag. This is differential testing.
- **Require diversity, not just a count.** Builds that share a model family, a contributor or a dependency fail together (Knight and Leveson's result on multiversion programming; design-considerations §12). Count builds as independent only across different model families and contributors, ideally different dependencies.
- **Resist fake accounts in layers:** account age and contribution history, plus in-person vouching. The non-profit meets people at workshops and partner organizations; a vouched build can count for more than an anonymous one.
- **Limits:** a shared poisoned dependency (the vetter's dependency audit) and a bug every model makes (the prover's tests) are not caught by agreement. Convergence adds evidence to the vetter's checks; it does not replace them.
- **Where the builds come from:** popular **gaps**. Organizations' agents build their own versions anyway; with consent, those builds become the comparison set, and a converged build can become a level-3 tool for everyone else.

## Distributed vetting *(proposed, not built)*

Ryan (2026-10-29): spread the cost of vetting by making **vetting skills**, so owners who want an unvetted tool help check it with their own AI. A sketch:
- A `vet-tool` skill runs the vetter's checks on one pinned version of one tool, in a sandbox with no secrets, using the owner's AI. It never needs the owner's passwords, keys, or bank or card numbers, and stops if a step seems to.
- It writes a short report, in the same record format, about the tool only: nothing from the owner's profile. The owner sees it and says yes before it is sent (as `share-safely` does for stories).
- At the commons, a report is one piece of evidence, not a verdict. A tool becomes `vetted` only by the rules below, and a person still approves the first listing.

**Open problem: defences against malicious tool submissions.** This is not solved. Anyone can submit a tool, and anyone can submit a vetting report, so an attacker could do both. Defences to design and test, none built:
- no single contributor can get a tool vetted alone: several independent vetters, across different people, model families and machines (see converging builds above);
- no vetting result from the tool's submitter, its maintainers, or accounts linked to them counts;
- results are tied to a pinned version and file hashes; any change starts again;
- provenance: who submitted it, where the code came from, signed releases where the project has them;
- reports and tool text are data, never instructions, for the agents that read them; a report that tells an agent what to do is a red flag;
- fake accounts and vetters who collude: account age, history, vouching (above). This is the hardest part, and we do not have an answer yet.

Until this exists, owners who help check a tool are checking it for themselves; their reports wait at the commons.

## Matching against a profile, cheaply and privately

1. **Download the index** (a `git pull`, or a zip). Ships with a prebuilt **SQLite full-text index**: SQLite is in the Python standard library, so no heavy dependencies.
2. **Build the query from the profile, on the machine.** The agent reads `profile/` and writes a short structured need list: moves × hats × inputs × constraints (from `limits.md`: "nothing sent without Sam seeing it", "no cloud for customer data"). The profile itself is never sent anywhere.
3. **Filter and search** with that list: a free, instant database query returns the top 20 records.
4. **Rerank and explain.** The agent reads those 20 short records (a few thousand tokens), drops anything that breaks `limits.md`, and keeps the best two or three, each tied to a quote from the profile.
5. **Show**, in the right place: as at most two "did you know" cards in the Ideas step (D21's rules unchanged), and as an **"Options"** line under each idea in `ideas.md`, best first by the preference above: a vetted tool (with level, openness tier, effort, upkeep, what it touches), or "no vetted tool yet; this is possible and was shown on made-up data, so your AI can build a small version". An unvetted tool may be named too, with its warning and the help-check condition (above).

Cost per interview: one database query and one short model read. No live web search, so it works on a library machine with only the model's network access.

## What flows back (only with consent)

At Close, the agent may offer two things, both reviewed by the person before anything leaves the machine:
- a **story**: anonymized, generalized ("a small repair shop", never a name), one paragraph, opened as a pull request or emailed to a maintainer;
- a **gap**: "I needed X and found nothing". Gaps are the most valuable records: they tell the scout what to search for, and they are a ready-made project list for open-source contributors, hackathons and workshop cohorts.

A shared index of *needs* is still sensitive in aggregate (design-considerations §8: a collection of profiles is a dataset of small organizations' vulnerabilities). So: only generalized stories and gaps go up, never profiles; consent is per item; the index publishes no counts per organization.

## Customizations stay local

An organization copies a recipe into its own folder and changes it freely. If the change is general (a fix, a new language), its agent can offer to send it upstream as a pull request. The index never needs to know about local copies. That is the "craft the foundations together, keep your own customizations" shape, in plain git.

## How to get there in small steps

0. **Now:** `cards.md` (D21). Hand-written, 13 cards: level-0 records in all but name.
1. **Schema and seed.** Turn the cards into capability records; a standard-library script that builds the SQLite index; a `find-options` skill that runs the matching steps. Test it in rehearse against the bike-shop profile.
2. **Prover first.** Show the seed capabilities on made-up data (level 1). This builds the safest, most useful layer, and it exercises the sandbox the vetter will need.
3. **Scout and triage, daily, on a cheap model,** writing level-0 records from GitHub topics. Measure: candidates found, kept, minutes of review per day.
4. **Vetter** for the tools that matching keeps wanting. First listings approved by a person.
5. **Gardener**, then **stories and gaps** from real sessions, with consent, after the workshop shows what people are willing to share.

## Related: the Agentic AI Design Exchange (checked 2026-10-29)

The Human Feedback Foundation runs the [Agentic AI Design Exchange](https://humanfeedback.io/raise/agentic-ai-design-exchange/) (announced 2026-10-21, funded by RBC). Canadian non-profit teams design, build and deploy their own AI agents in facilitated cohorts: 90-minute workshops, or 4 to 6 weekly one-hour sessions. The first cohort starts in fall 2026. Human oversight, measurement and evaluations are part of the design. Selected designs go into an open, Creative Commons-licensed library, an "Agentic Commons", launching early 2027.

How it relates to this proposal:
- **Overlap.** Both are open commons of what AI can do for small organizations. Theirs holds agent designs from cohort teams. This one holds capability records, tools and gaps, filled in by agents and checked by people. They should link to each other, not compete. A design in their library could be a capability record here, and a gap here could be a cohort project there.
- **Differences.** Their program covers registered non-profits and is run by people in cohorts. Get2Know also covers small businesses, and runs alone, so it can reach more people without volunteers. A Get2Know `profile/` could be a team's starting point before a cohort.
- **Not known yet:** which CC licence their library uses (this commons is CC0), whether outside projects can contribute, and whether code is in scope or only design write-ups. Ask them before planning any link.

## Still to decide

- Who reviews the daily digest and first tool listings, and for how many minutes a day.
- Where the scheduled jobs run (a CI workflow under the non-profit's account is the obvious home) and the monthly cap.
- The exact vetting checklist; start from existing supply-chain tools rather than writing our own.
- How many independent vetting reports make a tool `vetted`, and how to stop one person faking several (see "Distributed vetting").

## What this proposal is not sure of

- Whether the review load stays manageable; that is the thing step 2 measures.
- Whether owners act on open-source options at all, versus the commercial default. The workshop and real interviews will say.
- Whether plain full-text search plus a model rerank is good enough, or whether local embeddings would earn their dependency. Start without.
