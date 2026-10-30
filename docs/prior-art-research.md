# Prior art: interview skills, and who has already built this

Findings from a search on 2026-10-28. Not a verdict, not a recommendation. A map of what exists, with the parts worth stealing and the parts worth refusing, so the design agent does not spend a week rediscovering them.

Marks: **[✓]** read at the primary source during this search. **[~]** credible secondary or vendor claim, primary not verified. **[not found]** searched and did not turn up.

---

# Part 1 — Agent skills that interview a human

The best-developed interview technique packaged for an agent is Matt Pocock's `grilling` family, in `mattpocock/skills` (MIT licence, ~305k stars at the time of writing, ~37 skills). **[✓]** It is built for software planning, not for understanding a business. The mechanics transfer; the posture does not. Both halves matter.

## 1.1 The mechanism, precisely

The `grilling` skill **[✓]**

- Maps the subject as a **design tree**: every decision branches into the decisions that hang off it.
- Defines the **frontier** as every decision whose prerequisites are already settled — "the questions you can ask _now_ without guessing at answers you haven't heard yet."
- Asks the whole frontier in one **round**: numbered questions, each with a recommended answer.
- Recomputes the frontier after each round. A question that depends on another open question belongs to a later round.
- Splits **facts from decisions**: "Finding _facts_ is your job, never the user's." If a frontier question needs something in the environment, dispatch a sub-agent rather than ask. The round does not wait; only the downstream questions wait.
- Ends when **the frontier is empty** — "every branch of the design tree visited, nothing left silently assumed" — and then **stops and asks the user to confirm shared understanding** before acting.

`grill-with-docs` adds a glossary and ADRs; `wayfinder` extends the same structure across sessions; `to-spec` converts a settled conversation into a spec; `to-questionnaire` is the async variant. Their own docs are unusually candid about where each fails, which is why they are worth reading rather than skimming. **[✓]**

## 1.2 What transfers, and it is a lot

**The frontier is a coverage guarantee without a question bank.** This is the direct resolution of the tension in `design-considerations.md` §2 — constrain the conversation to guarantee coverage, or leave it free to listen. The frontier is a third option: coverage comes from a *dependency structure*, and the questions stay generated rather than scripted. Nobody has to write a question bank; the tree says what is askable now.

**Facts are the agent's job, decisions are the person's.** This is the documents-first rule stated as a hard split, and their docs are emphatic: an agent that answers its own questions "has broken the skill". For a business interview, the split has a third category the skill does not need and this project does: **experience**. Facts come from files. Experience — what a Tuesday is like, what people dread — only comes from the person, and no amount of looking things up substitutes for it.

**Frontier-empty as the termination condition, plus a confirmation gate before acting.** An interview otherwise has no definition of done. This gives it one that is checkable, and it separates "we have asked everything" from "we agree about what we heard".

**Write the artifact the moment it resolves, not in a batch.** In `grill-with-docs` a term goes into `GLOSSARY.md` as it settles, and the glossary — not the spec — is described as the main lasting output. **[✓]** For a resumable interview this is the difference between a state file and a transcript.

**Three gates for what deserves a record:** hard to reverse, surprising without context, and a real trade-off. Most decisions fail at least one, so most sessions produce no ADR at all, "and that is working as designed". **[✓]** That is a usable rule for the decision log, and it prevents the opposite failure — logging everything until the log is unreadable.

**A published failure list, which is worth adopting wholesale as a test suite [✓]:**

- It answered its own questions instead of asking.
- It ran out of questions and started building (the confirmation gate exists for this; weaker models skip it).
- It collapsed "interview until shared understanding" into two questions and an outline.
- A skill that names another skill does not reliably cause it to load, so the agent improvises an interview.
- Most of what was agreed "exists only in the context window" — the decisions evaporate when the session ends.
- Two questions land in one round when one answer should have changed the other.

Every one of those has a direct analogue in a business interview, and the last one is the resumability problem in its native habitat.

## 1.3 What does not transfer, and this is the important half

**Rounds, not one question at a time.** `grilling` deliberately asks the whole frontier per round, and its docs defend the choice. But the same docs say the sequential mode is a *supported* setting rather than a workaround, and that it is preferred by "users who read slowly, who work in a second language, or who use the sequential format to help them focus". **[✓]** That is the target population of a small-business interview, not an edge case. Take the dependency tree; reject the batch.

The underlying reason is a different one from reading speed: rounds are efficient for someone who already knows what they want and needs decisions extracted. They are poor for someone who is working out what they think. An owner describing their week is in the second state.

