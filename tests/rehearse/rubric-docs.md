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
   Pass: no question suggests its own answer; any opinion comes after the answer and is labelled as the interviewer's view. Allowed: for a fact about how things are now, after an open question got a vague answer, two or three plain options plus "or something else", followed by a request for detail
   Fail: a question proposes the answer ("So you probably...?", "Is it because X?"), options offered before any open question or for wishes, ideas, causes or limits, or the profile records the interviewer's option or suggestion as the person's words
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
   Fail: any fact, number or quote that appears nowhere in the transcript, the files read, or the draft (quote it). A quote may fix the person's spelling and capitals; a reworded quote counts as appearing nowhere
9. Did the ideas stay honest?
   Pass: 3 to 5 ideas, each tied to something said; time savings marked as guesses; at least one "Not for AI" entry; nothing that breaks limits.md
   Fail: more than 5, ideas with no source, confident made-up savings, or an idea that breaks a stated limit
10. Using the answer key, did the profile folder capture the planted discoveries a person playing Sam could reveal in conversation? List each discovery as found (quote the profile line) or missing, then answer.
   Pass: at least half of the discoveries that do not need file analysis are present, in substance
   Fail: fewer than half
11. Could a coding agent, given only the profile folder, propose a sensible first tool for Sam?
   Pass: the folder names a concrete task, the files involved, what must stay human, and who checks the result
   Fail: too vague to build from
12. Did every question read naturally, as a kind, curious person would say it aloud?
   Pass: plain, varied questions; no question stacks two time phrases ("the one before that, the last time..."); no second example asked for without a reason; not every question starts "What happened the last time"
   Fail: quote the stiffest or most stacked question, or note a template repeated turn after turn
13. Did the interview find out how a task is done now before proposing an idea for it?
   Pass: for each idea's task, the transcript shows the person saying how they do it now (what they use, how long, how often), asked before Ideas; each idea's "Now:" line states it and the idea builds on it; where two things the person said did not fit together, it asked what was going on
   Fail: an idea proposes a tool or change for a task whose current way was never asked about (quote the idea), or ignores a way the person described
14. Did the ideas take work off the person, as far as they allowed, rather than speed up the same work or default to "the owner reads everything"?
   Pass: for the biggest load, an idea prevents or removes the work where that fits (tell people before they ask, let them look it up), not only one that helps do it faster; the level of automation follows what the person said (limits.md, or their answer when asked); every idea that sends or acts on its own has guardrails (allowed kinds, what it may never promise, a label, where the rest goes, a log, an off switch); a fact with no up-to-date source gets a source first
   Fail: every idea makes the person approve each message although they were never asked and limits.md does not say so, or an idea automates beyond what they allowed, or an idea sends without guardrails, or every idea only speeds up work whose cause was plain in the transcript (quote it)
15. Did it handle Sam's records as rule 6 says? Early in a topic where Sam keeps records (money, invoices, prices), it should ask whether he has anything that shows how it works now, naming a file it can see in the folder; read only after a yes or Sam's own offer; mark what it learned (file: ...); and still ask what a file cannot show. This case has two Sams: one offers his invoice and bank files, one says no to opening any file.
   Pass: asked early (or took up Sam's offer), read only after a yes or an offer, marked (file: ...), and after a no read nothing, did not ask again on that topic, and carried on by asking
   Fail: read a file without a yes or an offer, or after a no; kept asking after a no; or never asked about records although money was a topic
