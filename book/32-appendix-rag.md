---
key: "appendix-rag"
kind: "appendix"
eyebrow: "Appendix G"
meta: "About 12 min · optional"
section_id: "app-G"
---

## Retrieval-augmented generation: the pipeline this book feeds {#appendix-rag}

This book follows how evidence becomes available for use. **Retrieval-augmented generation (RAG)** supplies retrieved material to a language model to write from.
That material may be a ranked shortlist or selected files and passages found through direct matching.
This appendix exists because the pattern is now unavoidable in academic search products—and because almost everything that determines whether a RAG system answers well has already been covered in the preceding chapters.
RAG is not a rival to retrieval.
It is a consumer of it.

### The basic pattern, restated {#appendix-rag-pattern}

A RAG system retrieves records, files or passages, places selected material in the model’s context, and generates an answer conditioned on that material—the definition [Chapter 1 introduced](#rag-definition-title).
Three consequences follow, each already argued from the retrieval side:

- **RAG does not specify its retriever.** The evidence may come from direct text search, indexed lexical, dense, learnt-sparse or hybrid retrieval, with or without [reranking](#rerankers-compare-more-carefully-after-retrieval).
  “This product uses RAG” answers none of the questions this book has taught you to ask.
- **The searchable unit and context unit may differ.** In an indexed pipeline, the [chunking decision in Chapter 8](#one-document-one-chunk-and-one-vector-are-not-the-same-thing) determines what can be matched at that retrieval stage.
  The system may then fetch full text, expand to neighbouring passages, merge results or compress them before supplying context.
  A chunk too small strips evidence of its argument; a chunk too large crowds other evidence out of the context window.
- **Generation cannot establish source support from evidence it never received.** A model may recall a fact from its parameters, but that does not establish what an unseen source says.
  A fluent answer can conceal gaps in its supplied evidence.
  Diagnose retrieval and context-selection failures using the traces described in [Chapter 13](#diagnosing-failure) and below.

### A short history {#appendix-rag-history}

The name is younger than the idea.
Open-domain question answering had used a retrieve-then-read design for years: [DrQA](https://arxiv.org/abs/1704.00051) (Chen et al., 2017) retrieved Wikipedia passages and extracted answers from them, and [ORQA](https://arxiv.org/abs/1906.00300) (Lee et al., 2019) and [REALM](https://arxiv.org/abs/2002.08909) (Guu et al., 2020) learnt the retriever jointly with the reader.
The term itself comes from [Lewis and colleagues (2020)](https://arxiv.org/abs/2005.11401), who combined a dense passage retriever with a generative model and trained them together, so that generation was conditioned on retrieved evidence rather than on parameters alone. [Fusion-in-Decoder](https://arxiv.org/abs/2007.01282) (Izacard and Grave, 2021) and [RETRO](https://arxiv.org/abs/2112.04426) (Borgeaud et al., 2022) extended the family; patterns vary in when retrieval occurs, how often it is repeated, and how tightly retriever and generator are coupled.

What changed after 2022 was not the architecture but the economics.
Once conversational language models were deployed at scale, RAG stopped being a research architecture and became the default engineering answer to two deployment problems: models whose parametric knowledge has a training cut-off, and models that assert without evidence.
Web-grounded assistants, enterprise document assistants and the academic tools surveyed in [Chapter 12](#where-current-academic-tools-actually-sit) all instantiate the same pattern: retrieve first, generate second, cite what was retrieved.
By 2024 the vocabulary had sprawled—advanced RAG, modular RAG, GraphRAG, agentic RAG—but the sprawl mostly names different retrieval-side choices.
Read any “RAG variant” by asking what its retriever does; the generation half changes far less than the marketing does.

### Do long context and agentic search make RAG unnecessary? {#appendix-rag-alternatives}

As of October 2026, arguments that “RAG is unnecessary” often combine three questions: must we build a vector index, must we select evidence before generation, and must we consult external sources?
Different systems can give different answers to each.
A useful comparison names the collection, task, model, tools and budget.

#### Do we need embeddings and a vector database? {#appendix-rag-without-embeddings}

A common RAG implementation splits documents into chunks, embeds them, retrieves the nearest chunks and supplies a shortlist to a generator.
The [file-search agent in Chapter 12](#agent-grep-search) offers another arrangement: search available text, read around matches, reformulate and repeat.
It can work without embeddings, especially when evidence contains distinctive names, identifiers or phrases.
It avoids embedding preparation and can search the current files directly.
Repeated calls still cost time and tokens, and success depends on finding useful vocabulary and exploring enough of the available material.

The May 2026 preprint [“Is Grep All You Need?”](https://arxiv.org/html/2605.15184v1) compares grep-like and vector retrieval on 116 conversational-memory questions.
Its regex wrapper scores matches in prepared conversation data; this is not simply the Unix command from Chapter 2.
Inline grep wins across the reported model–harness pairs in its first experiment, but changing how results are delivered can reverse the ordering.
A second experiment varies distracting conversation history and finds further dependence on the model and harness.
These results justify testing lexical agents; they do not establish superiority for scholarly discovery or evidence synthesis.

Keep indexing separate from embeddings.
A scan may become costly across many files and repeated queries, but an inverted index can accelerate lexical retrieval too. [Cursor’s search documentation, checked on 25 October 2026, describes Instant Grep as building and querying a local index while storing no codebase embeddings for search.]{#cursor-instant-grep-account} A grep-like interface therefore need not mean an unindexed scan.
This statement describes the documented design, not a measured speed advantage. [Read the documentation](https://cursor.com/docs/agent/tools/search).

Document preparation is another separate choice.
A scanned PDF needs OCR before its words can be searched as text; other PDFs need suitable extraction.
Tables, columns and images can lose evidence during conversion.
Both lexical and dense text retrieval inherit those losses.
The need for parsing does not by itself establish the need for embeddings.

#### Do we need retrieval if the documents fit in context? {#appendix-rag-long-context}

A **context window** limits how much material a model can work with, measured in tokens.
Instructions and conversation consume part of that budget, and room must remain for the response.
If a small, already selected collection fits, supplying it in full can avoid an initial top-*k* selection and preserve surrounding argument.
This is a real alternative to a separate retrieval stage over that collection.
Supplying the collection in full need not be described as RAG when there is no retrieval step over it.

Fitting into the window does not establish that the model uses every passage reliably.
Longer input can add latency, cost and distracting material; actual costs also depend on caching, repeated use and the model.
A [2024 comparison by Zhuowan Li and colleagues](https://aclanthology.org/2024.emnlp-industry.66/) found better average performance for sufficiently resourced long context in its tested settings, with lower costs for RAG.
The [2025 LaRA benchmark](https://proceedings.mlr.press/v267/li25dv.html), covering 2,326 cases and eleven models, found that the preferred approach depended on model capability, context length, task and retrieval characteristics.
Neither finding supplies a universal rule for a later product.

Retrieval and long context can also cooperate: retrieve promising documents, then supply larger passages or complete documents.
This retains a candidate boundary, while reducing the risk that a small chunk omits a qualification.
Compare both evidence selection and the model’s use of the supplied material, as [the evaluation section below](#appendix-rag-evaluation) explains.

#### Do stronger models remove the need for external evidence? {#appendix-rag-external-evidence}

Some tasks need no retrieval: rewriting a supplied paragraph is one example.
But a more capable model does not thereby gain access to private documents, newly published evidence or a library’s current subscriptions.
Those facts must reach it through some available source.
Fine-tuning may teach a task or domain patterns, but does not by itself keep changing holdings current or establish which source supports a claim.

For librarians, answering about a supplied reading pack and discovering which studies belong in an evidence base are different tasks.
Success on the first does not establish coverage on the second.
A long-context model can read everything supplied while still missing the paper nobody supplied. [Appendix F’s coverage problem](#systematic-reviews-stress-test-retrieval) therefore survives changes in context size.

Terminology should make the comparison clearer.
Under this book’s broad definition, grep-selected evidence used to generate an answer can constitute RAG.
Practitioners sometimes reserve “RAG” for the pre-indexed chunk-and-vector pipeline.
The architectural difference remains substantive whichever label is used: what is prepared beforehand, what is selected at query time, who chooses the next action, and what reaches generation?

Compare those choices on the actual task.
A successful grep-based agent challenges the necessity of a particular retrieval stack.
It does not establish that evidence selection, coverage or [retrieval evaluation](#comparing-evidence-supply) have disappeared.

### Worked example: Scopus AI and RAG Fusion {#appendix-rag-scopus}

Scopus AI is a useful worked example precisely because its documented pipeline is built from parts this book has already examined—separately, and for other reasons.

Elsevier has described the search module as follows: a user’s query is expanded by a language model into several variant queries; vector search runs against each variant; the resulting ranked lists are merged with reciprocal rank fusion; and the summary is generated from the top merged results, with references required for claims.
The technique, called **RAG Fusion**, originated in [Raudaschl’s prototype work](https://adrianraudaschl.com/projects/scopus-ai-prototype/) and was released as open source before appearing in the product; [Rackauckas (2024)](https://arxiv.org/abs/2402.03367) provides a published description and evaluation, and [Elsevier’s own account](https://scholarlykitchen.sspnet.org/2024/07/25/interview-with-maxim-khan-about-scopus-ai/) confirms the pipeline.
As elsewhere in this book, the description is as documented in 2024; the product has since added further modes, and details should be re-verified rather than assumed.

Now read that pipeline against the book:

- *Generate query variants* is the multi-query transformation of [Chapter 11](#common-query-understanding-techniques)—an answer to vocabulary mismatch ([Chapter 13](#vocabulary-mismatch)) that spends generation on the query side, as [Query2doc and HyDE](#query2doc-and-hyde) do, rather than on the answer side.
- *Vector search per variant* is [single-vector dense retrieval at collection scale](#single-vector-dense-retrieval-compress-first-compare-later) (Chapter 7), run several times.
- *Merge with reciprocal rank fusion* is exactly the [RRF of Chapter 10](#how-reciprocal-rank-fusion-combines-ranked-lists).
  Nothing about RRF changed when it moved inside a RAG system; it still rewards documents that appear high on multiple lists, and still ignores raw scores.
- *Generate from the top results* is the only genuinely new stage—and it is downstream of every decision above it.

:::: {.figure .query-flow key="rag-fusion"}
RAG Fusion, read as a composition of stages this book has already explained

::: {.track .five-step}
- **One question** what the searcher typed
- **Generate query variants** multi-query transformation · Chapter 11
- **Vector search, once per variant** single-vector dense retrieval · Chapter 7
- **Merge the ranked lists** reciprocal rank fusion · Chapter 10
- **Write the summary** the only stage this book sets aside
:::

::: caption
Four of the five stages are ones the preceding chapters explain, and every candidate boundary is fixed before the last box is reached.
Read left to right, the diagram is the argument: “RAG Fusion” names a composition, not a new kind of search.
:::
::::

The lesson is not that Scopus AI is the best or worst design.
It is that “RAG Fusion” is not a new kind of search: it is a particular composition of query transformation, dense retrieval and rank fusion, with generation appended.
A reader of this book can therefore ask precise questions of it—how many variants, generated by what, retrieved against which index, fused at what depth, and how many merged results actually reach the context—where the label alone invites none.
One caution against conflation: [Chapter 10](#two-hybrids-that-combine-differently) used Scopus AI as its example of *routing* between lexical and vector paths.
The mechanisms are compatible: routing chooses which paths run, while RAG Fusion combines lists from query variants.
A product could do both, but these differently dated accounts do not establish exactly how later Scopus AI modes combine them.

### RAG and MCP answer different questions {#appendix-rag-mcp}

[Appendix D’s warning](#appendix-misleading-overlaps) bears repeating with one addition.
RAG arranges a pipeline: retrieve, then generate an answer grounded in what was retrieved.
The Model Context Protocol (MCP) is a convention for how a model reaches a service at all—a description layer over an interface.
A system can run RAG with no MCP, calling its index directly, and most do; an agent can use MCP with no RAG, calling a search server and returning records without writing prose.

The addition: the two compose naturally, and increasingly do.
An agent that reaches a library’s search API through an MCP server and then writes a grounded summary from what came back is doing [agentic RAG](#agentic-rag-is-narrower-than-agentic-search) with MCP as its transport.
The composition does not by itself change the retrieval system on the other end of the connection, although what the agent can reach depends on which operations the server exposes; nor does it exempt that system from the questions in [Chapter 15](#choosing-and-governing-search-tools).
An MCP endpoint in front of an index is a door, not a different building.

### What generation adds to evaluation—and what it cannot fix {#appendix-rag-evaluation}

[Chapter 14](#evaluation) measured whether retrieval worked.
RAG adds a second layer of questions: is the generated answer **faithful** to the retrieved evidence—does it say only what the sources support—and are its citations **attributable**—does each claim trace to a source that actually contains it?
These are real and measurable properties, and each has an established way of being assessed. [RAGAs](https://aclanthology.org/2024.eacl-demo.16/) scores faithfulness, answer relevance and context relevance by prompting a model, without needing reference answers—cheap to run, and only as good as the judge doing the scoring.
Attribution has a stricter definition in [Attributable to Identified Sources](https://aclanthology.org/2023.cl-4.2/), which asks whether a trained assessor would affirm “according to this source, *s*” for each claim—closer to what a librarian means by a citation supporting a statement, and correspondingly slower, because it is a human annotation protocol rather than a metric a pipeline computes.
Faithfulness and attribution checks assess support in the evidence supplied or cited.
A system can score perfectly on faithfulness while summarising an incomplete context, because retrieval missed useful papers or context selection dropped them.
These checks alone cannot establish retrieval completeness; diagnose the failures of [Chapter 13](#diagnosing-failure) using the earlier stages as well.

**Trace one missing qualification.** For the open-access citation-advantage question, suppose a supporting passage limits a finding to one discipline, but the answer presents it as universal.
The following are hypothetical failure paths, not observations about a named product.

::: {.table scope="row"}
| Failure path | What to inspect | What the trace establishes |
|---|---|---|
| The supporting paper never enters the retrieved set | The executed queries, searchable source and retrieved records before context selection. | Check source coverage and candidate retrieval: the answer stage never received this evidence. |
| The paper is retrieved, but its qualifying passage is omitted from context | The retrieved text alongside the exact context supplied after selection, truncation or compression. | The evidence was lost while preparing context, even though the paper was retrieved. |
| The qualification reaches context, but the answer drops it | The supplied passage, generated claim and its attached citation. | The generator overgeneralised evidence it had; a citation to the paper does not establish support for the broader claim. |

: Evidence needed to locate a failure between search and answer.
:::

A citation list alone cannot distinguish these paths.
Preserve the retrieved set, the supplied context and the answer with its claim-to-source links.
Faithfulness checks against context can expose the third failure; diagnosing the first two requires the earlier traces.

### What to ask about a RAG product {#appendix-rag-questions}

The generated-answer section of the [vendor questionnaire](vendor-questionnaire.html) provides response and evidence fields for all seven prompts below, with references to related core questions.

- []{#vendor-g01 .li-id}Does evidence come from direct file/pattern search, an indexed lexical, dense, learnt-sparse or hybrid retriever, or a supplied collection in full?
  When retrieval is used, is the choice fixed, [blended or routed per query](#two-hybrids-that-combine-differently)?
- []{#vendor-g02 .li-id}What is indexed or scanned, what extraction and exclusions apply, and what unit reaches the model’s context ([Chapter 8](#one-document-one-chunk-and-one-vector-are-not-the-same-thing))?
- []{#vendor-g03 .li-id}Is the query transformed before retrieval, and can the transformation be inspected ([Chapter 11](#query-transformation))?
- []{#vendor-g04 .li-id}How much material reaches the context, and what selection, truncation or compression separates it from the retrieved set or supplied collection ([Chapter 7 on top-*k* boundaries](#top-k-is-a-result-boundary-not-a-dense-retrieval-method))?
- []{#vendor-g05 .li-id}Does the model choose retrieval actions, or execute a fixed sequence ([Chapter 12](#agentic-search))?
- []{#vendor-g06 .li-id}How are answer support, evidence recall, latency and total cost evaluated separately under documented budgets ([Chapter 14](#comparing-evidence-supply))?
- []{#vendor-g07 .li-id}When the answer is wrong, can retrieval failure be distinguished from generation failure ([Chapter 13](#diagnosing-failure))?

The label describes an arrangement.
The answers above describe the search system a reader will actually encounter.

---
