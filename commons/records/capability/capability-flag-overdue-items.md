+++
id = "capability-flag-overdue-items"
kind = "capability"
title = "Flag items in a list that have waited too long"
level = 0
status = "listed"
checked = "2026-10-29"
checked_by = "seed agent: written from the did-you-know cards (DESIGN D21)"
reviewed_by = ""
moves = ["watch"]
hats = ["operations"]
inputs = ["a list kept up to date, with dates"]
org_types = ["any"]
language = "en"
runs = ["hosted", "local"]
data = "whatever the person pastes in goes to the AI they use; with a local model, nothing leaves the computer"
touches = []
card = "Check a list each week"
related = ["tool-inventree"]
evidence = "general model ability; not yet shown on made-up data (level 1 needs a prover run)"
+++
## What is possible

An AI can check a list on request, or on a schedule, and flag rows past a limit: jobs waiting over two weeks, invoices past due, stock running low.

## The catch

It only knows what is in the list. If the list is stale, so is the answer.

## Level

**0, possible.** Not yet shown on made-up data. The related tools are options people use for this job, not proof that this works.
