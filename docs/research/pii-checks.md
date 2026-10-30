# PII checks for "share safely" (research, 2026-10-29)

**Question.** Before an owner shares a copy of `profile/`, a second check should catch personal details the agent missed. Should Get2Know depend on an existing PII tool, borrow its patterns, or stay with the Python standard library?

**Decision.** Stay standard library. Borrow pattern *ideas* from two MIT projects (Presidio, CommonRegex), written fresh with credit in the script's header. No optional extra for now. The script is `skill/.agents/skills/share-safely/scripts/check_share.py`; tests are in `tests/share_safely/`.

**Why.** The target user is a layperson on a library Mac. Anything that needs `pip install`, a 12 MB+ language model download, or a cloud account will not happen in that room. Python 3 itself may not be present on a Mac without the Command Line Tools, so the skill has a fallback (the agent reads line by line) and never asks the owner to install anything. The script runs on Python 3.9 to 3.14 (tested here on 3.9, 3.12 and 3.14 via `uv`).

## Sources checked

Licences were read from the GitHub API (`gh api repos/<repo> --jq .license.spdx_id`) on 2026-10-29, not from READMEs.

| Tool | Licence | What it is | Used? |
|---|---|---|---|
| [Microsoft Presidio](https://github.com/data-privacy-stack/presidio) (the repo now redirects from `microsoft/presidio` to `data-privacy-stack/presidio`) | MIT | Framework: regex recognizers with checksums and context words, plus a spaCy NER model for names; anonymizer | **Borrowed ideas**: Luhn validation for cards and Canadian SINs; SIN shape `[1-79]\d{2}([- ])\d{3}\1\d{3}` (first digit never 0 or 8); Canadian postal code letter sets (no D F I O Q U; no W or Z first). From `predefined_recognizers/country_specific/canada/ca_sin_recognizer.py`, `ca_postal_code_recognizer.py`, `generic/credit_card_recognizer.py`. **Not a dependency**: `presidio-analyzer` requires spaCy, numpy, pydantic, phonenumbers, tldextract and others, plus a separate spaCy model download. |
| [CommonRegex](https://github.com/madisonmay/CommonRegex) | MIT | One file of regexes (phone, email, street address, PO box, ZIP, card, SSN); last push 2023 | **Borrowed shape** of the street address (number, 1 to a few words, a street-type word) and PO box patterns. Changed: the street name must start with a capital or digit, because the original matches "15 minutes to drive". Its bare 5-digit ZIP pattern rejected: it fires on amounts. |
| [scrubadub](https://github.com/LeapBeyond/scrubadub) | Apache-2.0 | Python library to remove PII from free text; names via TextBlob, optional spaCy | **Rejected as dependency**: last release v2.0.1 on 2023-09-01; pulls textblob, phonenumbers, python-stdnum, dateparser, scikit-learn, faker. Useful as a list of what to look for (it covers CA postal codes and addresses). Nothing copied. |
| [spaCy](https://github.com/explosion/spaCy) | MIT | NLP library with named-entity recognition (finds PERSON, ORG, GPE in free text) | **Rejected for now.** It is the only option here that finds names nobody told it about, which is the real gap. But it is a compiled install plus a model download, and small English models miss many non-English names, which matters for Toronto owners. Revisit as an optional extra if real sessions show the agent pass missing names. |
| [detect-secrets](https://github.com/Yelp/detect-secrets) | Apache-2.0 | Finds API keys and passwords in code | Idea only: a keyword rule ("password: ...", "PIN is ..."). Its keys-in-code detectors do not fit plain-language profiles. |
| [gitleaks](https://github.com/gitleaks/gitleaks) | MIT | Go binary; regex rules for secrets in git history | Rejected: secrets, not personal details; a separate binary. |
| [trufflehog](https://github.com/trufflesecurity/trufflehog) | AGPL-3.0 | Secret scanner that verifies keys live | Rejected: secrets, AGPL, and live verification sends data out. |
| [Google Cloud Sensitive Data Protection](https://cloud.google.com/sensitive-data-protection/pricing) (formerly DLP) | Closed, paid cloud service (first 1 GB a month free, then per GB) | Hosted PII detection and de-identification | Rejected: sends the profile to another company to check whether it is safe to send, needs a Google Cloud account, and is closed. |

Canadian SIN facts: SINs for temporary residents start with 9 ([canada.ca](https://www.canada.ca/en/employment-social-development/services/sin/temporary-residents.html)); the check digit is Luhn (Presidio's recognizer, above). Presidio treats 0 and 8 as never-valid first digits; I did not find the official page that says so.

## What the script checks

Email; phone (North American, 10+ digits, and `+` international); card-like numbers (13 to 19 digits, Luhn); SIN (9 digits, Luhn, first digit not 0 or 8); IBAN; account numbers (after words like "account", "member", "transit", or any run of 8+ digits); Canadian postal codes (any case, with or without space); US ZIP only next to a state code or as ZIP+4; UK postcodes; street addresses (English and French street words), unit and PO box; "password/PIN/key is ..."; money amounts only with `--money`. Names: the business name from `profile/README.md`'s title, every "Was" value in the changes file (so anything replaced is looked for again), an optional `--names` file, and capitalized words in `profile/` that are not at a sentence start, not common, and never appear in lower case ("maybe a name"). Items the owner approved go under "Okay to keep" and are not reported again. It prints; it never edits or sends.

Tried on a copy of a simulated bike-shop profile from a rehearse run (not the answer key): it found the owner's and the mechanic's first names, the business name and the city, with two noise words ("Things", "Sam-confirmed").

## Honest limits

- **Regex cannot find names it was not told about.** A customer named only in free text ("the lady from the bakery, Mrs. Okafor") is caught only if the capitalized-word guess catches it, or the agent did. Names written in lower case, or that are also common words (Rose, Victor, Grace when "grace" appears elsewhere), are missed.
- **It cannot see identity by story.** "The only Ethiopian bike shop in Thunder Bay" has no PII pattern and identifies the owner at once. That needs judgment: the agent's generalizing pass and the owner's "could someone guess it is you?" question.
- **False alarms.** Dates written as 8 digits, product codes shaped like postcodes, and capitalized tool names it does not know. The owner can mark them okay.
- **Lower-case addresses** ("45 queen st") and phone numbers without area code are missed.
- **Only text files.** Images, PDFs and spreadsheets in the share folder are listed as "not checked".
- **Not tested on real owner data**, nor on non-English profiles.

So the order of defence is: (1) the agent's careful pass, replacing with roles and logging every change; (2) the owner reading exactly what leaves, with the change list; (3) this script as a backstop for the patterned things a tired reader skims past (numbers, emails, a name that slipped through twice).
