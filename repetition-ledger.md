# Anchor-claim repetition ledger

Status: **APPLIED — scripted verification complete**
Source audited: `search-textbook.html` at commit `9030f75`  
Scope: claims A–E only  
Inventory date: 2026-08-26  
Later amendments: one entry (L1 / E11), added 2026-09-04 after this inventory closed — see the final section

## Method and guardrails

The inventory was built from HTML-decoded, tag-stripped visible text. Curly quotes and dashes were normalised, entities decoded, inline-tag boundaries removed and whitespace collapsed before matching; footnote-reference numerals and heading-anchor glyphs were excluded from the quoted prose. Jaccard scores compare the best-matching sentence in each element with the fixed canonical wording below; they are discovery aids, not automatic edit decisions.

| Claim | Fixed comparison text | Canonical home |
|---|---|---|
| A — match ≠ relevance | “A match is not the same thing as relevance. A match is evidence that may suggest relevance.” | Chapter 1, `#distinction-match-relevance` |
| B — shortlist ceiling | “Every shortlist is also a bottleneck: a reranker, fusion stage or answer-generating model cannot rescue a relevant document that no earlier route allowed into the candidate set.” | Chapter 8, `#why-search-systems-use-multiple-stages` |
| C — query ≠ need | “The query is not the information need. The information need is that fuller purpose; a query is one expression or representation of it.” | Chapter 1, inside `#distinction-match-relevance`; Chapter 9 is the operational application |
| D — top-k boundary | “Top-k is therefore an output boundary, not a retrieval method.” | Chapter 6, `#top-k-is-a-result-boundary-not-a-dense-retrieval-method` |
| E — semantic goal | “Semantic search names the goal, not the architecture.” | Chapter 6, `#semantic-search-is-a-goal-not-an-architecture` |

Fully exempt zones remain inventoried where they match, but are never proposed for editing: `.self-check`, glossary, footnotes, `.detail-drawer` contents and exercises. Canonical-chapter reinforcement, deliberate previews and references, and mechanism-specific applications do not count against the budget of at most three short linked echoes outside the canonical chapter. Existing IDs, headings, classes, assets and structural elements must remain unchanged.

### Baseline invariants

| Measure | Before edits |
|---|---:|
| Core visible words (excluding self-checks, detail drawers, exercises and back-matter indexes) | 60,085 |
| `section.chapter` | 25 |
| `figure.ir-figure` | 46 |
| `figcaption` | 51 |
| `aside.chapter-close` | 13 |
| `section.self-check` | 13 |
| `blockquote.pull-quote` | 10 |
| IDs | 508, all unique |
| Internal links | 1,055, all resolved |

## Claim A — match is evidence, not relevance

Pattern family: `match is not`, `match is evidence`, `evidence about relevance`, `relevance itself`, `semantic similarity is not relevance`, `objective or true relevance`, `relevance is a judgement`, and `not relevance in the abstract`.

| ID | Location and role | J | Classification / disposition | Exact normalised source text |
|---|---|---:|---|---|
| A01 | `#sec-intro` pull-quote | .69 | Canonical — KEEP | A match is not the same thing as relevance. A match is evidence that may suggest relevance. |
| A02 | `#fig-1-5` caption | .11 | Canonical reinforcement — KEEP | Figure 1.5 A retrieval system can observe only the middle three boxes. It cannot see the need at one end or make the judgement at the other, which is why every mechanism in this book produces evidence about relevance rather than relevance itself. |
| A03 | `#sec-intro` body, “The rest of this book…” | .12 | Canonical reinforcement — KEEP | The rest of this book examines different ways retrieval systems generate evidence about relevance. Boolean conditions, BM25 scores, embedding similarity and neural rerankers should therefore not be confused with relevance itself. They are mechanisms for deciding what to retrieve or how to rank it. |
| A04 | `#sec-intro` chapter-close item | .24 | Canonical chapter close — KEEP | The query is a representation of the information need, and matching that representation supplies evidence about relevance rather than relevance itself. |
| A05 | `#sec-intro` self-check | .20 | Exempt retrieval practice — KEEP | That forty records satisfy the representation you supplied. Not that any of them helps with the need behind it — a record can match every term and still be an opinion piece, the wrong population or the wrong decade. And not that the database holds nothing better: the records your wording never reached are not in the set to be judged. Matching is evidence about relevance. The judgement is still yours, and it can only be made about what came back. |
| A06 | `#sec-boolean-admission` body, “Satisfying the query…” | .29 | Pure echo — **PROPOSE A1** | Satisfying the query is not the same as being relevant. Boolean retrieval tells us whether a record meets the conditions the searcher expressed. Those conditions may or may not represent the underlying information need perfectly. This does not make Boolean retrieval inferior: explicit eligibility rules remain valuable when a task requires inspectable, reproducible control over who may enter the result set. |
| A07 | `#sec-bm25-ranking` plain blockquote | .38 | BM25 application with duplicated opener — **PROPOSE A2** | Match is evidence, not relevance. BM25 uses observable lexical evidence—term occurrence, rarity, frequency and document length—to produce a ranking score. That score is useful for ordering candidates; it is neither relevance itself nor a calibrated probability that a document is relevant. |
| A08 | `#sec-embeddings` body, “Every retrieval embedding space…” | .10 | Training-data application — KEEP | Every retrieval embedding space embodies an operational model of relevance: its training data and objective determine which kinds of query–document relationships it learns to reward. Clicks, answer pairs, citations and other labels are proxies for a useful result, not direct observations of relevance itself. |
| A09 | `#sec-dense-at-scale` body, “Semantic similarity…” | .20 | Dense-retrieval application with redundant closer — **PROPOSE A3** | Semantic similarity is not relevance. A document can express meaning very similar to the query and still be unsuitable for the user’s task, context or inclusion criteria. Dense similarity supplies another kind of observable evidence; it does not solve the relevance problem. |
| A10 | `#sec-reranking-and-hybrid` body, “More carefully…” | .18 | Reranking application — KEEP | “More carefully” means using richer evidence to make a better task-specific relevance estimate within that shortlist. It does not mean that a later stage discovers objective or true relevance. |
| A11 | `#relevance-is-a-judgement` heading | .27 | Evaluation chapter’s own subject — KEEP | Relevance is a judgement, not a property. |
| A12 | `#sec-evaluation` body, “Earlier we separated…” | .24 | Evaluation application — KEEP | Earlier we separated matching from relevance and the query from the information need. We can now examine what information-retrieval researchers mean by relevance more carefully. A system can register that terms overlap, vectors are close or a reranker assigned a high score. Those observations may be evidence about relevance, but none is the judgement itself. |
| A13 | `#app-D` terminology table cell | .19 | Reference/index wording — KEEP | Relevance is a judgement; test collections. |
| A14 | `#app-D` body, “A vector can encode…” | .18 | Terminology application — KEEP | A vector can encode lexical weights, locations, citation patterns or manually chosen features. A similarity function compares whatever those vectors represent; it does not make the representation semantic, and even a semantic similarity score is evidence about relevance rather than a relevance judgement or probability. Useful semantic neighbourhoods depend on what was represented and how it was trained; vector, dense and semantic are separate properties. Chapter 6 explains the comparison, and the Vector Similarity Lab makes the distinction interactive. |
| A15 | `#app-E` body, “Editorial labels…” | .20 | Learning-to-rank application — KEEP | Editorial labels have their own boundary: they reflect a task definition, assessors and adjudication process. The ranker learns what the supplied evidence rewards, not relevance in the abstract. This is why Chapter 12’s account of relevance judgements applies as strongly to training data as to evaluation data. |

