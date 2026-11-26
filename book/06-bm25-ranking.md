---
key: "bm25-ranking"
kind: "chapter"
eyebrow: "Chapter 3"
meta: "About 13 min"
question: "How does matching evidence become a relevance ranking?"
legacy_anchors: ["ch2"]
---

## BM25 and ranked lexical retrieval {#bm25-ranking}

::: {.stage-map on="first-stage"}
:::

::: chapter-orient
Boolean retrieval treats every matching term as equally informative and every eligible record as equally good.
Neither is true.
A term occurring in three records is far more discriminating than one occurring in three hundred thousand, and a record using a term eight times is usually more about it than a record using it once.

BM25 is a standard way of turning those intuitions into a score.
This chapter explains what it measures, why repetition saturates rather than counting linearly, and how it runs over exactly the same inverted index the previous chapter built.

Scoring of this kind is **ranked retrieval**.
Rather than leaving every retrieved record tied, a ranked retrieval system assigns candidates graded scores and orders them from higher to lower scoring.
Ranked retrieval does not specify how those scores are calculated: they may come from lexical evidence, as with TF-IDF or BM25; from [dense-vector similarity](#single-vector-dense-retrieval-compress-first-compare-later); from [learnt sparse representations](#learnt-sparse-representations); or from combinations of several signals.

Once candidates have scores, the system can completely order them or retain only the highest-scoring results.
The latter is [**a top-*k* request**](#top-k-is-a-result-boundary-not-a-dense-retrieval-method): a result boundary, not a scoring method.
:::

### BM25: words as weighted clues {#bm25-words-as-weighted-clues}

Most academic databases allow a relevance sort, under user-facing labels such as **Relevance** or **Best Match**. [Scopus](https://service.elsevier.com/app/answers/detail/a_id/11423/supporthub/scopus/) and [Web of Science](https://webofscience.help.clarivate.com/en-us/Content/search-results.htm?Highlight=sort), for example, let a searcher choose relevance rather than date or citation-based ordering.
The label tells us that records will be ordered, but not how: [PubMed calls its default relevance sort Best Match](https://pubmed.ncbi.nlm.nih.gov/help/), a label whose [documented architecture](#bm25-and-lexical-ranking-in-academic-search) this chapter opens up below.

A common academic-search pattern has two controls.
A Boolean expression first defines the eligible set; a separate scoring method then orders the records that survive.
Strict Boolean logic can decide who passes, but it cannot distinguish among records that all pass.

> The ranking stage need not be plain BM25.
> Production systems may combine lexical scores with field weights, phrase and proximity boosts, citations, recency, resource type or peer-review status, and may rerank a shortlist later.
> “Relevance” or “Best Match” therefore names an ordering, not a formula.

The two-control pattern is not the only one.
Chapter 4 will show another valid architecture—BM25 retrieving and ranking candidates directly, without a strict Boolean `AND` gate.

### An introduction to BM25 {#an-introduction-to-bm25}

**BM25 is a lexical scoring function: it ranks documents by adding up weighted evidence from the analysed terms they share with the query.** The record with the highest total score ranks first, so a record matching one rare query term can outrank one matching several common terms.

BM25 is the default text-scoring model in Apache Lucene, and therefore in Elasticsearch, Solr and OpenSearch—the engines beneath a large share of the search tools libraries license.
It remains the standard baseline that newer retrieval methods are still measured against.[^lucene-family]

If you have met **TF-IDF**, you already know BM25’s central intuition: a matching word is evidence, and a rare word is stronger evidence than one that appears throughout the collection.
The word `delulu` matching tells you far more than the word `the` matching.
Like TF-IDF, BM25 can only see terms the query and the document share.
Unlike strict Boolean, it does not stop at yes-or-no.
Every match contributes to a graded score, and the grades are what produce the ranking.
Historically, BM25 developed within the probabilistic relevance tradition, independently of TF-IDF, although the two use some similar signals.[^bm25-probability]

> BM25 combines weighted term matches into a score used to rank candidates.
> The score is neither a probability of [relevance](#distinction-match-relevance) nor a direct judgement of whether the record meets the reader’s need.

In simplified form, BM25 adds a contribution for each matching query term.
Each contribution is built from four observable things—whether the term occurs, how rare it is, how often it appears and how long the document is—which amount to four questions:

1. **Did the term match at all?** A term that does not appear in the document contributes nothing.
2. **How rare is the term in the collection?** A term found in relatively few documents usually contributes more (higher score) than one found almost everywhere.
   This is inverse document frequency.[^bm25-idf]
3. **How often does it occur in the document, with diminishing returns?** Repeated occurrences provide more evidence that the document concerns the term, but each additional occurrence adds progressively less evidence.
   Seeing `delulu` twice may be more informative than seeing it once.
   Seeing\ `delulu`\ 100 times does not make a document 100 times more relevant.
   How quickly the extra evidence levels off—*term saturation*—is controlled in BM25 by a parameter conventionally written *k*~1~.[^bm25-query-frequency]
4. **Is that frequency unusually high given the document’s length?** Five occurrences in a short abstract may be stronger evidence (higher score) than five occurrences in a very long document.
   This is document-length normalisation and, like term saturation, the strength of this normalisation is controlled by a second parameter, conventionally written *b*.

None of these four ideas is exclusive to BM25—TF-IDF variants can use all of them.
BM25 specifies a particular way to combine term-frequency saturation with document-length normalisation.
Typical defaults are *k*~1~\ =\ 1.2 and *b*\ =\ 0.75, the values used in [Appendix C’s worked example](#how-bm25-actually-uses-the-posting-lists).

:::: {.figure .worked-figure key="bm25-four-questions"}
The four questions BM25 asks about each matching term

::: {.include src="figures/bm25-four-questions.html"}
:::

::: caption
BM25 adds the contributions of matching query terms.
Repetition saturates through *k*~1~; document length moderates the contribution through *b*.
The plot has linear axes and shows the term-frequency factor, not a probability of relevance.
:::
::::

:::: {.figure key="idf-rewards-rare-terms"}
Rare query terms contribute stronger lexical evidence through IDF

![Infographic comparing a rare and a common query term in a ten-document collection. Left, the rare term delulu appears in 2 of 10 documents and has higher IDF; a long bar labels a delulu match as stronger evidence. Right, the common term job appears in 9 of 10 documents and has lower IDF; a short bar labels a job match as weaker evidence. Text reads: rare terms usually contribute more to the BM25 score than very common terms; IDF rewards informative terms, not just matching terms.](images/03%20BM25%20-%20words%20as%20weighted%20clues/ChatGPT%20Image%20Jul%2026,%202026,%2009_33_13%20PM.png){width="1448" height="1086"}

::: caption
In this illustrative ten-document collection, `delulu` occurs in two records and `job` in nine.
The rarer term has higher IDF; all else equal, a match contributes more.
“Informative” here means discriminating between documents, not guaranteed usefulness for the reader’s need.
:::
::::

> **Try it:** [The BM25 Evidence Lab](bm25-evidence-lab.html) lets you change one source of evidence at a time — term rarity, repetition, document length — and watch a six-record ranking respond.
> Allow about five minutes for an initial exploration or fifteen minutes for the full seven-step guided tour, before discussion.
> No prior knowledge of the equation is needed.

This description uses the standard single-field form of BM25 as a simplifying reference; related variants adapt it to structured records and very long documents.[^bm25-variants]

::: {.common-confusion label="IR terminology"}
#### Best-match retrieval: rank by degree of match {#best-match-retrieval}

Traditional **best-match retrieval** assigns graded scores and orders candidates by estimated relevance.
A document can score usefully without every query term being compulsory. **Partial-match retrieval** is another historical name in this contrast; “partial” concerns how much query evidence is matched, not matching part of a word.

Best-match retrieval can be entirely lexical.
BM25 accumulates graded evidence from matches between analysed query and document terms.
Exact matches at the term level can therefore support best-match retrieval at the document level.
No embeddings or neural model are required.

The approaches can also be combined: Boolean conditions select an eligible set, then BM25 or another ranker orders it.
Hard filters still apply.
“Best” means highest under the scoring rule, not guaranteed relevance or complete coverage. [Chapter 4](#lexical-search-does-not-have-to-mean-boolean-search) separates admission, ranking and output limits using one example.

PubMed’s capitalised *Best Match* is a product label; the generic term names a retrieval approach.
The historical [EAGLES survey](https://www.ilc.cnr.it/EAGLES96/rep2/node32.html) describes Boolean and best-match retrieval; [Arampatzis and colleagues (2007)](https://trec.nist.gov/pubs/trec16/papers/uamsterdam-derijke.legal.final.pdf) examine combinations of Boolean and ranked retrieval.
:::

### BM25 and lexical ranking in academic search {#bm25-and-lexical-ranking-in-academic-search}

Academic search products document lexical evidence in their live ranking today, and one of them names BM25 directly.

:::: {.figure .worked-figure key="bm25-academic-search"}
BM25 and lexical ranking in academic search

::: {.include src="figures/bm25-academic-search.html"}
:::

::: caption
Three scholarly products describe ranking built on lexical evidence.
Each card summarises the product’s own documentation, cited in the text below; a production ranking pipeline should not be reduced to one formula.
:::
::::

[PubMed offers an unusually clear documented BM25 example](https://pmc.ncbi.nlm.nih.gov/articles/PMC6112631/).
Its published [multi-stage architecture](#why-search-systems-use-multiple-stages) for Best Match first retrieves and orders matching records with BM25, then uses LambdaMART[^lambdamart] to rerank the top 500.
PubMed’s current help still describes a weighted term-frequency stage followed by machine-learning reranking.
It therefore shows both BM25’s continuing role and why a production ranking pipeline should not be reduced to one formula.

Two product descriptions show how lexical evidence is usually embedded in richer ranking. [Scopus describes term frequency and inverse document frequency](https://service.elsevier.com/app/answers/detail/a_id/14182/supporthub/scopus/) alongside field, position and proximity signals. [Primo’s Central Discovery Index](<https://knowledge.exlibrisgroup.com/Primo/Content_Corner/Central_Discovery_Index/Documentation_and_Training/Documentation_and_Training_(English)/CDI_-_The_Central_Discovery_Index/080Search_and_Ranking_in_CDI>) combines field and rare-term weighting, term frequency, field length, phrase and proximity boosts with static signals such as resource type, recency, peer-review status and citations.

:::: {.figure key="primo-cdi-ranking-signals"}
One discovery index documents its ranking signals

![Primo Central Discovery Index documentation describing its ranking signals](images/04%20Lexical%20search%20does%20not%20have%20to%20mean%20Boolean%20search/primocdi.png){width="1448" height="1086"}

::: caption
Field and rare-term weighting, term frequency, field length, phrase and proximity boosts, combined with static signals such as resource type, recency, peer-review status and citations.
Vendor screenshot, reproduced for comment.
:::
::::

Only the PubMed example identifies BM25 directly.
The Scopus and Primo descriptions establish that lexical evidence is active in current academic search, but not that either user-facing ranking is plain BM25.[^lucene-family-examples]

### How BM25 uses the same inverted index {#how-bm25-uses-the-same-inverted-index}

The earlier Boolean explanation introduced the [dictionary and posting lists](#from-analysed-tokens-to-a-term-first-map) as a term-to-document map.
BM25 can use the same structure. [Boolean operators treat postings mainly as sets](#boolean-treats-postings-as-sets); BM25 uses term frequency, document frequency and document length to calculate graded scores.

:::: {.figure key="boolean-then-bm25"}
A common two-stage pattern: Boolean eligibility, then BM25 ranking

![Five-step flow diagram. Step 1, all indexed records: a pool of records tagged with terms such as delulu, job, interview, expectations, unrealistic and foolish. Step 2, Boolean eligibility filter: a gate for the query delulu AND job admits only records carrying both terms. Records with only one of them, or with neither, are excluded; an example record tagged delulu and interview fails the AND condition and never reaches ranking. Step 3, eligible result set: the records containing both delulu and job. Step 4, BM25 or relevance ranking: a ranking engine gives each eligible record a score. Step 5, ordered results: the records listed by descending illustrative score, from 2.13 to 0.65. Text reads: ranking orders only the records that got through; a record excluded by Boolean cannot be rescued by ranking.](images/02%20Boolean%20search%20-%20words%20as%20admission%20rules/ChatGPT%20Image%20Jul%2026,%202026,%2009_49_01%20PM.png){width="1448" height="1086"}

::: caption
In this common academic-search arrangement, a Boolean expression restricts which records may proceed and BM25 ranks the survivors.
Both controls use the same inverted index.
BM25 can also retrieve directly, as Chapter 4 explains.
:::
::::

In this two-stage arrangement, query processing has five conceptual steps:

1. **Look up each analysed query term.** The dictionary points to the corresponding posting lists.
2. **Gather the eligible records.** Boolean operations over those posting lists determine which records satisfy the query.
3. **Obtain the scoring evidence.** Postings can supply within-document term frequency, the dictionary supplies document frequency, and document metadata supplies length.
4. **Add the contributions.** BM25 combines the evidence for each matching query term into a document score.
5. **Choose the output boundary.** The engine may completely order the scored candidates or retain only a top-*k*.

The Boolean admission rule, BM25 scoring rule and top-*k* output boundary remain separate controls, even when a product executes them in one request.
In direct BM25 retrieval, the second step changes: the engine gathers the union of records matching any analysed query term and scores them without first enforcing a strict Boolean `AND`.

### Why the same index remains fast for ranked retrieval {#why-the-same-index-remains-fast-for-ranked-retrieval}

Selective access still matters.
The Boolean query obtains its eligible records from posting lists rather than scanning every document, and BM25 can read the scoring evidence stored with those same postings.
Ordered postings also help the engine bring together the score contributions belonging to the same document while moving forwards through the lists.

Production indexes add further engineering to store posting lists compactly and avoid unnecessary work.
Compression and blocks reduce storage and memory traffic, while score upper bounds and safe pruning can avoid scoring candidates that cannot enter the leading results.
These techniques change how efficiently the same term-to-document map is stored and traversed while preserving BM25’s term-based scoring. [Appendix C](#how-bm25-actually-uses-the-posting-lists) provides a complete worked scoring example and explains these techniques, including the pruning methods MaxScore, WAND and Block-Max WAND, in more detail.
The classic [*Introduction to Information Retrieval*](https://nlp.stanford.edu/IR-book/html/htmledition/the-term-vocabulary-and-postings-lists-1.html) provides another introduction to dictionaries, postings and basic query processing.

As a broad practical rule, lexical retrieval over an inverted index is generally fast and often less computationally demanding than dense retrieval at a similar scale.
That is not a universal benchmark result: hardware, index design, query mix and accuracy settings all matter.
The different candidate-generation machinery used for dense vectors is explained in [Chapter 7](#how-nearest-neighbour-indexing-makes-dense-retrieval-practical), after vectors and embeddings have been introduced.

:::: chapter-close
1. Best-match retrieval uses graded scores to rank candidates; it need not require every query term.
   BM25 is a lexical example.
   Exact term matches can contribute to a best-match ranking, and Boolean conditions can still restrict eligibility.
2. Rarer terms carry more weight, repeated terms saturate, and document length is normalised against the collection average, to a degree set by *b*.
3. The index does not change.
   The same posting lists that answered a Boolean query support a ranked one.
4. PubMed documents BM25 as the first stage of Best Match, and other academic systems document lexical evidence in their live ranking.

::: {.chapter-transition}
Chapter 4 asks what happens to a query term that is optional or matches no record, which is the question behind the first opening puzzle.
:::
::::

::: self-check
Two documents of the same length contain the same query term. It appears once in Document A and ten times in Document B. Does BM25 give Document B ten times as much credit? Why or why not?

:   No.
    BM25 applies term-frequency saturation: repeated occurrences add evidence, but each additional occurrence contributes progressively less than the previous one.
    Ten occurrences therefore do not produce ten times the contribution of one occurrence.

The same query term appears five times in a short abstract and five times in a much longer document. Under BM25, should those five occurrences contribute the same amount? Why or why not?

:   Usually no.
    BM25 normalises term frequency by document length, so five occurrences in a short document will generally provide stronger evidence than five occurrences in a much longer one.
    How strongly length matters depends on the setting of the parameter *b*; if length normalisation is turned off, document length has no effect.

A database says it uses BM25 for relevance ranking. What does that tell you about how the eligible records are ranked, and what remains unknown?

:   It tells you that matching records receive graded lexical scores based on matching analysed terms, with rarer terms contributing more, repeated occurrences showing diminishing returns, and document length affecting the contribution.
    It does not tell you the *k*~1~ and *b* settings, how different fields are weighted, what phrase, proximity or other ranking signals are added, or whether a later stage reranks the results.

BM25 scores exact matches between analysed terms. Does that prevent it from being a best-match method?

:   No.
    Term-level matches supply graded evidence for ranking documents.
    Best-match retrieval can be lexical, and Boolean filters can still restrict which records receive those scores.
:::

[^lucene-family]: **Apache Lucene** is a lower-level Java search library that provides indexing, text analysis, query processing and ranking components. **Elasticsearch**, **Apache Solr** and **OpenSearch** are separate, higher-level search servers or distributed search engines built on Lucene.
    They add facilities such as HTTP APIs, schemas or mappings, clustering, replication, faceting, aggregations and operational management.
    Their current documentation identifies BM25 as the default text similarity, although developers can tune or replace it: see the documentation for [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html), [Solr](https://solr.apache.org/guide/solr/latest/indexing-guide/similarity.html) and [OpenSearch](https://docs.opensearch.org/latest/field-types/mapping-parameters/similarity/).
    Knowing that a product uses one of these platforms therefore shows that BM25 is available in its technical lineage; it does not prove that the final ranking is unmodified BM25.
    Field boosts, query rewriting, static signals, vector retrieval and reranking may all alter the order shown to users.

[^bm25-probability]: Calling BM25 a **probabilistic relevance model** does not mean that its final score is a calibrated probability of relevance.
    Its origins lie in the Probability Ranking Principle: documents should be ranked in decreasing order of their estimated probability of relevance to the information need.
    The earlier Binary Independence Model used binary term-presence features and derived query-term weights from the odds that a term occurred in relevant rather than non-relevant documents.
    When relevance judgements were unavailable, collection statistics produced the Robertson–Spärck Jones form of inverse document frequency.
    BM25 extended this framework with graded document term frequency, saturation and length normalisation.
    It is best understood as a practical ranking function derived from a probabilistic theory, not a model that directly outputs reliable relevance probabilities.

[^bm25-idf]: There is no universal BM25 inverse-document-frequency formula.
    A classic Robertson–Spärck Jones form, when relevance judgements are unavailable, is:

    $$
    \log\left(\frac{N-df+0.5}{df+0.5}\right)
    $$

    where $N$ is the number of documents and $df$ is the number containing the term.
    This value becomes negative when a term occurs in more than half the collection.
    Implementations respond differently. [Apache Lucene](https://lucene.apache.org/core/10_1_0/core/org/apache/lucene/search/similarities/BM25Similarity.html), for example, uses:

    $$
    \log\left(1+\frac{N-df+0.5}{df+0.5}\right),
    $$

    which remains positive.
    Other implementations use different smoothing, flooring or IDF variants.
    Two systems described as using BM25 can therefore produce different rankings even before differences in tokenisation, fields, $k_1$ or $b$ are considered.

[^bm25-query-frequency]: The saturation described in the main text refers primarily to document term frequency.
    Some fuller BM25 formulations also include a separate query term-frequency factor:

    $$
    \frac{(k_3+1)qtf}{k_3+qtf},
    $$

    where $qtf$ is the number of times the term occurs in the query.
    Like $k_1$, $k_3$ creates saturation: repeating a query term can increase its weight, but the increase eventually tails off.
    In practice, $k_3$ is rarely exposed to users, and many contemporary implementations omit this factor or effectively treat each distinct query term once.
    This usually matters little for short queries, but may matter more for verbose or automatically generated queries containing repeated terms.

[^bm25-variants]: **BM25 is better understood as a family of related scoring functions than as one immutable formula.** [BM25F](https://doi.org/10.1145/1031171.1031181) adapts it to structured documents by combining differently weighted term-frequency evidence from fields such as title, abstract and keywords before applying BM25’s non-linear saturation.
    This is particularly relevant to scholarly and book search: [one experiment](https://doi.org/10.1007/978-3-540-78646-7_23) adapted BM25F to 10,000 digitised books using book-specific fields, while [biomedical full-text research](https://doi.org/10.1016/j.jbi.2022.104211) has evaluated it across article sections such as abstracts, methods, results and discussions. [BM25L](https://doi.org/10.1145/2009916.2010070) shifts length-normalised term frequency, and [BM25+](https://doi.org/10.1145/2063576.2063584) introduces a lower bound, in both cases seeking to reduce the over-penalisation of very long documents.
    These variants preserve the central point made here: they remain lexical ranking models driven principally by shared indexed terms.

[^lambdamart]: **LambdaMART** is a supervised learning-to-rank method based on boosted regression trees.
    It learns how to combine query–document features to improve the ordering of a candidate list; in this architecture, it can only reorder the 500 records supplied by BM25. [Chapter 9](#why-search-systems-use-multiple-stages)’s explanation of multi-stage search pipelines describes this shortlist principle, and [Appendix E](#appendix-learning-to-rank) introduces learning to rank more generally.
    The pointwise, pairwise and listwise labels in [Chapter 9’s LLM section](#llms-as-rerankers) describe reranking formulations rather than LambdaMART’s implementation.
    See Burges (2010).

[^lucene-family-examples]: Three examples make the boundary concrete. [Ex Libris documents Apache Solr alongside Cassandra for its Central Discovery Index](https://knowledge.exlibrisgroup.com/Summon/Content_Corner/Product_Documentation/CDI_Frequently_Asked_Questions_for_Summon_Customers); [Scite’s API documentation describes searches against a Scite Elasticsearch index](https://api.scite.ai/docs); and the open-source [Blacklight discovery interface uses Apache Solr as its index and search backend](https://workshop.projectblacklight.org/v7.11.1/solr/).
    These examples establish Lucene-family infrastructure and the availability of BM25-style lexical scoring, not the particular field weights, query processing, additional signals or later reranking that determine a user-facing order.
