---
key: "agentic-search"
kind: "chapter"
eyebrow: "Chapter 12"
meta: "About 25 min"
question: "Who chooses the next retrieval action?"
legacy_anchors: ["ch7"]
---

## Agentic search {#agentic-search}

::: {.stage-map on="" controller="on"}
:::

::: chapter-orient
Everything to this point has been a pipeline: an arrangement of stages, possibly with branches, all decided before the search ran.
Chapters 9 to 11 showed a system generating several queries, routing them to different retrievers, fusing the results and reranking the candidates—none of it necessarily agentic.
Agentic search removes that guarantee.
A model inspects what came back and decides what to do next.

That is a change in control, not in retrieval.
The retrievers, rerankers and fusion rules are the ones already described.
This chapter separates fixed, adaptive and agentic arrangements and shows where current academic tools sit.
It is candid about what agency costs, including two retrieval problems that iteration makes worse rather than better.
It ends with what agency is genuinely for.
That turns out to be narrower than the marketing suggests—and more useful to a library.
:::

::: {#agentic-search-who-chooses-the-next-retrieval-action .legacy-anchor}
:::

Chapter 11 also separated a task brief from the queries it produces.
The brief is the controller’s input: it defines scope, criteria, sources, coverage, stopping conditions and the required record.
The controller turns that specification into retrieval inputs and tool calls.
Calling the brief a query hides the layer that interprets it.

Pseudo-relevance feedback, met in Chapter 11, marks where the lines fall.
Its *content* adapts to the first ranking, but if the system always runs the same two passes, its *control sequence* is fixed.
A rule that decides whether to search again makes the control flow adaptive.
A model free to choose the next query, route, tool or stopping point from what it observes may make it agentic.

### Fixed, adaptive and agentic are not the same thing {#fixed-adaptive-and-agentic-are-not-the-same-thing}

:::: {.figure .query-flow key="control-arrangements"}
Three control arrangements, distinguished by who chooses the next action

::: {.track}
- **Fixed** the sequence is settled before any user arrives
- **Run the search** a first pass returns a yield, from preset steps in a preset order
- **No decision at run time** results may fill the next query, but cannot change the next operation
- **Records** one path, documented once
:::

::: {.track}
- **Adaptive** a constrained policy chooses among predefined branches
- **Run the search** a first pass returns a yield
- **A rule *or a model* picks a branch** observations select among routes the workflow designer explicitly enumerated
- **Records** path varies, but only along branches that exist
:::

::: {.track}
- **Agentic** a model plans actions while the search is running
- **Run the search** a first pass returns a yield
- **A model decides** uses the task and observations to compose the next query, tool or source call—or stops
- **Records** path chosen per question; only a trace shows it
:::

::: caption
The three arrangements differ at the third box and nowhere else: who chooses what happens next, and when.
The retrieval in the second box is identical in all three, and so is the output box, because what a system hands back is a separate property from who chose the sequence — as [Table 12.2](#tbl-12-2) sets out.
That is why agency is a property of the sequence, not of the retriever.
:::
::::

| Control arrangement | How the next action is decided |
|---|---|
| **Fixed workflow** | The system always follows a predetermined sequence: generate five queries, run BM25 and dense retrieval, fuse the lists, rerank a hundred candidates. It may also always run two-pass PRF; the second query changes with the first results, but the next action does not. |
| **Adaptive workflow** | Intermediate observations select among constrained branches that the workflow designer explicitly enumerated. The chooser may be a written rule, classifier or model, but it selects a branch rather than planning a new sequence of actions. |
| **Agentic search** | A model plans at least part of a multi-action retrieval trajectory from the task and what it has observed, choosing among the tools the harness permits. The tools are predefined; the sequence of actions is not. |

: Fixed, adaptive and agentic control arrangements, distinguished by how the next action is decided.

The middle row is the one usually left out, yet it is where a great many products actually sit—including most of the first wave of academic deep search.
It is also the row most often mistaken for the third, because a model may well be doing the choosing.
The useful question is not whether the operations existed before the query—an agent’s tools did too.
It is whether the workflow picks from a fixed menu of branches, or assembles its own sequence of actions.
Ai2 describe Asta Find Paper—the tool their earlier Paper Finder became—in close to the adaptive pattern: a semi-rigid flow whose predefined structure is shaped at key points by model decisions.
Librarians have made comparable branch decisions by hand for decades: run the search, inspect the yield, broaden or narrow, then search again.

The three rows are reference points along a continuum, from a prescribed sequence to a model planning a sequence within the available tools and limits.
A product may use different control arrangements in different modes.

> **Agentic search is search in which a model, working within a given set of tools, instructions and limits, plans at least part of a multi-action retrieval trajectory from the task and what it has observed—rather than only selecting among branches enumerated in advance.**

An agent’s **harness** specifies which tools it may call, which sources it can reach, how many rounds it is allowed and when it must stop. **Tool** here does not mean a product a library licenses.
It means one specific operation the model has permission to invoke—*run this search*, *fetch this record’s references*, *restrict to these years*—described precisely enough that the model can decide when to call it and what to pass in.
The definition does not require reasoning from first principles.
The harness is usually where the consequential design decisions live—and it is usually the part a vendor does not describe.

### Deep search can still be agentic search {#deep-search-can-still-be-agentic-search}

[Figure 1.3](#fig-1-3) sorted tools by output format and by how extensively they retrieve.
Agency is a third property, and it lies on neither axis.

| Pattern | Search trajectory | Main output |
|---|---|---|
| Scripted deep search | Predetermined repeated retrieval | Records |
| **Agentic deep search** | Model plans a retrieval trajectory from the task and intermediate results | Records |
| Scripted deep research | Predetermined retrieval, then synthesis | Report or answer |
| Agentic deep research | Model plans a retrieval trajectory before or during synthesis | Report or answer |

: Deep search and deep research compared by search trajectory and by main output.

Repeated retrieval establishes **iteration**; it does not, by itself, establish agency.
A fixed workflow can repeat searches, and an adaptive workflow can revise them through prewritten branches.
Call the process agentic when there is evidence that the model plans or chooses the sequence of actions.
Output format is separate: an agentic search may return a ranked list, while a fixed workflow may write a report.

The converse matters just as much.
A deep research tool that returns a long, fluent, well-cited report may have run an entirely fixed workflow underneath.
Length and polish of output are not evidence of agency; they are evidence of generation.

### Agentic RAG is narrower than agentic search {#agentic-rag-is-narrower-than-agentic-search}

Basic [retrieval-augmented generation (RAG)](#rag-definition-title) retrieves and then generates: what retrieval returns is placed in the model’s context so the answer it writes is grounded in those sources. **Agentic RAG** lets a model choose retrieval actions while working towards a generated response. **Agentic search** is broader than both: it may end with a ranked set of papers, passages or evidence and never generate prose at all.

Keeping these apart matters because, from the outside, RAG, deep research and agentic search look like a single marketing category.
They are not. [Appendix G](#appendix-rag) gives the RAG family its own short history and a worked product example.

### Where current academic tools actually sit {#where-current-academic-tools-actually-sit}

I tested the tools with a task: *find papers that could have been cited by a particular article but were not.* The probe, run and written up in December 2025 as “[Deep Research, Shallow Agency: What Academic Deep Research Can and Can’t Do](https://aarontay.substack.com/p/how-agentic-are-academic-deep-research)”, was deliberately ordinary.
It needs no specialist knowledge, only four ordinary steps: identify the paper, extract its reference list, find related work on the same topic, then subtract the second from the third.
The one thing it does not do is match any product’s predetermined workflow.

Most of the specialised academic tools did not complete the task.
Ai2 Asta Find Paper treated the request as a lookup and stopped once it had found the target article.
Consensus Deep Search returned papers the article already cited, despite running four sub-agents.
Undermind found related work, most of it already in the reference list.
Elicit’s screening pipeline—search, set criteria, screen, extract—has no step at which *is this one already cited?* could be asked.
SciSpace Agents came closest: it extracted the article’s reference list and attempted the comparison, and most of its suggestions were not already cited, although incomplete metadata broke a few matches and it was unclear whether it finished.
General-purpose assistants with web search mostly passed: Claude Sonnet did so with no academic connector at all, and earlier GPT models also succeeded, while Gemini and GPT-5.1 struggled when blocked from the full text.

Undermind’s case shows how hard the cause of a failure is to establish.
It asked clarifying questions that suggested it understood the request, and its internals are the least documented of the tools tested.
In related tests, its clarifying step sometimes warned that the system could not do the task requested.
That fits a fixed workflow with no step for this comparison, although the result alone cannot rule out a missing operation or poor choices of action.

Sorting the tools themselves is a separate exercise, done in April 2026 and written up as “[From Fixed Search Workflows to Agentic Academic Search](https://aarontay.substack.com/p/from-fixed-search-workflows-to-agentic)”.
It describes how these products were built at that point, and it will date quickly.

| Control arrangement | Tools, as built at the time of testing |
|---|---|
| **Adaptive workflow** | Undermind’s original deep search, Consensus Deep Search and Ai2 Asta Find Paper were built as predefined structures. A model contributes at set points, and those judgements can change the path taken: understanding the query, judging whether to search again, formatting the output. What it does not do is choose an action nobody provided for. The stages, and the moves available at each, were laid out by the designers. |
| **Agentic** | Elicit Research Agents combine tools and workflows flexibly rather than following one pipeline. A capability may still need to be asked for explicitly before it is reachable: telling Elicit to “search the web” produces behaviour its default academic search tool will not. |
| **Agentic, with broader tool access** | Undermind Projects runs three agents—Search Architect, Report Writer and Generalist—which select and chain tools dynamically and can call one another. SciSpace Agents takes a comparable approach across a large library of connectors. |

: Where current academic tools sat at the time of testing. The rows are reference points along a continuum.[Tested April 2026; products have changed since.]{.as-of}

Two things in that table matter more than the names.

First, **the same vendor appears at both ends.** Undermind’s original deep search ran a predefined structure; Undermind Projects does not.
Agency is a property of the mode you are using, not of the brand printed at the top of the page.
That is why a vendor’s marketing copy cannot answer the question for you.

Second, **Ai2 Asta Find Paper sits in the upper-left quadrant of [Figure 1.3](#fig-1-3)**—iterative search, returning records rather than a report—while running a predefined structure.
Repeated retrieval is not evidence of agency: a model may be making calls inside that structure without ever selecting a move its designers had not already provided.

One caveat about the evidence.
The uncited-references probe was a single task type, probing one kind of multi-step reasoning.
A tool could fail it and still perform well on other agentic tasks, or pass it through a lucky sequence of actions rather than robust reasoning.
Treat the table as an illustration of the distinction, not a league table.

#### Placing a tool from its documentation {#placing-a-tool-from-its-documentation}

One more product can be placed, and from a document rather than from testing — which makes it a different kind of evidence from the rows above.
Clarivate describe [Web of Science Research Assistant](https://clarivate.com/academia-government/blog/a-more-transparent-connected-experience-in-web-of-science-research-assistant/) as “fully agentic” in an April 2026 product post, and the same post says what the agency does: “It automatically determines whether the user needs a topic map, structured review, journal recommendation, or something else entirely.”
Before that release those were three separate guides, and the user picked between them.
What changed is who picks, not how many there are to pick from.
Read against [Table 12.1](#tbl-12-1), a model selecting among routes the designers enumerated is the adaptive row, whatever adjective the announcement uses.

Two qualifications keep that from being a verdict.
The clause “or something else entirely” is exactly where a blog post stops being able to settle anything: it may name a fourth enumerated route, or it may mean the model composes something, and the post does not say.
And a vendor writes for its own market, not to this book’s schema, so a label and a mechanism can diverge in either direction.
Consensus calls its mode Deep Search while [Table 12.2](#tbl-12-2) would file its report-shaped output under deep research.
Use the documented operations to assess the control arrangement, and record what the description leaves uncertain.

The same post does document a control property nothing else in this chapter exposes.
Before retrieval runs, the assistant shows its reading of the question, a proposed search strategy, the synonyms and expanded terms, and “the structured logic the agent intends to use”.
The post adds that “the search runs only after the user reviews and approves the strategy.”
Afterwards it returns the query in Advanced Search syntax, which is to say in a form a librarian can save, edit and rerun.
A harness that has to stop and ask is a narrower harness than one that does not, and this is a user-controlled approval gate before retrieval.
It is distinct from a stopping criterion for an ongoing search; users can also set limits or interrupt a run. [Chapter 15](#interpretability-requires-an-inspectable-pipeline) asks products for precisely this and mostly does not get it.

### Agency changes the sequence, not the retrieval {#agency-changes-the-sequence-not-the-retrieval}

The operations described so far can become tools for an agent.
It can search files with grep, construct or revise a Boolean query, run BM25, run dense or learnt-sparse retrieval, follow citations, apply metadata filters, choose a database, fuse result lists, rerank candidates, inspect a shortlist—and decide whether to go round again.

> Agency governs which operations run, in what order, and when to stop.

It does not change how BM25 scores a document, how an ANN index finds neighbours or what a cross-encoder does with a shortlist.
The retrieval machinery underneath is the machinery described in the preceding chapters.

[Scopus AI’s routing](#two-hybrids-that-combine-differently) is the smallest useful illustration of adaptive control.
The system decides, per question, whether to search lexically, over embeddings, or both.
That is a single choice among three constrained routes, made before retrieval; it does not compose a multi-action trajectory.
The lexical and vector paths are unchanged by being selected.
The routing decision can still be right or wrong for a given question, and a librarian may want to see it recorded.

> Agentic is not a synonym for dense, hybrid, multi-stage or iterative.

Agency completes a set of three independent properties. [Hybrid](#why-hybrid-retrieval-remains-attractive) describes which retrieval signals contribute; [multi-stage](#why-search-systems-use-multiple-stages) describes the order in which operations are applied; agentic describes who decided that order.
They combine freely.
Repeated model-directed BM25 searches are agentic but not hybrid.
Fixed parallel lexical and dense retrieval with reciprocal rank fusion is hybrid and multi-stage but not agentic.
A production pipeline may be all three at once.
A product may advertise one while possessing only that one.

:::: {.practice-callout label="Worked search sequence" label-class="callout-label"}
#### An intelligent search process can use a simple matching tool {#agent-grep-search}

Suppose an agent can search a folder of article text and read selected passages.
The task is the familiar question, “Does open access increase citations?”
Each grep call matches a string or pattern, as in [Chapter 2](#grep-searching-text-directly).
The model can nevertheless interpret the task, choose another expression and decide which surrounding text to inspect.

1. **Choose the searchable files.** The agent selects an available folder of extracted article text.
   This already limits coverage; papers outside the folder cannot be found by these calls.
2. **Search a phrase.** It searches for `citation advantage` and receives matching lines with file names and line numbers.
3. **Read around a match.** Suppose a paragraph discusses *selection bias*.
   Reading the paragraph supplies a qualification that the matching line alone did not convey.
4. **Search again.** The model chooses `selection bias` as another pattern, then reads the returned passages to assess whether they bear on the question.
5. **Assemble evidence and record the stopping point.** It retains passages with their source locations and stops at the allowed search budget.
   Reaching that budget does not establish complete coverage.

This is a hypothetical trace, not an observed product result.
The meaning-oriented work occurs in interpreting the task, reformulating searches and assessing passages; grep still performs lexical matching.
The same tools could appear in a fixed script.
What makes this example agentic is the model choosing the next action from what it finds.
If it returns only records, it is agentic search; if it generates an answer from the retrieved evidence, it also fits this book’s broad definition of [agentic RAG](#agentic-rag-is-narrower-than-agentic-search).

::: {#claude-code-grep-account}
Anthropic’s September 2025 account describes Claude Code combining upfront instruction files with on-demand exploration using tools such as glob and grep.
It also identifies costs of runtime exploration: extra latency, unproductive paths and the need for suitable navigation tools and guidance.
This is a dated architectural example, not a performance comparison with academic search. [Read the engineering account](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents).
:::

A more capable controller may discover better patterns, but it cannot make a missing file available or guarantee that an untried synonym was unnecessary.
The [debate about replacing a vector-search pipeline](#appendix-rag-alternatives) therefore needs evidence about the whole search process, including its costs and omissions.
::::

The clearest demonstration that agency and retrieval are separable comes from the products themselves. [Scite](https://scite.ai/) and the [Wiley AI Gateway](https://docs.scholargateway.ai/) now expose their search as **MCP servers**.
The **Model Context Protocol** is a convention for describing a service to a model rather than to a programmer.
The server publishes what operations it offers, what each expects and what it returns.
A model reads that description while working and decides whether to call it.
Wiley’s server returns full-text chunks likely to be relevant to the query, alongside the paper’s metadata.
A librarian can point a general-purpose agent at these and assemble a retrieval system whose controller is theirs and whose retrievers are the vendors’.

Notice what does and does not change in that arrangement.
Scite [documents its MCP server](https://docs.scite.ai/mcp/overview) as another route to the same tools behind its ChatGPT and Claude integrations, with the same search filters as its Search API.
It does not document whether results are ranked as in its web interface, and some interface features, such as its Assistant, are not offered through MCP.
The controller decides when to call the service, what to ask it and whether to search again.
These actions may improve the combined results while leaving each retriever’s scoring rule unchanged.[Scite MCP documentation checked October 2026.]{.as-of}

Two things MCP is not.
It is not a replacement for an **API**.
It is a description layer over a service the vendor already runs, not a different index; what an agent can retrieve still depends on which operations the server exposes, and a library’s authentication and entitlements still apply.
An MCP endpoint is not a route around a subscription.
Nor is it a rival to RAG. [Appendix D](#appendix-misleading-overlaps) separates that pair, which are the two most often confused.

### What agency costs, and what it buys {#what-agency-costs-and-what-it-buys}

More agency is not simply better.
It is a trade, and for a known task with an established procedure it may be a poor one.

| Consideration | Fixed or adaptive workflow | Agentic search |
|---|---|---|
| **Cost and speed** | Cheaper and faster. Most of the sequence is decided in advance; at most a branch is selected at query time, so little has to be reasoned out per question. | Slower and dearer. A model is invoked to choose, and often to justify, each successive action—and every round adds latency and tokens. |
| **[Reproducibility](#reproducibility-implication-title)** | The workflow and its rules can be documented. A fixed sequence follows the prescribed stages; adaptive control follows prewritten branches whose outcomes depend on inputs and intermediate results. Record the branch taken as well as the rules. | Comparatively weak. The path is chosen per question and two runs of the same question may legitimately differ, so only a trace of the actual run describes what happened. |
| **Anticipated tasks** | Reliable, and often the better choice. A well-designed pipeline for a known task is hard to beat. | May reach the same place by a longer, costlier route. |
| **Unanticipated tasks** | **Limited by the available procedure.** An unfamiliar task may still fit an existing sequence or branch. A task requiring a different sequence cannot be handled unless that sequence is available within the workflow. | **The reason to pay.** A model choosing its own actions can attempt a task nobody encoded in advance. |

: What agency costs and what it buys, against a fixed or adaptive workflow.

That final row gives a practical argument for agency: researchers sometimes need a sequence of actions the workflow does not provide.
An unfamiliar question alone is not enough to establish that need; it may still fit a well-designed fixed procedure.
Where a task fits a known procedure that a librarian could have specified, paying an agent to rediscover it is a poor bargain.

For retrieval, inspect the available actions, the effect of earlier results on later searches, and the stopping conditions.

**The menu is invisible as well as the path.** A trace tells you what a system did; it does not tell you what it could have done.
When a platform can theoretically do anything, a user has no reliable way to discover what it can actually do, or how the vendor has configured its agents.
Evaluators also need to know which operations were available to the system.
A user has no way of knowing that a tool’s academic search cannot extract references from a paper while its web search can.
So a capable system fails a task it could have completed—and the failure looks like incapacity.

**Recall failures compound across rounds.** The [shortlist bottleneck](#why-search-systems-use-multiple-stages) now applies once per round, and the rounds are not independent.
A reranker cannot rescue a document the retriever never returned.
In an agentic loop, round two is chosen from what round one returned.
A concept missed at the start may never be recovered, because nothing downstream has any reason to look for it.
Iteration compounds recall failures as readily as it repairs them.

**The stopping rule is a relevance judgement nobody wrote down.** A fixed workflow stops because it has run out of steps.
An agent may stop because its harness makes it—a round limit, a budget, a user’s interruption.
The consequential case is the other one: a model decided that what it had was good enough, which means it applied some operationalisation of relevance to results the user has not seen. [Chapter 1 distinguished matching from relevance](#distinction-match-relevance).
Here, the model may use its own assessment of the results to decide whether to continue searching.
Nothing in the interface states the criterion, and two runs may apply it differently. [Chapter 14](#relevance-is-a-judgement) gives this its proper name and [Appendix F](#when-is-it-safe-to-stop-screening) shows what a defensible stopping rule looks like for evidence-synthesis tasks that require high recall.

Choose the control arrangement for the task.
For agentic searches, record the actions, intermediate results and stopping conditions.

:::: {.figure .worked-figure key="agentic-search-trajectory"}
What came back shapes what gets searched next

::: {.include src="figures/agentic-search-trajectory.html"}
:::

::: caption
Feedback can reinforce an early omission or help repair it.
This is a possible trajectory, not evidence that citation searching always stays within one aspect.
:::
::::

### What the loop is for {#what-the-loop-is-for}

An agentic loop can respond to a weak result by selecting another available action, such as broadening the query or trying a different source.

#### An experiment with zero-result searches {#an-experiment-with-zero-result-searches}

Consider the query that returns nothing.
In a conventional catalogue that is the end of the interaction: the searcher is told there are no results and left to work out why.
I tested the alternative by pointing a model, through an [MCP server](#agency-changes-the-sequence-not-the-retrieval), at my own library’s Primo index, and replaying database searches drawn from our 2023 zero-result logs under the template *search for a database in Primo for X*.
The work is written up as “[What Changes When an LLM Agent Searches Your Library Catalogue?](https://aarontay.substack.com/p/what-changes-when-an-llm-agent-searches)” (June 2026).
Two limits belong with it: the examples were selected rather than sampled, and 2026 models were answering 2023 queries.
Read what follows as an exploratory demonstration of failure recovery, not a measured success rate.

A user looking for databases on `autism` gets nothing, because no database is called that.
The loop broadens—psychology, medicine, education, disability—and returns PsycINFO, Education Research Complete and SocINDEX. `cost of living` becomes inflation, household expenditure and consumer prices, and reaches the economics databases. `Rolex watches` is recognised as a question about luxury goods and produces Statista and Passport.
Misspellings resolve on the way past: `statis` to Statista, `refinituv` to LSEG—though that last one is where the dating problem bites hardest, since the rebrand it recovers postdates the query, and a 2026 model knows it in a way a 2023 one might not.

The comparison that matters is not against a human.
It is against [Primo’s own Natural Language Search](#query-understanding-in-current-discovery-products), which converts a question into a Boolean string in a single pass.
On simple misspellings it does well.
On `autism` it produced a creditable expansion—`(autism) OR (autistic disorder) OR (ASD) OR (autism spectrum) OR (neurodevelopmental disorder) OR (pervasive developmental disorder)`—six synonyms, and still zero results, because the problem was never the synonyms.
Both runs searched the same index.
The single-pass rewrite did not use the zero-result response to revise its query.
The loop did, broadening the search to related subject areas.

The comparisons narrow the explanation without establishing a single cause.
Dense retrieval was not required in the keyword-endpoint example.
MCP was not required to reproduce most of the result: a plain CSV of our database holdings, handed to the same model, also worked.
Rerunning the same queries on a mini model at low reasoning effort, in place of the frontier model at extra-high effort I had been using, made little difference in these examples.
That does not establish that model capability is generally irrelevant.
These examples suggest that feedback and the freedom to broaden a concept, shift granularity and try again matter.
They do not isolate the loop as the sole cause: a fixed or adaptive workflow could also implement useful retries, and the CSV comparison changes how the model receives the holdings.

In this demonstration, a keyword-oriented search endpoint became much more useful inside a loop that reformulated, broadened and recovered from zero results.
That supports a point [Chapter 3](#bm25-ranking) documents on other grounds: lexical retrieval remains useful.
It does not show that better retrieval is unnecessary.

For librarians this lands close to home. *Which database should I use?* is a question the literature has worried at for twenty years, and it has resisted every interface redesign aimed at it.
This is the first mechanism I have seen that looks capable of absorbing most of it.
It also moves the design question.
The thing to ask of a search system stops being *does it return the right result for a well-formed query* and becomes *does it recover when the query is poor*.
That is a different property, and one [Chapter 14](#evaluation) has to find a way to measure.

#### What the loop cannot know {#what-the-loop-cannot-know}

The limits fall exactly where a library’s knowledge does.
The loop works because the model has read the open web—libguides, vendor pages, reviews—and can therefore guess that autism research lives in PsycINFO.
A database the open web has barely heard of gets no such help, and a newly licensed one none at all.
Coverage, field quirks, embargo dates, what your institution actually subscribes to this year: these are what a model cannot infer and a library holds.
If loops like this absorb routine database questions, the work moves rather than disappears: to supplying that knowledge, such as current coverage and entitlements, and to the specialised request—*this variable, these companies, 2005 to 2020*—where it still runs out.

> A loop can use retrieval feedback to revise a query and try again without changing the retriever’s scoring function.
> In the selected examples, that process recovered useful results.

:::: chapter-close
1. Fixed, adaptive and agentic describe who decides the next action, not how documents are scored — and they are reference points along a continuum.
2. Result-dependent query content does not by itself make control adaptive or agentic: two-pass PRF can sit inside a fixed sequence.
3. An adaptive workflow may have a model choosing its branches.
   What makes it adaptive is constrained selection among explicitly enumerated branches; agentic control plans a trajectory from reusable actions, even though its tools are predefined too.
4. Agency does not change the underlying retriever’s scoring function, but a loop can improve the overall search process by observing failure and choosing another action.
5. An agent can only choose among the tools it has.
   It may combine available operations in new ways, but further reasoning or iteration cannot supply a tool or source it cannot reach.
6. A trace shows what a system did.
   It does not reveal what the system could have done, which is a separate and largely invisible limit.
7. Recall failures can compound across rounds when later actions depend too narrowly on earlier results; additional routes or reformulations can also recover candidates and increase cumulative recall.
8. Agentic RAG is a narrower case of agentic search, not a synonym for it.
9. What the loop buys is recovery.
   A query that returns nothing stops being the end of the interaction and becomes the input to the next attempt.
   In the selected examples, a keyword search inside a loop recovered results that a one-shot rewrite over the same index did not.
10. That recovery runs on what the open web knows.
    Coverage, entitlements and local quirks are what it cannot supply, and what a library can.

::: {.chapter-transition}
The pipeline is now complete, from interpreting and transforming retrieval inputs through to the controller that sequences later actions.
That makes a different question possible: not what each component does, but where a particular search went wrong.
:::
::::

::: self-check
A tool retrieves repeatedly, revises its searches from what it finds, and hands you a ranked set of papers. Is it agentic? Is it deep research?

:   Neither is established.
    Repeated retrieval and result-dependent revision can occur in a fixed or adaptive workflow.
    To establish agency, you need evidence that a model plans a multi-action retrieval trajectory from the task and its observations, rather than only selecting among branches enumerated in advance.
    Deep research names an output centred on a report or answer; returning ranked records does not establish it.

A deep research tool returns a long, fluent, well-cited report. What does that establish about agency?

:   Nothing.
    Length and polish are evidence of generation.
    The workflow underneath may be entirely fixed — and in current academic tools it often is.

Which three difficulties should you inspect in an iterative retrieval process?

:   The invisible menu: a trace shows actions taken, not every useful action that was available.
    Compounding misses: an early gap may steer later searches away from an entire concept.
    Stopping: diminishing yield does not establish that all relevant evidence has been found.
    Iteration can help, but does not automatically solve any of these.

An agentic loop over a plain keyword index beats a one-shot query rewriter over the same index. What does that establish about the retriever?

:   Both runs used the same underlying retriever, so the comparison concerns how it was used.
    The loop used the zero-result response to revise the query, whereas the single-pass rewrite did not.
    The selected examples support the value of feedback and reformulation, but do not isolate them as the sole cause or show that recovery requires agentic control.
    The smaller-model and holdings-CSV comparisons changed other aspects of the setup and should be interpreted separately.

An agent chooses grep patterns, reads surrounding passages and writes a supported answer. Which part is lexical, which part is agentic, and does it need embeddings?

:   Each grep call is lexical matching.
    The model’s choice of the next search or read from its observations is agentic control.
    Generating an answer from that evidence also fits the book’s broad RAG definition.
    This arrangement needs no embeddings, but its success does not establish complete coverage or superiority to an indexed retriever.
:::
