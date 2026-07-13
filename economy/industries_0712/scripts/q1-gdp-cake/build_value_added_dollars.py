#!/usr/bin/env python3
"""
Build ../../data/q1-gdp-cake/gdp-value-added-dollars-history.csv: each big
industry's value added in DOLLARS ($ billions), every year 2005-2025. Powers
the "slices in dollars, over time" line chart next to the shares-over-time
chart in us-econ-and-money-intro.html.

WHY DOLLARS TOO. The shares-history CSV (gdp-value-added-shares-history.csv)
answers "did the slice get bigger or smaller *compared to the whole cake*?".
This file answers the kid's other natural question: "how many actual dollars
of new value did each industry make each year?" — where every line climbs,
because the whole cake grew from ~$13T (2005) to ~$30.8T (2025). Same six
industries as the shares chart so the two read side by side. These are
NOMINAL dollars (not inflation-adjusted) — part of the climb is just prices
rising; the report says so in the caption.

SOURCE. BEA GDP-by-Industry quarterly value added via FRED, one series per
industry ($ billions, seasonally adjusted annual rate), averaged over each
year's four quarters to an annual figure — the same series and method behind
the shares CSV, so the two files agree by construction:
  Manufacturing                        VAMA
  Finance & insurance                  VAFI
  Professional, scientific & technical VAPST
  Health care & social assistance      VAHCSA
  Information                          VAI
  Real estate, rental & leasing        VARL
Download (one combined CSV, no API key needed):
  https://fred.stlouisfed.org/graph/fredgraph.csv?id=VAMA,VAFI,VAPST,VAHCSA,VAI,VARL

CROSS-CHECK. The 2025 rows must match the 2025 cake numbers embedded in
sections/page-scripts.html (gdp[] / goValue[]): Manufacturing 2896.5,
Finance 2441.9, Prof/sci/tech 2494.2, Health 2371.1, Information 1695.1,
Real estate 4238.6. The script asserts this before writing.

OUTPUT: ../../data/q1-gdp-cake/gdp-value-added-dollars-history.csv
  columns: year, industry, fred_series, value_added_bn, source
Raw download lands in /tmp/fred-va-dollars.csv.

Run:  python3 build_value_added_dollars.py
"""
import csv
import os
import urllib.request
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "data", os.path.basename(HERE),
                   "gdp-value-added-dollars-history.csv")
RAW = "/tmp/fred-va-dollars.csv"

SERIES = {  # FRED id -> report industry label (matches the shares CSV)
    "VAMA": "Manufacturing",
    "VAFI": "Finance & insurance",
    "VAPST": "Professional, scientific & technical",
    "VAHCSA": "Health care & social assistance",
    "VAI": "Information",
    "VARL": "Real estate, rental & leasing",
}
URL = ("https://fred.stlouisfed.org/graph/fredgraph.csv?id="
       + ",".join(SERIES))
FIRST_YEAR, LAST_YEAR = 2005, 2025

# 2025 cake numbers from sections/page-scripts.html — must match
CHECK_2025 = {
    "Manufacturing": 2896.5, "Finance & insurance": 2441.9,
    "Professional, scientific & technical": 2494.2,
    "Health care & social assistance": 2371.1,
    "Information": 1695.1, "Real estate, rental & leasing": 4238.6,
}
SOURCE_NOTE = ("BEA GDP-by-Industry value added via FRED (quarterly $B SAAR "
               "averaged to annual); nominal dollars, not inflation-adjusted")


def main():
    urllib.request.urlretrieve(URL, RAW)
    quarters = defaultdict(lambda: defaultdict(list))  # sid -> year -> [q vals]
    with open(RAW) as f:
        for row in csv.DictReader(f):
            year = int(row["observation_date"][:4])
            for sid in SERIES:
                if row.get(sid) not in (None, "", "."):
                    quarters[sid][year].append(float(row[sid]))

    rows = []
    for sid, label in SERIES.items():
        for year in range(FIRST_YEAR, LAST_YEAR + 1):
            vals = quarters[sid][year]
            assert len(vals) == 4, f"{sid} {year}: {len(vals)} quarters"
            annual = round(sum(vals) / 4, 1)
            if year == LAST_YEAR:
                want = CHECK_2025[label]
                assert abs(annual - want) < 0.5, \
                    f"{label} 2025: got {annual}, report says {want}"
            rows.append({"year": year, "industry": label, "fred_series": sid,
                         "value_added_bn": annual, "source": SOURCE_NOTE})

    rows.sort(key=lambda r: (r["year"], -r["value_added_bn"]))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year", "industry", "fred_series",
                                          "value_added_bn", "source"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
