"""Goldfish lenses on saved profiles (DESIGN D56, D57): an offline experiment, no interview.

Each reader gets a fresh `codex exec` in a temporary folder that holds only one `profile/`, and
returns up to 5 follow-up questions. Readers: six lenses, and six general readers with no lens
(the same prompt, sampled six times), so both groups cost the same.

A judge, which also gets the answer key, then marks each key item found or missing (quoting the
profile line when found, which the code checks), labels every question, and says which key items
it points at. It sees the 12 question sets only as A-L. It reports numbers, verdicts and profile
quotes, never key text. It runs 3 times per profile; the report takes the majority.

    python3 tests/goldfish/run.py            # list what would run; calls nothing
    python3 tests/goldfish/run.py --live     # run what is missing in out/ (spends codex usage)
    python3 tests/goldfish/run.py --report   # summarise out/ without calling anything
    add --compare to any of these for the interviewer's own plan against the goldfish

Outputs go to tests/goldfish/out/ (not tracked). Existing outputs are kept, never rerun.
"""

import argparse
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
REHEARSE = HERE.parent / "rehearse"
OUT = HERE / "out"
MODEL = "gpt-6.1-sol"
LENSES = ["money", "customers", "time", "risk", "ai-scout", "newcomer"]
GENERALISTS = ["generalist"] + [f"generalist-{i}" for i in range(2, 7)]
READERS = LENSES + GENERALISTS
JUDGE_RUNS = 3

# Two experiments share the readers' outputs. "lenses": six lenses against six generalists (D57).
# "compare": the same sets plus the interviewer's own next-session plan (its "Next questions" and
# "Ask first" notes, written as a set by hand in interviewer/), judged with a conversation key for
# the bike shop instead of the file-analysis key.
EXPERIMENTS = {
    "lenses": {"judge": "judge", "readers": READERS},
    "compare": {"judge": "compare", "readers": READERS + ["interviewer"]},
}
VERDICTS = ["key-hit", "useful", "answered", "leading", "unsafe", "unclear"]

RUNS = REHEARSE / "runs"
PROFILES = {
    "bike-cooperative": (RUNS / "2026-10-29-get2know-bike-shop-codex-skill-debadcb-cooperative-1/artifacts/files/profile",
                         REHEARSE / "fixture/answer-key.md"),
    "bike-hurried": (RUNS / "2026-10-29-get2know-bike-shop-codex-skill-bbf621c-hurried-1/artifacts/files/profile",
                     REHEARSE / "fixture/answer-key.md"),
    "collective-first": (RUNS / "2026-10-29-get2know-collective-first-codex-skill-295cce8-cooperative-1/artifacts/files/profile",
                         REHEARSE / "keys/collective.md"),
    "collective-resume-start": (REHEARSE / "scenarios/collective-resume/profile",
                                REHEARSE / "keys/collective.md"),
}

JUDGE = """You judge follow-up questions written by fresh readers who saw only `profile/`.

Files here:
- `profile/`: what an interviewer wrote about a business after one session.
- `key.md`: what a good interview should find out about this business. Only you see it.
- `sets/`: question sets A, B, C ... from different readers. Each question has a number.

1. Read `key.md` and split it into its separate items, numbered 1, 2, 3 ... in the order they appear.
2. For each key item, read all of `profile/` and decide: `found` if the profile states it (fully, or
   enough that the interviewer clearly knows it), else `missing` (absent, only hinted, or wrong).
   For `found`, copy one line from the profile, word for word, that shows it. Leave the quote empty
   for `missing`.
3. Label every question in every set with exactly one verdict:
   - `key-hit`: asking it would likely bring out a key item marked `missing`.
   - `useful`: a fair, useful question, but not about a missing key item.
   - `answered`: the profile already answers it.
   - `leading`: it states or suggests an answer the profile does not support.
   - `unsafe`: it asks for passwords, account or card numbers, or private details about a person.
   - `unclear`: too vague or too hard for an owner to answer.
   For a `key-hit`, give the missing key item numbers it points at.

Never quote, paraphrase or describe the key in your answer: item numbers, verdicts and profile
quotes only. Write no files.
"""

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["items", "questions"],
    "properties": {
        "items": {"type": "array", "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["n", "status", "profile_quote"],
            "properties": {
                "n": {"type": "integer"},
                "status": {"type": "string", "enum": ["found", "missing"]},
                "profile_quote": {"type": "string"},
            },
        }},
        "questions": {"type": "array", "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["set", "n", "verdict", "key_items"],
            "properties": {
                "set": {"type": "string"},
                "n": {"type": "integer"},
                "verdict": {"type": "string", "enum": VERDICTS},
                "key_items": {"type": "array", "items": {"type": "integer"}},
            },
        }},
    },
}


