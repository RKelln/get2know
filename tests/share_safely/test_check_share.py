"""Tests for skill/.agents/skills/share-safely/scripts/check_share.py.

Run from the repo root:
    python3 -m unittest discover -s tests/share_safely -v
or  uv run python -m unittest discover -s tests/share_safely -v

All data here is made up.
"""

import contextlib
import importlib.util
import io
import os
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(
    HERE, "..", "..", "skill", ".agents", "skills", "share-safely", "scripts", "check_share.py"
)
_spec = importlib.util.spec_from_file_location("check_share", SCRIPT)
cs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cs)


def kinds(line, money=False):
    return [k for k, _ in cs.scan_line(line, money=money)]


def luhn_complete(prefix):
    """Append the check digit that makes prefix pass Luhn."""
    for d in "0123456789":
        if cs.luhn_ok(prefix + d):
            return prefix + d
    raise AssertionError("no check digit")


class Luhn(unittest.TestCase):
    def test_known_good_and_bad(self):
        self.assertTrue(cs.luhn_ok("4111111111111111"))
        self.assertTrue(cs.luhn_ok("79927398713"))
        self.assertFalse(cs.luhn_ok("4111111111111112"))


class Patterns(unittest.TestCase):
    def test_email(self):
        self.assertEqual(cs.scan_line("write to sam.p+shop@example.ca today"),
                         [("email", "sam.p+shop@example.ca")])

    def test_phones(self):
        for text in ["(416) 555-0199", "416-555-0199", "416.555.0199", "+1 416 555 0199",
                     "4165550199", "+44 20 7946 0958"]:
            with self.subTest(text=text):
                self.assertEqual(kinds("call " + text), ["phone number"])

    def test_short_numbers_are_not_phones(self):
        self.assertEqual(kinds("we sold 120 bikes in 2025"), [])
        self.assertEqual(kinds("open 9 to 5, 6 days"), [])

    def test_card_needs_luhn(self):
        self.assertEqual(kinds("card 4111 1111 1111 1111"), ["card number"])
        self.assertEqual(kinds("card 4111-1111-1111-1111"), ["card number"])
        # Fails Luhn: not reported as a card (may still be a long number).
        self.assertNotIn("card number", kinds("ref 4111111111111112"))

    def test_sin_needs_luhn_and_valid_first_digit(self):
        sin = luhn_complete("13069254")
        spaced = "%s %s %s" % (sin[:3], sin[3:6], sin[6:])
        self.assertEqual(kinds("SIN " + spaced), ["SIN (social insurance number)"])
        self.assertEqual(kinds("SIN " + sin), ["SIN (social insurance number)"])
        bad = sin[:-1] + str((int(sin[-1]) + 1) % 10)
        self.assertNotIn("SIN (social insurance number)", kinds("SIN " + bad))
        self.assertEqual(kinds("SIN 846 454 280"), [])  # 8 is never a first digit

    def test_canadian_postal_code(self):
        for text in ["M5V 2T6", "m5v 2t6", "M5V2T6", "K1A-0B1"]:
            with self.subTest(text=text):
                self.assertEqual(kinds("Toronto ON " + text), ["postal code"])
        self.assertEqual(kinds("code D1A 1A1"), [])  # D is never used

    def test_us_zip_only_with_state_or_plus_four(self):
        self.assertEqual(kinds("Albany, NY 12207"), ["ZIP code"])
        self.assertEqual(kinds("zip 12207-1234"), ["ZIP code"])
        self.assertEqual(kinds("about 12207 kilometres"), [])

    def test_uk_postcode(self):
        self.assertEqual(kinds("London SW1A 1AA"), ["postcode"])

    def test_street_addresses(self):
        for text in ["45 Queen St W", "1200 Bloor Street West", "12 3rd Ave", "7 Maple Crescent",
                     "1200 rue Sainte-Catherine", "PO Box 77", "Unit 4B"]:
            with self.subTest(text=text):
                self.assertIn("street address", kinds("at " + text + " today"))

    def test_not_addresses(self):
        for text in ["15 minutes to drive there", "we fix 3 bikes on the line",
                     "2 people work Saturday", "open 7 days a week"]:
            with self.subTest(text=text):
                self.assertEqual(kinds(text), [])

    def test_account_numbers(self):
        self.assertIn("account number", kinds("account no. 12345-678"))
        self.assertIn("account number", kinds("Acct: 00412 3456789"))
        self.assertIn("long number (account?)", kinds("ref 98765432"))
        self.assertIn("bank account (IBAN)", kinds("IBAN GB33 BUKB 2020 1555 5555 55"))

    def test_secrets(self):
        self.assertEqual(kinds("wifi password: bikes4ever"), ["password or key"])
        self.assertEqual(kinds("the PIN is 4421"), ["password or key"])
        self.assertEqual(kinds("we never write passwords down"), [])

    def test_money_only_when_asked(self):
        line = "rent is $1,850 a month, about 2k dollars with power"
        self.assertEqual(kinds(line), [])
        self.assertEqual(kinds(line, money=True).count("money amount"), 1)
        self.assertIn("money amount", kinds("we made $4.5k in May", money=True))
        self.assertIn("money amount", kinds("we made 300 dollars", money=True))

    def test_one_number_reported_once(self):
        found = cs.scan_line("card 4111111111111111")
        self.assertEqual(len(found), 1)


