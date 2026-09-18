# Part I (Chapters 1–4): readability review

Reviewed 18 September 2026 against commit `8c201f1` (version 1.2.1). The findings
below **have been applied** to `search-textbook.html`; line numbers refer to the
file as reviewed, before revision.

The brief was readability with the content held fixed: no claim removed or
softened, no example or citation dropped, and nothing cut that is not stated within
a few hundred words of where it was. The earlier readability pass
(`readability-plan.md`, applied 5 September) had already shortened Chapter 1's
relevance section and swept the absolutes, so nothing here re-does that work, and
Chapter 1's section order — reordered three times already — is untouched.

What remained was of two kinds. Six placement and duplication problems: a paragraph
sitting above its own heading, a panel interrupting the simplest explanation, a
terminology panel after the section's bridge, one point made three times in 400
words, two adjacent Chapter 4 sections giving the same three verdicts twice, and a
heading whose entire body was one boxed panel. And a bounded set of sentence-level
repairs: a few 40–60 word sentences, one grammatical slip, one sentence that
contradicted what the reader had just read, and thirteen links whose text
("Discussed later", "the advanced appendix", "Where it was left") did not say where
they went.

Constraints kept throughout: no `id`, heading, figure, table, footnote or
reading-time label changed; the exempt zones in `repetition-ledger.md` (self-checks,
chapter closes, glossary, footnotes, the exercise) are byte-identical; the two
example families and the ledger's claims A–E are as they were. One structural
change, flagged below (finding 6), removes an `<aside>` wrapper.

## Findings applied

### 1. Chapter 4's last two sections gave the same three verdicts twice

**Locations:** `#returning-to-the-opening-puzzles` (`1642`) and
`#one-category-error-resolved-and-one-still-ahead` (`1647`–`1658`).

The first section gives the scite, Google Scholar and Semantic Scholar verdicts.
The second restated all three within 500 words, then the chapter close stated them
a third time. The second section is also the densest stretch of Part I — seven
sentences over thirty words — and it is the landing the whole part builds to.

**Applied:** the first section is now the single home of the verdicts. In the
distinction-map panel, the Google Scholar paragraph keeps the two things only it
says — that Puzzle 2 settles into an observation rather than a named confusion, and
the general form of the three controls — and reduces the restated verdict to a
clause: "A reported count is an estimate of matches, and a display limit is a
display boundary rather than a scoring decision." "Where it was left" became "The
verdict above"; "Read the distinction" became "See *Lexical search does not have to
mean Boolean search*." The 58-word sentence on the two Part II distinctions is now
three sentences with the same words, and "the remaining five" now says what they
are five of: "the remaining five of the six distinctions listed at the start of
Part I", with a link to that panel.

### 2. Chapter 1's puzzles lead-in sat above its own heading

**Location:** `1243`, the paragraph "Most librarians understand Boolean searching…
Here are three searches — all real, all screenshotted below…", which was the last
block before `<h3 id="three-familiar-search-results-and-three-puzzles">` and so read
as the tail of the relevance section, after the *Seven terms* panel.

**Applied:** moved verbatim to directly after the heading. Nothing else moved.

### 3. Chapter 3 opened by making the same point three times

**Locations:** the `#bm25-ranking` orientation (`1443`) and
`#bm25-words-as-weighted-clues` (`1444`–`1447`).

"Relevance / Best Match is a label, not a method" appeared in the orientation's
third paragraph (with the PubMed links), again as the first section's "The label
tells us that records will be ordered, but not how", and a third time as the
blockquote "names an ordering, not a formula." The orientation was also five
paragraphs before the first heading, the longest in Part I.

**Applied:** the orientation paragraph moved down and merged with the section's
first paragraph, so the Scopus/Web of Science sort example, the PubMed Best Match
example and "ordered, but not how" are one paragraph, and the blockquote stays as
the single set-off statement. The orientation is four paragraphs. The top-*k*
paragraph was left alone as a deliberate preview of Chapter 7.

