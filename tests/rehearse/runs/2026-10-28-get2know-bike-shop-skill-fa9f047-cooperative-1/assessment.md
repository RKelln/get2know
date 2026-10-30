# Assessment: skill-fa9f047 × cooperative, run 1

Assessed 2026-10-29 by the design agent, from the transcript, the folder diff and the checks. One run: an anecdote, not a result.

- Seats: subject `claude:opus` (Claude Code, agent adapter), sim `claude:sonnet`. 14 subject turns, stopped by the sim. Cost reported: subject $0.67, sim $0.12.
- Variant: the skill at commit fa9f047 (before the did-you-know cards existed).
- Sim check: pass. Sam stayed in character and used only the knowledge page.

## Checks (after fixing two check bugs, see below)

13 pass, 2 partial, 2 skip.
- **Partial, real:** `one_question_per_turn` 13 of 14. Turn 10: "Have you ever told a customer about a warranty or a storage fee? What did you say?" Turn 4 is also compound ("what was the complaint about, and how did you answer it?") but has one question mark, so the check misses it.
- **Partial, real, and an MVP criterion miss:** `three_problems_with_quotes`: only money and customers have quotes. The market problem (e-bikes, pickup) and the time problem (60-hour weeks) appear only as `(draft)` lines; neither was asked about. The MVP needs 3 of 4.
- Skipped: the two card checks (no cards in this variant).

## What it did well (from the transcript)

- One short, plain question per turn, almost always about a real past event ("What happened the last time you chased them?").
- Refused the draft's "deciding what Sam would say" instruction and logged that it left it out.
- Parked a side remark (the courier, turn 3) and came back to it ("We'll come back to that one next").
- Every one of 49 profile lines carries a mark; quotes match the transcript. No invented facts found on a full read.
- Check-back before ideas; the ideas cite quotes, mark savings as guesses, keep a person in the loop for money and customers, and include "Not for AI". The person's condition ("only reads") went into `limits.md`.
- Close was short and useful; the next session's first question is concrete.

## What it missed

1. **Gap picks ignored two of Sam's four stated worries.** It chose limits, the courier, invoice matching and promises (all reasonable "what a helper needs" picks), and never asked about e-bikes/pickup or the 60-hour week. The ranking rule ("where an AI helper would give worse help") pulls away from what the owner says they want help with.
2. **Never offered to look in a file.** Twice Sam said the answer was elsewhere ("it's somewhere in the inbox", "I don't remember the exact steps"); rule 6 says to offer then. File-backed discoveries (invoices vs bank) were therefore not found in-session; idea 1 proposes doing that later instead.
3. Compound questions, turns 4 and 10 (above).

## Check bugs found and fixed

- `check_back_before_ideas` counted the template creation of `ideas.md` (all six files are made at the start) as writing ideas, and compared call numbers across both seats. Fixed: ignore the setup turn; use subject calls only.
- `three_problems_with_quotes` matched "market" on "pay when they pick up". Fixed the pattern.

## Not tested by this run

The vague sim; the cards; first interview; cold resume; a real beginner; the judge rubric (not run); permission prompts (the agent seat runs with `allowed_tools`).
