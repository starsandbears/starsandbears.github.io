#!/usr/bin/env python3
"""
Build the state x industry GDP HISTORY (2005-2025) that powers the "how did
your state's layers grow?" chart in the state explorer
-> ../../data/state-explorer/state-gdp-history.csv (long form, provenance)
-> /tmp/state_hist_block.js   (compact JS block embedded in
                               sections/page-scripts.html)

WHAT IT PRODUCES. For each of the 50 states + DC + the United States row, each
of the same 20 NAICS-style industries as state-by-industry-<YEAR>.csv, a value
added figure ($ billions, NOMINAL — not inflation-adjusted; the chart caption
says so) for every year 2005-2025. The report draws one line per industry
(thick layers visible, the rest click-to-show in the legend) plus a computed
"whole cake" total.

SOURCE. BEA SAGDP2 (GDP by state, value added by industry, nominal), the SAME
file and table the single-year builder uses — so the last year here equals the
state explorer's bar charts by construction (asserted below).
  https://apps.bea.gov/regional/zip/SAGDP.zip -> /tmp/sagdp/SAGDP2__ALL_AREAS_1997_2025.csv
The "United States" row is BEA's own US line in the file (the sum of states;
~0.7% below headline national GDP because state accounts exclude some
federal/overseas activity — same ruler as the rest of the state explorer).

OUTPUT UNITS: $ billions, 1 decimal (raw file is $ millions).

Run (after downloading/unzipping SAGDP.zip as above):
  python3 scripts/state-explorer/build_state_gdp_history.py
"""
import csv, json, os

BEA = "/tmp/sagdp/SAGDP2__ALL_AREAS_1997_2025.csv"
FIRST, LAST = 2005, 2025
OUT_JS = "/tmp/state_hist_block.js"
_HERE = os.path.dirname(os.path.abspath(__file__))
OUT_CSV = os.path.join(_HERE, "..", "..", "data", os.path.basename(_HERE),
                       "state-gdp-history.csv")
CUR_CSV = os.path.join(_HERE, "..", "..", "data", os.path.basename(_HERE),
                       "state-by-industry-2025.csv")

NAME2ABBR = {"Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA",
"Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Florida":"FL",
"Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS",
"Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI",
"Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV",
"New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC",
"North Dakota":"ND","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI",
"South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT",
"Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY",
"United States":"US"}

SECTORS = {"11":"Agriculture, forestry, fishing","21":"Mining","22":"Utilities","23":"Construction",
"31-33":"Manufacturing","42":"Wholesale trade","44-45":"Retail trade","48-49":"Transportation & warehousing",
"51":"Information","52":"Finance & insurance","53":"Real estate, rental & leasing",
"54":"Professional, sci & technical","55":"Management of companies","56":"Administrative & waste svcs",
"61":"Educational services","62":"Health care & social assist.","71":"Arts, entertainment & rec.",
"72":"Accommodation & food svcs","81":"Other services"}
GOV = "Government"
IND = list(SECTORS.values()) + [GOV]  # 20 labels, same order as the explorer

YEARS = list(range(FIRST, LAST + 1))

def main():
    with open(BEA, encoding="latin-1") as f:
        rows = list(csv.reader(f))
    hdr = rows[0]
    yix = {y: hdr.index(str(y)) for y in YEARS}

    # hist[abbr][label] = [values $M per year]
    hist = {ab: {l: [0.0]*len(YEARS) for l in IND} for ab in NAME2ABBR.values()}
    for r in rows[1:]:
        if len(r) <= yix[LAST]: continue
        # GeoName appears as e.g. ' "United States *"' — strip spaces, quotes
        # and BEA's footnote asterisk before matching
        name = r[1].strip().strip('"').removesuffix("*").strip()
        ab = NAME2ABBR.get(name)
        if not ab: continue
        naics, desc = r[5].strip(), r[6].strip()
        if naics in SECTORS: lbl = SECTORS[naics]
        elif desc == "Government and government enterprises": lbl = GOV
        else: continue
        for k, y in enumerate(YEARS):
            try: hist[ab][lbl][k] = float(r[yix[y]])
            except ValueError: pass  # (D)/(NA) suppressions stay 0

    # US = sum of the 50 states + DC (the explorer's ruler), NOT BEA's
    # "United States *" line, which runs ~1% higher on some industries
    for l in IND:
        for k in range(len(YEARS)):
            hist["US"][l][k] = sum(hist[ab][l][k] for ab in hist if ab != "US")

    # cross-check: last year must equal the single-year explorer CSV ($M)
    cur = {}
    with open(CUR_CSV) as f:
        for r in csv.DictReader(f):
            cur.setdefault(r["state"], {})[r["industry"]] = float(r["gdp_millions_2025"])
    ab2name = {v: k for k, v in NAME2ABBR.items()}
    for ab in hist:
        for l in IND:
            want = cur[ab2name[ab]][l]
            got = hist[ab][l][-1]
            assert abs(got - want) < 0.6, f"{ab}/{l}: history {got} != explorer {want}"

    # long-form CSV ($B) for provenance
    src = ("BEA SAGDP2 value added by state x industry, nominal $ (annual, "
           "2005-2025); same table as state-by-industry-2025.csv")
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["state", "industry", "year", "value_added_bn", "source"])
        for ab in ["US"] + sorted(k for k in hist if k != "US"):
            for l in IND:
                for k, y in enumerate(YEARS):
                    w.writerow([ab2name[ab], l, y, round(hist[ab][l][k]/1000, 1), src])

    # compact JS block: arrays follow IND order; $B, 1 decimal
    js = {ab: [[round(v/1000, 1) for v in hist[ab][l]] for l in IND] for ab in hist}
    with open(OUT_JS, "w") as f:
        f.write("const HYRS=" + json.dumps(YEARS, separators=(",", ":")) + ";\n")
        f.write("const STHIST=" + json.dumps(js, separators=(",", ":")) + ";\n")

    print("years:", YEARS[0], "-", YEARS[-1], "| states:", len(hist), "| industries:", len(IND))
    tx = hist["TX"]["Mining"]; print("TX Mining $B 2005/2020/2025:", round(tx[0]/1000,1), round(tx[15]/1000,1), round(tx[-1]/1000,1))
    print("US total 2025 ($B):", round(sum(hist['US'][l][-1] for l in IND)/1000, 1))
    print("wrote", os.path.normpath(OUT_CSV), "and", OUT_JS,
          "(", round(os.path.getsize(OUT_JS)/1024, 1), "KB )")

if __name__ == "__main__":
    main()
