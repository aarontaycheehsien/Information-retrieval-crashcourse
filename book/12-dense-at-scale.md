---
key: "dense-at-scale"
kind: "chapter"
eyebrow: "Chapter 7"
meta: "About 18 min"
question: "What does it take to search a whole collection by vector, and where does the result list stop?"
---

## Dense retrieval at collection scale {#dense-at-scale}

::: {.stage-map on="first-stage"}
:::

::: chapter-orient
The previous chapter ended with an encoder that can turn a query or a passage into a vector—one trained so that promising candidates land nearby.
Something has to hold hundreds of millions of those vectors, compare a query against them fast enough to be worth using, and decide where the result list stops.

This chapter covers how vectors are stored and compared, how nearest-neighbour indexing keeps the comparison affordable, and what a top-*k* boundary is and is not.
Along the way it resolves the first of the two distinctions Part I left open: semantic search is not synonymous with dense retrieval.
Chapter 8 examines sparse and dense representations, including vectors calculated without learning.
:::

### Single-vector dense retrieval: compress first, compare later {#single-vector-dense-retrieval-compress-first-compare-later}

A conventional dense bi-encoder uses a query encoder and a document or passage encoder.
They may share weights or use distinct parameter sets; either way, they are normally trained jointly on the retrieval objective. [Dense Passage Retrieval](https://aclanthology.org/2020.emnlp-main.550/) is a well-known example of this dual-encoder pattern.[^bi-encoder]

Each indexed unit is encoded without seeing the query, so its vector can be calculated in advance and stored.
At search time, the system encodes the query and needs a rule for comparing that vector with the stored ones.
The comparison may be exhaustive, or a large collection may use an approximate nearest-neighbour index to reduce the work.

::: {#vector-similarity-explained}
Begin with a toy space that has only two unnamed dimensions, so it can be drawn on a page.
The query becomes an arrow, and each candidate becomes another arrow from the same starting point.
One candidate points in nearly the same direction as the query; another turns further away. **Similarity** here simply means a numerical comparison rule that gives a higher score to the relationship it treats as more alike.
:::

**Cosine similarity** is one common rule.
It compares the angle between two arrows: a smaller angle means greater directional alignment.
Their lengths do not matter.
Arrows pointing in the same direction have cosine similarity 1, perpendicular arrows have 0, and angles greater than 90° produce negative values, reaching −1 for exactly opposite directions.

**Dot product** is another common rule.
It multiplies matching coordinates and adds the results.
Direction still matters, but unless the vectors have first been normalised, their lengths matter too: a longer candidate can outscore one that is better aligned.
If the query and candidates are all normalised to length one, dot product and cosine similarity become numerically identical and give the same ranking.[^vector-similarity] Which rule applies is not a free choice: a model can learn to use magnitude, so a production system’s comparison rule should match the one its encoder was trained with.

:::: {.figure key="vector-similarity-two-rules"}
The same vectors can rank differently under cosine and dot product

![Two panels compare the same four off-axis vectors. Under cosine similarity, the better-aligned Candidate A ranks above the longer Candidate B. Under unnormalised dot product, B's greater length lets it narrowly overtake A. Candidate C has a negative score under both rules.](images/07%20Single-vector%20dense%20retrieval%20-%20compress%20first,%20compare%20later/vector-similarity-two-rules.png){width="1536" height="1024"}

::: caption
Cosine uses directional alignment, so A ranks first.
Unnormalised dot product also responds to length, so the longer B overtakes A—narrowly at the length drawn here; the [Vector Similarity Lab](vector-similarity-lab.html)’s guided tour lengthens B further so the reversal is unmistakable.
None of these values is a relevance probability.
:::
::::

Adding a third coordinate turns a two-number vector `[x, y]` into a three-number vector `[x, y, z]`.
The same comparisons still work.
Real text embeddings may have hundreds or thousands of coordinates and cannot be drawn directly, but cosine and dot product extend without needing a new idea: they apply the same operation across more matching coordinate pairs.

:::: {.figure key="vector-dimensions"}
From a drawable two-dimensional vector to many dimensions

![Three panels extend a vector from two coordinates, x and y, to three coordinates, x, y and z, and then to an n-coordinate list. The same cosine and dot-product comparison rules apply at every dimension. A caution notes that the drawn axes are anonymous toy coordinates, not semantic labels or a projection of a real embedding.](images/07%20Single-vector%20dense%20retrieval%20-%20compress%20first,%20compare%20later/vector-dimensions-from-2d-to-n.png){width="1693" height="929"}

::: caption
Adding coordinates extends the same pattern from `[x, y]` to `[x, y, z]` and then to an *n*-coordinate embedding.
The axes are anonymous toy coordinates rather than interpretable semantic labels.
:::
::::

Interpret a similarity score using the model and comparison rule that produced it.
The score is not a calibrated probability that a record is relevant, and scores from different models or searches need not be comparable.
Like the [ranked retrieval introduced in Chapter 3](#bm25-ranking), dense retrieval assigns candidates scores and orders them; what changes is where those scores come from.
The [Vector Similarity Lab](vector-similarity-lab.html) begins with the two-dimensional toy and lets you watch each step of the comparison.

::: {#distinction-semantic-dense .key-distinction-label}
Key distinction
:::

### Semantic search is a goal, not an architecture {#semantic-search-is-a-goal-not-an-architecture}

**Semantic describes what the search is trying to achieve: matching by meaning rather than only literal words.
It is usually contrasted with lexical search, which draws matching evidence from words or character sequences, through direct matching or analysed index terms.
BM25, ontology or query expansion, dense retrieval and neural reranking describe mechanisms a system might combine in trying to achieve the semantic goal.**

**“Semantic search” is not another name for “dense retrieval”.
Dense retrieval over vector embeddings is one technical approach to semantic search—the most familiar contemporary implementation of the goal, and very popular as of the mid-2020s.** Natural-language input does not imply dense retrieval either: it tells us what the search box accepts, not how a retrieval stage builds its candidates.

That popularity is why *semantic search*, *dense retrieval*, *vector search* and *embedding search* are often used as if they were synonyms.
They are not: *semantic* names an intended capability, *dense* describes the shape of a representation, *vector* names a kind of representation, and *embedding* names a learnt mapping into a vector space or, by shorthand, the vector it produces.

Those mechanisms do not contribute in the same way.
BM25 by itself remains lexical, but it may supply candidates that a meaning-aware model later reranks.
An ontology can add controlled concepts, synonyms and relationships to a lexical query.
A dense retriever can compare learnt representations without requiring word overlap.
A neural reranker can make a richer semantic comparison only after an earlier stage has retrieved a shortlist.
A product may use one or several of these arrangements.
The label *semantic* does not identify which of these components the product uses or at which stage.

**Semantic similarity is [not relevance](#distinction-match-relevance).** A document can express meaning very similar to the query and still be unsuitable for the user’s task, context or inclusion criteria.

:::: {.figure .worked-figure key="semantic-three-routes"}
One semantic goal, three possible routes

::: {.include src="figures/semantic-three-routes.html"}
:::

::: caption
These are possible mechanisms, not guaranteed matches.
In route 3, expansion supplies the lexical bridge: a reranker cannot rescue a document that never entered its shortlist.
Similar meaning alone does not establish relevance.
:::
::::

### What dense retrieval gains—and compresses {#what-dense-retrieval-gains-and-compresses}

:::: {.figure key="bi-encoder-pipeline"}
The bi-encoder pipeline: encode independently, then compare vectors

![The bi-encoder retrieval pipeline: encode independently, then compare vectors](images/07%20Single-vector%20dense%20retrieval%20-%20compress%20first,%20compare%20later/ChatGPT%20Image%20Jul%2026,%202026,%2009_42_53%20PM.png){width="1448" height="1086"}

::: caption
At search time only the query is encoded, then compared with the vectors stored in advance.
:::
::::

The benefit is vocabulary bridging.
A suitably trained model may place:

> Am I being delulu about getting this job?

near:

> How to recognise unrealistic expectations during a job search

even though the important expressions do not overlap lexically.

:::: {.figure key="dense-vocabulary-bridging"}
Dense retrieval can bridge different phrasings without lexical overlap

![Dense retrieval can bridge different phrasings without lexical overlap](images/07%20Single-vector%20dense%20retrieval%20-%20compress%20first,%20compare%20later/ChatGPT%20Image%20Jul%2026,%202026,%2009_44_11%20PM.png){width="1448" height="1086"}

::: caption
A suitably trained model can place a question near a passage that answers it even when the important expressions share no words.
:::
::::

A single-vector bi-encoder compresses each passage into one vector before the incoming query is known.
Details important to a particular query may therefore be poorly preserved.
Shorter chunks reduce that compression, but each chunk is still represented by one pooled vector.
Independent encoding therefore creates an information bottleneck as well as making precomputation possible: broad similarity may dominate a small but decisive detail, so a model can recover the general meaning while blurring an exact code, a rare name, a negation or the difference between a question and its opposite.

:::: {.figure key="single-vector-bottleneck"}
The compression bottleneck in single-vector dense retrieval

![The compression bottleneck in single-vector dense retrieval](images/07%20Single-vector%20dense%20retrieval%20-%20compress%20first,%20compare%20later/ChatGPT%20Image%20Jul%2026,%202026,%2009_44_01%20PM.png){width="1448" height="1086"}

::: caption
One vector must stand for everything in the passage, so broad similarity can dominate an exact code, a rare name or a negation.
:::
::::

### How nearest-neighbour indexing makes dense retrieval practical {#how-nearest-neighbour-indexing-makes-dense-retrieval-practical}

Chapters 2 to 4 separated [Boolean eligibility](#strict-boolean-search-words-as-admission-rules) from [direct BM25 candidate retrieval](#lexical-search-does-not-have-to-mean-boolean-search).
In both routes, an inverted index can jump from analysed query terms to matching records without scanning the complete collection.

A dense embedding does not provide an equivalent term-to-document pointer.
Most vector dimensions are active, the dimensions do not correspond directly to recognisable words, and a relevant document need not share any query term.
There is therefore no posting list for `delulu` that can directly identify all vectors expressing unrealistic expectations.

The exact baseline is a **flat** or **exhaustive** vector search: compare the query vector with every stored document or passage vector.
The engine can then construct a complete ranking or select only the leaders.
This route is exact, but its work grows with the collection size and vector dimensionality.
Here, exact means finding the true leaders under the vector comparison rule; it is separate from [exact-match retrieval](#exact-match-retrieval) in the Boolean sense.

At scale, dense-retrieval systems typically use an **approximate nearest-neighbour** index, or **ANN**, to reduce the number of comparisons.
Rather than examining every vector, an ANN structure searches promising regions or navigates through selected neighbours. [HNSW](https://doi.org/10.1109/TPAMI.2018.2889473), which organises vectors as a navigable multi-layer graph, is one widely used example.
Other approaches partition the vector space, compress vectors or combine several strategies.
ANN changes how the engine searches and may miss a true nearest neighbour; it does not define the number of results returned.

:::: {.figure .worked-figure key="ann-worked"}
The same requested top three, different search effort

::: {.include src="figures/ann-worked.html"}
:::

::: caption
Exact means exact under the chosen similarity rule, not guaranteed relevance.
This toy run illustrates a possible miss; it does not simulate HNSW or imply that ANN always misses a neighbour.
Real embeddings have many more dimensions.
:::
::::

### Candidate boundaries in lexical and dense retrieval {#candidate-boundaries-in-lexical-and-dense-retrieval}

A candidate boundary decides who can receive a score.
Strict Boolean admits only records satisfying its processed conditions; direct [BM25](#bm25-words-as-weighted-clues) normally requires at least one analysed-term match.
In the inverted-index implementations described here, both use posting lists, although either candidate set can still be very large.[^relatively-cheap-does-not-mean-costless-the-work]

Dense retrieval has no comparable term-match floor.
Unless a filter narrows the collection, every stored vector can receive a similarity score.
Even an unrelated document will be nearest if everything else is farther away.

::: pull-quote
> Nearest means best available, not necessarily relevant.
:::

::: {.question-callout label="Reasonable question"}
#### Why not return everything above a similarity score? {#dense-range-search-question-title}

A [range search](https://github.com/facebookresearch/faiss/wiki/Special-operations-on-indexes) can return vectors above a threshold.
The difficulty is calibration: similarity scores vary across queries, models and collections, so one threshold may return nothing for one query and thousands for another.
A fixed number of leaders gives a predictable output size.
:::

::: pull-quote
> With an inverted index, lexical retrieval can jump from a term to its matching documents. [Direct text scanning](#grep-searching-text-directly) finds lexical matches without those pointers.
> Dense retrieval searches for nearby vectors.
:::

The inverted index of [Chapter 2](#how-boolean-search-uses-an-inverted-index) and a dense-vector index provide two different routes to a candidate set:

| Indexed lexical route | Dense-vector route |
|---|---|
| Analyse the query into indexed terms. | Encode the query as a dense vector. |
| Follow each term to its posting list in an inverted index. | Use flat comparison or a nearest-neighbour index to search the stored vectors. |
| Strict Boolean requires its hard conditions; direct BM25 normally requires at least one analysed-term match. | Unless metadata or other filters narrow the candidates, every stored vector can receive a similarity score; flat search examines all, while ANN searches selected regions or neighbours. |
| Boolean alone supplies no ranking score; BM25 and related rankers use term-match evidence. | Vector similarity provides the initial retrieval score. |
| The output may be a Boolean eligible set, a complete lexical ranking or a lexical top-*k*. | The output may be a complete flat ranking, a thresholded range or a dense top-*k*. |

: How the candidate set is bounded on the indexed lexical route and on the dense-vector route.

This is a comparison between **indexing and retrieval routes**, not necessarily between two mutually exclusive kinds of product.
A product described as a **vector database** may store dense vectors and provide a nearest-neighbour index, but it may also support metadata filters, lexical fields or an inverted index.
Likewise, contemporary search engines can combine lexical and vector retrieval: both [Elastic](https://www.elastic.co/docs/solutions/search/hybrid-search) and [Weaviate](https://docs.weaviate.io/weaviate/search/hybrid) document hybrid search that combines keyword or full-text evidence with vector evidence.

::: {#distinction-top-k .key-distinction-label}
Key distinction
:::

### Top-*k*: complete rankings are possible—but often unnecessary {#top-k-is-a-result-boundary-not-a-dense-retrieval-method}

Information retrieval uses *k* for the requested number of leaders.
A **top-*k* request** asks for the *k* highest-scoring candidates rather than a complete ordering.
Ten highest BM25 scores and ten nearest vectors both have *k* = 10; only the scoring evidence differs.

Top-*k* is therefore an **output boundary**, not a retrieval method.
It is separate from the admission rule that forms the candidate set and from the ranking function that scores it.

Nor does top-*k* mean that only *k* candidates were examined.
An exhaustive method may score every candidate while retaining only the current leaders.
Exact BM25 pruning can safely skip candidates that cannot enter the leaders, while approximate nearest-neighbour search may inspect only part of the vector collection and miss a true neighbour.
Exactness is another independent choice; [Appendix C](#for-awareness-maxscore-wand-and-block-max-pruning) explains exact lexical pruning.

Visible counts and cut-offs reveal little about that execution.
Google Scholar’s 1,000-result display limit does not prove that the interface shows an exhaustively ranked global top 1,000.[^it-is-not-a-guarantee-that-every-match-has-been-] In multi-stage systems, different values of *k* can govern different transitions: [Chapter 9](#reranking-in-two-documented-academic-pipelines) shows a 30-record reranker budget and a five-abstract generation budget in Primo Research Assistant.

**A top-*k* result can be Boolean-filtered, lexical, dense or hybrid, and exact or approximate. *k* says how many leaders were requested.
It does not say which records could compete, how scores were calculated or how much work was done.**

### Returning to Puzzle 3: why did the keyword query retrieve more? {#returning-to-puzzle-three-why-did-the-keyword-query-retrieve-more}

*Semantic Scholar* sounds as though it searches by meaning, perhaps through dense retrieval, yet in August 2026 the question `Is there an open access citation advantage` returned only 13 results—far fewer than the dozens to hundreds of relevant studies on this established topic—while the keyword query `open access citation advantage` returned about 35,300.
Inspection of the leading results also favoured the keyword query.
Why did the more natural query perform worse?

The strongest architectural clue comes from Semantic Scholar’s documented 2025 main relevance-search pipeline:

> **Semantic Scholar’s documented main relevance search (2025)**\
> query → Elasticsearch keyword retrieval over titles, abstracts and author names → up to 1,000 candidates → LightGBM reranking

**The product name and natural-language-looking search box do not establish dense first-stage retrieval.** The living technical account, revised 25 April 2025, documents lexical first-stage retrieval rather than embedding-based first-stage retrieval in this pipeline.[^semantic-scholar-goal-architecture] On a lexical route, conversational words such as `is there an` may affect query analysis or execution, whereas the shorter query concentrates the vocabulary likely to occur in titles and abstracts.
Depending on rules that the result screen does not expose, those extra words could narrow or otherwise alter the candidate set.

The 2025 account documents keyword candidate retrieval, but it does not establish how the August 2026 interface processed these two queries.
The inspected results support a judgement of poorer search quality for the natural-language question in this example.
They do not establish the precise mechanism, or a general rule that keywords always work better.

The platform also uses SPECTER embeddings for author disambiguation and recommendations.
Their presence elsewhere still does not tell us which mechanism forms the candidates for main relevance search or where semantic capability enters that pipeline. [Chapter 9 returns to the LightGBM stage](#why-search-systems-use-multiple-stages) once reranking is in view.

OpenAlex’s documentation describes dense first-stage retrieval for [**Alice semantic search**](https://help.openalex.org/api/semantic-search/).
OpenAlex says Alice shipped in February 2026; its current documentation describes this route:

> **OpenAlex Alice semantic search (2026)**\
> query → query embedding → comparison against stored work embeddings → nearest works by cosine similarity

OpenAlex embeds work titles and abstracts with [GTE Large EN](https://huggingface.co/thenlper/gte-large) into 1,024-dimensional vectors, embeds the query with the same model, and returns the closest works by cosine similarity.
Its [25 April 2026 Alice account](https://blog.openalex.org/q2-2026-town-hall-what-we-shipped-and-whats-next/) describes a custom Elasticsearch vector index containing 413 million embeddings, including title-only embeddings for works without abstracts.
The API treats `search`, `search.exact` and `search.semantic` as alternatives and permits only one per request, so this documented Alice route should not be relabelled as a hybrid query.

| Question | Semantic Scholar documented main search (2025) | OpenAlex Alice semantic search (2026) |
|---|---|---|
| **Candidate retrieval** | Lexical candidate retrieval | Dense-vector candidate retrieval |
| **Core comparison** | Elasticsearch keyword matching | GTE Large EN embeddings compared by similarity |
| **Ranking after retrieval** | LightGBM reranking after the candidate boundary | Cosine similarity supplies the retrieval ranking |
| **What the label reveals** | The product name does not reveal the architecture | The documentation explicitly reveals a dense architecture |

: Semantic Scholar and OpenAlex Alice place candidate retrieval on different architectural routes.

Two systems can therefore both be discussed under the broad goal of semantic search while placing semantic capability in completely different parts of the pipeline.
One begins with lexical candidates and applies a learnt ranker afterwards; the other retrieves candidates directly by dense-vector similarity.

::: pull-quote
> A natural-language input box and the label “semantic search” do not identify the retrieval method.
> To establish that, inspect how the product forms candidates and ranks them.
:::

:::: chapter-close
1. Cosine similarity and dot product assign scores to pairs of vectors; those scores do not establish whether a record meets the reader’s need.
   Cosine similarity divides out both vector lengths and ranks on direction alone; an unnormalised dot product also responds to length, so the two rules can order the same candidates differently.
2. A single-vector bi-encoder has to compress a passage before it knows what will be asked of it, which is why broad similarity can dominate a small but decisive detail.
3. Approximate nearest-neighbour search often makes dense retrieval practical at large scale, and it introduces its own effects at the candidate boundary.
4. *Semantic search* describes a goal rather than an architecture.
   BM25, ontology expansion, dense retrieval and neural reranking name mechanisms a system may combine in pursuit of it.
5. Dense retrieval assigns similarity scores and orders candidates; top-*k* sets a result boundary rather than defining a retrieval method.

::: {.chapter-transition}
Chapter 8 asks what the vectors represent and whether each indexed item is a whole document, a record or a passage.
:::
::::

::: self-check
The same query and the same two candidate vectors are compared twice. Under cosine similarity A ranks first; under an unnormalised dot product B ranks first. What changed, and what would make the two rules agree?

:   Nothing about the vectors changed—only the comparison rule.
    Cosine divides the comparison by both vector lengths, so it ranks on directional alignment alone and A’s smaller angle wins.
    An unnormalised dot product also responds to magnitude, so B can be long enough to overtake a better-aligned but shorter candidate.
    Normalising the query and every candidate to length one removes magnitude from the comparison; the two rules then give numerically identical scores and the same ranking.
    Neither ordering is a statement about relevance—both are scores produced by a rule the searcher did not choose and the interface does not usually name.

A vendor says its product provides “semantic search”. What has it told you, and what must you still ask?

:   It has stated a goal or capability claim: the search is meant to match by meaning rather than only literal words.
    It has not specified an architecture.
    Ask whether meaning enters through ontology or query expansion, learnt-sparse or dense retrieval, neural reranking, or a combination; where BM25 or another lexical stage sits; and which stage forms the candidate boundary.

A search for a rare gene identifier returns plausible but wrong near-miss compounds. Name two structural reasons that is likely under single-vector dense retrieval.

:   Dense retrieval has no term-match floor: unless a filter narrows the candidates, every stored vector can be scored, and nearest means best available rather than relevant.
    And pooling compresses a passage into one vector before it knows what will be asked, so broad similarity can dominate an exact identifier.
:::

[^bi-encoder]: A dual encoder, also called a bi-encoder, encodes the query and each indexed text unit independently.
    The encoders may share all, some or none of their parameters.
    Independent encoding allows document or passage vectors to be precomputed, making first-stage retrieval efficient.
    A conventional single-vector bi-encoder produces one pooled vector per indexed unit.
    A late-interaction model retains several independently encoded token vectors.
    A cross-encoder instead processes the query and candidate text together, permitting detailed token interactions but normally at substantially greater computational cost.

[^vector-similarity]: Dense retrieval commonly compares vectors using a dot product or cosine similarity:

    $$
    \operatorname{cos}(q,d)=\frac{q\cdot d}{\lVert q\rVert\lVert d\rVert}.
    $$

    If every vector is normalised to unit length, ranking by cosine similarity is equivalent to ranking by dot product.
    Without normalisation, vector magnitude can also influence a dot-product score.
    The similarity function is part of the training setup: the model learns a geometry suited to the score on which it is optimised.

[^relatively-cheap-does-not-mean-costless-the-work]: “Relatively cheap” does not mean costless.
    The work needed depends on the selectivity of the query, the Boolean operators used, the number of matching documents, and whether the system must count, materialise or fully sort the complete result set.
    Very broad conditions in very large academic indexes can still produce millions of matches. [CDI, for example, limits certain one-word searches by narrowing where it searches and reducing the long tail of results while retaining the highest-ranked records](https://knowledge.exlibrisgroup.com/Primo/Content_Corner/Central_Discovery_Index/Documentation_and_Training/Documentation_and_Training_%28English%29/CDI_-_The_Central_Discovery_Index/080Search_and_Ranking_in_CDI#Boolean_Operators).
    This can even cause [a broad query such as science to report fewer results than science AND neurology](https://knowledge.exlibrisgroup.com/Primo/Content_Corner/Central_Discovery_Index/Documentation_and_Training/Documentation_and_Training_%28English%29/CDI_-_The_Central_Discovery_Index/080Search_and_Ranking_in_CDI#Boolean_Operators).
    The relative cost therefore depends on the collection, query, index, hardware and guarantees required.

[^it-is-not-a-guarantee-that-every-match-has-been-]: A system can show exact counts for Boolean matches, but that does not guarantee that every match has been fully scored and placed into a single exact total order.
    Display, counting and export limits can also affect what the user sees.

[^semantic-scholar-goal-architecture]: Semantic Scholar’s documented 2025 main relevance-search endpoint did not use embeddings for first-stage retrieval, although the same platform produced SPECTER embeddings for [author disambiguation]{.b} and [recommendations]{.b}.
    Kinney and colleagues’ living technical account, revised 25 April 2025, separates the platform’s components explicitly.
    Section 4.1 describes the relevance-search endpoint as keyword matching over titles, abstracts and author names in Elasticsearch, limited to 1,000 matches and reranked by LightGBM.
    Section 3.4.4 says SPECTER and SPECTER2 paper embeddings are used for author disambiguation and recommendations and made available for other applications.
    This is evidence about the documented architecture at that date, not a guarantee that every Semantic Scholar interface or later deployment works identically.
    See “[The Semantic Scholar Open Data Platform](https://arxiv.org/abs/2301.10140).”
