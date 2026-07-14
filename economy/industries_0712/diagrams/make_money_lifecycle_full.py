#!/usr/bin/env python3
"""
"The Life of Our Money — the full picture": merges the two hand-drawn-style
lifecycle diagrams (money-lifecycle = the Fed/QE story, bank-money-lifecycle =
the loans-create-deposits story) into one. The shared middle of both stories —
the years a $100 spends working in the economy — is the big center box; the
two nurseries (Fed bond trade, bank loan trade) feed into it from above, and
the two ways home (bond repaid at the Fed, loan repaid at the bank) drain it
below, each with its own recycle loop.

Same palette and embedded Excalifont as its two parents, so it reads as the
same family. Sources: Federal Reserve (QE/QT mechanics); Bank of England,
"Money creation in the modern economy" (Quarterly Bulletin 2014 Q1).

Emits two files (same layout):
  diagrams/money-lifecycle-full.excalidraw  (openable/editable in Excalidraw;
                                             re-export from there for the
                                             hand-drawn look if preferred)
  diagrams/money-lifecycle-full.svg         (responsive; embedded in the report)

Run: python3 diagrams/make_money_lifecycle_full.py
"""
import base64
import json
import os
import random
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1160, 900   # narrow canvas = less downscaling in the text column, so
                   # the 18px body text stays readable without zooming

INK = "#1e1e1e"
GREY = "#5b6678"
BLUE = "#1971c2"
PURPLE = "#8a5cc4"
# kind -> (fill, stroke, title_color)  — same palette as the parent diagrams
PAL = {
    "fedborn":  ("#ebfbee", "#2f9e44", "#2f9e44"),
    "bankborn": ("#b2f2bb", "#2f9e44", "#1971c2"),
    "work":     ("#e7f5ff", "#1c7ed6", "#1c7ed6"),
    "home":     ("#fff9db", "#f08c00", "#f08c00"),
}

# Latin subset of Excalifont — shared with make_bank_money_lifecycle.py; see
# that script's header for how it was built.
FONT_FILE = os.path.join(HERE, "excalifont-latin.woff2")

TITLE = "The Life of Our Money — the full picture 💵"
SUBTITLE = "born in two nurseries → one big working life → two ways home"

# box: (kind, x, y, w, h, title, [body lines])
BOXES = [
    ("fedborn", 140, 110, 450, 110,
     "1a. Born at the FED 🏛️",
     ["QE: when the economy needs more",
      "money, the Fed makes a brand-new $100."]),
    ("fedborn", 140, 250, 450, 110,
     "2a. TRADE for a bond 🤝",
     ["The Fed hands the $100 to banks",
      "and gets a bond."]),
    ("bankborn", 610, 160, 380, 150,
     "1b. Born at a BANK ✍️",
     ["A bank types a brand-new $100",
      "into a borrower's account, traded",
      "for a loan."]),
    ("work", 160, 420, 800, 180,
     "3. OFF TO WORK 🏪🏡🚗🍭 (for years)",
     ["Fed-born or bank-born, it hops from hand to hand so businesses and",
      "people can use it to create and consume — jobs, houses, food, cars,",
      "new shops, lessons, services, etc. — everyone takes a turn holding it.",
      "Its job: keep flowing and serving different people at different times."]),
    ("home", 140, 640, 450, 150,
     "4a. CALLED HOME to the Fed 🏛️",
     ["Pay-back day for the bond! Or the Fed",
      "could sell the bond to get the money",
      "back. The $100 returns to its maker.",
      "Reinvest it ♻ — or poof, gone: QT 💸💨"]),
    ("home", 610, 640, 470, 150,
     "4b. CALLED HOME to the bank 🏦",
     ["Pay-back day for the loan! The borrower",
      "hands back $100 they earned — erased 💸💨.",
      "The bank keeps only the interest."]),
]
# arrows: (points, dashed, color)
ARROWS = [
    ([(365, 220), (365, 250)], False, GREY),     # Fed birth -> bond trade
    ([(365, 360), (430, 420)], False, GREY),     # bond trade -> work
    ([(800, 310), (760, 420)], False, GREY),     # bank nursery -> work
    ([(430, 600), (365, 640)], False, GREY),     # work -> Fed home
    ([(780, 600), (845, 640)], False, GREY),     # work -> bank home
    ([(140, 715), (95, 715), (95, 305), (140, 305)], True, PURPLE),   # ♻ buy a NEW bond (2a)
    ([(1080, 715), (1110, 715), (1110, 480)], True, PURPLE),  # loan money: poof, gone
]
# label: (text, rect x, y — bg rect is 140x30, text sits inside)
LOOPLABELS = [("♻ REINVEST", 15, 495)]
# bank money doesn't recycle — the repaid $100 just vanishes
POOF = ("Poof,\ngone! 💸", 1040, 415)
FOOTER = ("Gone 💸 — but not wasted: while it lived, every $100 was traded into "
          "real things. Money comes and goes; what it builds stays.")
