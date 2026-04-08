# BCI Notes

A markdown-based knowledge base for Brain-Computer Interface concepts,
rendered as an interactive 3D galaxy. Each concept is a star; edges between
stars are taxonomy or association relationships.

Live viewer: open `vault/index.html` (served via any static HTTP server,
not `file://`, because it fetches `graph.json` and the markdown files).

```
python3 -m http.server 8000
# then visit http://localhost:8000/vault/
```

---

## How the taxonomy is organized

It uses an **action-based taxonomy**: top-level categories are the
operations a BCI system performs, not the kinds of things involved. This
makes the structure mirror the actual BCI pipeline (sense → clean →
decode → act) instead of fragmenting concepts by their physical type.

The six categories are arranged along the visible-light spectrum from
input (pink) to output (violet):

| Category    | Color  | What lives here                                  |
|-------------|--------|--------------------------------------------------|
| `sense`     | pink   | Acquire signals from the brain                   |
| `elicit`    | orange | Paradigms that evoke target brain responses      |
| `denoise`   | yellow | Remove artifacts and interference                |
| `decode`    | green  | Extract intent or sources from cleaned signals   |
| `stimulate` | blue   | Modulate or write to the brain                   |
| `apply`     | violet | End-user systems and outputs                     |

Each category is a folder. A file's category is determined by — and must
match — the folder it lives in.

### Two kinds of edges in the graph

- **Parent edges** (`parents:` in frontmatter) — taxonomy links to broader
  concepts. Rendered as solid blue arrows in the viewer. Example: `p300`
  has `parents: [erp]` because P300 is a kind of ERP.
- **Related edges** (`related:` in frontmatter, plus any `[[wikilinks]]`
  in the body) — peer associations. Rendered as faint dotted lines.
  Example: `opm-meg` is related to `squid-meg` because they're alternative
  ways to do MEG.

The viewer's "Tree only" toggle hides related edges so you can see just
the strict taxonomy.

---

## Anatomy of a concept file

A concept is a single markdown file with YAML frontmatter. Filename is
the slug followed by `.md` (kebab-case). Example:

```markdown
---
title: P300
slug: p300
category: elicit
aliases: [P3, P300 wave]
parents: [erp]
related: [eeg, oddball-paradigm, bci-speller]
level: intermediate
status: draft
---

# P300

The P300 is a positive deflection in the [[eeg]] occurring roughly 300 ms
after a rare, task-relevant stimulus. ...

## How it works
...

## Strengths
...

## Limitations
...

## Comparison with N400
...

## See also
- [[oddball-paradigm]]
- [[bci-speller]]

## Sources
- [Wikipedia: P300 (neuroscience)](https://en.wikipedia.org/wiki/P300_(neuroscience))
- ...
```

### Frontmatter fields

| Field      | Required | Notes                                                          |
|------------|----------|----------------------------------------------------------------|
| `title`    | yes      | Display name shown on the node and at the top of the wiki page |
| `slug`     | yes      | Stable ID, kebab-case. Used in `[[wikilinks]]` and graph IDs   |
| `category` | yes      | Must match the parent folder name (one of the six actions)     |
| `aliases`  | no       | Other names; informational only, does not affect the graph     |
| `parents`  | no       | Slugs of broader concepts. Creates **taxonomy** edges          |
| `related`  | no       | Slugs of peer concepts. Creates **association** edges          |
| `level`    | no       | `beginner` / `intermediate` / `advanced`. Shown as a pill      |
| `status`   | no       | `stub` / `draft` / `complete`. Shown as a pill                 |

### Body conventions

The body is plain markdown. Two conventions worth following:

1. Use `[[wikilinks]]` freely for cross-references in prose. The build
   script extracts them and adds them as related edges automatically, so
   you usually don't need to repeat them in `related:`.
2. Use the standard section structure when describing a technique:
   *(intro paragraph)*, `## How it works`, `## Strengths`, `## Limitations`,
   `## Comparison with X`, `## See also`, `## Sources`. Consistency makes
   the vault easier to skim.

### Sources section

Every concept page should end with a `## Sources` section listing the
authoritative references the content is grounded in. Format as a bulleted
list of links: Wikipedia first for general claims, then primary literature
(PubMed/PMC, Nature, NeuroImage, etc.), then established lab websites
or manufacturer documentation.

