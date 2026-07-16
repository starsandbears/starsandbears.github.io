# The Economy Boat & Our Money, Explained to My 8-Year-Old

An interactive, kid-friendly Q&A report on the US economy: where money comes
from, the GDP cake, industries, jobs & pay, the family budget (with a
"spend $1,000 on what you value" allocator), prices over time, supply &
demand, and AI & deflation, closing on an AI-abundance vision — with live
Plotly/Bokeh charts and a pick-your-state explorer.

**Page:** `us-econ-and-money-intro.html`
**Published at:** `https://starsandbears.github.io/economy/industries_0712/us-econ-and-money-intro.html` (after push)

## How the page is put together

The report is written LaTeX-style: a small **main file** plus one **child file
per section**, assembled by Jekyll — which GitHub Pages runs automatically on
every push. There is nothing to build locally and no generated file to keep in
sync: **the child files are the only source of truth.**

```
us-econ-and-money-intro.html   ← main file: <head>, hero, background
                                        playground (seesaws + cake slices),
                                        table of contents, and one include
                                        line per section (like \input)
style.css                             ← all page styles (linked from the main
                                        file)
sections/
  q0-money.html                       ← one child file per Q&A section; the
  q1-gdp-cake.html                      "qN" in the file name matches the
  q2-industry-and-jobs.html             Question-N chip displayed inside it
  state-explorer.html                 ← pick-your-state (no question number)
  q3-productivity.html
  q4-value-of-industry.html
  q5-family-budget.html               ← + the $1,000 allocator
  q6-over-time.html
  q7-by-age.html
  q8-where-you-live.html
  q9-supply-demand.html
  q10-ai-costs.html                   ← AI & costs + good/bad deflation and
                                        the AI-abundance smart-city vision (a
                                        bond/fund what-if sits inside, commented
                                        out)
  closing.html                        ← what is the economy / meaning of money
  footer.html                         ← sources & disclaimer
  page-scripts.html                   ← all chart-drawing JavaScript (Plotly
                                        calls + one embedded Bokeh document)
  a11y.html                           ← accessibility toolbar (read-aloud,
                                        dyslexia font, text size)
data/                                 ← every dataset behind the charts, in
  q0-money/                             per-section subfolders named after the
  q2-industry-and-jobs/ …               section they power (only sections with
                                        data have one); provenance docs at the
                                        root
scripts/                              ← data fetchers/builders, in the same
  q0-money/ …                           per-section folders; each writes its
                                        CSV into data/<same-section>/
diagrams/                             ← Excalidraw sources + generator script
                                        (money lifecycle); the page links
                                        money-lifecycle-full.svg (Question 0).
                                        bank-money-lifecycle.svg is currently
                                        unused
```

In the main file each section appears as:

```liquid
{% include_relative sections/q5-family-budget.html %}
```

Jekyll replaces that line with the file's contents when it builds the site.
Each child file is wrapped in `{% raw %} … {% endraw %}` — keep those as the
first and last lines; they tell Jekyll to treat everything in between as plain
HTML/JS.

## Editing

- **Change a section's words:** edit its file in `sections/`. That's it.
- **Add a section:** create `sections/qN-slug.html` (numbered Q&A) or
  `sections/slug.html` (unnumbered; copy an existing one as a template, keep
  the `raw` guards), then add its `include_relative` line in the main file
  where it should appear.
- **Reorder / remove:** move or delete the include line in the main file.
- **Renumbering:** the displayed "Question N" chips are hand-written and the
  file names now follow them. If you add, remove, or reorder a numbered
  section, also update (a) later sections' chips, file names, ids, and the
  include/TOC lines in the main file, and (b) any prose cross-references —
  search the folder for `Question <number>`. The `data/` and `scripts/`
  subfolders are named after their section too — rename them together with it
  (builder scripts derive their output folder from the folder name).
- **Site-wide styles:** all CSS lives in `style.css` (linked from the main
  file's `<head>`).
- **Chart data:** all of it — Plotly and Bokeh — is embedded in
  `sections/page-scripts.html`; the section files contain only each chart's
  empty mount point (a `div`), so don't look for numbers there. To refresh from
  source: run the matching `scripts/` builder (updates the CSV in `data/` for
  provenance), then update the embedded numbers in `page-scripts.html` to
  match. The Bokeh charts live inside one serialized `docs_json` document on a
  single (very long) line — edit it programmatically (parse → modify →
  re-serialize), not by hand.
- **Diagrams:** edit + run the matching `diagrams/make_*.py`, then replace the
  embedded/linked SVG it regenerates.

## Previewing

Opening the main file straight in a browser shows unprocessed
`include_relative` lines — that's expected: it's source, and the assembly
normally happens on GitHub's servers. To view locally:

```
python3 preview.py
```

It assembles the child files into **`_preview.html`** (marked "generated — do
not edit"; never commit it — if this folder ever becomes git-tracked, add
`_preview.html` to `.gitignore` first) and opens that in your browser. Edit a
section, re-run, refresh. Alternatives: push and view the live site (~1 min),
or `gem install jekyll && jekyll serve` from the repo root.

## Data & scripts

`data/` holds all 19 CSVs the charts were built from — organised into
per-section subfolders mirroring `sections/` — with provenance in
`data/sources.md` and `data/README.md`. `scripts/` holds the fetchers/builders (Python 3 stdlib
only; raw downloads land in `/tmp` — see each script's docstring for its
source URLs and run instructions).

*Data vintages: GDP/value added 2025; jobs & pay (QCEW) 2025; household
spending (CES) 2024; state PCE 2024; consumer-spending share of GDP (BEA/FRED)
2025; M2 & net worth (FRED/Z.1) 2025. Educational project — not investment,
financial, or legal advice.*
