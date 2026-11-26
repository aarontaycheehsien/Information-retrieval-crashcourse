---
key: "library-practice"
kind: "chapter"
eyebrow: "Chapter 15"
meta: "About 19 min"
question: "What must libraries record, inspect, test and require?"
legacy_anchors: ["ch9"]
---

## Implications for library practice and tool evaluation {#library-practice}

::: {.stage-map on="query-transformation analysis first-stage fusion reranking presentation" controller="on"}
:::

::: chapter-orient
Most librarians will never train a retriever.
They will license one, teach with it, document searches performed in it, and be asked whether its results can be trusted.
The technical content of this book exists to make those four things possible.

Three consequences follow, and they are ordered by dependency.
A search must be documentable before it can be compared.
Retrieval must be inspectable before an explanation means anything.
And both must be required in advance, because neither can be relied on to arrive later in a product that was not built to expose them.
:::

::: {#implications-for-library-practice .legacy-anchor}
:::

The three sections below are not all aimed at the same reader.
The first two are for anyone who documents a search or teaches someone else to.
Recording what a system actually searched, and being able to say why a particular record appeared, are ordinary professional practice once a system rewrites queries on your behalf.
The third reads like procurement, and it is — but its questions are also what make a vendor’s answer legible to whoever *is* in the room at renewal.
Even if that is never you, the section is the shortest statement of what the preceding fourteen chapters were for.
It converts every distinction the book has drawn into something a library can ask for and check.

### Reproducibility depends on what is fixed—and what is recorded {#reproducibility-implication-title}

Librarians often use *reproducible* to mean that another searcher can understand what was done and rerun it.
No retrieval method guarantees an identical result set forever: database coverage, indexing, controlled vocabulary, ranking configurations and model versions can all change.

The useful question is therefore not simply “Is this search reproducible?” but:

> **Which parts of the retrieval pipeline were fixed, documented, exportable and versioned?**

Three practical points follow.

- **Reproducibility is conditional:** the same query does not guarantee the same records or the same ranking once indexes, models and configurations move.
- **Record what the system actually searched:** saving the natural-language question is not enough when the system generated a Boolean query, expansions, subqueries, hypothetical text or an agentic sequence.
- **Separate rerunning from comparison:** an exact future recreation may be impossible.
  A saved query, trace and exported result set still let a later run be compared against the original.

::: {.orientation tag="div"}
**Start with a record you can make today:** the input, product and mode, search date, visible transformation, filters, result identifiers and observed limitation.
Separate what you observed from what the vendor documents and what remains unknown.

The detailed tables below are a reference checklist.
Internal model versions and candidate budgets may require vendor disclosure; access to traces and change notices belongs in institutional procurement discussions.
:::

At minimum, a record should cover four areas of the pipeline:

| Pipeline area | What should be recorded |
|---|---|
| **Query interpretation** | Original input, transformed queries, extracted filters, expansion terms, and model or parser version |
| **Candidate retrieval** | Database or index and its version, fields searched, indexed unit, retriever, parameters and cut-offs |
| **Ranking and fusion** | Sort order, ranking method, component result lists, fusion rule, reranking stage and final *k* |
| **[Retrieval control](#agentic-search-who-chooses-the-next-retrieval-action)** | Which arrangement applies — fixed, adaptive or agentic. For an adaptive workflow, the branch taken and the rule that chose it. For an agentic one, every query executed, each tool or source selected, the observations returned, the sequence, and the stopping point |

: The four pipeline areas a reproducible search record must cover.

::: {.details .detail-drawer}
Detailed reporting requirements, method by method

What supports reproducibility differs by retrieval component, and so does what has to be written down.
This table expands each row of the summary above.

| Component or method | What supports reproducibility | What needs to be recorded |
|---|---|---|
| **LLM or NLP query interpretation** | A visible, editable and exportable transformation makes it possible to inspect what was actually searched. A fixed rule-based parser may be repeatable, but LLM-generated rewrites are not guaranteed to be identical across runs. | Original input; exact generated Boolean query, expansions, subqueries or hypothetical text; extracted filters; prompt or template; model and parser version; sampling settings and seed if exposed; retrieval route; and whether a rerun reused a saved transformation or generated a new one. |
| **[Agentic orchestration](#agentic-search-who-chooses-the-next-retrieval-action)** | Reproducibility requires a recorded run. Fixed and adaptive workflows can document their rules in advance, but adaptive branches and result-dependent queries still need a trace of which path was taken. An agentic trajectory is chosen per question, so nothing short of a recorded trace of the actual run describes what happened. Two runs of the same question may legitimately follow different paths. | Controller model and its instructions; the tools, indexes and sources it was permitted to use; every query actually executed and in what order; the retrieval route chosen for each; the intermediate results that informed each subsequent action; iteration and budget limits; the stopping decision; and the final retrieved identifiers. What is needed is an **action and observation trace**—what the system did and what came back—not the model’s narrated reasoning. |
| **Strict Boolean** | The query states hard inclusion and exclusion conditions explicitly. Given the same records, indexing, analyser and query interpretation, eligibility should be repeatable. | Exact query as run, database and platform, fields, limits, controlled-vocabulary version, search date and result count. A later rerun may differ because records and indexing have changed. |
| **Ranked lexical retrieval, such as BM25** | Matching terms and their contributions are inspectable. A fixed collection and scoring configuration can produce a repeatable ranking. | Everything required for Boolean searching, plus tokenisation and stemming rules, query rewriting, field weights, ranking configuration, sort order and *k*. Adding records changes term rarity and document-length statistics, so rankings can move even when the query is unchanged. |
| **Single-vector dense retrieval** | A fixed encoder, fixed indexed units, stored vectors, similarity function and exact search procedure can produce repeatable scores. Dense retrieval is not inherently random. | Model and tokeniser version, text and metadata embedded, chunking rules, corpus and index version, similarity function, filters, *k* or threshold, and whether search was exact or approximate. ANN parameters and index construction can affect candidates near the retrieval boundary. |
| **Learnt sparse retrieval** | Vocabulary-aligned dimensions make model-generated terms and weights more inspectable than pooled dense dimensions. | Model and tokeniser version, generated expansion terms and weights where available, index version, scoring configuration and *k*. Recording only the words typed by the searcher is insufficient because the model may activate additional terms. |
| **Late-interaction retrieval** | Token-level score contributions can show which query and document tokens aligned most strongly. | Model and tokeniser version, indexed-unit boundaries, index and compression version, similarity and MaxSim configuration, pruning or ANN settings, and *k*. Inspectable token alignments do not make the underlying contextual vectors portable between model versions. |

: Detailed reporting requirements by retrieval method.
:::

LLM-based rewriting adds a specific reproducibility risk.
Sampling settings can make generation deliberately variable.
Model updates, prompt changes and hosted inference infrastructure can affect outputs even when a temperature of zero or greedy decoding is used.
This does not mean that every LLM call must vary; it means that identical output should not be assumed unless the complete system provides and tests that guarantee.
A technical account of why deployed inference can vary is provided in [Thinking Machines Lab’s discussion of LLM nondeterminism](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/).

Across all methods, save the search date, reported count, retrieved identifiers and—where possible—a raw export, alongside the exact retrieval inputs described above.
A rerun may then be compared with the original even when the live database or model has changed.

>

This aligns with [PRISMA-S](https://pmc.ncbi.nlm.nih.gov/articles/PMC7839230/), which recommends reporting the complete strategy, database and platform, limits, dates and result counts, while recognising that some proprietary or similarity-based discovery operations may not be fully replicable.

[Appendix F](#appendix-evidence-synthesis-high-recall-retrieval) applies these reproducibility principles to systematic-review retrieval and active-learning screening.

::: {#interpretability-and-understandability-depend-on-seeing-the-retrieval-pipeline .legacy-anchor}
:::

### Interpretability requires an inspectable retrieval pipeline {#interpretability-requires-an-inspectable-pipeline}

Documentation records what was done.
It does not, on its own, explain why any particular record appeared.
Explaining is a separate property, and it needs separate vocabulary.

**Transparency** means that information about the system is exposed. **Interpretability** means that a librarian can trace why a record was included, excluded, scored or reranked. **Understandability** means that the librarian can form an accurate, usable mental model of the system without having to inspect every equation or model weight.

These qualities overlap, but they are not interchangeable.
A vendor can publish a broad description of its ranking system without making a particular result interpretable.
A detailed score display can still be hard to understand.
And a fully documented, rerunnable search can still leave the reason for an individual result opaque.

> **Can a librarian trace why a record was included, scored, reranked or excluded—and identify which parts of that account remain unknown?**

Three distinctions do most of the work in answering it.
A highlighted term is not necessarily the cause of a result.
A generated explanation is not necessarily a faithful execution trace.
And an explanation can be perfectly understandable without exposing a single model weight.

::: {.details .detail-drawer}
Detailed inspection by pipeline stage

Every stage can expose something useful, and every stage has a limit on what that exposure proves.
The second and third columns are worth reading together: the value of an explanation lies as much in what it rules out as in what it shows.

| Pipeline stage | What a useful explanation shows | What that explanation cannot establish by itself |
|---|---|---|
| **[Query parsing, rewriting, expansion and routing](#beyond-one-query-expansion-decomposition-and-routing)** | The original input, extracted concepts and filters, generated Boolean query, expansion terms or subqueries, and the retrieval route actually selected. | That a rewrite preserved the searcher’s intended question or that omitted alternatives would not have changed the result set. |
| **Boolean eligibility and filters** | Which clauses and metadata conditions a record satisfied, and which required clause or filter excluded it. | That every eligible record is relevant, or that every excluded record is irrelevant. |
| **[BM25 and other lexical scoring](#bm25-words-as-weighted-clues)** | The analysed query terms that matched, their field or proximity evidence where exposed, and the factors that contributed to the lexical score. | That a displayed score is a probability of relevance, or that an unshown production reranker did not change the final order. |
| **[Dense retrieval](#single-vector-dense-retrieval-compress-first-compare-later)** | The indexed unit, encoder and similarity function, the candidate rank or similarity, and whether approximate nearest-neighbour search was used. | A simple human-readable reason why a particular latent feature made one passage closer than another. |
| **[Learnt sparse and late interaction](#neural-ir-broader-than-dense-retrieval)** | Model-generated expansion terms and weights where available, or the query-token and document-token alignments that contributed to a late-interaction score. | That visible terms or alignments describe the whole model decision, rather than one inspectable layer of it. |
| **Fusion, reranking and presentation** | The candidate lists, component ranks or scores, fusion rule, reranker stage, cut-off and any deduplication, diversification or display rules. | That a highlighted word, generated rationale, citation count or attractive snippet caused the final position. |
| **[Agentic orchestration](#agentic-search-who-chooses-the-next-retrieval-action)** | Which tool or retriever was selected at each step, the query sent to it, what came back, which action was chosen next, and when and why the process stopped. | That the model’s account of its own reasoning caused those choices. A generated narrative may be a plausible description of a trajectory without being evidence of what drove it. |

: What an explanation can show at each pipeline stage, and what it cannot establish by itself.
:::

A faithful explanation is an **execution trace**: it is derived from the actual query, index, candidates and scoring path used for that result.
A plausible post-hoc explanation may still be helpful for orientation, but it should be labelled as an interpretation, not presented as proof of what the system used.
Highlighted words and generated rationales are especially easy to mistake for causal evidence.
They may only describe a result after it was chosen.

**What a useful inspection trail contains:**

1. **Original query:** what the searcher entered, including fields, limits and filters.
2. **Transformed query:** the parsed, expanded, decomposed or generated form actually sent onward.
3. **Candidate source:** which retriever, indexed unit and route supplied the record.
4. **Matched evidence:** Boolean clauses, lexical contributions, token alignments or other evidence the system can faithfully expose.
5. **Scoring and reranking:** the stages that ordered the candidate and any cut-offs or approximate-search settings that shaped the shortlist.
6. **Fusion and display:** how component results were combined and how deduplication, diversification, snippets or labels changed what the searcher finally saw.
7. **Trajectory, where the system is [agentic](#agentic-search-who-chooses-the-next-retrieval-action):** the sequence of actions actually taken—each query, each source, each route—together with the observations that informed the next step and the point at which searching stopped.

:::: {.figure .worked-figure key="rationale-versus-trace"}
A convincing explanation and a recorded search path

::: {.include src="figures/rationale-versus-trace.html"}
:::

::: caption
All record details and ranks are hypothetical.
In a real product, call these facts a trace only when they come from the executed search.
Separate observed evidence, vendor documentation and unknowns; a generated narrative must not fill gaps as though they were recorded facts.
:::
::::

:::: {.figure .query-flow key="inspection-trail"}
The same trail, walked backwards from the result

::: {.track}
- **Start at the record** the one you are being asked to explain
- **Fusion and display** did deduplication, a snippet or a label change what was seen?
- **Scoring and reranking** which stage put it here, and what cut-off shaped the shortlist?
- **Matched evidence** what did the system actually match on?
:::

::: {.track}
- **Keep going back** each step answers a different question
- **Candidate source** which retriever, route and indexed unit supplied it?
- **Transformed query** what was actually sent, as against what was typed?
- **Original query** where the searcher started, and the only step most products expose
:::

::: caption
The diagram follows an inspection backwards through the recorded search path: from a displayed record towards the query and operations that supplied it.
This is the inspection order, not the system’s execution order.
Where the trail stops is the useful measure of a product: one that can show a matched term but not the transformed query has answered a question you did not ask.
:::
::::

This is also why a short explanation need not expose every engineering detail.
The aim is an accurate mental model and an actionable audit trail: enough information to diagnose an unexpected result, compare retrieval routes and recognise the limits of the explanation.

> **A search can be reproducible yet poorly understood if the saved query and identifiers do not reveal how records were selected or ranked.
> A clear-looking explanation does not make a search reproducible unless the relevant inputs, versions and outputs can also be recorded and rerun.**

::: {#what-to-ask-when-choosing-a-search-tool .legacy-anchor}
:::

### Choosing and governing search tools {#choosing-and-governing-search-tools}

A library licenses a retriever, or licenses a database containing one, so documentation and inspection are not only personal practices: they are things a library has to require in advance.

The [printable vendor questionnaire](vendor-questionnaire.html) gathers the nineteen questions below, with spaces for answers, evidence, library verification and follow-up.
Optional sections add the specialist prompts from Appendices E and G.

When a product advertises semantic, natural-language or AI search, the distinctions above become six groups of procurement and evaluation questions.
Vendor answers will arrive in vendor vocabulary; [Appendix D](#appendix-search-terminology) is a crosswalk from those labels to the mechanisms below, and is worth having to hand while the questions are being asked.
For products that also generate answers, [Appendix G](#appendix-rag-questions) adds the RAG-specific questions to this list.

::: {#vendor-inputs}
Before comparing query boxes, ask what the product accepts as a retrieval starting point.
Only text, or also controlled fields, a seed record, citation links, saved judgements and API predicates?
For an agentic mode, ask whether both the task brief and the queries generated from it can be exported.
An attractive text box may conceal that the product narrowed the search method before ranking began.
:::

##### Query interpretation, transformation and control {#vendor-group-1}

1. []{#vendor-q01 .li-id}**What does the system infer, change and decide?** Does it recognise fields, filters or intent without changing the input; correct, map, expand or generate retrieval inputs; choose retrieval routes; or construct a later query from earlier results?
   Can users inspect and export the interpretation, every transformed input, each route and any feedback records?

2. []{#vendor-q02 .li-id}**[Who controls the retrieval trajectory?](#agentic-search-who-chooses-the-next-retrieval-action)** Is the sequence fixed in advance, chosen from branches the designer enumerated—whether a rule, a classifier or a model picks the branch—or planned by a model from what it has observed?
   If a model chooses, what tools, sources and iteration limits bound it?
   Can users see every query it ran, every source it consulted, every route it took and the point at which it decided to stop?

##### Retrieval coverage and architecture {#vendor-group-2}

3. []{#vendor-q03 .li-id}**Which retrieval and ranking components are used?** Is there direct string/pattern search, indexed Boolean retrieval, BM25-like lexical ranking, dense retrieval or reranking?
   Do the components operate [in parallel, sequentially or both](#why-search-systems-use-multiple-stages), how many candidates survive each cut-off, and does the system select components by query or always combine them?

4. []{#vendor-q04 .li-id}**What role does the neural model perform?** Naming a model does not describe an architecture.
   Is it parsing or rewriting the query, producing the first-stage query and passage vectors, expanding the vocabulary of a sparse index, jointly reranking candidates, or generating the final answer?
   These are [different jobs with different failure modes](#how-a-contextual-encoder-becomes-a-retrieval-encoder), and a model can be present without doing the one you assumed.

5. []{#vendor-q05 .li-id}**What is the searchable unit?** Is the system indexing or directly scanning titles, abstracts, passages, sections or complete articles?
   For file search, which paths, formats and exclusions apply, and how is text extracted?
   A product whose index holds only abstracts cannot match evidence that occurs only in the full text at that retrieval stage, however sophisticated its vectors are.
   Ask separately whether it later fetches the full text, and what it passes on as context.

6. []{#vendor-q06 .li-id}**How are passage results assembled?** If five chunks from the same paper match, are their scores combined, is only the best retained, or are five near-duplicate results shown?

7. []{#vendor-q07 .li-id}**[How is the hybrid combined?](#why-hybrid-retrieval-remains-attractive)** A product may call itself hybrid because it contains two retrievers even when one signal rarely affects the final ranking.
   Ask where component lists are fused, whether a later stage reranks the merged candidates, what cut-offs apply, and whether users can inspect, compare or control the component result sets.

##### Exactness and failure testing {#vendor-group-3}

8. []{#vendor-q08 .li-id}**Is exact lexical matching retained?** Can users search identifiers, chemical strings, gene names, dataset titles and quoted phrases without semantic expansion quietly changing the task?

9. []{#vendor-q09 .li-id}**How is text tokenised and analysed?** Ask how the lexical path treats case, punctuation, hyphens and identifiers, and whether query and document analysis are compatible.
   For a dense model, ask whether it uses word, subword, character or byte inputs and how unfamiliar or newly coined strings are tested.

10. []{#vendor-q10 .li-id}**How are exactness, negation and exclusions tested?** Ask for examples involving identifiers, contradictory claims, `NOT`-like intent and near-duplicate names — not only attractive paraphrase demonstrations.

11. []{#vendor-q11 .li-id}**What trained the relevance model?** Web queries, question–answer pairs, citation links and scholarly relevance judgements teach different behaviours.
    How was the model adapted to the disciplines and document types being searched?

##### Auditability and repeatability {#vendor-group-4}

12. []{#vendor-q12 .li-id}**Can users inspect why a result appeared?** Can they move from the displayed record backwards through the retrieval route, transformed inputs, inferred constraints, any feedback records, matched evidence, ranking or reranking stages, and final fusion or display rules?
    Does the product distinguish a faithful execution trace from a helpful but post-hoc explanation?

13. []{#vendor-q13 .li-id}**Can the search be documented and rerun?** Can users export the original input; exact generated Boolean query, filters, expansions, subqueries or hypothetical text; retrieval route; ranking mode; model version; index date or file snapshot; *k* or threshold; retrieved identifiers; and, for file-search agents, executed patterns, searched paths, output limits, passages read and stopping conditions?
    When the same search is rerun, does the system reuse the saved transformation or ask an LLM to generate it again?

14. []{#vendor-q14 .li-id}**Are model, index and ranking changes disclosed?** Does the vendor announce when an update may change results a user previously obtained, and is there any way to tell after the fact which version produced a saved search?

##### Cost, limits and continuity {#vendor-group-5}

15. []{#vendor-q15 .li-id}**What does a search cost, and what limits apply?** Is pricing per seat, per query or per token?
    What are the rate and iteration limits, and what happens when one is reached — a refusal, a truncated result, or a silently shallower search?
    Does an agentic mode cost differently from the ordinary one, and can the library see per-query consumption? [Chapter 12](#what-agency-costs-and-what-it-buys) makes cost half of the agency trade; a product that cannot report it has settled that trade on your behalf.

16. []{#vendor-q16 .li-id}**What happens when a mode is retired?** Can saved searches, saved sets and stored traces be exported before a mode is withdrawn, and how much notice is given?
    Chapter 12 records both kinds of change: Ai2's [Paper Finder became Asta Find Paper](#fixed-adaptive-and-agentic-are-not-the-same-thing), and [Table 12.3](#where-current-academic-tools-actually-sit) distinguishes Undermind's original deep search from Undermind Projects.
    A search documented under a mode that no longer exists is not reproducible in any sense the library can act on.

##### Institutional evaluation {#vendor-group-6}

17. []{#vendor-q17 .li-id}**How is performance evaluated, and on whose queries?** Average benchmark scores can hide failures on the query types that matter locally.
    A serious evaluation uses the institution’s own disciplines, vocabulary, languages, document types and known relevant records.

18. []{#vendor-q18 .li-id}**Are failure cases part of the evaluation?** A vendor’s demonstration shows what the system does well.
    The searches that matter for procurement are the ones a library already knows to be difficult.

19. []{#vendor-q19 .li-id}**Can the library compare behaviour across an update?** If a saved set of local test queries can be rerun after a model, index or ranking change, a library can detect a regression that no release note mentions.

None of these questions requires reading a loss function.
All of them distinguish a retrieval design from a marketing label.

Libraries do not need access to every model weight or engineering detail.
They need enough visibility to establish what was actually searched, enough documentation to rerun or compare it later, and enough control to test it against their own collections and users.

The tokeniser may be able to encode every piece of the query.
The source article may be divided into sensible chunks.
Each chunk may receive a dense vector, while a separate lexical system indexes its analysed terms.
The final results may blend both signals.

That still does not mean the retrieval system has any rizz.

::: chapter-close
1. Reproducibility is conditional on a fixed system, and it is also a documentation practice rather than a property of a method.
2. Saving the natural-language question is insufficient whenever the system rewrote it.
3. A faithful explanation is an execution trace.
   A plausible narrative is not evidence of what drove a result.
4. Documentation and inspection cannot be assumed to arrive later.
   A vendor may add them, but a product that was not built to expose what it searched will not do so on a library’s timetable, which is why these are procurement questions rather than support tickets.
5. The questions that separate a retrieval design from a marketing label need no mathematics — only the distinctions this book has drawn, and the willingness to ask which one a vendor’s word names.
6. Libraries do not need model weights.
   They need enough visibility to establish what was searched, enough documentation to compare it later, and enough control to test it locally.
:::

::: self-check
A search is fully documented and can be rerun. Does that make it interpretable?

:   No.
    Documentation records what was done.
    Interpretability is being able to trace why a particular record was included, scored, reranked or excluded.
    A search can be perfectly reproducible while the reason for any individual result stays opaque — they are separate properties needing separate questions.

A tool displays a generated explanation of why a paper was returned. What must you establish before treating it as evidence?

:   Whether it is a faithful execution trace — derived from the actual query, index, candidates and scoring path used for that result — or a plausible account written afterwards.
    A highlighted word or a fluent rationale can describe a result convincingly without having caused it.

Short of model weights and engineering detail, what is the minimum a library actually needs?

:   Enough visibility to establish what was actually searched; enough documentation to rerun or compare the search later; and enough control to test the system against its own collections, disciplines and users.
    None of that requires reading a loss function.
:::
