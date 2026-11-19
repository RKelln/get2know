# The solution commons: what Get2Know grows into

**Status: research memo and design sketch, 2026-11-17.** Not a spec, not a decision record. It answers three questions: what Get2Know could grow into; how user stories and business workflows map to AI integration and real open-source code; and what stays expensive and slow, so the project does not merely move the problem.

Written to stay general — this is the long-term shape, not one deployment. §12 is the only section that faces outward, toward a funder; everything before it should hold whether or not that application goes anywhere.

Marks: **[✓]** checked at the primary source while writing. **[~]** credible secondary or vendor claim, not checked. **(ours)** a claim from Get2Know's own work, not external evidence.

---

## 0. The thesis in five sentences

Get2Know already produces the scarce thing: a written account of how a small organization actually works, in the owner's words, with its limits and its gaps. The next step is not to build tools for each organization; it is to make the *case* the unit of sharing — the situation, the decisions, the components and their pinned versions, the tests that passed, and the failures that cost money. Cases accumulate into a public, offline-searchable library that any agent can read, that costs nothing to copy, and that is paid into with situations rather than commits. Solutions in that library are deliberately small parts with fixed seams, so a local builder composes a dependable workflow instead of commissioning a monolith — and the organization keeps a folder it can read, run and leave with. The goal is not a platform that hosts the commons; it is a commons that makes platforms unnecessary for the work it covers.

The hard part is not the library. It is that judgement, verification, support and maintenance do not get cheaper just because code does — and a commons that pretends otherwise will hand the bill to the smallest organization in the room.

---

## 1. Where the project actually is

Worth stating plainly before designing the future of it.

**Built and exercised (ours):** a five-skill interview folder (`get2know`, `did-you-know`, `builder-brief`, `share-safely`, `teach-a-job`), a chat-prompt export, a `rehearse` harness with simulated owners and code checks, a capability-commons proposal with 43 seed records (30 tools checked at source, 12 capabilities, 1 gap), and a builder contract with acceptance tests and a gate.

**Exercised once, in public:** a library workshop on 2026-11-02 where participants played a made-up owner. It went well; nobody has yet used it on their own business, and no tool has been built from a brief and run by an owner for a month.

**Not tested at all:** `teach-a-job`, `builder-brief`, `share-safely`, the chat prompts, helper mode, other languages, and the whole build-and-hand-back half of the chain.

So the honest position is: **the front half of the chain works; the back half is designed and has never been run.** Any claim about composing tools, sharing cases or a commons of solutions is a design claim until §14's first experiment is done.

---

## 2. The unit of sharing is the case, not the code

Four existing shapes get most of the way, and each stops at a different place.

**Code references (xerj [✓]).** Xerj indexes open-source repositories so a coding agent reads the real definition instead of inventing one: local, CPU, MCP-ready, Apache-2.0, with a measured 2.7× fewer output tokens than grepping, 16 of 16 tasks solved in their own test. It answers *"what does this function do?"* It cannot answer *"has anyone built this job for an organization like mine, does it hold up, and what did it cost them?"* A definition is not a decision.

**Applications (ArtCraft [✓]).** ~298k stars across the org, 17 MIT/Apache desktop apps, an open agent factory (`autocraft`) and a public governance corpus (`craft-contrib`). Brandon Thomas's line from the talk is the right instinct: give people something they can *"take away all of the surface area that they don't use and constrain the apps to their specific workflow."* But an app is still a product with a shape someone else chose, and their money sits in compute, which is where the rent re-enters.

**Adaptors (OpenFn [✓]).** 100+ open-source adaptors connecting health and social-protection systems, a Digital Public Good, GovStack- and OpenHIE-compliant, used by 70+ NGOs and government ministries. Their distinction is the one this document is built on: *"Adaptors are reusable components… Workflows are the project-specific processes that you want to automate."* OpenFn is the closest working prior art for small reusable parts with good seams — and it is still a platform, with a job language and a runtime, serving ministries rather than a four-person arts organization.

**Templates (n8n, Zapier [~]).** The failure mode to design against: thousands of templates, most of them stale, none of them carrying evidence, and the ones that work locked to a platform whose pricing you cannot negotiate.

What is missing from all four is the thing a small organization actually owns and an agent actually needs: **the case**. Not the code, not the app, not the connector — the *situation and its worked resolution*.

### 2.1 What a case contains

A case is a folder, plain text, in the same format as the commons records (`+++` TOML header, Markdown body). Seven parts, each one cheap to write and expensive to reconstruct later:

1. **The situation.** The workflow in the owner's words with the evidence marks the interview already uses (`said:`, `file:`, `GAP:`), generalized: "a 12-person arts organization that rents its venue", never a name. This is the part that is hard to fake and valuable to reuse.
2. **What made it hard.** The constraint that decided the design: no API on the funder's portal; the bookkeeper works in a second language; the board has to approve anything touching member data.
3. **The decisions.** One line each, with the reason. Why the ledger stayed where it was; why the tool writes a file instead of a database; why the jury step was left human. This is the part that makes a rebuild possible and the part no code index carries.
4. **Components and pins.** Every open-source part, the exact version or commit, the licence (SPDX), and what it was asked to do. A lockfile, in effect.
5. **The seams.** The file formats and commands between the steps. If the seams are the file system, they get listed as `in.csv → out.md`.
6. **What was proven.** The acceptance tests, and the evidence they ran: on made-up data, on a copy of real data, on whose machine. A green test with no date and no machine is a claim, not evidence.
7. **What broke.** The failure record: what went wrong, what it cost in hours, what the fix was, and what would have prevented it. This is the part every commons in the world omits, and the only part that makes the next build cheaper in practice rather than in principle.

