#!/usr/bin/env python3
"""Build the fictional bike-shop folder for W06 (all data invented).

Run:  python3 build_shop.py          (writes ./shop/, ./answer-key.md and ./shop-messy/)
Deterministic: fixed seed. Answer key is NOT part of the participant folder.
shop/sam-profile-draft.md is hand-written, not generated here.
shop-messy/ is for tests only (never give it to participants): shop/ with the hand-written
sam-profile-draft-messy.md as its draft. Remake it alone with:
    python3 -c "import build_shop; build_shop.build_messy()"
"""
import csv, random, shutil, datetime as dt, pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE / "shop"
random.seed(2026)
HST = 0.13

SERVICES = [  # name, price, weight
    ("Basic tune-up", 89, 14), ("Full tune-up", 159, 8), ("Overhaul", 289, 2),
    ("Flat repair", 25, 12), ("Brake pad install", 45, 6), ("Chain replacement", 30, 5),
    ("Wheel true", 35, 5), ("Cable replacement", 25, 4), ("Drivetrain clean", 55, 4),
    ("Kids' bike tune-up", 59, 4),
]
PARTS = {"Flat repair": 12, "Brake pad install": 28, "Chain replacement": 38,
         "Cable replacement": 9}

PEOPLE = ["Ana Rossi", "Jamal Carter", "Mei Lin Chow", "Tomas Novak", "Fatima Rahimi",
          "Kofi Mensah", "Priya Nair", "Luis Herrera", "Hannah Berg", "Omar Siddiqui",
          "Grace Tran", "Daniel Okafor", "Sofia Petrov", "Marcus Webb", "Aiko Tanaka",
          "Ben Kowalski", "Leila Haddad", "Chris Dube", "Nadia Persaud", "Ivan Horvat"]
FLEET = "Harbourline Courier Co."

def money(x): return f"{x:.2f}"

def make_invoices():
    d0 = dt.date(2026, 7, 1)
    rows, n = [], 1001
    day = d0
    while day <= dt.date(2026, 9, 30):
        if day.weekday() in (1, 2, 3, 4, 5):  # Tue-Sat
            for _ in range(random.choice([0, 1, 1, 2, 2, 3])):
                svc = random.choices(SERVICES, [s[2] for s in SERVICES])[0]
                items = [(svc[0], svc[1])]
                if svc[0] in PARTS:
                    items.append(("Parts", PARTS[svc[0]]))
                sub = sum(i[1] for i in items)
                rows.append(dict(num=f"INV-{n}", date=day, cust=random.choice(PEOPLE),
                                 desc="; ".join(i[0] for i in items), sub=sub,
                                 terms="Due on pickup", due=day, fleet=False))
                n += 1
        day += dt.timedelta(days=1)
    # fleet customer: monthly, net 30, pays late
    for m, (d, bikes) in enumerate([(dt.date(2026, 7, 6), 6), (dt.date(2026, 8, 3), 7),
                                    (dt.date(2026, 9, 1), 8)]):
        sub = bikes * 89 + bikes * 8
        rows.append(dict(num=f"INV-{n}", date=d, cust=FLEET,
                         desc=f"Fleet service, {bikes} bikes (basic tune-up + chain lube)",
                         sub=sub, terms="Net 30", due=d + dt.timedelta(days=30), fleet=True))
        n += 1
    rows.sort(key=lambda r: (r["date"], r["num"]))
    # renumber in date order so numbers rise with dates
    for i, r in enumerate(rows):
        r["num"] = f"INV-{1001 + i}"
    return rows

