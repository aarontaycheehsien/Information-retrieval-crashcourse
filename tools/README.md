# Tooling

## Canvas-style annotation helper

Run `tools\start-annotation-editor.cmd` from Windows Explorer, Command Prompt, or PowerShell. It starts a server bound only to `127.0.0.1`, prints a tokenized editor URL, and serves this repository. Keep that terminal open and use the printed URL for Claude proposal controls. Opening the HTML file directly still supports comments, browser storage, sidecar import/export, and Codex copy/import, but not the Claude button.

The full-featured flow is:

1. Open the repository with **Open Folder**, select text in one supported block, and choose **Comment** (or press `Ctrl+Alt+M`).
2. Use **Run Claude**, or **Copy for Codex** and paste returned JSON through **Import proposal**. When Codex discovers the page's WebMCP tools, it can list annotations, read bounded context, and submit a proposal directly.
3. Review each proposal. Only **Accept** changes document text; dismissing, retrying, resolving, or deleting does not apply proposal text.

Annotations are stored as `<document-name>.annotations.json` beside the document when a writable folder handle is available. Otherwise they remain in browser storage until exported. Sidecars are ignored by Git by default.

The helper keeps jobs in memory, gives Claude no tools or filesystem access, and requests a strict proposal schema. Stop it with `Ctrl+C`. Automated checks use `node --test tools/annotation-agent-server.test.mjs` and a mock process, so they do not consume a Claude run.

`search-textbook.html` is the **source of truth**. Edit it directly. Nothing
generates it, and nothing overwrites your prose.

Two maintenance passes keep the machine-owned parts consistent. Both are
idempotent — safe to run any time, and they report "no changes needed" when
there is nothing to do.

## After editing

```bash
python tools/maintain.py
python tools/renumber_footnotes.py
```

### `maintain.py`

Rewrites, in place:

- **Table and figure numbers.** Derived from each chapter's own eyebrow
  (`Chapter 4` → `Table 4.1`, `Table 4.2`, …). To renumber a chapter, edit the
  eyebrow and re-run — the assets follow.
- **Appendix letters.** Derived from the order the appendices appear in, in both
  the eyebrow and the asset prefixes. Reorder them and the letters follow.
- **Both tables of contents.** Rebuilt from the actual headings, so a new
  chapter or section appears automatically. Sections nested inside a figure,
  aside or `<details>` are skipped, as are group-divider headings.
- **Asset anchors.** Each table label and figure label gets an `id` derived from
  the number just assigned — `tbl-4-1`, `fig-3-4` — so any asset can be linked
  to directly.
- **The Figures and tables index.** The two lists in the `#figures-and-tables`
  back-matter section are rebuilt from the assets themselves, in document order.
  Figure entries take their text from the figure's `<p class="figure-title">`;
  table entries take the first sentence after the em dash. The index therefore
  cannot disagree with the numbers in the text.

Then it reports what it cannot fix and exits non-zero:

- a table or figure with no `Table n.n` / `Figure n.n` label
- a table label that is a bare number with no caption sentence after the dash
- a figure with no `<p class="figure-title">` for the index to quote
- duplicate `id` attributes
- broken internal links
- **stale cross-references** — a link whose text names a chapter, appendix,
  figure or table that is not what the link points at. A link can stay valid
  and still lie: renumber a chapter, reorder two sections or move a table, and
  every href still resolves while the number in the prose now names something
  else. The broken-link check cannot see this, because the anchors are slugs
  and the numbers are prose.

  Checked: `Chapter 7`, `Chapters 10 to 12`, `Appendix D`, a bare number used
  as chapter link text (the Preface currency warning links `3`, `7`, `8`, `9`
  that way), and `Figure 6.2` / `Table 8.1`. A link whose text is exactly its
  target's own heading is exempt, so Appendix F's section *Applying Chapter 12
  to active learning* is not read as a claim about Chapter 12.

  Only *linked* mentions can be checked — currently 50 of the book's 91
  `Chapter N` mentions, and all 87 figure and table references. The other 41
  are plain prose with no anchor to verify against, so a renumbering still
  needs a read-through for those.

**Caption text lives in the HTML**, not in the tool. `maintain.py` only owns the
number prefix; everything after the em dash is yours.

### `renumber_footnotes.py`

Reads the superscript refs in document order and rewrites the numbers, the
`<li>` order in the footnotes list, and each backref's "Jump back to footnote N"
title so all three agree. Run it after moving or adding a footnote.

## Conventions the tools rely on

Keep these shapes when hand-editing, or the passes will not find the pieces:

| Thing | Markup |
|---|---|
| Chapter | `<section class="chapter" id="sec-KEY">` with `<p class="chapter-eyebrow">Chapter N</p>` then `<h2 id="KEY">` |
| Appendix | `<section class="chapter appendix" id="app-X">` with an `Appendix X` eyebrow |
| Front matter | Three eyebrows are recognised besides `Chapter N`: `Preface` numbers its assets `P.n`, `Introduction` numbers them `0.n`. Any other eyebrow is reported as an error rather than guessed at |
| Table label | `<p class="asset-label">Table 4.1 — caption sentence.</p>` immediately before the `.table-wrap` |
| Figure label | `<span class="asset-label-inline">Figure 4.1</span>` as the first child of the `<figcaption>` |
| Figure title | `<p class="figure-title" id="SLUG-title">` as the first child of the `<figure>`. Not a heading — figure titles must stay out of the document's heading outline |
| Asset index | `<ol id="figure-index">` and `<ol id="table-index">`, emptied and refilled on every run. Do not hand-edit their contents |
| Back-matter section | `<section class="chapter backsection">` with an `<h2 id="…">`. Gets a TOC row, no sub-entries, and no asset numbering |
| Pinned TOC links | `<ul class="toc-pinned">` sits *outside* `<ol id="toc-list">`, which is why it survives the rebuild. Both TOCs carry a copy |
| Chapter reading time | `<p class="chapter-meta">` immediately after the eyebrow; the page's own script moves it into the chapter-head row |

The `data-ch` attribute on a TOC chapter row must match its section id minus the
`sec-` prefix; `maintain.py` writes this for you.

Two things the page does at runtime rather than in the markup, so nothing needs
maintaining by hand: the **Copy link** control on every chapter heading, and the
first-use **term marks**, whose definitions are read out of the `#glossary`
definition list. To add a term mark, add the term to the glossary and, if it is
unambiguous enough to match safely in prose, to the `MARKED` list in the page
script.

## Historical edition

Until August 2026 the textbook was generated from
`how-search-decides-what-you-see.html`. That build pipeline has been removed;
its history remains available in Git. The HTML maintenance passes documented
above are the only current authoring tools.

The earlier single-flow article has been retired. Its content can be recovered
from Git history, while `how-search-decides-what-you-see.html` is retained only
as a redirect to the textbook.
