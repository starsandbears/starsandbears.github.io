# Data — US economy report

Reference data backing `../us-econ-and-money-intro.html`.
Compiled June 2026 via a deep-research cross-check against primary sources (BEA, BLS, Damodaran, Siblis), then used to refresh the report to 2025 data on a consistent NAICS classification.

## Status

The report has been **updated** (June 2026):
- **Staleness fixed** — GDP refreshed from 2024 to **full-year 2025** (BEA, released 2026-04-09; nominal GDP $30,762.1B).
- **Classification fixed** — jobs moved from BLS CES "supersectors" to **BLS QCEW on the same 20 NAICS sectors** as BEA value added, so Questions 1–3 are now apples-to-apples (finance & insurance kept separate from real estate). (The GICS market-cap section this note once covered has since been cut from the report.)

## Files

CSVs live in **per-section subfolders named after the section they power** — e.g. the data behind `sections/q2-industry-and-jobs.html` is in `data/q2-industry-and-jobs/`. Matching builder scripts sit in `../scripts/<same-folder>/`.

| File | What it holds |
|---|---|
| `sources.md` | Provenance for every dataset: source, vintage/as-of date, classification scheme, and URLs. |
| `crosscheck-2026-06.md` | Original fact-check findings: number spot-checks, staleness, corrections, classification recommendation. |
| `q1-gdp-cake/gdp-value-added-by-industry.csv` | BEA value added by industry — 2024 (original report) + full-year 2025 (current), all 20 NAICS sectors. |
| `q2-industry-and-jobs/employment-qcew-naics-2025.csv` | BLS QCEW employment by NAICS sector, 2025 annual averages (the basis used in Question 2). |
| `q3-productivity/margins-by-sector-2026-01.csv` | Damodaran net profit margins by sector, Jan 2026 (the profit chart in Question 3; unchanged, verified). |
| `q0-money/m2-vs-net-worth.csv` | M2 money stock vs households' net worth, annual averages 1990–2025 (FRED M2SL + Z.1 TNWBSHNO; the money-pile-vs-net-worth chart). Rebuild: `scripts/q0-money/build_m2_vs_net_worth.py`. |
| `q0-money/money-holders.csv` | Who **holds** America's ready money (cash, checking, savings, money-market funds), by sector — households ~66%, businesses ~21%, governments ~6%, rest of world ~8% (Fed Z.1, Q1 2026). Powers the "who holds the money?" chart. Rebuild with `scripts/q0-money/build_money_holders.py`. |
| `q1-gdp-cake/gdp-value-added-shares-history.csv` | Each industry's share of GDP over time (powers the cake-over-time chart). |
| `q1-gdp-cake/gdp-value-added-dollars-history.csv` | Each industry's value added in nominal dollars, 2005–2025 (the slices-in-dollars chart). Rebuild: `scripts/q1-gdp-cake/build_value_added_dollars.py`. |
| `q2-industry-and-jobs/gross-output-vs-value-added-2025.csv` | Gross output vs value added by industry, 2025 (money-through vs new-value chart). |
| `state-explorer/state-by-industry-2025.csv` | State × industry GDP/jobs/pay (the state picker; the superseded 2024 file is kept alongside). Rebuild: `scripts/state-explorer/build_state_by_industry.py`. |
| `state-explorer/state-gdp-history.csv` | State × industry value added, 2005–2025 nominal $B (the state layers-over-time chart). Rebuild: `scripts/state-explorer/build_state_gdp_history.py`. |
| `q2-industry-and-jobs/income_by_industry.csv` | Average pay by industry (the pay bars). Rebuild: `scripts/q2-industry-and-jobs/build_income_by_industry.py`. |
| `q5-family-budget/spending_history.csv` | BLS CES household spending by category, 1984–2024 (budget donut **and** the over-time charts in `sections/q6-over-time.html`). |
| `q7-by-age/spending_by_age.csv`, `q7-by-age/spending_by_income_class.csv` | Spending by age group / by income quintile (BLS CES 2024). |
| `q8-where-you-live/…` | `spending_by_state.csv` + `income_by_state.csv` (map & scatter), `spending-by-state-2024.csv` (per-state category chart — 11 kid categories from BEA SAPCE3 detail on the SAPCE2 per-capita ruler; rebuild: `scripts/q8-where-you-live/build_spending_by_state.py`). |
| `q9-supply-demand/supply-vs-need.csv` | Homes/cars/hospital-beds vs population, 2010 to each series' latest year (people & homes 2026, cars 2023, beds 2022; FHWA's 2024 car count skipped — NY reporting break). Rebuild: `scripts/q9-supply-demand/build_supply_vs_need.py`. |

Full source URLs and vintages for each dataset are in **`sources.md`**.

## Key facts

- **Numbers verified accurate.** Every figure traced to a primary source checked out within rounding; the 2025 value-added sectors sum to GDP with no statistical residual, and QCEW private + government reconciles to total covered employment.
- **2025 ranking shift:** finance & insurance ($2,441.9B) now exceeds health care ($2,371.1B) in value added; wholesale nearly equals retail.
- **Consistent-taxonomy basis:** BEA value added + BLS QCEW on matched NAICS sectors. For output and labor on one integrated NAICS account, see the BEA–BLS Integrated Industry-Level Production Account (KLEMS) — link in `sources.md`.

See `crosscheck-2026-06.md` for the full original cross-check, confidence levels, and source URLs.
