# Appendix D (A librarian's map of search terminology): review

Reviewed 10 November 2026 against commit `83edbee`. The appendix was about
2,970 words: four tables of term families and eight "misleading overlaps".
Twelve findings were reported. A recheck requested by the author withdrew one
and corrected the evidence for another. The author then asked for all to be
applied, following the reviewer's recommendations on the open decisions.

## Applied

### Rows that contradicted the chapters they point to

- **Deep search and deep research** were listed under agent terminology.
  Chapter 12 says repeated retrieval "does not, by itself, establish agency"
  and that output format is separate. The agent row now lists only agentic
  search, agentic retrieval and search agent, and its description says a model
  plans the sequence. A new row, *Iteration and output*, holds deep search,
  deep research, iterative retrieval and multi-hop retrieval and links
  Chapter 12's section on them.
- **Single-vector retrieval** was listed as a name for the bi-encoder
  arrangement. Chapter 9 says ColBERT also encodes query and document
  separately but keeps many vectors. The expression moved to the dense
  retrieval row.
- **Lexical retrieval** was listed as an expression for sparse retrieval. It
  is removed from that row, whose description now says the word describes
  shape and that a learnt sparse model can weight terms the text never
  contained. The lexical row keeps the expression.

### Structure

- **Exact-match and best-match** were in different tables although Chapters 2
  and 3 teach them as a pair. The best-match row moved from Table D.3 to
  Table D.1, directly after Boolean admission, and is now headed *Best-match
  ranking*. Its text and links are unchanged.
- **Two families added.** *Indexed unit* (chunk, chunking, passage, passage
  retrieval) in Table D.1, linking Chapter 8; and *Query transformation* (query
  understanding, rewriting, expansion, reformulation, pseudo-relevance
  feedback, Query2doc, HyDE) in Table D.2, linking Chapter 11. The glossary
  already defined these terms; the crosswalk had no place for them.

### Links and anchors

- The fusion row was labelled "RRF and score fusion compared" but linked only
  the reciprocal rank fusion section. It now links that section and Chapter
  10's section on combining scores.
- The eight overlaps had no anchors. Each now has one (`overlap-semantic-dense`,
  `overlap-neural-dense`, `overlap-vector-semantic`, `overlap-embedding-search`,
  `overlap-natural-language`, `overlap-hybrid`, `overlap-mcp-rag`,
  `overlap-state-of-the-art`). Chapter 12's "Appendix D separates that pair"
  now lands on the entry about MCP and RAG instead of the top of the section.
- Appendix A and Appendix D each discuss embedding models built on
  decoder-style models, with different sources. Each now links the other.
- "Transformer (neural) encoder models" lost its stray parenthesis.

Table D.1 has twelve rows, D.2 ten, D.3 six and D.4 four. Eight `id`s were
added; none was removed. The glossary lookup was rebuilt and now indexes the
eight overlap headings.

## Not applied

- **Two further overlaps** (sparse is not lexical; deep research is not
  agentic) were considered. The row changes above make both points, and adding
  them would change the count of eight that the section states.
- **Footnote sources without reference entries.** See the correction below.

## Corrections to the review as first reported

- **Withdrawn.** Seven works cited in this appendix's footnotes have no
  reference-list entry, which was reported as a gap. Across the book, 26 of 52
  external links in footnotes and 16 of 158 in the body have no entry. The
  reference list is not exhaustive by design, so the appendix follows normal
  practice.
- **Evidence corrected.** The point that sparse should not be equated with
  lexical was attributed to Figure 8.6. The wording is a banner inside that
  figure's image. The support in running text is Chapter 9 ("lexical in shape
  but learnt throughout") and Chapter 8 ("more meaning-aware than literal
  typed-term matching").

## Limits of what was verified

- The appendix states that its entries are a practitioner's reading of usage
  and carry no citations. That was not challenged, and no usage claim was
  checked against outside sources.
- The sources in the five footnotes were not read.
- The page was not inspected in a browser.

## What was checked

- Every replacement was an exact match asserted to occur once; the moved row
  was cut and pasted whole.
- `tools/maintain.py`, the footnote check, the four builder `--check`s,
  `check-product-claims.py --as-of 2026-09-19` and the four Python test suites
  pass. The Node browser checks were not run.
