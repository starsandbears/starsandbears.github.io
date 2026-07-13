#!/usr/bin/env python3
"""
Build the state x industry dataset (GDP, jobs, pay) that powers the state
pickers in the reports -> ../../data/state-explorer/state-by-industry-<YEAR>.csv (50 states + DC + a
"United States" total, x 20 NAICS-style industries).

WHAT IT PRODUCES
  - GDP  : each industry's value added, $ millions (BEA, nominal, YEAR)
  - jobs : each industry's employment, thousands (BLS QCEW, YEAR)
  - pay  : each industry's average annual pay, $ (BLS QCEW, YEAR)
  Method (consistent across GDP/jobs/pay): the 19 private industries are
  PRIVATE-sector only; "Government" is federal + state + local combined, so
  public teachers/hospital staff are counted once (in Government, not in the
  private education/health sectors).

RAW INPUTS (download first; large, not kept in the repo):
  1. QCEW state files (jobs & pay) -> /tmp/qs<YEAR>/<ABBR>.csv, one per state, from
     https://data.bls.gov/cew/data/api/<YEAR>/a/area/<FIPS>000.csv  (01 AL ... 56 WY, 11 DC).
     Jobs/pay per industry = sum over PRIVATE ownership (agglvl 54, own_code 5)
     per 2-digit NAICS; Government = fed+state+local (agglvl 51, own 1/2/3).
  2. BEA SAGDP (GDP by industry by state):
     https://apps.bea.gov/regional/zip/SAGDP.zip  -> unzip to /tmp/sagdp/
     (uses table SAGDP2, nominal current dollars).

OUTPUTS
  - ../../data/state-explorer/state-by-industry-<YEAR>.csv
  - /tmp/state_block.js  (const IND=[...]; const STATES={...}; embedded into the
                          hand-written Plotly state explorer in the economy report)

Run (after the two downloads above):
  python3 scripts/state-explorer/build_state_by_industry.py
"""
import csv, json, os

YEAR = "2025"
QS = "/tmp/qs" + YEAR
BEA = "/tmp/sagdp/SAGDP2__ALL_AREAS_1997_2025.csv"
OUT_JS = "/tmp/state_block.js"
# standalone home: written once, next to this report's other data
_HERE = os.path.dirname(os.path.abspath(__file__))
# scripts/<section>/ mirrors data/<section>/ — derive the folder name
OUT_CSV = os.path.join(_HERE, "..", "..", "data", os.path.basename(_HERE),
                       "state-by-industry-"+YEAR+".csv")