Pre-edit assessment: two pure later echoes and one mechanism-specific paragraph with a redundant closing sentence. The approved edits would leave no more than three short linked callbacks outside the canonical chapter.

## Claim B — shortlist and candidate ceilings

Pattern family: shortlist bottlenecks, `cannot rescue`, `never surfaced`, `never retrieved/indexed/became a candidate`, `never enters the competition`, `recall ceiling`, first-stage exclusion, and downstream inability to repair an upstream exclusion.

| ID | Location and role | J | Classification / disposition | Exact normalised source text |
|---|---|---:|---|---|
| B01 | `#sec-intro` body, “Whatever quadrant…” | .12 | Deliberate first teach and forward link — KEEP | Whatever quadrant a tool occupies, retrieval still comes first. A quick answer is retrieval followed by generation. Deep research is many rounds of retrieval followed by generation. Nothing in the right-hand column can discuss a paper that the left-hand machinery never surfaced—the shortlist bottleneck examined later in this book. That is the practical reason to spend a whole book on the less glamorous half. A generated answer can be fluent, correctly formatted and properly cited, and still be wrong about the state of the literature, simply because the search behind it missed something. No amount of prompt engineering or model upgrading reveals what was never retrieved. |
| B02 | `#sec-intro` self-check | .16 | Exempt retrieval practice — KEEP | A retrieval failure. Generation failures produce claims the sources do not support; this one is about what never became a candidate. Test it by searching for the missing paper directly in the same tool. If a direct search finds it but it never surfaces for the question, the shortlist is the problem, and no amount of prompting or model upgrading will reveal it. |
| B03 | `#fig-2-1` caption | .13 | Same-section duplication of B04 — **PROPOSE B1** | Figure 2.1 Ranking can push a weakly matched record down, but Boolean has already admitted it. The reverse error is worse: a relevant record that fails a compulsory AND condition never enters the competition at all. |
| B04 | `#sec-boolean-admission` body, “The reverse error…” | .12 | Boolean-admission application — KEEP | The reverse error is more serious. If a relevant record fails a compulsory AND condition, ranking cannot rescue it. It never enters the competition. |
| B05 | `#sec-representations-and-units` body, “The consequence is blunt…” | .13 | Separate indexing-boundary application — KEEP | The consequence is blunt: a system cannot retrieve evidence from text it never indexed. If a claim appears only in a paper’s results section, and the retrieval system holds only that paper’s abstract, no encoder, reranker or generated summary downstream can recover it. This is the same bottleneck logic that governs shortlists, applied one level earlier—at the point where the collection itself was defined. |
| B06 | `#sec-representations-and-units` chapter close | .11 | Separate indexing-boundary close — KEEP | A system cannot retrieve evidence from text it never indexed. No encoder, reranker or generated summary downstream can recover what the collection never held. |
| B07 | `#sec-representations-and-units` self-check | .14 | Exempt retrieval practice — KEEP | What the indexed unit actually is—titles, abstracts, sections or passages—because no encoder or reranker can recover evidence from text that was never indexed. And how several matching chunks from one paper are turned back into a single article-level result. |
| B08 | `#sec-reranking-and-hybrid` body, “This division of labour…” | 1.00 | Canonical — KEEP | This division of labour creates both an efficiency gain and a ceiling. First-stage retrieval normally balances speed with recall; reranking concentrates on precision near the top. Chapter 12 gives those two words their exact meaning, and explains why only the first of them is settled here. Every shortlist is also a bottleneck: a reranker, fusion stage or answer-generating model cannot rescue a relevant document that no earlier route allowed into the candidate set. |
| B09 | `#sec-reranking-and-hybrid` body, “Chapter 6 resolved…” | .10 | Canonical product application — KEEP | Chapter 6 resolved the misleading semantic/dense assumption behind Puzzle 3. We can now see the rest of the documented architecture. Semantic Scholar’s 2025 technical account describes an Elasticsearch keyword search over titles, abstracts and author names, capped at 1,000 matches, followed by a trained LightGBM reranker that emphasises direct title matches, citation counts and recency. The first stage determines which papers the learnt ranker ever gets to reconsider. The second stage changes the order within that boundary. This is machine-learned reranking, but not dense retrieval or an LLM reranker. LightGBM cannot retrieve a paper excluded by the first stage, and its presence does not by itself explain why the August 2026 natural-language query returned 13 results. Appendix E reconstructs the earlier documented 2020 version in depth; the architecture itself belongs in the main chapter. |
| B10 | `#fig-8-1` caption | .74 | Near-verbatim canonical/body duplication — **PROPOSE B2** | Figure 8.1 Every shortlist is also a bottleneck. No reranker, fusion stage or answer-generating model can rescue a relevant document that no earlier route allowed into the candidate set. |
| B11 | `#sec-reranking-and-hybrid` plain blockquote | .11 | Canonical chapter’s single claim quote — KEEP | A sophisticated reranker can reorder only what the retriever allowed it to see. |
| B12 | `#sec-reranking-and-hybrid` chapter close | .13 | Canonical chapter close — KEEP | A reranker can only reorder what the first stage returned. It cannot recover a document that was never retrieved. |
| B13 | `#sec-query-transformation` body, “This is especially…” | .21 | Query-transformation application with repeated rescue clause — **PROPOSE B3** | This is especially important for evidence searches. Ranking cannot rescue a relevant document if a rewrite, compulsory clause, filter or route prevented it from becoming a candidate; feedback can also reinforce an unrepresentative first ranking. Evaluation and reporting should therefore distinguish the original input, every transformed input, the selected routes and any intermediate results used to construct a later query. |
| B14 | `#sec-agentic-search` body, “Recall failures…” | .21 | Agentic-loop application — KEEP | Recall failures compound across rounds. The shortlist bottleneck now applies once per round, and the rounds are not independent. A reranker cannot rescue a document the retriever never returned. In an agentic loop, round two is chosen on the basis of what round one returned—so a concept missed at the start may never be recovered, because nothing downstream has any reason to look for it. Iteration compounds recall failures as readily as it repairs them. |
| B15 | `#sec-diagnosing-failure` body, “Single-vector dense…” | .14 | Diagnostic application — KEEP | Single-vector dense retrieval can also blur a decisive local difference when it pools a whole query or passage into one representation. A cross-encoder reads query and candidate jointly and therefore provides the strongest architectural opportunity to model these relationships. ColBERT-style late interaction preserves more token-level evidence than a pooled bi-encoder, but it still encodes query and document separately and can fail badly on logic and negation. NevIR (Weller et al., 2024) found cross-encoders strongest and late-interaction models next, while most evaluated systems still performed at or below a random ranking baseline. Neither architecture guarantees correct logic, and neither can rescue a record omitted from the first-stage shortlist. |
| B16 | `#sec-evaluation` body, “This also settles…” | .17 | Evaluation application — KEEP | This also settles something left loose in Chapter 8. A first-stage retriever is fast, shallow and broad; a reranker is slow, careful and narrow. Their division of labour is exactly the trade above, split across two stages. A candidate-generating route sets a recall ceiling for everything that processes its fixed output. Parallel routes or a later retrieval round can expand the cumulative candidate set; reranking the existing set cannot. |
| B17 | `#app-E` table cell | .06 | Worked reference application — KEEP | The candidate boundary made richer comparison affordable and remained the reranker’s recall ceiling. |
| B18 | `#app-F` body, “Coverage and retrieval…” | .18 | Evidence-synthesis application — KEEP | Coverage and retrieval must therefore be kept apart. Source selection decides which records could in principle be found. Candidate generation decides which indexed records enter the result set. In a multi-stage ranked pipeline, the first candidate set creates a recall ceiling for every reranker and generator downstream. Relative recall, known relevant studies and fully labelled benchmark datasets can test parts of that process, but none reveals every relevant item in the world. |
| B19 | `#app-F` body, “Candidate retrieval asks…” | .18 | Screening application — KEEP | Candidate retrieval asks, “Which records enter the screening pool?” TAR or active-learning screening asks, “Given that pool, which record should be screened next?” Collapsing the two hides where a miss occurred. A screening model cannot learn from or promote a record that the searches never retrieved. |
| B20 | `#fig-f-3` caption | .12 | Figure-specific boundary application — KEEP | Figure F.3 A relevant study may be absent from the available sources, excluded during candidate retrieval, or left in the unscreened tail. A downstream stage cannot repair an upstream exclusion. |

