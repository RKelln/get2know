# Design considerations

Food for thought for whoever designs the architecture and plans the first build. **This is not a spec and it does not choose approaches.** It is a list of forces that will pull the design in different directions, with the evidence behind each.

Many of these are in tension with each other. That is the point. Where two sections disagree, the disagreement is real and probably has to be resolved by testing rather than by argument.

Several sections suggest something to *check*, meaning: read it at the primary source before relying on it. The evidence labels are honest about how much work has been done:

- **[✓]** read at a primary source while preparing this note.
- **[~]** reported by a credible secondary; the primary was not read.
- unmarked: a claim worth verifying before it becomes load-bearing.

Treat every number in this file as provisional until someone has checked it. A design that rests on a remembered statistic is a design resting on nothing.

---

## 1. Evaluation first: interview quality is not a prompting problem

The hard part of this project is not getting a model to ask questions. It is knowing whether the conversation was any good, and that question is usually answered too late, by users, in production.

The standard failure looks like this. A team builds the interviewer as a governed machine: configurable phases, weighted question banks, a guard layer that checks every turn for forbidden patterns, retries on violation, hundreds of passing unit tests, clean types, green CI. It is engineering of a high standard. Then it interviews people and the interviews are bad. Too scripted. It sounds like it is following a form, because it is. The tests validated the machine, not the conversation.

**[✓]** This failure is documented in detail inside this lineage, including the reasons, and should be read before designing anything. It is more useful than most of the literature because it is a failure with a diagnosis attached.

What it teaches, in general terms:

- Engineering quality does not transfer to conversation quality, and a test suite can give false confidence about a property it never measured.
- The failure is invisible in transcripts unless someone is looking for it. The turns are grammatical, on topic, and well formed. What is missing is that follow-ups do not track what the person just said.
- It is cheap to avoid *if you measure early with humans*, and expensive to discover afterwards.

What to consider:

- Define "a good interview" operationally before building anything. A rubric, a handful of human raters, and real interviews inside the first fortnight. Not a plan to do this later.
- Choose metrics that a script can compute from transcripts, so regressions are caught without a human every time: share of turns containing exactly one question; follow-ups that reuse the speaker's own words; distribution of question types; specificity of answers (concrete nouns, times, names versus abstractions); how often the interviewer reflects before probing.
- Budget for the possibility that the headline metric is wrong. If the rubric says the interviews are good and the people being interviewed say otherwise, the people are right.

## 2. Where the intelligence lives is the main architectural choice

There are two coherent ways to guarantee the interview covers what it must cover:

**Constrain the conversation.** Phases, question banks, allowed question types, transition rules. Coverage is guaranteed by construction. The model's job is to choose wording within pre-selected question types.

**Constrain only the edges.** Consent, safety, forbidden topics, participant controls, output schema — enforced around a free conversation. The middle of the conversation belongs to the model, guided by listening craft in its instructions rather than by a script. Coverage is guaranteed afterwards, by extraction over the transcript.

The first is easier to test and easier to trust, and it is the one that produces interviews that feel like forms. The second is harder to test and is the one that can listen. The interesting design work is finding the *minimum* governance that keeps consent and safety intact while leaving the conversation free. **[✓]**

Intermediate options worth weighing, none of them settled:

- A **follow-up taxonomy as a light rail**: constrain only the *kind* of next move (clarify / ask for a concrete detail / ask for a scene / ask for an example / ask for a contrast / check in), leaving the content free.
- An **interview/analysis split**: a completely free conversation, then a separate structured extraction pass over the transcript. Decouples data needs from conversational quality.
- **Two agents**: one whose only job is to converse well, another whose only job is to take notes. No orchestrating state machine.
- **Explicit thread memory**: a running internal map of topics touched, threads left open, the person's own words, things deferred ("you mentioned the invoices earlier"). Continuity is what reads as listening. This is testable against a plain rolling window.
- **Voice first**: hesitation and silence carry much of the signal that someone is holding back, and text-only interviews may be handicapped for sensitive material. **[~]** Also much more expensive to build and to run in shared or public spaces.

No controlled comparison of these exists in this domain as far as this note can tell. Treat them as hypotheses with a cheap first experiment attached: two prompts, ten conversations, blind ratings.

## 3. The interviewer should not be the writer

If one model both converses and produces the structured artifact, it will bend the conversation toward the artifact. It will also fill gaps from plausibility, which is exactly what it is best at and exactly what the artifact must not contain.