**Recommendations attached to every question.** Each question carries a recommended answer and is worded so that "yes" accepts it. In software planning this is efficient: the user is the domain expert and the agent is a fast, well-read colleague. Their docs already name the two costs — a recommendation can argue *against* its own question, and the thing to watch for is "nodding along". **[✓]**

For a business interview it is contamination. The whole output is *what the person actually said*; an agent that proposes the answer is putting words in the record. This is a sharp fork worth writing down: **recommend for decisions, never for facts or experience.** Where the agent does have a view ("this sounds like a duplicate-entry problem, not an AI problem"), it should hold it until after the person's account is on the page, and then offer it as a separate, labelled opinion.

**The tracker.** `grilling` assumes a repository and an issue tracker; `wayfinder` puts the map and its tickets on one. **[✓]** This project must work with no repo, no tracker, no accounts, and probably no network beyond the model.

## 1.4 `wayfinder`: the best published shape for a multi-sitting task

`wayfinder` handles an effort too large for one session, and several of its structures are better than anything else found for a resumable interview **[✓]**:

- **The map is an index, not a store.** A decision lives in exactly one place, its ticket; the map holds a one-line summary and a link. A session loads the map at low resolution and opens detail only when needed. This is how a long-lived artifact stays readable.
- **Four sections:** destination; decisions so far (one line each, with a link); **"Not yet specified" — the fog of war**; out of scope.
- **The test for fog versus ticket:** can the question be stated precisely *now*? Not "can it be answered" — can it be *phrased*. When a ticket resolves, the fog in front of it clears and anything now specifiable graduates into a ticket.
- **The frontier is open, unblocked, unclaimed tickets**, and a session **claims a ticket by assigning it before doing any work**.
- **The destination is named first**, before any ticket exists, "because the destination fixes the scope you measure every ticket against".

The fog-of-war section is the missing piece in most interview designs: the place for "I know I will need to ask about X but cannot phrase it yet" — which is exactly what an open-question queue becomes once the interview is long. And "claims it before doing any work" is a concurrency primitive that a state file needs if two sittings, or two agents, can ever touch the same profile.

## 1.5 `to-spec`: what an artifact of this kind should and should not do

Two rules worth importing **[✓]**:

- **"It does not validate or decide anything. It records what you decided… If the spec states something you never said, that is a defect."** A profile written by an interview agent has the same obligation, and it should be stated in the same words.
- **Sketch the seams before writing prose.** `to-spec` identifies where the thing will later be tested and gets agreement on them first, preferring existing seams and "the ideal number of seams for a change is one". For this project that argues for deciding, with the owner, *what will be checked* before writing the opportunity brief — which is also the only way the brief can carry acceptance tests later.

## 1.6 The chain, as a shape

`grilling → to-spec → to-tickets → implement → code-review → retro` **[✓]**

An interview, a record of what was decided, work items, building, review, reflection. The shape this project needs is the same, over a business instead of a codebase. That is worth noting because it means the *interfaces* between stages are already thought through by someone — and because it shows what happens when one stage is missing: `to-spec`'s docs say that when the record step is skipped, later steps "soften precise answers into weaker prose, and the result can look complete while missing the thing you decided." **[✓]** An interview with no record stage has the same failure, and it will be invisible.

## 1.7 Also worth a look

- `to-questionnaire`: described as the skill for "a decision blocked on knowledge in someone else's head" **[~]** — that is the unaccompanied/async interview, and the docs page did not resolve at the path tried, so find it before designing that mode.
- `triage`: grilling applied to a vague report. The analogous stage here is turning a vague complaint into a scope-able problem.

---

# Part 2 — Has someone already built this? Yes, several someones

**The short answer: the core idea exists commercially in at least three products and academically in one paper.** Nothing found does the whole of what this project intends, but "nobody has thought of this" is not an available claim, and the design should not be built as if it were.

## 2.1 Academic: the closest thing to a controlled study

**LLMREI: Automating Requirements Elicitation Interviews with LLMs** — arXiv 2507.02564, submitted 3 July 2025, published at IEEE RE'25. **[✓]**

What it is: a chat bot that conducts requirements elicitation interviews with minimal human intervention, evaluated on 33 simulated stakeholder interviews in two scenarios (a hair salon and a ski resort), conducted in person by students through a chat interface. The students also played the stakeholders and later reviewed transcripts, which the authors name as a limitation: "we had to act as both interviewees and reviewers, making error identification more subjective."

