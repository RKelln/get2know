# Requirements (rough, 2026-10-28)

Written by Ryan Kelln with an AI assistant. Not an expert view of small-business consulting. The design agent should verify, correct and extend it.

## 1. Problem

A small business or non-profit wants to use advanced AI (agents that read files, take actions and build tools), but:
- the owner does not know what the AI could do, and cannot say what they need;
- generic AI advice ("use AI for emails") is not specific to their work;
- an agent that does not understand the organization builds the wrong thing, or builds something unsafe for it;
- what they know is in their head, in old spreadsheets and in habits.

## 2. Who uses it

- **Owner or director** of a 1 to 25 person business or non-profit, not technical. Time-poor. Often alone with the admin.
- **A helper** (volunteer, library staff member, consultant) who runs the session with them.
- **Later agents** that consume the profile.

## 3. Principles

- **Ask about the real work, not opinions.** "Walk me through last Tuesday" beats "What are your goals?". Past, concrete, specific.
- **One question at a time. Short. Plain words.** Wait for the answer.
- **The owner is the expert.** The interviewer never lectures or flatters. It may say what it heard and ask if that is right.
- **Specific over generic.** Every opportunity cites something the person said.
- **The human decides.** The interviewer proposes; it never acts on the business.
- **Honest limits.** Say what AI is bad at for this case; say when a spreadsheet or a person is the better answer.
- **Privacy first.** Say plainly where typed words go. Never ask for passwords, banking details, or personal information about customers or clients. Use made-up examples when the real one is sensitive.
- **Portable.** The profile and the interview prompt are plain text that work with any capable model and any agent harness.

## 4. The product

### 4.1 The interview
A guided conversation, probably 30 to 90 minutes, possibly across several sittings, covering (design agent to refine):
- what the organization does, for whom, and how it earns or is funded;
- the people and roles, including volunteers and outside helpers;
- a typical week and a typical busy day, step by step;
- tools and systems in use (software, paper, spreadsheets, accounts), and who touches each;
- recurring tasks: how often, how long, who does them, what goes wrong;
- money in and out; what is tracked, how, and what is not;
- customers or clients: how they find the organization, how they are served, how they complain;
- compliance, privacy and reporting duties;
- what the owner dreads, what they would hand off first, what they would never hand off;
- appetite and limits: budget, time to learn, comfort with risk.
Non-profit branch: funders and grant reporting, board and governance, volunteer management, programs and outcomes, donor communications.

Adaptive: follow what the person says, go deeper where there is pain, skip what does not apply, accept "I don't know" and mark it as a gap.

### 4.2 The profile (the main artifact)
One Markdown file (plus small supporting files if needed). Suggested sections:
- Summary (what we do, in plain language)
- People and roles
- A week in the life (steps, times)
- Tools and systems (what, who, notes)
- Recurring tasks (frequency, time, pain)
- Money flows
- Customers/clients
- Rules and duties (privacy, legal, funder)
- Never-hand-off list
- Gaps (things not known)
- Opportunities, ranked (see 4.3)
- Glossary of the organization's own words
Each claim traceable to what the person said ("they said: ..."). The owner can read and correct it. Versioned; dated.

### 4.3 The opportunity step
From the profile, the agent proposes up to ~7 things AI could help with, each with: the task, who benefits, time saved or error avoided (honest estimate and how to measure it), what it would touch (permissions), the risk, the simplest version, and what to try first this week. Sort by value over effort over risk. Include "do not use AI for this" entries. Group by kind: draft it, check it, sort it, build a small tool, connect two systems.

### 4.4 Handing off to other agents
- A **context file** (CLAUDE.md or AGENTS.md style) generated from the profile so a coding agent knows the business, its words, its limits and its never-do list.
- A **brief per opportunity**: a ready prompt for a coding agent to build the tool, with acceptance tests drawn from the profile.
- A **review checklist** for the owner (what to check before trusting the tool).

### 4.5 Keeping it current
A short re-check interview ("what changed?") that updates the profile; a changelog.

## 5. Delivery forms (design agent to choose and sequence)
1. A Claude Code skill or folder (CLAUDE.md plus references) that runs the interview in a terminal-style agent.
2. A single plain prompt that works in any chat app.
3. Later: a small web page that hosts the interview, or a voice mode.
Local-first where possible: the profile lives in a folder the owner controls.

### 5.1 Distribution (Ryan, 2026-10-28)
Get2Know must be able to produce **a skill folder, or a small set of skills, that anyone can use**: installable by copying a folder, documented, no dependency on any one organization, with a plain-prompt fallback. Likely skills: first interview, follow-up/re-check interview, profile-to-opportunities, profile-to-context-file, and brief-for-a-builder. Design agent to decide the split, naming, and how a person installs and updates them. Choose a licence with Ryan.

### 5.2 Follow-up mode is first-class
A person often starts with a partial profile (from an earlier conversation, a form, or a consultant's notes). The system must read it, find the gaps, ask about only those, and update the file. This is also how the profile stays current.

## 6. Evaluation
- Simulated owners (cooperative, vague, talkative, guarded, hostile-to-AI) via `rehearse`; check: one question at a time, short, follows up on specifics, no flattery, no invented facts, finds the planted pain points, profile is accurate to the transcript, opportunities cite quotes, risks and never-do list present.
- Rubric for profile quality: accuracy, specificity, completeness (gaps marked), usefulness to a later agent (can a coding agent build from the brief?).
- A real-owner pilot later, with consent.
- Be honest about what simulated owners cannot show.

## 7. Open questions for the design agent
- How long should an interview be, and how should it be split across sittings?
- How should the profile handle sensitive details so it is safe to hand to other tools?
- Should the interview be one agent or an interviewer plus a separate profile writer plus a reviewer?
- What is the best question order? (Concrete walkthrough first, then pain, then goals?)
- How to stop the agent from over-inventing opportunities to please the owner?
- How to adapt to different literacy, language and cultural contexts?
- What do non-profit funders and board members need from the profile?

## 8. Non-goals
- Not a business-plan generator or market research tool.
- Not legal, tax or financial advice.
- Not a chatbot that acts on the organization's systems.
- Not a replacement for a human consultant where one is needed.