class ChangesFile(unittest.TestCase):
    def test_parse_was_column_and_okay_list(self):
        text = """# Changes: builder-2026-10-29

## Changes
| # | File | Was | Now |
|---|---|---|---|
| 1 | how-we-work.md | Sam Rivera | the part-time mechanic |
| 2 | how-we-work.md | `sam@example.ca` | (removed) |
| 3 | ideas.md | (whole line removed) | |
| 4 | limits.md | Jo | a customer |

## Okay to keep
- Spoke Street Cycles
- (416) 555-0100
"""
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.changes.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            was, okay = cs.parse_changes_file(path)
        self.assertEqual(was, ["Sam Rivera", "sam@example.ca"])  # "Jo" too short; "(..." skipped
        self.assertEqual(okay, ["Spoke Street Cycles", "(416) 555-0100"])


    def test_removed_private_line_is_searched(self):
        text = """## Changes
| # | File | Was | Now |
|---|---|---|---|
| 3 | limits.md | - Never tell anyone about the loan from my sister (said: "nobody knows") | (removed, owner asked) |
"""
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.changes.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            was, _ = cs.parse_changes_file(path)
            self.assertEqual(was, ["Never tell anyone about the loan from my sister"])
            share = os.path.join(d, "share")
            os.makedirs(os.path.join(share, "briefs"))
            with open(os.path.join(share, "briefs", "loan-tracker.md"), "w", encoding="utf-8") as f:
                f.write("## Must never\n- never tell anyone about the loan from my sister (said: \"x\")\n")
            _, findings, _ = cs.scan_folder(share, names=was)
        self.assertEqual(
            findings,
            [(os.path.join("briefs", "loan-tracker.md"), 2, "removed before, still here",
              "Never tell anyone about the loan from my sister")],
        )


class Harvest(unittest.TestCase):
    def test_names_from_profile(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "how-we-work.md"), "w", encoding="utf-8") as f:
                f.write("# Shop: how we work\n## People\n"
                        "- The owner works with Priya on Saturdays (said: \"Priya does the books\")\n"
                        "- A customer named Okafor pays late; we use Square and Excel.\n"
                        "- Summer is busy. We bank with the Credit union.\n"
                        "- We keep a square of cardboard by the door.\n")
            names = cs.harvest_profile_names(d)
        # Noise is expected: "Credit" (from "Credit union") is reported as a maybe-name.
        self.assertIn("Priya", names)
        self.assertIn("Okafor", names)
        self.assertNotIn("Priya's", names)
        for word in ["Saturdays", "Square", "Excel", "Summer", "Shop", "People"]:
            self.assertNotIn(word, names)