A case is not a product listing. It is closer to a lab notebook or a legal precedent: a dated, attributable record of a situation resolved a particular way, useful to a stranger precisely because it is specific.

### 2.2 Why "the case" answers the contribution question

The usual price of using an open commons is code: you must be a programmer, or hire one, to pay in. Almost no small arts organization can pay that way, and the code they would contribute has little value to anyone else.

A case inverts it. The organization pays with the thing it has in abundance and the thing the commons cannot get any other way: **a real situation, how it was resolved, and what it cost.** The interview already writes most of it. Contributing is a review-and-generalize step, not a development project. That is a genuinely different contribution economy, and it is the only one that fits the population the project serves.

Two rules keep it honest:
- **Generalize by construction, not by scrubbing.** The case is written from the profile as "a maker-space with two staff", never as "X Studio" with the names removed afterwards. Scrubbing fails on identity-by-story (`design-considerations` §8, and `share-safely`'s checker is a backstop, not a defence).
- **Consent is per artifact, not per session.** The owner sees the exact case text before it leaves, as `share-safely` already requires.

### 2.3 Why the case is also the training set

Every case contains labelled narrow decisions: this repo is relevant to small organizations; this message fits an allowed kind; this figure has no source; this record is stale. Those are exactly the training and evaluation sets a *decision model* needs (the commons proposal's typed-questions idea), and exactly what a 7B-class model needs to be trustworthy on a boring step.

ArtCraft's talk makes the same move at the end, almost in passing: *"all of the decisions made by it are training data that we're going to use for evals and post training on the decision trees"* [✓ transcript]. A commons of cases is a decision corpus that grows with use. That is the mechanism by which the small-model claim in §11 stops being a hope.

---

## 3. The mapping: from a workflow to running code

The chain Get2Know already has is: interview → `profile/` → one picked idea → brief → build → hand-back. What it does not have is a repeatable way to get from a described workflow to *specific open-source parts, and the glue between them*, without a capable developer improvising each time.

Five steps, in order. The order matters: each step narrows the next.

### Step 1 — Describe the workflow as steps, in the owner's words

Not "grant reporting". The six steps someone actually performs, with the trigger for each ("the funder's email arrives", "the quarter ends"), the time it takes, and what goes wrong. The interview already asks for the triggering event (ours, D61 — failure demand), which is what makes this step possible.

### Step 2 — Classify each step by what it needs

Four kinds, and the classification decides everything downstream:

- **Facts** — a number, a date, a status that exists somewhere. Can come from a file, a database, an API.
- **Mechanical work** — match, sum, sort, deduplicate, convert, file. Deterministic code does this better than a model, always.
- **Language** — read a messy document, draft a paragraph in the organization's voice, explain a rule plainly, translate. This is where a model earns its place.
- **Judgement** — what to disclose, whether to return the money, whether an artist's work fits the program, whether a shortfall is the ED's problem. Stays human, and the case says why.

### Step 3 — Choose the automation level for each step, explicitly

The commons proposal already cites Sheridan and Verplank's 1978 levels of automation (checked via secondary sources) and Get2Know's shape order: *prevent it, let them look it up, answer on its own within a ceiling, assist, keep human* (ours, D61). The point of naming the level is that "AI does the workflow" and "AI drafts one email" are the same sentence otherwise, and the difference is where trust is lost.

### Step 4 — Name the existing component before writing anything

The default is that a mature open-source project already does the mechanical part, and the right move is to drive it, not replace it. Get2Know's commons already holds 30 such tools verified at source: CiviCRM (AGPL-3.0-or-later) for membership and donations, GnuCash (GPL-2.0-or-later) and Frappe Books (AGPL-3.0) for ledgers, ERPNext (GPL-3.0) and Odoo Community (LGPL-3.0) for the larger back office, Kimai (AGPL-3.0-or-later) for time, EspoCRM (AGPL-3.0-or-later) and SuiteCRM (AGPL-3.0) for contacts, pretix (AGPL-3.0) for ticketing, InvenTree (MIT) for equipment loans, Listmonk (AGPL-3.0) for mail, Formbricks (AGPL-3.0) for intake forms, Nextcloud (AGPL-3.0-only) for files, LibreOffice (MPL-2.0) for documents people insist on.

The rule to state in the brief and enforce in the build: **nothing new without a name and a reason.** A new component is allowed only when step 4 comes up empty, and then it is written as a candidate for the commons, not as part of the org's private tool.

The list is not only back-office. The ArtCraft applications are MIT/Apache and ship a CLI and an MCP server by design [✓], which makes them legitimate components for an arts organization's *media* work — photo preparation, motion graphics, cutting a short video — rather than a rival product. The same test applies: drive one, don't rebuild it, and record what it did. ArtCraft's own ambition ("take away all of the surface area they don't use and constrain the apps to their specific workflow") is precisely the composition thesis, aimed at creative software instead of administration.

### Step 5 — Write only the seams, prove them, record the case

What remains is glue, a custom view, and the tests. That is the honest description of "AI builds your tool": it writes the small amount of code that connects parts which already exist, plus whatever surface the organization actually uses. The ArtCraft line applies literally — take away the surface area they don't use and constrain the thing to their workflow.

### 3.1 Worked example: quarterly grant reporting at a four-person artist-run centre

The workflow everyone in the arts knows, and a good test because it is data-heavy, judgement-heavy, and the portal is hostile.

| Step | Needs | Level | Component | What we write |
|---|---|---|---|---|
| Funder's call arrives | facts | prevent + look it up | shared calendar file; a mail filter | a `deadlines.md` the agent maintains; one reminder |
| Gather activity numbers | facts + mechanical | answer within ceiling | ticketing CSVs, GnuCash export, attendance sheets | a normalizer: any CSV → one `activity.csv` |
| Reconcile budget vs actual | mechanical | assist | ledger export + the approved budget PDF (`pdftotext`) | a diff that names each variance and its source line |
| Draft the narrative answers | language | assist | none; a model with the org's own words from `profile/` | a prompt + a fact sheet; **no number enters the draft without a source** |
| Attach documents, submit | mechanical | keep human | the funder's portal, unchanged | a checklist; the ED clicks submit |
| File the receipt, set next deadline | mechanical | on its own | files + calendar | two lines of code and a log entry |

**The seams:** `activity.csv` → `budget-diff.md` → `draft/<question>.md` → a checklist → the portal. Every step writes a file a person can open. Nothing holds state the next step cannot read.

**The decisions written into the case:** the ledger stays where it is (the bookkeeper's habit beats a migration); the diff never guesses a category (an unmatched line is a `?`, not a best-fit); the narrative draft may say "we underspent on X" only if the ED has already said what that means.

**What stays hard, and the case says so:** the portal has no API and changes yearly; the bookkeeping is only as good as the bookkeeper; and whether to disclose a shortfall is the ED's call, not the tool's. The tool makes the situation legible. It does not fix the bookkeeping, and pretending otherwise would be the problem-shifting this document is trying to avoid.

**Size:** a few hundred lines of glue, one skill, one test fixture. Not a product, and not a startup.

### 3.2 A second example, chosen to show a limit

Artist call intake and jurying: 140 submissions, three jurors, access needs, conflict-of-interest rules, a deadline, and an outcome letter to every applicant.

AI does: de-duplication, eligibility checks against the posted criteria, anonymizing files for a blind round, scheduling, and drafting the two hundred words of the outcome letter. AI does not: rank the work, break a tie, or decide whose practice fits. The case records that the jury step was left human *and why*, which is more useful to the next organization than the automation is.

---

## 4. What a "brick" must be, to be a brick

Ryan's framing — small reusable parts with good seams so what gets built is more robust than whole custom software — only holds if "brick" is a testable standard rather than a metaphor. Seven properties. A component that fails any one of them is a product wearing a brick costume.

1. **One job, stated in a sentence.** If the sentence needs an "and", it is two components.
2. **Drivable from a shell, with `--json`.** No SDK required, no daemon required. This is what makes it usable by any agent, and it is the difference between a component and a framework.
3. **Files in, files out.** The universal seam. A component may have an API, but if the only way to get data out is the API, it fails the brick test for this population — an organization must be able to take its data and leave.
4. **A licence that composes.** SPDX-declared, checked automatically. Copyleft is fine and often preferred (§9.2); *undeclared* is not.
5. **No account, no phone-home.** Anything needing a hosted service is a second-tier component and says so on the label (the openness tiers the commons already uses).
6. **A test fixture, shipped.** One small made-up dataset and the expected output. This is how a stranger — or an agent — checks the component still does what the record claims.
7. **A declared blast radius.** What it reads, what it writes, what it touches: money, customers, staff. One line. An owner cannot weigh a risk nobody named.

**What we deliberately do not standardise:** the language, the database, the UI, the host, the model, the file layout. The seam catalogue is the standard; everything else is a default someone can overrule. The moment the commons also owns the runtime, it has become the platform it was founded against.

### 4.1 The seam catalogue

Six, and no more to start:

- **A folder of plain files** (CSV, JSONL, Markdown) — the default interface between steps, and the thing the owner can always open.
- **SQLite** — the local store; in the Python standard library, so no install (ours, the commons already builds its index this way).
- **A CLI with `--json`** — how an agent drives a component.
- **MCP** — how an agent discovers and calls a tool that is not local.
- **HTTP + JSON** — for anything that genuinely lives elsewhere.
- **A watched folder or cron** — the smallest possible scheduler, and the honest one for a single machine.

A component may offer more. It must offer at least one of the first three.

---

## 5. The library: Togather-shaped, not platform-shaped

Ryan's analogy is the right one, and it is worth being precise about which parts transfer. Togather (ours) is a self-hostable Go server that ingests many sources, normalizes them to one schema, puts doubtful items in a review queue, exposes a public API and a set of agent skills, and is run per community by a foundation. Four of those five properties are what a solution commons needs.

**Borrowed from Togather:**
- **Normalise to one record schema**, so tools can be written once against it.
- **A review queue with a cap**, not an ever-growing pile (the commons proposal's deliberate bottleneck).
- **Agent skills as the interface** — a library that only a web UI can browse is a library agents cannot use, and agents are half the users here.
- **A public API and a local copy** — a `git pull` or a signed bundle, searchable offline. No account, no login, no per-seat pricing.
- **Run by an institution, per community** — but see §9 on capture.

**Not borrowed:** Togather ingests whatever it finds. The commons cannot; every record carries provenance and a verdict, and the verdict is the product.

### 5.1 The mechanics, concretely

- **One record per file, TOML header, Markdown body** — already the convention in `commons/records/`, and the reason is sound: `tomllib` is in the standard library.
- **A prebuilt SQLite full-text index** shipped with the bundle, so a laptop with no network can search 10,000 cases in milliseconds.
- **A lockfile per case** (`components.lock`) with commit hashes, so a rebuild in 2029 is the same build as 2027.
- **Grading, not gatekeeping.** Every record has `status` and an evidence grade (`possible`, `shown`, `recipe`, `vetted`, `stale`) — the ladder the commons already defines. Nothing is hidden; unsupported claims are labelled, not deleted. Hidden things get re-created outside the commons, worse.
- **Mirrors and forks are first-class.** The registry is a git repository under CC0. If it is captured, it is copied, and the copy is legitimate. This is the structural answer to "who watches the librarian".

### 5.2 What an agent actually gets

Not a prompt stuffed with records. A two-step protocol, because context is the scarce resource and injection is the standing risk:

1. **Find, deterministically.** The agent turns `profile/` into a short need list (`moves × hats × inputs × limits`, already designed in the commons proposal), then runs a local query. Top 20 records, structured fields only — never free text from the corpus.
2. **Read three, in full.** Only the top three, from the signed bundle, with their components, seams, tests and failure notes. That is the context budget: a few thousand tokens of *situated* knowledge instead of a model's prior.

Then `build-from-record`: settle the `OPEN:` lines, use the pins as given, run the shipped fixture before writing anything, and keep the acceptance tests unchanged (ours, D67 — a changed test is a new approval).

**MCP surface, deliberately minimal** (Ryan's stance): `find`, `get`, `components_for`, `record_case`. Four tools. The browsing UI is a static site; the editing UI is a text editor and a pull request.

### 5.3 The failure record is the product

Worth saying twice. Every software commons in existence collects success stories and star counts. None collects autopsies with a bill attached. A case that records *"the ticketing CSV export changed its column order in v9.3 and broke the normalizer for a week"* saves every later organization the week — and no model could have invented it, because invented failures are plausible and therefore useless. The failure record is the one artifact that must come from a real deployment, which makes it the strongest argument that this ecosystem cannot be simulated into existence.

---

## 6. Why this should be more robust than custom software — and where that claim fails

The claim under examination: a workflow composed of small, pinned, tested parts is more dependable than one bespoke application.

**Five mechanisms that make it true:**

1. **Small blast radius.** A broken normalizer loses one step, not the organization's records. A monolith fails as a whole.
2. **The parts are maintained by people who care about the part.** CiviCRM's contributors maintain memberships for thousands of organizations. Nobody maintains the thirteenth bespoke invoice matcher.
3. **Version pins plus a shipped fixture** mean a change is detectable before it reaches the owner. npm and PyPI fail here because nothing pins *and* tests the composition.
4. **The seam is a file.** The owner can inspect anything, and can leave with everything. No format, no database, no export tool required.
5. **Independently built cases can be compared.** Different organizations' agents solving the same situation produce different code; running them on the same made-up data and comparing outputs and behaviour is differential testing, and agreement is evidence of safety while divergence flags a risk. The commons proposal already sketches this; it is the strongest available answer to "how do you trust code nobody reviewed".

**Three ways it fails, all real:**

- **Glue rot.** The glue is the least-maintained code in the composition and the most specific to the organization. This is the honest successor to "bespoke software". Responses: the glue is generated from the case and re-generatable; it is small enough to read; it has a test; and the case names who can fix it next year (ours, D67).
- **Interface drift.** An upstream component changes shape, and every composition that used it breaks at once. This is *worse* than a monolith in one specific way: it fails many organizations simultaneously. Responses: pins, the shipped fixture, and a gardener that re-checks compositions rather than records. The npm ecosystem is the cautionary case: a single transitive dependency can break a million builds, because nobody tested the composition.
- **Loss of conceptual integrity.** Fred Brooks's argument in *The Mythical Man-Month* is that a system's design must come from one mind or it becomes incoherent, and this is the strongest objection to collectively composed software. The answer is not that Brooks was wrong; it is that composition happens at the level of bricks while the *design* stays local — one builder, one case, one owner's constraints. The commons supplies materials and a precedent, not a committee that designs your tool. If the ecosystem ever starts shipping "the arts org suite", it has become a product and lost the argument.

**And one thing the claim gets wrong if stated carelessly:** a composition is not automatically safer than a monolith. Ten unvetted components have ten supply chains. Robustness comes from the pins, the tests and the review, not from the smallness. Small parts are *legible*; legibility is what makes review possible.

---

## 7. What stays expensive and slow

This is the section that decides whether the project is honest. AI collapsing the cost of writing code moves the bottleneck; it does not remove it.

### 7.1 What genuinely gets cheaper

- **The first draft of anything.** A working script, a form, a report template, a parser for an ugly CSV.
- **Explanation.** Reading an unfamiliar codebase, a funder's guidelines, a licence, a stack trace.
- **The long tail of tiny tools.** The 40-line thing nobody would ever have commissioned.
- **Translation between vocabularies.** The owner's words into a schema, and back.
- **Finding.** Code search, documentation, prior art. Xerj reports a 2.7× reduction in output tokens against Claude Code grepping the same source, 16 of 16 tasks solved — their benchmark, on 8 tasks in 4 libraries written for the test, so read it as a direction rather than a result [✓].

### 7.2 What does not get cheaper, and is where the money actually goes

1. **Deciding what to build.** Understanding a business well enough to know which of forty possible tools is worth a week. This is the entire reason Get2Know exists, and it is why the interview is the expensive, high-value part.
2. **Verification.** Someone has to run the thing on real data, in the real week, and decide whether the output is right. Models cannot certify their own output; every serious practitioner has learned this the hard way.
3. **Data cleanup and migration.** The numbers are wrong because the bookkeeping is wrong. No amount of code generation fixes a decade of inconsistent categories.
4. **Integration with hostile systems.** A funder's portal with no API, a point-of-sale locked to a vendor, a spreadsheet emailed monthly. This is where integrators earn their fee and where AI helps least.
5. **Identity, permissions, hosting, backup.** The unglamorous infrastructure. A local tool that nobody backs up is a data loss waiting for a date.
6. **Support and maintenance.** The month-thirteen question (ours). Every commercial product in the prior-art survey ends at the handoff; *nobody* answers this, which is both the gap and the difficulty.
7. **Liability.** Money, grants, tax receipts, access needs, personal data. Someone is answerable, and that someone is a person.
8. **Getting people to change a habit.** The most under-budgeted cost in every tool project ever run.
9. **Review in the commons.** The proposal already names it as the deliberate bottleneck, and it stays the bottleneck: someone reads, runs and grades. AI can pre-sort; it cannot be the accountable reviewer.
10. **Model cost and drift.** Recipes depend on model behaviour; a model upgrade can invalidate a prompt that was proven last quarter. Evidence needs re-running, not just re-reading.

### 7.3 The 50% claim, restated

"AI runs at least 50% of the workflows in an average arts organization" is the kind of number a proposal wants and a design should refuse.

What is defensible: **half the *steps* in a typical arts organization's administrative week have a known, tested path** — a component plus a seam plus a case — and a local builder can compose them without inventing anything. A six-step workflow with four known steps is not "67% automated"; two of those steps are still a person's judgement and one is still a portal. The measurable target is *coverage of steps*, plus *reuse fraction* (§10), not a headline percentage of workflows. Claiming the latter invites exactly the disappointment that kills commons projects.

### 7.4 Where the rent re-enters

ArtCraft gives away the applications and sells the compute [✓]. Any commons assembled by agents has the same exposure at three points:

- **Model APIs.** The whole pipeline is cheap only if the models are. This is why the small-model ladder in §11 is not just an ethical posture; it is the rent defence.
- **Hosting.** "Runs on a laptop" is true and insufficient; organizations want a URL. Hosting is a real cost, and someone will charge for it. Fine — as long as the tool runs elsewhere tomorrow.
- **Support.** The most defensible business in this ecosystem is not software; it is being the person who answers the phone. That is a legitimate business, and it is also where gatekeeping sneaks back in (§9.3).

---

## 8. User stories

Written as the people, not as requirements. Each ends with what stays hard, because a user story that ends in triumph is marketing.

**1. Maya, executive director, four-person artist-run centre.** Reports to two public funders and one foundation, quarterly. Spends nine days a year reconciling numbers and writing narratives, and still gets a "please clarify" email most rounds. What she gets: a budget-vs-actual diff that names its source lines, a fact sheet, and drafts she edits rather than writes; and next quarter's deadline already in her calendar. What stays hard: the portal, the bookkeeping, and deciding how much of a shortfall to disclose.

**2. Dev, operations, twelve-person arts organization.** Runs box office, memberships, venue rentals and a 400-name mailing list across pretix, a spreadsheet and Mailchimp. What they get: one nightly job that reconciles ticket sales to deposits, flags the mismatches, and updates the membership list from the same export — three small components and a cron line. What stays hard: the payment processor's fees and chargebacks, which no tool makes pleasant.

**3. Aisha, member of an unfunded collective with no staff.** A shared inbox, an open call for submissions twice a year, and a Google Drive nobody can find anything in. What she gets: intake through a form instead of email, automatic acknowledgements, a folder per applicant, and a checklist for the jury week that the collective wrote once and reuses. What stays hard: nobody is on duty. A commons can give a collective a *procedure*; it cannot give it a staff member.

**4. Tom, library technician running a monthly "AI for your organization" session.** Uses Get2Know with beginners, most of whom are not ready to build anything. What he gets: the interview, the cards, the profile, and — this is the change — *real cases from organizations like theirs*, so the session ends with "here is how a five-person gallery did it", not "here is what might be possible". What stays hard: follow-through. Most attendees will not build; the commons has to be useful to someone who only reads.

**5. Priya, independent developer.** Three small orgs a month, each wanting a tool nobody will pay properly for. What she gets: a library of cases with pins and tests, so each job starts from something proven; a brief with acceptance tests the client already approved; and a public record of the work that becomes her portfolio. What stays hard: she is still the support contract, and the fee is still small. Her business improves only if each job gets genuinely smaller — which is exactly what the commons is for, and exactly what a platform vendor would never want.

**6. Jordan, artist-member with access needs.** Needs the workshop page to say whether the room is step-free, whether there is a quiet space, and how to ask for an interpreter. What they get: intake and event pages that *must* answer those questions before publishing (the checklist is a component, not a suggestion), and a profile their own organization's agent reads before answering any question about access. What stays hard: the honest answer may be "no", and only the organization can decide whether to publish a limitation. This is the clearest "not for AI" surface in the whole set.

**7. A program officer at an arts council.** Funds forty organizations, each of which rebuilds the same admin. What they get, eventually: evidence that a grant bought infrastructure rather than forty bespoke tools; a sector-level view of which gaps remain (the commons' gaps list) as an input to their own programs. What stays hard: they cannot fund maintenance, which is the whole problem, and any tool that merely exports to *their* form has optimized for the funder, not the organization.

**8. A coding agent, 2029.** Given a brief and a profile, it must build something a person can run and keep. What it needs: three cases, a seam convention, pinned components, and tests it is forbidden to reword. What stays hard: it has no memory of the conversation that produced the brief, and it will confidently invent a library that does not exist (§10) unless the commons is the path of least resistance.

**9. An upstream maintainer.** CiviCRM's, pretix's, Kimai's. What they get: reproducible bug reports from real small-organization workloads, with fixtures attached — famously the scarcest input an established open-source project has (ours, from the ArtCraft note: "nothing in that repo has a real animator's workload behind it yet, and that's the scarcest input they have"). What stays hard: they did not ask for this, and the commons must not become a support queue aimed at volunteers.

---

## 9. Economics, governance, and the ways it gets captured

### 9.1 Who pays for what

- **The organization pays** for its build and its support, because it is the direct beneficiary and it must own the result.
- **A commons steward (an institution, funded) pays** for the record layer: review, grading, the gardener, the mirrors. This is cheap per record and expensive per month, which is the shape a foundation grant fits.
- **Integrators and third-party businesses** pay by using the commons as their materials, and contribute cases back as the price of the material.
- **Funders pay** for infrastructure they can see: a gaps list, a maintained component, a sector-wide tool.

The unsolved line: **who pays for the maintenance of a component nobody's revenue depends on.** The honest answers are mutualized support (a cooperative of organizations each paying a little), funder programs that accept maintenance as a cost, and upstream projects that already have funders. Any of these is better than a subscription that holds the tool hostage.

### 9.2 Licences are a design constraint, not paperwork

Composition has licence consequences and the commons must compute them rather than hope.

- **AGPL is the default licence of the strongest components here** — CiviCRM, pretix, Kimai, EspoCRM, Listmonk, Formbricks, Frappe Books, Nextcloud. If an integrator hosts a modified version of a composition containing AGPL code, the AGPL's network clause applies to that service. This is a feature as much as a constraint: it makes enclosing the commons legally hard, which is why the openness tier matters.
- **Source-available is not open.** Invoice Ninja (Elastic-2.0) and Akaunting (BUSL-1.1) are already `excluded` in the commons for exactly this reason, and the exclusion record explains why.
- **A composition needs a computed licence profile.** A small, deterministic check: given the lockfile, what is the strongest copyleft in the set, and what does that oblige the person hosting it to do? One page, plain words, in the case. This is a five-hour tool and it prevents a category of expensive mistake.

### 9.3 Capture, in four shapes

1. **The registry becomes the gate.** Solved structurally only by making forks easy and mirrors normal, and by refusing to host a runtime.
2. **A vendor's components become de facto standard.** Acceptable if the components are genuinely open and the licence composes; fatal if "certified" becomes a paid badge. Rule: grading is evidence-based and free; nobody can buy a grade.
3. **Integrators become the new gatekeepers**, holding the knowledge of how the org's tool works. Countered by the contract already in the builder design: the case and the one-page README are deliverables, and "who can fix it next year" is a required field. Switching must be cheap or the whole argument collapses.
4. **The commons becomes a support queue for upstream volunteers.** Countered by routing bugs to the upstream project as contributions, not demands, and by keeping the volume throttled to what reviewers and maintainers can absorb.

---

## 10. Security, and why the commons is a defence as well as a target

**The numbers that justify the whole approach.** Package hallucination is measured, not hypothetical: at least **5.2% of packages** recommended by commercial code models and **21.7%** by open-weight models do not exist, across **205,474 unique fabricated names**, with repetition making slopsquatting practical (Spracklen et al., USENIX Security '25) [✓]. Now consider an agent told to "just build the invoice matcher": the most likely failure mode of low-cost, AI-built software is a dependency that was invented and then registered by someone else. A curated commons with **pins, hashes and an offline bundle** is the direct mitigation — the agent takes the component from a list it can verify rather than from memory.

**The threats this design must answer:**

- **Records are data, never instructions.** Already a rule for owner files (ours, D27) and harder here: the commons is text written by strangers, read by agents. Search returns structured fields; full record text is read only for the top three, from a signed bundle; any record containing instructions to an agent is a defect and is reported as one.
- **Supply chain.** Licence and dependency audit, known-vulnerability scan, sandboxed run, pinned version, and re-checks tied to file hashes. The vetter design exists (commons proposal) and has never been run. **Do not claim vetting.** The honest statement is: the ladder limits exposure, and level-3 tools reach an owner only after checks that are designed but untested.
- **Malicious contribution.** Anyone can submit a case and a favourable vetting report. The open problem is exactly that, and it is unsolved in the proposal for good reasons. The partial answers: independence requirements, no credit from the submitter, version-and-hash pinning, and in-person vouching through workshops.
- **Convergence as evidence.** Independent builds that behave identically are unlikely to be malicious in the same way. This is the most interesting unbuilt idea in the proposal, and the one most worth a small experiment.
- **Model-mediated risk.** An agent that reads 5,000 records has 5,000 injection surfaces. Retrieval discipline (§5.2) is not a nicety; it is the security boundary.

---

## 11. Model strategy: the small-model claim needs a mechanism

Mozilla's call is explicit: small models, efficiency, and "projects that use a frontier-class model when a 7B model will do" are out of scope [✓]. Get2Know today runs on Claude Code and Codex, which is a real mismatch against that criterion. The fix is not to claim smallness; it is to show where each kind of work belongs.

**The ladder:**

- **Frontier model, once per organization, for the interview.** Reasons it is justified: it is the highest-judgement language task in the system, it happens once, it is the owner's own existing subscription rather than a new per-org cost, and its output is plain text that outlives the model. Also honest: no one has shown a 7B model can run this interview well, and Get2Know's own rehearsal shows how easily the interviewer supplies a frame the owner then answers inside.
- **7B-class or a narrow classifier for the repetitive decisions** — relevance, tagging, fits-a-limit, is-this-stale, does-this-message-fit-an-allowed-kind. Each is a typed question with a fixed answer set, scored on a hand-labelled set, and tested for *presentation invariance* (reword and reorder the question; the answer distribution should not move) — the one capture property measurable without a human subject (ours, `docs/research/agent-lean.md`).
- **Deterministic code for everything mechanical.** Sums, matches, sorts, conversions, diffs. "Do not use a model to add up invoices" is a rule, not a preference.
- **No model at all where a file will do.** The strongest efficiency claim in the whole design: much of the pipeline is a script reading a CSV.

**Why the commons makes the middle rung real:** every case contributes labelled decisions and their outcomes, and every composition contributes a fixture with expected output. That is a growing, sector-specific evaluation corpus — the thing that lets a small model be *trusted* on a boring step, and the thing nobody else is collecting for small cultural organizations. ArtCraft says it outright: the decisions become eval and training data [✓]. This is the technical novelty most worth putting in a proposal, because it is a mechanism rather than a promise.

---

## 12. If this becomes the HFF / Mozilla application

Only the parts that are uncomfortable, since the comfortable parts write themselves.

**The call's hard requirements, checked against the project:**

- *Working technology, deployed with the people it serves; not a wireframe.* Get2Know has a working skill set and one workshop where participants played a made-up owner. That is a **working prototype bordering on an early pilot**, not a deployment with real users. This is the single biggest gap in any application, and it is closed with real organizations, not with text.
- *Product-community fit evidence.* Eligible forms include users, contributors, community involvement, partners, downstream adoption. Realistic assets: a library workshop and a repeat, a working rehearsal harness others can run, 43 seed records checked at source, and named arts organizations willing to pilot. Thin but genuine; overstating it is the risk.
- *Charitable purpose and eligibility.* Funding must be receivable from a US 501(c)(3); fiscal sponsorship is explicitly allowed. Eligibility and the fiscal-sponsor route need confirming before writing a budget, not after.
- *AI-use policy.* "All submitted content must ultimately reflect your own original work, ideas, and voice" and applications that appear heavily AI-generated may be reviewed [✓]. This document is scaffolding for thinking. Pasting it into the form would be the wrong move twice over: it reads like a document, not a person.

**What can be claimed with a straight face:**

- The novel unit of contribution: **cases**, not code — a commons that a non-programmer can pay into.
- **Offline-first, account-free, CC0 records**, searchable on a library machine, owned by the organization.
- A **model ladder with a mechanism**: the corpus the commons produces is what makes small models trustworthy on the steps that repeat.
- **Arts organizations as the tailored population**: small, under-resourced, high-trust, unusually willing to share practice, and badly served by both enterprise software and generic chatbots.
- **Leaving something behind that others can build on** — the call asks for exactly this, and a case commons is that artifact by construction.

**What should not be claimed:**

- That half of an arts organization's workflows run themselves (§7.3).
- That components are vetted, or that robustness has been demonstrated. It is designed, not proven.
- That the builder half of the chain works. It has never been run.
- A business model that does not name support, hosting and maintenance as costs.

**On "SaaS for SaaS".** The phrase names the right shift and carries the wrong shape. Right: the organization stops buying software and instead commissions *software-making*, with a result it owns. Wrong: "as a service" implies a subscription and a vendor holding the runtime — the arrangement this whole design exists to avoid. The honest commercial form is a workshop plus an integrator practice: someone is paid to understand the organization, compose the tool from strong parts, and answer the phone afterwards. The grant's job is the layer underneath that makes those practices cheap and portable — the case commons, the seam kit, the evidence — not a product that someone has to keep selling. A subscription over the tool would be the same enclosure with a friendlier tone, and the case records make it visible if it happens.

**The honest pitch, in one line:** the call funds the transition from "an interview that produces a profile" to "a commons where a profile becomes a running tool someone else can reuse" — and the twelve months are exactly the time that transition takes, in a handful of real arts organizations, with the evidence recorded.

---

## 13. Prior art, and what to take from each

| Thing | What it is | Take | Refuse |
|---|---|---|---|
| **xerj** [✓] | Local code-reference index for agents; Apache-2.0; MCP | Retrieval of *code truth*, and the discipline of measured token/task gains | The idea that a definition is a decision: it indexes what code is, not what a situation needed |
| **ArtCraft / autocraft / craft-contrib** [✓] | 17 MIT/Apache creative apps, an open agent factory, a public governance corpus | House rules for agent fleets (a person is accountable; check then claim; verify don't guess; report only what ran); the referee pattern; one write module as a hard gate; "the scarce resource is maintainer judgement, not tokens" | App-shaped thinking; the compute subscription as the business; "clean room" claims that are not clean room |
| **OpenFn** [✓] | 100+ open adaptors, DPG, GovStack/OpenHIE, 70+ NGOs and ministries | Adaptor-vs-workflow distinction; adaptors as the model for bricks; sector-scale proof that small connectors beat monoliths | A platform with its own job language and runtime; ministry-scale assumptions |
| **CiviCRM, pretix, Kimai, ERPNext, EspoCRM, GnuCash, InvenTree, Listmonk, Formbricks, Nextcloud** [✓ licences] | Mature AGPL/GPL/MIT admin software | The mechanical 80% already exists and should be driven, not rebuilt; copyleft as enclosure-resistance | Installing one of them as "the system" — that is the monolith with extra steps |
| **Agent Skills + MCP registries** [~] | The distribution layer for agent capabilities now exists | Cheap distribution; a folder is an install | Undifferentiated listing with no evidence: slopsquatting's front door |
| **n8n / Zapier templates** [~] | Thousands of workflow templates | The user need is real and proven | Stale templates with no tests, tied to a platform that owns the runtime |
| **DPG registry / GovStack building blocks** [~] | Catalogues of reusable public-sector components and specs | "Building block" as the right granularity | Specs heavy enough to need a ministry to read them |
| **Operable, NxtOS** [✓ as marketing] | 15–20 minute business interviews producing a workflow map and an opportunities list | The interview is legible and sellable in that shape | Ending at the handoff; JSON for an agent with no maintenance path |
| **Eghbal, *Working in Public*** [~] | Open source is maintenance, not creation | The maintenance question is the real design question, and the month-thirteen test | The assumption that a healthy commons is self-sustaining |
| **Brooks, *No Silver Bullet*; *The Mythical Man-Month*** [~] | Accidental vs essential complexity; conceptual integrity | AI removes accidental complexity and leaves the essential kind; design needs one mind | Any claim that generation removes the need for judgement |

---

## 14. The cheapest next experiments, in order

Each one is meant to be falsifiable, and none requires the whole ecosystem to exist.

1. **Write ten real cases by hand**, from the workshop fixture plus three real arts organizations (with consent), before building any library machinery. If writing a case is a two-day job, the contribution economy is dead and the whole design changes. Target: half a day each.
2. **One end-to-end build from a case, by a fresh agent**, scored on four things: did it use the pins, did it add a dependency it should not have, did the accepted tests survive unchanged, could the owner start and stop the thing unaided.
3. **Measure novelty per build.** Lines of new code per composition, and the fraction of steps served by an existing component. The health metric of a commons is that this number *falls* as the corpus grows — if it does not, the commons is not doing any work.
4. **Write the seam conformance kit**: five checks a component must pass (shell + `--json`, file in/out, licence declared, no account, fixture shipped). Run it on the 30 seed tools and publish the failures; that is a real, cheap artifact with immediate value.
5. **A licence-composition checker** (SPDX in, obligations out, one page in plain words). Five hours, deterministic, prevents an expensive class of mistake.
6. **One injection test on retrieval**: put an instruction inside a record's body and confirm the find/read protocol never acts on it. A `rehearse`-style case, no model judgement needed.
7. **Ask a funder** whether commons maintenance is fundable, and at what granularity. This is the sustainability question and it is answerable by a conversation rather than a build.

---

## Sources

Checked while writing this memo (2026-11-17) unless marked otherwise.

- **Mozilla Foundation, Human-Scale AI Incubator** — call for proposals and FAQs, read at source: seven projects, up to $500k over three years ($300k + 12 months from April 2027, up to $200k + 2 years follow-on), three principles (Small, Intentional, Tailored), six evaluation criteria, deadline 20 Nov 2026 23:59 PT, fiscal sponsorship allowed, AI-use policy. [✓]
- **xerj.org** — query engine, code-reference use case, Apache-2.0, 2.7× fewer output tokens versus Claude Code grepping, 16 of 16 tasks solved on their test. [✓]
- **ArtCraft** — `docs` in this repo's sibling research: `research/notes/2026-11-16-artcraft-open-source-the-world.md` (GitHub API checks 2026-11-16) and the talk transcript `research/raw/videos/2026-11-16-artcraft-open-source-the-world.md`. [✓]
- **OpenFn** — adaptors docs ("adaptors are reusable components… workflows are the project-specific processes"), 100+ adaptors on the site, 62 publicly supported in docs, DPG, GovStack/OpenHIE; `OpenFn/lightning` LGPL-3.0 via GitHub API. [✓]
- **Spracklen et al.**, "We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs", USENIX Security '25 (arXiv 2406.10279): ≥5.2% commercial / 21.7% open-weight, 205,474 unique hallucinated names. [✓]
- **Component licences** — GitHub API, 2026-11-17: civicrm-core AGPL-3.0, pretix AGPLv3 (LICENSE file), Kimai AGPL-3.0, EspoCRM AGPL-3.0, ERPNext GPL-3.0, Odoo LGPL-3.0, InvenTree MIT. The rest from this repo's `commons/records/tool/`. [✓]
- **Get2Know internal** — `docs/capability-commons.md`, `docs/design-builder-side.md`, `docs/DESIGN.md` (D25, D61, D66, D67, D27), `docs/prior-art-research.md`, `docs/research/agent-lean.md`, `commons/records/`. (ours)
- **Togather** — instance and pipeline description from the operating skill, not a public specification. [~]
- **Brooks** (1975, 1986) and **Eghbal** (2020) — cited for the argument, not re-read this session. [~]
