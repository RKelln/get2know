"""Tests for the quote matching in tests/rehearse/checks.py (quotes_are_verbatim, DESIGN D59). Standard library only.

Run: python3 -m unittest tests/quotes/test_quotes.py

A (said: "...") quote may fix the owner's spelling, but must not add, drop, swap or move a word.
checks.py imports rehearse's Check; a stand-in is enough here, so rehearse need not be installed.
"""

import sys
import types
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tests" / "rehearse"))
if "rehearse.checks" not in sys.modules:
    stub = types.ModuleType("rehearse.checks")
    stub.Check = type("Check", (), {})
    sys.modules.setdefault("rehearse", types.ModuleType("rehearse"))
    sys.modules["rehearse.checks"] = stub

import checks  # noqa: E402

OWNER = [
    "i dont no who has payed, ive never checked",
    "We was slammed saturday and the tune up was $89",
    "I hate chasing them",
    "the keys are in the box by the door",
]
TURNS = [f" {checks._qnorm(t)} " for t in OWNER]


def match(quote):
    return checks._quote_match(quote, TURNS)


class SpellingFixesPass(unittest.TestCase):
    def test_exact_words(self):
        self.assertEqual(match("I hate chasing them"), "exact")
        self.assertEqual(match("we was slammed Saturday"), "exact")  # capitals and grammar left as said

    def test_misspellings_fixed(self):
        self.assertEqual(match("I don't know who has paid"), "fixed")  # dont, no -> know, payed
        self.assertEqual(match("I've never checked"), "fixed")

    def test_gaps_still_allowed(self):
        self.assertEqual(match("I don't know ... I've never checked"), "fixed")


class RewordingFails(unittest.TestCase):
    def test_swapped_word(self):
        self.assertIsNone(match("I dislike chasing them"))

    def test_grammar_tidied(self):
        self.assertIsNone(match("We were slammed Saturday"))

    def test_dropped_word(self):
        self.assertIsNone(match("I don't know who paid"))

    def test_reordered(self):
        self.assertIsNone(match("chasing them I hate"))

    def test_number_changed(self):
        self.assertIsNone(match("the tune up was $79"))

    def test_two_short_swaps(self):
        # One short one-letter swap (in -> on) in nine words is allowed; that is the known limit (D59).
        self.assertEqual(match("the keys are on the box by the door"), "fixed")
        self.assertIsNone(match("the keys are on the box at the door"))


if __name__ == "__main__":
    unittest.main()