def codex(workdir: Path, prompt: str, out: Path, schema: Path | None = None) -> None:
    argv = ["codex", "exec", "--skip-git-repo-check", "--ignore-user-config", "--ignore-rules",
            "--ephemeral", "-C", str(workdir), "-s", "read-only", "-m", MODEL, "-o", str(out)]
    if schema:
        argv += ["--output-schema", str(schema)]
    log = out.with_suffix(".log")
    with log.open("w") as f:
        subprocess.run(argv + ["-"], input=prompt, text=True, stdout=f, stderr=subprocess.STDOUT,
                       check=True, timeout=900)


def reader_prompt(reader: str) -> str:
    lens = "generalist" if reader.startswith("generalist") else reader
    common = (HERE / "common.md").read_text()
    return common.replace("{LENS}", (HERE / "lenses" / f"{lens}.md").read_text().strip())


def run_reader(label: str, reader: str) -> str:
    profile, _ = PROFILES[label]
    out = OUT / label / f"{reader}.md"
    if out.exists():
        return f"{label}/{reader}: kept"
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(profile, Path(tmp) / "profile")
        codex(Path(tmp), reader_prompt(reader), out)
    return f"{label}/{reader}: {len(questions(out))} questions"


def questions(path: Path) -> list[str]:
    return re.findall(r"^\s*\d+\.\s*Q:\s*(.+)$", path.read_text(), re.M) if path.exists() else []


CONVERSATION_KEYS = {"bike-cooperative": REHEARSE / "keys/bike-shop-conversation.md",
                     "bike-hurried": REHEARSE / "keys/bike-shop-conversation.md"}


def key_for(label: str, exp: str) -> Path:
    return CONVERSATION_KEYS.get(label, PROFILES[label][1]) if exp == "compare" else PROFILES[label][1]


def set_file(label: str, reader: str) -> Path:
    return HERE / "interviewer" / f"{label}.md" if reader == "interviewer" else OUT / label / f"{reader}.md"


def blocks(path: Path) -> dict[int, str]:
    """Question number -> its Line: text."""
    found = re.findall(r"^\s*(\d+)\.\s*Q:.*?\n\s*Line:\s*(.+)$", path.read_text(), re.M)
    return {int(n): line for n, line in found}


def set_names(label: str, exp: str = "lenses") -> dict[str, str]:
    """Reader -> anonymous set letter, fixed per profile so the judge does not see reader names."""
    order = EXPERIMENTS[exp]["readers"][:]
    random.Random(label).shuffle(order)
    return {reader: chr(ord("A") + i) for i, reader in enumerate(order)}


def judge_path(label: str, run: int, exp: str = "lenses") -> Path:
    return OUT / label / f"{EXPERIMENTS[exp]['judge']}-{run}.json"


def run_judge(label: str, run: int, exp: str = "lenses") -> str:
    profile, key = PROFILES[label][0], key_for(label, exp)
    out = judge_path(label, run, exp)
    if out.exists():
        return f"{label}/{out.stem}: kept"
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work"
        shutil.copytree(profile, work / "profile")
        shutil.copy(key, work / "key.md")
        (work / "sets").mkdir()
        for reader, letter in set_names(label, exp).items():
            shutil.copy(set_file(label, reader), work / "sets" / f"{letter}.md")
        schema = Path(tmp) / "schema.json"
        schema.write_text(json.dumps(SCHEMA))
        codex(work, JUDGE, out, schema)
    return f"{label}/{out.stem}: done"


