# Story and gap records for the commons

The commons is a proposed public list of what AI can do for small organizations, and which open-source tools do it. People send back two kinds of record: a **story** (a real use, made general) and a **gap** (a need nobody meets yet). Gaps are the most useful: they become a to-do list for people who build open tools.

Each record is one short Markdown file with a header in TOML between two `+++` lines, the same shape as the commons' own records. The header lets a program sort records without reading them. Use the words from the profile's ideas where you can (the moves and hats). Leave a field out if it is not known; never guess. The file name is the record's `id` plus `.md`: `story-` or `gap-` and a few short words, as `story-match-payments-to-invoices.md`.

These fields are always there: `id`, `kind`, `title`, `status = "found"` (nobody at the commons has checked it yet), `checked` (today), `checked_by = "owner"`, `reviewed_by = ""`. The `[consent]` table comes last, because every line after it belongs to it.

## Rules for every record

- No business name, no person's name or role that only one person has ("the founder's daughter").
- Place: a province, state or country at most, and only if the owner wants it. No city or street.
- Size: a range (`1`, `2-5`, `6-20`, `21-50`).
- Kind of organization in general words ("a bike repair shop", "a small food bank").
- Dates: month and year only, except `checked` and the consent date, which the commons needs in full.
- Money: none, or a rough range the owner agrees to ("under $100 a month").
- Nothing from `limits.md` that the owner did not pick for this record.
- Ask: "Could someone who knows you guess it is you?" A rare kind of business in a small town is easy to guess. Make it more general until the answer is no.

## Story

```
+++
id = "story-match-payments-to-invoices"
kind = "story"
title = "Matching payments to invoices"
status = "found"
checked = "2026-11-02"
checked_by = "owner"
reviewed_by = ""
org = "a small bike repair shop"
size = "2-5"
place = "Ontario, Canada"            # optional
language = "en"
moves = ["check"]                    # read, draft, check, sort, watch, connect, build
hats = ["bookkeeper"]
inputs = ["bank CSV export", "invoices as PDF"]
runs = "local"                       # offline | local | needs a hosted service
touches = ["money"]                  # money, customers, staff
tools = []                           # open-source tools used, with links, if any
when = "2026-11"
result = "worked"                    # worked | partly | did not work

[consent]
licence = "CC0-1.0"
public = "now"                       # now | not before YYYY-MM-DD
checked_by_owner = "2026-11-02"
note = "The owner read this text and agreed to share it."
+++
# Matching payments to invoices

What they needed, in one or two plain sentences.
What they tried, and what the AI did.
What happened: the result, and what they had to check by hand.
What they would tell another small organization.
```

## Gap

```
+++
id = "gap-booking-page-with-text-reminders"
kind = "gap"
title = "Booking page that texts people a reminder"
status = "found"
checked = "2026-11-02"
checked_by = "owner"
reviewed_by = ""
org = "a small food bank"
size = "6-20"
language = "en"
moves = ["connect", "draft"]
hats = ["front desk"]
inputs = ["a shared phone", "a paper sign-up sheet"]
must = ["runs on a cheap host", "no customer data leaves the country"]   # from their limits, made general
tried = ["a commercial booking app (too costly)", "a spreadsheet (no reminders)"]
when = "2026-11"

[consent]
licence = "CC0-1.0"
public = "now"
checked_by_owner = "2026-11-02"
note = "The owner read this text and agreed to share it."
+++
# Booking page that texts people a reminder

What they needed, in one or two plain sentences.
What they tried and why it did not fit (cost, closed, too hard, breaks a rule).
What "good enough" would look like for them.
```

## Consent, in plain words (say this before they agree)

- CC0 means anyone may copy, change and use the record, for anything, without asking or giving credit.
- Until they send it, they can change their mind for any reason.
- After it is published, it can be taken off the list, but copies may already exist. That is the point of no return.
- They can choose "not before" a date instead of "now".
- Each record is its own choice. Saying yes to one is not yes to others.

The commons is a proposal: where to send records is not set yet. If there is no address, the record stays in `share/` until there is.
