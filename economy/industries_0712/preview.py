#!/usr/bin/env python3
"""
Instant local preview of the report — no Jekyll needed.

The main file (index.html) is SOURCE: it holds
{% include_relative sections/... %} lines that GitHub Pages' Jekyll expands at
deploy time. Opening it directly in a browser therefore shows the raw include
lines instead of the page. This script does the same expansion Jekyll does —
strip the front matter, inline each included child file, drop the
{% raw %}/{% endraw %} guards — writes the result to _preview.html, and opens
it in your browser.

_preview.html is a throwaway build artifact — don't commit it (its underscore
prefix means Jekyll excludes it from the published site anyway; if economy/
ever becomes git-tracked, add _preview.html to .gitignore first).
NEVER edit it — edit the files in sections/ and re-run this.

Run:  python3 preview.py            (writes _preview.html and opens it)
      python3 preview.py --no-open  (just writes the file)
"""
import os
import re
import sys
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(HERE, "index.html")
OUT = os.path.join(HERE, "_preview.html")


def main():
    doc = open(MAIN, encoding="utf-8").read()
    # 1. front matter off
    assert doc.startswith("---\n---\n"), "main file lost its front matter?"
    doc = doc[len("---\n---\n"):]
    # 2. expand the include_relative lines (paths are relative to the main file)
    def inline(m):
        return open(os.path.join(HERE, m.group(1)), encoding="utf-8").read()
    doc, n = re.subn(r'\{% include_relative ([^ ]+) %\}', inline, doc)
    # 3. drop the raw guards
    doc = doc.replace("{% raw %}\n", "").replace("{% endraw %}\n", "")
    leftover = [l for l in doc.split("\n") if "{%" in l or "{{" in l]
    assert not leftover, f"unexpanded Liquid remains: {leftover[:2]}"

    banner = ("<!-- GENERATED PREVIEW - DO NOT EDIT. "
              "Edit sections/*.html and re-run preview.py -->\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(banner + doc)
    print(f"expanded {n} includes -> {OUT}")
    if "--no-open" not in sys.argv:
        webbrowser.open("file://" + OUT)


if __name__ == "__main__":
    main()
