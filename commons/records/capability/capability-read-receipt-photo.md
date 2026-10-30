+++
id = "capability-read-receipt-photo"
kind = "capability"
title = "Read a receipt photo"
level = 0
status = "listed"
checked = "2026-10-29"
checked_by = "seed agent: written from the did-you-know cards (DESIGN D21)"
reviewed_by = ""
moves = ["read"]
hats = ["bookkeeper"]
inputs = ["a photo or typed copy of a receipt"]
org_types = ["any"]
language = "en"
runs = ["hosted", "local"]
data = "whatever the person pastes in goes to the AI they use; with a local model, nothing leaves the computer"
touches = ["money"]
card = "Read a receipt photo"
related = ["tool-gnucash"]
evidence = "general model ability; not yet shown on made-up data (level 1 needs a prover run)"
+++
## What is possible

An AI can read a photo of a receipt and add the date, shop, total and tax to a list.

## The catch

Blurry photos give wrong numbers. Check totals against the paper.

## Level

**0, possible.** Not yet shown on made-up data. The related tools are options people use for this job, not proof that this works.
