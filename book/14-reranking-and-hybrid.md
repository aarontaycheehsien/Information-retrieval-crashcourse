---
key: "reranking-and-hybrid"
kind: "chapter"
eyebrow: "Chapter 9"
meta: "About 21 min"
question: "How are several retrieval and ranking components assembled into a pipeline?"
legacy_anchors: ["ch5"]
---

## Reranking and multi-stage retrieval {#reranking-and-hybrid}

::: {.stage-map on="fusion reranking"}
:::

:::: chapter-orient
Many production search systems use several stages.
Comparing a query against every document in a collection rules out any expensive comparison, so real systems retrieve cheaply and broadly first, then spend computation on a shortlist small enough to afford it.

The decision to retrieve cheaply first and compare carefully later explains cross-encoders, LLM rerankers and the place of late interaction.
It also explains result diversification, which judges what a candidate adds to the items already selected.
Hybrid retrieval, which runs more than one retriever at once and must then combine what they return, is [Chapter 10](#hybrid-and-fusion)’s subject.
These ideas only become meaningful now that the first-stage methods exist.

::: {.orientation label="Before you start"}
#### Three questions about reranking {#chapter-8-orientation-title}

This chapter asks three questions about spending more computation on an existing shortlist:

1. **Why retrieve in stages at all?** A shortlist makes more expensive query–document comparisons affordable.
   It also sets [a ceiling](#why-search-systems-use-multiple-stages): reranking can reorder only the records on it.
2. **What can a second pass afford that a first cannot?** Three arrangements answer this differently: [cross-encoders](#cross-encoder-reranking), [late interaction](#where-colbert-style-late-interaction-fits) and [LLM rerankers](#llms-as-rerankers).
3. **How can a result list cover several aspects of a topic?** [Diversification](#ranking-a-useful-set-not-only-relevant-items) considers what each candidate adds to the items already selected.

The common constraint is the candidate pool: reranking changes its order but cannot add an excluded record. [Chapter 10](#why-hybrid-retrieval-remains-attractive) asks what changes when several retrievers contribute candidates.
:::
::::

### Rerankers: compare more carefully after retrieval {#rerankers-compare-more-carefully-after-retrieval}

A **reranker** is a second-pass scorer.
It does not search the collection; it receives a list of candidates that an earlier stage already retrieved and decides how they should be ordered.
Everything it can do is therefore bounded by what that earlier stage handed it.

“More carefully” means using richer evidence to make a better task-specific relevance estimate within that shortlist.
It does not mean that a later stage discovers objective or true relevance.

### Why search systems use multiple stages {#why-search-systems-use-multiple-stages}

Many production search systems are pipelines rather than one scoring formula. [Query understanding and transformation](#words-sent-to-retrieval-may-not-be-the-words-you-typed) may first interpret or rewrite the input, while retrieval control may route it.
Once retrieval begins, fast methods search the full collection, while progressively more expensive methods examine progressively fewer records.
Applying the most detailed query–document comparison to millions of records for every search would usually be too slow and costly.

| Stage | Main job | Why it belongs here |
|---|---|---|
| **First-stage candidate retrieval** | Use Boolean, BM25, dense, learnt-sparse or another indexed route to search the full collection and produce a manageable shortlist. | Speed and recall matter most: the aim is to retain as many potentially relevant records as practical without examining every record deeply. |
| **Fusion and deduplication** *(optional)* | Combine and reconcile candidates supplied by parallel lexical, dense or other retrievers. | Different routes may recover complementary records, but their lists and scores must be merged before later comparison. |
| **Reranking** | Apply a richer model to the shortlist and distinguish the strongest candidates from plausible but weaker ones. | More computation can be spent on each query–candidate pair because only a small portion of the collection remains. |
| **Display or answer generation** | Present the leading records or use selected sources to ground a generated response. | This stage works only with surviving results. Presentation or generation does not search the omitted records again. |

: The stages of a multi-stage pipeline, and why each belongs where it does.

This division of labour creates both an efficiency gain and a ceiling.
First-stage retrieval normally balances speed with recall; reranking concentrates on precision near the top.
Every shortlist is also a bottleneck: a reranker, fusion stage or answer-generating model cannot rescue a relevant document that no earlier route allowed into the candidate set. [Chapter 14](#precision-and-recall) gives recall and precision their exact meanings, and separates candidate-pool recall from recall at the displayed cut-off.

[Chapter 7 resolved the misleading semantic/dense assumption behind Puzzle 3](#returning-to-puzzle-three-why-did-the-keyword-query-retrieve-more).
We can now see the rest of the documented architecture.
Semantic Scholar’s 2025 technical account describes an Elasticsearch keyword search over titles, abstracts and author names, capped at 1,000 matches, followed by a trained LightGBM reranker that emphasises direct title matches, citation counts and recency. **The first stage determines which papers the learnt ranker ever gets to reconsider.** The second stage changes the order within that boundary.

This is machine-learned reranking, but not dense retrieval or an LLM reranker.
LightGBM cannot retrieve a paper excluded by the first stage, and its presence does not by itself explain why the August 2026 natural-language query returned 13 results. [Appendix E reconstructs the earlier documented 2020 version in depth](#appendix-why-ltr-becomes-a-reranker).

:::: {.figure key="retrieve-then-rerank"}
Retrieve broadly, then rerank a shortlist more carefully

![Retrieve broadly, then rerank a shortlist more carefully](images/09%20Rerankers%20-%20compare%20more%20carefully%20after%20retrieval/ChatGPT%20Image%20Jul%2026,%202026,%2009_45_42%20PM.png){width="1491" height="1055"}

::: caption
Fast stages search the collection; expensive stages see only the survivors.
:::
::::

### Cross-encoder reranking {#cross-encoder-reranking}

A **bi-encoder** encodes the query and candidate independently.
Document or passage vectors can therefore be calculated in advance, and search reduces to comparing the query vector with stored vectors.
That is what makes large-scale dense retrieval practical.
The cost is that the query and document do not interact until after each has already been compressed into its representation.

A **cross-encoder** does the opposite.
It places the query and one candidate into the model together, typically as a single input sequence.
Attention then runs across all their tokens before the model produces a ranking score—its estimate of task-specific relevance.
The model can therefore examine whether a particular query term aligns with a particular passage, whether a qualifier changes the claim, or whether two otherwise similar texts differ in negation, entity or intent.
Cross-encoder is an arrangement rather than a model: the same pretrained encoder that [a bi-encoder trains for independent encoding](#how-a-contextual-encoder-becomes-a-retrieval-encoder) can be trained to score query–candidate pairs jointly instead.
Putting BERT to work this way is how the arrangement became prominent in retrieval ([Nogueira and Cho, 2019](https://arxiv.org/abs/1901.04085)).

The [training example from Chapter 6](#how-a-contextual-encoder-becomes-a-retrieval-encoder) shows what that buys, because the difficulty it was built to illustrate does not go away once training ends.
The query was:

> Am I being delulu about getting this job?

Suppose a first-stage retriever of the kind Chapter 7 deployed returns a shortlist with both passages near the top of it—the one that addresses the stated need:

> How to recognise unrealistic expectations during a job search

and the hard negative it was trained against:

> Ten signs that you performed well in your job interview

Both are about job-seeking, both are advice, and both share vocabulary with the query.
That is why they are hard to separate once each has been [pooled into a single vector](#model-tokens-are-not-indexed-terms).
The compression happens before the passage knows what will be asked of it, so the distinction the query turns on need not survive it.
A cross-encoder processes the query together with each candidate in turn.
These interactions give it access to the detail needed to distinguish advice about unrealistic expectations from advice about interview performance.

The price is computation.
The candidate representation cannot be precomputed and reused, because its encoding depends on the query.
Reranking 100 candidates requires roughly 100 query–candidate model evaluations.
This is usually affordable for a shortlist, but not for millions of records.
Cross-encoder scores also reflect their training data, text truncation and definition of relevance; joint attention makes finer comparison possible, not infallible.

:::: {.figure key="bi-encoder-vs-cross-encoder"}
Bi-encoders precompute; cross-encoders compare query and candidate together

![Bi-encoders precompute independent vectors; cross-encoders compare query and candidate together](images/09%20Rerankers%20-%20compare%20more%20carefully%20after%20retrieval/ChatGPT%20Image%20Jul%2026,%202026,%2009_45_53%20PM.png){width="1491" height="1055"}

::: caption
Joint encoding permits a finer comparison but cannot be precomputed.
:::
::::

### Where ColBERT-style late interaction fits {#where-colbert-style-late-interaction-fits}

ColBERT sits between the pooled bi-encoder and the full cross-encoder.
Like a bi-encoder, it encodes the query and document independently, so document token vectors can be prepared before the query arrives.
Unlike a conventional bi-encoder, it does not reduce each indexed unit to one vector.
Its late-interaction score compares query-token vectors with document-token vectors after encoding.

This preserves more local matching evidence than a single pooled vector without paying the full cost of jointly encoding every query–document pair.
ColBERT-style models can be used for first-stage retrieval or to rerank a shortlist, depending on the implementation and scale.
They require more storage and computation than single-vector retrieval, but normally less query-time work than a cross-encoder over the same candidates.[^colbert-maxsim]

:::: {.figure key="late-interaction-position"}
Where late interaction sits between bi-encoders and cross-encoders

![Where ColBERT-style late interaction sits between bi-encoders and cross-encoders](images/09%20Rerankers%20-%20compare%20more%20carefully%20after%20retrieval/ChatGPT%20Image%20Jul%2026,%202026,%2009_47_23%20PM.png){width="1672" height="941"}

::: caption
Late interaction keeps one vector per token rather than one per passage.
The cost is storage.
:::
::::

::::: {.details .technical-note}
Optional worked example: how MaxSim adds token matches

:::: {.figure .worked-figure key="maxsim-worked"}
From token similarities to one score

::: {.include src="figures/maxsim-worked.html"}
:::

::: caption
Highlighted row maxima expose which token alignments contributed to this score.
They do not explain why the model learnt those similarities.
Whole-word tokens simplify this illustration; a real model uses its own tokeniser.
:::
::::
:::::

**Token vectors need more storage.** Keeping one vector per token rather than one per passage multiplies the index by roughly the number of tokens in a passage—two orders of magnitude is a fair mental estimate before compression.
This is why late interaction is an infrastructure decision rather than a model swap. [ColBERTv2](https://arxiv.org/abs/2112.01488) reports cutting the footprint of earlier late-interaction systems by six to ten times through residual compression—and the fact that such work was necessary tells you how large the untreated figure is.

**The scoring provides inspectable token alignments.** Because the score is a sum of per-query-token maxima, it decomposes: for each word in the query, the system can name the document token that matched it most strongly.
That is an *inspectable alignment*, not a post-hoc rationalisation, and it is closer to the evidence a lexical system can show than anything a pooled vector offers.
The limit is that the token vectors themselves remain latent: you can see *which* tokens aligned, not *why* the model considered them similar.
ColBERT is therefore inspectable at the scoring layer without being transparent end to end. [Chapter 15](#interpretability-requires-an-inspectable-pipeline) returns to what that distinction buys.
For a visual, in-depth introduction, see [Amélie Chatelain’s multi-vector search lecture](https://meet.ameliechatelain.com/lectures/multi-vector-search/#21).

All three ways of encoding—independent, joint and token-level—are now on the table, and they answer the question [Chapter 5’s section on BERT](#what-bert-is-and-what-it-still-needs) had to leave open.
A single pretrained encoder can be deployed in any of them: encode query and candidate **independently** and compare two pooled vectors, encode them **jointly** in one sequence and score the pair, or encode them separately as **sets of token vectors** and compare those.
The arrangement affects both cost and the detail available for comparison.
Independent encoding allows document representations to be computed in advance.
Joint encoding usually costs too much to apply to every record in a large collection for each query, while token-level comparison retains separate representations that a single pooled vector combines.

> To understand the system’s behaviour, ask how query and document representations are compared and what ranking task the model was trained on.

### LLMs as rerankers {#llms-as-rerankers}

A general-purpose or specially trained large language model can also act as a reranker.
Instead of merely comparing embeddings, it receives the query, candidate text and sometimes explicit relevance instructions.
This makes it possible to ask the model to consider criteria such as population, method, date, study design or whether a passage actually answers the question rather than merely sharing its topic.

LLM reranking is commonly framed in three ways:

- **Pointwise:** judge or score each candidate independently.
  This scales linearly with the shortlist, but the scores may require calibration and the model does not directly compare candidates.
- **Pairwise:** compare two candidates and choose which is more relevant.
  Direct comparison can help with subtle distinctions, but many comparisons may be needed and preferences can be inconsistent.
- **Listwise:** present several candidates together and ask the model to return an ordering.
  This gives the model comparative context, but long lists exceed context limits, so systems often use sliding windows or repeated partial rankings.
  Input order can influence the result.

:::: {.figure key="llm-reranking-strategies"}
Pointwise, pairwise and listwise LLM reranking

![Pointwise, pairwise, and listwise LLM reranking](images/09%20Rerankers%20-%20compare%20more%20carefully%20after%20retrieval/ChatGPT%20Image%20Jul%2026,%202026,%2009_46_17%20PM.png){width="1448" height="1086"}

::: caption
Three ways to ask a model for an order, with different costs and failure modes.
:::
::::

Pointwise, pairwise and listwise prompting differ in computational cost and failure modes.
Research has demonstrated both listwise and pairwise LLM reranking, including zero-shot listwise reranking ([Ma et al., 2023](https://arxiv.org/abs/2305.02156)) and pairwise ranking prompting ([Qin et al., 2024](https://aclanthology.org/2024.findings-naacl.97/)).

The words *pointwise*, *pairwise* and *listwise* also occur in classical learning-to-rank research, where they describe what the training objective learns from.
Here they describe how an LLM is asked to judge candidates at reranking time.
The shared vocabulary does not make the two arrangements identical; [Appendix E](#appendix-ltr-objectives) separates them.

LLM rerankers can use richer instructions and longer textual context than many conventional rankers, but they are usually slower and more expensive.
They may also be sensitive to prompt wording, candidate order, context-window limits, model updates and sampling settings.
A generated explanation can make a decision easier to inspect, but a plausible explanation is not evidence that the ranking is correct.

The practical questions are therefore: what produced the shortlist, how many candidates reached the reranker, what text and metadata the reranker saw, which ranking formulation it used, and how the complete pipeline was evaluated.

### Ranking a useful set, not only relevant items {#ranking-a-useful-set-not-only-relevant-items}

A ranking can be strong item by item and poor as a list.
Suppose the first six papers are all highly relevant reviews of the same subtopic, using similar evidence and reaching much the same conclusion.
The sixth may add less to an exploratory search than a slightly lower-scoring paper on another aspect.
A conventional relevance ranker scores each query–document relationship. **Result diversification** also asks how much the next candidate adds to the set already selected.

::: pull-quote
> Relevance asks how well each item fits the query.
> Diversity asks what it adds to the items already selected.
:::

This changes the optimisation target.
The system is no longer simply sorting independent relevance scores; it is constructing a list or subset whose members should be both useful and not needlessly repetitive.
Diversification names that objective; a reranker names a pipeline position, and deduplication removes records judged equivalent under a separate rule.

For academic search, diversification is most attractive for exploration: mapping several interpretations of an ambiguous term, exposing different methods or disciplines, and choosing less redundant passages for a generated answer.
Its meaning still depends on what the system represents as different—topic, method, geography, viewpoint, publication type, author community or merely wording.
Topical dissimilarity does not automatically produce viewpoint diversity, fairness or balanced evidence.

Where high recall is required, diversity-aware selection does not replace formal candidate retrieval.
It may reorder a pool, but it can push a highly relevant near-neighbour below the displayed cut-off; in a systematic review, similar papers remain separate evidence. [Appendix E compares the main diversification methods and the metrics used to evaluate aspect coverage](#appendix-diversity-aware-ranking-metrics).

:::: {.figure .worked-figure key="diversification-worked"}
A good next paper adds something

::: {.include src="figures/diversification-worked.html"}
:::

::: caption
Schematic papers and stipulated usefulness illustrate the diversification objective, not a calculated algorithm output or findings about actual studies.
Shared aspects do not make papers duplicates.
Broader topical coverage does not guarantee balanced evidence; a high-recall review may need every relevant study.
:::
::::

### Reranking in two documented academic pipelines {#reranking-in-two-documented-academic-pipelines}

Two systems already mentioned in this book document their reranking stage precisely enough to see the pattern, and they use different machinery for it.

[PubMed Best Match](#bm25-and-lexical-ranking-in-academic-search) retrieves and orders records with BM25, then applies LambdaMART to **the top 500**. [Primo Research Assistant](#top-k-is-a-result-boundary-not-a-dense-retrieval-method) retrieves through CDI’s largely lexical ranking, then reranks **the top 30** with embeddings.

The two numbers are budgets, not statements about relevance.
Each limits which records receive the second score; what happens to the rest depends on the product.
PubMed continues the list below 500 in Best Match order, whereas Primo Research Assistant’s answer is bounded again by a five-source limit, so its tail is not merely unreranked.
Everything outside the first stage’s results is unreachable either way.
When a vendor says its search “uses AI reranking”, ask which model is used and *how many candidates it receives*.

**Learning to rank (LTR)** names the broader supervised approach behind LambdaMART.
Instead of manually fixing the final influence of every ranking factor, a system is trained on examples to combine signals into an ordering.
Those signals can include lexical evidence such as BM25 and field matches alongside document or query properties such as recency, publication type or past usage.
They need not be embeddings, and the model learns only from the features and relevance evidence it is given. [Appendix E](#appendix-rank-fusion-and-learning-to-rank) develops the idea without requiring the algorithmic detail.

```{=html}
<div class="ir-figure" role="group" aria-labelledby="primo-ra-pipeline-title">
<p class="figure-title" id="primo-ra-pipeline-title">One product, every stage in this book</p>
<p>Primo Research Assistant repays tracing end to end: its documented pipeline uses almost every mechanism this book has described, and each stage constrains the next.</p>
<p class="asset-label" id="tbl-9-3">Table 9.3 — One discovery product mapped to the stages described in this book, with the chapter that explains each. <span class="as-of">Vendor documentation checked in August 2026; see Chapter 1 for the September 2026 account.</span></p><div class="table-wrap"><table>
<thead><tr><th>Stage</th><th>What the documentation describes</th><th>Explained in</th></tr></thead>
<tbody>
<tr><td>1. Query transformation</td><td>An LLM converts the user’s question into an <code>OR</code>-connected Boolean query, and can auto-refine a limited set of filters such as date range, peer-reviewed status and resource type.</td><td><a href="#when-a-system-writes-the-boolean-query">When a system writes the Boolean query</a></td></tr>
<tr><td>2. Candidate retrieval</td><td>That query goes to CDI, whose retrieval is largely lexical over an inverted index.</td><td><a href="#how-boolean-search-uses-an-inverted-index">Inverted indexes</a></td></tr>
<tr><td>3. First-stage ranking</td><td>CDI’s proprietary ranking combines rare-term and field weighting, term frequency, field length, phrase and proximity boosts with static signals—resource type, recency, peer-review status, citations.</td><td><a href="#bm25-and-lexical-ranking-in-academic-search">BM25 in academic search</a></td></tr>
<tr><td>4. Reranking</td><td>Up to the 30 leading results are reordered with embeddings.</td><td>This section</td></tr>
<tr><td>5. Result boundary</td><td>The abstracts of the top five (<em>k</em> = 5) are passed to the LLM for generation.</td><td><a href="#top-k-is-a-result-boundary-not-a-dense-retrieval-method">Top-<em>k</em> as a result boundary</a></td></tr>
</tbody>
</table></div>
<p class="ir-figure-note">A teaching decomposition of Primo Research Assistant’s documented workflow, mapped to the chapters that explain it. The two budgets—30 candidates reranked, five abstracts passed to generation—are the ones discussed above.</p>
</div>
```

Two things follow from reading [Table 9.3](#tbl-9-3) as a chain.
The **embedding stage is fourth, not first**: a paper CDI’s lexical ranking never placed in the top 30 is not reordered, it is simply absent.
And the evidence reaching generation is **five abstracts**, not five papers, so anything stated only in a full text was never in play.
Here, lexical retrieval still determines which papers are available to the AI reranker and answer generator.

::: {#distinction-neural-dense .key-distinction-label}
Key distinction
:::

::: {#for-awareness-two-neural-variants .legacy-anchor}
:::

### Neural information retrieval is broader than dense retrieval {#neural-ir-broader-than-dense-retrieval}

**Neural information retrieval names an umbrella category, not a dense representation or a single pipeline stage.** A neural model may retrieve with one dense vector, retain several token vectors for late interaction, produce sparse vocabulary-aligned weights, or rerank candidates retrieved by another method.
The cross-encoders and LLM rerankers above are therefore part of neural IR even when the first-stage retriever is lexical.

Most contemporary examples in this book use Transformers, but neural IR is older and broader than that architecture: earlier systems used feed-forward, convolutional and recurrent networks, and a Transformer model is not inherently a retriever.[^neural-ir-before-transformers]

#### Learnt sparse retrieval in the pipeline {#learnt-sparse-in-the-pipeline}

Late interaction, described above, is one of two arrangements that sit awkwardly between the simpler lexical–dense categories this book has used.
The other is [learnt sparse retrieval](#learnt-sparse-representations), which runs the other way: lexical in shape but learnt throughout.
Chapter 8 explained the representation.
This section sits immediately before hybrid retrieval because learnt sparse retrieval is one alternative to it: a single sparse index carrying both typed and expanded terms.
Systems can also combine it with dense retrieval.

**[Chapter 7’s term-match floor](#candidate-boundaries-in-lexical-and-dense-retrieval) still applies.** For the sparse term-matching route described here, a non-zero matching score requires overlap between active vocabulary dimensions.
Learnt expansion can create that overlap even when the original query and document share no typed query term.
As a concrete literature-review example, Elicit [described work on SPLADE](https://elicit.com/blog/semantic-search) in June 2024: model-suggested related terms enrich the query before they are sent to [regular full-text search](#what-full-text-search-means-in-ir).
That account describes work under way when it was written rather than a settled production architecture.[^elicit-pricing-inference]

**It can use familiar inverted-index technology.** Because the representation stays sparse and vocabulary-aligned, learnt sparse retrieval can be served by Lucene-family inverted-index machinery and does not inherently require a separate dense-vector index.
That is an architectural distinction from dense retrieval, not a claim that every library operates its own index: many libraries license hosted discovery systems and manage neither technology directly.

**The cost reappears as query latency.** Expansion is not free: adding terms to a query lengthens the posting lists the engine must traverse, and the terms a model adds tend to be common ones with long lists.
“Runs on an inverted index” therefore means the infrastructure is familiar, not that the query is as cheap—[Appendix C](#appendix-learnt-sparse-query-cost) gives the measured size of the gap and what is known about closing it.

Learnt sparse retrieval has a named academic development example in Elicit; the cited account does not confirm production deployment. **Late interaction does not appear to have a comparable publicly documented deployment in a major academic search product**—it is well represented in the research literature and in general-purpose retrieval infrastructure, less so on a vendor’s architecture page.
The storage cost described above is the usual explanation offered.
Absence of documentation is not evidence of absence, and this is exactly the kind of claim that dates, so treat it as a description of what is currently inspectable rather than of what exists.

Both SPLADE and ColBERT remain dependent on model vocabulary and training data, and neither escapes [out-of-distribution transfer](#out-of-distribution).[^splade-limitations] Both are nevertheless among the more inspectable neural approaches.
SPLADE exposes weighted vocabulary terms and ColBERT exposes token alignments, which provide more scoring evidence than a single pooled dense score.
Those artefacts do not explain how every contextual representation was formed or make either model transparent end to end.

:::: chapter-close
1. Multi-stage retrieval exists because accuracy and scale trade against each other.
2. A reranker can only reorder what the first stage returned.
   It cannot recover a document that was never retrieved.
3. Neural information retrieval is an umbrella category, not a synonym for dense retrieval.
   It includes dense bi-encoders, learnt sparse retrieval, late interaction and neural reranking.
4. Joint encoding, late interaction and learnt sparse retrieval preserve different amounts of query–document evidence and can occupy different pipeline stages.

::: {.chapter-transition}
Chapter 10 turns to a different design decision: running more than one candidate-generation route, deciding whether to blend or route them, and combining ranked lists whose scores may not share a scale.
:::
::::

::: self-check
A vendor says its product uses “neural information retrieval”. What architectures might that label cover, and what does it leave unknown?

:   It may mean dense bi-encoder retrieval, learnt sparse retrieval, ColBERT-style late interaction, or a neural cross-encoder or LLM reranking candidates from another retriever.
    The label does not identify whether the representation is sparse or dense, whether the neural model retrieves or only reranks, what supplied its candidates, or how many candidates reached it.

Why can a stronger reranker improve precision without raising the recall ceiling set by the first stage?

:   The reranker receives a fixed shortlist and can only reorder its members.
    Better comparisons may move relevant candidates upwards, improving the visible ranking, but a relevant record omitted by every candidate-generation route is unavailable to every later stage.
:::

[^colbert-maxsim]: A simplified ColBERT late-interaction score is:

    $$
    \operatorname{score}(q,d)=\sum_{i\in q}\max_{j\in d}q_i\cdot d_j.
    $$

    Each query-token vector $q_i$ is compared with the document-token vectors $d_j$.
    For each query token, the strongest document-token similarity is retained, and these maxima are summed.
    This **MaxSim** decomposition is what makes the contributing token alignments inspectable.
    Because document-token vectors are computed without seeing the query, they can be indexed in advance.
    Practical implementations use approximation, compression and pruning rather than exhaustively comparing every stored token vector.
    ColBERTv2 uses residual compression, while [PLAID](https://arxiv.org/abs/2205.09707) uses centroid-based pruning to reduce search cost.

[^neural-ir-before-transformers]: Pre-Transformer neural IR included [DSSM’s feed-forward encoders](https://www.microsoft.com/en-us/research/publication/learning-deep-structured-semantic-models-for-web-search-using-clickthrough-data/), [C-DSSM’s convolutional architecture](https://www.microsoft.com/en-us/research/publication/a-convolutional-latent-semantic-model-for-web-search/) and [paired LSTM query–document encoders](https://arxiv.org/abs/1502.06922).
    Interaction-focused neural rankers also predated Transformer cross-encoders: examples include [DRMM](https://doi.org/10.1145/2983323.2983769) and [K-NRM](https://arxiv.org/abs/1706.06613). [Appendix D](#appendix-misleading-overlaps) places these architectures within the wider neural-IR terminology.

[^elicit-pricing-inference]: Elicit’s [13 June 2024 engineering post](https://elicit.com/blog/semantic-search) describes SPLADE work in progress, not a confirmed production rollout.
    Its [changelog entry for 25 July 2024](https://support.elicit.com/en/articles/14823097-changelog) subsequently announces unlimited search, summaries and chat and removal of credits.
    The timing is suggestive of lower search-serving costs, potentially from a SPLADE deployment, but that is an inference rather than confirmation: neither source attributes the pricing change to SPLADE or reports its deployment costs.
    Pricing can also reflect commercial decisions or other engineering changes.
    It does not establish that SPLADE is generally cheaper than BM25 or dense retrieval.
    Sources checked 12 September 2026.

[^splade-limitations]: Vocabulary-aligned dimensions make SPLADE’s terms and expansions inspectable, but learnt sparse models remain constrained by their output vocabularies.
    Rare names and identifiers may be divided into fragments that do not preserve an entity cleanly.
    The [DyVo study](https://aclanthology.org/2024.emnlp-main.45/) proposed dynamic entity vocabularies specifically to address that problem.
    Sparsity also does not remove OOD transfer: changes in vocabulary, queries, corpora or retrieval tasks can degrade learnt expansions and weights, and low-frequency terms from the training data can remain difficult.
