"""
make_assignment.py -- personal assignment sheet generator (EMQA, Energy MBA).

Student:     python make_assignment.py --id 12345678 --assignment 1
             python make_assignment.py --id 12345678 --assignment 2 --role B
Team:        python make_assignment.py --id "12345678+23456789" --assignment 1
Instructor:  python make_assignment.py --roster roster.csv --assignment 2 --out params_A2.csv
             (roster.csv: columns id[,role]; one row per student or team)

The parameters are a deterministic function of the ID (SHA-256 seed): the same ID always gives
the same sheet, and different IDs give different test windows, hours and settings.
Roles (assignment 2): B battery, H hydro, R solar, S supplier/industrial consumer.
"""
import argparse
import json
import sys

import pandas as pd

import emqa_assign as ea

LABELS = {
    "en": {
        "title": "EMQA personal assignment sheet",
        "keep": "Copy this block, unchanged, into the first cell of your notebook and into the memo appendix.",
    },
    "ro": {
        "title": "Fișa personală a temei EMQA",
        "keep": "Copiați acest bloc, nemodificat, în prima celulă a notebook-ului și în anexa memoriului.",
    },
}


def sheet(p, lang="en"):
    lines = [f"== {LABELS[lang]['title']} (A{p['assignment']}) ==", LABELS[lang]["keep"]]
    for k, v in p.items():
        lines.append(f"  {k:<24}: {v}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", help="student ID (or team: IDs joined by +)")
    ap.add_argument("--assignment", type=int, choices=[1, 2], required=True)
    ap.add_argument("--role", choices=list(ea.ROLES), help="assignment 2 role: " + "; ".join(f"{k}={v}" for k, v in ea.ROLES.items()))
    ap.add_argument("--roster", help="CSV with column id (and role for assignment 2)")
    ap.add_argument("--out", default=None, help="output CSV for --roster")
    ap.add_argument("--lang", choices=["en", "ro"], default="en")
    ap.add_argument("--json", action="store_true", help="print JSON instead of the text sheet")
    a = ap.parse_args(argv)
    if a.roster:
        r = pd.read_csv(a.roster, dtype=str)
        rows = []
        for _, x in r.iterrows():
            role = x.get("role") if a.assignment == 2 else None
            rows.append({k: (json.dumps(v) if isinstance(v, list) else v)
                         for k, v in ea.params(x["id"], a.assignment, role).items()})
        out = pd.DataFrame(rows)
        dup = out.drop(columns=["student_id"]).astype(str).duplicated(keep=False).sum()
        print(f"{len(out)} sheets; rows sharing ALL settings with another row: {dup}")
        out.to_csv(a.out or f"params_A{a.assignment}.csv", index=False)
        print("written", a.out or f"params_A{a.assignment}.csv")
        return 0
    if not a.id:
        ap.error("--id or --roster is required")
    p = ea.params(a.id, a.assignment, a.role)
    print(json.dumps(p, indent=1) if a.json else sheet(p, a.lang))
    return 0


if __name__ == "__main__":
    sys.exit(main())
