+++
id = "capability-answer-from-own-documents"
kind = "capability"
title = "Answer questions from your own documents, on your own computer"
level = 0
status = "listed"
checked = "2026-10-29"
checked_by = "seed agent"
reviewed_by = ""
moves = ["read"]
hats = ["any"]
inputs = ["the documents", "a computer that can run a local model"]
org_types = ["any"]
language = "en"
runs = ["hosted", "local"]
data = "whatever the person pastes in goes to the AI they use; with a local model, nothing leaves the computer"
touches = []
card = ""
related = ["tool-ollama", "tool-jan"]
evidence = "general model ability; not yet shown on made-up data (level 1 needs a prover run)"
+++
## What is possible

An AI running on the organization's own computer can answer questions from its own documents (policies, price lists, past reports) without sending them to an AI company.

## The catch

Local models make more mistakes than big online ones. Ask it to quote where each answer came from.

## Level

**0, possible.** Not yet shown on made-up data. The related tools are options people use for this job, not proof that this works.