Pre-edit assessment: one body/caption duplicate in Chapter 2, one near-verbatim canonical caption, and one later echo attached to new reporting content. All other hits teach or apply a distinct boundary.

## Claim C — query is not the information need

| ID | Location and role | J | Classification / disposition | Exact normalised source text |
|---|---|---:|---|---|
| C01 | `#sec-intro` body, “A retrieval system can observe…” | .94 | Canonical — KEEP | A retrieval system can observe and compare representations: analysed query terms, controlled-vocabulary headings, fields, citations, embeddings and other signals. It cannot directly observe everything the person wants to know or accomplish. The query is not the information need. The information need is that fuller purpose; a query is one expression or representation of it. The system acts on the representation, not on the need itself. |
| C02 | `#sec-intro` chapter close | .36 | Canonical chapter close — KEEP | The query is a representation of the information need, and matching that representation supplies evidence about relevance rather than relevance itself. |
| C03 | `#sec-beyond-boolean` body, “This is another consequence…” | .27 | Pure echo — **PROPOSE C1** | This is another consequence of separating the query from the information need: if the query is an imperfect expression of the need, even a retrieval system that handles the query correctly can produce poor results. |
| C04 | `#sec-query-transformation` plain blockquote | .38 | Operational application with duplicated opener — **PROPOSE C2** | The query is not the information need. A query is something a retrieval system can act on that represents some aspect of the need. Depending on the system, that representation might be keywords, a natural-language question, a seed document, a citation, an embedding, retrieval feedback or another object. |
| C05 | `#sec-evaluation` body, “Earlier we separated…” | .17 | Evaluation callback — KEEP | Earlier we separated matching from relevance and the query from the information need. We can now examine what information-retrieval researchers mean by relevance more carefully. A system can register that terms overlap, vectors are close or a reranker assigned a high score. Those observations may be evidence about relevance, but none is the judgement itself. |

