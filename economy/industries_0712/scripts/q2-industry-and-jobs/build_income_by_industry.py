#!/usr/bin/env python3
"""
Build ../../data/q2-industry-and-jobs/income_by_industry.csv from the BLS QCEW national 2025
annual-average file (area US000).

Source file (official BLS QCEW Open Data Access API):
    https://data.bls.gov/cew/data/api/2025/a/area/US000.csv

QCEW reports industry data split by ownership (Federal/State/Local/Private),
not as a single "Total Covered" row at the NAICS-sector level. The official
"average annual pay" for a sector overall is the employment-weighted aggregate
across ownerships:  sum(total_annual_wages) / sum(annual_avg_emplvl).
This is exactly how BLS derives avg_annual_pay, so the result equals the
official total-covered average annual pay for each sector.

Metric: MEAN (average) annual pay per employee, total covered ownership, 2025.
"""
import csv
import os

# raw input (large, not in repo): download first with
#   curl -s "https://data.bls.gov/cew/data/api/2025/a/area/US000.csv" -o /tmp/qcew_us000_2025_raw.csv
SRC = "/tmp/qcew_us000_2025_raw.csv"
_HERE = os.path.dirname(os.path.abspath(__file__))
# scripts/<section>/ mirrors data/<section>/ — derive the folder name
OUT = os.path.join(_HERE, "..", "..", "data", os.path.basename(_HERE),
                   "income_by_industry.csv")
YEAR = 2025
SOURCE = ("BLS QCEW 2025 annual averages, national (area US000), avg annual pay, "
          "total covered; https://data.bls.gov/cew/data/api/2025/a/area/US000.csv")

# NAICS sectors as published by QCEW (industry_code -> label)
SECTORS = [
    ("11", "Agriculture, forestry, fishing and hunting"),
    ("21", "Mining, quarrying, and oil and gas extraction"),
    ("22", "Utilities"),
    ("23", "Construction"),
    ("31-33", "Manufacturing"),
    ("42", "Wholesale trade"),
    ("44-45", "Retail trade"),
    ("48-49", "Transportation and warehousing"),
    ("51", "Information"),
    ("52", "Finance and insurance"),
    ("53", "Real estate and rental and leasing"),
    ("54", "Professional, scientific, and technical services"),
    ("55", "Management of companies and enterprises"),
    ("56", "Administrative and support and waste management services"),
    ("61", "Educational services"),
    ("62", "Health care and social assistance"),
    ("71", "Arts, entertainment, and recreation"),
    ("72", "Accommodation and food services"),
    ("81", "Other services (except public administration)"),
    ("92", "Public administration"),
]
LABELS = dict(SECTORS)

# Aggregate wages and employment across all ownership codes per sector.
agg = {code: {"wages": 0, "emp": 0} for code, _ in SECTORS}
total_check = None
with open(os.path.abspath(SRC)) as f:
    for row in csv.DictReader(f):
        ic = row["industry_code"]
        if ic in agg:
            agg[ic]["wages"] += int(row["total_annual_wages"] or 0)
            agg[ic]["emp"] += int(row["annual_avg_emplvl"] or 0)
        # National all-industries total covered (own 0, agglvl 10) for validation
        if ic == "10" and row["own_code"] == "0" and row["agglvl_code"] == "10":
            total_check = (int(row["total_annual_wages"]), int(row["annual_avg_emplvl"]),
                           int(row["avg_annual_pay"]))

rows_out = []
for code, _ in SECTORS:
    w, e = agg[code]["wages"], agg[code]["emp"]
    pay = round(w / e) if e else 0
    rows_out.append((LABELS[code], pay, code, e))

with open(os.path.abspath(OUT), "w", newline="") as f:
    wri = csv.writer(f)
    wri.writerow(["industry", "avg_annual_pay", "year", "source"])
    for label, pay, code, emp in rows_out:
        wri.writerow([label, pay, YEAR, SOURCE])

# Report
print(f"{'sector':55s} {'avg_annual_pay':>15s} {'emp(000s)':>12s}")
for label, pay, code, emp in rows_out:
    print(f"{label:55s} {pay:>15,d} {emp/1000:>12,.0f}")

if total_check:
    tw, te, tp = total_check
    derived = round(tw / te)
    print("\nVALIDATION (national, all industries, total covered):")
    print(f"  BLS published avg_annual_pay = {tp:,}")
    print(f"  derived sum(wages)/sum(emp)  = {derived:,}")