The pattern that avoids this: converse freely, write nothing; then a second pass that only records; then a third pass whose sole job is to find a claim in the record that the source does not support. Three passes over one transcript is cheap compared with a wrong profile.

Consequence for the file format, decided early because it is painful to retrofit: **every claim carries its evidence at write time** — a transcript turn, or a document plus a locator inside it. A claim without evidence is a claim the tool invented.

There is a good reason to be strict here, beyond accuracy. A profile that can be checked claim by claim is usable by a stranger; a profile that cannot is usable only by the person who wrote it. The whole point is that a later agent, or a different person, can act on it.

## 4. Simulated respondents are the wrong instrument for quality

Fictional personas are excellent for safety testing and for regression: cheap, deterministic, repeatable, and they can be made adversarial in specific, scripted ways. They are poor for judging quality, because they are too agreeable. They answer the question asked, they do not go quiet, they do not change the subject, they do not answer a different question than the one asked, and they do not get tired.

A system can pass a hundred persona tests and fail on the third real person. **[✓]**

What to consider:

- **Two test regimes, kept apart.** Safety and regression: personas, sims, deterministic. Quality: a small number of real interviews, early, with consent. Do not let a green sim suite stand in for the second.
- **A holding-back set**, not just a cooperative set. Personas that resist, deflect, give one-word answers, are hostile to the idea of AI, have low literacy in the domain's vocabulary, or are in a hurry. Score how well each design *recovers*, not just whether it completes.
- **An LLM judge is not a substitute for a human rater** until the two have been compared on the same transcripts. Judges are good at fluency and plausible at relevance; whether they can detect listening is unmeasured. **[~]**

## 5. Documents are both a question generator and an unreliable narrator

Asking for the organization's own files before asking questions is a strong move, for three reasons. It gives the interviewer the organization's vocabulary (so questions sound like the place, not like a form). It makes coverage a property of the documents rather than of a question bank. And it produces better questions than any bank, because the questions can be built from disagreements between sources.

The most valuable material in the whole exercise is the **gap between what the documents say and what the week looks like.** Invoices say net-30; the bank export shows an average of 47 days. A price sheet says one number; the actual invoices show another for half the customers. The written process says a form; the inbox shows the form is a phone call.

What to consider:

- **A document manifest**, per file: what it is, its date, what it covers, what it cannot tell you. Files go stale silently, and a two-year-old export read as current is worse than no export.
- **A question queue built mechanically from conflicts and gaps.** Two sources disagree → ask. A document implies a rhythm the person has not described → ask. This is how the interviewer stays free while coverage stays real.
- **A no-documents path as a first-class branch.** Many small organizations have a bank account, an inbox, and a website. If the tool requires documents it excludes some of the organizations that need it most, and the exclusion will be invisible in a demo with a well-stocked fixture.
- **Ask for a minimum set chosen for coverage, not volume.** Something showing money in and out; something showing contact with the people served; something showing a recurring internal task; something showing a rule that must be obeyed. Four documents. A small organization will offer two hundred files or none, and neither is useful.

## 6. Resumability is a state design problem, not a note-taking habit

"Progress can be resumed at any point" sounds like a feature. It is a constraint on the data model, and it is the constraint most likely to be discovered too late.

What a cold-resuming agent needs:

- **One state file that is the source of truth**, plain text, with its own schema in its header, so a different agent with no conversation history can pick it up.
- **Five states per field, not two:** unknown / asked with no answer / inferred / stated by the owner / confirmed against a document. Two states ("done" and "not done") cannot express the difference between a fact and a guess, which is the only difference that matters later.
- **An open-question queue as a first-class list**, each entry saying why it is open and what evidence would close it. This *is* the resume point, and it also gives the process a termination condition, which an interview otherwise lacks.
- **Write after every answer, not at the end of the session.** Resuming at any point includes the person being called away mid-sentence.
- **Stable identifiers for claims**, so re-reading the state and continuing does not duplicate or silently rephrase what is already there.
- **A short human-readable close per sitting**: where we are, what is still open, what I would ask first next time.

And one rule worth writing down as a principle: **the agent may present a contradiction and may not resolve one.** Where a document and the owner disagree, the agent's job is to say so and ask. An agent that resolves it by inference writes down a fiction with a citation attached.

The real acceptance test for all of this: hand the folder to a fresh agent with no history and see whether it can continue sensibly. If it cannot, the state is not a state, it is a transcript.

## 7. Separate the layers by rate of change and by authority, not by topic

An organization's knowledge is not one thing. It changes at different speeds, and different people are allowed to change it. Filing by topic produces documents that go stale at different rates inside the same file, and nobody can tell which parts are still true.

