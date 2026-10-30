+++
id = "capability-match-payments-to-invoices"
kind = "capability"
title = "Match payments to invoices"
level = 0
status = "listed"
checked = "2026-10-29"
checked_by = "seed agent: written from the did-you-know cards (DESIGN D21)"
reviewed_by = ""
moves = ["check"]
hats = ["bookkeeper"]
inputs = ["a list of invoices", "a bank export"]
org_types = ["any"]
language = "en"
runs = ["hosted", "local"]
data = "whatever the person pastes in goes to the AI they use; with a local model, nothing leaves the computer"
touches = ["money", "customers"]
card = "Match payments to invoices"
related = ["tool-gnucash", "tool-erpnext", "tool-frappe-books"]
evidence = "general model ability; not yet shown on made-up data (level 1 needs a prover run)"
+++
## What is possible

An AI can compare a list of invoices with a bank export and show which invoices look unpaid, late, or paid the wrong amount.

## The catch

Payments under a different name, or split into parts, can fool it. Treat the list as 'look at these', not the answer.

## Level

**0, possible.** Not yet shown on made-up data. The related tools are options people use for this job, not proof that this works.