Three approaches: zero-shot with a **three-sentence** system prompt; least-to-most with an elaborate guideline prompt (five-step process, predefined roles, explicit follow-up "question pathways", scenario examples); and fine-tuning a GPT-3.5 model on recordings of real interviews, which was **abandoned** — the fine-tuned versions produced incoherent responses, lost the thread, and in one case switched language mid-interview.

Findings **[✓]**:

- A similar number of common interviewer errors to human interviewers.
- Up to **60.94%** of requirements fully elicited, **12.76%** partially, **73.7%** total, on the better of the two prompts.
- "A notable ability to generate highly context-dependent questions."
- **Correction 2026-10-28 (checked at source, see `DESIGN.md` §4):** the next bullet overstates the paper. Short and long prompts elicited about the same (73.7% vs 68.1%), with "no significant difference" per the authors; the long prompt made fewer mistakes; the one-question instruction failed in about a third of short-prompt turns.
- **The short prompt beat the long, guideline-heavy prompt at eliciting requirements.** The elaborate scaffolding did not buy coverage. This is the single most useful data point found for the tension in `design-considerations.md` §2, and it points away from scripting.
- They had to add an explicit instruction to **ask one question at a time**, because the bot "would sometimes overwhelm users by asking multiple questions at once". That failure was not in the existing mistake taxonomy.
- They categorized errors using **Bano et al.'s framework** of common elicitation-interview mistakes, and built the guidelines from **Ferrari et al.'s** requirements-interview guidance (discuss existing systems, involve multiple stakeholders, summarize key points).
- There is a **replication package** with the prompts, raw interview data, and ground-truth labels: `doi.org/10.5281/zenodo.14988928`. Get it before writing a prompt.

Why it is adjacent rather than the same thing: the artifact is a *requirements list for a software system*, not an operating profile of a business. It has no consent layer, no ownership or portability design, no notion of the organization's constraints or values, and it assumes a human in the room. The authors themselves conclude that human-led interviews remain necessary "to cope with highly sensitive or complex elicitation scenarios, where interpersonal dynamics play a crucial role in uncovering unspoken requirements". **[✓]**

Two things to take directly: **the mistake taxonomy as an evaluation rubric** (Bano et al., plus the one-question-at-a-time addition), and **the finding that less scaffolding elicited more**.

## 2.2 Commercial: three products, all closed

**Operable** — operable.work. "You can't hand your business to an agent it can't understand." Voice-first, a **20-minute first session**, one workflow at a time. Output: a current-state workflow, a tool list, and a machine-readable JSON artifact with an `agentOpportunities` array. Free to use. Pitched explicitly against consultants and against SOP-writing. **[✓]** as marketing copy; not tested. The closest thing found to this project, and deliberately narrow: one workflow, not the business.

**NxtOS** — nonlinearos.com. A **15-minute guided interview** that "keeps your words, so what comes out reads like you, not a consultant's template", producing a one-page "Action Organizer": every core function in a row, its current level of autonomy, the level it should reach, and the one function to start with. The map is then read by the user's existing Claude or ChatGPT subscription so the AI "knows your business" before answering. Free Mac app; a guided month with four touchpoints, then **$1,500/month continuation**. **[✓]** as marketing copy. Closest on "keep their words" and on handing the map into a general subscription rather than a bespoke app.

**AIOS** — aios.tech. Voice interview → analysis → prioritized roadmap with ROI estimates and tool matching. Testimonials only. **[~]** Weakest evidence, most consulting-shaped of the three.

Adjacent services (not products): The Agent Company, 100fold, Aire Labs — all "we embed and build for you", which is the model this project's cooperative framing is an alternative to.

**What the commercial field converges on:** one workflow, fifteen to twenty minutes, a JSON export, an opportunities list, and a handoff into an agent. That framing is legible, sellable, and *not the same as understanding a business*. It is a real risk that a design aimed at "agent-readable business context" drifts into it by default, because it is the shape the market has already validated.

**What none of them offer, and what a small nonprofit specifically cannot buy:** open source; an artifact in the org's own folder that survives the vendor; a profile rather than a workflow; anything about constraints, values, or who must say yes; any teaching; any maintenance path; any consent design. That cluster is the only honest differentiation, and it is a strong one — but it is a *positioning* claim, not a technical moat, so it has to be built, not asserted.

## 2.3 Nonprofit AI readiness: many tools, all questionnaires

Neon One, TappHQ, BBNK Nonprofit Talent, Enspire, nonprofitassessment.org, and Georgetown's AI Toolkit for Nonprofits. **[✓]** as existing pages; the assessments themselves not taken.

All are form-based, scored across pillars or dimensions, and return a prioritized action plan or roadmap. Most are lead generation for a service. Two worth reading:

- **Georgetown's AI Toolkit** — a research-based adoption framework for the nonprofit sector, rather than a product.
- **nonprofitassessment.org** — "about seven minutes, and it never argues for adopting anything". That posture is rare enough to be worth studying.

The structural point: the nonprofit sector is being served **forms**, not interviews. A form cannot follow up, and the follow-up is where the value is. This is the same gap the project exists to fill, which is encouraging, and also a warning about how the sector expects this to look.

## 2.4 GitHub: nothing implementing it

Searched (2026-10-28, `gh search repos` plus topic searches): `ai-readiness`, `digital-maturity`, `business-discovery`, `interview-agent`, `ai consultant agent`, `discovery call agent`, `onboarding interview agent`, `business context agent`, `company knowledge agent`, `requirements elicitation`. **[✓]**

What turned up:

- **Scorecards and maturity assessments** — single-file questionnaires, small, often for consulting lead generation, sometimes in Spanish or Portuguese for SME diagnostics.
- **Job-interview agents** — a crowded field, all about candidates and hiring, which is a different problem with the opposite power dynamic.
- **Company-knowledge RAG agents** — "answer employee questions from company documents, with citations and per-folder access control". These are the **opposite direction**: they consume the documents that already exist and answer questions from them. They do not elicit what is not written down, and they do not produce anything an agent can act on.
- **Project-context formats** — e.g. `.faf`, "persistent project context" MCP servers. Adjacent in spirit (an artifact that carries context to an agent), but they *store* context rather than *elicit* it.

No repository found that interviews a business and produces an operating profile. The nearest usable code is Matt Pocock's `grilling` (MIT) and LLMREI's Zenodo replication package.

**LLMREI is not on GitHub** as far as this search could tell — a repository with the same name exists but is empty. **[not found]** beyond that.

---

# Part 3 — What this changes about how to think about it

**Novelty is not the available claim.** The available claims are: open and portable; the artifact belongs to the organization; interview quality measured rather than asserted; teaching built in; maintenance designed in. Those are worth more than novelty anyway, and they are checkable.

**Two free gifts.** LLMREI's prompts, mistake taxonomy, and finding that short beats elaborate. Grilling's dependency structure, termination condition, record gates, and failure list. Both are licences you can use.

**One free warning.** The commercial field has already converged on "one workflow, twenty minutes, export JSON for an agent". That is the shape a funder or a partner will recognize and ask for. If the design drifts into it by default, it has rebuilt Operable with worse distribution.

**One question to put to the design agent, early:** *what does an operating profile give that a workflow map cannot?* If the answer is only "more thorough", the narrower product is the better product and the project should narrow. If the answer is structural — the week, the money, the constraints, the values, the never-hand-off list, who else must say yes, who maintains it — then say that, and design for it, because that is the part none of the existing tools attempt.

**And one thing none of them do at all:** ask what happens in month thirteen. Every product above ends at the handoff. The maintenance question is unanswered in the entire field.

---

## Sources

- `mattpocock/skills` — MIT, `skills/productivity/grilling/SKILL.md`, `docs/productivity/grilling.md`, `docs/engineering/grill-with-docs.md`, `docs/engineering/to-spec.md`, `docs/engineering/wayfinder.md`. **[✓]** Read 2026-10-28.
- LLMREI, arXiv 2507.02564 (IEEE RE'25). **[✓]** Abstract and results sections read; replication package at `doi.org/10.5281/zenodo.14988928` not yet fetched.
- Bano et al. — mistake taxonomy for elicitation interviews. **[~]** Cited by LLMREI; primary not read. Pull it as a rubric.
- Ferrari et al. — requirements interview guidelines. **[~]** Same.
- Operable (operable.work), NxtOS (nonlinearos.com), AIOS (aios.tech). **[✓]** Pages read; claims are vendor marketing, not tested.
- Nonprofit readiness assessments: Neon One, TappHQ, BBNK, Enspire, nonprofitassessment.org, Georgetown AI Toolkit for Nonprofits. **[✓]** Pages seen; assessments not taken.
- GitHub searches as listed in §2.4. **[✓]** 2026-10-28.

---

## Suggested next reads, in order

1. LLMREI's replication package — the prompts and the labelled interviews are the cheapest possible head start, and the labelled mistakes are a ready-made rubric.
2. Bano et al.'s mistake taxonomy, at source.
3. `to-questionnaire` and `wayfinder` in full, before designing the unaccompanied and multi-sitting modes.
4. One of Operable or NxtOS, used for real on a single workflow, as a competitive teardown. Twenty minutes, free, and it will settle more design questions than another week of reading.
