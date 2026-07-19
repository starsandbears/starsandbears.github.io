#!/usr/bin/env python3
"""
Build ../../data/q0-money/m2-vs-net-worth.csv: the money pile (M2)
next to what families OWN (household & nonprofit net worth), annual averages,
1990-latest. Powers the "how much money is alive right now?" chart in
index.html (mount point #m2Line).

WHY BOTH SERIES ON ONE CHART. M2 counts the dollars alive right now — but a
dollar's life story ends with it erased (loan repaid / QT), having been traded
along the way into real things that KEEP value: houses, businesses, savings.
Net worth (assets minus debts) is where all those finished lifetimes of money
piled up. Showing ~$22T of money next to ~$180T of family net worth is the
point: money comes and goes; what it builds accumulates.

SERIES (both FRED, no API key needed via fredgraph.csv):
  M2SL      M2 money stock, monthly, $ billions, seasonally adjusted
            -> annual average, matching the m2Vals array already on the page
  TNWBSHNO  Households & nonprofit organizations; net worth (Fed Z.1 table
            B.101, line 39), quarterly, $ millions, not seasonally adjusted
            -> annual average of the quarters

RAW INPUT (downloaded to /tmp, not kept in the repo):
  curl -sL "https://fred.stlouisfed.org/graph/fredgraph.csv?id=M2SL" -o /tmp/M2SL.csv
  curl -sL "https://fred.stlouisfed.org/graph/fredgraph.csv?id=TNWBSHNO" -o /tmp/TNWBSHNO.csv
(this script downloads them itself if missing)

OUTPUT: ../../data/q0-money/m2-vs-net-worth.csv
        (year, m2_bn, net_worth_bn, source) — and prints the JS arrays to
        paste into sections/page-scripts.html.

Run: python3 scripts/q0-money/build_m2_vs_net_worth.py
"""
import csv
import os
import urllib.request
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, "..", "..", "data", "q0-money", "m2-vs-net-worth.csv"))
FIRST_YEAR = 1990


def fred_annual_avg(series_id, unit_divisor, obs_per_year):
    """Fetch a FRED series; return {year: annual avg, $B} for COMPLETE years
    only (obs_per_year observations), so a partial current year can't sneak
    in as a fake annual figure."""
    path = f"/tmp/{series_id}.csv"
    if not os.path.exists(path):
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        urllib.request.urlretrieve(url, path)
    by_year = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            val = row[series_id].strip()
            if not val or val == ".":
                continue
            by_year[int(row["observation_date"][:4])].append(float(val))
    return {y: sum(v) / len(v) / unit_divisor
            for y, v in by_year.items() if len(v) == obs_per_year}


def main():
    m2 = fred_annual_avg("M2SL", 1, 12)         # monthly, $B -> $B
    nw = fred_annual_avg("TNWBSHNO", 1000, 4)   # quarterly, $M -> $B
    # keep only complete-ish years present in both, from FIRST_YEAR on
    years = sorted(y for y in m2 if y in nw and y >= FIRST_YEAR)
    src = ("FRED M2SL (monthly, $B, annual avg); FRED TNWBSHNO = Fed Z.1 "
           "B.101 household & nonprofit net worth (quarterly, $M, annual avg)")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "m2_bn", "net_worth_bn", "source"])
        for y in years:
            w.writerow([y, round(m2[y]), round(nw[y]), src if y == years[0] else ""])
    print("wrote", OUT, f"({years[0]}-{years[-1]})")
    print("\nJS arrays for sections/page-scripts.html:")
    print("const m2Years=[" + ",".join(str(y) for y in years) + "];")
    print("const m2Vals=[" + ",".join(str(round(m2[y])) for y in years) + "];")
    print("const nwVals=[" + ",".join(str(round(nw[y])) for y in years) + "];")


if __name__ == "__main__":
    main()
