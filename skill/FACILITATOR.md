# Get2Know: notes for whoever runs the session

Short. For a workshop, a library session, or helping one owner.

## What it is

An AI interviewer. It asks one plain question at a time about how an organization really works, writes the answers into a `profile/` folder of plain text files, then suggests 3 to 5 places AI could help, and at least one place it should not. It never sends anything or changes other files. If someone asks to share their profile, it makes a cleaned copy in a `share/` folder next to `profile/`; they send it themselves.

## Before the session

- Each person needs this folder, opened in Claude Code (start Claude Code *in* this folder).
- The first time, Claude Code asks whether to trust the folder. Say yes.
- If they will practise on a made-up business, put its files in this same folder.
- Say this out loud: what people type goes to the AI company that runs the model. Use made-up details on shared computers.

## The one sentence to say

> "Type **hi**, and answer its questions as the owner."

Starting from earlier notes or a draft profile? It will ask; they say yes and name the file.

## What good looks like (about 20 to 25 minutes)

1. It says hello, says what will happen, gives the privacy note, asks if there are notes to start from.
2. With notes: it reads them, makes `profile/`, and names the 3 or 4 gaps that matter most.
3. One short question at a time. It writes as it goes, quietly; it says so when it makes a new file or changes something said earlier. (To hear a line after every answer, set it in `SETTINGS.md`.)
4. After about 8 answers: a short summary and "Is anything wrong or missing?"
5. 3 to 5 ideas in `profile/ideas.md`, the top one said out loud, and "stop or keep going?"
6. Close: where the folder is, one thing to try this week, what next.

## If it goes wrong

| What you see | What to say or do |
|---|---|
| It asks several questions at once | Tell them: "Answer the first one only." |
| It asks permission to edit or read a file | Yes, if it is inside this folder. Otherwise say no and ask why. |
| It gets stuck or they lose the thread | Type "where were we?" Its notes are in `profile/interview-notes.md`. |
| They are out of time | Type "let's stop here". It saves notes and says how to carry on. |
| It suggests something that sends emails or touches money on its own | Point out it should always have a person checking; check `limits.md`. |
| It asks for a password, account number or a customer's details | Say no. That is a fault: note it and tell the organizer. |
| Claude Code closed by accident | Start it again in the same folder and type "hi". It picks up from `profile/`. |

## Sitting with one owner (helper mode)

You are the helper: a volunteer, librarian, consultant or friend. The owner is the one being interviewed.
- Start with: "**Hi, I'm helping an owner.**" It will greet you both and explain how it works.
- You may type. Type the owner's answers in **their** words, not a tidier version. If you want to add something of your own, start it with `Helper:`. It marks your words differently from theirs.
- Read each question out if that helps. Explain a word if they are stuck. Do not answer for them, even when you think you know.
- **The owner says yes or no**: to starting, to reading a file, to each idea, to copying the folder. Pass each of those questions to them.
- **Limits are theirs.** When it asks what must stay human or what rules apply, stay quiet. It will not write your words into `limits.md`.
- If they want to talk in another language, let them type in it, or type it for them. It will switch, and write the profile in that language.
- At the end, make sure they leave with the folder, and know to come back in about two weeks and say "hi" ("did you try it?").

## Training other helpers

About 45 minutes; no technical background needed.
1. **Watch one** (10 min): run a session on a made-up business while they watch. Point out the one-question rhythm, the files filling up in `profile/` as it goes, and the check-back.
2. **Play the owner** (15 min): each trainee answers as a made-up owner while another types as the helper. Then swap.
3. **Read the folder** (10 min): open `profile/` together. Find a `(said: ...)` line, a `(said by helper: ...)` line and a `GAP:`. Ask: would the owner agree with every line?
4. **Talk through the hard parts** (10 min): the owner goes quiet and the helper wants to fill in; the owner wants to share a customer's details; the owner asks "what should I say?"; the owner is tired (type "let's stop here").
What helpers most often get wrong: answering for the owner, tidying the owner's words, and saying yes to something on the owner's behalf.

## After

- The person keeps the `profile/` folder. On a shared or public computer, copy it out before logging off (USB, email, or the take-home script).
- To use it on their own business: a new, empty folder with this skill in it, then "hi".
- Later, in the same folder: "hi" in about two weeks asks how the idea went; "things have changed" months later updates the profile. Staff or volunteers can be heard too, with the owner's okay.
- How long it waits before asking "did you try it?" (14 days) or "what has changed?" (30 days) is set in `SETTINGS.md`, at the top of the folder. The owner can change the numbers in any text editor.

## Your deployment

Add a short section here for your own setting: who the participants play, which files they start from, and what is not allowed on your machines.