SOURCE = "source: https://starsandbears.com/economy/industries_0712/"

_B62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


# ---------------------------------------------------------------- Excalidraw
def _base(kind_type, i, x, y, w, h, **extra):
    e = {"id": "full%02d" % i, "type": kind_type, "x": x, "y": y,
         "width": w, "height": h, "angle": 0, "strokeColor": INK,
         "backgroundColor": "transparent", "fillStyle": "solid",
         "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1,
         "opacity": 100, "groupIds": [], "frameId": None,
         "index": "a" + _B62[i // 62] + _B62[i % 62],
         "roundness": None, "seed": random.randint(1, 2 ** 31),
         "version": 1, "versionNonce": random.randint(1, 2 ** 31),
         "isDeleted": False, "boundElements": [], "updated": 1,
         "link": None, "locked": False}
    e.update(extra)
    return e


def _txt(i, x, y, s, size, color, bg="transparent"):
    lines = s.split("\n")
    width = max(len(l) for l in lines) * size * 0.55
    return _base("text", i, x, y, width, size * 1.25 * len(lines),
                 strokeColor=color, backgroundColor=bg, fontSize=size,
                 fontFamily=5, textAlign="left", verticalAlign="top",
                 text=s, originalText=s, lineHeight=1.25, autoResize=True,
                 containerId=None)


def build_excalidraw():
    els, i = [], 0
    els.append(_txt(i, 140, 20, TITLE, 36, INK)); i += 1
    els.append(_txt(i, 140, 84, SUBTITLE, 20, BLUE)); i += 1
    for kind, x, y, w, h, title, body in BOXES:
        fill, stroke, tcol = PAL[kind]
        els.append(_base("rectangle", i, x, y, w, h, strokeColor=stroke,
                         backgroundColor=fill, roundness={"type": 3},
                         opacity=60 if kind == "bankborn" else 100)); i += 1
        els.append(_txt(i, x + 20, y + 14, title, 20, tcol)); i += 1
        els.append(_txt(i, x + 20, y + 48, "\n".join(body), 18, INK)); i += 1
    for pts, dashed, color in ARROWS:
        (x0, y0) = pts[0]
        rel = [[px - x0, py - y0] for (px, py) in pts]
        xs = [p[0] for p in rel]; ys = [p[1] for p in rel]
        els.append(_base("arrow", i, x0, y0,
                         max(xs) - min(xs), max(ys) - min(ys),
                         strokeColor=color, strokeWidth=2,
                         strokeStyle="dashed" if dashed else "solid",
                         points=rel, startArrowhead=None,
                         endArrowhead="arrow", startBinding=None,
                         endBinding=None, lastCommittedPoint=None)); i += 1
    for text, x, y in LOOPLABELS:
        els.append(_txt(i, x + 8, y + 4, text, 19, BLUE, bg="#b2f2bb")); i += 1
    els.append(_txt(i, POOF[1], POOF[2], POOF[0], 20, PURPLE)); i += 1
    els.append(_txt(i, 60, 812, FOOTER, 16, GREY)); i += 1
    els.append(_txt(i, 60, 848, SOURCE, 20, BLUE, bg="#b2f2bb")); i += 1
    doc = {"type": "excalidraw", "version": 2,
           "source": "https://excalidraw.com", "elements": els,
           "appState": {"gridSize": 20, "gridStep": 5,
                        "gridModeEnabled": False,
                        "viewBackgroundColor": "#ffffff",
                        "lockedMultiSelections": {}},
           "files": {}}
    out = os.path.join(HERE, "money-lifecycle-full.excalidraw")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    return out, len(els)


# ----------------------------------------------------------------------- SVG
def build_svg():
    p = []
    for kind, x, y, w, h, title, body in BOXES:
        fill, stroke, tcol = PAL[kind]
        op = ' fill-opacity="0.6"' if kind == "bankborn" else ""
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" '
                 f'ry="14" fill="{fill}"{op} stroke="{stroke}" '
                 f'stroke-width="2.5"/>')
        p.append(f'<text x="{x+20}" y="{y+34}" font-size="20" '
                 f'fill="{tcol}">{escape(title)}</text>')
        for j, line in enumerate(body):
            p.append(f'<text x="{x+20}" y="{y+66+j*24}" font-size="18" '
                     f'fill="{INK}">{escape(line)}</text>')
    for pts, dashed, color in ARROWS:
        da = ' stroke-dasharray="7 6"' if dashed else ""
        mk = "ahp" if color == PURPLE else "ah"
        d = "M " + " L ".join(f"{x} {y}" for (x, y) in pts)
        p.append(f'<path d="{d}" fill="none" stroke="{color}" '
                 f'stroke-width="2.5"{da} marker-end="url(#{mk})"/>')
    for text, x, y in LOOPLABELS:
        p.append(f'<rect x="{x}" y="{y}" width="140" height="30" rx="6" '
                 f'fill="#b2f2bb"/>')
        p.append(f'<text x="{x+8}" y="{y+22}" font-size="19" '
                 f'fill="{BLUE}">{escape(text)}</text>')
    for j, line in enumerate(POOF[0].split("\n")):
        p.append(f'<text x="{POOF[1]}" y="{POOF[2]+20+j*26}" font-size="20" '
                 f'fill="{PURPLE}">{escape(line)}</text>')
    head = (f'<text x="140" y="56" font-size="36" '
            f'fill="{INK}">{escape(TITLE)}</text>'
            f'<text x="140" y="104" font-size="20" fill="{BLUE}">'
            f'{escape(SUBTITLE)}</text>')
    cap = (f'<text x="60" y="828" font-size="16" fill="{GREY}">'
           f'{escape(FOOTER)}</text>'
           f'<rect x="52" y="846" width="560" height="30" rx="6" '
           f'fill="#b2f2bb"/>'
           f'<text x="60" y="867" font-size="19" fill="{BLUE}">'
           f'{escape(SOURCE)}</text>')
    with open(FONT_FILE, "rb") as f:
        font_b64 = base64.b64encode(f.read()).decode("ascii")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="100%" style="height:auto;max-width:{W}px;display:block;'
           f'margin:auto" font-family="Excalifont, Xiaolai, sans-serif">'
           f'<defs>'
           f'<style>@font-face {{ font-family: Excalifont; '
           f'src: url(data:font/woff2;base64,{font_b64}); }}</style>'
           f'<marker id="ah" markerWidth="9" markerHeight="9" refX="6.5" '
           f'refY="3" orient="auto" markerUnits="strokeWidth">'
           f'<path d="M0,0 L7,3 L0,6 Z" fill="{GREY}"/></marker>'
           f'<marker id="ahp" markerWidth="9" markerHeight="9" refX="6.5" '
           f'refY="3" orient="auto" markerUnits="strokeWidth">'
           f'<path d="M0,0 L7,3 L0,6 Z" fill="{PURPLE}"/></marker>'
           f'</defs>'
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>'
           f'{head}{"".join(p)}{cap}</svg>')
    out = os.path.join(HERE, "money-lifecycle-full.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    return out, len(svg)


if __name__ == "__main__":
    ex, n = build_excalidraw()
    sv, b = build_svg()
    print("wrote", ex, "|", n, "elements")
    print("wrote", sv, "|", b, "bytes")