Pre-edit assessment: one pure echo and one load-bearing application with a duplicated opener. Both proposed rewrites become short linked callbacks.

## Claim D — top-k is an output boundary

| ID | Location and role | J | Classification / disposition | Exact normalised source text |
|---|---|---:|---|---|
| D01 | `#sec-bm25-ranking` body, “Once candidates…” | .44 | Deliberate forward definition — KEEP | Once candidates have scores, the system can completely order them or retain only the highest-scoring results. The latter is a top-k request: a result boundary, not a scoring method. |
| D02 | `#sec-bm25-ranking` list item | .15 | Mechanism step — KEEP | Choose the output boundary. The engine may completely order the scored candidates or retain only a top-k. |
| D03 | `#sec-bm25-ranking` body, “The Boolean admission rule…” | .17 | BM25 structural application — KEEP | The Boolean admission rule, BM25 scoring rule and top-k output boundary remain separate controls, even when a product executes them in one request. In direct BM25 retrieval, the second step changes: the engine gathers the union of records matching any analysed query term and scores them without first enforcing a strict Boolean AND. |
| D04 | `#sec-beyond-boolean` body, “An admission rule…” | .24 | Part I structural triad — KEEP | An admission rule, a ranking function and a top-k output boundary therefore solve different problems: who may compete, how candidates are ordered, and how many leaders are retained. A production system can control all three independently. |
| D05 | `#sec-beyond-boolean` body, “Google Scholar…” | .26 | Product application — KEEP | Google Scholar: the reported hit count, relevance ordering and viewable set are different properties. Google Scholar reports millions of matches but documents a display limit of 1,000 results. That is an observable output boundary, but it does not reveal the scoring signals, whether every match received a final score, or whether the displayed records are a global top-k. |
| D06 | `#sec-beyond-boolean` chapter close | .22 | Already a compact summary — KEEP | Admission, ranking and the top-k output boundary are separate controls. |
| D07 | `#sec-beyond-boolean` self-check | .14 | Exempt retrieval practice — KEEP | The admission rule decides who may compete, the ranking function orders the candidates, and the top-k output boundary decides how many leaders are retained. |
| D08 | `#sec-embeddings` body, “Before any of that…” | .20 | Forward preview — KEEP | Before any of that can be searched, something has to produce the vectors. This chapter builds that encoder in three moves: from one stored vector per word, to representations that depend on the words around them, to the training without which proximity in the resulting space means nothing in particular. What it takes to run the result against a whole collection—including its top-k boundary—is the next chapter. |
| D09 | `#sec-dense-at-scale` orientation | .22 | Canonical orientation — KEEP | This chapter deploys that encoder. It covers how vectors are stored and compared, how nearest-neighbour indexing keeps the comparison affordable, and what a top-k boundary is and is not. Along the way it resolves the first of the two distinctions Part I left open: semantic search is not synonymous with dense retrieval. The second—that a vector need not be dense, learnt or semantic—is the next chapter’s opening business. |
| D10 | `#sec-dense-at-scale` body, “Top-k is therefore…” | 1.00 | Canonical definition — KEEP | Top-k is therefore an output boundary, not a retrieval method. It is separate from the admission rule that forms the candidate set and from the ranking function that scores it. |
| D11 | `#sec-dense-at-scale` body, “Nor does top-k…” | .11 | Canonical exactness elaboration — KEEP | Nor does top-k mean that only k candidates were examined. An exhaustive method may score every candidate while retaining only the current leaders. Exact BM25 pruning can safely skip candidates that cannot enter the leaders, while approximate nearest-neighbour search may inspect only part of the vector collection and miss a true neighbour. Exactness is another independent choice; Appendix C explains exact lexical pruning. |
| D12 | `#sec-dense-at-scale` chapter close | .26 | Canonical chapter close — KEEP | Dense retrieval assigns similarity scores and orders candidates; top-k sets a result boundary rather than defining a retrieval method. |
| D13 | `#sec-reranking-and-hybrid` table cell | .08 | Pipeline-map label — KEEP | 5. Result boundary. |
| D14 | `#sec-reranking-and-hybrid` table cell | .31 | Cross-chapter mapping — KEEP | Top-k as a result boundary. |
| D15 | `#sec-diagnosing-failure` body, “Before any of that…” | .08 | Diagnostic application — KEEP | Before any of that, establish that the record could have been returned at all. A record absent from the collection, still inside an indexing lag, or excluded by a date limit, format facet or access filter was never eligible, and no amount of vocabulary work will retrieve it. A record that was retrieved but fell outside the result boundary was matched; a cutoff hid it. Where a system indexes passages rather than whole documents, a claim split across separate indexed units may leave no single unit carrying enough evidence to rank. And when a returned result simply lacks a word that was typed, the four explanations in Chapter 4 apply first: analysis may have removed the term; rewriting may have changed it; it may have survived but been optional; or it may have survived without matching a posting. These checks are cheap, and they eliminate causes that no amount of representation work would address. |
| D16 | `#sec-diagnosing-failure` body, “A result screen…” | .12 | Diagnostic checklist — KEEP | A result screen supplies symptoms, not causes. Work from a known relevant record or a controlled contrast whenever possible, confirm the record was eligible and inside the result boundary, then ask: |
| D17 | `#sec-evaluation` body, “A ranked retriever…” | .17 | Evaluation application — KEEP | A ranked retriever instead orders records and may expose only a candidate set such as the top k. That boundary is not unique to dense retrieval; BM25 and other ranked methods can impose it too. If a relevant record falls outside the candidates made available, reranking, screening and an LLM cannot recover it later. The empirical question is therefore whether the complete workflow has adequate sensitivity for the task. Appendix F follows that boundary through retrieval, active-learning screening and stopping. |
| D18 | `#sec-evaluation` body, “The simplest repair…” | .35 | Metric disambiguation — KEEP | The simplest repair is to stop measuring the whole list. Precision@k is precision calculated over the first k results only—precision@10 being common because ten roughly matches a first page. Here k is an evaluation depth: it need not equal the retriever’s top-k output boundary or a reranker’s candidate budget. The measure is easy to explain and captures what informal first-page comparisons are usually doing. |
| D19 | `#app-C` body, “The four-record example…” | .16 | Implementation detail — KEEP | The four-record example is tiny, so scoring every candidate is easy. At web or library scale, an engine would prefer not to calculate a complete score for a document that cannot possibly enter the requested top k. Dynamic pruning methods combine the current threshold θ with safe upper bounds on the contribution still available. |
| D20 | `#app-C` body, “With valid upper bounds…” | .10 | Implementation detail — KEEP | With valid upper bounds, these methods change the work performed, not the answer: they return the same exact top k as exhaustive scoring. That guarantee is different from approximate early termination, which may deliberately trade some result quality for speed. The original methods are described by Turtle and Flood’s MaxScore work, Broder and colleagues’ WAND paper and Ding and Suel’s Block-Max indexes paper. |
| D21 | `#app-D` terminology table cell | .31 | Reference/index wording — KEEP | Ranked retrieval and BM25; top-k as a result boundary. |
| D22 | `#app-F` plain blockquote | .46 | Evidence-synthesis application — KEEP | Top-k is not a dense-retrieval issue. It is a ranked-retrieval boundary issue. |

