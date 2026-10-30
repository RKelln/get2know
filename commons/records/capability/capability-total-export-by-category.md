+++
id = "capability-total-export-by-category"
kind = "capability"
title = "Total a bank export or spreadsheet by category"
level = 0
status = "listed"
checked = "2026-10-29"
checked_by = "seed agent: written from the did-you-know cards (DESIGN D21)"
reviewed_by = ""
moves = ["read"]
hats = ["bookkeeper"]
inputs = ["a CSV or spreadsheet export, account numbers removed"]
org_types = ["any"]
language = "en"
runs = ["hosted", "local"]
data = "whatever the person pastes in goes to the AI they use; with a local model, nothing leaves the computer"
touches = ["money"]
card = "Total a spreadsheet by category"
related = ["tool-libreoffice", "tool-gnucash"]
evidence = "general model ability; not yet shown on made-up data (level 1 needs a prover run)"
+++
## What is possible

An AI can total a bank export or spreadsheet by month or by kind of spending, and list the biggest costs.

## The catch

It can put things in the wrong group. Look at the groups before trusting the totals.

## Level

**0, possible.** Not yet shown on made-up data. The related tools are options people use for this job, not proof that this works.