```markdown
## Sources
- [Wikipedia: Magnetoencephalography](https://en.wikipedia.org/wiki/Magnetoencephalography)
- [Boto et al. 2018, Nature](https://www.nature.com/articles/nature26147)
```

---

## Adding a new concept node

The minimal workflow:

1. **Pick a slug** — kebab-case, descriptive, unique. Example: `csp` for
   Common Spatial Patterns. Check no existing file has this slug.

2. **Pick a category** — one of `sense`, `elicit`, `denoise`, `decode`,
   `stimulate`, `apply`. The category is the folder you'll put the file
   in.

3. **Copy the template:**

   ```bash
   cp vault/_template.md vault/decode/csp.md
   ```

4. **Fill in the frontmatter** — title, slug, category, parents, related.
   Keep `parents:` for true "is-a" relationships only. Use `related:` (or
   inline `[[wikilinks]]`) for everything else.

5. **Write the body** — at minimum a one-paragraph definition. Aim for
   the standard sections (How it works / Strengths / Limitations /
   Comparison / See also / Sources). 300–700 words is a reasonable target.

6. **Cross-link from neighbors.** When you add a new node, also edit the
   nodes it relates to and add the new slug to *their* `related:` lists
   or body wikilinks. This makes the new star visibly connected in the
   graph instead of floating alone.

7. **Rebuild the graph:**

   ```bash
   python3 vault/build_graph.py
   ```

   You should see something like `Wrote vault/graph.json: N nodes, M edges`.
   The script also warns about wikilinks pointing to non-existent slugs —
   fix typos before committing.

8. **Reload the viewer** — refresh `http://localhost:8000/vault/` and
   the new star should appear in its category color.

That's it. Commit and push; CI runs `build_graph.py` automatically on
deploy (see `.github/workflows/static.yml`), so you don't *have* to commit
the regenerated `graph.json`, but doing so keeps the local viewer working
without requiring a build step.

### Adding a new category

The six action categories are intended to be stable. If you really need a
new one:

1. Create the folder under `vault/`.
2. Add it to `CATEGORY_ORDER` and `CATEGORY_COLORS` in `vault/index.html`
   (search for those constants near the top of the inline `<script>`).
3. Update this README's category table.
4. Move/create files into the new folder and set their `category:` field.

---

## Editing in Obsidian (recommended)

The vault is fully Obsidian-compatible. Point Obsidian at the `vault/`
folder and you get autocomplete for `[[wikilinks]]`, the standard graph
view, backlinks, and the local-graph sidebar. Use Obsidian for *editing*
content, then use the custom 3D viewer for *exploring* and *publishing*.

The custom viewer is intentionally not a substitute for an editor — it's
read-only and optimized for the cosmic aesthetic, not for content
authoring.

---

## How the build works

`build_graph.py` walks every `.md` file in the category subfolders
(skipping `_template.md` and `README.md`), parses YAML frontmatter,
extracts `[[wikilinks]]` from the body, and emits `graph.json` containing:

- A `nodes` array — one entry per concept, with id, label, category, etc.
- An `edges` array — `parent` edges from `parents:`, plus `related` edges
  from `related:` and from body wikilinks (deduplicated).

The viewer (`vault/index.html`) loads `graph.json` into
[3d-force-graph](https://github.com/vasturiano/3d-force-graph), renders
each node as a glowing sprite colored by category, and renders the
markdown wiki page in the side panel when you click a star.

### Quality checks the build script does

- Warns if a `[[wikilink]]` or `parents:`/`related:` slug doesn't match
  any existing concept (broken reference).
- Skips files without YAML frontmatter.
- Deduplicates edges so a concept declared in both `related:` and a
  wikilink doesn't get a double edge.

---

## Conventions to keep the vault healthy

- **One concept per file.** If a page is growing past ~1000 words and
  developing distinct sub-topics, split it.
- **Slugs are forever.** Renaming a slug breaks every wikilink that
  points to it. Pick carefully; if you must rename, grep the vault for
  the old slug and update all references.
- **Cite everything.** Every claim that includes a number, a date, or
  an attribution should map to a source in the `## Sources` section.
- **Wikilinks over plain mentions.** When you mention another concept,
  use `[[its-slug]]` so the graph captures the connection automatically.
- **Frontmatter must round-trip.** Don't put complex YAML in frontmatter
  fields the build script doesn't expect — stick to the schema in the
  template.
