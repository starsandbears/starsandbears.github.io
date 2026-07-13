#!/usr/bin/env python3
"""
Build ../../data/q9-supply-demand/supply-vs-need.csv: a small, honest "supply vs demand" table
for the three big consumer categories the kid asked about — housing,
transportation and medical services — next to population (a stand-in for how
many people "need" the thing).

WHY THIS SHAPE. True supply/demand *curves* (how much would be made or wanted at
each price) are theoretical and nobody publishes them. What we CAN count are the
physical quantities that stand in for supply, and population that stands in for
demand pressure:
  * Housing   -> total housing units (the homes that exist)
  * Transport -> registered motor vehicles (cars & trucks on the road)
  * Medical   -> staffed hospital beds (derived from beds-per-1,000 x population)
  * "Need"    -> resident population
Indexed against population, a supply line that falls *behind* population means
the thing got scarcer per person (upward price pressure); a line that pulls
*ahead* means it got roomier per person (downward pressure). This matches the
report's price/CPI story (cars ~ kept up -> tame; beds shrank -> medical soared).

WINDOW: 2010 to each series' latest available year — the lines deliberately
end at different times (updated 2026-07-12): people & homes run to 2026 (FRED
publishes them near-real-time), cars to 2023, hospital beds to 2022 (the World
Bank/OECD series ends there). The FHWA vehicle classification changed in 2007,
so we stay after it. FHWA's 2024 MV-1 IS published but is EXCLUDED on purpose:
New York's registered-vehicle count jumps +124% in it (9.4M -> 21.0M, footnote
(3) — a state reporting change), inflating the national total +4.5% in one
year. Include 2024 only if you adjust or footnote the NY series break.

SOURCES (each value below was read from the primary source, not estimated):
  * population_thousands — FRED POPTHM (Population, resident, thousands),
    January value each year.
    https://fred.stlouisfed.org/graph/fredgraph.csv?id=POPTHM
  * housing_units_thousands — FRED ETOTALUSQ176N (Total Housing Units for the
    US, Census HVS, thousands), Q1 (Jan 1) value each year.
    https://fred.stlouisfed.org/graph/fredgraph.csv?id=ETOTALUSQ176N
  * registered_vehicles — FHWA Highway Statistics, Table MV-1, grand total of
    all registered motor vehicles (all states + DC).
    https://www.fhwa.dot.gov/policyinformation/statistics/<YEAR>/mv1.cfm
  * hospital_beds_per_1000 — World Bank SH.MED.BEDS.ZS (Hospital beds per 1,000
    people, US), which follows OECD Health Statistics.
    https://api.worldbank.org/v2/country/USA/indicator/SH.MED.BEDS.ZS

CAVEATS (also disclosed in the report): population is only a rough stand-in for
demand (income, borrowing costs, age, and *where* people want to live matter
too); national housing/vehicle counts hide local shortages; hospital beds are
one of several medical-capacity measures. Absolute beds are derived as
beds_per_1000 * population, so they inherit both series' definitions.

OUTPUT: ../../data/q9-supply-demand/supply-vs-need.csv
  columns: year, population_thousands, housing_units_thousands,
           registered_vehicles, hospital_beds_per_1000
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# scripts/<section>/ mirrors data/<section>/ — derive the folder name
OUT = os.path.join(HERE, "..", "..", "data", os.path.basename(HERE),
                   "supply-vs-need.csv")

# year: (population_thousands FRED POPTHM Jan,
#        housing_units_thousands FRED ETOTALUSQ176N Q1,
#        registered_vehicles FHWA MV-1 grand total,
#        hospital_beds_per_1000 World Bank SH.MED.BEDS.ZS)
ROWS = [
    (2010, 308706, 131626, 242060545, 3.03),
    (2012, 313636, 132619, 253639386, 2.90),
    (2015, 320997, 134862, 263610219, 2.75),
    (2017, 325901, 136818, 272429803, 2.80),
    (2019, 329766, 139069, 276491174, 2.72),
    (2020, 331443, 140266, 275936367, 2.71),
    (2022, 333349, 143121, 282174766, 2.68),
    # later years: None where the source hasn't published yet (see WINDOW note)
    (2023, 335770, 144709, 284614269, None),
    (2024, 338787, 146183, None, None),
    (2025, 341268, 147594, None, None),
    (2026, 342540, 149006, None, None),
]


def main():
    with open(os.path.abspath(OUT), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "population_thousands", "housing_units_thousands",
                    "registered_vehicles", "hospital_beds_per_1000"])
        for r in ROWS:
            w.writerow(["" if v is None else v for v in r])

    print("wrote", os.path.abspath(OUT), "|", len(ROWS), "years")
    print("indexed to 2010=100 (per person = count / population):")
    base = ROWS[0]
    fmt = lambda v, b: ("%5.1f" % (100 * v / b)) if v is not None else "    —"
    for y, pop, hou, veh, bpk in ROWS:
        beds = bpk * pop if bpk is not None else None  # per-1,000 x pop(thousands)
        print("  %d  people %s  homes %s  cars %s  beds %s"
              % (y, fmt(pop, base[1]), fmt(hou, base[2]),
                 fmt(veh, base[3]), fmt(beds, base[4] * base[1])))


if __name__ == "__main__":
    main()
