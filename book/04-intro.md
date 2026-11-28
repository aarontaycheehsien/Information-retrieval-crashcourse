---
key: "intro"
kind: "chapter"
eyebrow: "Chapter 1"
meta: "About 17 min"
question: "When an academic AI search tool hands you an answer with citations, what decided which papers were supplied as evidence?"
---

## The retrieval problem {#intro}

::: chapter-orient
### An answer appears {#an-answer-appears}

As documented in September 2026, a student signs into the library discovery layer, opens Primo Research Assistant and asks, in plain English, “Is there an open access citation advantage?”
The panel shows five article cards under Sources, followed by an Overview of sources with numbered inline citation markers—the visible answer assembled from the selected records.
:::

:::: {.figure key="primo-ra-opening-caption" title-id="" aria-labelledby="primo-ra-opening-caption"}
Primo Research Assistant: five sources and an overview

![Primo Research Assistant showing the question is there an open access citation advantage, five source cards and an Overview of sources with numbered citation markers](images/primoresearchassistant.png){width="1357" height="919"}

::: {#primo-ra-opening-caption .caption}
**Primo Research Assistant’s visible answer surface.** The panel shows five article cards under Sources and an Overview of sources with numbered inline citations.
The screenshot establishes what the interface presents, not how the records were selected.[Screenshot checked September 2026.]{.as-of}
:::
::::

::::: {.details}
Optional comparison: the Scopus AI answer surface

Ask Scopus AI the same question and the furniture changes.
In the supplied screenshot, Scopus AI presents a Deep research report headed “Open access citation advantage”, with a quick-reference/key-findings table, supporting citation links and a follow-up question field.
The offer is identical—natural-language question in, synthesised cited answer out.

:::: {.figure key="scopus-ai-opening-caption" title-id="" aria-labelledby="scopus-ai-opening-caption"}
Scopus AI: a deep-research report with cited findings

![Scopus AI deep-research report for open access citation advantage showing a key findings table, supporting citations and a follow-up question field](images/scopus-ai-deep-research.png){width="853" height="1096"}

::: {#scopus-ai-opening-caption .caption}
**Scopus AI’s visible deep-research view.** The report presents a quick-reference and key-findings table with supporting citation links and a field for a follow-up question.
The screenshot establishes the output surface, not the undocumented retrieval details.[Screenshot checked September 2026.]{.as-of}
:::
::::
:::::

These tools are where most librarians now meet “AI search”, and where most professional discussion begins and ends: is the summary accurate, are the citations real, did it invent a paper?
Those are reasonable worries—but they concern the last thing the tool did.
This book is about everything it did first.

### Anatomy of a cited answer {#anatomy-of-a-cited-answer}

For once, we do not have to guess.
Ex Libris documents the [Primo Research Assistant pipeline](<https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_(English)/015_Getting_Started_with_Primo_Research_Assistant>) in unusual detail.
For teaching purposes, we can group that account into five steps, separating source selection from reranking and leaving response delivery implicit:

1. **Query conversion.** The user’s natural-language question is sent to an LLM, which converts it to a Boolean query containing several variations connected with `OR`.
2. **Retrieval.** That query runs against the Central Discovery Index (CDI) and returns up to 30 results.
3. **Reranking.** The top results are reranked using embeddings to identify the five sources that best address the query.
4. **Selection.** Those top five sources become the working set.
5. **Generation.** GPT-4.1 Mini writes an overview from the five abstracts and supplies inline citations.

Read that list again.
The steps are not equal in cost or importance, but notice where they fall: only the final step writes prose.
Steps 1–4 select the evidence the final step receives.

::: {#primo-ra-content-scope}
**Coverage comes before ranking.** Research Assistant searches CDI metadata and abstracts, subject to content exclusions such as insufficient metadata or abstracts and some provider collections.
A record available through the library’s wider discovery system may therefore fall outside the assistant’s searchable scope.
If it cannot enter that scope, changing the query or reranking cannot bring it into the working set.[Content scope documentation checked October 2026.]{.as-of}
:::

[Scopus AI](https://www.elsevier.com/products/scopus/scopus-ai) is documented more thinly.
In Elsevier’s 2024 account, it expands a question into multiple query variants, fuses the retrieved lists using what Elsevier calls “RAG Fusion”, and generates a Topic Summary or Expanded Summary with references required for claims.
The same two-part architecture is visible, with a different index and a fusion step.
This is a historical architecture example, developed in [Appendix G](#appendix-rag), rather than a description of every later mode; where the documentation runs out, so does this description.

Strip away the product names and a general shape emerges.
The strip below shows the stages an AI search pipeline can contain, in the order they run.
Not every product uses all six stages, and no stage is guaranteed to be present; Table 1.1 maps Primo Research Assistant onto them.
Reading a product against this map—which stages exist, which are absent, which are documented and which are guesswork—is the core skill this book teaches.

::: {.stage-map on=""}
:::

::: stage-key
[Query transformation](#query-transformation)
:   The words you typed may be rewritten, expanded, translated into filters or split into several queries before retrieval ever sees them.

[Analysis & execution rules](#boolean-admission)
:   Text becomes index terms, and the rules decide which records are eligible to be returned at all.

[First-stage retrieval](#bm25-ranking)
:   One pass fast enough to run against the entire collection, producing the candidate set.
    It may be lexical, dense or both.

[Fusion](#hybrid-and-fusion)
:   Several candidate lists — from different retrieval methods or different queries — are combined into a single list.

[Reranking](#reranking-and-hybrid)
:   A shortlist is compared again, more carefully than collection-scale retrieval could afford.
    Nothing excluded earlier can be recovered here.
    In the tool dissected above, this is where 30 candidates became 5.

[Presentation](#library-practice)
:   What the reader is finally shown, in what order and with what explanation — and what a library can record about it.
:::

| Pipeline stage | Documented Primo behaviour mapped to this stage |
|---|---|
| Query transformation | LLM Boolean conversion |
| Analysis & execution | Query executed against CDI |
| First-stage retrieval | Up to 30 results |
| Fusion | No separate fusion stage documented (contrast: Scopus AI RAG Fusion) |
| Reranking | Embedding rerank, top 5 |
| Presentation | Five sources plus generated overview |

: The book’s six pipeline stages mapped onto Primo Research Assistant’s documented workflow. No separate fusion stage is described.

Do not infer the controller—the bar above the stages, which chooses and sequences them—from the answer format.
Primo’s documented pipeline specifies a sequence of stages.
The historical Scopus RAG Fusion account illustrates query expansion and fusion; later Scopus modes can use adaptive routing. [Chapter 12](#agentic-search-who-chooses-the-next-retrieval-action) distinguishes fixed, adaptive and agentic control by how the next action is chosen.

::: {.common-confusion label="Key definition"}
#### Retrieval-augmented generation (RAG) {#rag-definition-title}

In RAG, retrieval selects evidence and a language model generates an answer conditioned on it.
Retrieval limits the *supplied evidence*; it does not guarantee that every generated statement comes from that evidence.
A model can draw on its parameters, invent a citation or omit a retrieved source.

The evidence may come from ranked search or direct file and passage matching; RAG does not require embeddings. [Appendix G](#appendix-rag-alternatives) compares retrieval pipelines, file-search agents and supplying a small collection in full.
:::

### Two machines, one product {#retrieval-not-generation}

Two different problems sit inside answer-generating AI search products:

- **Retrieval** selects which records become available for consideration and helps order them.
- **Generation** turns some of those records into prose.

Two things follow from that split, and together they are why this book spends fifteen chapters on the first machine and none on the second.

**Retrieval sets a ceiling generation cannot raise.** That overview was written from the abstracts of exactly five papers.
Fluent generation cannot establish source-supported coverage of a paper absent from the supplied evidence—the [shortlist bottleneck examined in Chapter 9](#why-search-systems-use-multiple-stages).

**Missing evidence is especially hard to notice.** A paper absent from an answer may never have been retrieved, or it may have been retrieved and then omitted.
A fluent answer alone does not tell us which happened.
This book concentrates on the first possibility: evidence the retrieval process failed to supply.

For the same reason, the [six-stage strip](#anatomy-of-a-cited-answer) in the previous section maps the retrieval machine only.
It has no stage for generation: where a product writes an answer, as Primo Research Assistant does in its fifth step, that prose is built from what the stages supplied and reaches the reader at Presentation.

### Two axes: output format and retrieval iteration {#two-axes-output-format-and-retrieval-iteration}

The diagram below sorts current academic tools along two axes that describe different things.
The horizontal axis is output format: what the tool hands you—a ranked list of records, or a synthesised answer or report.
The vertical axis is **entirely a retrieval property**: how extensively the system retrieves—a single or limited pass, or repeated, multi-step searching.
That produces four recognisable shapes: quick search, quick answer, iterative search and deep research.[^iterative-not-agentic]

:::: {.figure key="ai-search-2x2-caption" title-id="" aria-labelledby="ai-search-2x2-caption"}
Four shapes of AI academic search

::: {.include src="figures/ai-search-2x2-caption.html"}
:::

::: {#ai-search-2x2-caption .caption}
**Output format on the horizontal axis; retrieval iteration on the vertical.** I introduced this framework in “[Why I Think Academic Deep Research—or at Least Deep Search—Will ‘Win’](https://aarontay.substack.com/p/why-i-think-academic-deep-research)”.
The boxes are softer than they look and products migrate between them: Scopus AI has since added a deep-search mode, and Web of Science Research Assistant now describes itself as [agentic](#agentic-search-who-chooses-the-next-retrieval-action). [Chapter 12](#where-current-academic-tools-actually-sit) examines that claim, and where these tools actually sit.
Treat it as a snapshot rather than a taxonomy. [Products placed as of August 2026.]{.as-of}
:::
::::

Primo Research Assistant and the core Scopus AI experience sit in the quick-answer quadrant: a single or limited retrieval pass, followed by generation.
The deep-research tools in the upper right differ from them not mainly in how they write, but in how much they retrieve.
Retrieval deserves attention independently of output format.

In these retrieval-based search modes, a quick answer follows retrieval,[^rag-basic-pattern] and deep research repeats retrieval while building an answer.
This describes these search modes, not every use of a language model; [Appendix G](#appendix-rag-long-context) considers answering from a supplied collection without a separate retrieval step.

Agency is a separate question: who decides what to search for next?
Neither axis records that choice.
A tool in the upper half may follow a workflow fixed by an engineer, or may let a model choose each subsequent action from what the previous round returned.
That third property—agency—is examined in [Chapter 12](#agentic-search-who-chooses-the-next-retrieval-action), once there are enough retrieval components for a controller to choose among.

::: {.common-confusion label="Common confusion"}
#### Leaving out generation does not mean leaving out large language models {#llms-in-retrieval-title}

An LLM can sit inside the *retrieval* half of a pipeline, and the pipeline dissected at the start of this chapter puts it there.
Those uses are covered here:

- **Writing the query.** An LLM can turn a natural-language question into a Boolean expression, complete with fields and filters, before any searching happens—exactly what Primo Research Assistant is documented to do. [Chapter 11](#when-a-system-writes-the-boolean-query) discusses this.
- **Inventing text to search with.** An LLM can draft a passage resembling a relevant document and use it to expand the query or as the input to dense retrieval. [Chapter 11](#query2doc-and-hyde) covers Query2doc and HyDE.
- **Reordering candidates.** An LLM can act as a reranker, judging or ordering a shortlist that an earlier retriever produced. [Chapter 9](#llms-as-rerankers) discusses this.
- **Controlling the loop.** An LLM can inspect intermediate results and decide what to search or examine next.
  Repeated retrieval is what places a tool in the upper half of the diagram; letting a model select those actions is what may make the process [agentic](#agentic-search-who-chooses-the-next-retrieval-action).
  The two are separate properties.

What falls outside this book is the generation of prose for the reader.
These earlier uses of an LLM help construct, select or order the evidence.
Each raises the same questions as other retrieval components: which records became candidates, which were excluded, and whether you can inspect why.
:::

So this book does not cover how language models generate text, how to detect a fabricated citation, how to write prompts, or how general-purpose agent architectures and planning algorithms work.
It covers what happens before any of that: how text becomes searchable, how a system decides which records are eligible, how it ranks them, and how much of that you can establish from the outside.
It does examine one narrow slice of agent behaviour—[how an agent selects, repeats and stops retrieval actions](#agentic-search-who-chooses-the-next-retrieval-action)—because that slice is retrieval design.

::: {#distinction-map-title .legacy-anchor}
:::

::: {#distinction-match-relevance .key-distinction-label}
Key distinction
:::

### What does “relevant” actually mean? {#what-does-relevant-actually-mean}

A carefully built search strategy makes its conditions explicit, inspectable and reproducible.
A record that meets those conditions has passed a useful test.
But that is different from establishing whether it helps the searcher accomplish a particular task.
Even a strong match needs to be judged against the purpose of the search.

::: pull-quote
> A match is evidence about relevance, not a guarantee of usefulness.
:::

Behind every query stands a person who wants something—an answer, an overview, evidence for a decision.
That fuller purpose is the **information need**.
Queries, filters and task briefs can communicate substantial detail about it, using terms, headings, fields or other supplied criteria. **The query represents the information need; it is not the need itself.** How fully it expresses that need depends on what the searcher supplies and what the system can use. [Chapter 11 returns to this](#distinction-query-object) once the choice between expressions starts to matter.

:::: {.figure .worked-figure key="relevance-chain"}
One study, two relevance judgements

::: {.include src="figures/relevance-chain.html"}
:::

::: caption
The query, the retrieved study and its findings stay the same. The task changes what the librarian needs the evidence to establish.
:::
::::

**[Relevance judgement](#term-relevance-judgement){.term-mark aria-describedby="definition-relevance-judgement" data-term="Relevance judgement" data-def="A recorded decision that a particular record does or does not satisfy the relevance criteria for a represented information need. Retrieval metrics compare systems against these operational judgements rather than objective truth."} assesses whether a document is useful for the purpose of the search.** For the adoption decision, the librarian could follow up with a search for evaluations of accuracy or staff workload. Requiring both terms in the original query could miss studies that report those outcomes only in the full text.

::: {.practice-callout label="Evidence synthesis"}
#### Search-resistant concepts {#evidence-synthesis-search-resistant}

Evidence-synthesis searchers will recognise this distinction.
Not every part of a review question or eligibility criterion can be represented reliably in a search strategy.
Some concepts are poorly indexed, inconsistently described or difficult to express as dependable search terms.
These are sometimes called **search-resistant concepts**.

Rather than make every criterion a compulsory search condition, the strategy may retrieve a broader set of potentially relevant records and leave some criteria to screening.
This lets reviewers assess what retrieval cannot reliably encode.
:::

When Primo Research Assistant selects five sources, the score is an estimate based on the evidence and training available to the system.
It does not establish that the sources answer this reader’s need.
A high score for the demonstration study would not turn participant reactions into evidence of answer accuracy.

Information-retrieval researchers distinguish several perspectives on relevance: how strongly a system estimates that a document matches a query, whether it addresses the topic, whether it adds to the reader’s understanding, and whether it is useful for a particular task.
These perspectives are related, with no single hierarchy among them. [Chapter 14 separates the four](#relevance-is-a-judgement), with the research behind them, and puts them to work on evaluation.
Their common point is that **relevance is a relationship, not a property.** No document is relevant on its own.
It is relevant *to* someone, *for* something.

Boolean matching, BM25 scores, embedding similarity and neural rerankers all help systems estimate relevance.
Even sophisticated retrieval methods cannot guarantee that the documents they rank highly will meet a particular reader’s information need.
That distinction matters when evaluating what an academic search tool actually delivers.

::: {.orientation label="Before the opening puzzles"}
#### Seven terms to carry forward {#opening-vocabulary-title}

Retrieval
:   Selecting and ordering records for an information need.

Candidate set
:   The records available to the next stage of a search pipeline.

Index
:   The searchable representation of a collection.

Ranking
:   Ordering candidates by a score or other rule.

Reranking
:   Reordering a shortlist produced by an earlier stage.

Generation
:   Producing prose from retrieved material; a separate operation from retrieval.

Information need
:   The fuller purpose behind a query, which queries, filters and task briefs can express in varying detail. [Just established above](#what-does-relevant-actually-mean).

The [complete glossary](#glossary) is in the end matter.
Other terms are introduced where their mechanisms first appear.
:::

::: {#two-familiar-search-results-and-two-puzzles .legacy-anchor}
:::

### Three familiar search results—and three puzzles {#three-familiar-search-results-and-three-puzzles}

Most librarians understand Boolean searching.
That understanding predicts certain behaviour: add a required word, and the result set shrinks; add an impossible word, and it empties.
Here are three searches—all real, all screenshotted below—where that prediction fails or falls short.

**Puzzle 1.** Take a genuine question—is there an open-access citation advantage?—and append an invented string unlikely to occur in the collection.
Run it in scite.
A strict Boolean `AND` query would return nothing if it required that string and the string matched no indexed terms.
In the observed search, useful-looking papers still appeared near the top, and the interface reported millions of results. *Why didn’t the invented string empty the result list?*

::::: {.evidence-stack aria-label="Puzzle one screenshot"}
:::: {.figure .evidence-card key="scite-opening-caption" title-id="" aria-labelledby="scite-opening-caption"}
Puzzle one: the nonsense term did not empty the result list

![Scite paper search returning results for a meaningful open-access question followed by an invented string](images/scite.png){width="1483" height="916"}

::: {#scite-opening-caption .caption}
**Observed behaviour:** relevant-looking results remain even though the query contains a string that is unlikely to occur in the collection.
:::
::::
:::::

**Puzzle 2.** In the example, Google Scholar reported about 9.4 million results for `open access`.
The interface stopped at page 100, and Google Scholar’s help documents a limit of 1,000 displayed results per query. *What about the remaining reported matches?
Were they ranked?
Were they even scored?*

::::: {.evidence-stack aria-label="Puzzle two screenshot"}
:::: {.figure .evidence-card key="scholar-opening-caption" title-id="" aria-labelledby="scholar-opening-caption"}
Puzzle two: the reported result set is much larger than the viewable list

![Google Scholar page 100 for an open access search reporting about 9.4 million results](images/googlescholar1000.png){width="1041" height="373"}

::: {#scholar-opening-caption .caption}
**Observed behaviour:** the interface reports millions of matches, while [Google Scholar documents a 1,000-result display limit](https://scholar.google.com/intl/us/scholar/help.html).
:::
::::
:::::

**Puzzle 3.** The name *Semantic Scholar* invites the expectation that it will handle a natural-language question well.
In August 2026, `Is there an open access citation advantage` returned just 13 results, for an established topic with dozens to hundreds of relevant studies.
Strip the question down to its keywords—`open access citation advantage`—and the same system returned about 35,300.
Inspection of the leading results also showed poorer relevance for the natural-language question.
The question performed worse in this comparison; the judgement rests on the known literature and the inspected results, not on the counts alone. *Why did the more natural query perform worse?*

::::: {.evidence-stack aria-label="Puzzle three screenshots"}
:::: {.figure .evidence-card key="semantic-scholar-opening-caption" title-id="" aria-labelledby="semantic-scholar-opening-caption"}
Puzzle three: a natural-language question retrieved fewer papers than a short keyword query

::: {.include src="figures/semantic-scholar-opening-caption.html"}
:::

::: {#semantic-scholar-opening-caption .caption}
**Observed behaviour in August 2026:** the natural-language question returned 13 results, while the unquoted keyword query returned about 35,300.
The contrast establishes a difference in visible behaviour; it does not reveal how Semantic Scholar parsed or executed either query.
:::
::::
:::::

Hold on to all three.
These screenshots establish visible behaviour, not the products’ complete internal architectures, and this book will not resolve them immediately—part of the point is discovering which of them *can* be resolved from the outside at all.
The outcome is not the one most readers expect.

::: {#puzzles-under-answer-layers}
The puzzles carry extra weight because systems like these can sit underneath an answer-generating layer.
Primo Research Assistant converts questions to Boolean queries, so Puzzle 3—natural language meets a query parser—is not academic.
A reranker chooses five survivors from thirty, so Puzzle 2—which fraction of the reported results was ever scored—is not academic either.
:::

### A map of the arguments ahead {#a-map-of-the-arguments-ahead}

Each of the three puzzles leaves a question open and tempts you into a mistake, and naming those mistakes now is most of what the rest of Part I and Part II are for.

::: {#opening-puzzles-title .legacy-anchor}
:::

| Puzzle: the question to keep open | The tempting mistake, and where the book takes it up |
|---|---|
| **1 · scite.** Why did the invented string not exclude every scite result? | A record that came back without one of your words tempts you to conclude the system stopped matching words at all. *Taken up: [Chapter 4](#returning-to-the-opening-puzzles).* |
| **2 · Google Scholar.** What do the reported count and the 1,000-record display limit each measure, and how many of the reported matches were ever scored? | A hit count of 9.4 million beside a thousand viewable records tempts you to read a reported total as a set of ranked results. *Taken up: [Chapter 4](#returning-to-the-opening-puzzles).* |
| **3 · Semantic Scholar.** Why did expressing the information need as a natural-language question make Semantic Scholar’s search perform worse? | A product named *Semantic Scholar* tempts you to read a label as an architecture. *Taken up: [Part II](#distinction-map-vocabulary); [Chapter 7](#returning-to-puzzle-three-why-did-the-keyword-query-retrieve-more).* |

: The three opening puzzles: the question each leaves open, the mistake it tempts, and where the book takes it up.

Puzzles 1 and 2 are the same mistake in different clothes: each reads a property of the display as a property of the machinery.
Three chapters of ordinary lexical retrieval are enough to correct them, and [the end of Part I](#distinction-map-interface) settles both.
Puzzle 3 is a different kind of error altogether.
It mistakes vocabulary for architecture, and no amount of squinting at an interface will ever settle it; it needs mechanisms that [Part II](#distinction-map-vocabulary) builds, and it is taken up in [Chapter 7](#returning-to-puzzle-three-why-did-the-keyword-query-retrieve-more).
Between them they cover a great deal of what a product description can say truthfully and still be heard as something stronger than it is. [Appendix D collects the wider terminology overlaps](#appendix-misleading-overlaps).

[The answer-surface screenshots that open the chapter were checked in September 2026; the Semantic Scholar counts were observed in August 2026.
The Primo pipeline is described from documentation checked by September 2026; the Scopus RAG Fusion account dates to 2024.
A documentation check is not a behavioural test of every stage.]{.as-of}

:::: chapter-close
1. Answer-generating academic search tools combine retrieval of source material with generation of an overview.
   The Primo walkthrough shows how several decisions constrain the evidence before writing begins.
2. Retrieval and generation are separate problems.
   A fabricated citation is a generation failure; a missing paper may have been lost during retrieval or omitted from the answer.
   Inspect the working set before diagnosing.
3. The shortlist bottleneck: retrieval limits the evidence supplied to generation.
   Coverage limits which records can enter the search at all; candidate and source-selection limits narrow the working set further.
   In Primo Research Assistant, five records supply the abstracts for the overview.
4. An LLM can sit inside the retrieval half of a pipeline; its presence says nothing about which retrieval method is being used.
5. Tools differ along two independent axes: output format and retrieval iteration.
   Neither records agency.
6. The query represents the information need.
   Matching helps a system estimate relevance; usefulness must be assessed against the reader’s purpose.
   Those judgements can guide later searches.
7. Three familiar results—a nonsense term that did not empty a result list, a reported count far larger than the viewable list, and a natural-language question that produced fewer papers and poorer leading results than a shorter keyword query—leave three questions about admission, ranking and architecture open.

::: {.chapter-transition}
Explaining these puzzles—and auditing pipelines like the one that opened this chapter—requires knowing what a search system does with words before it does anything else.
Chapter 2 begins with the strictest possible answer: words as admission rules.
:::
::::

::: self-check
Primo Research Assistant’s answer to your question cites five real, accurately summarised papers—but misses the one paper everybody in the field would name. Which machine failed, and how would you tell?

:   First distinguish the retrieved working set from the sources used in the answer.
    If the paper was retrieved but omitted, generation or source selection may explain its absence.
    If it never entered the working set, inspect the Boolean conversion, CDI coverage and representation, the top-30 boundary and the embedding rerank to five sources.
    Searching for the paper directly tests availability, but does not prove where the original run lost it.

A vendor says its discovery tool “uses a large language model”. Which half of the product does that tell you about?

:   Neither, on its own.
    An LLM can sit in the retrieval half—writing a Boolean query (as Primo Research Assistant’s does), generating a pseudo-document, reranking a shortlist, choosing the next action—or only in the final generation step.
    Naming the model locates no component.

Paper A is outside the assistant’s searchable scope; Paper B reaches its 30 candidates but misses its five-source working set; Paper C reaches that working set but is uncited. Where was each lost, and what evidence would distinguish the cases?

:   **A · Coverage.** Compare the paper’s record and collection with the assistant’s documented scope.
    Finding it in the library’s wider discovery system does not establish that the assistant can search it.

    **B · Reranking and source selection.** Compare the candidate list with the five-source working set.
    This requires a retrieval trace or another way to inspect the intermediate candidates.

    **C · Answer generation.** Compare the supplied working set with the overview’s citations.
    A source can be supplied without being cited.
    If the tool exposes only the final answer, record the remaining uncertainty rather than infer the exclusion point.

The opening diagram has two axes. Which one is a retrieval property, and what third property does neither axis record?

:   The vertical axis is the retrieval property: how extensively the system retrieves, in one pass or many.
    The horizontal axis is output format.
    Neither records agency — who decides what to search for next — which is why a fixed workflow and an agentic one can occupy the same quadrant.

A search returns forty records, every one of which contains all three of your search terms. A colleague says the search worked. What has been established, and what has not?

:   That forty records satisfy the representation you supplied.
    Not that any of them helps with the need behind it — a record can match every term and still be an opinion piece, the wrong population or the wrong decade.
    And not that the database holds nothing better: the records your wording never reached are not in the set to be judged.
    Matching is evidence about relevance.
    Assess usefulness against the task, and use those judgements to guide another search if needed.

Why can the demonstration study in this chapter be useful for an introductory workshop yet insufficient for deciding whether to introduce the service? What further evidence would you seek?

:   The workshop needs a concrete example of a service and participants’ reactions.
    The adoption decision also needs evidence about answer accuracy, staff workload and performance in actual consultations.
    The study’s contribution changes with the purpose, even though it still matches the same search.
    Seek evaluations addressing those questions, then assess their methods and conditions; adding terms alone does not establish usefulness.
:::

[^iterative-not-agentic]: **Iterative is not the same as agentic.** The vertical axis measures how many retrieval rounds occur, not how the next one is chosen.
    A tool can run several passes from a fixed script—expand the query, search again, merge the results—without any model selecting among actions.
    Marketing language routinely blurs the two. [Chapter 12](#agentic-search-who-chooses-the-next-retrieval-action) separates them properly.

[^rag-basic-pattern]: **Retrieval-augmented generation**, or **RAG**, refers to a broad family of architectures that combine retrieval with a generative model.
    Patterns vary in when retrieval occurs, how often it is repeated, what is retrieved, how results are reranked or filtered, and how retrieved evidence is supplied to the model.
    In the most basic retrieve-then-generate pattern, the system retrieves a shortlist of records or passages, places some of them in the model’s context, and generates an answer conditioned on that material.
    RAG therefore does not specify a retrieval method: the shortlist may come from lexical, dense or hybrid retrieval. [Appendix G](#appendix-rag) traces the family’s history and works through a documented product example.
