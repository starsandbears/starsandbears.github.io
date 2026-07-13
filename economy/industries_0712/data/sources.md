# Data sources & provenance

Provenance for every dataset in this folder. Verified June 2026 against primary sources during the deep-research cross-check (see `crosscheck-2026-06.md`). ★ = primary government source. Most figures corroborated via FRED, which mirrors BEA/BLS primary series.

---

## `q1-gdp-cake/gdp-value-added-by-industry.csv` — GDP value added by industry

- **Primary source:** ★ U.S. Bureau of Economic Analysis (BEA), *GDP by Industry* (Value Added by Industry).
- **As-of / vintage:**
  - `va_2024_report` = BEA full-year 2024, third estimate (the report's original figures, now superseded).
  - `va_2025` + `share_2025` = BEA full-year **2025, third estimate, released 2026-04-09** (current basis used in the report). All 20 sectors; they sum to GDP ($30,762.1B) with no statistical residual.
- **Classification:** NAICS-based industry sectors (20). `naics` column gives the sector code.
- **URLs:**
  - GDP by Industry portal: https://www.bea.gov/data/gdp/gdp-industry
  - 2025 release (2026-04-09): https://www.bea.gov/news/2026/gdp-third-estimate-industries-corporate-profits-state-gdp-and-state-personal-income-4th
  - iTable (annual value added by industry): https://apps.bea.gov/iTable/?reqid=150&step=2&isuri=1&categories=gdpxind
  - FRED mirror series (column `fred_series`): https://fred.stlouisfed.org/series/GDPA (and VARL, VAG, VAMA, VAPST, VAFI, VAHCSA, VAR, VAW, VAI, VAC, VAT, VAAF, VAOSEG, VAMCE, VAU, VAM, VAAER, VAES, VAAFH)
- **Note:** Administrative & waste (NAICS 56) has no standalone FRED dollar series; derived as VAPBS − VAPST − VAMCE. The exact sum-to-GDP validates it.

## `q1-gdp-cake/gdp-value-added-dollars-history.csv` — Value added by industry in dollars, 2005–2025

- **Primary source:** ★ BEA GDP-by-Industry value added, via FRED quarterly dollar series ($B, SAAR) averaged to annual: VAMA, VAFI, VAPST, VAHCSA, VAI, VARL — the same six series behind `gdp-value-added-shares-history.csv`, so the two files agree by construction.
- **As-of / vintage:** fetched **2026-07-12**; the 2025 rows match the 2025 cake (third estimate, `gdp-value-added-by-industry.csv`) within rounding — the builder asserts this before writing.
- **Units:** **nominal** $ billions (not inflation-adjusted); the report's chart caption says so.
- **Rebuild:** `scripts/q1-gdp-cake/build_value_added_dollars.py`
- **URL:** https://fred.stlouisfed.org/graph/fredgraph.csv?id=VAMA,VAFI,VAPST,VAHCSA,VAI,VARL

## `q2-industry-and-jobs/employment-qcew-naics-2025.csv` — Employment by NAICS sector

- **Primary source:** ★ U.S. Bureau of Labor Statistics (BLS), *Quarterly Census of Employment and Wages* (QCEW), national annual averages.
- **As-of / vintage:** **2025 annual averages (preliminary** — subject to the fall 2026 annual revision). Verified against the BLS QCEW open-data file.
- **Classification:** **NAICS sectors — the SAME taxonomy as the BEA GDP sectors above** (this is the point of the classification fix). `qcew_basis` column records the ownership/agglvl codes used. Government = federal + state + local ownership across all industries (matches BEA's Government sector); private sectors use private ownership.
- **Why QCEW (not CES):** CES publishes coarser "supersectors" (e.g. "financial activities" bundles finance + insurance + real estate). QCEW reports the underlying NAICS sectors, so finance & insurance (52) and real estate (53) stay separate — essential for matching BEA and for the report's "real estate is #1" narrative.
- **Coverage note:** QCEW counts UI-covered jobs (~96% of employment), total ≈155.7M — a few million below the CES headline (~159M) because it excludes most self-employed/proprietors. Use QCEW shares for sector structure, not as a substitute for the CES headline.
- **URLs:**
  - QCEW program: https://www.bls.gov/cew/
  - 2025 US annual data file: https://data.bls.gov/cew/data/api/2025/a/area/US000.csv
  - CES headline total (for reference) via FRED: https://fred.stlouisfed.org/series/PAYEMS

## `q3-productivity/margins-by-sector-2026-01.csv` — Net profit margins by sector

- **Source:** Aswath Damodaran (NYU Stern), *Margins by Sector (US)* — ~6,000 US-listed firms, dollar-weighted aggregates.
- **As-of / vintage:** **January 2026** dataset. Verified exact.
- **Classification:** Damodaran industry groups (US-listed public companies only; not whole-economy).
- **URLs:**
  - Margins by sector: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/margin.html
  - Methodology essay: https://aswathdamodaran.substack.com/p/data-update-5-for-2025-profitability

## Classification note (why the schemes don't line up)

The datasets use three different taxonomies and are **not directly comparable**:

- **BEA value added** — NAICS sectors (splits finance & insurance from real estate; government is its own sector).
- **BLS CES supersectors** — bundles differently: "Financial activities" = finance + insurance + real estate; "Education & health services" = *private* education + health (government education sits in "Government").
- **GICS** (margins) — classifies *companies* by market behavior; "Information Technology" ≠ NAICS "Information."

**For an apples-to-apples output-vs-jobs comparison on one consistent NAICS taxonomy:**
- ★ BLS QCEW (Quarterly Census of Employment and Wages) — jobs on the same NAICS sectors as BEA: https://www.bls.gov/cew/ (data files: https://www.bls.gov/cew/downloadable-data-files.htm)
- ★ BEA–BLS Integrated Industry-Level Production Account (KLEMS) — pairs value added/output with labor on identical NAICS industries: https://www.bea.gov/data/special-topics/integrated-industry-level-production-account-klems and https://www.bls.gov/productivity/articles-and-research/bea-bls-integrated-production-accounts.htm

---

## `q9-supply-demand/supply-vs-need.csv` — supply vs the "need" (population)

- **Source:** ★ FRED **POPTHM** (resident population, thousands; January value per year) and **ETOTALUSQ176N** (Census HVS total housing units, thousands; Q1 value); FHWA *Highway Statistics* **table MV-1** grand total (all registered motor vehicles); World Bank **SH.MED.BEDS.ZS** (hospital beds per 1,000, follows OECD Health Statistics).
- **As-of / vintage:** updated **2026-07-12**. Ragged end on purpose — each series runs to its latest published year: population & housing **2026**, vehicles **2023**, beds **2022**.
- **Deliberate exclusion:** FHWA's 2024 MV-1 exists but is skipped: New York jumps +124% (9.4M → 21.0M registered vehicles, table footnote (3) — a state reporting change), inflating the national total +4.5% in one year. Include it only with an adjusted or footnoted NY series.
- **Reproduce:** `python3 scripts/q9-supply-demand/build_supply_vs_need.py` (values hand-carried from the sources listed in its docstring; the script prints the 2010=100 index the chart shows).
- **URL:** https://fred.stlouisfed.org/graph/fredgraph.csv?id=POPTHM · https://fred.stlouisfed.org/graph/fredgraph.csv?id=ETOTALUSQ176N · https://www.fhwa.dot.gov/policyinformation/statistics/2023/mv1.cfm · https://api.worldbank.org/v2/country/USA/indicator/SH.MED.BEDS.ZS

## `q0-money/m2-vs-net-worth.csv` — money alive (M2) vs families' net worth

- **Source:** ★ FRED series **M2SL** (M2 money stock, monthly, $ billions, SA) and **TNWBSHNO** (households & nonprofit organizations net worth, Fed *Z.1 Financial Accounts* table B.101, quarterly, $ millions, NSA).
- **As-of / vintage:** fetched 2026-07-12; complete years **1990–2025**, each value the annual average of the months/quarters. A partial current year is deliberately excluded (the builder requires 12 months / 4 quarters).
- **What it powers:** the `#m2Line` chart — the money pile next to the net worth all of money's finished lifetimes left behind (~$22T vs ~$177T, 2025 avg; ~$183T by 2026-Q1).
- **Reproduce:** `python3 scripts/q0-money/build_m2_vs_net_worth.py` (downloads both series to /tmp itself).
- **URL:** https://fred.stlouisfed.org/graph/fredgraph.csv?id=M2SL · https://fred.stlouisfed.org/graph/fredgraph.csv?id=TNWBSHNO

## `q0-money/money-holders.csv` — who holds America's ready money, by sector

- **Source:** ★ Federal Reserve, *Z.1 Financial Accounts of the United States* (quarterly holder-side levels, $ millions), from the full-release data download. Each row carries its exact Z.1 mnemonic in `fl_series`.
- **As-of / vintage:** **2026-Q1** (obs date 2026-03-31; June 2026 Z.1 release). Cross-checked against the FRED mirrors (BOGZ1FL… series) — exact matches for corporate/rest-of-world rows; household rows are the *households & nonprofits* sector (FL15…), slightly larger than FRED's households-only FL19… variant.
- **Sectors × instruments:** households & nonprofits (15), nonfinancial corporate (10), nonfinancial noncorporate/small business (11), state & local governments (21), federal government (31), rest of the world (26) — each holding checkable deposits & currency (3020x), time & savings deposits (3030x), and money-market fund shares (3034x).
- **Ruler caveat (disclosed in the report):** holder-side sector accounts total ~$31.0T vs headline M2 ~$23.1T (FRED M2SL), because Z.1 sector data include large time deposits and institutional MMF shares that M2's definition excludes. Shares are of the holder-side total. Context figures cited alongside: bank reserves (FRED WRESBAL, ~$3.1T) and the Treasury General Account (FRED WTREGEN, ~$0.77T) — both money *outside* M2.
- **Reproduce:** download the Z.1 zip (URL below, ~35 MB) then `python3 scripts/q0-money/build_money_holders.py`.
- **URL:** https://www.federalreserve.gov/datadownload/Output.aspx?rel=Z1&filetype=zip (release page: https://www.federalreserve.gov/releases/z1/)