Disposition: **no edits**. These are progressive definitions, compact summaries, mappings or later applications; the stale work order’s supposed second freestanding Chapter 4 restatement does not exist.

## Claim E — semantic search names a goal

| ID | Location and role | J | Classification / disposition | Exact normalised source text |
|---|---|---:|---|---|
| E01 | `#sec-preface` body, “Today, semantic search…” | .88 | Preface landing definition — KEEP | Today, semantic search is commonly implemented with dense retrieval: queries and documents are encoded as dense vector representations—usually called embeddings—and compared by similarity. But semantic search names the goal, not the architecture. Query or ontology expansion layered onto lexical retrieval, learnt sparse retrieval, semantic reranking of a lexical shortlist, and hybrid combinations can also provide meaning-oriented matching. |
| E02 | `#sec-beyond-boolean` body, “Two further distinctions…” | .26 | Deliberate Part I transition — KEEP | Two further distinctions become important as we turn to neural retrieval. First, semantic search does not mean dense retrieval: semantic names a goal, while dense retrieval names one technical route towards it. Second, vector does not automatically mean dense, learnt or semantic. BM25 scores can be represented with sparse, vocabulary-aligned vectors, while contemporary bi-encoders usually produce learnt dense vectors. These distinctions are related, but they are not the same claim. |
| E03 | `#semantic-search-is-a-goal-not-an-architecture` heading | .50 | Canonical heading — KEEP | Semantic search is a goal, not an architecture. |
| E04 | `#sec-dense-at-scale` body, “Semantic describes…” | .14 | Canonical definition — KEEP | Semantic describes what the search is trying to achieve: matching by meaning rather than only literal words. It is usually contrasted with lexical search, which draws its evidence from matches between analysed query and document terms. BM25, ontology or query expansion, dense retrieval and neural reranking describe mechanisms a system might combine in trying to achieve the semantic goal. |
| E05 | `#sec-dense-at-scale` body, “Dense retrieval over…” | .17 | Canonical terminology disambiguation — KEEP | Dense retrieval over vector embeddings is the most familiar contemporary implementation of the semantic goal. This is why semantic search, dense retrieval, vector search and embedding search are often used as if they were synonyms. They are not: semantic names an intended capability, dense describes the shape of a representation, vector names a kind of representation, and embedding names a learnt mapping into a vector space or, by shorthand, the vector it produces. |
| E06 | `#sec-dense-at-scale` chapter close | .33 | Canonical chapter close — KEEP | Semantic search describes a goal rather than an architecture. BM25, ontology expansion, dense retrieval and neural reranking name mechanisms a system may combine in pursuit of it. |
| E07 | `#sec-dense-at-scale` self-check | .18 | Exempt retrieval practice — KEEP | It has stated a goal or capability claim: the search is meant to match by meaning rather than only literal words. It has not specified an architecture. Ask whether meaning enters through ontology or query expansion, learnt-sparse or dense retrieval, neural reranking, or a combination; where BM25 or another lexical stage sits; and which stage forms the candidate boundary. |
| E08 | `#app-D` terminology table definition | .14 | Reference/index wording — KEEP | A goal or capability claim that the system goes beyond literal term matching, usually contrasted with lexical search. Dense retrieval over embeddings is the most familiar contemporary implementation, but the labels reveal little about architecture: lexical retrieval may supply candidates, while ontology or query expansion, learnt-sparse retrieval, dense retrieval and neural reranking may contribute meaning-oriented evidence at different stages. |
| E09 | `#app-D` terminology table link cell | .31 | Reference/index wording — KEEP | Semantic search is a goal, not an architecture; vector, dense and semantic are different properties. |
| E10 | `#app-D` body, “The association is understandable…” | .15 | Explicit terminology reminder — KEEP | The association is understandable: dense retrieval over vector embeddings is the most familiar contemporary implementation of semantic search. It is not an equivalence. Chapter 6 establishes the main distinction: semantic describes a goal, usually contrasted with lexical matching, while BM25, ontology expansion, dense retrieval and neural reranking describe mechanisms that may contribute to it at different stages. Learnt sparse retrieval and query expansion can support meaning-oriented matching, while another system may apply a semantic model only when reranking a lexical shortlist. This appendix is a terminology reminder, not where the argument is introduced. |
| E11 | `#sec-preface` body, “Two products can both claim…” | .14 | Added 2026-09-04, not seen at inventory — EDITED, see L1 | Two products can both claim to offer “semantic search” while doing quite different things under the hood. One might be BM25 with query expansion. Another might use dense-vector retrieval, learnt sparse retrieval, lexical–dense fusion, or a neural reranker over a lexical shortlist. Those are not implementation details in the trivial sense. They affect how you should enter your search query, which papers even make it into the candidate set and which ones rise high enough for the user to see. |

