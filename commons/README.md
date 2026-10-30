# The capability commons: records

This folder holds the records of the capability commons proposed in `docs/capability-commons.md`: what AI can do for a small organization, and which open-source tools do it. **Status: seed, 2026-10-29.** No record here has been reviewed by a person yet (`reviewed_by` is empty on all of them).

## Licence: CC0

Everything in `commons/records/` is dedicated to the public domain under **CC0 1.0** (https://creativecommons.org/publicdomain/zero/1.0/legalcode). Anyone may copy, change and reuse the records for any purpose, without asking and without credit. By adding a record you agree to dedicate it the same way. Write records in your own words: never paste a project's README or other text you do not have the right to give away. `check.py` is code and falls under the repository's MIT licence.

## Layout

```
commons/
  README.md        this file
  check.py         checks every record (standard library only)
  records/
    capability/    level 0-1: "an AI can do X"
    recipe/        level 2: "here is a way to do it" (none yet)
    tool/          an open-source project, vetted or not
    story/         a real use, anonymized, with consent (none yet)
    gap/           a need with no good open answer yet
```

One record per file. The file name is the record's `id` plus `.md`, and the id starts with its kind (`tool-gnucash`, `capability-sort-inbox`).

## Record format

A Markdown file that starts with a header in **TOML** between two `+++` lines, then plain words for people. TOML, not YAML, because Python reads TOML with its standard library (`tomllib`), so no extra packages are needed.

```
+++
id = "tool-example"
kind = "tool"
title = "Example"
status = "listed-not-vetted"
checked = "2026-10-29"
...
+++
## What it does
Plain words, grade 6.
```

Fields every record has: `id`, `kind`, `title`, `status`, `checked` (date last confirmed true, `YYYY-MM-DD`), `checked_by` (who or what checked), `reviewed_by` (the person who reviewed it; empty until then), `related` (ids of linked records).

Capability records add `level` (0 or 1), `moves`, `hats`, `inputs`, `org_types`, `language`, `runs`, `data`, `touches`, `evidence`, and `card` (the title of the did-you-know card it came from, if any).

Tool records add `url`, `licence` (an SPDX id or expression; `LicenseRef-...` for a licence SPDX does not list), `licence_note`, `osi` (true if the licence is OSI-approved), `openness`, `open_core`, `vetted`, `last_release`, `last_release_date`, `archived`, `runs`, `hats`, `does`.

## Status and level, honestly

The ladder in the proposal has four levels; only capabilities and recipes are placed on it here. A **tool** sits at level 3 only when it has passed the vetter (`vetted = true`, with `level = 3`, `vetting_report` and `pinned_version`). Until then:

| `status` | Means | Shown to an owner? |
|---|---|---|
| `found` | the scout found it; nobody has checked it | no |
| `listed` | a capability, gap or recipe checked by an agent and awaiting a person's skim | as "this is possible" |
| `listed-not-vetted` | a tool whose facts (licence, releases, what it does) were checked at the source; its code was not | by name, with a one-line warning that nobody has checked its code; for use only if the owner agrees to help check it (decided with Ryan, 2026-10-29); otherwise the owner gets the level-0 knowledge or another option |
| `vetted` | passed the vetter; a person approved the first listing | yes, preferred |
| `stale` | archived, licence changed, no release in 18 months, or a dead link | no, until re-checked |
| `excluded` | checked and **not open source** (for example source-available). Kept so the scout does not add it again and an agent can say why it is not offered | no, except to explain |

`openness`: `"1"` fully open (OSI licence, runs without a closed service; commercial open source counts), `"2"` open connector to a closed service, `"source-available"` code you can read but not under an open-source licence. `open_core = true` means some features sit in a paid, closed edition: listed in tier 1, with the catch said in `licence_note`.

## Checking

```
python3 commons/check.py                        # all records
python3 -m unittest discover -s tests/commons   # the checker's own tests
```

`check.py` checks: required fields, the kind and status words, dates (format, real, not in the future), the licence field (SPDX shape; OSI needed for openness 1 or 2; source-available must be `excluded`), that an unvetted tool claims no level, file name = id, unique ids, and that every `related` id exists. It does not check that a record is *true*; that is the `checked` date's job and the gardener's.

## The seed (2026-10-29)

- **30 tool records** for established projects. Each one checked the same day through the GitHub API (licence file, latest release, archived flag) and, where there are no GitHub releases, the project's download page or newest tag. Licence variants (`-only` or `-or-later`) were taken from package metadata or file headers where found; where not found the record uses the bare id GitHub reports and says so in `licence_note`.
- **12 capability records**, level 0: eleven from the did-you-know cards (`card` names the card) and one new (answering from your own documents on a local model).
- **1 gap**: a production-ready open booking page with text reminders.

Not vetted, all of it. A record's `checked` date says when its facts were true, not that the software is safe.
