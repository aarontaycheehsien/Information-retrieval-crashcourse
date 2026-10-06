# Factual accuracy review

Reviewed 25 September 2026 on branch `fable-1` at commit `02cc5b3`. The review looked
for serious factual errors across the whole of `search-textbook.html`. It recomputed
every worked calculation and checked the highest-risk product and research claims
against their sources.

**Result: no serious factual errors found.** One cross-reference was corrected.

## Corrected

- **Table 2.3 caption.** It said the D1–D4 records are "returned to in Chapters 3–4
  and Appendix C". Chapters 3 and 4 never use them. Chapter 3 uses a ten-document
  illustration, and Chapter 4 uses the apple/orange cards and the lab's records. The
  caption now says "returned to in Appendix C".

## Recomputed and correct

- Figure 3.1's saturation factors (1.00, 1.375, about 2.08).
- Appendix C's IDF values, its four BM25 scores and component contributions, the
  heap threshold and the WAND bound (0.810).
- Table 10.1's RRF scores.
- The MMR values in Table E.4.
- Figure 7.7's distances.
- Table 14.3's means.
- Figure 14.1's precision and recall.
- The WSS@95 example.
- The Puzzle 2 and Puzzle 3 arithmetic.
- The Chapter 8 binary and TF vectors.
- The MaxSim sum.
- Appendix B's WordPiece pieces and IDs, confirmed by running the
  `google-bert/bert-base-uncased` tokeniser, whose vocabulary size is 30,522.

## Checked against sources and correct

- **Primo Research Assistant:** GPT-4.1 Mini, up to 30 CDI results, embedding
  rerank to five.
- **NDE Natural Language Search:** six permutations.
- **OpenAlex Alice:** GTE Large EN, 1,024 dimensions, cosine similarity, one search
  mode per request, shipped February 2026, 413M embeddings, 25 April 2026 post.
- **Semantic Scholar, Kinney et al. v2 (25 April 2025):** titles, abstracts and author
  names in Elasticsearch, 1,000 matches, a LightGBM reranker favouring title matches,
  citations and recency. §3.4.4 describes SPECTER for author disambiguation and
  recommendations.
- **Semantic Scholar 2020:** about 190M papers, top 1,000, LightGBM with LambdaRank,
  22 features, KenLM.
- **PubMed Best Match:** top 500 reranked by LambdaMART, with no citation-count
  feature.
- **CDI:** the ranking signals and the *science* versus *science AND neurology*
  example.
- **Web of Science Research Assistant post (9 April 2026):** all quotations, and the
  three earlier guides.
- **EBSCO AI-Assisted Search:** parsing into keywords and noun phrases; no model
  named.
- **Elicit:** 13 June 2024, SPLADE described as work in progress.
- **ASReview:** no default stopping threshold, and the ideal value is still under
  research.
- **ColBERTv2:** 6–10× smaller footprint.
- **NevIR:** at or below random; cross-encoders best, late interaction next.
- **Greenhalgh and Peacock:** 495 sources, 30% from the protocol, 51% from
  snowballing.
- **Kempny et al.:** 35,000 simulations, five datasets, 2.9–76.9%.
- **Byrne et al.:** feature-extractor effect.
- **Repke et al.:** 15 methods, 81 datasets, one method reliably meets the target but
  stops conservatively.
- **Model and research chronology:** the Transformer (2017), GPT (June 2018), BERT
  (October 2018), ELMo (2018), RankBrain (2015) and BERT in Google Search (2019).
- **Model details:** BioBERT, PubMedBERT and SciBERT corpus figures, and SPECTER.

## Flags for the author, not changed

- **Repke et al.'s reliable method.** The abstract confirms that one method met the
  recall target conservatively. The full text was blocked, so this review could not
  confirm that the method is CMH.
- **Refinitiv to LSEG, Chapter 12.** The book says the rebrand "postdates the query".
  LSEG announced it in late August 2023 and applied it from November 2023. That holds
  only if the 2023 log entries predate those dates.
- **NDE model name.** Table 11.4 now reads "GPT-4.1 Mini" at the author's request. The
  Ex Libris page itself says "ChatGPT 4.1Mini".
- Claims resting on the author's own April–June 2026 posts were not re-verified. These
  are the Chapter 12 probe results, the tool placements and the Undermind Projects
  agent names.