Disposition: **no edits**. The current Chapter 6 prose is progressive rather than two consecutive duplicated bold paragraphs, and the supposed Chapter 8/10 echoes are absent.

**Amended 2026-09-04.** The disposition above stands for E01–E10. E11 was found later and edited; it restates E01’s mechanism list four lines above it, and neither instrument in this workstream could have flagged it. See L1 under *Later amendments*.

## Approved and applied reversible edits

All eight entries were approved after the user delegated the editorial decision. Each `before` snippet was verified verbatim immediately before editing, and each `after` snippet occurs exactly once in the resulting source.

### A1 — Chapter 2 pure echo

Before:

```html
<p><strong>Satisfying the query is not the same as being relevant.</strong> Boolean retrieval tells us whether a record meets the conditions the searcher expressed. Those conditions may or may not represent the underlying information need perfectly. This does not make Boolean retrieval inferior: explicit eligibility rules remain valuable when a task requires inspectable, reproducible control over who may enter the result set.</p>
```

After:

```html
<p>Boolean retrieval tells us whether a record meets the conditions the searcher expressed, <a href="#distinction-match-relevance">not whether it is relevant to the underlying need</a>. This does not make Boolean retrieval inferior: explicit eligibility rules remain valuable when a task requires inspectable, reproducible control over who may enter the result set.</p>
```

### A2 — Chapter 3 duplicated blockquote opener

Before:

```html
<blockquote><p><strong>Match is evidence, not relevance.</strong> BM25 uses observable lexical evidence—term occurrence, rarity, frequency and document length—to produce a ranking score. That score is useful for ordering candidates; it is neither relevance itself nor a calibrated probability that a document is relevant.</p></blockquote>
```

After:

```html
<blockquote><p>BM25 uses <a href="#distinction-match-relevance">observable lexical evidence</a>—term occurrence, rarity, frequency and document length—to produce a ranking score. That score is useful for ordering candidates; it is neither relevance itself nor a calibrated probability that a document is relevant.</p></blockquote>
```

### A3 — Chapter 6 redundant closing sentence

Before:

```html
<p><strong>Semantic similarity is not relevance.</strong> A document can express meaning very similar to the query and still be unsuitable for the user’s task, context or inclusion criteria. Dense similarity supplies another kind of observable evidence; it does not solve the relevance problem.</p>
```

After:

```html
<p><strong>Semantic similarity is <a href="#distinction-match-relevance">not relevance</a>.</strong> A document can express meaning very similar to the query and still be unsuitable for the user’s task, context or inclusion criteria.</p>
```

### B1 — Figure 2.1 duplicate caption sentence

Before:

```html
<figcaption><span class="asset-label-inline" id="fig-2-1">Figure 2.1</span> Ranking can push a weakly matched record down, but Boolean has already admitted it. The reverse error is worse: a relevant record that fails a compulsory <code>AND</code> condition never enters the competition at all.</figcaption>
```

After:

```html
<figcaption><span class="asset-label-inline" id="fig-2-1">Figure 2.1</span> Ranking can push a weakly matched record down, but Boolean has already admitted it.</figcaption>
```

### B2 — Figure 8.1 near-verbatim canonical caption

Before:

```html
<figcaption><span class="asset-label-inline" id="fig-8-1">Figure 8.1</span> Every shortlist is also a bottleneck. No reranker, fusion stage or answer-generating model can rescue a relevant document that no earlier route allowed into the candidate set.</figcaption>
```

After:

