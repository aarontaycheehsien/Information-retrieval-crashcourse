---
key: "diagnosing-failure"
kind: "chapter"
eyebrow: "Chapter 13"
meta: "About 18 min"
question: "What kind of retrieval failure does the evidence suggest, and what should a librarian investigate next?"
legacy_anchors: ["ch8"]
---

## Diagnosing retrieval failure {#diagnosing-failure}

::: {.stage-map on="query-transformation analysis first-stage fusion reranking presentation" controller="on" label="Pipeline map: every stage is highlighted, because a failure can originate at any of them"}
:::

::: chapter-orient
A relevant article uses *myocardial infarction*, but the search used *heart attack*.
A librarian’s first response is familiar: inspect the record’s language, add synonyms or controlled vocabulary, follow citations and revise the search.
Information retrieval gives that familiar problem a standard name: **vocabulary mismatch**.

You have already encountered most of the machinery behind this diagnosis.
This chapter brings it together.
It distinguishes vocabulary mismatch from out-of-vocabulary and representation problems, and asks whether a learnt retriever is being used out of distribution.
It then examines cases where every word is present but the relationships between them are not preserved.

Every stage on the map above is highlighted, because a failure can originate at any of them.
The subject throughout is retrieval—whether the right records were found and ranked—and the distinction matters for diagnosis: a fluent summary built on the wrong three records is a retrieval failure, not a writing one.
:::

