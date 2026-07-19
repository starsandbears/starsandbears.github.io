# Deep-research cross-check — US economy report

**Subject:** `../index.html`
**Date of check:** June 2026
**Method:** Multi-source web research against primary sources (BEA, BLS, NYU Stern/Damodaran, Siblis). Each load-bearing number corroborated against at least one independent source (mostly FRED, which mirrors BEA/BLS primary series).

---

## Bottom line

The report's data is **sound and accurately transcribed** — every number traceable to a primary source checks out within rounding (May 2026 employment and Jan 2026 Damodaran margins match *exactly*; all ten 2024 value-added figures within ~3%). **But there is meaningfully newer data:** BEA released full-year **2025** GDP-by-industry on **2026-04-09**, and the **Sept 2025 comprehensive update** revised 2024 nominal GDP to **$29,298.0B** (was $29,184.9B). On classification, the report's three schemes genuinely don't line up 1:1, but there is a clean fix (BLS QCEW or BEA–BLS KLEMS).

---

## Task A — Is there newer data than 2024?

**Yes — full-year 2025 is available now.**

- Latest annual GDP-by-industry came with **"GDP (Third Estimate), Industries… 4th Quarter and Year 2025," released 2026-04-09** (delayed from late-March by the Oct–Nov 2025 government shutdown). Real GDP rose **2.1%** in 2025.
- **Full-year nominal GDP: 2024 = $29,298.0B; 2025 = $30,762.1B** (FRED GDPA, sourced from BEA). 2024 was revised **+$113B** from the report's $29,184.9B by the Sept-2025 comprehensive update.
- **Update schedule:** prior-year annual industry detail lands with the late-March "4th Quarter and Year" third estimate, then is revised in the fall (Sept) annual GDP-by-industry / comprehensive NIPA update. Expect the next 2025 revision ~Sept 2026.

2025 value-added-by-industry figures are in `gdp-value-added-by-industry.csv`. Notable 2024→2025 shifts: **finance & insurance jumped past health care**; **wholesale nearly caught retail**; information grew strongly.

---

## Task B — Industry-classification consistency

### Why the three schemes don't align
- **BEA value-added by industry** = ~20 NAICS-based sectors; splits *Finance & insurance* from *Real estate & rental/leasing*; *Government* is its own sector (federal/state/local).
- **BLS CES "supersectors"** = establishment-survey groupings. "**Financial activities**" bundles **finance + insurance + real estate** (BEA reports those as two separate sectors). "**Education & health services**" = *private* education + health/social assistance and **excludes public/government education** (that sits in CES "Government"). "Professional & business services" merges BEA's professional/scientific/technical + management + administrative/waste.
- **GICS** (Damodaran/market-cap sections) is an **equity-market taxonomy unrelated to NAICS** — classifies *companies* by revenue/market behavior, not establishments by production. GICS "Information Technology" ≠ NAICS "Information" (Amazon/Alphabet/Meta sit in Consumer Discretionary / Communication Services, not IT). Cannot be reconciled to NAICS 1:1; should not be compared head-to-head with GDP/jobs sectors.

### Recommended consistent-taxonomy fix (output vs. jobs on one NAICS scheme)
1. **Best single source — BEA–BLS Integrated Industry-Level Production Account ("KLEMS").** Purpose-built to pair **value added / gross output with labor input on identical NAICS industries** (to ~3-digit).
   - BEA: https://www.bea.gov/data/special-topics/integrated-industry-level-production-account-klems
   - BLS: https://www.bls.gov/productivity/articles-and-research/bea-bls-integrated-production-accounts.htm
2. **Simplest practical pairing for ~20 sectors:** BEA **Value Added by Industry** + **BLS QCEW** (Quarterly Census of Employment and Wages), which counts employment on the *same NAICS sectors* (covers ~95% of jobs).
   - https://www.bls.gov/cew/ — data files: https://www.bls.gov/cew/downloadable-data-files.htm
   - QCEW is more granular/consistent than CES supersectors. (CES does have NAICS-sector series, but its *published* supersectors are the bundled groupings that cause the mismatch.)