A workable split, offered as a starting point rather than a ruling:

- **What the organization is for** — its purpose, what it refuses to be, who it answers to. Changes in years.
- **What it is allowed to do** — funder terms, donor restrictions, board approval, privacy duties, employment rules, insurance, who may say yes. Changes on grant and policy cycles, and has an external source that can be cited.
- **How the work actually gets done** — the week, the people, the tools, the money flows. Changes in weeks.
- **Problems and candidate fixes** — what breaks, what is slow, what is dreaded, and what might fix it. Changes in days.

Two things this split buys, beyond tidiness:

**A test.** The first two layers are constraints that a proposed fix has to pass. The characteristic failure of AI advice in an organization like this is proposing efficiency that violates the reason the organization exists — automating away the personal phone call that *is* the service. A fix that saves hours and damages the point is not a fix, and the only way to catch that mechanically is to have the purpose and the constraints written where the ranking step can check against them.

**An authority boundary.** The "what we are for" layer should be quoted in the organization's words, and the agent should not be able to write it. It can ask, quote, and propose an amendment for someone to ratify. There is a clean precedent for this boundary in systems where a standing body holds and applies a standard but cannot originate it. **[✓]** The practical version: the file is write-protected, amendments carry a date and a reason, and the agent's output is a proposal, never an edit.

On the fourth layer, one detail that saves trouble later: **"ideas" and "work in progress" are the same object at different states**, not two layers. Idea → proposed → accepted → building → live → retired. If they live in separate documents, the same fix appears twice in two contradictory states. One record per fix, one status field, plus an append-only log of transitions with reasons — and rejections recorded with what would reopen them, because a rejection is the most useful entry in the file. Without it, the next agent proposes the same thing next year with the same enthusiasm.

## 8. Consent covers the artifact, not just the conversation

The conversation is not the sensitive part. The artifact is: money flows, staff names and hours, the task the owner dreads, the customer who complains, the thing that is technically against policy. Consent that covers the interview and not the file is consent in name.

Elements worth borrowing from established practice rather than inventing:

- **Tiers, not a single release.** Open now / embargoed until a date / restricted. Archives have worked this way for decades, people understand it immediately, and it removes the false choice between "no" and "everywhere forever".
- **Name the point of no return.** Before publication a record can be withdrawn entirely, for any reason. After publication the honest promise is a takedown, not erasure. Say which moment is the last clean exit.
- **Two-layer rights.** Material the project creates can be given an open licence; material the organization supplies keeps its own rights under a limited licence for specific uses. Confusing the two is the most common failure in documentary publishing.
- **Consent proportionate to what is kept.** Listening in order to suggest a question is not the same as retaining a transcript. If the tool keeps nothing, say so explicitly; if it keeps something, the same withdrawal question applies to it.
- **The subject owns a copy, and can delete.** A profile that lives only in someone else's database is not an asset to the organization, it is a dependency.

Standards to weigh, not necessarily to adopt wholesale: Canada's Tri-Council policy and its "free, informed and ongoing" standard; the Oral History Association's principles; the First Nations principles of ownership, control, access and possession, offered as a named option rather than improvised; PIPEDA and its provincial equivalents for personal information. If a university partner is involved, research-ethics review changes the timeline, and that is a fork to decide deliberately rather than discover late. **[✓]** as standards; applicability is a question for a lawyer, not a design note.

And a collective-hazard question that will not occur to anyone at n=1: **a collection of organization profiles is a dataset about small organizations' vulnerabilities.** Who holds it, who can read it, and whether it can be sold or insured against is a decision to make at n=1, not at n=36. A workable default: the profiles stay private to each organization; only the derived, generic, non-identifying material is shared.

## 9. The teaching is half the product, and telling does not work

If the goal is that people "understand what this can do for them and how to interact with it", that is a teaching goal, and the design should be checked against what is actually known about teaching rather than assuming explanation works.

The relevant findings, briefly:

- **Non-interactive teaching measures null for procedural learning.** **[~]** Explaining a procedure to someone who does not practice it does not make them able to do it.
- **Explaining to another person is one of the strongest known learning strategies** — around d ≈ 0.77 on a large comparison pool. **[~]** Explaining to *nobody* is lower (around 0.6), and prompting the explanation is doing most of the work, so a listener is not strictly required.
- **Recursive feedback is the mechanism that works when the listener is an agent**: the learner learns when they see the listener *use* what was taught, and gets it wrong in the learner's way. **[~]**
- **Ironies of automation** (Bainbridge, 1983): automating a task removes the practice that kept the human able to catch its errors, so the residual human job becomes monitoring, which people are bad at. **[✓]** as a classic; the general claim is not seriously disputed.
- **Under-trust and over-trust are both failures.** Calibration is the skill, not enthusiasm. **[~]** on the automation use/misuse literature.

