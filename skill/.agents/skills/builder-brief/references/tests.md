# Acceptance tests (the owner approves these)

An acceptance test is a check, in plain words, that says the tool does its job. The owner approves them before anyone builds. This is on purpose: when a tool does a job for you, you slowly lose the feel for that job, and then you cannot spot when the tool is wrong. Deciding what "working" means, in your own words, keeps that feel. It is the one part of building the owner should never hand off.

## Shape

Each test is one plain sentence, in one of these shapes, with a mark saying where it came from:

- **Does the job:** "When I give it <input>, it <result>." (from "What it must do")
- **Never:** "It never <thing>." (from "What it must never do" and `limits.md`)
- **Goes wrong safely:** "If <something is missing or odd>, it <says so / stops / asks>, and does not guess."
- **Undo:** "I can <stop it / delete what it made>, and my old files are unchanged."
- **A person checks:** "Nothing goes to a customer (or touches money) until <role> has looked at it."

These follow the plain shapes of EARS (a way of writing requirements: "when...", "if...", "never..."), so a builder can turn each one into a code test without changing its meaning.

Under a test, add a **worked example** when you have one: a small input and the exact result expected, from the owner's real example or made up and labelled so.

```
3. When I give it last month's invoices and the bank file, it lists every invoice with no matching payment. (said: "I never know who still owes me")
   Example (made up): invoice 1042 for $380, no $380 payment from that customer → it is on the list.
```

## Rules

1. **8 or fewer.** The owner must be able to read them all in one go. Pick the ones that matter most.
2. **At least one "never" test for each `limits.md` line that touches the tool,** and one undo test. Never drop these to make room.
3. **Something the owner could check by looking.** "It lists...", "it stops and says...". Not "it is accurate" or "it is fast".
4. **No invented numbers.** "Within a day" only if they said it. Otherwise write what they said, or leave a `GAP:`.
5. **No technical words.** "File", "list", "email" are fine. "API", "database", "endpoint" are not; the builder will work out those.
6. **The owner's example wins.** If their real example does not fit a test, change the test, not the example.

## Getting a real approval, not a nod

A quick "looks fine" is not yet approval. Show the tests, ask what is wrong or missing, fix them, then ask the owner to tie one test to a real time this went wrong. Their example goes under that test. Only then write `Approved by the owner`, with their words.