**Recommendation:** report GDP/value added from BEA GDP-by-Industry and jobs from BLS QCEW on matched NAICS sectors for an apples-to-apples table; cite KLEMS if also showing productivity / output-per-worker on the same industries.

---

## Task C — Number spot-checks

| Figure | Report value | Source value | Verdict | Source |
|---|---|---|---|---|
| Total US GDP 2024 (nominal) | $29,184.9B | $29,298.0B (revised) | **Stale** — correct as Mar-2025 3rd est., since revised +0.39% | BEA / FRED GDPA |
| Real estate VA 2024 | 4,025.8 | 4,052.4 | OK (+0.7%) | BEA / FRED VARL |
| Government VA 2024 | 3,293.7 | 3,296.3 | ✓ (+0.08%) | BEA / FRED VAG |
| Manufacturing VA 2024 | 2,913.1 | 2,880.7 | OK (−1.1%) | BEA / FRED VAMA |
| Professional/sci/tech VA 2024 | 2,381.2 | 2,355.1 | OK (−1.1%) | BEA / FRED VAPST |
| Health care VA 2024 | 2,211.7 | 2,209.4 | ✓ (−0.1%) | BEA / FRED VAHCSA |
| Finance & insurance VA 2024 | 2,164.2 | 2,229.2 | OK (+3.0%, largest revision) | BEA / FRED VAFI |
| Retail VA 2024 | 1,841.7 | 1,849.1 | ✓ (+0.4%) | BEA / FRED VAR |
| Wholesale VA 2024 | 1,706.8 | 1,706.3 | ✓ | BEA / FRED VAW |
| Information VA 2024 | 1,569.5 | 1,592.7 | OK (+1.5%) | BEA / FRED VAI |
| Construction VA 2024 | 1,312.3 | 1,305.4 | ✓ (−0.5%) | BEA / FRED VAC |
| Total nonfarm emp (May 2026) | 159M | 159.001M | ✓ exact | BLS CES / FRED PAYEMS |
| Education & health svcs | 27.886M | 27,886K | ✓ exact | FRED USEHS |
| Government | 23.387M | 23,387K | ✓ exact | FRED USGOVT |
| Professional & business svcs | 22.468M | 22,468K | ✓ exact | FRED USPBS |
| Leisure & hospitality | 17.079M | 17,079K | ✓ exact | FRED USLAH |
| Retail | 15.458M | 15,457.9K | ✓ exact | FRED USTRADE |
| Manufacturing | 12.605M | 12,605K | ✓ exact | FRED MANEMP |
| Financial activities | 9.104M | 9,104K | ✓ exact | FRED USFIRE |
| Information | 2.783M | 2,783K | ✓ exact | FRED USINFO |
| Whole-market net margin | 9.7% | 9.74% | ✓ | Damodaran Jan 2026 |
| Semiconductor net margin | 30.5% | 30.45% | ✓ | Damodaran |
| Software net margin | 25.5% | 25.49% (System & Application) | ✓ | Damodaran |
| Bank (money center) net margin | 28.9% | 28.89% | ✓ | Damodaran |
| Air transport net margin | 2.5% | 2.51% | ✓ | Damodaran |
| Grocery net margin | 1.3% | 1.32% | ✓ | Damodaran |
| Total US public market cap | ~$69T | $68.96T (Jan 1, 2026) | ✓ exact | Siblis Research |
| S&P 500 total cap | ~$60T | plausible (~87% of $69T) | OK — not independently pinned | — |
| Info Tech ~$19.2T (~32% of S&P 500) | 32% | ~30–32% early 2026, drifting up | OK / Medium — date it | S&P DJI / MacroMicro |

