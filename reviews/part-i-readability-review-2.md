# Part I (Chapters 1–4): second readability review

Reviewed 9 November 2026 against commit `1268e25` on `more-readable` (version
1.2.1, with the unreleased grep and exact-match/best-match additions). Findings
1–10 below **have been applied** to `search-textbook.html`: 3–10 first, then 1 and
2 in a follow-up commit. Finding 11, the content gap and the accessibility note
are **recorded only** and remain open.

The September pass (`part-i-readability-review.md`) fixed placement and
duplication. This pass found three things it could not have: figures that have
drifted from the edited text, sequencing damage from the October additions, and
an overloaded Chapter 1. Product claims were not checked against external
sources.

## Applied in the follow-up: the two figures

### 1. Figure 3.3 carries product claims found nowhere else

The raster infographic has Europe PMC and Web of Science panels. Neither product's
ranking is described in the prose or the evidence register ("Europe PMC" occurs
nowhere in the book's text). Its PubMed panel repeats the paragraph beneath it
almost word for word. Either source and register the two extra panels, or redraw
the figure with PubMed, Scopus and CDI only.

**Applied:** redrawn as an HTML figure from the book's existing `worked-figure`
components, with PubMed, Scopus and Primo CDI only. Each card restates what the
section's prose and evidence register already say; two lines separate what is
established from what is not. The Europe PMC and Web of Science panels were
dropped, not sourced: restoring either needs a cited source and a register entry.
The figure title, its anchor and its evidence-register block are unchanged.

### 2. Figure 4.5 contradicts Chapter 4

- One "query processing" band holds tokenisation, spelling correction and synonym
  expansion, although the chapter separates analysis from transformation.
- "BM25 and other models typically operate after candidate generation" conflicts
  with direct BM25 retrieval.
- Document-length normalisation is filed under "additional signals", although
  Chapter 3 teaches it as one of BM25's four questions.
- "Lemmatization" is a US spelling; the minimum-match example is two of four
  terms where the chapter uses two of three.

The caption carries three disclaimers to compensate. Redraw it in HTML like
Figures 4.1–4.4, or cut it.

**Applied:** redrawn as an HTML figure in four bands using the chapter's own
terms: what retrieval receives (understanding and transformation, then
analysis), admission (all, some or any terms), ranking (BM25's evidence, further
lexical evidence, and signals that are not lexical matches) and the output
boundary. The caption drops the disclaimer about illustrative field weights,
which the figure no longer shows. Title and anchor are unchanged.

Both figures are now readable by screen readers, searchable and translatable.
The two PNG files remain in `images/` but nothing in the book references them.
One CSS rule was added (`.worked-kicker.worked-band`) for spacing between bands.

## Open: not applied

### 11. The Part I checklist

Five of the six distinctions on the Part I divider cannot be checked in Part I.
The September review declined to change this. At minimum, align its order and
wording with the Part II panel, which lists the same ideas as five equated errors
in a different order.

### Content gap: the reader's own operators

Chapter 2 never explains how truncation, phrase or proximity operators execute
over the index, yet its first self-check tests truncation. Two short paragraphs
would close this: wildcard expansion against the term dictionary, and positional
postings (Manning, Raghavan and Schütze, 2008, *Introduction to Information
Retrieval*, sections 3.2 and 2.4).

### Accessibility

Figures 2.1, 3.2 and 3.5 are raster infographics whose alt text only repeats
the title (3.3 and 4.5 were too, before the follow-up). Their embedded text cannot be read by a screen reader,
searched or translated. They render at about 40 per cent of native size with no
way to enlarge them.

### Noticed in passing

The full-text-search terminology panel in Chapter 2 sits inside the preceding
pull-quote's `<blockquote>`. Not changed here.

## Applied

### 3. Dangling references in the Part I landing

`#one-category-error-resolved-and-one-still-ahead`. "The one collapse of this
kind" had no antecedent: "collapse" is not used as a noun before Part III. It now
reads "the one confusion of the six listed at the start of Part I", matching the
Preface and the Part II panel. "Two of its instances" became "Two of them". The
60-word sentence was split in two. The final sentence no longer uses
"vocabulary-aligned vectors" and "bi-encoders" before Part II defines them; it
says that lexical term weights such as BM25's can be held in vectors and points
to Chapter 8.

### 4. Forward references in Chapter 2

- The exact-match panel cited grep's `-F` about 1,000 words before grep was
  introduced. The contrast between literal-string matching and exact-match
  retrieval now sits in the grep panel, linking back.
- "Soft conjunction" occurred once in the book and was never defined. The
  full-text-search panel now says the engine may "require only some of the query
  terms".
- "OpenAlex, Semantic Scholar, Ex Libris CDI" gained its "and".

### 5. "Delulu" glossed

At its first use in the body: "internet slang for 'delusional'".

### 6. Chapter 2: grep panel and the repeated worked example

The grep panel split Table 2.3 from Table 2.4. It now sits in *How Boolean search
uses an inverted index*, straight after "does not normally reread every record",
as the scanning baseline the index avoids. Table 2.3 stays where it was, so no
table is renumbered; the panel shows `records.txt` as its own four-line listing.

*Boolean treats postings as sets* repeated Figure 2.3's `delulu AND interview`
example under its own heading. The heading and the repeated listing were removed
and the two sentences on `OR`, `NOT` and set processing now follow the figure.
The anchor `#boolean-treats-postings-as-sets` is kept on that paragraph. The
section signpost says "four sections" accordingly.

### 7. Chapter 3 reaches BM25 sooner

- "BM25 is a standard way of turning those intuitions into a score" now follows
  the paragraph that states the intuitions, instead of sitting two paragraphs
  later.
- The best-match terminology panel moved from before *An introduction to BM25*
  to the end of that section, after the four questions it depends on.
- One of three introductory definitions of BM25 was removed ("BM25 is one
  standard lexical answer to the ranking problem").

### 8. Chapter 1: the two-by-two

- New heading *Two axes: output format and retrieval iteration*
  (`#two-axes-output-format-and-retrieval-iteration`), so the two-by-two no
  longer sits unannounced under *Two machines, one product*.
- The axes were explained three times in about 200 words. They are now explained
  once, before the figure.
- "Quick answer" and "deep research" were used before Figure 1.3 defined them.
  Those two sentences moved below the figure; footnotes 2 and 3 swapped numbers
  as a result.
- One new sentence states that the six-stage strip maps the retrieval machine
  only and has no stage for generation.

Chapter 1's section order is otherwise unchanged.

### 9. Chapter 4 repetition

- The four jobs are listed in the order they run (understanding, transformation,
  analysis, execution rules), matching Figure 4.4 and the stage strip. The
  chapter opening lists them in the same order.
- The paragraph restating understanding versus transformation straight after the
  list was removed; its example recurs two paragraphs later.
- The caveat that an interface cannot identify the architecture appeared seven
  times in the chapter's last 900 words. Two body-text instances were removed.
  The Figure 4.3 caption, the two verdicts, the summary and the self-check keep
  theirs.

### 10. Table 1.2 and the paragraph beneath it

- Puzzle 2's open question was "How does Google Scholar decide which tiny
  fraction of the reported results appears first?", which Chapter 4 never
  answers. It now asks what the reported count and the display limit each
  measure, and how many reported matches were ever scored, which is what the
  puzzle text asks and what Chapter 4 addresses.
- "Four chapters of ordinary lexical retrieval" became "Three".
- Puzzle 3 "needs mechanisms that Part II builds, and it is taken up in
  Chapter 7", in line with Table 1.2 and Chapter 4.

## What was checked

- Every replacement and block move was an exact match asserted to occur once.
- `tools/maintain.py`: no problems found; second run "no changes needed".
- `tools/renumber_footnotes.py`: 56 footnotes, renumbered once, then in order.
- `--check` passes for the product-claims, glossary, digest and vendor
  questionnaire builders; `test-product-claims.py`, `test-glossary-hub.py`,
  `test-digest.py` and `test-vendor-questionnaire.py` pass. The Node browser
  checks were not run.
- One `id` added (the new heading), none removed.
- `data/product-claims.json`: three excerpts updated for the added "and".
  `data/digest-selections.json`: the result-screen panel's omit list updated for
  the reworded and removed paragraphs. `read-this-first.html` regenerated.
- Rendered page inspected in headless Chromium for the new Chapter 1 heading, the
  relocated grep panel and the relocated best-match panel. The only console error
  was a blocked CDN request in the review environment.
- Visible words, excluding evidence registers: Chapter 1 4,530 → 4,578;
  Chapter 2 3,265 → 3,312; Chapter 3 2,656 → 2,649; Chapter 4 3,064 → 2,991.
  No reading-time label changes.
- The narrated-video sources under `tools/chapter-*-investigations/` are dated
  snapshots and were not changed.