```html
<figcaption><span class="asset-label-inline" id="fig-8-1">Figure 8.1</span> Fast stages search the collection; expensive stages see only the survivors.</figcaption>
```

### B3 — Chapter 9 rescue-clause echo

Before:

```html
<p>This is especially important for evidence searches. Ranking cannot rescue a relevant document if a rewrite, compulsory clause, filter or route prevented it from becoming a candidate; feedback can also reinforce an unrepresentative first ranking. Evaluation and reporting should therefore distinguish the original input, every transformed input, the selected routes and any intermediate results used to construct a later query.</p>
```

After:

```html
<p>This is especially important for evidence searches. A rewrite, compulsory clause, filter or route can <a href="#why-search-systems-use-multiple-stages">exclude a relevant document before ranking</a>; feedback can also reinforce an unrepresentative first ranking. Evaluation and reporting should therefore distinguish the original input, every transformed input, the selected routes and any intermediate results used to construct a later query.</p>
```

### C1 — Chapter 4 pure echo

Before:

```html
<p>This is another consequence of separating the query from the information need: if the query is an imperfect expression of the need, even a retrieval system that handles the query correctly can produce poor results.</p>
```

After:

```html
<p>Because <a href="#distinction-match-relevance">the query is only a representation of the information need</a>, even a retrieval system that handles it correctly can produce poor results.</p>
```

### C2 — Chapter 9 duplicated blockquote opener

Before:

```html
<blockquote><p><strong>The query is not the information need.</strong> A query is something a retrieval system can act on that represents some aspect of the need. Depending on the system, that representation might be keywords, a natural-language question, a seed document, a citation, an embedding, retrieval feedback or another object.</p></blockquote>
```

After:

```html
<blockquote><p>A query represents some aspect of the need in <a href="#distinction-match-relevance">a form a retrieval system can act on</a>. Depending on the system, that representation might be keywords, a natural-language question, a seed document, a citation, an embedding, retrieval feedback or another object.</p></blockquote>
```

## Filtered generic sweep — observations only

The book-wide sweep compared 2,154 eligible sentence blocks at Jaccard ≥ .80 after excluding navigation, asset indexes, references, examples, self-checks, detail drawers, exercises, glossary content, footnotes and nested parent/child duplicates. Seven pairs remained. E01/E04 is already classified under Claim E; the other six are `OUT-OF-SCOPE` and must not be edited in this workstream.

| J | First sentence | Second sentence | Status |
|---:|---|---|---|
| 1.00 | Preface: “It is usually contrasted with lexical search, which draws its evidence from matches between analysed query and document terms.” | Chapter 6: same sentence | Claim E — deliberate landing/canonical repetition, KEEP |
| 1.00 | Chapter 2: “Posting lists are normally sorted by document identifier.” | Appendix C: same sentence | OUT-OF-SCOPE |
| 1.00 | Chapter 4 body: “The bad term stops deciding who competes and starts distorting who wins.” | Chapter 4 figure caption: same sentence | OUT-OF-SCOPE |
| 1.00 | Chapter 10 body: “An agent can only choose among the tools it has.” | Chapter 10 chapter close: same sentence | OUT-OF-SCOPE |
| .89 | Chapter 1: “One decides which records exist as far as your question is concerned, and in what order they are placed.” | Chapter 1 list item: “Retrieval decides which records exist as far as your question is concerned, and in what order they are placed.” | OUT-OF-SCOPE |
| .86 | Chapter 6 body: “Each indexed unit is encoded without seeing the query, so its vector can be calculated in advance and stored.” | Figure 6.3 caption: same sentence after its label | OUT-OF-SCOPE |
| .85 | Chapter 6 body: “Each indexed passage must compress its topic, named entities, claims, qualifications and terminology into one point before it knows which query will arrive.” | Figure 6.5 caption: near-identical sentence after its label | OUT-OF-SCOPE |

## Approval record

- Inventory commit: `52a1552` (`audit: inventory anchor-claim repetition`)
- Human approval: delegated by the user with “you decide”; all eight conservative edits approved
- Approved and applied edit IDs: A1–A3, B1–B3 and C1–C2
- Source drift check: PASS — all eight `before` snippets occurred exactly once before editing; all are absent afterwards; every `after` snippet occurs exactly once

### Final counts and word delta

| Claim family | Before | After | Interpretation |
|---|---:|---:|---|
| A — match ≠ relevance | 15 | 14 | One pure echo removed; retained matches are canonical reinforcement or applications |
| B — shortlist ceiling | 20 | 17 | Two duplicated captions and one later rescue-clause echo removed |
| C — query ≠ need | 5 | 4 | One duplicated opener removed; remaining linked callback is shorter |
| D — top-k boundary | 22 | 22 | Intentionally unchanged |
| E — semantic goal | 10 | 10 | Intentionally unchanged |
| **Total raw pattern hits** | **72** | **67** | Claim budgets satisfied after contextual classification |

Core visible words changed from 60,085 to 59,991: **−94 words (−0.1564%)**. This is informational only and is consistent with a narrowly scoped anchor-claim trim.

| Edited chapter | Before | After | Existing chip | Scaled result |
|---|---:|---:|---:|---:|
| Chapter 2 | 2,347 | 2,314 | 13 min | 13 min |
| Chapter 3 | 1,889 | 1,884 | 11 min | 11 min |
| Chapter 4 | 1,890 | 1,878 | 10 min | 10 min |
| Chapter 6 | 3,025 | 3,010 | 16 min | 16 min |
| Chapter 8 | 4,947 | 4,931 | 24 min | 24 min |
| Chapter 9 | 3,193 | 3,180 | 17 min | 17 min |

