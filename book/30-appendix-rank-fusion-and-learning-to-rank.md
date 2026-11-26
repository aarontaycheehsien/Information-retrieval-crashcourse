---
key: "appendix-rank-fusion-and-learning-to-rank"
kind: "appendix"
eyebrow: "Appendix E"
meta: "About 19 min · optional"
section_id: "app-E"
---

## Learning to rank, diversification and rerankers {#appendix-rank-fusion-and-learning-to-rank}

[Chapters 9](#reranking-and-hybrid) and [10](#hybrid-and-fusion) introduced four ideas that are easy to collapse into one.
Reciprocal rank fusion combines several ranked lists by a fixed rule.
Diversification chooses a result set for relevance together with novelty or aspect coverage.
Learning to rank learns from examples how signals should contribute to an ordering.
Reranking names the place in a pipeline where a shortlist is scored again.
They can occur together, but none identifies what retrieved the candidates in the first place.

This appendix develops the learning-to-rank account from the companion essay “[Learning about Learning to Rank: A Librarian’s Understanding](https://aarontay.substack.com/p/f9dddff5-e08a-4952-a65c-dd3a0b1e08e9)” and contains the method and evaluation detail that Chapters 9 and 10 deliberately leave out.
Links back to the relevant chapter sections keep the model architectures there rather than repeating them here.

### Fusion and reranking solve different problems {#appendix-fusion-and-reranking}

**Fusion** begins with two or more result lists.
Its immediate problem is how to reconcile them: the lexical route may place one paper first while the dense route omits it, and their scores may have unrelated meanings and ranges.
A fusion rule produces one shared candidate list.

**Reranking** begins after candidates have been assembled.
It examines those candidates again and assigns a new order, perhaps using a cross-encoder, an LLM or a learning-to-rank model.
A pipeline can fuse without reranking, rerank one unfused list, or fuse and then rerank.
In every case, the earlier candidate boundaries remain ceilings.

::: {#appendix-how-rrf-combines-ranked-lists .legacy-anchor}
:::

The worked explanation of reciprocal rank fusion is now in [Chapter 10](#how-reciprocal-rank-fusion-combines-ranked-lists).
The section below covers learning a ranking function from features and judgements.

### Learning to rank: learning how signals should combine {#appendix-learning-to-rank}

**Learning to rank (LTR)** is a family of supervised machine-learning methods for ordering candidates.
The compact intuition is that the designer supplies examples of better and worse results plus a set of measurable features; the model learns a ranking function that combines those feature values so its order better agrees with the training evidence.

The methods introduced earlier in the book are mainly ways to estimate **topical match**.
BM25 asks how strongly the query terms occur; dense and late-interaction models learn whether query and text belong together.
A searcher may care about other things as well: freshness in a fast-moving field, authority or quality signals, a preference for systematic reviews, language, availability, or the local importance of one collection.
Sorting by newest is a blunt response because it can place a barely relevant new record above an excellent older one.
A ranking function can instead give such preferences a smaller influence while retaining topical match as the main signal.

The features can cross the categories used elsewhere in this book:

- **Lexical evidence:** a BM25 score, the number of query terms matching the title, field matches or term proximity.
- **Document properties:** publication date, publication or resource type, language, length, usage or popularity; a scholarly system could also supply citation-based signals or availability.
- **Query properties:** query length, special characters, topic or other evidence about what kind of ranking may be useful.
- **Query–document features:** the fraction of the query matched in a title or author field, an exact phrase match, proximity, or a neural ranking score.

The actual set is system-specific. [PubMed’s documented LambdaMART example](https://doi.org/10.1371/journal.pbio.2005343) used BM25, title matches, proximity, publication year and type, past usage and other query and document features; it did *not* list citation count among them. [Other academic search products document citation and recency signals](#bm25-and-lexical-ranking-in-academic-search) in their ranking, but do not necessarily disclose whether LTR learns their influence.
“Uses machine learning” therefore does not reveal which factors were supplied, what the training labels represented or how stable the learnt balance is across disciplines.

### A toy mixture—and why raw scores cannot simply be added {#appendix-ltr-toy-mixture}

Suppose a scholarly search designer wants topical match to dominate while giving small nudges to newer and more cited work.
A deliberately simple score might be written:

::: {.equation-scroll tabindex="0" role="region" aria-label="Weighted ranking formula"}
$$
S(q,d)=0.8\,s_{\mathrm{BM25}}(q,d)+0.1\,s_{\mathrm{fresh}}(d)+0.1\,s_{\mathrm{cite}}(d)
$$
:::

The expression communicates an intention, but adding the raw inputs would be meaningless.
A BM25 score is query- and implementation-dependent, a year is around 2026, and citations range from zero to many thousands with a very long tail.
The largest numerical scale would dominate regardless of the written weights.

A production design must first transform or calibrate the features.
Freshness might use a decay such as $e^{-\lambda\,\mathrm{age}}$, so the contribution falls smoothly rather than at an arbitrary date boundary.
Citations might use $\log(1+c)$ to compress the long tail.
BM25 scores might be calibrated from their observed distribution for the queries and implementation in question; there is no universal BM25 maximum that transfers cleanly between systems or even between queries.
The resulting values can then be put on comparable ranges.

This is the same score-compatibility problem that made [RRF attractive](#how-reciprocal-rank-fusion-combines-ranked-lists): RRF avoids it by discarding raw scores and using ranks.
Score fusion or a linear LTR model retains more information, but must learn or impose a meaningful scale.

Even after scaling, choosing 0.8, 0.1 and 0.1 by hand remains a judgement.
LTR estimates the combination from training evidence.
In a linear model that may really mean learning three coefficients.
A tree-based or neural model can learn nonlinear interactions: citation count may matter differently for a six-month-old paper and a twenty-year-old one, or an exact author match may matter only for a query that looks like a person’s name.
The governing idea remains **learn the ranking function from examples instead of setting the final mixture entirely by hand.**

Learning does not remove the designer’s values.
Someone still chose the features, transformations, labels, candidate pool, metric and training population.
A recency feature that helps biomedicine may systematically work against historical research; a citation feature imports field, age and coverage effects. [Chapter 15’s governance questions](#choosing-and-governing-search-tools) apply to those choices, not just to the final model.

### Four separate choices hide inside “the model learnt to rank” {#appendix-ltr-training-choices}

LTR follows the familiar supervised-learning loop: represent an example with features, compare the model’s output with some target evidence, calculate a loss, update the model and repeat.
What differs is that the desired output is an order.
Four questions keep the pieces separate.

| Question | Typical choices | What it determines |
|---|---|---|
| **Where does supervision come from?** | Graded relevance judgements; pairwise human preferences; clicks, saves, downloads or dwell time | What behaviour or conception of relevance the system is able to learn. |
| **How is ranking formulated?** | Pointwise, pairwise or listwise examples | Whether learning treats candidates individually, as preferences between two candidates, or as a query-level list. |
| **What objective is optimised?** | Regression or classification loss; pairwise logistic or hinge loss; a listwise or metric-aware surrogate | Which mistakes training penalises, and how strongly—especially near the top of the list. |
| **What model represents the ranking function?** | Linear model; ranking SVM; boosted decision trees such as LambdaMART; neural ranker | Which relationships and feature interactions can be learnt, and the cost of training and inference. |

: Four independent design choices in a learning-to-rank system.

These choices are related but not interchangeable.
Human assessors could grade three documents 3, 2 and 0; a pointwise method could predict those grades, a pairwise method could derive $A>B$, $A>C$ and $B>C$, and a listwise method could use all three labels together.
The raw evidence has not changed.
Its formulation for learning has.

One influential web-search lineage shows why the distinctions matter. [RankNet, LambdaRank and LambdaMART](https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/) emerged from related Microsoft work from the mid-2000s onward, but the names do not describe three sizes of one model.
RankNet used a neural network and a pairwise probability loss; LambdaRank shaped pairwise training gradients according to the ranking improvement a swap would produce; LambdaMART combined those metric-aware gradients with MART boosted decision trees.
A training formulation, an objective and a model family can change independently.

### What click logs teach—and what they cannot {#appendix-ltr-clicks}

Explicit relevance judgements are expensive, which makes behavioural traces tempting.
Clicks, saves, downloads and dwell time can supply millions of observations without asking assessors to label every query–document pair.
They are not clean ground truth.

A result at rank one is more likely to be seen and clicked because it is at rank one.
Its title, snippet, access label and document type change that probability.
A user may click a lower result because they have already read the leading paper, because the lower title is intriguing, or because they are seeking related rather than topically identical work.
Logs also come from a ranking already in production, so the system mainly receives feedback about documents that the previous system chose to expose.
Training naively on that evidence can preserve a prior ranking’s blind spots in a feedback loop.

[Semantic Scholar’s 2020 engineering account](https://medium.com/ai2-blog/building-a-better-search-engine-for-semantic-scholar-ea23a0b661e7) gives an unusually concrete response.
Its team ran random position-swap experiments, estimated the propensity for a result to be clicked at each position, and weighted training examples by inverse propensity to correct for position bias.
It also removed roughly a third of query–result groups that failed plausibility filters.
Those steps reduce particular biases; they do not turn clicks into a universal relevance judgement.

Editorial labels have their own boundary: they reflect a task definition, assessors and adjudication process.
The ranker learns what the supplied evidence rewards, not relevance in the abstract.
This is why [Chapter 14’s account of relevance judgements](#relevance-is-a-judgement) applies as strongly to training data as to evaluation data.

### Why pointwise, pairwise and listwise appear twice {#appendix-ltr-objectives}

[Classical LTR groups methods](https://doi.org/10.1561/1500000016) partly by the form of the learning problem.
The labels are best understood through what an error means.

| Formulation | Training intuition | Characteristic strength and limit |
|---|---|---|
| **Pointwise** | “Get each item’s relevance right.” Treat every query–document pair as an individual classification or regression problem. | Simple and produces a score per candidate, but its loss does not directly express which document should outrank another for the same query. |
| **Pairwise** | “Put the better item above the worse one.” Penalise a model when $d_i$ should outrank $d_j$ but receives the lower score. | Directly ranking-aware, but creates many possible pairs and does not by itself value an error at ranks one and two more than the same reversal at ranks 101 and 102. |
| **Listwise** | “Get the query-level list right.” Learn from a group of candidates together, perhaps by matching a distribution over rankings or using a metric-aware surrogate. | Can align learning more closely with top-weighted list quality, but needs query-level grouping and more complex training machinery. |

: Pointwise, pairwise and listwise formulations during LTR training.

Metrics such as [nDCG, MAP and MRR](#rank-changes-the-question) evaluate an ordering, but sorting is not a straightforward differentiable function.
LTR therefore commonly optimises surrogate losses whose reduction tends to improve the desired ranking metric.
LambdaRank is an influential bridge: it constructs pairwise “lambda” gradients and weights a reversal according to how much swapping the two documents would change a measure such as nDCG. **LambdaMART** applies that idea while learning boosted decision trees.
The result is often called pairwise because its gradients concern document pairs and metric-aware because the strength of those gradients reflects list quality; the textbook categories have useful but not perfectly sealed borders.

In [Chapter 9’s LLM discussion](#llms-as-rerankers), the same three words describe how candidates are presented to a model at *inference* time: separately, in pairs or as a list.
An LLM used pairwise at inference might have been trained in some other way.
Conversely, a pairwise-trained tree ranker normally receives one completed feature vector at a time when deployed.
The vocabulary names a comparison shape, but that shape can occur during training or when a reranker is applied.

### Diversification methods and diversity-aware metrics {#appendix-diversity-aware-ranking-metrics}

[Chapter 9 introduces result diversification](#ranking-a-useful-set-not-only-relevant-items) as a change in objective: the system chooses a useful set rather than scoring every query–document relationship independently.
The classic methods differ mainly in what they must know about diversity.

#### Classic diversification methods

| Method | What it needs | How it selects | Main limitation |
|---|---|---|---|
| **[Maximal marginal relevance (MMR)](https://doi.org/10.1145/290941.291025)** | A relevance score between query and candidate, and a similarity score between candidates. | Greedily chooses the candidate that best balances query relevance against similarity to the most similar item already selected. | It has no explicit model of aspects or intents. Whatever the similarity function regards as different becomes “diversity”, and too much penalty can promote an irrelevant outlier. |
| **[IA-Select](https://doi.org/10.1145/1498759.1498766)** | Possible query intents or categories, their estimated probabilities, and how well each candidate satisfies each one. | Greedily adds the candidate with the greatest expected gain for intents not yet adequately satisfied. | The intent set, probabilities and document–intent judgements must come from somewhere. A missing or badly weighted intent cannot receive coverage. |
| **[xQuAD](https://doi.org/10.1007/978-3-642-12275-0_11)** | Possible query aspects represented as subqueries, estimates of their importance, and candidate relevance to the original query and each aspect. | Mixes general query relevance with expected coverage of aspects not already covered by the selected documents. | It can only diversify over the aspects it represents, and automatically generated subqueries may be incomplete or misleading. |
| **[Determinantal point process (DPP)](https://doi.org/10.1561/2200000044)** | A positive semidefinite kernel expressing item quality and pairwise similarity. | Models a subset jointly. High-quality sets containing dissimilar items receive greater probability because the relevant determinant is larger. | Constructing the kernel and finding the best fixed-size subset can be expensive; the matrix makes the selection less immediately interpretable than a simple relevance score. |

: Four classic diversity-aware methods, the signals they require and the behaviour they encourage.

MMR makes the intuition easiest to see.
Let *R* be the candidates, *S* the items already selected, and *d* a candidate not yet in *S*.
The next item is chosen by:

::: {.equation-scroll tag="div" tabindex="0" role="region" aria-label="Maximal marginal relevance formula"}
$$
\operatorname*{arg\,max}_{d\in R\setminus S}
\left[\lambda\,\operatorname{Rel}(d,q)
-(1-\lambda)\max_{s\in S}\operatorname{Sim}(d,s)\right]
$$
:::

With *λ* = 1, the method behaves like the original relevance ranking.
Lowering *λ* gives progressively more weight to avoiding similarity with what has already been chosen.
The equation does not say how relevance or similarity must be calculated.
They might come from BM25, embeddings, topics, metadata, citation relations or a mixture. **MMR is therefore not another name for vector search, dense retrieval or neural reranking.** Dense embeddings are one convenient way to supply its two similarities, not part of its definition.

**A worked MMR choice.** For the book’s open-access citation-advantage question, suppose three candidate papers remain under consideration.
A has the highest relevance score, 0.95, and is selected first.
B largely repeats its aspect of the question; C covers another aspect.
These are schematic candidates with stipulated scores, not reported measurements or judgements about named papers.
For this example, relevance and similarity are both on a comparable 0–1 scale; raw BM25 and cosine scores should not simply be substituted without deciding how to scale them.

::: {.table scope="row"}
| Remaining candidate | Relevance | Similarity to A | MMR at λ = 0.9 | MMR at λ = 0.5 |
|---|---|---|---|---|
| B: highly relevant, largely repeats A | 0.90 | 0.90 | 0.9 × 0.90 − 0.1 × 0.90 = **0.72** | 0.5 × 0.90 − 0.5 × 0.90 = 0.00 |
| C: relevant, covers another aspect | 0.75 | 0.20 | 0.9 × 0.75 − 0.1 × 0.20 = 0.655 | 0.5 × 0.75 − 0.5 × 0.20 = **0.275** |

: One MMR selection after paper A has been chosen.
:::

At λ = 0.9, B wins: relevance dominates.
At λ = 0.5, C wins because its lower redundancy outweighs its slightly lower relevance.
The example starts with the most relevant item because the redundancy comparison has no selected item to compare against when the set is empty.
Later choices use the maximum similarity to *any* selected item, not just A.

IA-Select and xQuAD are **explicitly aspect-aware**.
They are useful when an underspecified query may represent several intents, or when one query has several facets worth covering.
MMR is commonly called **implicit diversification** because it needs no named aspects: it treats dissimilarity itself as a proxy for novelty.
A DPP goes further towards set selection.
Instead of scoring only the next document against the current list, it defines a probability distribution over subsets in which similar items repel one another.

These methods are related to reranking, but not identical to it.
MMR, IA-Select and xQuAD are commonly applied greedily to reorder a candidate list, while a DPP can select or sample a subset jointly.
Public documentation for major academic databases rarely names one of these methods, so a diverse-looking result page is not evidence that any particular method is in production.

#### Diversity-aware evaluation

Ordinary precision, MAP and nDCG use each record’s relevance judgement without asking whether earlier records already covered the same aspect.
Two rankings containing the same relevance grades in the same positions can therefore receive the same score even if one repeats a single subtopic and the other covers five.

[**Alpha-nDCG (α-nDCG)**](https://doi.org/10.1145/1390334.1390446) rewards relevant records placed high, with progressively less gain for aspects already covered.
It adds aspect-level judgements and discounts the gain from an aspect each time it has already appeared, which suits tasks that value coverage of several known subtopics rather than repeated evidence for only one.
Intent-aware precision, ERR-IA and subtopic recall express related coverage objectives.
None can reward a diversity dimension the assessors never labelled.

### Why LTR often becomes a reranker—but does not have to {#appendix-why-ltr-becomes-a-reranker}

LTR is a way of learning an order; reranking is a position in a pipeline.
They overlap often, not necessarily.
A cheap additive score using BM25 plus precomputed document values such as freshness can sometimes be evaluated during first-stage retrieval or in a light rescore. [WAND, MaxScore and block-max methods](#for-awareness-maxscore-wand-and-block-max-pruning) exploit BM25’s sum of per-term contributions and upper bounds to avoid fully scoring candidates that cannot enter the current top *k*.
Static document features can be fetched while candidates are scored, although extra boosts need usable bounds or they weaken pruning.

A more elaborate LTR model is less naturally term-decomposable.
A boosted tree generally needs a completed feature vector before its splits can be evaluated, and the expensive part may be constructing that vector rather than adding the tree outputs.
Field-aware matches, author parsing, phrase statistics, neural scores and random access to metadata are manageable for hundreds of candidates and prohibitive for every match in a hundred-million-record corpus.
The production answer is the pipeline from [Chapter 9](#why-search-systems-use-multiple-stages): retrieve a high-recall shortlist cheaply, then spend feature and model computation on that shortlist.

The documented 2020 Semantic Scholar system makes the division visible.
The figures below describe that historical deployment, not necessarily the service now.

| Part | What the engineering account reported | What it illustrates |
|---|---|---|
| **Candidate stage** | Elasticsearch searched almost 190 million indexed papers and supplied the top 1,000. | The candidate boundary made richer comparison affordable and remained the reranker’s recall ceiling. |
| **Ranker** | A LightGBM boosted-tree ranker used a LambdaRank objective. | Modern machine-learning ranking need not use embeddings or a neural network. |
| **Features** | Twenty-two features included title, abstract and venue matching; author matches; paper age and citations; and language-model probabilities of matched or unmatched phrases. | The feature-extraction bill can dominate the model arithmetic. The team chose fast KenLM probabilities because some features called the model dozens of times. |
| **Supervision** | Click data were corrected for position propensity and filtered for noisy or implausible groups. | Behavioural evidence needs an account of exposure, interface effects and noise. |
| **Evaluation and correction** | The team built a separate 250-query, manually analysed test and added post-hoc rules for known-item patterns after the learnt model. | A held-out metric on log-like data did not settle production quality; error analysis and explicit rules remained part of the ranking system. |

: Semantic Scholar’s documented 2020 learning-to-rank pipeline, as a worked production example.

The model was trained offline.
At query time the system did not “learn again”; it calculated query-dependent feature values for the 1,000 candidates and applied the stored model.
That distinction is easy to miss when a product says its ranking happens “on the fly.”
The order is computed on the fly, while the ranking function was learnt in advance.

:::: {.figure .query-flow key="ltr-offline-online"}
What is learnt in advance, and what happens per query

::: {.track}
- **Learnt once, offline** and only redone when the model is retrained
- **Features and labels chosen** which signals are available, and what counts as a better result
- **Training** adjust the function until its order agrees with the labels
- **A stored ranking function** fixed until someone retrains it
:::

::: {.track}
- **Applied per query, online** this is the part that happens “on the fly”
- **A retriever supplies a shortlist** and sets the recall ceiling for everything after it
- **Feature values computed** for those candidates and this query, which is often the expensive part
- **The stored function scores them** producing a new order, not a new model
:::

::: caption
The two tracks run on different clocks.
Everything on the top track was settled before the query arrived, including whose judgements defined a better result; only the bottom track responds to what was typed.
A product describing its ranking as happening “on the fly” is describing the bottom track, which says nothing about when the top one was last run.
:::
::::

PubMed supplies the other documented scholarly example, and the one most librarians will actually be asked about.
Its Best Match ranking uses [BM25 to supply 500 candidates, which a LambdaMART model then reorders](#bm25-and-lexical-ranking-in-academic-search).
The division of labour is the same as Semantic Scholar’s, at half the candidate depth: a cheap lexical pass sets the ceiling, and the learnt model spends its budget inside it.
The documented feature set is worth knowing for a different reason.
It combines title matches, term proximity, publication year and type and past usage — and, as noted above, does not list citation count, which is the signal most searchers assume a scholarly ranker must be using.
A searcher who scrolls past the 500th candidate has left the reranked region entirely.
In both systems, the model’s sophistication does not relax the shortlist ceiling.
It only spends the available budget more carefully above it.

### A reranker is broader than learning to rank {#appendix-reranker-is-broader-than-ltr}

For much of production search, “reranker” has meant exactly the kind of tree-based LTR stage described above: combine lexical matches, freshness, authority, popularity, document type and other features over a shortlist.
It still can.
The term now covers a wider set of second-pass comparators.

[Cross-encoders](#cross-encoder-reranking) read the query and each candidate together; [late-interaction models](#where-colbert-style-late-interaction-fits) retain token-level representations and may retrieve or rerank; [LLM relevance judges](#llms-as-rerankers) can apply explicit criteria pointwise, pairwise or listwise.
A pipeline may use a lightweight tree ranker and then an expensive neural or LLM reranker over an even smaller set.
The unifying production pattern is:

::: pull-quote
> Retrieve cheaply → spend more computation reranking a shortlist.
:::

What makes the component a reranker is where it runs, not which model family it belongs to.
What makes a method LTR is that a ranking function was learnt from supervised examples, not that it necessarily occupies the second stage.
Keeping those definitions separate makes it possible to describe a three-stage system without calling every learnt component the same thing.

### What to ask about either method {#appendix-questions-for-fusion-and-ltr}

Include the ranking-method section of the [vendor questionnaire](vendor-questionnaire.html) to record answers to these four prompts alongside the core questions.

- []{#vendor-e01 .li-id}**Before RRF:** which retrievers supplied lists, how deep was each list, were they weighted equally, and how were duplicates handled?
- []{#vendor-e02 .li-id}**Before LTR:** which features and transformations were available, what supplied the labels, how were click and exposure biases handled, which objective and model were used, and when was it last retrained?
- []{#vendor-e03 .li-id}**Before reranking:** which retriever produced the candidates, how many reached each later stage, what text and metadata did each stage see, and what was the latency budget?
- []{#vendor-e04 .li-id}**For evaluation:** which metric and cut-off were used, did the test candidate distribution match deployment, which queries or groups worsened, and was the complete pipeline tested on this collection and user task?

The method name describes a mechanism.
The answers above describe the search system a reader will actually encounter.

---
