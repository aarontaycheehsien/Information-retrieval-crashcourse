# Chapters 5–11: consistency and readability review

Reviewed 6 September 2026 against commit `b2a351f`. Review only; the textbook and companion pages have not been edited. Locations below refer to the reviewed files before any revisions.

The progression is sound: learnt representations → retrieval training → collection-scale retrieval → representation choices → reranking → fusion → query transformation. The main problems are local statements that undo distinctions explained correctly elsewhere, plus some residue from chapter restructuring. Targeted revision is preferable to another structural overhaul.

## Consistency findings, in priority order

### 1. Chapter 8 equates indexed units with generator context immediately after separating them

**Locations:** `search-textbook.html:2022–2024`; Appendix G at `3752` and `3782`.

Chapter 8 says “the indexed unit is also the unit that reaches a model’s context.” The preceding paragraph, its own chapter summary, and Appendix G correctly explain that subsequent fetching, expansion, merging or compression can change that unit. This directly affects the questions readers are supposed to ask vendors.

**Suggested replacement:** “In RAG systems, chunking also affects the evidence available for an answer. The system may supply the retrieved chunk itself, fetch a larger unit, or compress several retrieved units before constructing the model’s context.”

### 2. The calculated/learnt contrast returns after Chapter 5 explicitly corrects it

**Locations:** `search-textbook.html:1544`, `1558`, `1562–1563` versus `1960`, `1971`, `1995`, `2024`, and Appendix D at `3362`.

Chapter 5 correctly says both outputs are calculated; the difference is whether the mapping was specified or fitted during training. Chapter 8 then asks “Were the numbers calculated or learnt?”, says every number is “produced by neural training”, and repeats the binary distinction in a figure caption and summary. Learners can come away thinking stored neural outputs are learnt individually rather than computed for new texts.

**Suggested terminology throughout:** “specified weighting rule versus learnt mapping.” For example: “BM25 computes weights using a specified formula and collection statistics. SPLADE computes weights using a trained model.” Apply this to Figure 8.6 and its image text as well as prose and Appendix D.

### 3. SPLADE is described as retaining BM25’s actual coordinates

**Locations:** `search-textbook.html:1971–1973`, glossary `3828`; compare Chapter 6 at `1707–1710`, Appendix B, and the SPLADE footnote at `4221`.

