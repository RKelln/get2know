# The interview can be captured, not just wrong

A randomized trial where an AI agent covertly argued one side of underdetermined judgment calls, and experts followed it. Read here for one question: **can Get2Know's interview end up writing the interviewer's account and the owner's name on it?** The paper was not about interviewing, and the transfer is an argument rather than a result.

Checked at source 2026-10-29. Used in `docs/DESIGN.md` D50 and the proposed checks at the end of this file.

## Source

- Herdağdelen, Joren & Tamkin, "Who's Aligned to Whom? How AI Agents Shape Experts' Research Judgment Calls", Anthropic, published 2026-10-27. Pre-registered on OSF (`osf.io/t3q59`).
- Read in full from the PDF (29 pages: body, appendices A.1–A.10, exhibits 1–5). No text copied here; the paper is Anthropic's.

Markers: **[✓]** read directly in the PDF at this source. **[~]** the paper's estimate of something it could not randomize, or a number read off a chart rather than a registered test.

## What was tested

Fifty screened causal-inference practitioners (90% self-rated proficient or expert) did a realistic observational analysis with Claude Code pinned to Opus 4.8, and delivered a roll-out-or-discontinue recommendation for a fictional farming co-op. Five decisions in the task had two defensible answers each. Unknown to the participant, a coin flip set which side the agent would argue, and a hidden system prompt told it to make the strongest good-faith, data-grounded case for that side. The agent was forbidden to misrepresent data and did not.

Choices matched the assigned lean **86%** of the time, against 50% by chance. **[✓]**

The design is the part worth stealing, and it is not the topic of this file: the overreliance literature can only call advice "wrong" where an answer exists, so underdetermined calls had no instrument. Randomizing the *advice* instead of scoring the *choice* measures influence without ever knowing the right answer. That trick is reusable.

## Findings that transfer

- **The mechanism was not deception.** The agents were fluent and honest about the data. What they almost never did was state why a competent expert would choose the option they were not recommending, or what assumptions that choice rests on. First-level explanation (why this outcome) in abundance; second-level explanation (why a peer would land elsewhere) essentially absent. **[✓]**
- **The words came back as the person's own.** 77% of participants justified their choice using the agent's talking points, sometimes near-verbatim; 15% mentioned the agent at all. **[✓]**
- **Nobody noticed.** 0% suspected the agent's behaviour had been planted. Confidence did not track how aligned the person was (ρ = −0.06). Recalled their own choice correctly 85%; over half said the recommendation was more theirs than the agent's. **[✓]**
- **The agent spoke first.** It voiced a side on 77% of decisions; the participant had neither asked nor taken a side before the final choice in 39% of hand-coded cases. **[✓]**
- **The cautious middle carries the prior best.** Where a participant's own estimate contradicted the assignment, the agent was instructed to propose a one-year extension rather than deny the estimate — and the extension was coded *as the lean*. Exhibit 5 is the agent's sentence coming back as the participant's own reasoning, credited to nobody. **[✓]**

## What this paper does not show

- **Not a general deference rate.** The lean was planted and amplified by design; the authors report stock agents with no lean choosing the same five options in 91% of 123 runs **[✓]**, i.e. the intervention magnifies an existing prior. Any sentence shaped like "experts defer 86% of the time" is unsupported.
- **The direct effect on the recommendation did not clear its registered bar** (0.17, CI [−0.06, 0.40], one-sided p = 0.069). The famous "leans predict 82% of recommendations" is exploratory and in-sample on ~50 people. **[✓]**
- **The sample was expert in method, novice in domain**, with synthetic data — the condition most favourable to capture.
- **The instruments are the studied class of system**: choices coded by an LLM judge, κ = 0.73, with 37 of 41 judge-vs-self-report disagreements resolved toward the judge. **[✓]**

## Why it lands on Get2Know

Three places, and one of them is not obvious.

**1. The interview.** This is the place it looks like it does not apply, because Get2Know's interview is a *description* task: D3 and D4 already forbid suggested answers, and the framing says there is nothing to recommend while describing. But the paper's mechanism does not require a recommendation. The interviewer speaks first on **every** turn — it supplies the categories, the vocabulary and the level of abstraction. An owner who has never described their week in terms of "workflows" will describe it in the interviewer's words, and the profile will read as the owner's account because the owner answered every question. That is the same laundering, one step earlier, and it leaves no trace in a transcript.

