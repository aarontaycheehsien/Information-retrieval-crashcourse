# Whole-book consistency review, second pass

Reviewed 25 September 2026 on branch `fable-1` against commit `71519b3`, after the
companion releases (evaluation kit, product-claims register, vendor questionnaire,
glossary hub, digest, Rank Fusion Lab) and the second readability pass over every
chapter. The whole of `search-textbook.html` was read: Preface, fifteen chapters, three
part dividers and exercises, seven appendices, glossary, 56 footnotes and back matter.
Automated checks covered reading-time sums, chapter navigation labels, pipeline-map
highlighting, anchors, and every main-text external link against the reference list.

## Findings applied

| Where | Was | Now |
|---|---|---|
| Chapter 1, pipeline key | The *Fusion* card linked to Chapter 9; the strip above it links to Chapter 10 | Links to Chapter 10 |
| Chapter 1, dating note | "The opening screenshots were checked in September 2026", although the Puzzle 3 counts are dated August 2026 | The answer-surface screenshots were checked in September; the Semantic Scholar counts were observed in August |
| Application exercise I, Next link | "Embeddings and the retrieval encoder" (a retired title) | "Embeddings: what the learnt geometry encodes" |
| Table 9.3 caption | "mapped to every stage described in this book"; Table 1.1 says the product skips fusion | "mapped to the stages described in this book" |
| Appendix E, PubMed paragraph | PubMed's 500 candidates were "a fifth" of Semantic Scholar's 1,000 | "half the candidate depth" (claim-register excerpts updated) |
| Appendix G, basic pattern | "the definition Chapter 1 introduced" linked to the section after the definition | Links to the RAG key-definition box |
| Appendix D, misleading overlaps | "eight additional comparisons"; four of them restate core distinctions | "restate four of the six core distinctions as reminders and add four more" |
| Appendix D, own voice | "learned" in a family label, a table caption and three sentences; the book spells it "learnt" | "learnt"; the quoted common-expression lists keep "learned" |
| Application exercise III | "agentic control if any"; Table 15.1's fourth row is retrieval control for every arrangement | "retrieval control (fixed, adaptive or agentic)" |
| Glossary, *Representation* | "the broadest of the three terms below"; in alphabetical order *Embedding* comes above | "the broadest of three nested terms: representation, vector and embedding" |
| Glossary, four relevance levels | Linked only to Chapter 1, which says Chapter 14 separates them | Also link to Chapter 14's *Relevance is a judgement* (`data/glossary-map.json`) |
| References | *Where to go deeper* says the list records the sources cited in the main text; eight research sources cited there had no entry | Added: Alammar (2018), Carpenter (2024), Cohen et al. (2006), Es et al. (2024), Lewis et al. (2020), Rashkin et al. (2023), Raudaschl (n.d.), Santhanam et al. (2022), in alphabetical position. Venues and pages checked against the publisher pages |

## Flags for the author, not changed

- **Product documentation missing from the reference list.** About 25 more main-text
  links are product or technical documentation with no reference entry. Examples are
  Google Scholar help (Puzzle 2's evidence), PostgreSQL, Elastic, Weaviate and Faiss
  documentation, the GTE and BERT model cards, and Web of Science Advanced Search.
  Other product documentation *is* listed, so the list is inconsistent. Either add
  entries or narrow the claim to "research sources and cited product documentation".
- **Model-name spelling.** Unresolved from the first review: "GPT-4.1 Mini" (Chapter 1,
  Primo Research Assistant) against "ChatGPT 4.1 Mini" (Table 11.4, NDE Natural
  Language Search).
- **Generative AI disclosure.** It names the BM25 Evidence Lab and Vector Similarity
  Lab but not the Rank Fusion Lab or the other new companions. The tools used for
  those are the author's to state.
- **CHANGELOG.** Not updated: it carries uncommitted repository-organisation edits.

## Follow-up applied the same day, at the author's request

- **Model name.** Table 11.4 and the matching register entry now say "GPT-4.1 Mini",
  as Chapter 1 does. The regenerated teaching notes follow.
- **Disclosure.** It now names all three labs and the newer companion pages: the
  evaluation kit and its workbooks, the vendor questionnaire, the Read this first
  digest and the glossary lookup.
- **Documentation references.** Sixteen entries were added after each linked page was
  fetched to confirm its title: ASReview's *Simulate a review*, Chatelain (2026), the
  Web of Science *Advanced Search* page, Cohan et al. (2020, SPECTER), Elastic, Elsevier
  (2025), Faiss, the Hugging Face BERT card, Google Scholar search help, PubMed Advanced
  Search Builder, PostgreSQL, Scite, Tay (2026c), the GTE card, Weaviate and Wiley.
  Same-author entries were relettered (ASReview n.d.-a/b, Clarivate n.d.-a/b, Tay
  2026a–e); nothing in the text cites by those labels. The ten main-text links still
  without a matching URL all point to works already listed under another URL, for
  example DrQA, PubMed Best Match, *Introduction to Information Retrieval* and the
  PubMed User Guide. The list holds 150 entries in alphabetical order.
- **Dead link.** Chapter 12's Wiley AI Gateway link (`wiley.com/en-us/ai`) returned
  404. It now points to Wiley's AI Gateway documentation at `docs.scholargateway.ai`,
  in the text and in the `scite-mcp` and `wiley-mcp` register evidence.

## Checked and consistent

Part reading times (67, 107, 82) against the chapter labels. Every other Previous/Next
label. The six core distinctions across the Preface, the Part I checklist, Part II's
panel, Chapter 4 and the closing section. The nineteen vendor questions in six groups.
Figure 3.1's saturation factors. Table 14.3's means. Figure 1.3 quadrants against
Chapter 12. The Primo budgets (30 and 5), PubMed 500, Semantic Scholar 1,000, and RRF
with c = 60. The chapter attributions in all appendices. The glossary against the
chapters.

## Verification

`maintain.py` found no problems. The footnotes are in order (56). The product-claims,
glossary and digest `--check` runs pass, as do `test-glossary-hub`,
`test-product-claims`, `test-digest`, `test-vendor-questionnaire`,
`test-evaluation-kit`, `test-labs.cjs`, `test-rank-fusion.cjs` and
`test-vector-tour.cjs`.
