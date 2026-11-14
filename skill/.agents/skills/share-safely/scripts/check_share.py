#!/usr/bin/env python3
"""Second check for a share folder: look for private details that were missed.

Part of the Get2Know "share-safely" skill. Standard library only, Python 3.8+.

    python3 check_share.py share/builder-2026-10-29
    uv run check_share.py share/builder-2026-10-29 --money

It reads every text file in the folder and prints each line that looks like
an email, phone number, card number, SIN, postal code, street address,
account number, password, or a name. Names come from:
  - the "Was" column of the changes file next to the folder
    (share/<name>.changes.md), so anything the AI replaced is checked again;
  - an optional --names file (one name per line);
  - capitalized words in the original profile/ folder ("maybe a name");
  - the business name in the title of profile/README.md.

It never changes a file and never sends anything. It only prints.
Exit code: 0 nothing found, 1 something to look at, 2 could not run.

This check only knows patterns. It misses names it was not told about,
details written in words ("my neighbour on Elm"), and anything that
identifies a business by its story. The AI pass and the owner's own read
are the main defence; this is a backstop.

Pattern sources (see docs/research/pii-checks.md): Luhn card and SIN checks
and the Canadian postal code letters follow Microsoft Presidio's
recognizers (MIT licence); the street-address and PO box shapes are adapted
from CommonRegex (MIT licence). Written fresh, not copied.
"""

import argparse
import os
import re
import sys

TEXT_EXTENSIONS = {".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml", ".toml", ".html", ".py", ".sh", ""}

# ---------------------------------------------------------------- patterns

EMAIL = re.compile(r"[A-Za-z0-9._%+'-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")

# Card-like: 13 to 19 digits, spaces or dashes allowed between them. Luhn checked.
CARD = re.compile(r"(?<![\d-])\d(?:[ -]?\d){12,18}(?![\d])")

# Canadian SIN: 9 digits, first digit not 0 or 8, as 123 456 789 / 123-456-789 /
# 123456789. Luhn checked. (Presidio ca_sin_recognizer uses the same shape.)
SIN = re.compile(r"(?<![\d-])[1-79]\d{2}([ -]?)\d{3}\1\d{3}(?![\d-])")

# Phone: North American (416) 555-0199, 416.555.0199, +1 416 555 0199, and
# international numbers starting with +.
PHONE = re.compile(
    r"(?<![\w+])(?:\+?1[ .-]?)?\(?[2-9]\d{2}\)?[ .-]?\d{3}[ .-]?\d{4}(?!\d)"
    r"|(?<![\w+])\+\d{1,3}(?:[ .-]?\(?\d{1,4}\)?){2,5}(?!\d)"
)

# Canadian postal code. Letters D F I O Q U never appear; W and Z never first.
CA_POSTAL = re.compile(
    r"\b[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d\b",
    re.IGNORECASE,
)

US_STATES = (
    "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO "
    "MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC"
).split()
# US ZIP only next to a state code, or as ZIP+4: a bare 5-digit number is
# usually an amount.
US_ZIP = re.compile(r"\b(?:(?:" + "|".join(US_STATES) + r")\s+\d{5}(?:-\d{4})?|\d{5}-\d{4})\b")

UK_POSTCODE = re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]? ?\d[ABD-HJLNP-UW-Z]{2}\b")

STREET_WORDS = (
    "street|st|avenue|ave|road|rd|drive|dr|boulevard|blvd|lane|ln|court|ct|crescent|cres|"
    "place|pl|way|terrace|trail|trl|parkway|pkwy|highway|hwy|circle|cir|square|sq|"
    "gardens|gdns|grove|close|row|line|sideroad|concession"
)
# The street name must start with a capital or a digit ("45 Queen St W",
# "12 3rd Ave"), so "15 minutes to drive" is not an address. Lower-case
# addresses ("45 queen st") are missed: a known limit.
STREET = re.compile(
    r"\b\d{1,5}[A-Za-z]?(?:-\d{1,5})?,?\s+(?:[A-Z0-9][A-Za-z0-9'.-]*\s+){1,4}(?i:" + STREET_WORDS + r")\b\.?"
    r"(?:\s+(?i:north|south|east|west)\b|\s+[NSEW]\b)?"
)
STREET_FR = re.compile(r"\b\d{1,5},?\s+(?:rue|avenue|boulevard|chemin|route)\s+[A-Za-zÀ-ÿ'-]+", re.IGNORECASE)
UNIT = re.compile(r"\b(?:unit|suite|apt|apartment)\.?\s*#?\s*\d+[A-Za-z]?\b", re.IGNORECASE)
PO_BOX = re.compile(r"\bP\.?\s?O\.?\s?Box\s+\d+", re.IGNORECASE)

