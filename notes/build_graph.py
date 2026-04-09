#!/usr/bin/env python3
"""
Walk the notes vault, parse frontmatter + [[wikilinks]] from each concept .md file,
and emit graph.json for the Cytoscape viewer.

Edge types:
  - "parent"  : taxonomy edge from child -> parent (frontmatter `parents:`)
  - "related" : association edge (frontmatter `related:` + body wikilinks)

Run from repo root or from inside notes/:
    python3 notes/build_graph.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

NOTES_DIR = Path(__file__).resolve().parent
OUTPUT = NOTES_DIR / "graph.json"

# Files to skip when walking the notes vault
SKIP_NAMES = {"_template.md", "README.md", "index.md"}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")


def parse_file(path: Path):
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        print(f"  ! skipping (no frontmatter): {path}", file=sys.stderr)
        return None
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"  ! YAML error in {path}: {e}", file=sys.stderr)
        return None
    body = m.group(2)

    slug = meta.get("slug") or path.stem
    wikilinks = {w.strip() for w in WIKILINK_RE.findall(body)}

    return {
        "slug": slug,
        "title": meta.get("title", slug),
        "category": meta.get("category", path.parent.name),
        "aliases": meta.get("aliases") or [],
        "parents": meta.get("parents") or [],
        "related": meta.get("related") or [],
        "level": meta.get("level", "intermediate"),
        "status": meta.get("status", "stub"),
        "file": str(path.relative_to(NOTES_DIR)).replace("\\", "/"),
        "wikilinks": sorted(wikilinks),
    }


def build_graph():
    concepts = []
    for md in sorted(NOTES_DIR.rglob("*.md")):
        if md.name in SKIP_NAMES:
            continue
        # Skip top-level notes files (only walk category subfolders)
        if md.parent == NOTES_DIR:
            continue
        parsed = parse_file(md)
        if parsed:
            concepts.append(parsed)

    by_slug = {c["slug"]: c for c in concepts}

    nodes = []
    for c in concepts:
        nodes.append(
            {
                "data": {
                    "id": c["slug"],
                    "label": c["title"],
                    "category": c["category"],
                    "level": c["level"],
                    "status": c["status"],
                    "file": c["file"],
                }
            }
        )

    edges = []
    seen = set()

    def add_edge(src, tgt, etype):
        if src == tgt:
            return
        if tgt not in by_slug:
            print(f"  ! {src}: {etype} target '{tgt}' not found", file=sys.stderr)
            return
        key = (src, tgt, etype)
        if key in seen:
            return
        seen.add(key)
        edges.append(
            {
                "data": {
                    "id": f"{src}__{etype}__{tgt}",
                    "source": src,
                    "target": tgt,
                    "type": etype,
                }
            }
        )

    for c in concepts:
        for p in c["parents"]:
            add_edge(c["slug"], p, "parent")
        for r in c["related"]:
            add_edge(c["slug"], r, "related")
        for w in c["wikilinks"]:
            # Skip if already declared explicitly
            if w in c["parents"] or w in c["related"]:
                continue
            add_edge(c["slug"], w, "related")

    graph = {
        "generated_from": "notes/",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "categories": sorted({n["data"]["category"] for n in nodes}),
        "nodes": nodes,
        "edges": edges,
    }

    OUTPUT.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(NOTES_DIR.parent)}: "
          f"{len(nodes)} nodes, {len(edges)} edges")


if __name__ == "__main__":
    build_graph()