class Folder(unittest.TestCase):
    def make_tree(self, d, share_text, changes=None):
        os.makedirs(os.path.join(d, "profile"))
        with open(os.path.join(d, "profile", "how-we-work.md"), "w", encoding="utf-8") as f:
            f.write("## People\n- The owner works with Priya and a mechanic.\n")
        share = os.path.join(d, "share", "builder-2026-10-29")
        os.makedirs(share)
        with open(os.path.join(share, "how-we-work.md"), "w", encoding="utf-8") as f:
            f.write(share_text)
        with open(os.path.join(share, "photo.png"), "wb") as f:
            f.write(b"\x89PNG")
        if changes is not None:
            with open(share + ".changes.md", "w", encoding="utf-8") as f:
                f.write(changes)
        return share

    def run_main(self, args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cs.main(args)
        return code, out.getvalue()

    def test_clean_folder(self):
        with tempfile.TemporaryDirectory() as d:
            share = self.make_tree(d, "## People\n- The owner and the bookkeeper.\n")
            code, out = self.run_main([share])
        self.assertEqual(code, 0)
        self.assertIn("Found nothing", out)
        self.assertIn("photo.png", out)  # says what it could not check

    def test_finds_leftovers(self):
        changes = "## Changes\n| # | File | Was | Now |\n|---|---|---|---|\n| 1 | how-we-work.md | Lee Chan | a customer |\n"
        with tempfile.TemporaryDirectory() as d:
            share = self.make_tree(
                d,
                "## People\n- Priya keeps the books.\n- A customer, lee chan, pays late.\n"
                "- Email shop@example.ca\n",
                changes=changes,
            )
            code, out = self.run_main([share])
        self.assertEqual(code, 1)
        self.assertIn("maybe a name (from your profile): Priya\n      in how-we-work.md line 2\n", out)
        self.assertIn("removed before, still here: Lee Chan\n      in how-we-work.md line 3\n", out)
        self.assertIn("email: shop@example.ca\n      in how-we-work.md line 4\n", out)

    def test_groups_repeats(self):
        with tempfile.TemporaryDirectory() as d:
            share = self.make_tree(d, "Priya opens.\nThen Priya's van.\nAsk Priya.\n")
            code, out = self.run_main([share])
        self.assertIn("Priya\n      in how-we-work.md lines 1, 2, 3\n", out)
        self.assertIn("Found 1 thing(s) to look at, in 3 line(s)", out)

    def test_business_name(self):
        with tempfile.TemporaryDirectory() as d:
            share = self.make_tree(d, "Welcome to Spoke & Chain.\n")
            with open(os.path.join(d, "profile", "README.md"), "w", encoding="utf-8") as f:
                f.write("# Spoke & Chain: profile folder\nMade with Get2Know.\n")
            code, out = self.run_main([share])
        self.assertEqual(code, 1)
        self.assertIn("business name (from your profile): Spoke & Chain", out)

    def test_allow_list(self):
        changes = "## Okay to keep\n- shop@example.ca\n"
        with tempfile.TemporaryDirectory() as d:
            share = self.make_tree(d, "Email shop@example.ca\n", changes=changes)
            code, out = self.run_main([share, "--no-profile"])
        self.assertEqual(code, 0, out)

    def test_names_file(self):
        with tempfile.TemporaryDirectory() as d:
            share = self.make_tree(d, "Ask Dmitri about it.\n")
            names = os.path.join(d, "names.txt")
            with open(names, "w", encoding="utf-8") as f:
                f.write("# people\nDmitri\n")
            code, out = self.run_main([share, "--names", names, "--no-profile"])
        self.assertEqual(code, 1)
        self.assertIn("Dmitri", out)

    def test_missing_folder(self):
        code, out = self.run_main(["/no/such/folder"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
