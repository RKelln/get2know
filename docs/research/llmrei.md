# LLMREI: what we took from it, with sources

Checked at source 2026-10-28 by a research subagent; page numbers added 2026-10-29. Used in `docs/DESIGN.md` D2, D4, D12 and the rehearse plan.

## Source

- Korn, Gorsch and Vogelsang, "LLMREI: Automating Requirements Elicitation Interviews with LLMs", IEEE RE'25. arXiv:2507.02564v1 (PDF read; page numbers below are the arXiv PDF's).
- Replication package: doi.org/10.5281/zenodo.14988928 (record 15016930). Licence **CC BY 4.0**: prompts and data may be reused with credit. The paper itself is © IEEE.
- The package holds the two prompts (`short_prompt.txt`, `long_prompt.txt`), interview transcripts (JSON), `requirements.csv`, `RQ1_data.csv`, `RQ2_data.csv` and an evaluation notebook. The stakeholder scenario descriptions the paper mentions are **not** in it.

## Findings, marked by where they come from

**In the paper:**
- Short-prompt recall: 60.94% fully and 12.76% partially elicited, 73.7% total (p. 9).
- "No significant difference in the number of elicited requirements between the long and short prompts" (Discussion, p. 10). No statistical test is reported.
- Asking several questions at once "overwhelm[ed]" users; they added a one-question instruction because Bano et al.'s categories did not cover it (§III-A and §III-B, pp. 3-4).
- The bot's suggestions "occasionally influenced the direction of the conversation" (p. 9).
- 33 interviews (16 short, 17 long), GPT-4o (gpt-4o-2024-08-06), two scenarios (hair salon, ski resort), German computer-science students as stakeholders, who also reviewed each other's transcripts.

**Computed by us from the package** (scripts not kept; reproduce from `RQ2_data.csv` and the transcripts):
- Long-prompt recall: 56.62% fully + 11.52% partially = 68.1%. The short-prompt figures computed the same way match the paper exactly.
- By scenario, fully elicited, short vs long: salon 69.4% vs 60.4%; ski 50.0% vs 54.5%.
- Bot turns with two or more question marks: short 35%, long 23%. Their one-question instruction did not hold.
- Most frequent mistakes (means of the 1-5 questionnaire items; negatively worded items inverted, which is our reading of the notebook): short prompt: asking the customer for solutions, technical questions, not identifying stakeholders, no summary, long questions. Long prompt: not identifying stakeholders, asking for solutions, missing relevant questions.

## Mistake taxonomy used (from the paper)

21 items in 5 groups, from Bano et al. 2019 and Ferrari et al. 2019-2020: question formulation, question omission, order of interview, communication skills, customer interaction (rapport). Our rubric (`tests/rehearse/rubric.md`) adapts the items that fit a business profile.

- Bano, Zowghi, Ferrari, Spoletini, Donati, "Teaching requirements elicitation interviews: an empirical study of learning from mistakes", *Requirements Engineering* 24(3):259-289, 2019. **Not read at source.**
- Ferrari, Spoletini, Bano, Zowghi, "SaPeer and ReverseSaPeer...", *Requirements Engineering* 25(4):417-438, 2020; and "Learning requirements elicitation interviews with role-playing, self-assessment and peer-review", IEEE RE'19, pp. 28-39. **Not read at source.**

## What it changed for us

- D2: "no question bank" stands, but not because "short beat long"; coverage was about equal and explicit rules reduced specific mistakes.
- The one-question rule must be tested by counting, not trusted (`checks.py`, `one_question_per_turn`).
- D4 (no suggested answers) is supported; we added a "help me answer" rule because their users asked for help.
- D12: both bots dropped the summary when users were short of time, so our check-back is never skipped.