No reading-time chip changes were warranted after proportional scaling and nearest-minute rounding.

### Final verification

- PASS — `python tools/maintain.py`: no changes needed; no problems found
- PASS — `python tools/renumber_footnotes.py`: all 56 footnotes already in order
- PASS — all 508 pre-edit IDs remain; no IDs were added or duplicated
- PASS — all 1,061 post-edit internal links resolve
- PASS — structural counts remain 25 chapters, 46 `.ir-figure` elements, 51 captions, 13 chapter closes, 13 self-checks and 10 pull-quotes
- PASS — `git diff --check`
- PASS — affected HTML elements and new link targets parse correctly in the DOM
- NOT AVAILABLE — in-app visual inspection; the local browser plugin could not initialise its trusted runtime path. No alternate browser surface was substituted. Because every edit shortens existing prose without changing element structure or CSS classes, this is recorded as a non-blocking tooling limitation.

## Later amendments

Everything above describes the workstream that closed at `9030f75`. Entries here were found after that inventory and are kept separate so the two are not confused. The counts, approval record and verification above are not restated or revised.

### L1 — Preface mechanism list restated by its own key-definition aside

Found 2026-09-04, applied on top of `906fe1a`. Inventoried as E11.

The preface body paragraph and the `.common-confusion` aside four lines below it name the same five mechanisms in the same order, with the wording substituted throughout:

| E11 — preface body | E01 — key-definition aside |
|---|---|
| BM25 with query expansion | Query or ontology expansion layered onto lexical retrieval |
| dense-vector retrieval | commonly implemented with dense retrieval |
| learnt sparse retrieval | learnt sparse retrieval |
| lexical–dense fusion | hybrid combinations |
| a neural reranker over a lexical shortlist | semantic reranking of a lexical shortlist |

**Why neither instrument flagged it.** Both scored the pair far below their thresholds:

| Comparison | J | Instrument | Outcome |
|---|---:|---|---|
| E11 best-matching sentence vs the Claim E fixed wording | .14 | Claim E scan | not flagged |
| E11 enumeration vs E01 enumeration, compared directly | .21 | Book-wide sweep at ≥ .80 | not flagged |

Only seven tokens are shared between the two lists — `a`, `learnt`, `lexical`, `or`, `retrieval`, `shortlist`, `sparse`. The repetition is in the referents, not the words, so no token-overlap threshold could have caught it: lowering the cut-off far enough to surface a .21 pair would return most of the book. This is a limit of the method rather than a lapse in applying it. Jaccard remains a sound discovery aid for verbatim and near-verbatim echo, as the guardrails section already states; conceptual restatement of this kind has to be found by reading.

**Disposition: trim E11, keep E01.** E01 is the landing definition and is written to stand alone for a reader who skips the body or returns to it later; the guardrails already exempt that role from the echo budget. E11’s unique work is the stake (“I’m not sure it does anymore”) and the consequence sentence, neither of which appears anywhere else. Only the enumeration was cut.

Before:

```html
<p>Two products can both claim to offer “semantic search” while doing quite different things under the hood. One might be BM25 with query expansion. Another might use dense-vector retrieval, learnt sparse retrieval, lexical–dense fusion, or a neural reranker over a lexical shortlist. Those are not implementation details in the trivial sense. They affect how you should enter your search query, which papers even make it into the candidate set and which ones rise high enough for the user to see.</p>
```

After:

```html
<p>Two products can both claim to offer “semantic search” while doing quite different things under the hood. One might be BM25 with query expansion. Another might compare learnt vectors instead, with no lexical stage anywhere. Those are not implementation details in the trivial sense. They affect how you should enter your search query, which papers even make it into the candidate set and which ones rise high enough for the user to see.</p>
```

Two constraints shaped the replacement wording:

- The quoted phrase “semantic search” is retained verbatim. It is the first markable occurrence in the preface, so the glossary term-mark and its tooltip still attach to this paragraph; rewording it would have moved the mark to the aside, which `SKIP` does not exclude.
- “returns a paper that shares none of your words” was rejected. Chapter 1 already says a record “can come back missing one of your words while the system is still scoring on nothing but words” — a different claim, about ranked lexical retrieval rather than dense, that the book keeps deliberately apart. Near-identical wording ten lines away would blur two distinctions the argument depends on separating.

**Accompanying change, not a repetition finding.** Five glossary entries were added in the same pass — *neural search*, *vector search*, *embedding search*, *agentic search* and *AI-powered search* — so that the preface’s list of vendor labels has definitions behind it. The glossary is a fully exempt zone under the guardrails, and none of the five were added to the `MARKED` list, so no new term-marks appear and no echo budget is affected. This also closes a dangling reference: the existing *Agentic RAG* entry described itself as “a narrower case of agentic search”, a term the glossary did not define.

Word delta: the edited paragraph goes from 80 to 73 words (**−7**). The book-wide core-count above is not recomputed; this entry is not part of that measurement.

Verification:

- PASS — `python tools/maintain.py`: no changes needed; no problems found
- PASS — HTML parses with every tag balanced and no unclosed elements
- PASS — the `before` snippet occurred exactly once before editing and is absent afterwards; the `after` snippet occurs exactly once
- PASS — first-use term-mark simulation still resolves “semantic search” to the edited paragraph
- PASS — glossary integrity: 79 entries, no duplicate `<dt>` labels, no collisions with `MARKED` or `MARKED_CASED`
- NOT AVAILABLE — in-app visual inspection; the browser surface in this session could not open local files. Recorded as non-blocking for the same reason as above: the edit shortens existing prose without changing element structure or CSS classes.
