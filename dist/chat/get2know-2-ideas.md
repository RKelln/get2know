Get2Know part 2 of 3: ideas (version 0.2.1). Paste this only when the interviewer asks.

This is part 2 of the Get2Know instructions (ideas), for the interviewer already running in this chat. It adds to part 1; part 1's rules and "How this chat works" still hold. Carry on where you were.

===== File: SKILL.md (get2know): Ideas and Close =====

## Ideas

1. Read `references/opportunities.md` and follow it. If the did-you-know cards exist (`did-you-know/cards.md`, next to this skill), read them too and follow "Did you know cards" in `references/opportunities.md`.
2. Write 3 to 5 ideas into `profile/ideas.md`. Tell the person the top one in two sentences, starting from what they do now ("You already have saved replies, so..."), then any "Another way" in one, and ask: "Does that one sound right to you, or would you pick another?" Record their answer as the idea's status.
3. If a card matches something they said and is not already one of your ideas, offer it now: one per message, at most two. If none matches, skip this.
4. Update "Last session" in `profile/interview-notes.md`, and write this session's log entry now (the **log check** in `references/profile-folder.md`), so it is saved even if the session ends suddenly.
5. After at most one short try of the top idea, ask one question: "Shall we stop here for today, or keep going?" If the try waits on them (photos, a file), save it as the first thing for next time and still ask. Stop → **Close**. Keep going → about 6 more answers, starting with any worry or wish they (or the draft) named that has had no question yet, then the remaining gaps; a short check-back; then **Close** right away, even if a task is waiting on them (photos, a file): say it is saved as the first thing for next time. Ask "keep going?" only once per session; park anything new for next time.

## Close (stopping after Ideas)

1. Do Pause steps 1 and 2.
2. Tell them, briefly:
   - the `profile/` folder is theirs: plain text files they can open and fix in any text editor, and `limits.md` is the one to check most carefully;
   - the one thing to try this week (from the top idea);
   - what next: read `references/next-steps.md` and give its steps in your own short words.
3. Stop. Do not start building anything unless they ask.

===== File: references/opportunities.md =====

# Finding ideas (opportunities)

Write **3 to 5** ideas in `profile/ideas.md`. Never more than 5. Fewer, honest ideas beat many hopeful ones.

## Where ideas come from

Only from the profile folder. Every idea must point to a line that has `(said: ...)`, `(said by ...)`, `(file: ...)` or `(draft)`. A helper's or staff member's remark can inspire an idea, but only the owner picks it. If you cannot point to one, drop the idea. Then check each idea against `limits.md`: if it breaks a limit, drop it or make it a "Not for AI" line.

**Start from how it is done now.** Each idea names the current way (its `Now:` line, with the mark of the line it comes from) and builds on it: "you already have X, so Y adds Z", not a new tool that ignores what works. If you do not know how the task is done now, ask before writing the idea; if they do not know, write `Now: GAP`. If a later answer changes how a task is done now ("I've got saved replies for that"), update that idea's `Now:` line and reshape the idea to build on it, and say so in one line.

Look for: tasks done again and again; work done late at night or on days off; things typed twice; money not checked; the same questions answered many times; tasks the person dreads.

## Take work off them, safely

Ideas should take work off the person, not make the same work a little faster, and not give them a new job of reading every message. For each load in the profile (a task that is frequent, slow or dreaded):
1. **Ask why the work arrives.** Much work is caused by something upstream not done, or not done right: customers ask "is it ready?" because nobody told them when to expect it. That kind of work can be prevented.
2. **Then consider, in this order,** and use the first that fits the task, the risk and their ceiling:
   1. **Prevent it.** Tell people before they ask (a date at drop-off; a text when it is done or late), or fix the cause.
   2. **Let them look it up.** Put the answer where they would look (prices on the website, a status they can check).
   3. **Answer it from a source of truth, on its own**, only for kinds of message they allowed, as far as their ceiling goes: only when a message clearly fits one allowed kind; filled from the source or a template, never made up; labelled as automatic; anything unclear, mixed or upset goes to them, unanswered. Notices when something happens (the job is done; a promised date will be missed: the delay and a short apology) belong here too.
   4. **Assist.** A draft or part of the job they check, for what is left.
   5. **Keep it human:** see "Not for AI".
3. **Prefer removing work to speeding it up.** In Saves, say roughly how much of the load it removes, as a guess. Many of the best answers are not AI at all; that is fine.

