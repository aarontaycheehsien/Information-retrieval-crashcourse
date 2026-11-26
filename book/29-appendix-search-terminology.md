---
key: "appendix-search-terminology"
kind: "appendix"
eyebrow: "Appendix D"
meta: "Reference — dip in as needed"
section_id: "app-D"
---

## A librarian’s map of search terminology {#appendix-search-terminology}

Search terminology has multiplied quickly, but the expressions used in research papers, product documentation and marketing copy are not all synonyms.
Some name a representation, some a matching or indexing method, some a model architecture or pipeline stage, some describe only the interface, output or intended capability, and some report evidence about a system rather than describing it at all.

This appendix is a crosswalk rather than a controlled vocabulary.
Usage varies between communities and products.
Its purpose is to identify what level a label usually describes, show which apparently similar labels must be kept apart, and point back to the sections of this book that explain the underlying mechanism.
What follows is a practitioner’s reading of how these words are used rather than a sourced survey of usage, which is why the entries carry no citations: treat each one as a prompt to check what a particular vendor or paper means by the word, not as a finding about what it must mean.
For a single word defined rather than placed in a family, the [glossary](#glossary) is the quicker route.
The overlaps collected below extend the six confusions the Preface promises rather than replacing them: those six are set out, with the mechanism that settles each, at [the end of Part I](#distinction-map-interface) and [the opening of Part II](#distinction-map-vocabulary).

The convention used throughout this book is that **representation** is the broad term, **vector** names an ordered list of numbers, and **embedding** names a learnt mapping into a vector space and, by common shorthand, the vector it produces.
Sparse or dense describes the shape of a vector; specified or learnt describes how the rule that produced its values was obtained.

### A practical terminology map {#appendix-terminology-map}

When reading any of these labels, ask a prior question: *what kind of thing is being named?* A representation, an index, an architecture, a stage, a user interface and a benchmark result can all occur in the same product description without being interchangeable descriptions of it.

##### Representations, matching methods, architectures and infrastructure

::: {.table scope="row"}
| Family | Common expressions | What the label usually describes | Read in this book |
|---|---|---|---|
| Vector-based matching | vector search; vector similarity search; similarity search; embedding search; embedding-based retrieval; vector embedding search | Queries and indexed items are represented as vectors and compared using a similarity or distance function. Commercial usage often implies learnt dense embeddings, although vector representations can also be sparse and need not be learnt. | [A vector does not have to be dense or semantic](#a-vector-does-not-have-to-be-dense-or-semantic) |
| Neighbour-finding method | nearest-neighbour search; *k*-nearest-neighbour search; kNN search; approximate nearest-neighbour search; ANN search | The mechanism used to find nearby vectors. ANN is an efficiency technique; it does not say how the vectors were learnt or what they represent. | [How nearest-neighbour indexing makes dense retrieval practical](#how-nearest-neighbour-indexing-makes-dense-retrieval-practical) |
| Dense retrieval | dense retrieval; dense vector search; dense embedding retrieval; dense passage retrieval; semantic vector search | Queries and documents are represented by relatively short learnt vectors in which most dimensions are non-zero. Modern systems commonly encode the query and document independently. | [Single-vector dense retrieval](#single-vector-dense-retrieval-compress-first-compare-later) |
| Encoder architecture | bi-encoder retrieval; dual-encoder retrieval; two-tower retrieval; Siamese retrieval; single-vector retrieval | The query and document are encoded separately, allowing document representations to be precomputed. These names describe the model arrangement rather than the whole category of dense retrieval. | [How an encoder becomes a retrieval encoder](#how-a-contextual-encoder-becomes-a-retrieval-encoder); [contrast with a cross-encoder](#cross-encoder-reranking) |
| Multi-vector retrieval | multi-vector retrieval; token-level retrieval; late-interaction retrieval; ColBERT-style retrieval | A query or document retains several vectors, often one per token, instead of being compressed into one pooled vector. ColBERT is neural and dense but not conventional single-vector retrieval. | [Where ColBERT-style late interaction fits](#where-colbert-style-late-interaction-fits) |
| Sparse retrieval | sparse retrieval; sparse vector search; lexical retrieval; term-based retrieval; bag-of-words retrieval | The representation has many possible dimensions but relatively few active ones. Traditional TF–IDF and BM25 are sparse, and the category now also includes learnt models. | [Sparse and dense vectors](#a-vector-does-not-have-to-be-dense-or-semantic); [compare first-stage approaches](#comparing-the-three-first-stage-approaches) |
| Learnt sparse retrieval | learned sparse retrieval; neural sparse retrieval; sparse neural retrieval; learned lexical retrieval; vocabulary-space retrieval; neural term expansion | A neural model learns sparse, vocabulary-aligned term weights that can still be searched through an inverted index. SPLADE is the principal example in this book. | [The representation](#learnt-sparse-representations); [its place in a pipeline](#neural-ir-broader-than-dense-retrieval) |
| Traditional lexical search | keyword search; lexical search; full-text search; exact-term search; term matching | Search based on words or character sequences: direct string/pattern matching, or analysed terms searched through an index. “Keyword search” is imprecise because a lexical system can accept a natural-language question and need not apply strict Boolean rules. | [Lexical does not have to mean Boolean](#lexical-search-does-not-have-to-mean-boolean-search); [what full-text search means](#what-full-text-search-means-in-ir) |
| Boolean admission | Boolean retrieval; exact-match retrieval | Records satisfy the processed query specification or do not. This need not mean literal string matching, and a separate ranker can order the eligible records. | [Exact-match retrieval](#exact-match-retrieval); [admission and ranking](#lexical-search-does-not-have-to-mean-boolean-search) |
| Infrastructure labels | vector database; vector store; vector index; semantic index; embedding index | Storage and indexing infrastructure, not a complete retrieval method. The label alone establishes neither the quality of the representation nor how relevance is calculated. | [Vector indexing](#how-nearest-neighbour-indexing-makes-dense-retrieval-practical); [inverted indexing](#how-boolean-search-uses-an-inverted-index) |

: Terms describing what is represented, how it is compared and what infrastructure makes the comparison practical.
:::

##### Pipelines, combinations and control

::: {.table scope="row"}
| Family | Common expressions | What the label usually describes | Read in this book |
|---|---|---|---|
| Combined retrieval | hybrid search; hybrid retrieval; sparse–dense retrieval; lexical–semantic search; lexical–vector search; hybrid vector search; fusion retrieval | Results or signals from two or more retrieval routes are combined. Today “hybrid” commonly means lexical plus dense retrieval, but the word does not identify the component methods or fusion rule. | [Why hybrid retrieval remains attractive](#why-hybrid-retrieval-remains-attractive); [blending results and selecting retrieval routes](#two-hybrids-that-combine-differently) |
| Rank and score fusion | rank fusion; rank aggregation; reciprocal rank fusion; RRF; score fusion; score blending | Several result lists are merged. Rank fusion uses positions; score fusion uses component scores and therefore needs a decision about their scales and relative influence. | [RRF and score fusion compared](#how-reciprocal-rank-fusion-combines-ranked-lists) |
| Result diversification | search result diversification; diversity-aware ranking; novelty-aware ranking; MMR; IA-Select; xQuAD; DPP | A ranking or subset is chosen for relevance together with novelty, reduced redundancy or coverage of several aspects. It commonly reorders a candidate list but is not inherently dense, neural or the same operation as fusion or deduplication. | [Ranking a useful set](#ranking-a-useful-set-not-only-relevant-items); [methods and metrics in Appendix E](#appendix-diversity-aware-ranking-metrics) |
| Learning to rank | learning to rank; LTR; L2R; learnt ranking; LambdaMART; LambdaRank; RankNet | A supervised method learns how to order candidates from training examples and selected features. It may be a later reranker and need not use embeddings or a neural model. | [Learning to rank](#appendix-learning-to-rank) |
| Pipeline terminology | multi-stage retrieval; retrieve-and-rerank; candidate generation; first-stage retrieval; neural reranking; semantic reranking; cross-encoder reranking | A fast method retrieves candidates and a more expensive stage reorders a shortlist. A product’s “semantic” component may therefore be a reranker rather than its initial retriever. | [Why search systems use multiple stages](#why-search-systems-use-multiple-stages); [rerankers](#rerankers-compare-more-carefully-after-retrieval) |
| Neural umbrella terms | neural search; neural retrieval; neural information retrieval; deep retrieval; deep semantic search; learned retrieval | Any use of neural networks in retrieval or ranking. The umbrella includes dense retrieval, learnt sparse retrieval, late interaction and neural reranking; it identifies no single architecture. | [Neural IR beyond dense retrieval](#neural-ir-broader-than-dense-retrieval); [neural reranking](#rerankers-compare-more-carefully-after-retrieval) |
| Agent terminology | agentic search; agentic retrieval; search agent; deep search; deep research; iterative retrieval; multi-hop retrieval | A process that may plan, reformulate, search repeatedly, follow evidence or call several tools. This control arrangement is largely independent of whether each search is lexical, dense or hybrid. | [Fixed, adaptive and agentic](#fixed-adaptive-and-agentic-are-not-the-same-thing); [agency changes the sequence](#agency-changes-the-sequence-not-the-retrieval) |
| Access and integration | API; MCP; Model Context Protocol; MCP server; tool call; function calling; connector; integration | How one program reaches another’s service. An API is a contract a developer writes code against; MCP describes the same kind of service to a model, which reads that description while working and decides whether to call it. Neither names a retrieval method, neither changes what the underlying index contains, and neither grants access a licence did not already grant. | [Agency changes the sequence](#agency-changes-the-sequence-not-the-retrieval) |

: Terms describing how retrieval components are combined, sequenced, learnt or controlled.
:::

##### Interfaces, outputs, modalities and capability claims

::: {.table scope="row"}
| Family | Common expressions | What the label usually describes | Read in this book |
|---|---|---|---|
| Ranked output | ranked retrieval; best-match retrieval; partial-match retrieval; relevance ranking; relevance sort; Best Match | Graded scores order candidates by estimated relevance. The traditional names do not require every query term to match or imply substring matching. A product’s Best Match label does not identify its scoring formula, and hard admission conditions may still apply. | [Best-match retrieval](#best-match-retrieval); [PubMed’s documented example](#bm25-and-lexical-ranking-in-academic-search); [top-*k* as a result boundary](#top-k-is-a-result-boundary-not-a-dense-retrieval-method) |
| Meaning-oriented labels | semantic search; semantic retrieval; meaning-based search; conceptual search; intent-based search; contextual search | A goal or capability claim that the system goes beyond literal term matching, usually contrasted with lexical search. Dense retrieval over embeddings is the most familiar contemporary implementation, but the labels reveal little about architecture: lexical retrieval may supply candidates, while ontology or query expansion, learnt-sparse retrieval, dense retrieval and neural reranking may contribute meaning-oriented evidence at different stages. | [Semantic search is a goal, not an architecture](#semantic-search-is-a-goal-not-an-architecture); [vector, dense and semantic are different properties](#a-vector-does-not-have-to-be-dense-or-semantic) |
| AI umbrella labels | AI search; AI-powered search; AI-assisted search; intelligent search | A broad claim that some machine-learning or generative component contributes. It does not identify whether that component transforms the query, retrieves candidates, fuses lists, reranks results, generates an answer or merely changes the interface. | [Why the label does not reveal the pipeline](#what-this-book-is); [retrieval and generation are different operations](#retrieval-not-generation) |
| Query-interface labels | natural-language search; conversational search; question-based search; free-text search | How a query is entered, not necessarily how retrieval works. A sentence may be interpreted without being rewritten, or become a Boolean query, dense embedding or several generated searches. | [Understanding and transformation differ](#words-sent-to-retrieval-may-not-be-the-words-you-typed); [what a system can do with a query](#common-query-understanding-techniques) |
| Generative approaches | generative retrieval; generative search; generative information retrieval; LLM-based retrieval | In the strict research sense, a model generates document identifiers or retrieval targets. Product usage often means conventional retrieval followed by answer generation, which is a different arrangement. | [This book separates retrieval from generation](#retrieval-not-generation); [generated text used for retrieval](#query2doc-and-hyde). Strict generative retrieval is not developed here. |
| RAG terminology | retrieval-augmented search; RAG search; agentic RAG; retrieval-augmented answering; grounded search; answer engine | Retrieval supplies evidence to a generative answer. RAG does not specify its retriever, which may be lexical, dense, sparse, hybrid or selected by an agent. | [The basic RAG pattern](#appendix-rag-pattern); [agentic RAG and agentic search](#agentic-rag-is-narrower-than-agentic-search); [Appendix G](#appendix-rag) |
| Media and modality | multimodal search; cross-modal retrieval; text-to-image retrieval; image–text search | The query and retrieved items may use different media, often through a shared representation space. “Multimodal” describes the data involved, not the retrieval architecture. | This book concentrates on text retrieval; multimodal retrieval is not developed here. |

: Terms describing what a system accepts or returns, the media involved, or a claimed capability rather than an implementation.
:::

##### Evaluation and performance claims

::: {.table scope="row"}
| Family | Common expressions | What the label usually describes | Read in this book |
|---|---|---|---|
| Retrieval measures | precision; recall; precision@k; MRR; MAP; nDCG; α-nDCG; ERR-IA; subtopic recall; F1 | What was measured about a ranking, not a property the system possesses. Each encodes a different idea of a good result list. Diversity-aware measures additionally need aspect-level judgements, so they cannot reward a diversity dimension the assessment never represented. | [Precision and recall](#precision-and-recall); [rank-aware measures](#rank-changes-the-question); [diversity-aware measures](#appendix-diversity-aware-ranking-metrics) |
| Judgements and test collections | relevance judgement; qrels; ground truth; gold set; test collection; pooling | The fixed apparatus that makes two systems comparable at all. “Ground truth” overstates it: these are recorded human decisions about particular needs, and unjudged records are normally scored as irrelevant. | [Relevance is a judgement](#relevance-is-a-judgement); [test collections](#test-collections-and-benchmarks) |
| Benchmarks and transfer | benchmark; leaderboard; BEIR; MTEB; zero-shot; out-of-distribution (OOD); out-of-domain; distribution shift; generalisation | How a system performed on someone else’s collection, queries, tasks and assessors. “Zero-shot” means the model was not trained on that particular benchmark—not that it needs no training, and not that it will transfer to your collection. | [What a benchmark number is worth](#test-collections-and-benchmarks); [OOD transfer](#out-of-distribution) |
| Comparative claims | state of the art; SOTA; outperforms; beats BM25; improves relevance by n% | A comparison on some benchmark, using some metric, against some baseline. Until all three are named it is not yet a claim that can be checked, and it is never by itself a claim about a particular library’s collection. | [What a number cannot settle](#what-a-number-cannot-settle); [building an evaluation set you own](#building-a-local-evaluation-set) |

: Terms describing evidence about a system rather than the system itself.
:::

### The most misleading overlaps {#appendix-misleading-overlaps}

The safest reading of an attractive label is as a question, not an answer.
These eight terminology comparisons restate four of the [six core distinctions](#core-distinction-checklist) as reminders and add four more; they are not a replacement syllabus.

:::: {.terminology-overlaps}
::: {.terminology-overlap}
#### “Semantic search” does not mean “dense retrieval”

The association is understandable: dense retrieval over vector embeddings is the most familiar contemporary implementation of semantic search.
It is not an equivalence. [Chapter 7 establishes the main distinction](#semantic-search-is-a-goal-not-an-architecture): semantic describes a goal, usually contrasted with lexical matching, while BM25, ontology expansion, dense retrieval and neural reranking describe mechanisms that may contribute to it at different stages.
Learnt sparse retrieval and query expansion can support meaning-oriented matching, while another system may apply a semantic model only when [reranking a lexical shortlist](#rerankers-compare-more-carefully-after-retrieval).
This appendix is a terminology reminder, not where the argument is introduced.
:::

::: {.terminology-overlap}
#### “Neural information retrieval” does not always mean “dense retrieval”

A common form of first-stage neural retrieval today uses [dense bi-encoders](#single-vector-dense-retrieval-compress-first-compare-later) built from Transformer (neural) encoder models.
Increasingly, embedding models are also being adapted from decoder-only language-model backbones.[^decoder-backbone-embeddings]

Dense representations can also be learnt using non-Transformer neural architectures.
Earlier neural retrieval systems in the 2010s used feed-forward networks[^dssm-non-transformer], convolutional networks[^cdssm-non-transformer], and paired recurrent encoders such as LSTMs[^lstm-non-transformer] to map queries and documents into dense vectors.
Neither dense retrieval nor bi-encoder retrieval therefore necessarily implies a Transformer.

Also, neural information retrieval is broader than conventional single-vector dense retrieval.
It includes first-stage methods such as [learnt sparse retrieval and ColBERT-style late interaction](#neural-ir-broader-than-dense-retrieval), as well as neural ranking architectures such as [cross-encoders](#cross-encoder-reranking), which are commonly used to rerank an initial set of candidates.[^pre-transformer-interaction-rankers]

**Neural information retrieval is therefore an umbrella category covering several distinct retrieval and ranking architectures.**
:::

::: {.terminology-overlap}
#### “Vector search” does not necessarily mean “semantic search”

A vector can encode lexical weights, locations, citation patterns or manually chosen features.
A similarity function compares whatever those vectors represent; it does not make the representation semantic, and even a semantic similarity score is evidence about relevance rather than a relevance judgement or probability.
Useful semantic neighbourhoods depend on what was represented and how it was trained; [vector, dense and semantic are separate properties](#a-vector-does-not-have-to-be-dense-or-semantic). [Chapter 7 explains the comparison](#vector-similarity-explained), and the [Vector Similarity Lab](vector-similarity-lab.html) makes the distinction interactive.
:::

::: {.terminology-overlap}
#### “Embedding search” is informal; “vector embedding search” is largely redundant

Embedding search usually means comparing vectors produced by learnt mappings.
The longer phrase “vector embedding search” adds little precision because embeddings already live in vector spaces.
In either case, the useful questions are [what was embedded, what representation was produced and what training shaped the space](#from-word2vec-to-retrieval-embeddings).
:::

::: {.terminology-overlap}
#### “Natural-language search” says nothing about the backend

The label may mean only that the interface accepts a sentence.
The system may [rewrite it before retrieval](#words-sent-to-retrieval-may-not-be-the-words-you-typed), then use ordinary lexical matching, dense retrieval or several agent-generated searches.
:::

::: {.terminology-overlap}
#### “Hybrid search” needs a qualifier

Prefer “hybrid lexical–dense retrieval” when that is what is meant.
Hybrid can also describe other combinations, and even two lexical–dense systems may [route and fuse their evidence differently](#two-hybrids-that-combine-differently).
:::

::: {.terminology-overlap}
#### “MCP” is not an alternative to “RAG”—or to an API

They answer different questions. **RAG** arranges a pipeline: retrieve, then let a model generate an answer grounded in what was retrieved. **MCP** is a convention for how a model reaches a service at all.
A system can run RAG with no MCP, calling its index directly, and most do; an agent can use MCP with no RAG, calling a search server and handing back records without writing prose.
Products shipping both at once are what make the pair look like rivals. **API** belongs in the same correction: MCP is a description layer over the kind of interface libraries have called for years, aimed at a model instead of a developer, and it grants no access a licence did not already grant. [Chapter 12](#agency-changes-the-sequence-not-the-retrieval) shows what does and does not change when a vendor exposes its search this way. [Appendix G](#appendix-rag-mcp) adds the case the rivals framing obscures: the two compose, as when an agent reaches a search service over MCP and then writes a grounded answer from what came back.
:::

::: {.terminology-overlap}
#### “State of the art” names a benchmark, not a capability

A claim to beat the state of the art is a claim about one metric on one test collection against one baseline.
It carries no guarantee about a different collection, a different discipline, a different language or a different definition of relevance—and an average improvement is compatible with getting systematically worse on the queries a particular library cares about. [Chapter 14](#what-a-number-cannot-settle) sets out what to ask of such a claim.
:::
::::

---

[^decoder-backbone-embeddings]: **Qwen3-Embedding** is a clear published example of this direction.
    The Qwen team describes its embedding series as built on the Qwen3 foundation model and deployed as a dual encoder, using the hidden state at the final `[EOS]` token as the text representation.
    Qwen models are [causal, or decoder-only, language models](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html).
    Google’s **Gemini Embedding** report similarly describes an embedding model that leverages the capabilities of the Gemini large-language-model family, while the later [Gemini Embedding 2](https://ai.google.dev/gemini-api/docs/models/gemini-embedding-2) extends that lineage to multimodal inputs.
    The Qwen documentation makes the decoder-style adaptation explicit; Google establishes the Gemini lineage but discloses fewer details about the precise architectural conversion.
    See the Qwen team, “[Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models](https://qwenlm.github.io/blog/qwen3-embedding/)” (2025), and Lee et al., “[Gemini Embedding: Generalizable Embeddings from Gemini](https://arxiv.org/abs/2503.07891)” (2025).

[^dssm-non-transformer]: **DSSM** (Huang et al., 2013) converted queries and documents into letter-trigram “word-hashing” vectors, passed them through deep feed-forward networks, and projected them into a common low-dimensional semantic space.
    Cosine similarity supplied the matching score, while clickthrough data trained the model to favour clicked documents over sampled alternatives.
    It is an early non-Transformer example of dense query and document representations used for web search.
    See Huang et al., “[Learning Deep Structured Semantic Models for Web Search Using Clickthrough Data](https://www.microsoft.com/en-us/research/publication/learning-deep-structured-semantic-models-for-web-search-using-clickthrough-data/)” (CIKM 2013).

[^cdssm-non-transformer]: **C-DSSM**, also described as a convolutional latent semantic model, replaced DSSM’s bag-of-words-style treatment with convolution over local word n-gram contexts, followed by max pooling and further nonlinear layers that produced one global vector for each query or document.
    It was likewise trained from clickthrough data and compared the resulting vectors in a shared space.
    See Shen et al., “[A Convolutional Latent Semantic Model for Web Search](https://www.microsoft.com/en-us/research/publication/a-convolutional-latent-semantic-model-for-web-search/)” (2014).

[^lstm-non-transformer]: **Paired LSTM-RNN encoders** provide a recurrent alternative.
    Palangi et al. used an LSTM-RNN on the query side and another on the document side, reading each sequence word by word and using the final hidden representation as its dense sentence vector; cosine similarity then scored the pair.
    The paper trained separate query-side and document-side parameter sets.
    Calling this a *Siamese LSTM* is therefore convenient but slightly loose if *Siamese* is reserved for encoders with tied weights; *paired LSTM encoders* or *LSTM dual encoder* is more exact.
    See Palangi et al., “[Deep Sentence Embedding Using Long Short-Term Memory Networks: Analysis and Application to Information Retrieval](https://arxiv.org/abs/1502.06922)” (2016).

[^pre-transformer-interaction-rankers]: Before Transformer cross-encoders, interaction-focused neural rankers such as **DRMM** and **K-NRM** already learnt relevance from detailed query–document term interactions.
    They are conceptual predecessors rather than cross-encoders in the present architectural sense.
    DRMM summarised per-query-term similarity histograms with a feed-forward matching network and a term-gating network, while K-NRM applied kernel pooling over a query–document word-similarity matrix.
    Neither jointly contextualised a concatenated query–document sequence through Transformer self-attention.
    See Guo et al., “[A Deep Relevance Matching Model for Ad-hoc Retrieval](https://doi.org/10.1145/2983323.2983769)” (CIKM 2016), and Xiong et al., “[End-to-End Neural Ad-hoc Ranking with Kernel Pooling](https://arxiv.org/abs/1706.06613)” (SIGIR 2017).