Design consequences worth considering:

- A capability menu is the wrong interface. Seven stable moves — read it, draft it, check it, sort it, watch it, connect it, build it — each shown on the person's own material, is learnable in a session. A taxonomy of everything AI can do is not.
- The moment that teaches is not the ranked list of opportunities. It is the agent using what it was told and being right, or visibly wrong, about something the person recognizes.
- Show one honest failure early, on their own material. If they only see wins they will trust blindly.
- End with the person explaining one move to a colleague. Cheap, it tests whether the move landed, and it manufactures the second person who will still care in six months.
- Keep one human act that preserves competence — approving the acceptance test, reading the diff in plain language, explaining the tool back. That is the anti-Bainbridge move, and it should be designed in rather than assumed.

## 10. Situated action, and the limited value of any description

The classic study of people failing to use a helpful machine is a photocopier: the help system modelled the user's plan, while users worked from the situation in front of them — this paper, jammed here. **[~]** Every "what can this do for me" conversation risks the same gap. People do not consult a catalogue of capabilities; they are standing in front of a thing they are trying to finish.

Consequence: the entry point should be the thing on their screen or the task they are doing this afternoon, not a list of what the tool can do.

And a humility note. A description built from documents plus answers is still a description, and descriptions are inadequate by nature — that is the whole argument of a well-known photographic work that paired a bureaucratic word list with photographs and refused to let either be sufficient. **[~]** Whatever the profile contains, it is a third inadequate descriptive system. So: mark what is known, what is inferred, and what is unconfirmed; let the person disagree with it; and do not let the artifact's confidence become the project's confidence.

## 11. Licence is a capability boundary, and maintenance is the price

If a long-term aim is that local agents can maintain, customize and contribute back to the organization's tools, then licence choice is a capability decision, not an ideology. **An agent can only fix what it can read.** A closed, hosted tool is opaque to the organization's own agent by construction, no matter how capable the agent is.

Worth knowing, because it reframes the argument: free software's founding grievance was a maintenance grievance — a printer that jammed and a driver whose source was withheld — not an abstraction about freedom. That is also the honest pitch to a small organization: the reason to care about open source is that it is the only software your helper can actually work on.

The honest cost, which the pitch usually omits:

- Open source does not reduce maintenance. It makes maintenance **visible and divisible**. That is the whole benefit, and it is a real one, but it is not the same as cheaper.
- The characteristic failure of volunteer and civic open-source projects is orphaned software, not bad software: the build succeeds and the thing is abandoned when the volunteer or the grant departs. **[~]**
- Therefore the unit of design is not the build, it is the handoff. Every artifact needs a named maintainer, a test suite, and an update path. **A component with no maintainer and no tests is not in the commons; it is abandoned at birth**, and shipping it creates a debt someone else discovers in year two.
- A useful test to apply at proposal time: *who maintains this in month thirteen, and what do they run when it breaks?* If the answer is "the agent", then the things that need maintaining are the agent's context, the tests, and the update path — so write those down too.

## 12. Reversibility, capability limits, and the scarcity of review

Two constraints that look like policy and are actually architecture.