**Confidence:** High for all BEA value-added, BLS employment, Damodaran, and Siblis figures. Medium for S&P 500 $60T and the IT 32% weight (plausible and consistent, but the exact IT weight rose through 2026).

---

## Corrections needed (if refreshing the report)

- **Update headline 2024 nominal GDP $29,184.9B → $29,298.0B** (Sept-2025 comprehensive update). Re-label $29,184.9B as "March 2025 third estimate, since revised."
- **Add full-year 2025** as the current dataset: nominal GDP **$30,762.1B**; refresh the value-added table to 2025 (see CSV). Relabel 2024 column as revised where it moved (notably finance & insurance 2,164.2→2,229.2; real estate 4,025.8→4,052.4; manufacturing 2,913.1→2,880.7).
- **Note the 2025 ranking change:** finance & insurance now exceeds health care and nearly ties professional/sci/tech; wholesale nearly equals retail.
- **Employment, margins, Siblis $69T need no change.** Optionally date/update the IT/S&P 500 weight, which has risen since Jan 2026.
- **Classification footnote:** state explicitly that Sections 1, 2, and 4/6 use different taxonomies (NAICS value-added vs. CES supersectors vs. GICS) and are not directly comparable; if cross-comparison is intended, rebuild jobs on QCEW/NAICS or use BEA–BLS KLEMS.

---

## Sources (★ = primary government)

1. ★ BEA, "GDP (Third Estimate)… 4th Quarter and Year 2025," 2026-04-09 — https://www.bea.gov/news/2026/gdp-third-estimate-industries-corporate-profits-state-gdp-and-state-personal-income-4th
2. ★ BEA, "GDP (Advance Estimate), 4th Quarter and Year 2025" — https://www.bea.gov/news/2026/gdp-advance-estimate-4th-quarter-and-year-2025
3. ★ BEA, "GDP… 4th Quarter and Year 2024 (Third Estimate)," Mar 2025 (report's original source) — https://www.bea.gov/news/2025/gross-domestic-product-4th-quarter-and-year-2024-third-estimate-gdp-industry-and
4. ★ BEA GDP by Industry / iTable — https://www.bea.gov/data/gdp/gdp-industry
5. ★ BEA value-added & nominal GDP series via FRED: GDPA, GDP, VARL, VAG, VAMA, VAPST, VAHCSA, VAFI, VAR, VAW, VAI, VAC — e.g. https://fred.stlouisfed.org/series/GDPA
6. ★ BLS Employment Situation, May 2026 (CES) — https://www.bls.gov/news.release/empsit.nr0.htm ; series via FRED PAYEMS, USEHS, USGOVT, USPBS, USLAH, USTRADE, MANEMP, USFIRE, USINFO
7. ★ BLS QCEW — https://www.bls.gov/cew/ ; data files https://www.bls.gov/cew/downloadable-data-files.htm
8. ★ BEA–BLS Integrated Industry-Level Production Account (KLEMS) — https://www.bea.gov/data/special-topics/integrated-industry-level-production-account-klems ; https://www.bls.gov/productivity/articles-and-research/bea-bls-integrated-production-accounts.htm
9. Damodaran (NYU Stern), Net Margins by Sector, "as of January 2026" — https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/margin.html
10. Siblis Research, US Stock Market Total Market Value (Jan 1, 2026 = $68.96T) — https://siblisresearch.com/data/us-stock-market-value/
11. S&P Dow Jones Indices, S&P 500 Information Technology sector — https://www.spglobal.com/spdji/en/indices/equity/sp-500-information-technology-sector/ ; MacroMicro — https://en.macromicro.me/collections/34/us-stock-relative/121244/sp-500-gics-sectors-weightings-monthly

**Unresolved caveat:** the exact S&P 500 total market cap (~$60T) and precise IT share could not be pinned to a single primary source; aggregators put IT ~30% in Jan 2026 and higher later in 2026, so the report's "~32%" is reasonable for early 2026 but should be dated.