“Keep BM25’s vocabulary coordinates” and “The coordinate system does not change” are too literal. The useful commonality is vocabulary-aligned sparse coordinates. Standard SPLADE uses a BERT WordPiece output vocabulary; a conventional lexical analyser need not use that vocabulary. The footnote already supplies the missing distinction. The [SPLADE v2 paper](https://www.piwowarski.fr/publication/formal_splade_2021-qabs5ajy/formal_splade_2021-QABS5AJY.pdf) explicitly identifies the WordPiece vocabulary.

**Suggested replacement:** “SPLADE retains the idea of sparse, vocabulary-aligned coordinates, but its vocabulary comes from the model and need not match a conventional BM25 index’s analysed terms.” Label the whole-word heart-attack expansion as schematic.

### 4. Chapter 11 makes SPLADE’s component boundary too categorical

**Locations:** Chapter 9 at `search-textbook.html:2152`; Chapter 11 at `2343` and its self-check at `2380`.

Chapter 9 describes Elicit’s model-suggested terms being sent to regular full-text search. Chapter 11 insists SPLADE is never a separate rewrite handed to another engine. These need reconciliation: a weighted sparse representation can be inspected and passed to an inverted-index backend; physical component boundaries do not establish the conceptual distinction.

**Suggested replacement:** “SPLADE predicts a weighted vocabulary representation; an LLM rewrite produces text or structured expressions. Both outputs can be inspected and passed between components, but they are different forms of retrieval input.”

Also date the Elicit example. Its cited [engineering article](https://elicit.com/blog/semantic-search) is from June 2024 and describes work underway at that time; it alone does not establish the complete current production architecture.

### 5. Routing becomes a combination rule in Chapter 10

**Locations:** `search-textbook.html:2182–2184`, `2205–2214`; Appendix D at `3387`; glossary at `3819`.

The operational definition requires combining multiple candidate-generation routes. Yet “Two hybrids that combine differently” includes a route that may select only one retriever, and says its “combination rule is a decision rather than a fixed blend.” Selecting a path and merging outputs are independent decisions, as the chapter otherwise explains correctly.

**Suggested heading:** “Blending results and selecting retrieval routes.”

**Suggested clarification:** “Scopus AI can select a lexical path, a vector path, or both. A run selecting one path does not combine routes under this book’s definition; a run selecting both still needs a fusion rule.” This also aligns with Appendix G’s explanation that routing and RAG Fusion can coexist.

### 6. The relevance example conflicts with the authoring guidance and becomes too definite

**Locations:** `tools/README.md:118–130`; `search-textbook.html:1700`, `1731–1757`, `2064–2076`.

The maintenance guidance expressly rules out using *delulu* for judged relevance or reranking. Chapters 6 and 9 now use it for exactly that purpose. Chapter 6 labels the example hypothetical and the judgements task-dependent; Chapter 9 shifts into saying a dense retriever returns both passages and they look alike after pooling, despite showing no measured model output.

The interview-performance passage is also not self-evidently irrelevant to a person assessing whether their expectations are unrealistic.

**Suggested repair:** Keep the useful recurring example, update the authoring convention to permit explicitly stipulated training labels, state the assumed information need, and open Chapter 9’s example with “Suppose a first-stage retriever returns both passages.” Avoid presenting the hypothetical ordering as an observed effect of compression.

### 7. Several small references and definitions have not followed the revisions

| Location | Issue | Suggested change |
|---|---|---|
| `search-textbook.html:2076` | “Chapter 5 used that pair” | Chapter **6** contains the positive/hard-negative training pair. |
| `search-textbook.html:2024` | Next-navigation label still says “Reranking, multi-stage and hybrid retrieval” | Match Chapter 9’s current title, “Reranking and multi-stage retrieval”. The destination itself works. |
| `search-textbook.html:2174` | “The pipeline table above” and a concept “not yet named” | Explicitly cite Table 9.1; hybrid has already been named in Chapter 10’s title and opening. |
| Glossary `search-textbook.html:3859`, Appendix E `3443` | RRF described as requiring lists from several retrievers | Say “several ranked lists”. Chapter 10 and Appendix G correctly allow multiple queries through the same retriever. |
| `search-textbook.html:3903` | Link labelled “SPLADE v2” points to the original SPLADE paper | Rename the label, or link to [the actual v2 paper](https://arxiv.org/abs/2109.10086). The bibliography at `4016` correctly names the original. |

### 8. Word2Vec’s teaching simplification loses qualifications supplied elsewhere

**Locations:** `search-textbook.html:1571`, `1580`, `1586`, `1599–1674`; footnote at `4149`.

The earlier account distinguishes CBOW from Skip-gram. Figure 5.6 and the later prose describe Word2Vec generally as recovering a hidden word from neighbours, which is the CBOW arrangement. Label that row “Word2Vec: CBOW illustration”. “How much the model may look at is the whole of the difference” also overstates the analogy across different training tasks; say this is the difference the diagram illustrates.

The main king/man/woman example says queen is the nearest vector, while the footnote explains the exclusion of input words. Move a short qualification into the main example: “In the familiar demonstration, excluding the input words from the candidate answers, queen is returned.”

Finally, “the relation ... was never stated anywhere in what it was trained on” should become “the relationship was not supplied as an explicit training label.” The current wording makes a claim about the entire corpus that the training argument does not require.

### 9. The two reranker budgets do not imply the same treatment of the tail

**Locations:** `search-textbook.html:2128–2130`, `2140–2146`.

After comparing PubMed’s 500 and Primo Research Assistant’s 30, the text says “Everything below the line is ordered by the first stage alone.” This conflates an unreranked continuation with exclusion from the assistant’s answer pipeline. The following Primo walkthrough correctly says records outside the shortlist are absent from its reranking stage, and only five abstracts reach generation.

**Suggested replacement:** “The budget limits which records receive the second score. Whether lower-ranked records remain accessible depends on the product; Primo Research Assistant’s answer uses a further five-source boundary.”

### 10. Teaching notes overgeneralise relevance training and omit new examples from the currency checklist

**Locations:** `teaching-notes.html:191`, `209–216`; Chapters 5–7 and 10; Appendix G.

“Every embedding space carries a theory of relevance” conflicts with Chapter 5’s distinction between word-context training and retrieval training. Use “Every retrieval-trained embedding space rewards particular proxies for relevance.”

The re-verification checklist names the Primo and query-transformation tables but omits Chapter 7’s Semantic Scholar/OpenAlex comparison and Chapter 10’s blending/routing examples. Add these, plus Appendix G’s explicitly historical Scopus RAG Fusion example. Preserve separate architecture dates and dates checked, as the notes already recommend.

## Readability improvements by chapter

| Chapter | Highest-return improvement |
|---|---|
| **5** | Begin with the existing concrete encoder-output example. Shorten the advance warning about difficulty and the opening roadmap. Keep Word2Vec history available, but mark it as optional mechanism/history so readers can reach contextualisation and task training sooner. Replace “This is where the book stops being about words” with “This chapter moves from explicit term matching to learnt representations.” |
| **6** | Give the short chapter visible subheadings for pooling, separate encoding, and training signals. The current encoder section carries several conceptual transitions under one heading. Change the OOD self-check to ask what should be investigated: poor chemistry performance alone does not diagnose which adaptation was omitted. |
| **7** | Keep the lab immediately beside cosine/dot product. Add its useful sentence that the comparison rule should match the model’s training. Then use a compact three-way distinction—eligibility, score, output depth—to reduce repeated explanations across the top-k section, table and summary. Retain the dated product comparison. |
| **8** | Preserve the stepwise lexical-vector walkthrough; it is clear and already says this is not a historical derivation of BM25 from TF–IDF. Reduce repetition among the four questions, Table 8.2, Figure 8.6 and summary. Two chunking figures make almost the same point; make one show a concrete difference between retrieved chunk and supplied context instead. |
| **9** | Shorten the opening promise so it matches reranking and diversification; leave hybrid’s introduction to Chapter 10. Explain learnt sparse retrieval mainly in Chapter 8 and use a short pipeline application here. In the cross-encoder example, replace “the passage knows what will be asked” and “at that resolution the two look much alike” with explicit statements about independent encoding and a possible ranking error. |
| **10** | This chapter is already compact. Repair the routing/fusion distinction before cutting it. Define the operation first, show the RRF example, then use the two products as applications. Replace the claim that RRF is a “neutral” baseline with “simple rank-based baseline”; equal list weights and input depths still embody choices. |
| **11** | The three-group introduction already helps, but Table 11.1 and Figure 11.1 still require readers to process the same eight categories twice. Visually group the rows under the existing three groups; work three representative examples in full and retain all eight as reference. Move the open-access-status warning beside the filter/API example. Replace “reliably partial” in the summary with “limited to supported constraints”. |

Two further wording issues deserve attention in that pass. Table 11.1 labels pseudo-feedback as something the searcher supplies, even though the system assumes the relevance of the initial results; distinguish user judgements from system-assumed relevance. Figure 11.1 presents the eight mechanisms as separate doors, although the following prose correctly says they cooperate: an API can carry a free-text query, and a seed can initiate citation traversal. Say they are useful overlapping distinctions, not mutually exclusive input types.

## Checks and boundaries of this review

- Read Chapters 5–11, relevant surrounding passages, appendices A–G, glossary, teaching notes, lab prose and lab calculation/example code. Also checked the existing readability plan so already-applied improvements were not proposed as new work.
- `node tools/test-labs.cjs` passed: script syntax, BM25 admission/ranking and examples, saturation-chart agreement, vector ranking, unit normalisation and bar bounds.
- Parsed the textbook, teaching notes and both labs: no duplicate IDs or broken internal/cross-file fragment links among those four files. Working links can still have stale labels, as noted above.
- RRF’s worked arithmetic is consistent. BM25’s match requirement and the vector lab’s cosine/dot-product distinction are aligned with the chapters. Appendix F’s distinction between retrieval feedback and screening feedback agrees with Chapter 11.
- This is a source/text and consistency review, not a complete browser-layout audit or fresh verification of every vendor claim. Primary-source checks were targeted to the SPLADE vocabulary, Elicit description and SPLADE paper identity findings.

Suggested revision order: fix findings 1–5, reconcile the example convention and stale references, then make the chapter-specific readability changes. Preserve the current overall chapter order.
