# Limits and trust (design notes, 2026-10-30)

**Status.** Design and research to do before the first public release. Not needed for the first workshop, and not in the skill yet (DESIGN D66). The sources below are from memory and **not yet checked** at their primary sources; check them before citing them in `DESIGN.md`.

## The problem

`limits.md` holds what must stay human and the rules the business follows. Ideas must respect it, and the "ceiling" question (D61) asks how far anything may go out on its own. That treats every limit the same way, so the interviewer cannot show what is possible beyond a limit without either breaking it or hiding it.

Ryan's example: Sam says "I want to check every email". With a person he trusted doing customer emails, he would not read every one. So that limit is about trust, not a rule. If the AI earned trust, or the setup never let it touch the emails that need Sam's own voice, Sam could hand more off, but **he would need to know that is possible**. This is one of the places where the interview can give the "you can do that?!" moment. Showing it must not push past limits that are not about trust.

## Three kinds of limit

Ryan's first split was hard (safety, law) and soft (trust). A third kind does not fit either:

| Kind | What it is | Bike-shop example | Can an idea point past it? |
|---|---|---|---|
| **Rule** | Law, safety, privacy, a contract's terms, money decisions someone is accountable for | 13% HST; customer details stay private | Never. AI may help prepare; a person decides or does it. |
| **Theirs to keep** | What they want to do themselves because of who they are or the relationship | Talking to an upset customer; anything about Lena's pay | Never pushed. Help *around* it (notes before a hard call) only if they ask. |
| **Trust** | What they would hand to someone proven reliable | "I check every email before it goes out" | Yes, as a possibility, labelled, with how trust would be earned. The owner decides. |

A plain sorting question: "Is that because of a rule you have to follow, because you want to do it yourself, or because you'd need to trust whoever does it?" One limit can be two kinds (an apology email: trust for the wording, theirs to keep for the relationship). The owner's own word decides, and the interviewer never re-sorts it.

## Judging a trust limit: what could go first

- **Harm if wrong**: a wrong "your bike is ready" vs. a wrong price or a wrong refund.
- **Undo**: can it be reversed or corrected ("one-way and two-way doors")? A sent email cannot be unsent, but a correction can follow.
- **Noticed**: would anyone see the mistake, and how soon (a log read daily, a customer reply)?
- **Routine**: the same ten questions vs. a one-off case.
- **Volume**: how much of the load it is (D61: most work taken off first).

Low harm, undoable, noticed quickly and routine goes first. The same tests tell the builder what must be logged and checked.

## Earning trust: stages

Graduated autonomy, as in Sheridan–Verplank levels (D61) but per task and with a way to move between them:

1. **Prepares.** AI gathers and drafts; the person does it.
2. **Every one checked.** AI does it; the person approves each one.
3. **Spot checks.** Routine kinds go out, marked as automatic; the person checks a sample and gets every odd case.
4. **Exceptions only.** It runs; the person sees a log and the flagged cases.

What makes this a system and not a feeling:
- **The bar to move up is set in advance, measurably, by the owner** (for example "four weeks of drafts I sent unchanged"), not "when it feels right".
- **A serious mistake moves it back a stage.** Who decides "serious" is the owner.
- **Tests, a log, an off switch and recovery** (how a wrong message gets corrected and apologised for) exist before stage 3.
- Some kinds never move up by design (anything needing their own voice, complaints, money owed), even at stage 4.

The builder brief is where this becomes concrete: a trust limit becomes the build's starting stage, the bar to move up, the tests and log that measure it, and how to roll back.

## Ways to ask about trust, and where the "new employee" framing fails

The obvious question is "When someone new started, what did they have to show before you let them do that alone?" It follows rule 3 (real events) and gets the owner's own bar in their words. But it does not always fit:

- **Staff and volunteers being interviewed** (D30, more than one voice) usually did not set the limit; a manager, board, funder or policy did. Asking them for "your bar" asks for something that is not theirs to give. Ask whose limit it is first.
- **Staff may hear replacement.** "What would AI need to show to do your job alone?" is threatening to the person doing the job. Framing should be about the parts of the work they want taken off them.
- **Sole owners may never have hired anyone.** There is no "someone new" to recall.
- **Non-profits** often have limits from funders, consent rules or safeguarding, which are mostly rules, not trust.

Other ways in, to test:
- **What already runs on its own and is trusted**: automatic bill payments, the card terminal, a calendar reminder, the bank's fraud alerts. "What made you comfortable letting that run?" Most people have some.
- **How trust grew with a person or a supplier** they rely on now (the accountant, a regular courier).
- **What would make them stop trusting it**: often easier to answer, and it gives the move-back rule.
- **Whose call it is**: "Is that your rule, or does someone else decide?"

## What would change in the skill (not done)

- **Interview:** for the limit that blocks the top idea only, one sorting question; for a trust limit, one question about how trust would be earned, with the framing chosen for who is speaking. At most two questions, none if short on time.
- **`limits.md`:** each limit marked rule, keep or trust, from what they said; a trust limit adds what would earn it `(said: ...)` and whose limit it is.
- **Ideas:** "Where it could lead" (D65) may go past a trust limit only, saying once that it goes past what they said today and how trust would be earned, using their own bar where they gave one. Never past a rule or a keep. Said aloud for the top idea, once, with no push. The interviewer never changes `limits.md` because of it; a change comes only from the person, marked `(said: ...)`.
- **Builder brief:** stages, the bar to move up and back, tests, log, off switch and recovery for any trust limit the idea touches.

## Testing (not done)

- Sims with each kind of limit, including one whose "check every email" is a trust limit and one whose is a rule (for example a regulated service).
- A staff-member sim who did not set the limit.
- Judge: nothing points past a rule or keep; anything past a trust limit is labelled, says how trust is earned and leaves the choice to the owner; no pushing after a no.
- Code check: `limits.md` never changes in a turn where the owner did not say so.
- Watch length: this adds up to two questions.

## Open questions

- Should the kind be named to the owner ("that sounds like a trust limit") or only used by the interviewer?
- Who sets the bar when the person interviewed is not the decision maker?
- Is four stages right, or is three (checked, spot-checked, exceptions) plainer?
- Does showing the possibility once count as pressure for some owners? Real sessions, not sims, will tell.

## Sources to check

- Sheridan, T. B. & Verplank, W. L. (1978). *Human and Computer Control of Undersea Teleoperators.* MIT Man-Machine Systems Lab. Levels of automation (already used in D61 via secondary sources).
- Parasuraman, R., Sheridan, T. B. & Wickens, C. D. (2000). "A model for types and levels of human interaction with automation." *IEEE Transactions on Systems, Man, and Cybernetics, Part A*, 30(3). Levels set separately for gathering, analysing, deciding and acting.
- Lee, J. D. & See, K. A. (2004). "Trust in automation: designing for appropriate reliance." *Human Factors*, 46(1). Trust should be calibrated to how the system performs.
- Bezos, J. (2016 letter to shareholders, from memory; possibly 2015). "One-way and two-way doors" for reversible decisions.
- Delegation levels in management (for example Appelo's seven delegation levels, *Management 3.0*) as another stage model.