::: {#diagnosing-where-retrieval-goes-wrong .legacy-anchor}
:::

::: {#three-different-ways-vocabulary-can-go-wrong .legacy-anchor}
:::

### First, could the record have been returned? {#could-the-record-have-been-returned}

From the result screen, many retrieval failures look alike: a relevant record is missing, or an irrelevant one sits near the top.
The useful question is which evidence would distinguish several possible explanations, because more than one can apply at once.

**Before diagnosing anything, establish that the record could have been returned.** Investigate these four questions before reaching for the lenses below.
Coverage and visible filters may be testable from the interface; hidden candidate sets, indexed units and cut-offs may require documentation or a saved trace.
Record what remains unknown rather than treating an unavailable trace as proof of exclusion.

1. **Was it eligible?** A record absent from the collection, still inside an indexing lag, or excluded by a date limit, format facet or access filter was never in play.
   No amount of vocabulary work will retrieve it.
2. **Was it matched but hidden?** A record that was retrieved but fell outside the [result boundary](#top-k-is-a-result-boundary-not-a-dense-retrieval-method) was matched; a cutoff hid it.
   That points at a different stage from a record that never matched.
   The [Vector Similarity Lab](vector-similarity-lab.html)’s cutoff experiment shows how the order of filter and cut-off decides this.
3. **Was the evidence split?** Where a system indexes passages rather than whole documents, a claim split across [separate indexed units](#one-document-one-chunk-and-one-vector-are-not-the-same-thing) may leave no single unit carrying enough evidence to rank.
4. **Is a typed word missing, or not visibly matched?** Then [Chapter 4’s four explanations](#what-might-have-happened-to-a-missing-query-word) apply first—including a match in an indexed field or version that the result excerpt does not show.

For direct file search, inspect the searched paths, readable formats and exclusion rules as well as the pattern.
Ripgrep normally skips ignored and hidden files; [its documentation](https://github.com/BurntSushi/ripgrep) describes how to change those defaults.
Check whether extraction or OCR preserved the relevant passage, whether matches were truncated before reaching the model, and whether the agent stopped before trying a different expression.
A literal match also does not establish that a passage affirms a claim: read its negation and qualifications.

Once eligibility is established, the diagnosis works through the missing record’s language, its representation, the retriever’s training and the matching behaviour that produced the result.

:::: {.figure .worked-figure key="missing-paper-boundaries"}
The same missing paper, four different explanations

::: {.include src="figures/missing-paper-boundaries.html"}
:::

::: caption
The symptom is the same; the stage to investigate differs.
Establish these boundaries before diagnosing vocabulary mismatch, OOV, distribution shift or composition.
:::
::::

### Four diagnostic lenses {#four-diagnostic-lenses}

| What a librarian might notice | What the evidence points to | Where this was set up | Likely remedy to test |
|---|---|---|---|
| A known relevant record uses different terminology | [**Vocabulary mismatch**](#vocabulary-mismatch): an observed relationship between query and record | [Boolean admission](#boolean-admission), [BM25](#bm25-ranking) and [query transformation](#query-transformation) | Synonyms, controlled vocabulary, query or document expansion, dense or hybrid retrieval |
| A coined term, identifier or specialised string disappears or behaves strangely | [**OOV or weak representation**](#out-of-vocabulary): a problem relative to a named vocabulary or representation | [Index analysis](#before-the-index-text-becomes-tokens) and [model tokenisation](#how-dense-models-receive-text) | Inspect fields, analysis and tokenisation; preserve an exact lexical route; test representation quality |
| A model works plausibly in general but poorly for this discipline, query style, corpus or retrieval purpose | Suspected [**OOD transfer or distribution shift**](#out-of-distribution): a training–deployment relationship | [Retrieval training](#how-a-contextual-encoder-becomes-a-retrieval-encoder) and [evaluation transfer](#test-collections-and-benchmarks) | Test locally; adapt, retrain or replace the model; retain lexical or hybrid fallbacks |
| All the words occur, but their direction, negation or relationship is wrong | [**Negation, relation or composition is not preserved**](#composition-failure): a matching or model-capability problem | [Explicit logic](#boolean-admission) and [interaction-heavy reranking](#cross-encoder-reranking) | Explicit logic, phrase or proximity controls, cross-encoder reranking or targeted training; late interaction is a weaker token-preserving option |

: A diagnostic map for retrieval failures. The rows are prompts for investigation, not an exhaustive or mutually exclusive taxonomy.

The four rows are different kinds of claim, which is why they cannot simply be tried in turn.
Vocabulary mismatch is a relationship visible between a query and a relevant record.
OOV is a property relative to a named vocabulary.
OOD is a relationship between training and deployment.
A failure of negation, direction or composition is a limit in matching or model capability.

The rest of the chapter takes those diagnostic questions in order, beginning with the problem librarians have always managed.
A synonym or controlled term may sometimes work around lexical OOV; it does not by itself address OOD transfer or a failure of logic and relation.

::: {#1-vocabulary-mismatch .legacy-anchor}
:::

### Vocabulary mismatch: a problem librarians already know {#vocabulary-mismatch}

Suppose a search for `heart attack recovery` misses a relevant article titled:

> Rehabilitation after myocardial infarction

The query and the article express sufficiently related concepts using different lexical forms.
The **vocabulary mismatch problem** long predates neural retrieval. [Furnas and colleagues (1987)](https://doi.org/10.1145/32206.32212) showed how rarely people choose the same words for the same objects and operations; later IR work states the problem directly as lexically different but semantically related query and document terms ([Jeong et al., 2021](https://aclanthology.org/2021.sdp-1.2/)).

Librarians have never needed an embedding to recognise this.
They respond with synonyms, spelling and morphological variants, controlled vocabulary, citation searching, pearl growing and iterative reformulation.
In strict Boolean search, `OR` and subject headings make those bridges explicit. [Query transformation](#query-transformation) may add them automatically.

BM25 changes the ranking rule, not the identity of the terms.
It can rank a record from partial lexical overlap, and stemming or analysis may connect morphological variants.
But BM25 does not itself make `heart attack` synonymous with `myocardial infarction`.

A suitably trained dense retriever offers another bridge.
It can place the complete query and document representations near one another without exact overlap.
That is one modern response to vocabulary mismatch.
It is not the origin of the problem, and it is not a guarantee that every paraphrase will be connected.

[Chapter 6](#a-worked-training-example)’s `delulu` example is the same diagnosis in newer clothing: a searcher writes `delulu about getting this job` while a relevant page discusses `unrealistic expectations during a job search`.
The age or register of the expressions may affect whether a learnt model connects them, but the visible query–document relation is still vocabulary mismatch.

> Dense retrieval is a newer response to an old retrieval problem.

::: {#2-different-kinds-of-vocabulary-gap .legacy-anchor}
:::

::: {#vocabulary-and-representation-gaps .legacy-anchor}
:::

### Out-of-vocabulary (OOV): missing from which vocabulary? {#out-of-vocabulary}

Suppose a DOI, gene name or chemical identifier is visibly present in a record, yet searching it returns nothing useful or behaves unpredictably.
The first question is not whether the string is simply “too new” for search.
It is which component failed to preserve it.

**Out of vocabulary** is meaningful only relative to a named vocabulary.
An analysed query term can be absent from the index vocabulary, a complete word can be absent from an older word-level model’s vocabulary, or a string can be present as model tokens without having acquired a useful retrieval representation.
Those are not the same condition.

| Question | What failure means |
|---|---|
| **Is there a corresponding term in the index vocabulary?** | After [lexical tokenisation and analysis](#before-the-index-text-becomes-tokens), the analysed query term has no corresponding indexed term and posting list. It therefore contributes no direct lexical evidence. |
| **Can the model tokeniser encode the string?** | A word-level model may lack a complete-word entry; a subword model may divide the string into known pieces; a byte-level model can encode valid UTF-8 input, while a character-level model depends on its supported inventory or fallback. |
| **Has the model learnt a useful representation?** | The string is technically representable, but its pieces or their contextual use were not learnt well enough for the retrieval task. |

: “Out of whose vocabulary?” separates literal OOV from a representation or training-exposure problem.

The first two questions concern literal vocabularies.
The third does not.
It describes a **representation or training-exposure gap**.
Keeping it subordinate to the OOV investigation prevents “the tokeniser can encode the pieces” from being mistaken for “the retriever has learnt a useful representation.”

A query term can therefore be missing from the index but encodable by a model tokeniser.
It can be tokenisable but poorly represented.
It can appear exactly in the collection while being divided awkwardly by the model. [Chapter 2](#before-the-index-text-becomes-tokens)’s index analysis and [Chapter 6](#how-dense-models-receive-text)’s account of word and subword tokenisation, and of [the difference between model tokens and indexed terms](#model-tokens-are-not-indexed-terms), explain why.

`rizzlord` is partly compositional.
A model may infer a plausible meaning if its tokeniser produces useful pieces resembling `rizz` and `lord`, and its training gave those pieces informative contextual representations. [Appendix B runs this exact string through BERT’s tokeniser](#appendix-wordpiece-worked-example), which turns out to hold no `rizz` piece at all: it produces `ri`, `##zz` and `##lord`, representable without being the decomposition a reader would make.
Another model may split the same string very differently.
A pure byte-level model can encode any valid UTF-8 form of `iykyk`, `frfr` or `skibidi`; a character-level model can do so only when its inventory or fallback covers the characters.
As [Appendix B](#appendix-character-and-byte-inputs) explains, either may encode the expression without knowing how it is being used.

> Tokenising a term is not the same as understanding it.

The reverse case is equally important.
Suppose an identifier called `DELULU-427` appears in three indexed documents and exact identity matters.

If the query and documents are [analysed consistently](#before-the-index-text-becomes-tokens), a lexical system can match the surface form directly.
A keyword field might preserve the complete string; an ordinary text field might split it into `delulu` and `427`.
BM25 can give rare matching components substantial weight without ever having encountered the identifier during model training.

A standard single-vector dense retriever can usually encode the string as model tokens, but may blur it with related strings or concepts after contextualisation and pooling.
Research on salient-phrase-aware dense retrieval documents this weakness, and shows that better training can mitigate it ([Chen et al., 2022](https://aclanthology.org/2022.findings-emnlp.19/)).

This is why a lexical path remains important for gene and protein identifiers, chemical strings, dataset titles, model names, article identifiers, product codes, personal names and newly coined terminology.
The lesson is not that dense retrieval always fails on identifiers.
It is that omitting exact lexical matching creates avoidable risk when exact identity determines relevance.

::: {#3-out-of-domain .legacy-anchor}
:::

::: {#domain-shift .legacy-anchor}
:::

### Out-of-distribution (OOD): when deployment differs from training {#out-of-distribution}

A search tool may look excellent on ordinary questions yet repeatedly miss relevant legal or biomedical papers.
It may find one answer-bearing passage but perform poorly when a librarian asks for all studies meeting review criteria.
Every word can be familiar while the retrieval behaviour is wrong for the setting or purpose.

In neural IR, **out of distribution** is used broadly for situations in which deployment differs from the distributions or retrieval conditions represented during training.
This can include shifts in queries or corpora and, in some IR work, shifts in retrieval task and relevance pattern.

**Domain shift** is a familiar case, but the retrieval literature does not settle on one fixed partition.
For a librarian investigating a failure, three sites of shift are especially useful:

- **Query shift:** users ask in a different style, register, length or intent, or submit query types the training data scarcely contained.
- **Corpus or domain shift:** the collection differs in discipline, genre, language, document type, time period or terminology.
- **Task or relevance shift:** the deployment rewards a different query–document relationship.
  A model trained to find answer-bearing web passages may be used for high-recall evidence searching, known-item retrieval or citation discovery.
  See [Appendix F](#appendix-evidence-synthesis-high-recall-retrieval) for why this task shift is especially important in systematic-review retrieval.

All the words in the new setting may be familiar.
A model can therefore be OOD without encountering an OOV token and without facing a simple vocabulary mismatch.
Conversely, a new discipline can create OOD transfer, specialised OOV strings and query–document vocabulary mismatch at the same time.

This is the other side of [Chapter 6’s retrieval-training story](#how-a-contextual-encoder-becomes-a-retrieval-encoder).
That chapter showed that positive pairs, negatives and training labels teach a model what should rank together.
Once a model has learnt an operationalisation of relevance from one distribution of queries, documents and judgements, OOD asks how well those rewarded relationships transfer elsewhere.

The retrieval literature operationalises that problem more broadly than subject domain. [BEIR](https://arxiv.org/abs/2104.08663) (Thakur et al., 2021) was designed to test zero-shot generalisation across heterogeneous retrieval tasks and domains. [MS-Shift](https://doi.org/10.1007/978-3-031-28244-7_40) isolates changes in query semantics, intent and length (Lupart et al., 2023).
Work on generative IR additionally tests query variations, unseen query types, unseen tasks and corpus expansion ([Liu et al., 2025](https://doi.org/10.1007/978-3-031-88711-6_26)).

A single poor result cannot prove OOD, especially when a vendor does not disclose the training distribution.
The evidence becomes stronger when performance is plausible on familiar benchmark-like queries but degrades systematically for one discipline, collection, query style or retrieval purpose.
That is why the practical response is comparative local evaluation, followed where possible by adaptation, retraining or replacement—not simply adding another synonym.

BM25 has a limited kind of robustness here.
Its matching rule does not import a learnt semantic interpretation from another dataset, and its principal term statistics come from the target collection.
It still depends on analysers, fields, parameters and query formulation, and it cannot bridge different terminology by itself.
BEIR found it a robust zero-shot baseline while some more expensive neural and reranking approaches performed better on average.
That is evidence about those benchmark tasks, not a law that lexical systems always transfer well or dense systems always transfer badly.

> A learnt retriever may transfer its operational model of relevance badly: OOD is the question of whether what was learnt travels to this retrieval situation.

::: {#when-every-word-is-familiar-and-search-still-gets-it-wrong .legacy-anchor}
:::

### When every word is known: failures of negation, relations and composition {#composition-failure}

Sometimes no vocabulary is missing, the query need not be OOD, and lexical overlap is nearly perfect.
What fails is the relationship among the pieces.

Compare three retrieval requirements:

- `A causes B`, not merely a passage saying that `B causes A`.
- `The intervention does not increase risk`, not one saying that it `does increase risk`.
- Two concepts participating in the required relationship, not simply occurring independently in the same passage.

A bag-of-words lexical score preserves the presence of the terms but not necessarily their direction, scope or roles.
BM25 may score the opposed passages similarly because the lexical evidence is almost identical.
Strict Boolean preserves logic that the searcher states explicitly, but ordinary term conjunction still does not encode who caused what or which proposition a negation governs.

Phrase operators, positional indexes, proximity scoring and n-grams can preserve adjacency and local order.
They are valuable callbacks to Chapters 2 and 3, but adjacency alone does not solve causality, negation or relation binding.

Single-vector dense retrieval can also blur a decisive local difference when it pools a whole query or passage into one representation.
A cross-encoder reads query and candidate jointly and therefore provides the strongest architectural opportunity to model these relationships.
ColBERT-style late interaction preserves more token-level evidence than a pooled bi-encoder, but it still encodes query and document separately and can fail badly on logic and negation. [NevIR](https://aclanthology.org/2024.eacl-long.139/) (Weller et al., 2024) found cross-encoders strongest and late-interaction models next.
Most evaluated systems still performed at or below a random ranking baseline.
Neither architecture guarantees correct logic, and neither can rescue a record omitted from the first-stage shortlist.

This is a capability failure rather than a formally standard IR category.
It is still a useful diagnostic lens, because the intervention it calls for differs from synonym expansion or domain adaptation. [BoolQuestions](https://aclanthology.org/2024.findings-emnlp.156/) (Zhang et al., 2024) and [NevIR](https://aclanthology.org/2024.eacl-long.139/) document why Boolean-logic and negation tests belong in a retrieval evaluation.

> All the terms can be present while the relationship that determines relevance is lost.

::: {#matching-failures-to-remedies .legacy-anchor}
:::

### Diagnose before choosing a remedy {#diagnose-before-choosing-a-remedy}

> A result screen supplies symptoms, not causes.

Work from a known relevant record or a controlled contrast whenever possible, and settle [whether it could have been returned](#could-the-record-have-been-returned) first.
Then ask:

1. **Does the relevant record simply use different terminology?** Investigate [vocabulary mismatch](#vocabulary-mismatch).
2. **Does an identifier, new coinage or specialised string disappear or behave inconsistently?** Ask [out of whose vocabulary](#out-of-vocabulary), and inspect index fields and analysis separately from model tokenisation and representation.
3. **Does the model work plausibly elsewhere but poorly for this discipline, corpus, query style or retrieval purpose?** Investigate [OOD transfer](#out-of-distribution), and compare performance on a local query set before adapting or replacing anything.
4. **Are all the words present but their relationships wrong?** Investigate [negation, relations and composition](#composition-failure).

[Table 13.1](#tbl-13-1) gives the remedy worth testing first in each case.
Reach for it only after the question above it has an answer.
The order matters more than the list: the same remedy applied to the wrong diagnosis is what makes a search look unfixable.

The answers can overlap.
A newly coined chemical identifier may be OOV for one component, weakly represented by another and concentrated in a corpus unlike the model’s training data.
A specialised query may combine OOD transfer with a logic failure.
Diagnosis therefore means accumulating evidence and testing interventions.

::: {#comparing-the-three-main-approaches .legacy-anchor}
:::

### What different first-stage approaches preserve {#comparing-the-three-first-stage-approaches}

Every diagnosis above ends at the same place: something the retrieval method did not preserve.
That is worth stating directly, because it is what separates the four lenses from a list of complaints about products.

| Method | What it preserves best | Characteristic strength | Characteristic blind spot |
|---|---|---|---|
| Strict Boolean | Explicit logic over analysed terms | Explicit, auditable inclusion and exclusion on a fixed database and platform | A weak `AND`, `OR` or `NOT` changes the eligible set completely |
| BM25 | Analysed lexical term evidence, especially rare matching terms | Strong first-stage ranking when wording overlaps | Weak vocabulary bridging and no inherent phrase meaning |
| Single-vector dense retrieval | Overall learnt similarity | Scalable paraphrase retrieval using precomputed representations | Pooling may blur exact identity or decisive local details |

: Three contrasting first-stage retrieval patterns used throughout this book: what each preserves, its characteristic strength and its blind spot.

These are three reference patterns, not a complete list of first-stage methods. [Direct file search with grep](#grep-searching-text-directly) can supply unranked text matches.
Learnt sparse retrieval and ColBERT-style late interaction can also operate at the first stage, as [Chapter 9](#neural-ir-broader-than-dense-retrieval) explained. [Query transformation](#query-transformation) changes or creates retrieval inputs; retrieval control routes them.
Rerankers compare a shortlist after retrieval. [Agentic search](#agentic-search-who-chooses-the-next-retrieval-action) describes how subsequent actions are selected and sequenced.
A real system may combine all of them.

That is why asking whether a product “uses vectors” tells us very little.
The same holds for most of the vocabulary a vendor is likely to use: [Appendix D](#appendix-search-terminology) sets out which labels name a representation, which name a matching method, which name a pipeline stage, and which name only an interface or an aspiration.

No first-stage approach preserves everything equally well.
Hybrid and multi-stage systems exist partly because there is no single representation that eliminates vocabulary, distribution and composition problems.
The practical conclusion is diagnostic: determine what evidence was lost before choosing Boolean expansion, lexical retrieval, dense retrieval, adaptation, reranking or hybridisation.

:::: chapter-close
1. Vocabulary mismatch is the familiar problem of a query and relevant document expressing related concepts in different lexical forms.
2. OOV is always relative to a specified vocabulary.
   A tokeniser’s ability to encode a string does not establish that the retriever has learnt a useful representation for it.
3. OOD concerns transfer from training to deployment.
   In neural IR it can cover shifts in queries or corpora and, in some work, retrieval task or relevance pattern.
4. Negation, relations and composition can fail even when vocabulary is familiar and lexical overlap is complete.
5. These are different diagnostic lenses rather than parallel categories.
   They can overlap, and remedies must be tested against the suspected origin of the failure.

::: {.chapter-transition}
Diagnosis supplies hypotheses, not proof.
The next chapter shows how to turn those hypotheses into comparisons—and how to decide what “better retrieval” means for the task at hand.
:::
::::

::: self-check
A known relevant paper uses *myocardial infarction* while the query uses *heart attack*. Is either expression necessarily OOV?

:   No.
    This is evidence of vocabulary mismatch: query and document use different lexical forms for related concepts.
    Either expression could be present in both the index and the model vocabulary.
    OOV asks whether a string is absent from a specified vocabulary, which is a different question.

A subword tokeniser can encode every piece of a new chemical identifier. What has that established—and what has it not?

:   It has established that the string is not literally OOV for that tokeniser.
    It has not established that the lexical index preserves the identifier, that the query and document are analysed consistently, or that the retriever has learnt a useful representation.
    Inspect those layers separately and keep an exact lexical route when identity determines relevance.

A retriever performs well on web questions but poorly on high-recall evidence searches even though every word is familiar. What should you investigate?

:   OOD transfer, especially task or relevance shift.
    The training pairs may have taught the model to find short answer-bearing passages rather than the broad set of studies a reviewer would judge eligible.
    Test that hypothesis on a local query and relevance set; vocabulary familiarity neither proves nor rules it out.
:::
