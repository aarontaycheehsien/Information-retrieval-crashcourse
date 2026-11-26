---
key: "hybrid-and-fusion"
kind: "chapter"
eyebrow: "Chapter 10"
meta: "About 9 min"
question: "When a system runs more than one retriever, how does it combine their results, and what information does the combination preserve or discard?"
---

## Hybrid retrieval and rank fusion {#hybrid-and-fusion}

::: {.stage-map on="fusion reranking"}
:::

::: chapter-orient
Choosing retrievers and combining their answers are separate design decisions.
A lexical route may preserve an identifier that a dense representation blurs; a dense route may recover a paraphrase that shares no useful indexed term.
The two retrievers return separate candidate lists that must be combined.
The system must still decide which routes run, how deep each list is, how duplicate records are treated, and how evidence from unlike scoring scales becomes one order.

This chapter separates *blending* from *routing*.
A blend runs prescribed routes and combines their outputs; a route chooses which path or paths to use for this query.
It then treats reciprocal rank fusion as a deliberately simple baseline: RRF uses positions rather than incompatible raw scores, rewards agreement near the top, and exposes the cut-offs and weighting choices that a label such as “hybrid search” otherwise hides.
:::

### Why hybrid retrieval remains attractive {#why-hybrid-retrieval-remains-attractive}

