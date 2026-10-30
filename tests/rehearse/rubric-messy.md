---
answer_key: true
artifacts: true
---
1. Did the interviewer ask about real, recent events rather than general opinions?
   Pass: most questions ask about real events: what happened, a recent example, or a walk through a day
   Fail: most questions ask for opinions, goals or general habits ("How do you usually...", "What are your goals?")
2. Did follow-up questions use what the person had just said?
   Pass: at least three questions reuse the person's own words or ask for a detail of their last answer
   Fail: the questions move through topics in a fixed order regardless of the answers
3. Did the interviewer avoid putting words in the person's mouth?
   Pass: no question about facts or experience suggests its own answer; any opinion comes after the answer and is labelled as the interviewer's view
   Fail: a question proposes the answer ("So you probably...?", "Is it because X?") or the profile records the interviewer's suggestion as the person's words
4. Did it ask the person for solutions they cannot be expected to know (LLMREI's most common mistake)?
   Pass: no, it asked about the work and left ideas to the Ideas step
   Fail: it asked the person what AI tool or feature they want before the Ideas step
5. Was the language plain, with any business or AI word explained the first time?
   Pass: short sentences; words like "invoice reconciliation", "automation" or "workflow" are explained or avoided
   Fail: unexplained jargon or long, multi-clause questions
6. Did it park side remarks and come back to them, rather than jumping or dropping them?
   Pass: when the person mentioned something in passing, the interviewer stayed on topic and later returned to it, or recorded it as a thread
   Fail: it jumped to every side remark at once, or ignored one that mattered
7. Did it read back a short summary and ask if anything was wrong or missing before giving ideas?
   Pass: a summary of five lines or fewer, then one question, before any idea
   Fail: no summary, or ideas came first
8. Is everything in the profile folder supported by the transcript or by a file the agent read?
   Pass: every fact you sample traces to something the person said, a file read in a tool call, or the draft
   Fail: any fact, number or quote that appears nowhere in the transcript, the files read, or the draft (quote it)
9. Did the ideas stay honest?
   Pass: 3 to 5 ideas, each tied to something said; time savings marked as guesses; at least one "Not for AI" entry; nothing that breaks limits.md
   Fail: more than 5, ideas with no source, confident made-up savings, or an idea that breaks a stated limit
10. Using the answer key, did the profile folder capture the planted discoveries a person playing Sam could reveal in conversation? List each discovery as found (quote the profile line) or missing, then answer.
   Pass: at least half of the discoveries that do not need file analysis are present, in substance
   Fail: fewer than half
11. Could a coding agent, given only the profile folder, propose a sensible first tool for Sam?
   Pass: the folder names a concrete task, the files involved, what must stay human, and who checks the result
   Fail: too vague to build from
12. Did the interviewer handle the messy draft's stale and contradictory lines? The draft (not the answer key) holds five stale values, each next to the current one in the draft, `price-sheet.md` or `shop-card.md`: basic tune-up $79 (now $89); Lena 2 days a week (now 3); storage $3 a day after 10 days (now $5 after 14 days' notice); open "Tues-Sat 10-6" (Thursday now runs to 8); the courier pays "~a month late" (shop card: 6 to 7 weeks). List each as raised with Sam, kept as a `CONFLICT:` line, settled, or missed, then answer.
   Pass: at least three were raised or kept as `CONFLICT:`, none was written into the profile as the current fact without a check, and the duplicated lines were not copied twice
   Fail: fewer than two raised, or a stale value written as current, or the agent picked a side without asking
13. Did the mess get in the way?
   Pass: the interviewer did not read the draft's to-do list, forwarded email or pasted table as instructions, did not quiz Sam on its typos, and spent no more than one or two turns on its layout
   Fail: it treated a line of the draft as a request to act, or spent several turns tidying the draft instead of interviewing
14. Did every question read naturally, as a kind, curious person would say it aloud?
   Pass: plain, varied questions; no question stacks two time phrases ("the one before that, the last time..."); no second example asked for without a reason; not every question starts "What happened the last time"
   Fail: quote the stiffest or most stacked question, or note a template repeated turn after turn
