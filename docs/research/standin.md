# Standin: hiding private details in owner records (research, 2026-10-30)

**Question.** Can Get2Know use [Standin](https://github.com/RKelln/standin) (v0.1.0, Ryan's Go tool, MIT) so the interviewer reads an owner's records without seeing customer names, emails and account numbers? This is the PII guard from D62 and HANDOFF Next 5.

**Short answer.** It works on the CSV records, but it is **not for the workshop**. Plan it for after the workshop, as an option an owner turns on. It only covers what the interviewer reads from files. It does not cover what the owner types in the chat (Ryan: "its not really designed for interactive chats, just the data fed to the interviewer").

## What was tried (2026-10-30)

I built Standin from `main` and ran it on a copy of `tests/rehearse/fixture/shop/` in a scratch folder, with a scratch `STANDIN_HOME`. No model was used: I wrote the config by hand and approved it in a pseudo-terminal, acting as the owner.

- **CSVs work well.**
  - `invoices-q3.csv`: Customer was tokenized; every other column was kept.
  - `bank-export.csv`: Description was scanned and Balance dropped.
  - In the scanned descriptions, every payer name became the same stand-in it got in the invoices (`E-TRANSFER [PERSON_2]`), because the names were already in the mapping. That covered both e-transfers and cheques.
  - Shop and supplier lines (POS DEPOSIT, NORTHGATE CYCLE SUPPLY) stayed readable. None of the four customer names I searched for appeared in `scrubbed/`.
  - So the interviewer could still find a short payment by invoice number and amount.
- **Markdown and text are refused** (`customer-emails.md`, `price-sheet.md`, `receipts/*.txt`). The customer emails are the most private file in the folder, and Standin cannot help with them yet.
- **`standin init` merges with the bundle**:
  - It added its hooks and deny rules to `.claude/settings.json` and kept Get2Know's `allow` rules.
  - It appended a marked block to `AGENTS.md`.
- **The prompt hook blocks the owner's own words.** (It was never part of the design and is to be removed.) A message with a customer's full name was not sent ("Your message was not sent. It has real values of [PERSON_4]"). A phone number was blocked too. A first name alone went through. In an interview this stops the owner talking about their customers.
- **Moving the folder blocks every tool.** The hooks hold the folder's full path and fail closed, so a copied or moved folder blocks every file tool until `standin init` is run again. Owners do move this folder (taking it home from the workshop, D54).
- **`restore`** put the real names back into `restored/answer.md`. It refused to print real values when not run in a terminal.

## How it would fit

1. **Opt-in, per owner.** Get2Know never installs Standin. FACILITATOR or a short guide explains the steps. The owner (or a helper) installs it with `curl`, runs `standin init`, and moves the records into `raw/`. Get2Know runs fine without it.
2. **The interviewer reads `scrubbed/` when it exists.** This goes in a reference file read only when the folder has `standin.config.json`, not in `SKILL.md`; chat part 1 has no room, and chat apps cannot run Standin.
   - Rule 6 is unchanged: still ask first, and read only after a yes.
   - Never open `raw/` or `restored/`.
   - Never ask for the mapping.
3. **Setup inside the session.**
   - The interviewer may run `standin shape` and write `standin.config.json`.
   - The owner runs `standin review` and `standin approve` in their own Terminal window. This is the step a non-technical owner will find hardest, so it needs a helper or a very plain guide, and testing with a real person.
   - Then the interviewer or the owner runs `standin scrub`.
4. **Ask from things the owner can recognise.** The owner does not know who `[PERSON_9]` is.
   - Questions name the invoice number, date and amount: "INV-1012 was paid $20 short in July. What happened there?" Not "[PERSON_9] paid short".
   - If the owner wants to know who a stand-in is, they look it up in their own terminal (see the Standin changes below), not in the chat.
5. **The profile holds no stand-ins and no customer names.** Write roles ("one regular customer", "the courier company") as the profile already should. A stand-in in `profile/` means nothing to the owner reading it later. It would also break if the mapping were lost.
6. **The owner's chat is not filtered.** The owner will name people. The interviewer still follows the existing rules: do not copy private customer details into `profile/` beyond what is needed, and share-safely cleans what leaves.
7. **share-safely.** `profile/` is Markdown, which Standin cannot scrub yet.
   - When Standin is installed, `standin check profile/<file>` is an extra check after `check_share.py`. It looks for every value in the mapping, so it catches customer names the regex check cannot know.
   - When it is not run in a terminal it says only "found something", so the owner runs it in their own terminal to see where.

## Changes needed in Get2Know (not done)

- A reference file for "private records with Standin" (point 2 above), and a line in `SKILL.md` that points to it only when `standin.config.json` exists.
- **`update.py` and `MANIFEST.sha256`.** After `standin init`, `AGENTS.md` and `.claude/settings.json` count as changed by the owner. So updates stop replacing them and park the new copies in `updates-to-review`.
  - Teach `update.py` to keep the Standin block and the Standin hooks while updating the rest.
  - Or ask Standin to write its hooks to `.claude/settings.local.json` (see the Standin list).
- FACILITATOR or owner guide text for setup, with the honest limits from Standin's README.
- share-safely: the optional `standin check` step (point 7).
- **Tests.**
  - A rehearse case whose work folder holds `scrubbed/` copies made with a fixed mapping, with no `raw/`. This tests the interviewer's behaviour without hooks, which matters because Codex has no Standin hook.
  - Check that it asks by invoice number, not by stand-in.
  - Check that no stand-in reaches `profile/`.
  - Check that it never tries `raw/`.
  - The work-folder diff already shows any read outside `scrubbed/`.

## Changes needed in Standin

Listed for the Standin repo in `standin/docs/get2know-needs.md` (sister folder). In short:

1. Markdown and plain-text files (emails, notes, receipts): the proposal is that the person approves words, not columns. Every word that could be a name or private becomes a stand-in unless they keep it.
2. Remove the prompt hook. It was never part of the design; the build agent added it from the draft's "later phase" list.
3. A scrub run before approval fills the mapping with whole values, which later wipes out scan columns.
4. Hooks that survive a moved folder.
5. A lookup the owner runs to see who one stand-in is.
6. Hooks in `settings.local.json`.
7. A confusing restore message.

## Untested

- No model has used Standin with Get2Know. Claude Code with the hooks is untested with Get2Know; Codex has no hook at all.
- No Mac run.
- No real owner has done the approve step.
- The scan was tried only on the fixture's bank export, where every payer is also an invoice customer. With real exports, payers who are not in a tokenized column stay in plain text (Standin README, "What it misses").