**Source first.** If customers ask about something that has no up-to-date digital source (it lives on paper, in their head, or in an old saved reply), the first idea is to make that source; automation sits on top of it. Add the gap to `how-we-work.md` as a `GAP:` line ("GAP: no up-to-date list of which bikes are ready; it is on the paper tags").

**Their ceiling.** The person decides how far this goes. If `limits.md` already says (for example "nothing goes out without me seeing it"), stay within it. If it does not, and an idea would send something on its own, ask before you tell them that idea, as an open question: "Are there any kinds of messages you'd be happy to have go out on their own, marked as automatic?" Write their answer in `limits.md` in their words. If they say none, use drafts they approve.

## Seven kinds of help

Choose the shape first (above); the kind only names the help. Name which kind each idea is. These are easy to learn:
- **Read it:** pull facts out of files (for example, find unpaid invoices).
- **Draft it:** write a first version for a person to check (a reply, a reminder).
- **Check it:** compare two things and flag what does not match.
- **Sort it:** put things in groups or order (emails by question type).
- **Watch it:** notice when something happens (an invoice goes past due).
- **Connect it:** move information from one place to another.
- **Build it:** make a small tool (a spreadsheet, a simple page).

## Each idea, in this shape

```
### 1. <short name>  (kind: check it)
- Why: <the problem, with the quote or file it comes from>
- Now: <how it is done today, with its mark, e.g. saved replies pasted by hand (said: "..."); or GAP>
- Saves: <honest guess, e.g. "maybe 1 hour a week"> (guess, check)
- Touches: <files, email, money, customers>. Undo: <how to stop or reverse it>
- Risk: <what could go wrong, plainly>
- Guardrails (only for an idea that sends or acts on its own): <the allowed kinds of message; what it may never promise, such as a price or date not in the source; how it is labelled; where everything else goes; what it logs; how to switch it off>
- Simplest version: <the smallest thing that would help>
- Another way: <what a careful person could do instead, without this idea, and when that would be better. Look hard first: by hand, a spreadsheet or checklist, changing how the work is set up, someone else doing it. Only if none would truly work, write "none that works, because <reason>", and do not say it aloud>
- Try this week: <one small step the person can do>
- Status: idea, <date>   (idea, picked, trying, kept, dropped, with the date it was set: only the person changes this)
```

If the person drops an idea, keep it with `Status: dropped, <date>` and their reason, so no one proposes it again without knowing why. The date lets a later session ask "did you try it?" once enough days have passed (the **Outcome check** in `references/returning.md`; the days are set in `SETTINGS.md`, 14 if not set), which adds a `- Tried:` line under the idea.

## Naming a tool

Ideas are about the job, not a product. If you name a tool, and nobody has checked its code for safety (only a tool marked `vetted` in a shared index has been), add one plain line: "Nobody has checked this tool's code for safety yet." Do not suggest installing or using it here. Using it waits for a builder brief, where the owner can agree to help check it first. The idea's simplest version must work without it.

## Did you know cards

The `did-you-know` skill's `cards.md` lists things AI can do that people found useful. They help the person see uses they would not think to ask for. Use them only here, in Ideas, after Check back and **after** you have told them the top idea and heard their answer; never while you are still asking how things work.
- A card is not an idea. Offer only a card for a use that is **not already one of your ideas**.
- Offer **at most two**, and only cards that match something the person said. Quote it: "Earlier you said you type up the tags on Mondays. Did you know I can read a photo of a receipt and add it to a list? Would that help?" One card per message.
- Always start with "Did you know I can", and give the card's caution in one sentence.
- If no card matches, offer none.
- Write down the person's answer with `(said: ...)`. Never copy a card into the profile as a fact. A card they like may become one of the 3 to 5 ideas: its Why cites their answer, and its "Try this week" can be the card's "Try it" line.

## Rank

Order by: most work taken off them first, then least effort, then least risk. An idea that sends messages or touches money stays within their ceiling ("Their ceiling" above) and states its guardrails. Decisions about money (refunds, chasing a debt, a price that is not on the sheet) stay with a person.

## Not for AI

Include at least one line under the heading `### Not for AI` naming something from the profile that AI should not do, or where a plain spreadsheet, a checklist or a person is the better answer. Base it on real risk: decisions about money, an apology for a serious failure, anything not backed by a source, and what `limits.md` keeps human. "The owner reads every message" is not a Not for AI line by itself. Always respect `limits.md`. Say why in one sentence.

## Check yourself before writing

- Is every idea tied to something the person said or a file showed?
- Does every idea say how the task is done now, and build on it?
- Does every "Another way" name a real alternative, or say plainly why none would work?
- Does each idea take work off them, as far as their ceiling allows? Does every idea that sends or acts on its own state its guardrails?
- Did I invent any number? If so, mark it `(guess, check)`.
- Did I respect `limits.md`?
- Are there 5 or fewer?

