# Stars & Bears — authoring guide

Instructions for writing a new **note** (article). Every note reuses one shared
style template — **"The Pacific"** — established by the two reference
implementations. When building a note, copy their structure exactly rather than
inventing a new layout:

- `history/jefferson_0705/index.html`
- `science/artificial_womb/index.html`

Each note is a **single self-contained `index.html`** (inline `<style>` and
`<script>`, no shared stylesheet) living in a category folder — e.g.
`history/<slug>/`, `science/<slug>/`, `economy/<slug>/`. Decorative SVGs are
inline and `aria-hidden="true"`.

The landing page (`/index.html`, the whiteboard theme) is separate and does
**not** use this template; only the notes do.

## Design tokens (`:root`)

```
--ink:#1a1a1a; --paper:#fbfaf7; --muted:#6b6b6b; --line:#e3e0d8;
--accent:#b8472d;  /* terracotta — kickers, quote rule, active nav */
--accent2:#2d6a8e; /* blue — links & source citations */
--gold:#c08a2e; --green:#3d7a5a;
--serif:'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif; /* prose */
--sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif; /* labels & nav */
```

Warm paper, ink serif prose, sans for labels/navigation. Fluid type with
`clamp()`; no hard breakpoints for sizing.

## Header

Two parts, in this order:

1. **`.topbar`** — a slim bar with a serif `.home` link ("The Pacific") on the
   left and `.crumbs` breadcrumbs on the right (e.g. `All notes · History`).
2. **`header.hero`** — an uppercase sans `.kicker`, the serif `<h1>` title, and
   a serif `.lede` one-liner. Bottom border `3px double var(--line)`.

The topbar is repeated at the **bottom** as `.topbar.bottom` with back links
(`← The Pacific`, `More in <category> →`).

## The navigator (contents table)

`<nav class="sidenav" aria-label="Contents">` — the primary in-page wayfinding:

- **Wide screens:** `position:fixed`, vertically centered on the **left**,
  `width:214px`. Grouped links — `.toc-lead` (top-level), `.toc-group` +
  `.toc-head` (uppercase accent group headings), nested links indented.
- **≤1040px:** the *same markup* reflows to a sticky, blurred **horizontal
  strip** at the top (`position:sticky; display:flex; white-space:nowrap`) — no
  duplicate nav.
- **Scroll-spy:** the link for the section in view gets `.active`
  (`box-shadow:inset 3px 0 0 var(--accent)`), driven by the script.
- Section targets use `scroll-margin-top` so they clear the sticky nav.

## Layout — text on the right side

`.shell` is a two-column grid: **`grid-template-columns:214px minmax(0,1fr)`**,
centered with a max-width (~1240–1360px). The reading content goes in
**`.body-col { grid-column: 2 }`** — i.e. the article text sits in the **right**
column, beside the fixed left-hand navigator. (Prose itself is left-aligned /
justified; "right side" refers to this column placement.) Below 1040px the grid
collapses to a single column and the body spans full width.

## Footer

A rounded, bordered `<footer>` card holding **References** (numbered `ol.refs`
with `↩` back-links to each citation) and **Further sources** (`.reading`
grouped link lists). Followed by the bottom `.topbar.bottom` return bar.
Footnotes are `sup.fn` superscripts linking to the references; both ends use
`scroll-margin-top` and a `:target` highlight.

## Accessibility (required — match it exactly)

Every note ships the full layer:

- **Skip link** (`.skip`) as the first tab stop → the focusable content
  section (`tabindex="-1"`).
- **Accessibility toolbar** (`.a11y`, fixed bottom-right) with an `aria-expanded`
  toggle opening a `role="region"` panel:
  - **Read aloud** — Web Speech API narration that **underlines the current
    word** via the CSS Custom Highlight API (`::highlight(speech)`), auto-scrolls
    to keep it visible, marks the active block `.ar-active`, with
    play/pause/resume/stop + a speed control. Reads prose/headings; skips code.
  - **OpenDyslexic font** toggle — swaps `--serif`/`--sans`, widens spacing.
  - (artificial_womb also adds a **text-size** control via a `--fs` scale var.)
- **Persistence:** preferences are saved under the site-wide `localStorage`
  keys `sb-dyslexic` and `sb-rate`, so they carry across notes.
- **Graceful degradation:** if Web Speech or the Custom Highlight API is
  unavailable, controls disable or narration proceeds without the underline —
  never a broken state.
- `:focus-visible` outlines on all interactive elements; `prefers-reduced-motion`
  disables smooth-scroll/animation.
- **ARIA/semantics:** `nav aria-label`, `role="status" aria-live="polite"` for
  reader state, `aria-pressed` on toggles, `<caption>`/`<thead>`/`scope` on
  tables, proper heading order (one `h1`, then section `h2`, sub `h3`).
- Contrast meets WCAG AA (ink 15.9:1, accent 4.7:1, accent2 5.4:1 on paper).

There is a fuller, live reference of all of the above in
`the_pacific/style-guide/index.html`.

## After writing a note

**Append** a new entry to the end of the landing page's `POSTS` array in
`/index.html`; don't re-order the existing notes. Cards size to their own
content. The board is a 6-unit-wide grid. Optional per-note tweaks: `span` sets
card width in sixths of the row (default 2 = 1/3; 3 = 1/2, 4 = 2/3, 6 = full) so
a longer note grows width before height; `color:` sets the sticky-note colour
(`'yellow'|'blue'|'pink'|'green'|'purple'`) instead of the position-based default.

```js
{ cat:'hist'|'sci'|'tech'|'econ', url:'<category>/<slug>/index.html',
  title:'…', date:'Month D, YYYY', read:'N min', excerpt:'…',
  span:3, color:'purple' }
```

Link the `url` to the folder's **`index.html`** (not the bare directory, so it
resolves under `file://` too).
