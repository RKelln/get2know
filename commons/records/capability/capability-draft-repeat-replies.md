+++
id = "capability-draft-repeat-replies"
kind = "capability"
title = "Draft replies to repeat customer questions"
level = 0
status = "listed"
checked = "2026-10-29"
checked_by = "seed agent: written from the did-you-know cards (DESIGN D21)"
reviewed_by = ""
moves = ["draft"]
hats = ["front desk"]
inputs = ["a price list or rules", "a few example questions"]
org_types = ["any"]
language = "en"
runs = ["hosted", "local"]
data = "whatever the person pastes in goes to the AI they use; with a local model, nothing leaves the computer"
touches = ["customers"]
card = "Draft replies to the same questions"
related = ["tool-freescout", "tool-zammad"]
evidence = "general model ability; not yet shown on made-up data (level 1 needs a prover run)"
+++
## What is possible

An AI can draft replies to questions customers ask again and again, from the organization's own price list and rules, for a person to check and send.

## The catch

It can state a price or a promise nobody made. A person reads every reply before it goes out.

## Level

**0, possible.** Not yet shown on made-up data. The related tools are options people use for this job, not proof that this works.
