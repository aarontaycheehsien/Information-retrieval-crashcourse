---
key: "query-transformation"
kind: "chapter"
eyebrow: "Chapter 11"
meta: "About 20 min"
question: "What are you giving the system, what mechanism receives it, and what can happen before the next retrieval pass?"
legacy_anchors: ["ch6"]
---

## Understanding, transforming and routing queries {#query-transformation}

::: {.stage-map on="query-transformation" controller="on" label="Pipeline map: the stages this chapter covers are highlighted"}
:::

::: chapter-orient
Chapter 4 separated interpreting a request from changing its retrieval input.
Chapters 9 and 10 then added several retrievers, fusion and route selection.
Together they allow a system to do more than rewrite one lexical query into another.

Search can start from a seed paper, citation relationship, relevance judgement or structured condition as well as free text.
This chapter examines which component receives each input, how the input may be transformed, and how earlier results can inform a later search.
:::

::: {#beyond-one-query-expansion-decomposition-and-routing .legacy-anchor}
:::

::: {#query-understanding-changing-the-query-before-retrieval .legacy-anchor}
:::

[Chapter 4’s](#words-sent-to-retrieval-may-not-be-the-words-you-typed) distinction now has three parts. **Query understanding** interprets the request and may leave the retrieval input unchanged. **Query transformation** changes or creates retrieval inputs. **Retrieval control** chooses where those inputs go, whether several paths run, and whether another search happens.

These operations are often grouped loosely under *query understanding*, but they do not occupy one pipeline stage.
Interpretation may trigger transformation, a routing decision or both.
Most transformations occur before a retrieval pass, while feedback methods construct a later query from the results of an earlier one.

::: {#distinction-query-object .key-distinction-label}
Key distinction
:::

### Before phrasing: identify the query object {#before-phrasing-identify-the-query-object}

Keywords, questions and prompts are text inputs.
Where the system’s design is known, choose wording for the component that will receive it.
Also consider whether a seed paper or another query object would suit the task.
Where the design is undisclosed, compare input forms against known relevant records.

> A query represents some aspect of the need in [a form a retrieval system can act on](#distinction-match-relevance).
> Depending on the system, that representation might be keywords, a natural-language question, a seed document, a citation, an embedding, retrieval feedback or another object.

Read the query objects in three groups: text and structured conditions; known records and relationships; and feedback, monitoring or delegated tasks.
The table keeps the exact distinctions available for reference.

::: {.table scope="col"}
| What stands for the need | Mechanism addressed | What changes in practice |
|---|---|---|
| **Free-text string** | Lexical, dense or hybrid retrieval | Terms, phrases or prose become the retriever’s input. The visible box does not reveal whether the system will analyse words, encode a vector, rewrite the text or run several routes. |
| **Controlled term or structured expression** | Subject headings, named fields, proximity, filters or Boolean logic | The query addresses the record’s annotation and database structure. A MeSH heading, field tag or tested search hedge is not merely a more formal keyword. |
| **Citation edge** | Backward and forward citation traversal, co-citation or bibliographic coupling | Citation searching follows relationships between papers. It can reach work whose vocabulary the searcher did not anticipate, but it inherits gaps and delays in the citation graph. |
| **Seed document** | Query by example using text similarity, citation relations or both | The known paper stands for the need. For example, [PubMed Similar Articles](https://pubmed.ncbi.nlm.nih.gov/help/#similar-articles) compares title, abstract and MeSH words with a word-weighted algorithm; another system could instead use embeddings or a citation graph. |
| **Relevance judgement** | Explicit retrieval feedback or pseudo-relevance feedback | A later retrieval input is constructed from records accepted or rejected after an initial search, so the next pass may add candidates. The two sources differ: explicit feedback uses the searcher’s own judgements, whereas pseudo-relevance feedback asks the searcher for nothing and instead assumes that its own highly ranked records are relevant—an unverified assumption that can strengthen either a useful signal or an early mistake. |
| **Browse or monitoring target** | Journal, author, subject or collection browsing; saved-search alerts | The search follows collection structure or a continuing relationship. It can surface a record the searcher could recognise but could not yet name. |
| **Programmatic predicate** | API filters, identifiers, sorting and pagination | The request becomes reproducible and composable. The [OpenAlex API](https://help.openalex.org/api/filtering/), for example, documents attribute–value filters, intersections, negation, ranges and identifier lists. |
| **Task brief** | An agentic controller that generates and sequences later queries and tool calls | Scope, inclusion and exclusion criteria, sources, coverage, stopping conditions and output requirements belong here. They instruct the controller; they are not all terms that each underlying retriever knows how to obey. |

: The query object determines which retrieval mechanism the search addresses.
:::

Take the question behind Puzzle 3—*is there an open access citation advantage?*—and approach it through each of the eight query objects below.

:::: {.figure key="one-need-eight-objects"}
One information need, eight ways in

::: {.include src="figures/one-need-eight-objects.html"}
:::

::: caption
The eight rows of the table above, worked against the question behind [Puzzle 3](#three-familiar-search-results-and-three-puzzles): *is there an open access citation advantage?* Every box represents the same need, and none of them is a rephrasing of another—each addresses a different mechanism, reaches a different part of the literature, and fails in a different way.
Only the first is what most advice about “how to phrase a search” is actually about.
The eight are overlapping distinctions rather than mutually exclusive input types: an API request can carry a free-text query, and a seed document can initiate citation traversal.
:::
::::

For the API example, a filter on the retrieved paper’s open-access status would change this search, since a relevant study of the open-access citation advantage may itself be paywalled—which is why the example filters by year instead.

Active-learning screening in systematic reviews uses relevance judgements too, but it is **screening feedback** rather than the retrieval feedback shown in Table 11.1.
Inclusion and exclusion judgements repeatedly reprioritise the remaining records inside an existing candidate pool; they do not construct a later retrieval pass or inherently add candidates.
See [Appendix F](#appendix-evidence-synthesis-high-recall-retrieval).

#### Using several query objects together {#using-several-query-objects-together}

These objects cooperate.
Free-text and controlled-vocabulary searches can find seeds; citation traversal can expose missing terminology; accepted records can drive a feedback pass; an API can make the resulting procedure repeatable.
This is especially important when recall matters.

In one audit of a single review of complex evidence, Greenhalgh and Peacock traced 495 included sources: only 30% came from the protocol-defined database and hand searches, while 51% were found by snowballing.
That result is not a universal estimate for every review.
It is a concrete demonstration that one well-phrased database query may still cover only one route to the literature.

Seed-based methods also differ from one another.
Direct citations follow an explicit edge.
Bibliographic coupling finds papers that share references; co-citation finds papers cited together; text similarity compares their language or representations.
Sjögårde and Ahlgren’s 2024 evaluation found that combined citation approaches generally retrieved more relevant publications than any one citation relation, and that adding PubMed’s text-based related-article score improved the combination on some measures.

This wider view also explains why real searching is iterative.
Bates called the pattern *berrypicking*: the need and the useful query develop as the searcher encounters documents, authors, citations and terminology.
What changes between steps may therefore be the words, the seed, the graph edge, the judged examples or the source being browsed.
Describing these steps only as changes to query wording leaves out the papers, citation links and relevance judgements used to guide the search.

### Choosing wording for each receiving component {#phrase-for-the-mechanism-not-the-box}

When a string really is the query, its useful form depends on what will read it.
A polished paragraph is not intrinsically more semantic than a short term list, and a keyword string is not intrinsically more reproducible than a visible structured expression.

::: {.table scope="col"}
| Receiver | Useful input | Do not assume |
|---|---|---|
| **Lexical or Boolean retriever** | Observable concepts, variants, phrases, controlled terms, fields and tested operators | Extra explanation becomes background understanding. It may simply add optional or required words. |
| **Dense retriever** | A concise description resembling the information need the model was trained to match | Longer prose is always better. Verbose queries can dilute the central signal, and effectiveness depends on training and domain (Gupta and Bendersky, 2015). |
| **LLM query translator** | Concepts, constraints and enough context to produce inspectable retrieval inputs | The generated syntax is valid or complete. Validate fields, controlled terms, logic and recall in the target database. |
| **Agentic controller** | A brief specifying goal, scope, criteria, sources, coverage, limits, stopping and required record | Every retriever receives or follows the whole brief. Ask for the generated queries, chosen routes and stopping trace. |
| **Undisclosed pipeline** | Queries varied systematically against known relevant records | The shape of the input box identifies the mechanism. Test short terms, a question, fielded syntax and a known-item title separately. |

: The useful form of a text input depends on its receiver.
:::

Research on automated query construction reinforces the distinction.
In systematic-review screening, Wang and colleagues found that converting Boolean strategies into natural-language queries could improve a neural ranker, while fusion with the original Boolean results helped in some settings and not in others.
In a separate evaluation of LLM-generated Boolean strategies, outputs varied and could contain invalid MeSH terms.
Meanwhile, the FollowIR benchmark found that existing retrieval models often treated detailed relevance instructions as basic keywords and struggled with the long-form information; instruction-following improved after targeted training.

The findings do not support a general rule that longer or more natural-language queries work better.
Use [Table 11.2](#tbl-11-2) to choose an input format for the component receiving it.
Inspect any generated query, then test input variants against known relevant records.

> The input box does not tell you what object the system will construct from your input, which mechanism will receive it, or which other search method should run alongside it.

For [grep](#grep-searching-text-directly), the receiving component expects a literal string or regular expression.
A model may translate the task into several such patterns, but each call still matches text. [Chapter 12](#agent-grep-search) follows that distinction through a search sequence.

### What a system can do with your query {#common-query-understanding-techniques}

Figure 11.2 sets out what can happen to a text input before, and between, retrieval passes; the subsections below take the steps in turn.

:::: {.figure .query-flow key="query-understanding-flow"}
For a text input, interpretation can change retrieval inputs or retrieval decisions

::: {.track}
- **Text input** keywords, a question or a longer description
- **Interpret the request** recognise phrases, entities, intent, dates or constraints
- **Transform or route** change the input, choose a path or run several paths
- **Retrieval** Boolean, BM25, dense or another first-stage method
:::

::: {.track}
- **Initial results** a first retrieval pass supplies ranked records
- **Optional feedback** select terms or evidence from those results
- **New retrieval input** construct a second query from the feedback
- **Later results** run another retrieval pass
:::

::: caption
This figure follows the text-input path only.
The first row separates interpretation, changed retrieval inputs and route selection.
The optional second row shows why pseudo-relevance feedback is not purely upstream: an initial ranking helps construct a later query.
Neither arrangement identifies the retriever or makes the workflow agentic.
:::
::::

#### When a system writes the Boolean query {#when-a-system-writes-the-boolean-query}

A search interface can use an NLP parser[^nlp-parser] or a language model to turn a natural-language request into fields, filters and Boolean clauses before retrieval.
For example, Web of Science Smart Search makes its interpretation visible:

:::: {.figure key="web-of-science-smart-search" aria-labelledby="web-of-science-smart-search-caption"}
Web of Science Smart Search makes the transformation visible

![Web of Science Smart Search translating a natural-language request about dates, affiliation, apples, oranges and bananas into a structured fielded query](images/11%20Query%20understanding%20-%20changing%20the%20query%20before%20retrieval/web-of-science-smart-search-structured-query.png){width="1167" height="318"}

::: {#web-of-science-smart-search-caption .caption}
The interface translates “apple oranges bananas from 2020 to 2024, affiliation is from university of california” into `PY=(2020-2024) AND OG_SMART=(university of california) AND TS=(apple) AND TS=(oranges) AND TS=(bananas)`.
Dates and organisation become filters; the topics become separate conditions.
:::
::::

[Primo NDE Natural Language Search](https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_%28English%29/040Search_Configurations/Natural_Language_Search_in_the_NDE_UI) likewise documents classifying the input, generating a Boolean query and expanding it into `OR`-connected permutations.
In both products, the generated query remains visible and editable.

Primo VE NDE Natural Language Search is distinct from the [Primo Research Assistant](https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_%28English%29/015_Getting_Started_with_Primo_Research_Assistant) discussed earlier, which documents an LLM converting a question into Boolean variations before CDI retrieval and [embedding reranking in a multi-stage pipeline](#why-search-systems-use-multiple-stages).

The transformation changes what is sent to retrieval, not necessarily the retriever.
Natural-language input may still lead to Boolean admission and lexical ranking; visibility matters because an omitted concept or misread constraint changes the candidate set before ranking.

#### What changed, and when {#what-changed-and-when}

The useful questions are what the system changed and when.
The operations below can be combined, and they are not mutually exclusive.

| Operation | Typical effect or examples | When it happens | Main risk |
|---|---|---|---|
| **Interpret the request** *([example above](#when-a-system-writes-the-boolean-query))* | Recognises phrases, entities, dates, languages, document types, intent or proposed constraints. The interpretation may inform a later step without changing the retrieval input. | Before retrieval | A misclassification can trigger the wrong transformation or retrieval decision. |
| **Correct, map or expand** *([met earlier](#words-sent-to-retrieval-may-not-be-the-words-you-typed))* | Correction may replace `autsim` with `autism`; mapping translates a term into controlled vocabulary or another representation; expansion adds variants, synonyms or related concepts. | Before retrieval | A wrong replacement changes the request; weak additions cause topic drift. |
| **Create alternative retrieval inputs** | Decomposes a request, generates several reformulations, or creates pseudo-document text through Query2doc or HyDE. | Before retrieval | Relationships may be lost, one formulation may dominate, or generated details may steer retrieval. |
| **Use retrieval feedback** | Pseudo-relevance feedback runs an initial search, selects terms from highly ranked records and uses them to construct a second search. | After an initial retrieval | Off-topic initial results can reinforce the mistake. |
| **Route retrieval** | Chooses one keyword, Boolean, dense or hybrid path for the request. | Around retrieval | A hidden choice can make a relevant route—and its records—unreachable. |
| **Coordinate retrieval** | Runs several queries or retrievers, then combines their lists through the [fusion machinery of Chapter 10](#why-hybrid-retrieval-remains-attractive). | Around retrieval | One path may be overrepresented, while hidden fusion rules obscure why a record moved. |

: What a system can do with a query, when it happens and the main risk it introduces.

Pseudo-relevance feedback constructs a later query from the results of an earlier retrieval pass.
Yet a workflow that always performs those two passes can still be fixed and non-agentic: the query contents adapt to the results, while the sequence was prescribed in advance.

A system might identify a date filter, generate three reformulations, send each to lexical and dense retrievers, fuse their candidate lists and rerank the result.
Calling the interface “natural-language search” reveals none of those internal decisions.

::: {.common-confusion label="Representation boundary"}
**Not every apparent expansion is query transformation.** [SPLADE](#learnt-sparse-representations) can assign weight to terms the searcher never typed, but what it produces is a weighted vocabulary representation, whereas an LLM rewrite produces text or a structured expression.
Both outputs can be inspected, and either can be passed between components—[Elicit’s described SPLADE approach](#neural-ir-broader-than-dense-retrieval) feeds expanded terms to a full-text engine—so a component boundary is not what separates them.
They are different forms of retrieval input.
Product descriptions may call either query enrichment or expansion.
:::

### Query2doc and HyDE: generating text to retrieve text {#query2doc-and-hyde}

[**Query2doc**](https://aclanthology.org/2023.emnlp-main.585/) prompts an LLM to generate a pseudo-document and uses its language to expand the original query.
The expanded text can help a sparse retriever such as BM25 by supplying vocabulary likely to appear in relevant documents, and it can also be used with dense retrieval.

[**HyDE**, short for Hypothetical Document Embeddings](https://aclanthology.org/2023.acl-long.99/), uses a related idea differently.
An LLM writes a hypothetical document that might answer the query.
A dense encoder embeds that generated document, and the system retrieves real documents whose vectors are nearby.

> **HyDE searches from the vector of an imagined relevant document.
> The imagined document is a retrieval aid, not evidence.**

Query2doc uses generated language to enrich a query; HyDE uses a generated document as a pivot into a dense vector space.
Generated text can help retrieve relevant documents, but invented details can also steer the search towards unsuitable material.
Retrieval grounds the search in real indexed documents, but it does not retroactively make every detail in the generated text true.
Multi-query generation is also the front half of the RAG Fusion pipeline examined in [Appendix G](#appendix-rag-scopus): there the generated variants are all retrieved against, and their ranked lists fused, rather than one being chosen.

:::: {.figure .worked-figure key="query2doc-hyde-paths"}
Generated text takes two different routes to real sources

::: {.include src="figures/query2doc-hyde-paths.html"}
:::

::: caption
Both methods generate a retrieval aid.
Query2doc adds its language to the query; HyDE searches from its embedding.
Either can import unsupported assumptions, so retain the generated text in the search record.
:::
::::

### Query interpretation and transformation in current discovery products {#query-understanding-in-current-discovery-products}

Current research products illustrate different combinations of interpretation, transformation and retrieval.
In each case the useful question is what the system inferred, what retrieval input it produced and what machinery received that input.

| Product | How it interprets or transforms the input | Retrieval arrangement | What it illustrates |
|---|---|---|---|
| [**Web of Science Smart Search**](https://webofscience.zendesk.com/hc/en-us/articles/32587676013713-Smart-Search) | An NLP parser identifies entities and constructs a structured Web of Science Boolean query. | Document search can run a Boolean keyword path and a semantic-vector path, then blend their results. | One interface can combine conventional query parsing, Boolean retrieval and vector retrieval. |
| [**EBSCOhost and EDS AI-Assisted Search**](https://about.ebsco.com/artificial-intelligence/products/ai-assisted-search) *(formerly Natural Language Search)* | AI parses the input into keyword and noun phrases. | The parsed query is sent to EBSCO’s established search engine, which applies its usual relevance ranking and specialist search functions. | AI query parsing can be added upstream of an existing retrieval engine; EBSCO’s public product page does not identify the model as an LLM. |
| [**Primo VE NDE Natural Language Search**](https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_%28English%29/040Search_Configurations/Natural_Language_Search_in_the_NDE_UI) | GPT-4.1 Mini identifies fields and filters, generates a basic Boolean query, then creates six related OR-connected permutations. | Primo’s Advanced Search receives the resulting structured Boolean query; users can inspect and edit the generated query. | Generative AI can produce an auditable Boolean search rather than directly replacing lexical retrieval. |

: Query interpretation and transformation in current discovery products, and what each case illustrates. [Vendor documentation checked August 2026.]{.as-of}

##### Natural-language filter extraction is useful but limited {#natural-language-filter-extraction-is-useful-but-limited}

Some academic search tools can also recognise a limited set of constraints in a natural-language request, then turn them into fields, filters or refinements.
Recognition is query understanding; constructing the fielded or filtered input is transformation.
Neither operation is equivalent to supporting every filter, field tag or complex Boolean relationship available in the underlying database.
A comparative review in [Katina Magazine](https://katinamagazine.org/content/article/reviews/2025/deep-dive-into-three-ai-academic-search-tools) illustrates these differences, while the product documentation defines the currently supported controls:

| Product | Constraints it can infer from natural language | Documented boundary |
|---|---|---|
| [**Web of Science Research Assistant**](https://webofscience.zendesk.com/hc/en-us/articles/31437630410129-Web-of-Science-Research-Assistant) | Document requests can include constraints such as an institution, country or region, publication year or recency, and requests for highly cited or seminal papers. | Its guidance treats these as supported query patterns, but lists complex field-tagged Boolean queries as unsupported. Natural-language filter handling is therefore useful without being a replacement for the complete advanced-search language. |
| [**Primo VE NDE Natural Language Search**](https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_%28English%29/040Search_Configurations/Natural_Language_Search_in_the_NDE_UI) | It can recognise identifiers, author and title-related fields, resource type, online availability, peer-reviewed or open-access status, holdings, creation date and requested language. | The recognised fields and facets come from a defined list. Ex Libris also documents known failures in author detection and cases where fields may be joined with `OR` instead of the intended relationship. |
| [**Primo Research Assistant**](https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_%28English%29/015_Getting_Started_with_Primo_Research_Assistant) | A question can request online availability, books, journal articles or peer-reviewed material, and a preset or custom date range. | Auto-refinement is confined to these supported categories. If a user manually changes a refinement, that field switches to manual mode and is no longer inferred automatically for the query. |

: Natural-language filter extraction across products, with the documented boundary in each case. [Vendor documentation checked August 2026.]{.as-of}

The practical lesson is to distinguish **query-derived filters** from filters the user selects explicitly after retrieval.
Evaluators should test which natural-language formulations activate each supported constraint, whether the generated filter is visible, and what happens when the request contains an unsupported or ambiguous limit.

These examples are not one natural-language architecture.
A product may interpret with a conventional parser or generative model, transform the input into a structured query, and then use Boolean, lexical, vector or hybrid retrieval.
The interface label alone does not reveal which operations occurred.

::: pull-quote
> Understanding interprets the request.
> Transformation changes what a retrieval pass receives.
:::

This is especially important for evidence searches.
A rewrite, compulsory clause, filter or route can [exclude a relevant document before ranking](#why-search-systems-use-multiple-stages); feedback can also reinforce an unrepresentative first ranking.
Evaluation and reporting should therefore distinguish the original input, every transformed input, the selected routes and any intermediate results used to construct a later query.

All of these operations can appear in a non-agentic workflow.
A designer can prescribe five reformulations, two retrievers, one fusion rule and one reranker in advance—even the two-pass feedback workflow above. [Chapter 12](#fixed-adaptive-and-agentic-are-not-the-same-thing) asks the separate question: who chooses what happens next?

:::: chapter-close
1. The useful question comes before phrasing: what object stands for the information need, and what mechanism will receive it?
2. Free-text strings, controlled expressions, citation edges, seed documents, relevance judgements, browse targets, API predicates and task briefs address different mechanisms.
3. Query understanding interprets a request and may or may not change what retrieval receives.
4. Transformation creates changed or additional retrieval inputs; routing and coordination control which retrieval paths use them.
5. Pseudo-relevance feedback constructs a later query from an initial ranking.
   It is retrieval-dependent, but a prescribed two-pass workflow need not be agentic.
6. Query2doc and HyDE use generated text differently, which makes that text part of the search strategy and part of what must be recorded.
7. Natural-language filter extraction is useful and reliably partial.

::: {.chapter-transition}
Interpretation, transformation, routing and feedback can all be arranged in advance.
Part III asks who chooses the next action while a search is running.
:::
::::

::: self-check
A researcher types a polished question, follows a citation from one relevant paper, and asks an agent to search until three named databases have been covered. Which three different kinds of input are involved?

:   The question is a text query, the citation is a graph edge used for traversal, and the coverage instruction is part of a task brief to the controller.
    Treating all three as phrasing styles would hide the different mechanisms they address.

Why can pseudo-relevance feedback not be described as an entirely upstream stage? Does using feedback make the workflow agentic?

:   PRF needs an initial ranking before it can select terms and construct a second query, so it includes a retrieval-to-transformation feedback loop.
    No: a system can be programmed to run those same two passes every time.
    The second query adapts to the first results, while the control sequence remains fixed.

Is SPLADE’s expansion the same kind of operation as an LLM generating three reformulations of a query?

:   No—though not because one is inspectable and the other is not.
    The LLM produces alternative retrieval inputs as text.
    SPLADE produces a weighted vocabulary representation, whose activated terms can also be listed.
    Either can be handed to another component, so what separates them is the form of the retrieval input, not where a component boundary falls.

Query2doc and HyDE both generate text. How do they differ, and what risk do they share?

:   Query2doc uses the generated language to expand a query for a lexical or dense retriever; HyDE embeds the generated document and retrieves real documents near that vector.
    Both can import invented details that steer retrieval, so the generated text—not only the user’s question—belongs in the search record.
:::

[^nlp-parser]: **NLP parser** here means a rule-based or statistical natural-language-processing component rather than a generative model.
    Such a system runs a pipeline — tokenisation, part-of-speech tagging, syntactic or dependency parsing, and named-entity recognition — to identify the concepts, populations, dates and document types in a typed question, then applies mapping rules or templates that attach synonym lists, controlled-vocabulary terms and field tags, and assembles them into a Boolean expression.
    Clinical query builders and PICO-style form interfaces work this way, and many production systems now combine both approaches.
    The practical difference from an LLM is repeatability: a fixed parser applies the same rules to the same input and returns the same query, whereas an LLM generates the expression afresh and may return a different one on a later run.
    Either way the transformation decides the eligible set before ranking begins, which is why the generated query should be visible and exportable.
    For the underlying techniques, see Daniel Jurafsky and James H.
    Martin, [*Speech and Language Processing*](https://web.stanford.edu/~jurafsky/slp3/).