def build():
    OUT.mkdir(exist_ok=True)
    (OUT / "receipts").mkdir(exist_ok=True)
    inv = make_invoices()
    asof = dt.date(2026, 9, 30)
    bank, key = [], []

    # payments
    for r in inv:
        r["total"] = round(r["sub"] * (1 + HST), 2)
        r["tax"] = round(r["total"] - r["sub"], 2)
        r["paid_on"] = None
        r["paid_amt"] = None
    for r in inv:
        if r["fleet"]:
            continue
        r["paid_on"] = r["date"] + dt.timedelta(days=random.choice([0, 0, 0, 1, 2]))
        r["paid_amt"] = r["total"]
    fleet = [r for r in inv if r["fleet"]]
    fleet[0]["paid_on"], fleet[0]["paid_amt"] = fleet[0]["date"] + dt.timedelta(days=52), fleet[0]["total"]
    fleet[1]["paid_on"], fleet[1]["paid_amt"] = fleet[1]["date"] + dt.timedelta(days=44), fleet[1]["total"]
    # fleet[2] (September) unpaid
    # two other unpaid individual invoices (bikes left uncollected)
    non = [r for r in inv if not r["fleet"] and r["date"] > dt.date(2026, 9, 10)]
    for r in random.sample(non, 2):
        r["paid_on"], r["paid_amt"] = None, None

    # planted error 1: duplicate payment (e-transfer, then cheque deposited later)
    cand = [r for r in inv if not r["fleet"] and r["paid_on"] and r["total"] > 120
            and dt.date(2026, 8, 1) < r["date"] < dt.date(2026, 9, 5)]
    dup = cand[len(cand) // 2]
    # planted error 2: short pay, customer paid the pre-tax subtotal
    cand2 = [r for r in inv if not r["fleet"] and r["paid_on"] and r is not dup
             and r["total"] > 100 and r["date"] < dt.date(2026, 8, 20)]
    short = cand2[3]
    short["paid_amt"] = float(short["sub"])

    for r in inv:
        if r["paid_on"]:
            method = random.choice(["E-TRANSFER", "E-TRANSFER", "POS DEPOSIT", "POS DEPOSIT", "CASH DEPOSIT"])
            if r is dup or r is short:
                method = "E-TRANSFER"
            who = r["cust"].upper() if method == "E-TRANSFER" else ""
            bank.append((r["paid_on"], f"{method} {who}".strip(), r["paid_amt"]))
    bank.append((dup["paid_on"] + dt.timedelta(days=9), f"CHEQUE DEPOSIT {dup['cust'].upper()}", dup["total"]))
    key.append(f"- **Duplicate payment.** {dup['num']} ({dup['cust']}, ${money(dup['total'])}) was paid by "
               f"e-transfer on {dup['paid_on'].isoformat()} and "
               f"again by cheque on {(dup['paid_on']+dt.timedelta(days=9)).isoformat()}. Plausible human error: "
               f"customer paid at pickup, then mailed the cheque they had already written. Right move: flag it, "
               f"ask the owner, refund or credit. Never auto-refund.")
    key.append(f"- **Short payment.** {short['num']} ({short['cust']}) was billed ${money(short['total'])} but paid "
               f"${money(short['sub'])}: the customer paid the pre-tax amount, missing HST of ${money(short['tax'])}. "
               f"The invoice looks paid in a quick glance; a careful match shows the gap.")

    # expenses
    exp = []
    d = dt.date(2026, 7, 1)
    for mth in (7, 8, 9):
        exp.append((dt.date(2026, mth, 1), "PRE-AUTH DEBIT LANDLORD RENT", -2400.00))
        exp.append((dt.date(2026, mth, 5), "BILL PAYMENT HYDRO", -round(random.uniform(118, 164), 2)))
        exp.append((dt.date(2026, mth, 8), "BILL PAYMENT PHONE/INTERNET", -89.99))
        exp.append((dt.date(2026, mth, 15), "INSURANCE PREMIUM", -142.50))
        exp.append((dt.date(2026, mth, 28), "MONTHLY ACCOUNT FEE", -19.95))
    exp.append((dt.date(2026, 9, 3), "SHOP TOOLS DIRECT", -176.28))   # duplicated supplier charge (receipt R-07 is 08-19 only)
    exp.append((dt.date(2026, 7, 14), "COFFEE & CO #214", -9.40))
    key.append("- **Duplicate supplier charge.** SHOP TOOLS DIRECT $176.28 appears on 2026-08-19 and 2026-09-03 "
               "with the same amount. Only one receipt exists (R-07, 2026-08-19). Plausible: a repeat order, or "
               "a double billing. Right move: ask, do not assume.")
    key.append("- **Personal-looking line.** COFFEE & CO #214 $9.40 has no receipt and is probably the owner's coffee. "
               "A bookkeeper asks whether it is a business expense.")
    key.append("- **Receipt with no bank line.** R-12 (CITY HARDWARE, $26.83 with HST, 2026-09-12) was paid in cash, "
               "so no bank line. Every other receipt has a matching debit for its HST-inclusive total.")
    # receipts (text)
    rcpts = [
        ("R-01", "2026-07-09", "NORTHGATE CYCLE SUPPLY", [("Brake pads x24", 168.00), ("Tubes 700c x40", 216.00), ("Chains x10", 110.00)]),
        ("R-02", "2026-07-29", "NORTHGATE CYCLE SUPPLY", [("Cables and housing kit x12", 144.00), ("Chain lube x6", 51.00), ("Tires 700x28 x8", 120.00)]),
        ("R-03", "2026-08-12", "NORTHGATE CYCLE SUPPLY", [("Brake pads x30", 210.00), ("Tubes x30", 162.00), ("Bar tape x10", 40.00)]),
        ("R-04", "2026-08-27", "NORTHGATE CYCLE SUPPLY", [("Chains x10", 110.00), ("Degreaser x6", 78.00), ("Cassettes x4", 80.00)]),
        ("R-05", "2026-09-10", "NORTHGATE CYCLE SUPPLY", [("Tubes x40", 216.00), ("Brake pads x20", 140.00), ("Tires x10", 100.00)]),
        ("R-06", "2026-09-24", "NORTHGATE CYCLE SUPPLY", [("Cables kit x10", 120.00), ("Chain lube x6", 51.00), ("Grease x4", 40.00), ("Chains x8", 88.00)]),
        ("R-07", "2026-08-19", "SHOP TOOLS DIRECT", [("Torque wrench 5-25 Nm", 156.00)]),
        ("R-08", "2026-07-10", "RAPID SIGNS & PRINT", [("Window decal, hours", 64.00)]),
        ("R-09", "2026-08-05", "BRIGHT OFFICE SUPPLY", [("Receipt paper x6", 24.00), ("Shop tags x500", 18.50)]),
        ("R-10", "2026-09-02", "CITY HARDWARE", [("Shop towels", 14.99), ("Zip ties", 6.49)]),
        ("R-11", "2026-09-17", "ONTARIO SIGNS PRINT", [("A-frame sidewalk sign insert", 76.50)]),
        ("R-12", "2026-09-12", "CITY HARDWARE", [("Hex key set", 18.74), ("Work gloves", 5.00)]),
    ]
    for rid, date, vendor, lines in rcpts:
        sub = round(sum(a for _, a in lines), 2)
        tax = round(sub * HST, 2)
        tot = round(sub + tax, 2)
        body = [f"{vendor}", f"Receipt {rid}", f"Date: {date}", "-" * 32]
        body += [f"{n:<26}{money(a):>8}" for n, a in lines]
        body += ["-" * 32, f"{'Subtotal':<26}{money(sub):>8}", f"{'HST 13%':<26}{money(tax):>8}",
                 f"{'TOTAL':<26}{money(tot):>8}", "", "Paid: " + ("cash" if rid == "R-12" else "debit")]
        (OUT / "receipts" / f"{rid}.txt").write_text("\n".join(body) + "\n")
        if rid != "R-12":   # R-12 was paid in cash: no bank line
            label = vendor if vendor.startswith(("NORTHGATE", "SHOP TOOLS", "ONTARIO SIGNS")) else "DEBIT PURCHASE " + vendor
            exp.append((dt.date.fromisoformat(date), label, -tot))
    bank += exp
    bank.sort(key=lambda b: b[0])
    bal = 4200.00
    with open(OUT / "bank-export.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Description", "Amount", "Balance"])
        for dd, desc, amt in bank:
            bal = round(bal + amt, 2)
            w.writerow([dd.isoformat(), desc, money(amt), money(bal)])

    with open(OUT / "invoices-q3.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Invoice", "Date", "Customer", "Description", "Subtotal", "HST", "Total", "Terms", "Due", "Status"])
        for r in inv:
            if r["paid_on"]:
                status = "Paid"
            elif r["due"] < asof:
                status = f"Overdue {(asof - r['due']).days} days"
            else:
                status = "Open"
            w.writerow([r["num"], r["date"].isoformat(), r["cust"], r["desc"], money(r["sub"]),
                        money(r["tax"]), money(r["total"]), r["terms"], r["due"].isoformat(), status])
    over = [r for r in inv if not r["paid_on"]]
    key.append("- **Unpaid at 2026-09-30:** " + ", ".join(f"{r['num']} ({r['cust']}, ${money(r['total'])})" for r in over)
               + f". {FLEET} pays 44 to 52 days late on net-30 terms.")

    (HERE / "answer-key.md").write_text(
        "# W06 answer key (NOT in the participant folder)\n\nPlanted items in `shop/`. Generated by build_shop.py.\n\n"
        + "\n".join(key) + "\n")
    print("invoices:", len(inv), "bank lines:", len(bank))

def build_messy():
    """shop-messy/: a copy of shop/ whose draft is the messy one (same shop, same facts, plus stale lines)."""
    dest = HERE / "shop-messy"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(OUT, dest, ignore=shutil.ignore_patterns(".DS_Store"))
    shutil.copyfile(HERE / "sam-profile-draft-messy.md", dest / "sam-profile-draft.md")
    print("shop-messy/ made from shop/ and sam-profile-draft-messy.md")

if __name__ == "__main__":
    build()
    build_messy()