def norm(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", text).strip().lower()


def read_judge(label: str, run: int, exp: str = "lenses") -> dict | None:
    """One judge run: missing items (a `found` whose quote is not in the profile counts as missing),
    bad quotes, verdicts per reader, and the missing items each reader's questions point at."""
    path = judge_path(label, run, exp)
    if not path.exists():
        return None
    readers = EXPERIMENTS[exp]["readers"]
    data = json.loads(path.read_text())
    profile_text = norm(" ".join(p.read_text() for p in PROFILES[label][0].glob("*.md")))
    items, missing, bad = set(), set(), 0
    for item in data["items"]:
        items.add(item["n"])
        quote = norm(item["profile_quote"].strip().lstrip("-* ").strip('"'))
        if item["status"] == "missing":
            missing.add(item["n"])
        elif len(quote) < 15 or quote not in profile_text:
            missing.add(item["n"])
            bad += 1
    letters = {letter: reader for reader, letter in set_names(label, exp).items()}
    verdicts = {reader: {v: 0 for v in VERDICTS} for reader in readers}
    hits = {reader: set() for reader in readers}
    question_hits = []   # (reader, question number, missing items it points at)
    for q in data["questions"]:
        reader = letters.get(q["set"].strip().upper()[:1])
        if not reader:
            continue
        verdicts[reader][q["verdict"]] += 1
        if q["verdict"] == "key-hit":
            hits[reader] |= set(q["key_items"]) & missing
            question_hits.append((reader, q["n"], set(q["key_items"]) & missing))
    return {"items": items, "missing": missing, "bad_quotes": bad, "verdicts": verdicts, "hits": hits,
            "question_hits": question_hits}


def majority(sets: list[set]) -> set:
    return {x for x in set().union(*sets) if sum(x in s for s in sets) * 2 > len(sets)}


def report() -> None:
    totals = {reader: {v: 0 for v in VERDICTS} for reader in READERS}
    for label in PROFILES:
        runs = [j for j in (read_judge(label, r) for r in range(1, JUDGE_RUNS + 1)) if j]
        if not runs:
            print(f"\n{label}: no judge runs yet")
            continue
        print(f"\n{label}: key has {'/'.join(str(len(j['items'])) for j in runs)} items by run;"
              f" missing {'/'.join(str(len(j['missing'])) for j in runs)};"
              f" 'found' quotes not in the profile {'/'.join(str(j['bad_quotes']) for j in runs)}")
        missing = majority([j["missing"] for j in runs])
        lens_hits = majority([set().union(*(j["hits"][r] for r in LENSES)) for j in runs]) & missing
        gen_hits = majority([set().union(*(j["hits"][r] for r in GENERALISTS)) for j in runs]) & missing
        print(f"  majority: {len(missing)} missing; six lenses reach {len(lens_hits)},"
              f" six generalists reach {len(gen_hits)}; only lenses {len(lens_hits - gen_hits)},"
              f" only generalists {len(gen_hits - lens_hits)}, either {len(lens_hits | gen_hits)}")
        for group, readers in (("lens", LENSES), ("gen", GENERALISTS)):
            parts = []
            for r in readers:
                reached = majority([j["hits"][r] for j in runs]) & missing
                parts.append(f"{r.replace('generalist', 'g')}:{len(reached)}")
            print(f"  {group}: " + "  ".join(parts))
        for j in runs:
            for r in READERS:
                for v in VERDICTS:
                    totals[r][v] += j["verdicts"][r][v]
    print(f"\nVerdicts by reader, all profiles, summed over judge runs:")
    print("  " + " ".join(f"{v:>12}" for v in ["reader", *VERDICTS]))
    for group, readers in (("six lenses", LENSES), ("six generalists", GENERALISTS)):
        for r in readers:
            print(f"  {r:>12} " + " ".join(f"{totals[r][v]:>12}" for v in VERDICTS))
        print(f"  {group:>12} " + " ".join(f"{sum(totals[r][v] for r in readers):>12}" for v in VERDICTS))


def report_compare() -> None:
    """The interviewer's own plan against the goldfish. A goldfish question whose Line is a GAP: line
    asks about something already on the profile's open list, so only non-GAP hits count as new."""
    rows = []
    for label in PROFILES:
        runs = [j for j in (read_judge(label, r, "compare") for r in range(1, JUDGE_RUNS + 1)) if j]
        if not runs:
            print(f"\n{label}: no compare runs yet")
            continue
        missing = majority([j["missing"] for j in runs])

        def reached(readers, skip_gap=False):
            per_run = []
            for j in runs:
                got = set()
                for reader, n, its in j["question_hits"]:
                    if reader in readers and not (skip_gap and "GAP" in blocks(set_file(label, reader)).get(n, "")):
                        got |= its
                per_run.append(got)
            return majority(per_run) & missing

        plan = reached(["interviewer"])
        one = reached(["generalist"])
        gens = reached(GENERALISTS)
        lenses = reached(LENSES)
        fish = gens | lenses
        fish_new = reached(GENERALISTS + LENSES, skip_gap=True) - plan
        print(f"\n{label}: key {'/'.join(str(len(j['items'])) for j in runs)} items by run;"
              f" missing {'/'.join(str(len(j['missing'])) for j in runs)}, majority {len(missing)};"
              f" bad 'found' quotes {'/'.join(str(j['bad_quotes']) for j in runs)}")
        print(f"  interviewer's plan reaches {len(plan)} ({len(questions(set_file(label, 'interviewer')))} questions)")
        print(f"  one generalist {len(one)}; six generalists {len(gens)}; six lenses {len(lenses)}; all goldfish {len(fish)}")
        print(f"  goldfish reach and the plan does not: {len(fish - plan)}"
              f" (one generalist: {len(one - plan)}); of those, not via a GAP line: {len(fish_new)}")
        print(f"  plan reaches and no goldfish does: {len(plan - fish)}")
        rows.append((label, len(missing), len(plan), len(one), len(fish), len(fish - plan), len(fish_new)))
    totals = {r: {v: 0 for v in VERDICTS} for r in ("interviewer", "generalists", "lenses")}
    for label in PROFILES:
        for run in range(1, JUDGE_RUNS + 1):
            j = read_judge(label, run, "compare")
            if not j:
                continue
            for reader, counts in j["verdicts"].items():
                group = "interviewer" if reader == "interviewer" else "generalists" if reader in GENERALISTS else "lenses"
                for v in VERDICTS:
                    totals[group][v] += counts[v]
    print("\nVerdicts, all profiles, summed over judge runs:")
    print("  " + " ".join(f"{v:>12}" for v in ["set", *VERDICTS]))
    for group, counts in totals.items():
        print(f"  {group:>12} " + " ".join(f"{counts[v]:>12}" for v in VERDICTS))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--live", action="store_true", help="call codex (spends usage)")
    ap.add_argument("--report", action="store_true", help="summarise out/ only")
    ap.add_argument("--compare", action="store_true", help="the interviewer's plan against the goldfish")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    exp = "compare" if args.compare else "lenses"
    if args.report:
        return report_compare() if args.compare else report()
    readers = [(label, r) for label in PROFILES for r in READERS if not (OUT / label / f"{r}.md").exists()]
    judges = [(label, n, exp) for label in PROFILES for n in range(1, JUDGE_RUNS + 1)
              if not judge_path(label, n, exp).exists()]
    if not args.live:
        for label, (profile, key) in PROFILES.items():
            print(f"{label}: {profile.relative_to(HERE.parent)} (judge key: {key_for(label, exp).name})")
        print(f"To run: {len(readers)} reader calls and {len(judges)} judge calls on {MODEL}"
              f" (outputs already in out/ are kept). Add --live to run.")
        return
    with ThreadPoolExecutor(args.jobs) as pool:
        for line in pool.map(lambda job: run_reader(*job), readers):
            print(line, flush=True)
        for line in pool.map(lambda job: run_judge(*job), judges):
            print(line, flush=True)
    report_compare() if args.compare else report()


if __name__ == "__main__":
    sys.exit(main())
