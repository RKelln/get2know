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
- Another way: <what a careful person could do instead, without this idea, and when that would be better>
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
- Does each idea take work off them, as far as their ceiling allows? Does every idea that sends or acts on its own state its guardrails?
- Did I invent any number? If so, mark it `(guess, check)`.
- Did I respect `limits.md`?
- Are there 5 or fewer?