# Account numbers: a long run of digits, or digits after an account word.
LONG_NUMBER = re.compile(r"(?<![\d.,$-])\d{8,}(?![\d.,-])")
ACCOUNT = re.compile(
    r"\b(?:account|acct|a/c|transit|institution|routing|iban|member|policy|licen[cs]e|"
    r"customer|client)\s*(?:no\.?|number|#|num)?\s*[:#]?\s*([A-Z]{0,4}[\d][\d -]{3,}\d)",
    re.IGNORECASE,
)
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,4})?\b")

SECRET = re.compile(
    r"\b(?:password|passwd|passcode|pin|api[ _-]?key|secret|token|login)\b\s*(?:is|:|=)\s*\S+",
    re.IGNORECASE,
)

MONEY = re.compile(
    r"(?:[$€£]\s?\d[\d,]*(?:\.\d+)?\s?[kKmM]?\b)"
    r"|(?:\b\d[\d,]*(?:\.\d+)?\s?(?:dollars|bucks|CAD|USD|EUR|GBP)\b)",
    re.IGNORECASE,
)


def luhn_ok(digits):
    """True if the digit string passes the Luhn checksum."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def only_digits(text):
    return "".join(c for c in text if c.isdigit())


# ---------------------------------------------------------------- names

# Words that are often capitalized but are not names. Kept short on purpose:
# a word that appears in lower case anywhere in the files is also skipped.
COMMON_CAPS = set(
    """
    I AI GAP CONFLICT README TODO OK Okay Yes No Not None Notes Note
    Monday Tuesday Wednesday Thursday Friday Saturday Sunday Mon Tue Wed Thu Fri Sat Sun
    January February March April May June July August September October November December
    Jan Feb Mar Apr Jun Jul Aug Sep Sept Oct Nov Dec
    Christmas Easter Thanksgiving Canada Canadian English French Ontario Quebec
    Mr Mrs Ms Dr St The A An And Or But If When Then So We Our Us They Their You Your
    He She His Her It Its This That These Those What Who Why How Where Which
    Summary People Tools Money Customers Clients Members Ideas Limits Log Status
    Excel Word Google Gmail Outlook Microsoft Apple iPhone Android Facebook Instagram
    WhatsApp Square Shopify QuickBooks Wave Xero Etsy Amazon Interac PayPal Stripe
    Claude ChatGPT Codex OpenAI Anthropic Get2Know HST GST PST CRA SIN PDF CSV
    """.split()
)

CAP_WORD = re.compile(r"\b[A-Z][a-z]+(?:['’-][A-Z]?[a-z]+)?\b")
SENTENCE_START = re.compile(r"(?:^|[.!?:]\s+|^\s*(?:#+|[-*+]|\d+[.)]|\|)\s*|\|\s*|[\"“(]\s*)$")


def harvest_profile_names(profile_dir):
    """Capitalized words in profile/ that are probably names.

    Skips words at the start of a sentence, line, heading or list item,
    common capitalized words, and any word that also appears in lower case.
    Noisy by design: results are labelled "maybe a name".
    """
    texts = [text for _, text in read_text_files(profile_dir)]
    lower_words = set()
    candidates = set()
    for text in texts:
        lower_words.update(re.findall(r"\b[a-z][a-z'’-]+\b", text))
        for line in text.splitlines():
            for m in CAP_WORD.finditer(line):
                if SENTENCE_START.search(line[: m.start()]):
                    continue
                candidates.add(re.sub(r"['’]s$", "", m.group(0)))  # Sam's -> Sam
    return {
        w for w in candidates
        if w not in COMMON_CAPS and w.rstrip("s") not in COMMON_CAPS
        and w.lower() not in lower_words and len(w) > 2
    }


def business_name(profile_dir):
    """The name in profile/README.md's title ("# Spoke Shop: profile folder"), or None."""
    try:
        with open(os.path.join(profile_dir, "README.md"), encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.match(r"^#\s+(.+?):\s*profile folder\s*$", line.strip(), re.IGNORECASE)
                if m and m.group(1).strip() not in ("<Name>", "Name"):
                    return m.group(1).strip()
    except OSError:
        pass
    return None


CHANGE_TABLE_HEADER = re.compile(r"^\s*\|(.+)\|\s*$")


def parse_changes_file(path):
    """Return (was_values, okay_values) from a changes file.

    was_values: every cell in a table column headed "Was", including whole
    removed lines, except notes in brackets such as "(whole line removed)".
    okay_values: every "- item" line under a heading containing "Okay to keep".
    """
    was, okay = [], []
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
    except OSError:
        return was, okay
    was_col = None
    in_okay = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            in_okay = "okay to keep" in stripped.lower()
            was_col = None
            continue
        if in_okay and stripped.startswith(("- ", "* ")):
            item = clean_cell(stripped[2:])
            if item:
                okay.append(item)
            continue
        m = CHANGE_TABLE_HEADER.match(line)
        if not m:
            was_col = None
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if was_col is None:
            lowered = [c.lower() for c in cells]
            if "was" in lowered:
                was_col = lowered.index("was")
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue  # the |---|---| line
        if was_col < len(cells):
            value = clean_was(cells[was_col])
            if value and len(value) > 2 and not value.startswith("("):
                was.append(value)
    return was, okay


LIST_MARK = re.compile(r"^(?:[-*+]|\d+[.)])\s+")
TRAILING_MARK = re.compile(r"\s*\((?:said|file|draft|guess)\b[^()]*(?:\([^()]*\)[^()]*)*\)\s*$", re.IGNORECASE)


def clean_cell(text):
    text = text.strip().strip("`").strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'“”":
        text = text[1:-1].strip()
    return text


def clean_was(text):
    """A "Was" cell as text to search for: a whole removed line (say a private
    limits line) is searched without its list mark and its evidence marks,
    because another file may repeat it in other words around it."""
    text = clean_cell(text)
    text = LIST_MARK.sub("", text)
    while True:
        shorter = TRAILING_MARK.sub("", text)
        if shorter == text:
            break
        text = shorter
    return text.strip()


def read_names_file(path):
    names = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                names.append(line)
    return names


# ---------------------------------------------------------------- scanning

def read_text_files(folder):
    """Yield (relative path, text) for each text file under folder."""
    for root, dirs, files in os.walk(folder):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for name in sorted(files):
            if name.startswith("."):
                continue
            path = os.path.join(root, name)
            if os.path.splitext(name)[1].lower() not in TEXT_EXTENSIONS:
                yield os.path.relpath(path, folder), None
                continue
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    yield os.path.relpath(path, folder), f.read()
            except OSError:
                yield os.path.relpath(path, folder), None


def phrase_pattern(phrase):
    """Whole-word, case-insensitive match that ignores extra spaces."""
    parts = [re.escape(p) for p in phrase.split()]
    body = r"\s+".join(parts)
    left = r"(?<!\w)" if phrase[:1].isalnum() else ""
    right = r"(?!\w)" if phrase[-1:].isalnum() else ""
    return re.compile(left + body + right, re.IGNORECASE)


def scan_line(line, money=False):
    """Return a list of (kind, text) found in one line of text."""
    found = []
    taken = []  # spans already reported, so one number is not reported twice

    def free(span):
        return all(span[1] <= a or span[0] >= b for a, b in taken)

    def add(kind, m, group=0):
        span = m.span(group)
        if free(span):
            taken.append(span)
            found.append((kind, m.group(group).strip()))

    for m in EMAIL.finditer(line):
        add("email", m)
    for m in CARD.finditer(line):
        if luhn_ok(only_digits(m.group(0))):
            add("card number", m)
    for m in SIN.finditer(line):
        if luhn_ok(only_digits(m.group(0))):
            add("SIN (social insurance number)", m)
    for m in PHONE.finditer(line):
        if len(only_digits(m.group(0))) >= 10:
            add("phone number", m)
    for m in IBAN.finditer(line):
        add("bank account (IBAN)", m)
    for m in ACCOUNT.finditer(line):
        add("account number", m, 1)
    for m in LONG_NUMBER.finditer(line):
        add("long number (account?)", m)
    for m in CA_POSTAL.finditer(line):
        add("postal code", m)
    for m in US_ZIP.finditer(line):
        add("ZIP code", m)
    for m in UK_POSTCODE.finditer(line):
        add("postcode", m)
    for pattern in (STREET, STREET_FR, PO_BOX, UNIT):
        for m in pattern.finditer(line):
            add("street address", m)
    for m in SECRET.finditer(line):
        add("password or key", m)
    if money:
        for m in MONEY.finditer(line):
            add("money amount", m)
    return found


def scan_folder(folder, names=(), maybe_names=(), allow=(), money=False, business=None):
    """Scan every text file in folder. Return (files_checked, findings, skipped).

    findings: list of (file, line number, kind, text).
    """
    allow_lower = {a.lower() for a in allow}
    name_patterns = [(n, phrase_pattern(n)) for n in sorted(set(names), key=len, reverse=True)]
    maybe_patterns = [(n, phrase_pattern(n)) for n in sorted(set(maybe_names) - set(names))]
    business_pattern = phrase_pattern(business) if business else None
    findings, skipped, checked = [], [], 0
    for rel, text in read_text_files(folder):
        if text is None:
            skipped.append(rel)
            continue
        checked += 1
        for lineno, line in enumerate(text.splitlines(), 1):
            hits = scan_line(line, money=money)
            for name, pat in name_patterns:
                if pat.search(line):
                    hits.append(("removed before, still here", name))
            if business_pattern is not None and business_pattern.search(line):
                hits.append(("business name (from your profile)", business))
            for name, pat in maybe_patterns:
                if pat.search(line):
                    hits.append(("maybe a name (from your profile)", name))
            for kind, value in hits:
                if value.lower() in allow_lower:
                    continue
                findings.append((rel, lineno, kind, value))
    return checked, findings, skipped


# ---------------------------------------------------------------- command line

def default_changes_file(folder):
    folder = os.path.normpath(folder)
    return folder + ".changes.md"


def default_profile(folder):
    guess = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(folder))), "profile")
    return guess if os.path.isdir(guess) else None


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Look for private details left in a share folder. Prints only; changes nothing."
    )
    p.add_argument("folder", help="the share folder to check, e.g. share/builder-2026-10-29")
    p.add_argument("--changes", help="changes file (default: <folder>.changes.md)")
    p.add_argument("--names", help="a text file with one name per line to look for")
    p.add_argument("--profile", help="the original profile folder, to find likely names (default: ../../profile)")
    p.add_argument("--no-profile", action="store_true", help="do not look for names from the profile")
    p.add_argument("--money", action="store_true", help="also flag money amounts")
    p.add_argument("--allow", action="append", default=[], help="text that is okay to keep (repeat as needed)")
    args = p.parse_args(argv)

    if not os.path.isdir(args.folder):
        print("I could not find the folder: %s" % args.folder)
        return 2

    names, allow = [], list(args.allow)
    changes = args.changes or default_changes_file(args.folder)
    if os.path.isfile(changes):
        was, okay = parse_changes_file(changes)
        names.extend(was)
        allow.extend(okay)
    elif args.changes:
        print("I could not find the changes file: %s" % changes)
        return 2
    if args.names:
        if not os.path.isfile(args.names):
            print("I could not find the names file: %s" % args.names)
            return 2
        names.extend(read_names_file(args.names))

    maybe, business = set(), None
    profile = None if args.no_profile else (args.profile or default_profile(args.folder))
    if profile:
        if not os.path.isdir(profile):
            print("I could not find the profile folder: %s" % profile)
            return 2
        maybe = harvest_profile_names(profile)
        business = business_name(profile)

    checked, findings, skipped = scan_folder(
        args.folder, names=names, maybe_names=maybe, allow=allow, money=args.money,
        business=business,
    )

    print("Checked %d file(s) in %s." % (checked, args.folder))
    print("Names and removed text looked for: %d. Possible names from the profile: %d." % (len(set(names)), len(maybe)))
    for rel in skipped:
        print("Not checked (not a text file): %s. Open it yourself, or leave it out." % rel)
    if not findings:
        print("Found nothing. This check only knows some patterns.")
        print("Still read every file yourself before you send it.")
        return 0
    groups = {}
    for rel, lineno, kind, value in findings:
        groups.setdefault((kind, value), {}).setdefault(rel, []).append(lineno)
    print("Found %d thing(s) to look at, in %d line(s):" % (len(groups), len(findings)))
    print()
    for (kind, value), where in groups.items():
        print("  %s: %s" % (kind, value))
        places = []
        for rel, lines in where.items():
            word = "line" if len(lines) == 1 else "lines"
            places.append("%s %s %s" % (rel, word, ", ".join(str(n) for n in lines)))
        print("      in " + "; ".join(places))
    print()
    print("Some of these may be fine. For each one: change it, or tell the AI it is okay to keep.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
