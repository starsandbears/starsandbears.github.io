# The Hitchhiker's Guide to Swimming — Volume One: introducing the water

A learning note in the spirit of Douglas Adams and of David Foster Wallace's
"This Is Water", told through verbatim, source-verified quotations. Its theme
in one line: influence is inevitable; it is not neutral; and so much of it is
a gift. Volume One makes those three moves in order — an ordinary Thursday
replayed from underwater (influence is everywhere and impossible to opt out
of), the manipulation philosophers on why no water is neutral and what makes
a decision your own anyway, and the gifts the water carries from the swimmers
who came before — with an undersea CSS/SVG scene swimming behind the text.

The series continues onward:

- **Volume II** — the temperature of the water: persuasion, coercion and
  manipulation, and empowering vs. steering — at `../water_temperature/`
- **Volume III** — a discussion panel with fellow fishes on how to swim —
  at `../swimming/`
- **Volume IV** — becoming water; the treasure is still under the seaweed,
  and its location has no path yet

**Page:** `index.html`
**Published at:** `https://starsandbears.github.io/science/water/`

## How the page is put together

The note is written LaTeX-style: a small **main file** plus one **child file
per section**, assembled by Jekyll — which GitHub Pages runs automatically on
every push. There is nothing to build locally and no generated file to keep in
sync: **the child files are the only source of truth.**

```
index.html                     ← main file: <head>, undersea background
                                 (rays, bubbles, fish, whales, octopus, crab,
                                 turtle, jellyfish, seafloor), topbar,
                                 contents sidenav, hero, and one include line
                                 per section (like \input)
style.css                      ← all page styles (linked from the main file)
preview.py                     ← local preview: expands the includes the way
                                 Jekyll does and writes _preview.html
sections/
  thursday.html                       ← 1 · An ordinary Thursday: the same day
                                        twice, from above and from underwater
                                        (+ the "The water" part divider)
  no-still-water.html                 ← 2 · There is no neutral water: no
                                        influence-free baseline; manipulation
                                        as hidden influence; relational
                                        autonomy
  gifts.html                          ← 3 · Gifts in the water: the whale
                                        grandfather, the octopus father, and
                                        gratitude before any caution
  next-volume.html                    ← To be continued: the map of
                                        Volumes II–IV
  footer.html                         ← Sources & notes; the reference list
                                        between the REFS markers is GENERATED
                                        — edit data/sources.json instead
  a11y.html                           ← accessibility toolbar (read-aloud,
                                        dyslexia font, text size)
  page-scripts.html                   ← scrollspy + accessibility JavaScript
data/
  sources.json                        ← the bibliography: each source with
                                        area, finding, and (where the full
                                        text was reachable) the verbatim
                                        quotes used on the page plus where
                                        each was verified
scripts/
  build_references.py                 ← regenerates the reference list in
                                        sections/footer.html from sources.json
                                        and verifies every in-text citation
                                        resolves and every source is cited
```

## Editing rules

- Quotations on the page are **verbatim complete passages** — no elisions.
  Never touch quote text without re-verifying against the linked source;
  every quote lives in `data/sources.json` with a `quote_source` note saying
  where it was checked.
- After changing citations or `data/sources.json`, run
  `python3 scripts/build_references.py`.
- To preview locally, run `python3 preview.py` (never edit `_preview.html`).