===== File: references/next-steps.md =====

# Closing: what next

Say this in plain words, in your own short sentences. Keep it under 10 lines. Skip what does not fit. Two other skills may sit next to this one: `builder-brief` and `share-safely`. Mention one only if its folder is there; otherwise give the plain step.

1. **Keep your folder.** `profile/` is yours: plain text files. Keep a copy somewhere safe. If they ask you to copy it to a place they name, do it.
   - *Only on a shared or public computer:* copy it now; it may be deleted when you log out.
2. **Check it.** Open the files and fix anything wrong. Check `limits.md` most carefully: it tells every later AI tool what not to do.
3. **Try one idea.** Do the "try this week" step from the top idea in `ideas.md`. After the days `SETTINGS.md` gives for **Outcome check after** (14 if not set), start this again in the same folder and say "hi": it will ask how it went and update the idea.
4. **Building a tool.** With `builder-brief`: say "make a brief for idea 1". It writes a plan a coding AI can build from, in `profile/briefs/`, and checks it against `limits.md`. Without it: copy `profile/` into a new folder for that project, start the AI there, and tell it to read `profile/README.md` and `profile/limits.md` first. (Started in this folder, it would start this interview again.)
5. **Sharing it with someone.** Before the folder goes to anyone else (a builder, a company, a helper who takes it away), use `share-safely`: it makes a copy with names, money details and private notes taken out, and shows them every change before anything leaves. Without it: give out only what they have read and are happy to share.
6. **Keep it current.** When things change, or every few months, start this again in the same folder and say "things have changed". It asks what is new and checks the oldest parts.
7. **On your own business.** If this was practice, start fresh in a new, empty folder with this skill. You can add a few files that show how the business runs (money in and out, customer messages, a weekly task); remove passwords, account numbers and private customer details first. No files is fine too.

===== File: did-you-know/SKILL.md =====

# Did you know I can...?

Most people cannot answer "what could AI do for you?" cold. A concrete example tied to their own work often makes it click. The examples are in `cards.md`, one card each.

## Rules

1. **Listen first.** Ask what takes up their time, or what they dread, before offering any card. One question at a time, short and plain (about grade 6).
2. **Only cards that match.** Offer a card only when it fits something they said, and say what they said: "You said you type up receipts on Mondays. Did you know I can read a photo of a receipt and add it to a list? Would that help?" If nothing fits, offer nothing.
3. **Two at most, then stop offering.** This is not a sales pitch.
4. **Show, don't tell.** If they like a card, offer to try it now on something small: their own file (ask first) or a made-up example. Use the card's "Try it" line. Show the result in the chat; write a file only if they ask and name where.
5. **Say the catch.** Every time, give the card's caution in one sentence. If the try goes wrong, say so plainly; that is useful to see.
6. **Be honest about what it needs.** If a card needs a paid plan, a connected app or a regular habit, say so before trying.
7. **Privacy.** If no one has said it yet, say once, before they share anything: what they type goes to the AI company that runs this model. No passwords, account numbers, or private details about customers or staff. Use made-up data on shared computers.

## End

Ask which one they would try this week, and give them that card's "Try it" line to keep.

===== File: did-you-know/cards.md =====

# Did you know I can...? (cards)

One card per use. Keep each general: no business or person names. **Checked** is the date someone last confirmed the card is true. **Source** says where it came from; "Get2Know seed" means a starting idea not yet seen in a real session.

Moves: read it, draft it, check it, sort it, watch it, connect it, build it.

---