### 4. Chapter 2's *In practice* panel interrupted the simplest explanation

**Location:** `1293`–`1297`. The panel sat between "A Boolean system requires a
record to satisfy both conditions" and the AND / OR / NOT list, and ended "We will
discuss this in a later section."

**Applied:** moved to the end of the same section, immediately before "The
admission decision is now clear…", where it hands off to the analysis sections. Its
last sentence now names them: "The sections that follow trace that path, from
*Before the index: text becomes tokens* to *From analysed tokens to a term-first
map*." The reader meets the operators, the pull-quote and the expansion example
uninterrupted.

### 5. Chapter 2 ended bridge → terminology digression → summary → bridge

**Location:** `1433`–`1441`. The section's bridge to ranking ("What is missing is a
graded ranking rule") was followed by the seven-paragraph *Terminology* panel on
full-text search, then the chapter close, whose last line is the same bridge.

**Applied:** the bridge paragraph now follows the panel, so the section ends on it.
The panel's paragraphs 2–4 became one paragraph with every example kept (the DOI
and publication-year exact-value contrasts, the analysis-into-terms description);
PostgreSQL, the coverage-versus-capability confusion and "FTS does not identify a
query rule" are unchanged. Seven paragraphs became four.

### 6. A Chapter 4 heading whose whole body was one boxed panel

**Location:** `#early-google-non-boolean-did-not-mean-non-lexical` (`1605`). The
section was 72 words: a heading, then a single *common-confusion* aside labelled
"Historical counterexample", so heading and label said the same thing and a
two-sentence aside wore the styling of a key definition. Three inbound links target
the heading, so it stays.

**Applied (the one structural change):** the aside and its label were removed and
the text set as two plain paragraphs — the history, with footnotes 12 and 13 in
place, and the lesson. The book has one fewer `common-confusion` aside (7 → 6).

### 7. Sentence-level repairs

- **Chapter 4 opening (`1521`).** The 41-word sentence with two dash styles is now
  two: "…four things that the word 'search' usually blurs together: query analysis,
  execution rules, understanding and transformation. It then uses them to show
  exactly how far the first two opening puzzles can be taken, and where the
  interface stops answering."
- **Chapter 1 map paragraph (`1285`).** The 42-word opener split after "machinery";
  and "can say truthfully and still **have** heard as something stronger" corrected
  to "still **be** heard".
- **Figure 1.3 caption (`1183`).** Split after "agentic", and the trailing "near the
  end of this book" replaced with a checkable "Chapter 12 examines that claim, and
  where these tools actually sit."
- **Chapter 1, Scopus paragraph (`1149`).** The caveat sentence no longer lands
  mid-description; the description, then "The same two-part architecture is
  visible…", then the caveat.
- **Chapter 1, "controller" (`1164`).** First prose use of the word now glosses it:
  "the controller — the bar above the stages, which chooses and sequences them".
- **Chapter 4, rewriting section (`1608`).** "Until now this book has quietly
  assumed that the words reaching the index are the words you typed" contradicted
  the previous section's second story, Figure 4.3 and Chapter 1's LLM Boolean
  conversion. Now: "So far this book has treated rewriting only in passing: as one
  of the four stories above, and as the first step of Primo Research Assistant's
  pipeline in Chapter 1. Now drop the assumption…"

### 8. Link text that did not name its destination

Thirteen links, hrefs unchanged. Each now names a chapter, appendix or section, so
`maintain.py`'s stale-cross-reference check can verify it (it could not verify
"Discussed later"). The targets' chapters were confirmed from the file before
renaming: `#when-a-system-writes-the-boolean-query` and `#query2doc-and-hyde` are
Chapter 11, `#llms-as-rerankers` and `#why-search-systems-use-multiple-stages`
Chapter 9, `#agentic-search-who-chooses-the-next-retrieval-action` Chapter 12,
`#how-nearest-neighbour-indexing-makes-dense-retrieval-practical` Chapter 7, and
both posting-list anchors Appendix C.

