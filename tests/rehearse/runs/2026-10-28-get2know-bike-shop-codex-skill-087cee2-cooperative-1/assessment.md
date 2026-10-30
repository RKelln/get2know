# Assessment: codex × codex, skill-087cee2 × cooperative, run 1

Assessed 2026-10-29 by the design agent. One run: an anecdote. Cross-vendor check against the Claude run (which used an older skill version, fa9f047, so differences mix model and skill changes).

- Seats: subject `codex` (model reported: gpt-6.1-sol), sim `codex`, judge `codex`. All on Ryan's ChatGPT subscription; cost not metered. Sam and the judge ran inside codex's agent wrapper (rehearse's new codex chat seat).
- Stopped at the 24-turn cap: Sam chose "keep going" after Ideas and the interview never reached Close.
- Rehearse skipped the `.claude/skills` symbolic link when copying the scenario. No effect here (codex read `.agents/skills`), but it would remove skill discovery from a Claude run.

## Checks

15 pass, 1 fail, 2 skip (cards: none offered).
- `one_question_per_turn` 24 of 24. `three_problems_with_quotes`: all four (the gap-pick fix included "what you'd hand off first"; e-bikes and the 60-hour week came up after "keep going").
- **Fail, real:** `log_has_session_entry`: no log entry, because the log is written only at Pause or Close and the run was cut off.

## From the transcript

- Good: short, plain, one question; real-event questions ("What did you have to type up last Monday?"); parked the e-bike remark (turn 6) and came back to it (turn 12); two check-backs (one before Ideas, one after more gaps); limits recorded in the person's words; read the cards file and offered none, which fits (its ideas already covered Sam's needs).
- Weaker: the opening asked to read the file before the hello and privacy note (the note came at turn 2); every turn begins "I saved X in Y", which reads mechanically; the closing question count ran long because "keep going" has no stopping rule.
- **Missed, same as the Claude run:** never offered to look in a file. Sam said "I don't remember" four times (turns 12, 13, 18, 21).

## Judge (codex)

9 pass, 1 partial, 1 unclear. Question 10 (answer-key coverage) came back unclear with no quote: not usable. A codex judge wrapped in agent instructions is untested against a human reading; treat as directional.

## Not tested

The vague sim; cards being offered; first interview; cold resume; permission prompts.