NAME2ABBR = {"Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA",
"Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Florida":"FL",
"Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS",
"Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI",
"Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV",
"New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC",
"North Dakota":"ND","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI",
"South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT",
"Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
ABBR2NAME = {v:k for k,v in NAME2ABBR.items()}

# NAICS 2-digit sector code -> report label (19 private sectors)
SECTORS = {"11":"Agriculture, forestry, fishing","21":"Mining","22":"Utilities","23":"Construction",
"31-33":"Manufacturing","42":"Wholesale trade","44-45":"Retail trade","48-49":"Transportation & warehousing",
"51":"Information","52":"Finance & insurance","53":"Real estate, rental & leasing",
"54":"Professional, sci & technical","55":"Management of companies","56":"Administrative & waste svcs",
"61":"Educational services","62":"Health care & social assist.","71":"Arts, entertainment & rec.",
"72":"Accommodation & food svcs","81":"Other services"}
GOV = "Government"
IND = list(SECTORS.values()) + [GOV]  # 20 labels

def blank():
    return {lbl:0.0 for lbl in IND}

# ---- QCEW jobs & pay ----
jobs, wages = {}, {}
for ab in ABBR2NAME:
    fp = os.path.join(QS, ab+".csv")
    jb, wg = blank(), blank()
    gov_emp = gov_wage = 0
    with open(fp) as f:
        for r in csv.DictReader(f):
            ag, own, ic = r["agglvl_code"], r["own_code"], r["industry_code"]
            emp = int(r["annual_avg_emplvl"] or 0); w = int(r["total_annual_wages"] or 0)
            if ag == "54" and own == "5" and ic in SECTORS:      # private sector
                jb[SECTORS[ic]] += emp; wg[SECTORS[ic]] += w
            elif ag == "51" and ic == "10" and own in ("1","2","3"):  # government (fed/state/local)
                gov_emp += emp; gov_wage += w
    jb[GOV] = gov_emp; wg[GOV] = gov_wage
    jobs[ab], wages[ab] = jb, wg

# ---- BEA GDP ($millions, YEAR) ----
gdp = {ab: blank() for ab in ABBR2NAME}
naics2lbl = {code:lbl for code,lbl in SECTORS.items()}
with open(BEA, encoding="latin-1") as f:
    rows = list(csv.reader(f))
hdr = rows[0]; yidx = hdr.index(YEAR)
for r in rows[1:]:
    if len(r) <= yidx: continue
    name = r[1].strip()
    ab = NAME2ABBR.get(name)
    if not ab: continue
    naics = r[5].strip(); desc = r[6].strip(); val = r[yidx].strip()
    try: v = float(val)
    except ValueError: continue
    if naics in naics2lbl:
        gdp[ab][naics2lbl[naics]] = v
    elif desc == "Government and government enterprises":
        gdp[ab][GOV] = v

# ---- assemble + US aggregate ----
def pay_from(w, j):
    return {lbl: (round(w[lbl]/j[lbl]) if j[lbl] else 0) for lbl in IND}

STATES = {}
us_j, us_w, us_g = blank(), blank(), blank()
for ab in ABBR2NAME:
    j, w, g = jobs[ab], wages[ab], gdp[ab]
    STATES[ab] = {"n": ABBR2NAME[ab],
                  "gdp":[round(g[l],1) for l in IND],
                  "jobs":[round(j[l]/1000) for l in IND],      # thousands of jobs
                  "pay":[pay_from(w,j)[l] for l in IND]}
    for l in IND: us_j[l]+=j[l]; us_w[l]+=w[l]; us_g[l]+=g[l]
US = {"n":"United States",
      "gdp":[round(us_g[l],1) for l in IND],
      "jobs":[round(us_j[l]/1000) for l in IND],
      "pay":[pay_from(us_w,us_j)[l] for l in IND]}
ALL = {"US":US, **STATES}

with open(OUT_JS,"w") as f:
    f.write("const IND="+json.dumps(IND)+";\n")
    f.write("const STATES="+json.dumps(ALL, separators=(",",":"))+";\n")

src="GDP: BEA SAGDP2 nominal "+YEAR+"; Jobs/Pay: BLS QCEW "+YEAR+" (private sectors=private ownership, Government=fed+state+local)"
rows_out=[["state","industry","gdp_millions_"+YEAR,"jobs_thousands_"+YEAR,"avg_pay_"+YEAR,"source"]]
for ab in ["US"]+list(ABBR2NAME):
    d=ALL[ab]
    for i,l in enumerate(IND):
        rows_out.append([d["n"],l,d["gdp"][i],d["jobs"][i],d["pay"][i],src])
with open(OUT_CSV,"w",newline="") as f:
    csv.writer(f).writerows(rows_out)

# sanity
print("states:",len(STATES),"+US | industries:",len(IND))
print("US Government jobs (k):", US["jobs"][IND.index(GOV)], "| US Health care jobs (k):", US["jobs"][IND.index("Health care & social assist.")])
print("US total GDP ($M):", round(sum(US["gdp"])) , "| US Manufacturing pay:", US["pay"][IND.index("Manufacturing")], "Accommodation pay:", US["pay"][IND.index("Accommodation & food svcs")])
print("CA GDP total ($M):", round(sum(STATES["CA"]["gdp"])), "| CA gov jobs(k):", STATES["CA"]["jobs"][IND.index(GOV)])
print("wrote", OUT_JS, "and", OUT_CSV)
print("JS size (KB):", round(os.path.getsize(OUT_JS)/1024,1))