[Table 9.1](#tbl-9-1)’s second stage combines candidates supplied by *parallel* retrievers, which is what this chapter’s title means by **hybrid**: a system that draws on more than one retrieval method at once.
Every method needed to build one has now been described, so this is the point to ask why anyone would.

Hybrid retrieval protects against systems with different and partly complementary blind spots.

Boolean can provide explicit control.
BM25 can preserve analysed lexical term evidence, including rare identifiers.
Dense retrieval can bridge different formulations in a compact latent space.
Rerankers and other neural architectures may add further signals.
Combining lexical and dense routes can recover relevant material missed by either route alone.

**Hybrid and multi-stage are not synonyms.** In this book’s operational definition, hybrid combines candidates or scores from multiple candidate-generation routes. [Multi-stage](#why-search-systems-use-multiple-stages) means that later operations process candidates supplied by an earlier stage.
One is about combining retrieval routes; the other is about the order in which work is done.
Vendors use *hybrid* less consistently, so their architecture still has to be inspected.

A system can be hybrid, multi-stage, both or neither; Figure 10.1 works through the sequential cases.
A single scoring stage that combines lexical and dense candidate-generation scores can be hybrid without using a reranking cascade.

:::: {.figure .worked-figure key="hybrid-pipeline-comparison"}
Count the retrieval routes; then follow the stages

::: {.include src="figures/hybrid-pipeline-comparison.html"}
:::

::: caption
Candidate generation supplies records; fusion combines evidence about them; reranking reorders supplied candidates.
A single scoring stage can also blend lexical and dense evidence, as described in the text.
These examples show sequential arrangements.
:::
::::

The arrangement and the combination method both matter.
A system may merge ranked lists with **reciprocal rank fusion (RRF)**, combine normalised scores, or combine parallel retrieval with a later reranker.
Which paths run at all is a separate [routing](#common-query-understanding-techniques) decision, taken up below with two products.
RRF is a fusion rule, not a relevance model or reranker; the formula and a worked example follow.

### How reciprocal rank fusion combines ranked lists {#how-reciprocal-rank-fusion-combines-ranked-lists}

::: {.practice-callout tag="p"}
Try the [Rank Fusion Lab](rank-fusion-lab.html) alongside the worked calculation below.
Follow each record’s contribution, change the constant, and distinguish input cutoffs from output depth.
The lab uses schematic records, not relevance judgements.
:::

**Reciprocal rank fusion (RRF)** is an unsupervised rule introduced by [Cormack, Clarke and Büttcher (2009)](https://doi.org/10.1145/1571941.1572114).
It ignores the raw score produced by each retriever and uses only each record’s rank position.
For a document [d]{.var}, its fused score is:

$$
\operatorname{RRF}(d)=\sum_{r \in R}\frac{1}{c+r(d)}
$$

[R]{.var} is the set of input rankings, [r]{.var}([d]{.var}) is the position of document [d]{.var} in one ranking, and a document absent from a supplied list contributes nothing from that list.
The constant [c]{.var} softens the advantage of the very first positions; the original paper fixed it at 60 after pilot testing.
The constant can be tuned for a different collection or task.
The original paper calls this constant [k]{.var}; this book uses [c]{.var} to distinguish it from top-[k]{.var} result depth.

Suppose a lexical and a dense retriever each return three records.
With [c]{.var}\ =\ 60, the calculation is:

| Record | Lexical rank | Dense rank | RRF score | Fused rank |
|---|---|---|---|---|
| A | 1 | 2 | 1/61 + 1/62 = 0.03252 | 1 |
| C | 3 | 1 | 1/63 + 1/61 = 0.03227 | 2 |
| B | 2 | — | 1/62 = 0.01613 | 3 |
| D | — | 3 | 1/63 = 0.01587 | 4 |

: A worked reciprocal rank fusion example over two short result lists.

:::: {.figure .worked-figure key="rrf-record-journey"}
Follow the same records from two lists into one

::: {.include src="figures/rrf-record-journey.html"}
:::

::: caption
The same schematic records and calculations as Table 10.1.
Matching letters preserve record identity across the lists; teal marks records supplied by both routes and ochre marks records supplied by just one.
RRF uses positions, not raw retrieval scores.
:::
::::

A wins because both retrievers place it near the top; C follows because it is first in one list and third in the other.
Agreement is rewarded without requiring a BM25 score and a vector-similarity score to be made numerically comparable.

Once scores have become ranks, RRF cannot distinguish a narrow first–second gap from an overwhelming one.
Results below each input cutoff contribute nothing, so the depths of the supplied lists matter.
The lists also contribute equally unless the implementation adds explicit weights.
Use RRF as a baseline and compare it with the individual retrievers on representative queries.

RRF has also travelled beyond hybrid retrieval.
Elsevier’s 2024 account of Scopus AI’s “RAG Fusion” describes applying this formula—not to lexical and dense lists for one query, but to the ranked lists returned by several generated variants of the same question, before a summary is written from the merged top results.
Nothing about RRF changes when it moves inside a generative product; the composition is worked through in [Appendix G](#appendix-rag-scopus).

### Blending results and selecting retrieval routes {#two-hybrids-that-combine-differently}

The difference between blending and routing is easiest to see in two current products.

[**Web of Science Smart Search**](https://webofscience.zendesk.com/hc/en-us/articles/32587676013713-Smart-Search) **blends.** An [NLP parser first builds a structured Boolean query](#when-a-system-writes-the-boolean-query); document search can then run a Boolean keyword path and a semantic-vector path and combine their results.
This is the parallel arrangement described above.
Its query-parsing stage is not the hybrid part: parsing changed the query; the blend is what makes it hybrid.

**Scopus AI routes.** Rather than always running both paths, it can decide per question whether to search lexically, to search over vector embeddings, or to do both.
Selecting a route and combining results are separate decisions: a run that takes one path combines nothing and is not hybrid under this book’s definition.
A run that takes both still needs a fusion rule to merge what they return.
The answer to “is this a lexical search or a vector search?” may therefore differ from one query to the next.

A blend runs and combines prescribed paths; a route is a retrieval-control decision made at query time.
A rule, classifier or model may make that choice; routing alone therefore does not establish agency.

:::: chapter-close
1. Hybrid retrieval is a claim about how results are combined, not merely about containing two retrievers.
2. Blending and routing are different designs: one merges on every query, the other chooses per query.

::: {.chapter-transition}
Hybrid retrieval is not a quality guarantee.
Its result depends on the evidence each route preserves, the candidate depth allowed to each, and the rule used to combine them.
RRF combines ranks without requiring the input scores to be on the same scale, but it discards score gaps and depends on the supplied lists and their cut-offs.
Routing determines which retrievers contribute candidates for a particular query.
Chapter 11 asks how a query is interpreted, transformed and routed.
:::
::::

::: self-check
Give an example of a pipeline that is multi-stage but not hybrid, and one that is hybrid but not multi-stage.

:   BM25 followed by a cross-encoder reranker is multi-stage without being hybrid under this book’s definition: one candidate-generation route supplies a set that a later stage reorders.
    A single scoring stage that blends lexical and dense evidence is hybrid without being multi-stage.

Two products call themselves hybrid. One blends both routes on every query; the other picks a route per query. What follows for explaining an individual result?

:   With a blend, the same evidence sources contribute every time, so the explanation has a fixed shape.
    With routing, “was this a lexical or a vector search?” may have a different answer for each query — so the routing decision itself has to be exposed before any single result can be accounted for.
:::
