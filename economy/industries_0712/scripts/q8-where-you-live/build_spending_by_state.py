#!/usr/bin/env python3
"""
Build ../../data/q8-where-you-live/spending-by-state-2024.csv: per-capita
consumer spending by 11 kid-friendly categories, for every state (50 + DC + a
"United States" row), from BEA SAPCE tables, 2024. Powers the per-state
spending chart in the reports.

IMPORTANT — different measure. This is **BEA PCE per person**, NOT the BLS CES
household budget used in the rest of the spending story. PCE counts spending on
behalf of consumers (e.g. employer/government-paid health care), is per-person
not per-household, and uses BEA's category definitions. So the totals and mix
differ from the CES donut. It is, however, the only spending-by-category data
that exists for all 50 states, and it's good for comparing states.

METHOD. Categories are built from the DETAILED table SAPCE3 (PCE by type of
product, $ millions, 113 lines), then converted to per-person dollars with each
state's own ratio of SAPCE2 line 1 (per-capita total, $) to SAPCE3 line 1
(total, $M) — so the numbers stay exactly on the SAPCE2 per-capita ruler.
"Everything else" is the residual (total minus the named buckets): mostly
personal care, tobacco, magazines, jewelry, social & religious organizations,
net foreign travel, and nonprofits serving households. Suppressed (D) detail
lines in small states count as 0 in their bucket, so their dollars land in
"Everything else" instead of vanishing.

RAW INPUT (download first; large, not kept in the repo):
  curl -sL "https://apps.bea.gov/regional/zip/SAPCE.zip" -o /tmp/sapce.zip
  unzip /tmp/sapce.zip -d /tmp/sapce
  -> uses SAPCE3__ALL_AREAS_1997_2024.csv and SAPCE2__ALL_AREAS_1997_2024.csv

OUTPUT: ../../data/q8-where-you-live/spending-by-state-2024.csv
  columns: state, category, per_capita_2024_usd, source
Also emits /tmp/spend_state_block.js (const SPCATS / SPEND) for embedding in
sections/page-scripts.html (the Plotly pick-a-state spending chart).
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC3 = "/tmp/sapce/SAPCE3__ALL_AREAS_1997_2024.csv"
SRC2 = "/tmp/sapce/SAPCE2__ALL_AREAS_1997_2024.csv"
OUT = os.path.join(HERE, "..", "..", "data", os.path.basename(HERE),
                   "spending-by-state-2024.csv")
OUT_JS = "/tmp/spend_state_block.js"
YEAR = "2024"

NAME2ABBR = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
"California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
"District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
"Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
"Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
"Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
"Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
"New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
"North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
"Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
"South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
"Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
"West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}

# category -> SAPCE3 line codes to sum (non-overlapping levels of the hierarchy)
BUCKETS = [
    ("Housing & utilities", ["49"]),
    ("Getting around", ["4", "36", "68"]),        # vehicles + gasoline + transport svcs
    ("Food (in & out)", ["26", "81"]),            # groceries + restaurants & hotels
    ("Health care & medicine", ["60", "40", "21"]),  # health svcs + drugs + therapeutic equip
    ("Fun & recreation", ["13", "76", "41"]),     # rec goods & vehicles + rec svcs + rec items
    ("Money services & insurance", ["86"]),       # financial services and insurance
    ("Home stuff & furniture", ["8", "42", "107"]),  # furnishings + supplies + maintenance
    ("Phones & internet", ["96", "24"]),          # communication svcs + phone equipment
    ("School & learning", ["100", "22"]),         # education services + educational books
    ("Clothes", ["30"]),
]
TOTAL_LINE = "1"


def load(path):
    """-> {state_name: {line_code: value}} for the YEAR column."""
    rows = csv.reader(open(path, encoding="latin-1"))
    hdr = next(rows)
    yi = hdr.index(YEAR)
    out = {}
    for r in rows:
        if len(r) <= yi:
            continue
        name = r[1].strip().strip('"').removesuffix("*").strip()
        if name not in NAME2ABBR and name != "United States":
            continue
        try:
            v = float(r[yi])
        except ValueError:
            continue  # (D)/(NA) suppressions -> bucket treats as 0
        out.setdefault(name, {})[r[4].strip()] = v
    return out


def main():
    d3, d2 = load(SRC3), load(SRC2)
    src = ("BEA SAPCE3 detail x SAPCE2 per-capita ruler, Personal Consumption "
           "Expenditures by state, 2024 (per person; different measure than BLS CES)")

    cats = [c for c, _ in BUCKETS] + ["Everything else"]
    spend, out_rows = {}, []
    order = ["United States"] + list(NAME2ABBR)
    for name in order:
        t3, t2 = d3.get(name), d2.get(name)
        if not t3 or not t2:
            continue
        factor = t2[TOTAL_LINE] / t3[TOTAL_LINE]  # $M -> per-capita $
        vals = [round(sum(t3.get(ln, 0.0) for ln in lines) * factor)
                for _, lines in BUCKETS]
        vals.append(round(t2[TOTAL_LINE] - sum(vals)))
        spend[name] = vals
        out_rows += [[name, c, v] for c, v in zip(cats, vals)]

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["state", "category", "per_capita_2024_usd", "source"])
        for a, b, c in out_rows:
            w.writerow([a, b, c, src])

    with open(OUT_JS, "w") as f:
        f.write("const SPCATS=" + json.dumps(cats) + ";\n")
        f.write("const SPEND=" + json.dumps(spend, separators=(",", ":")) + ";\n")

    us = spend["United States"]
    print("wrote", os.path.normpath(OUT), "+", OUT_JS, "| states:", len(spend))
    print("US per-capita total 2024: $%d (SAPCE2 line 1: $%d)"
          % (sum(us), round(d2["United States"][TOTAL_LINE])))
    for c, v in zip(cats, us):
        print("  %-28s $%-7d %4.1f%%" % (c, v, 100 * v / sum(us)))


if __name__ == "__main__":
    main()
