# Tooling

## Product evidence and currency

`data/product-claims.json` maintains the claim register. The HTML remains the
source of truth for chapter prose; only `BEGIN/END PRODUCT CLAIMS` blocks are
generated. `product_claims.py` shares validation, date rules and renderers between:

```powershell
python tools/build-product-claims.py
python tools/maintain.py
python tools/build-product-claims.py --check
python tools/check-product-claims.py --as-of 2026-09-19
python tools/test-product-claims.py
node tools/check-product-claims.mjs
```

All Python commands use the standard library. Set `CLAIMS_NODE_MODULES` to the
bundled runtime's `node_modules` directory for the browser check. It serves the
repository on a temporary loopback port, blocks external browser requests, and
saves desktop, mobile, print-media and no-JavaScript screenshots in the ignored
`outputs/product-claims/` directory. Inspect those images before release.

### Data and editorial workflow

- Stable `id` values identify assertions, not chapter numbers. Repeated instances
  share an ID. Different product modes and materially different historical
  architectures need separate records. Preserve old IDs when correcting wording.
- `evidence_date` means when the described evidence applies, not a promise of
  current behaviour or necessarily a publication date. `evidence_basis` is
  documentation, observation, screenshot or inference. An inference must retain
  its alternatives and limits. URLs and available source locators are recorded
  under `evidence`; an absent source requires an explicit `evidence_gap`.
- Dates accept `YYYY`, `YYYY-MM`, `YYYY-MM-DD` or JSON `null`. Never invent a day
  for a month-only date, infer a check date from publication, or replace an
  unknown with the migration/build date.
- Append chronological `reviews`, each with `checked_on`, `finding`, explanatory
  `notes` and zero-based `evidence_indices` identifying the evidence actually
  used. A supported finding requires evidence. The allowed findings are
  `supported` (within the stated scope), `changed` and `not established`.
  Record what was inspected and what that inspection cannot establish.
- A changed/failed check does not erase earlier support. Inspect **every** linked
  location, including figure images, tables and captions. Correct the prose,
  explicitly retain an historical account, or add a separately scoped record.
  Append a supported review only when evidence supports the resulting assertion.
- `locations` pair an existing anchor with an exact normalised excerpt. Update
  these after an intentional source edit; validation rejects stale excerpts and
  missing anchors. Superscript footnote numbers are excluded from normalisation.
  Broad section anchors are sometimes shared; the excerpt identifies the actual
  passage. Automatic validation finds textual drift, not every semantic omission.
- `coverage` records chapter/appendix decisions and exclusions, including sections
  with no product claims. Review it whenever adding a product assertion. New main
  sections require a coverage decision. Research findings, generic mechanisms,
  fictional exercises and professional-methodology guidance are outside this
  product-specific inventory. The latter still needs separate currency review.
- `teaching_groups` preserve nine assignments, not nine total claims. Additional
  claims can remain outside those groups. Both reader views link to canonical IDs.

The initial inventory is a migration of the book's existing evidence, not a fresh
verification of linked pages or product behaviour. Recorded checks explicitly
identify themselves as inherited. Several assertions have no attached direct
source; these gaps remain visible rather than being filled by guesswork.

### Currency and reproducibility

The report is read-only. Without `--as-of`, it uses the local current date. It
separates overdue current-facing claims, unknown supporting-check dates,
changed/unresolved claims, historical examples and checks within the age window.
Categories may overlap. An evidence gap is unresolved even without a review.

Overdue means **more than 365 days** since the last supporting check. A later
failed attempt never refreshes that date. Partial dates use the first possible
day conservatively and label age approximate; an historical example is never
overdue just for being old. A recent check of a 2020 source does not establish
2026 behaviour. Historical evidence dates remain unchanged.

The generated HTML uses the explicit `currency_as_of` date in the JSON, visibly
labelled a static snapshot. Advance it intentionally before publication and
rebuild; doing so recalculates age, never inserts a review. Keeping the date in
data makes builds deterministic. The CLI can report any later date without
changing the published files. There is no scheduled monitor or external fetch.

Invalid data, missing local references, source drift and generated-content drift
fail checks; age warnings do not. After rebuilding, run the existing evaluation
kit and vendor-questionnaire checks too. The register links are kept outside
question bodies consumed by the questionnaire builder.

## Vendor questionnaire

`vendor-questionnaire.html` is generated from three maintained sources:

- Question wording and six group headings in `search-textbook.html`, identified
  by `vendor-q01`–`vendor-q19`, `vendor-e01`–`vendor-e04`, `vendor-g01`–`vendor-g07`,
  `vendor-group-1`–`vendor-group-6` and the intake paragraph `vendor-inputs`.
- `tools/fixtures/vendor-questionnaire.json`, the explicit mapping of groups,
  questions, related core answers and three declared narrative omissions. The
  omissions remove commentary after the intake prompt and Q15/Q16; they do not
  remove any requested vendor information.
- `tools/templates/vendor-questionnaire.html`, the page layout and print controls.

Do not edit the generated page by hand. Build and check with Python's standard
library, then inspect browser/print output with the bundled Node/Playwright runtime:

```powershell
python tools/build-vendor-questionnaire.py
python tools/test-vendor-questionnaire.py
node tools/check-vendor-questionnaire.mjs
```

Set `QUESTIONNAIRE_NODE_MODULES` to the bundled runtime's `node_modules` path
for the browser check. It serves only this repository on a temporary loopback
port and saves screenshots and four A4 print variants under the ignored
`outputs/vendor-questionnaire/` folder. These PDFs are QA intermediates, not
additional published downloads. Check their page images before release.