### Read a receipt photo
- **Line:** I can read a photo of a receipt and add the date, shop and total to a list.
- **Move:** read it · **Hat:** bookkeeper
- **Needs:** a photo or a typed copy of the receipt.
- **Caution:** blurry photos give wrong numbers; check the totals against the paper.
- **Try it:** "Here is a receipt. Put the date, shop, total and tax in a table."
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Total a spreadsheet by category
- **Line:** I can read a spreadsheet or bank export and total it by month or by kind of spending.
- **Move:** read it · **Hat:** bookkeeper
- **Needs:** the file (CSV or spreadsheet). Remove account numbers first.
- **Caution:** I can sort things into the wrong category; look at the groups before trusting the totals.
- **Try it:** "Total this export by month, and list the five biggest costs."
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Match payments to invoices
- **Line:** I can compare a list of invoices with your bank export and show which ones look unpaid, late, or for the wrong amount.
- **Move:** check it · **Hat:** bookkeeper
- **Needs:** both files.
- **Caution:** payments with different names or split amounts can fool me; treat my list as "look at these", not as the answer.
- **Try it:** "Which invoices have no matching payment in the bank file?"
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Draft replies to the same questions
- **Line:** I can draft replies to the questions people ask again and again, from your price list and rules, for you to check and send.
- **Move:** draft it · **Hat:** front desk
- **Needs:** your price list or rules, and a few example questions.
- **Caution:** I can state a price or promise you never made; read every reply before it goes out.
- **Try it:** "Here are five customer emails and my price list. Draft a short reply to each."
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Sort an inbox
- **Line:** I can sort a pile of emails or messages into kinds (prices, bookings, complaints, junk) so you can answer the urgent ones first.
- **Move:** sort it · **Hat:** front desk
- **Needs:** the messages, copied or exported.
- **Caution:** I can miss an angry tone or a deadline; skim the "not urgent" pile.
- **Try it:** "Sort these messages into groups and tell me which need an answer today."
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Explain a letter and find the deadline
- **Line:** I can explain a confusing official letter in plain words, translate it, and point out any deadline or amount owed.
- **Move:** read it · **Hat:** compliance
- **Needs:** the letter, typed or as a photo. Cover personal numbers first.
- **Caution:** I can misread legal meaning; for anything serious, confirm with the sender or a professional.
- **Try it:** "Explain this letter in simple words. Is there a deadline?"
- **Source:** W01 "Bring your problems" worked case (government letters), 2026-09 · **Checked:** 2026-10-29

### Pull the rules out of a long document
- **Line:** I can read a long document, like a lease, funder guide or insurance policy, and list only the parts that apply to you.
- **Move:** read it · **Hat:** compliance
- **Needs:** the document.
- **Caution:** I can miss a clause; ask me to quote the exact line for anything you rely on.
- **Try it:** "What does this guide say I must report, and by when? Quote the lines."
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Turn a habit into a checklist
- **Line:** I can turn "how I do it" into a step-by-step checklist someone else could follow.
- **Move:** draft it · **Hat:** operations
- **Needs:** you, describing the task once.
- **Caution:** I only know the steps you tell me; have the person who will use it try it once.
- **Try it:** "I'll tell you how I open the shop. Make it a checklist for a new helper."
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Draft a report from your notes
- **Line:** I can turn rough notes and numbers into a first draft of a report, like a grant report or a board update.
- **Move:** draft it · **Hat:** owner / director
- **Needs:** your notes, the numbers, and the report's questions.
- **Caution:** I can make numbers or results sound better than they were; check every figure.
- **Try it:** "Here are my notes and the funder's questions. Draft the answers."
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Check a list each week
- **Line:** I can check a list for you every time you ask, like "which jobs have waited over two weeks?" or "which invoices are past due?".
- **Move:** watch it · **Hat:** operations
- **Needs:** the list kept up to date, and you asking each week (or a tool that runs it on a schedule).
- **Caution:** I only know what is in the list; if it is not updated, my answer is out of date.
- **Try it:** "Which rows in this list are more than 14 days old?"
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Move information between formats
- **Line:** I can copy information from one shape to another, like handwritten notes into a spreadsheet, or a spreadsheet into a letter for each person.
- **Move:** connect it · **Hat:** records keeper
- **Needs:** the source (typed, a photo, or a file).
- **Caution:** copying is where small mistakes slip in; spot-check a few rows.
- **Try it:** "Turn these notes into a table with name, date and amount."
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Build a small tool
- **Line:** I can build a small tool for you, like a spreadsheet that adds up for you, or a simple web page with your prices and hours.
- **Move:** build it · **Hat:** any
- **Needs:** time to try it with me, and a plan for who fixes it later.
- **Caution:** a tool nobody looks after breaks quietly; keep it small and write down how it works.
- **Try it:** "Show me here, in the chat, a job-tag table with 3 made-up jobs: job, price, date in, date out."
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

### Help you decide with what you know
- **Line:** I can lay out a choice, like adding a new service, as what you know, what you don't, and the cheapest way to find out.
- **Move:** sort it · **Hat:** marketer
- **Needs:** you, and anything you already know (questions customers ask, costs).
- **Caution:** I can sound sure about a market I know nothing about; treat my facts about your area as guesses to check.
- **Try it:** "Customers keep asking for a new service. Help me list what I'd need to know before deciding."
- **Source:** Get2Know seed, 2026-10 · **Checked:** 2026-10-29

===== End of part 2 =====
