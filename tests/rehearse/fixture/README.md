# W06 bike shop: source files (for facilitators and tests)

Spoke & Chain is a made-up shop. Every person, business, number and bank line here is invented.
Participants get only `shop/`; its `shop-card.md` says the shop is made up.

- `shop/`: the participant folder. `sam-profile-draft.md` is Sam's draft from a first interview,
  hand-written; the other files come from `build_shop.py`.
- How participants fill the draft's GAPs: answer from the files in `shop/` (`invoices-q3.csv`,
  `bank-export.csv`, `receipts/`, `customer-emails.md`, `price-sheet.md`, `shop-card.md`), or decide
  what Sam would say. If unsure, say "I don't know"; the interviewer marks it as a gap. (This used to
  sit at the end of the draft; it was moved here because the interviewer read it as an instruction.)
- `answer-key.md`: what a careful look finds. For facilitators and test judges only. Never put it in
  a participant or agent folder.
- `sam-profile-draft-messy.md` and `shop-messy/`: tests only. The same shop with a messy draft
  (duplicates, stale numbers, a pasted table, a to-do list, a forwarded email). Not for participants.
- `python3 build_shop.py` remakes `shop/` data files, `answer-key.md` and `shop-messy/` (fixed seed).

Licence: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); `build_shop.py` is MIT. Master copy: `tests/rehearse/fixture/` in the Get2Know repo; the workshop copies `shop/` from there.