`python tools/build-vendor-questionnaire.py --check` detects generated-page drift.
The generator also rejects missing/duplicate anchors, unmapped source questions
and changed narrative boundaries so a source edit cannot silently drop a question.
The two optional sections are hidden by default. There is no response storage,
network request or scoring logic in the reader page.

## Local retrieval evaluation kit

`evaluation-kit.html` is the reader guide. Its two downloads are generated from
one layout and formula definition in `tools/build-evaluation-kit.mjs`, with the
controlled Figure 14.1 rankings, seed subset and five probe prompts in
`tools/fixtures/evaluation-kit.json`. Edit those sources, then regenerate both
workbooks together. Do not hand-edit the distributed XLSX files.

Use the bundled Node runtime and `@oai/artifact-tool` dependencies returned by
the workspace dependency loader. Set `EVALUATION_NODE_MODULES` to that runtime's
`node_modules` directory, then run:

```powershell
node tools/build-evaluation-kit.mjs
python tools/test-evaluation-kit.py
powershell -NoProfile -ExecutionPolicy Bypass -File tools/test-evaluation-kit.ps1
node tools/check-evaluation-guide.mjs
```

The builder stages XLSX files and worksheet previews in the ignored
`outputs/evaluation-kit/` directory and copies the two workbooks into
`downloads/`. The local dependency junction is also confined to that staging
directory. No runtime dependencies are needed by readers.

The Python check uses only the standard library. It checks saved values,
formula errors, table structure, links and the example against the book's actual
Figure 14.1. The PowerShell check requires desktop Excel and opens a disposable
copy in a separate hidden instance. It tests recalculation, short/empty runs,
missing judgements and seeds, invalid input, edits, table extension and
save/reopen. The browser check uses bundled Playwright with headless Edge,
checks the guide and downloads, and saves desktop/mobile previews for review.

The workbook holds two runs and fifty query slots. Records are an expandable
Excel table. Formula-owned columns are Records I–Q, Queries T–U and Comparison
A–Q; Comparison B4 is the editable shared cutoff. Capture counts are distinct
records at the recorded capture depth, not raw duplicate positions. Blank
judgements stay unjudged, and changing the cutoff cannot silently relabel an
incomplete capture as complete. The guide explains extension and rerun steps.

## Canvas-style annotation helper

Run `tools\start-annotation-editor.cmd` from Windows Explorer, Command Prompt, or PowerShell. It starts a server bound only to `127.0.0.1`, prints a tokenized editor URL, and serves this repository. Keep that terminal open and use the printed URL for Claude proposal controls. Opening the HTML file directly still supports comments, browser storage, sidecar import/export, and Codex copy/import, but not the Claude button.

The full-featured flow is:

1. Open the repository with **Open Folder**, select text in one supported block, and choose **Comment** (or press `Ctrl+Alt+M`).
2. Use **Run Claude**, or **Copy for Codex** and paste returned JSON through **Import proposal**. When Codex discovers the page's WebMCP tools, it can list annotations, read bounded context, and submit a proposal directly.
3. Review each proposal. Only **Accept** changes document text; dismissing, retrying, resolving, or deleting does not apply proposal text.

Annotations are stored as `<document-name>.annotations.json` beside the document when a writable folder handle is available. Otherwise they remain in browser storage until exported. Sidecars are ignored by Git by default.

The helper keeps jobs in memory, gives Claude no tools or filesystem access, and requests a strict proposal schema. Stop it with `Ctrl+C`. Automated checks use `node --test tools/annotation-agent-server.test.mjs` and a mock process, so they do not consume a Claude run.

`search-textbook.html` is the **source of truth for authored prose**. Edit it
directly. The product register additionally generates marked evidence blocks;
neither that builder nor the maintenance passes overwrite your prose.

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
  target's own heading is exempt, so Appendix F's section *Applying Chapter 15
  to active learning* is not read as a claim about Chapter 15.

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

### The two recurring example families

Worked examples come from two standing families, so a reader is not learning a
new collection every chapter. Each has a job, and they are not interchangeable:

- **`delulu`** (and occasionally `rizz`) — unfamiliar terminology and lexical
  stress tests. It runs from the Preface through Chapters 2–7, 9 and 13, and
  Appendix C's BM25 walkthrough. Use it where the point is analysis,
  tokenisation, out-of-vocabulary behaviour or a term the system may not know.
  Do not use it where relevance has to be judged against a real information
  need: its relevance judgements are too ambiguous to carry precision or
  recall examples. It may carry training labels the text explicitly
  stipulates. Chapters 6 and 9 use it that way: they state the assumed need
  and present the positive and the hard negative as labels rather than as
  facts about the passages.
- **The open-access citation advantage** — realistic academic searching. It is
  the question behind Puzzle 3, the worked need in Chapter 11's eight query
  objects, and the search used in Chapters 1 and 7. Use it where the point is
  what a real searcher is trying to find.

Where an example needs judged relevance, reuse the `AI academic libraries` need
already worked in Chapters 1 and 13 rather than inventing records. The book
sources its examples to systems that are named and dated; a fictional corpus
would cost that.

## Historical edition

Until August 2026 the textbook was generated from
`how-search-decides-what-you-see.html`. That build pipeline has been removed;
its history remains available in Git. The HTML maintenance passes documented
above are the only current authoring tools.

The earlier single-flow article has been retired. Its content can be recovered
from Git history, while `how-search-decides-what-you-see.html` is retained only
as a redirect to the textbook.

## Interactive lab checks

Run `node tools/test-labs.cjs` for scoring and existing lab examples, then
`node tools/test-vector-tour.cjs` for the vector lab’s prediction/reveal flow,
cutoff/filter ordering, sandbox challenges and complete shared-state reset.
The latter executes the page script with a small DOM fixture; it does not
replace a rendered-browser layout check.