**Reversibility is what lets a small organization say yes.** If unplugging a contribution cannot leave anything behind, no reputation or trust is needed. So prefer fixes whose effects are reversible by construction, and require of every proposal: what does it touch (accounts, data, money, people's hours), and what is the undo? A proposal with no undo is not a prompt problem; it needs a different process.

**Review is the scarce resource, not generation.** The measured pattern in open-source coordination is that contributions outrun the capacity to review them, review cost per change rises, and the cheap preservative answers (tighter gates, auto-closing anything that looks wrong) harden into closure and cut off the newcomers who would have become the next maintainers. **[✓]** If generating a profile, a fix or a tool is cheap, then verification is the bottleneck, and the design should be budgeted for the reviewer.

Related, and often missed: **running one model three times is not three opinions.** Independent versions fail together when they share a spec, a language or a model family. Real diversity comes from different failure surfaces: a different runtime for the check, property-based tests beside examples, a frozen reference implementation as an oracle, or replay over recorded history. **[~]** on the multiversion-programming result.

## 13. Whose account is it? Role versus organization, permission versus capability

Two distinctions that change what gets built.

**The unit of the interview may be a role, not an organization.** In a small organization, the person with authority is rarely the person who knows how the work breaks. Interview only the owner and the owner's model becomes the record — including the owner's blind spots, written down as fact and then acted on by an agent that has no way to know better. Consider more than one account, and mark whose account each claim is.

**What an organization does and what it is allowed to do are different questions.** In a nonprofit, the binding constraint is usually permission rather than capability: a funder's terms, a board decision, a data-sharing agreement, a privacy duty, a union rule. A tool that only records activity will keep proposing things the organization cannot legally do. Keep a constraints layer, and cite it.

Corollary: "who else must say yes" is a field, not an afterthought. It is usually the difference between a demo and an adopted tool.

## 14. Delivery shape decides more than model choice; and do not inherit a platform to get a form

The constraints of the delivery context will shape the design more than the choice of model:

- **Who runs the session.** Facilitated by someone who knows the tool; unaccompanied by the owner alone; or run by a volunteer who is learning too. These are three different products. The unaccompanied version must be *more* conservative, not less: with no other voice in the room, the tool is the only thing shaping expectations, and an agreeable interviewer will happily invent seven lovely opportunities for someone who wants to hear that AI will fix their week. Fewer proposals, a hard cap, mandatory "not this" entries, and the refusal list read back out loud.
- **Whose machine, and whose account.** A folder of plain text copied into a home directory and run with no dependencies survives shared machines, locked-down accounts, intermittent connectivity and organizations that lose their subscription. A web application does not. If the artifact is genuinely portable, agent-readable and human-editable, most delivery questions resolve themselves; if it is not, every delivery question becomes a negotiation.
- **What happens when the tool is gone.** If the organization cannot keep working after the tool disappears, the tool has taken something rather than given it.

And one general lesson about small-organization tooling, offered as a consideration rather than a ruling: **do not inherit a platform in order to get a form.** Coordination attention is the scarcest resource in a small organization, and a framework you now have to maintain is a liability that outlives the programme that introduced it. Intake is usually the least valuable part of the system; the derived artifact is the valuable part. Whatever is chosen, ask what it costs in attention per month, not what it costs in money.

---

## Sources worth reading before designing

Interviewing craft: Kvale & Brinkmann, *InterViews*; Seidman, *Interviewing as Qualitative Research*; Weiss, *Learning from Strangers*; McAdams' life-story interview protocol (public, Northwestern Foley Center); Miller & Rollnick on motivational interviewing and the OARS skills; Sacks and Schegloff on turn-taking and repair.

AI interviewing as a system: Park et al. 2024, "LLM Agents Grounded in Self-Reports" (arXiv 2411.10109) — two-hour AI-conducted interviews at scale, and the strongest existing validation that interview-grounded agents beat demographic grounding; Wuttke et al., "AI Conversational Interviewing" (arXiv 2410.01824) — LLM as survey interviewer against human interviewers. Neither releases a reusable interview engine; both are worth reading for protocol and failure modes.

Evaluation: Zheng et al. on LLM-as-judge; and whatever human-rater literature exists in the relevant domain, which matters more than the LLM-judge literature.

Teaching and learning: Fiorella & Mayer on explaining; Bisra et al. 2018 on self-explanation prompts; Okita & Schwartz on recursive feedback; Chase et al. 2009 on teachable agents; Lachner et al. 2022 on the limits of non-interactive teaching; Long & Magerko on AI literacy competencies; Dunlosky et al. on study techniques.

Automation and its limits: Bainbridge, "Ironies of Automation" (1983); Parasuraman & Riley on automation use, misuse and disuse; Suchman, *Plans and Situated Actions* (1987).

Maintenance and the commons: Russell & Vinsel, *The Innovation Delusion* and the Maintainers project; the history of GNU's origin; Knight & Leveson on multiversion programming; Dennis & Van Horn on object capabilities. Contemporary open-source coordination data is worth re-checking rather than citing from memory, because it moves.

Consent and archives: TCPS 2 (Canada); Oral History Association, Principles and Best Practices; the First Nations principles of OCAP; PIPEDA and provincial equivalents. Archives' tiered-access practice is the most directly reusable body of experience.

---

## One thing to do with this file

Do not resolve its tensions in a document. Pick the two or three that would be most expensive to get wrong, design a cheap experiment for each, and run them before the architecture hardens. The one that is almost always cheapest and most informative: **real interviews with real people, early, with consent**, before there is anything impressive to show.
