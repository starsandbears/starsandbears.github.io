#!/usr/bin/env python3
"""
Build ../../data/q0-money/money-holders.csv: who HOLDS America's ready money (checkable
deposits & currency, time & savings deposits, money-market fund shares), by
sector — households, nonfinancial businesses big & small, state & local
governments, the federal government, and the rest of the world. Powers the
"who holds the money?" question in us-econ-and-money-intro.html.

WHY THESE CATEGORIES. M2 (the headline "money supply", ~$23.1T, FRED M2SL) is
defined from the LIABILITY side: currency + checkable deposits + savings/small
time deposits + retail money-market funds. The Fed's Z.1 Financial Accounts
report the same money-like instruments from the HOLDER side, sector by sector.
The two rulers don't line up perfectly — Z.1 sector holdings include some
items M2 excludes (large time deposits, institutional MMF shares held by
companies), so the holder-side total runs somewhat larger than M2. We present
holder SHARES of the holder-side total and say so.

TWO THINGS THIS TABLE DELIBERATELY SHOWS ARE *NOT* IN M2:
  * Banks: M2 is what banks OWE the public — a deposit is the holder's asset
    and the bank's IOU. Banks' own spending money is their reserve balances at
    the Fed (FRED WRESBAL, ~$3.1T), a different kind of money outside M2.
  * The federal government's main checking account (the Treasury General
    Account) lives at the Fed, outside M2 (FRED WTREGEN, ~$0.8T). The small
    federal row below is Treasury cash held at commercial banks etc.

RAW INPUT (download first; ~35 MB zip -> ~590 MB XML, not kept in the repo):
  curl -sL "https://www.federalreserve.gov/datadownload/Output.aspx?rel=Z1&filetype=zip" -o /tmp/z1.zip
  unzip -o /tmp/z1.zip -d /tmp/z1     -> uses /tmp/z1/Z1_data.xml (SDMX)

SERIES (Z.1 quarterly levels, $ millions; mnemonic = FL + sector + instrument):
  sectors: 15 households & nonprofits | 16 nonprofits | 10 nonfinancial
           corporate | 11 nonfinancial noncorporate (small business) |
           21 state & local govts | 31 federal govt | 26 rest of the world
  Households are shown ALONE: Z.1 sector 15 bundles nonprofits in with
  households, so we subtract the separate nonprofit sector (16) per
  instrument and emit "Households" (derived) + "Nonprofits" rows.
  instruments: 3020x checkable deposits & currency | 3030x time & savings
               deposits | 3034x money-market fund shares

OUTPUT: ../../data/q0-money/money-holders.csv
  columns: holder, instrument, fl_series, as_of, value_musd, source
Run:  python3 scripts/q0-money/build_money_holders.py   (after the download above)
"""
import csv
import os
import re

SRC = "/tmp/z1/Z1_data.xml"
HERE = os.path.dirname(os.path.abspath(__file__))
# scripts/<section>/ mirrors data/<section>/ — derive the folder name
OUT = os.path.join(HERE, "..", "..", "data", os.path.basename(HERE),
                   "money-holders.csv")