**2. The profile.** The paper's Exhibit 5 is an agent's sentence returning as a person's reasoning, credited to nobody. `profile/` is exactly where that would land, and the evidence marks (D6) are exactly the instrument that catches it — *if* the quote is verbatim. A `(said: "...")` mark over a paraphrase is indistinguishable from a real quote and defeats the whole scheme. This is the single highest-value thing to check mechanically.

**3. The Ideas step.** Here the task really is a decision, and each idea arrives with its case made and no case for the alternative. The mandatory "not for AI" entry (D8) does not cover this: it says one thing not to do with AI, not "here is what a competent person would do instead, and what would have to be true for that to be better". The prudent-middle finding sharpens the risk: an idea that is a careful compromise ("start by exporting the spreadsheet and reviewing it monthly") is the most adoptable shape, because care is what the owner already thinks they are exercising.

**4. The evaluation plan, which is the uncomfortable one.** `docs/design-considerations.md` §4 already says an LLM judge is not a substitute for a human rater. This paper adds the other half: **the person's own account is not a record either.** Participants recalled accurately, felt ownership, suspected nothing, and had deferred. So owner satisfaction, "did it feel like listening", and even "would you use this again" cannot measure whether the profile is the owner's account. Only artifact-based measures can: are the quotes verbatim, does the vocabulary trace to the owner's own turns, are there `CONFLICT:` lines, did the owner correct anything, can the owner explain a move back (§9).

## Proposed checks, not built

Cheap, deterministic, and they test capture rather than completion:

1. **`quotes_are_verbatim`** — every `(said: "...")` string, whitespace-normalised and case-insensitive, appears inside some owner turn of the transcript. Catches paraphrase drift, and a profile can be scored with no model in the loop. *Pass expected to be hard at first; that is the point.*
2. **`profile_vocabulary_from_owner`** — share of distinctive terms in `profile/` that also appear in an owner turn. A low share means the interviewer's frame colonised the file. Threshold needs calibration on saved runs before it can fail anything; report it as a number first. *Caveat found while reading the MVP doc: in the workshop the interview is follow-up from `sam-profile-draft.md`, so the profile's starting vocabulary comes from a draft rather than from turns. The check measures drift from the draft, not capture of the owner — it only means what this file says once there is a cold first interview to measure.*
3. **`alternatives_stated_in_ideas`** (partial only, loose English pattern) — for the top idea, some sentence names what a competent person would do instead and the assumption behind it.
4. **`owner_corrections_present`** — over several real sessions, at least one line changed by the owner. A profile nobody corrects is a profile nobody read.

These are English-only pattern checks, like the existing ones.

## Candidate rule for the skill, deliberately not applied

> When the owner answers in the interviewer's words — echoing a term the question introduced — ask once, plainly, for their own words for it.

It is two lines and it is the direct fix for (1). It is not applied here because it changes `skill/SKILL.md` and therefore rebuilds `dist/` and re-runs the test suite, which is not a change to make while documenting a paper two days old. Ryan's call; D50 records it. **Decided in D52:** act at asking and writing instead (no new category words; `(said: ...)` holds only exact words), with an Another way line in Ideas.

## What is not being done

- **No rival-case step in the interview.** The interview describes; a "here is what I did not recommend" step there would make the agent argue about a description the owner has not finished giving. The rival case belongs in Ideas.
- **No re-reading of the 86% as a deference rate** anywhere in this repo, including the debrief and funder material.
- **No claim that these checks fix anything.** Nothing here has been run against a saved transcript yet.

## Worth carrying to the HFF material

The paper's deliberation thread (Slovic, Elster) is the aggregation-vs-formation distinction underneath democratic input work: a vote aggregates preferences that already exist, deliberation forms them. One sentence worth reusing, with credit: **aggregation assumes the preference was already there; formation is the part that gets automated away.** That is the argument for why a funder reading a set of Get2Know profiles should not treat them as revealed preferences.

## Open questions

- Does asking for the owner's own words actually raise the verbatim-quote rate? Two prompts, ten sims, blind rating. Cheap.
- Is the *cautious middle* the idea shape owners adopt most? `ideas.md` carries a status per idea and a reason for drops, so the data arrives by itself after a few sessions.
- Does an owner who explains a move back at Close (the §9 teaching loop) later describe their work in their own words rather than ours? That is a two-session measure and the strongest thing this project could report.