| Where | Was | Now |
|---|---|---|
| Ch1 LLM panel ×2 | "Discussed later." | "Chapter 11 discusses this." / "Chapter 9 discusses this." |
| Ch1 LLM panel | "Query2doc and HyDE." (fragment) | "Chapter 11 covers Query2doc and HyDE." |
| Ch1 shortlist ceiling | "examined later in this book" | "examined in Chapter 9" |
| Ch1 agency | "examined near the end of this book" | "examined in Chapter 12" |
| Ch2, Ch3 ×2 | "the advanced appendix", "the worked example in the appendix" | "Appendix C", "Appendix C's worked example" |
| Ch3 | "the later dense-retrieval section" | "Chapter 7" |
| Ch4 missing-word story 2 | "a section below" | "*The words sent to retrieval may not be the words you typed*" |
| Ch4 after Figure 4.4 | "the list offered a few paragraphs ago" | "the four stories of the previous section" |
| Ch4 distinction map | "Read the distinction", "Where it was left" | see finding 1 |
| Ch2 *In practice* | "We will discuss this in a later section." | see finding 4 |

The five "Read the distinction" and two "Where it was left" links elsewhere in the
book are outside Part I and were not touched.

## Considered and not applied

- **Chapter 1's section order** — the previous plan's reasoning stands.
- **Ledger echoes of claims A–E** in Part I are within budget.
- **Chapter 3's four BM25 questions** are long bullets by design; the figure then
  illustrates each.
- **List-shaped long sentences** (the PubMed / Web of Science / Scopus / EBSCOhost /
  Ovid sentence; "Not every product uses all six stages…") scan fine as lists.
- **The Part I divider's six distinctions**, five of which point into Part II, pair
  deliberately with the Part II divider's "Five confusions are left".
- **The `as-of` dating paragraph** closing Chapter 1 is already styled as a note.
- **CHANGELOG.md** is untouched, as in `readability-plan.md`; whether this joins a
  1.2.2 entry is a release decision.

## What was checked

- Every edit was an exact-match replacement asserted to occur once; three block
  moves were positional. Thirty edits in all.
- `python tools/maintain.py` — "no changes needed", "no problems found" (asset
  numbering, both tables of contents, anchors, duplicate IDs, internal links, stale
  cross-references — which now covers the renamed links).
- `python tools/renumber_footnotes.py` — "already in order (56 footnotes)".
- Byte-identical against the pre-edit file: all 15 chapter closes, all 15
  self-checks, `#exercise1`, the glossary, the footnotes section; the whole of the
  front matter and Preface; and everything from the Part II divider onward. 603
  IDs, none added or removed; every internal `href` resolves.
- Counts: `common-confusion` asides 7 → 6 (finding 6); `ir-figure`, `figcaption`,
  `pull-quote`, `chapter-close`, `self-check` and footnote-reference counts
  unchanged.
- Rendered page, served locally and inspected in the browser: the puzzles heading
  is followed by its lead-in; the *In practice* panel sits between the synonym
  paragraph and the section bridge; Chapter 2 ends panel → bridge → summary;
  Chapter 3's orientation is four paragraphs; Early Google renders as two plain
  paragraphs; no console errors. Term marks: 223 in the book before and after, and
  per chapter 8 / 6 / 11 / 12 for Chapters 1–4 before and after, so the two block
  moves did not lose a first-use mark. A screenshot could not be taken because the
  app window was hidden; the layout checks above are DOM checks.
- Visible words in Part I: 12,172 → 12,191. The plan estimated a loss of 150–250;
  the named section titles and the Chapter 12 explanatory sentence added slightly
  more than the trimmed restatements removed, because the brief was to keep every
  claim. No reading-time label moves at the book's 211 words per minute.