# holder label -> {instrument label -> Z.1 FL mnemonic}
# "Households & nonprofits" is fetched but not emitted directly: the CSV gets
# "Households" = sector 15 minus the "Nonprofits" (sector 16) series below.
COMBINED = "Households & nonprofits"
WANT = {
    COMBINED: {
        "checkable deposits & currency": "FL153020005",
        "time & savings deposits":       "FL153030005",
        "money-market fund shares":      "FL153034005"},
    "Nonprofits": {
        # FL163030205 is really "other deposits & short-term investments";
        # the Fed's own households-only series nets it against the BROADER
        # FL153030205 (= FL153030005 + ~$72B FL153030505). We keep subtracting
        # from FL153030005 so every sector uses the same time-&-savings ruler —
        # a deliberate ≤0.4% divergence from the official FL193030205.
        "checkable deposits & currency": "FL163020005",
        "time & savings deposits":       "FL163030205",
        "money-market fund shares":      "FL163034003"},
    "Big companies (nonfin. corporate)": {
        "checkable deposits & currency": "FL103020005",
        "time & savings deposits":       "FL103030003",
        "money-market fund shares":      "FL103034000"},
    "Small businesses (noncorporate)": {
        "checkable deposits & currency": "FL113020005",
        "time & savings deposits":       "FL113030003",
        "money-market fund shares":      "FL113034003"},
    "State & local governments": {
        "checkable deposits & currency": "FL213020005",
        "time & savings deposits":       "FL213030000",
        "money-market fund shares":      "FL213034003"},
    "Federal government": {
        "checkable deposits & currency": "FL313020005",
        "time & savings deposits":       "FL313030003"},
    "Rest of the world": {
        "checkable deposits & currency": "FL263020005",
        "time & savings deposits":       "FL263030005",
        "money-market fund shares":      "FL263034003"},
}


def main():
    mnems = {m for d in WANT.values() for m in d.values()}
    # match EVERY series header (any prefix FL/FU/FR/FA..., any frequency) so
    # `cur` always resets — otherwise a wanted FL series would absorb the
    # observations of the FU/FR flow series (or the annual .A variant) that
    # follow it in the file. Only the quarterly (.Q) level series is kept.
    series_re = re.compile(r'SERIES_NAME="([A-Z]{2}\d{9})\.([QA])"')
    # NOTE: assumes the release's fixed attribute order (OBS_VALUE before
    # TIME_PERIOD, single space) — e.g. <frb:Obs OBS_STATUS="A"
    # OBS_VALUE="55865" TIME_PERIOD="1946-12-31" />
    obs_re = re.compile(r'OBS_VALUE="(-?[\d.]+)" TIME_PERIOD="(\d{4}-\d{2}-\d{2})"')
    last = {}          # mnemonic -> (date, value)
    cur = None
    with open(SRC, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = series_re.search(line)
            if m:
                cur = m.group(1) if (m.group(1) in mnems
                                     and m.group(2) == "Q") else None
                continue
            if cur:
                o = obs_re.search(line)
                if o:
                    last[cur] = (o.group(2), float(o.group(1)))

    missing = mnems - set(last)
    assert not missing, f"series not found in Z1_data.xml: {missing}"

    src = ("Federal Reserve Z.1 Financial Accounts of the United States "
           "(holder-side levels, $ millions, quarterly)")
    rows, totals = [], {}
    for holder, d in WANT.items():
        for instr, mnem in d.items():
            date, val = last[mnem]
            if holder == COMBINED:   # emit households NET of nonprofits
                np_mnem = WANT["Nonprofits"][instr]
                np_date, np_val = last[np_mnem]
                assert np_date == date, f"{mnem} vs {np_mnem}: {date} != {np_date}"
                holder_out, mnem_out, val_out = (
                    "Households", f"{mnem} minus {np_mnem}", val - np_val)
            else:
                holder_out, mnem_out, val_out = holder, mnem, val
            rows.append([holder_out, instr, mnem_out, date, round(val_out), src])
            totals[holder_out] = totals.get(holder_out, 0) + val_out
    with open(os.path.abspath(OUT), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["holder", "instrument", "fl_series", "as_of",
                    "value_musd", "source"])
        w.writerows(rows)

    grand = sum(totals.values())
    print("wrote", os.path.abspath(OUT), "| as of", rows[0][3])
    print(f"holder-side total: ${grand/1e6:,.1f}T   (M2 is defined narrower)")
    for h, v in sorted(totals.items(), key=lambda kv: -kv[1]):
        print(f"  {h:<36} ${v/1e6:>5.1f}T  {100*v/grand:5.1f}%")


if __name__ == "__main__":
    main()
