---
key: "representations-and-units"
kind: "chapter"
eyebrow: "Chapter 8"
meta: "About 16 min"
question: "What is actually stored, and what does one stored item stand for?"
---

## Representations and indexed units {#representations-and-units}

::: {.stage-map on="analysis first-stage"}
:::

::: chapter-orient
The previous chapter compared stored vectors without saying what one of them contains.
It also used *indexed unit* as though the phrase were self-explanatory.
What a retrieval stage can match depends on the indexed text, how it is divided into units and how those units are represented.

This chapter views the lexical machinery you already know as coordinates: binary presence, term frequency, TF–IDF and BM25 weights.
This is a comparison of representations, not a chronological claim that BM25 was derived from TF–IDF.
That progression is enough to show that *vector* names the numerical object, while *sparse*, *learnt* and *semantic* name three independent properties.
The chapter also distinguishes a source document from its searchable units and explains how matches from those units become displayed results.
:::

::: {#distinction-vector-semantic .key-distinction-label}
Key distinction
:::

### A vector does not have to be dense or semantic {#a-vector-does-not-have-to-be-dense-or-semantic}

Dense text embeddings are now the most visible vectors in search, but they are not the only kind.
Long before dense retrieval, lexical systems could already represent a document as an ordered list of numbers.
The easiest way to see this is to build the representation one decision at a time.

#### Step 1 — Fix the coordinate system: one vocabulary term per dimension {#step-1-fix-the-coordinate-system}

Suppose a tiny collection contains three documents:

- **D1:** *heart attack treatment*
- **D2:** *job interview tips*
- **D3:** *cancer treatment*

After the text has been analysed, the collection vocabulary is `[attack, cancer, heart, interview, job, tips, treatment]`.
That ordered vocabulary defines a seven-dimensional vector space.
Coordinate 1 always means `attack`, coordinate 2 always means `cancer`, and so on.
A real collection may have millions of vocabulary dimensions; the ordering is arbitrary, but it must remain consistent.

This first choice determines what the coordinates *mean*.
It does not yet determine what numbers to put in them.

#### Step 2 — Binary presence: a Boolean-like starting point {#step-2-binary-presence}

Put `1` in a coordinate when the term is present and `0` when it is absent:

- **D1:** `[1, 0, 1, 0, 0, 0, 1]`
- **D2:** `[0, 0, 0, 1, 1, 1, 0]`
- **D3:** `[0, 1, 0, 0, 0, 0, 1]`

These are vectors.
They are also **sparse**: each vector is defined over all seven vocabulary dimensions, but most coordinates are zero.
In a million-term vocabulary, a short document might activate only a few hundred coordinates.
Implementations therefore store the non-zero term–weight pairs rather than writing out every zero.

The word *Boolean-like* needs care here.
A binary vector records the same presence or absence evidence used by Boolean retrieval, but **the vector does not itself specify AND, OR or NOT**.
For the query *heart treatment*, the query vector is `[0, 0, 1, 0, 0, 0, 1]`.
Counting shared ones gives D1 two overlaps, D3 one and D2 none.
That is a simple graded overlap score.
By contrast, the strict Boolean query `heart AND treatment` admits only D1, while `heart OR treatment` admits D1 and D3.
The coordinates supply term evidence; the retrieval rule decides how that evidence is used.

:::: {.figure key="binary-sparse-lexical-vector-space"}
The same three documents in a full collection vocabulary

![A two-stage worked example. First, a collection dictionary is built from a corpus, running alphabetically from a and aardvark through attack, cancer, heart, interview, job and treatment to zygote, with an example vocabulary size of 2,345,678 terms. Second, the same three documents — heart attack treatment, job interview tips and cancer treatment — are written as binary vectors across that vocabulary: one column per term, a 1 where the term occurs and 0 everywhere else, so almost every entry is zero. Side panels note where the binary values come from, that documents match a query through overlapping ones, and that an inverted index stores only the terms that actually occur.](images/08%20A%20vector%20does%20not%20have%20to%20be%20dense%20or%20semantic/binary-sparse-lexical-vector-space.png){width="1402" height="1122"}

::: caption
The seven-dimensional space used above is this same construction with the vocabulary shrunk to fit on a page.
At collection scale the coordinate system has millions of columns and a short document activates a handful of them, which is why the zeros are never actually stored.
The values here are binary for clarity; the steps that follow replace them with counts and then with weights. [Open the full-resolution figure.](images/08%20A%20vector%20does%20not%20have%20to%20be%20dense%20or%20semantic/binary-sparse-lexical-vector-space.png)
:::
::::

#### Step 3 — Term frequency: replace “is it present?” with “how much is present?” {#step-3-term-frequency}

Binary presence treats one occurrence and ten occurrences alike.
A **term-frequency** or **TF** vector keeps the same vocabulary dimensions but replaces the ones with counts or count-derived values.
If D1 were *heart attack treatment treatment treatment*, its raw-TF vector would be `[1, 0, 1, 0, 0, 0, 3]`.
The coordinate meanings have not changed; only the weighting rule has.

TF captures repetition, which is often useful evidence that a document is about a term.
Raw counts also create a problem: repetition can grow without limit, and longer documents have more opportunities to accumulate large counts.
A better lexical weighting scheme should decide both how much repeated use helps and how document length should affect the score.

#### Step 4 — TF–IDF: let distinctive terms count more {#step-4-tf-idf}

Term frequency looks only inside one document. **Inverse document frequency**, or **IDF**, looks across the collection.
A term that appears in nearly every document is usually less discriminating than one that appears in only a few.
A common schematic form is `TF–IDF(t,d) = TF(t,d) × IDF(t)`, with `IDF(t)` increasing as the term’s document frequency decreases.

In the toy collection, `treatment` occurs in D1 and D3, whereas `heart` occurs only in D1.
TF–IDF therefore gives the rarer `heart` dimension more collection-level emphasis.
The result is still a vocabulary-aligned sparse vector: absent terms remain zero, present terms receive calculated non-zero weights, and every coordinate can still be named.

#### Step 5 — BM25: add saturation and document-length normalisation {#step-5-bm25}

[BM25](#bm25-words-as-weighted-clues) develops the same lexical idea further.
It retains IDF, but repeated occurrences show **diminishing returns**: the tenth occurrence of a term adds less evidence than the first.
It also adjusts term-frequency evidence in relation to document length, so a long document does not receive an automatic advantage merely because it contains more words.
Parameters control the strength of saturation and length normalisation.

BM25 can therefore be viewed as a calculated sparse vector representation.
Query terms activate vocabulary dimensions, document coordinates contain BM25-style term contributions, and the final score can be expressed as a dot-product-style sum over matching dimensions.[^bm25-sparse-vector] This is a mathematical view of the score, not a claim that a search engine writes millions of zeros or performs dense nearest-neighbour search.
In practice, an [inverted index](#how-bm25-uses-the-same-inverted-index) jumps directly to the postings for active query terms and accumulates their contributions.

:::: {.figure key="lexical-vector-weighting-progression"}
One vocabulary space, progressively richer lexical weights

![A five-step worked example uses the same seven-term collection vocabulary to represent three documents as binary-presence, term-frequency, TF–IDF and BM25 vectors. The coordinates stay aligned with vocabulary terms while the weighting rule changes. A side panel shows that an inverted index stores only active term entries and accumulates their weights for a query.](images/08%20A%20vector%20does%20not%20have%20to%20be%20dense%20or%20semantic/lexical-vector-weighting-progression.png){width="1536" height="1024"}

::: caption
Binary presence, TF, TF–IDF and BM25 can all use the same vocabulary-aligned coordinates.
What changes is the value placed in each active coordinate and the rule used to score a query; the vectors remain sparse, so an inverted index can store only non-zero term entries. [Open the full-resolution figure.](images/08%20A%20vector%20does%20not%20have%20to%20be%20dense%20or%20semantic/lexical-vector-weighting-progression.png)
:::
::::

| Representation or rule | What a document coordinate stores | What this adds | Important limitation or qualification |
|---|---|---|---|
| Binary presence | `1` if the term occurs; otherwise `0` | A compact record of term presence | Does not distinguish one occurrence from many |
| Strict Boolean retrieval | May use the same presence evidence | AND, OR and NOT impose hard admission conditions | The operators are retrieval logic, not properties of the vector itself |
| Term frequency | A count or count-derived value | Repeated use can provide more evidence | Raw repetition and document length can dominate |
| TF–IDF | Term frequency weighted by collection rarity | Distinctive terms contribute more than ubiquitous ones | Exact TF and IDF formulas vary; basic forms do not provide BM25’s full saturation and length treatment |
| BM25 | A calculated term contribution using IDF, saturated TF and length normalisation | A strong ranked lexical score | It remains lexical: normally at least one analysed query term must match |

: The lexical progression keeps vocabulary dimensions fixed while enriching the values and retrieval rule.

The progression is therefore **not** “Boolean vectors become semantic vectors”.
The dimensions remain lexical throughout.
What changes is the value stored in each vocabulary coordinate and the rule that turns active coordinates into an eligible set or a ranking.

A dense embedding is built the other way round.
Nobody assigns its coordinates to stated vocabulary terms.
They are **latent dimensions**, settled during training, and what any one of them contributes is spread across the representation rather than readable from that coordinate alone.

:::: {.figure key="lexical-and-dense-vector-dimensions"}
What vector dimensions mean in lexical and dense spaces

![A side-by-side explanation of vector dimensions. In a sparse lexical space, a collection dictionary supplies one interpretable term dimension per column and most values are zero. In a dense embedding space, a model learns many latent dimensions, most values are non-zero and individual coordinates usually do not correspond to words. A lower panel contrasts the two approaches and shows SPLADE as a learnt sparse bridge that retains vocabulary dimensions.](images/08%20A%20vector%20does%20not%20have%20to%20be%20dense%20or%20semantic/lexical-and-dense-vector-dimensions.png){width="1448" height="1086"}

::: caption
A vector is a list of numbers, but the vector space determines what each number means.
Sparse lexical vectors use explicit vocabulary dimensions and support efficient inverted indexing; dense embeddings use learnt latent dimensions whose meaning is distributed across the representation.
SPLADE is a useful bridge: it is learnt and sparse while retaining vocabulary-aligned coordinates. [Open the full-resolution figure.](images/08%20A%20vector%20does%20not%20have%20to%20be%20dense%20or%20semantic/lexical-and-dense-vector-dimensions.png)
:::
::::

### Four questions about a representation {#four-questions-about-a-representation}

1. **Is it a vector?** A vector is an ordered list of numbers.
   Binary presence, TF–IDF, BM25-style weights and dense embeddings can all be written as vectors.
2. **Is it sparse or dense?** Sparse means that relatively few dimensions are active; dense means that most are active.
   This describes the shape of a representation.
3. **Was the weighting rule specified or learnt?** Both routes calculate their numbers.
   TF–IDF and BM25 apply a specified formula to collection statistics; a neural model applies a weighting or mapping fitted during training.
4. **What evidence do the dimensions preserve?** Dimensions may stand for words, metadata fields, locations, colours, citation patterns or distributed latent features.
   Their design and training—not density alone—determine whether the representation supports meaning-oriented matching.

The same text could be represented by a sparse lexical vector such as `[1.6, 1.4, 2.2, 0, 0]` over `[open, access, citation, advantage, embargo]`, or by a toy dense embedding such as `[0.14, −0.37, 0.81, 0.05, −0.21, 0.63, −0.12, 0.28]`.
In the first, each coordinate has a recognisable term label.
In the second, most coordinates are active, but `latent 3 = 0.81` does not mean “citation” by itself.
These values are illustrative of structure, not output from a named model.

:::: {.figure key="sparse-vs-dense-vectors"}
Sparse and dense vectors compared

![A sparse vocabulary-aligned vector with mostly zero coordinates compared with a dense learnt vector with values in most latent coordinates](images/08%20A%20vector%20does%20not%20have%20to%20be%20dense%20or%20semantic/ChatGPT%20Image%20Jul%2026,%202026,%2009_35_31%20PM.png){width="1448" height="1086"}

::: caption
A sparse lexical representation may be enormous in principle yet cheap to store because only a small number of term coordinates are active.
A dense embedding is usually much shorter, but most of its latent coordinates contain non-zero values.
:::
::::

Density still says nothing by itself about semantics.
An article described by `[year, pages, references, citations] = [2026, 14, 32, 87]` has a fully active—and therefore dense—feature vector.
Its coordinates are explicit bibliographic facts, not a semantic text embedding.

### The converse case: learnt weights in vocabulary coordinates {#learnt-sparse-representations}

A representation can be as sparse as BM25’s, and keep coordinates that each stand for a vocabulary term, while having every number in it computed by a learnt mapping.
This is **learnt sparse retrieval**, and [**SPLADE**](https://doi.org/10.1145/3404835.3463098) is its principal example in this book.

Each dimension still stands for one vocabulary term, and almost all of them are still zero.
The vocabulary is not BM25’s, though: SPLADE’s coordinates are the output vocabulary of a transformer language model—[WordPiece subword units](#appendix-wordpiece-worked-example) in the standard implementation—rather than whatever analysed terms a lexical index happens to hold.

BM25 and learnt sparse models both use sparse, vocabulary-aligned representations, but calculate their weights differently.
BM25 reads a count off the document and adjusts it using collection statistics.
A learnt sparse model instead *predicts* a weight for each term in its vocabulary, having read the passage.
The prediction ranges over the whole vocabulary, not only the words present, so a term the text never contained can still receive weight.
A training penalty then drives the overwhelming majority of the remaining predictions to zero.
That penalty is what keeps the representation sparse enough to hold in an inverted index.[^splade-mechanics]

A toy representation of *heart attack* might therefore activate `heart`, `attack`, `myocardial` and `infarction` while leaving almost the whole vocabulary at zero.
The last two were never typed and need not appear anywhere in the passage.
They are still named coordinates, so the representation can be read back: an analyst can list which terms received weight and how much, which a pooled dense embedding does not permit.
The whole words used here are schematic; a real model activates entries of its own subword vocabulary.

:::: {.figure key="splade-sparse-expansion"}
A learnt sparse model expands within the vocabulary

![Schematic SPLADE query expansion: delulu, job and expectations receive weights alongside additional terms unrealistic, career and search](images/08%20Representations%20and%20indexed%20units/ChatGPT%20Image%20Jul%2026,%202026,%2009_44_49%20PM.png){width="1448" height="1086"}

::: caption
Because the weight for each vocabulary term is predicted rather than counted, terms absent from the input can receive weight.
This schematic query example starts with “delulu job expectations” and also activates terms such as “unrealistic” and “career”; the displayed weights illustrate the mechanism, not measured output from a specified model.
Every activated dimension still carries a term label, and almost every other dimension stays at zero.
:::
::::

Judged by the four questions above, the representation is *learnt*, like a dense embedding; *sparse* and vocabulary-labelled, like BM25; and more meaning-aware than literal typed-term matching.
Learnt sparse retrieval is therefore one alternative to running separate lexical and dense retrievers, because a single inverted index can carry both exact terms and learnt expansions; it can also be one of the routes in a hybrid. [Chapter 9](#learnt-sparse-in-the-pipeline) explains its use in a retrieval pipeline; [Appendix C](#appendix-learnt-sparse-query-cost) examines the query-time cost of expansion.

| Method or case | Shape | Where the numbers come from | What the dimensions or conditions represent |
|---|---|---|---|
| Boolean conditions | Not primarily a graded vector ranking | Searcher-specified logic over indexed terms | Hard lexical admission requirements |
| BM25 | Sparse | Specified formula over collection statistics | Vocabulary terms and their lexical evidence |
| Explicit bibliographic features | Potentially dense | Measured or recorded values | Named fields such as year, pages and citations |
| SPLADE-style retrieval | Sparse | Learnt mapping, trained under sparsity constraints | Vocabulary terms, including learnt expansions |
| Dense bi-encoder | Dense | Learnt neural mapping | Distributed latent features |

: Representation shape, provenance and evidence are independent properties.

:::: {.figure key="density-and-learning-axes"}
Density and learning are separate axes of a representation

![A two-by-two matrix. The horizontal axis, how the representation is produced, runs from a specified rule on the left to a learnt mapping on the right. The vertical axis, representation shape, runs from sparse at the top to dense at the bottom. Top left, BM25: sparse weights computed using a specified formula and collection statistics. Top right, learnt sparse retrieval such as SPLADE: sparse weights computed using a learnt neural mapping. Bottom left, latent semantic analysis: dense vectors from a specified decomposition of collection statistics using truncated SVD, not a mapping fitted to training data, and little used today. Bottom right, dense bi-encoder: dense embeddings computed using a learnt neural mapping. A panel to the side notes that Boolean search is primarily logical admission rules rather than graded vector ranking. A banner below reads: do not equate sparse with lexical and dense with semantic.](images/08%20A%20vector%20does%20not%20have%20to%20be%20dense%20or%20semantic/density-and-learning-axes.png){width="1448" height="1086"}

::: caption
BM25 is sparse and uses a specified weighting rule, SPLADE is sparse and uses a learnt one, and a dense bi-encoder produces dense embeddings from a learnt mapping.
Latent semantic analysis fills the fourth quadrant: its dimensions come from a specified matrix decomposition over collection statistics rather than from a mapping fitted to training examples, which is why it sits on the specified side despite being derived from data.
It is little used in current retrieval and is not otherwise covered in this book.
Whether a representation is sparse or dense does not tell us whether the rule that produced it was specified or learnt.
:::
::::

How vectors are compared is one more independent choice.
Dot product can combine sparse lexical weights or dense latent features; cosine similarity can likewise be applied to different numerical representations.
Neither operation makes the underlying vector dense, learnt or semantic. [Chapter 7’s similarity explanation](#vector-similarity-explained) and the [Vector Similarity Lab](vector-similarity-lab.html) work through that arithmetic. **The choice of representation does not determine the comparison rule or which scored records are returned.**

Terminology varies across fields and systems.
This book keeps [Chapter 5’s](#representation-vector-embedding-title) terms; other sources may call SPLADE-style outputs **sparse embeddings**.[^embedding-terms]

### One document, one chunk and one vector are not the same thing {#one-document-one-chunk-and-one-vector-are-not-the-same-thing}

Dense retrieval also forces us to stop using **document** as though it meant only one thing.

A source document might be an article, paper, report, webpage or book.
The retrieval system may index its abstract, sections, paragraphs, sentences or overlapping token windows.
Those are the **indexed units**.

A 20-page article might therefore produce one indexed abstract, ten section units or 50 overlapping passages.
In a conventional dense bi-encoder, each of those indexed units receives one pooled vector, so 50 passages become 50 independently searchable vectors.
The units stay separate: no single vector captures the complete paper, and nothing automatically combines evidence spread across different chunks.

:::: {.figure key="chunking-strategies"}
The same article indexed under different chunking strategies

::: {.include src="figures/chunking-strategies.html"}
:::

::: caption
How finely the source is cut, how each unit is represented and how matches are grouped back into results are separate choices, and only the last is visible in a result list.
:::
::::

These are separate choices:

- **Source-document granularity:** the object a person thinks of as the document.
- **Indexed-unit granularity:** the text unit the system searches.
- **Representation granularity:** how each indexed unit is encoded.
- **Result aggregation:** whether matching passages are displayed separately or combined into one article-level result.

:::: {.figure key="paper-as-many-vectors"}
A paper split into many searchable chunks and vectors

![A paper split into many searchable chunks and vectors](images/08%20One%20document,%20one%20chunk%20and%20one%20vector%20are%20not%20the%20same%20thing/ChatGPT%20Image%20Jul%2026,%202026,%2009_41_26%20PM.png){width="1536" height="1024"}

::: caption
Many independently searchable units do not mean that the complete paper has been captured faithfully, nor that evidence spread across chunks will be combined.
:::
::::

The [Wiley AI Gateway](https://aarontay.substack.com/p/from-fixed-search-workflows-to-agentic) returns chunks of the *full text* that may be relevant to a query, alongside the paper’s metadata—so the indexed unit is a passage, and evidence buried in a methods section is reachable.
A discovery layer built over [records described by their metadata and abstracts](#bm25-and-lexical-ranking-in-academic-search) is working with a much coarser unit.
Both may describe themselves as searching articles.

**Indexed units determine what can match at a particular retrieval stage.** An abstract index cannot directly match a claim found only in the results section.
A later fetch of full text, neighbouring passages or a parent section may nevertheless supply that evidence.
Ask separately what the system indexes, what it retrieves and what it supplies as context.

When evaluating a product, ask what text was embedded, how large each unit was, and how matching passages are combined into article-level results.[^chunking] In RAG systems chunking also decides what evidence is available for an answer.
The system may supply the retrieved chunk itself, fetch a larger unit, or compress several retrieved units before the model’s context is assembled.
These choices affect the evidence supplied to the answer generator. [Appendix G](#appendix-rag) examines how retrieved passages become context for generation.

:::: chapter-close
1. A *vector* is an ordered list of numbers.
   Binary presence, term frequency, TF–IDF and BM25 weights can all be written as vectors, so the word names the numerical object rather than any property of it.
2. *Sparse* and *dense* describe the shape of a representation; *specified* and *learnt* describe how the rule that produced its numbers was obtained.
   The two axes vary independently—BM25 is sparse with a specified rule, SPLADE is sparse with a learnt one.
3. Density alone does not establish whether a representation supports semantic matching.
   A fully active vector of bibliographic facts is dense and not semantic; a learnt sparse representation can be meaning-aware with almost every dimension left at zero.
4. Source document, indexed unit, representation and result aggregation are four separate choices, and only the last of them is visible in a result list.
5. An indexed retrieval stage can match only its indexed evidence; direct file search is limited by the text it can access and scan.
   A later fetch may supply more text, so searchable units and generator context must be documented separately.

::: {.chapter-transition}
A first-stage retriever, lexical or dense, has to be fast enough to run against an entire collection—which limits how carefully it can compare anything.
The next chapter asks what a system can afford once it has a shortlist.
:::
::::

::: self-check
A vendor says its product “uses vectors, not keywords”. What has that ruled out?

:   Almost nothing.
    A vector is an ordered list of numbers, and the lexical representations in this chapter are vectors too—BM25 term weights can be written as one.
    The claim describes the numerical object, not whether the dimensions are vocabulary terms or latent features, not whether the rule behind them was specified or fitted during training, and not whether the comparison is meaning-aware.

BM25 and SPLADE both produce sparse representations. What separates them, and what does that tell you about the word *sparse*?

:   Provenance.
    BM25’s weights come from a specified formula over collection statistics; SPLADE’s come from a mapping trained under a sparsity constraint, which also lets it activate terms the document never contained. *Sparse* therefore describes only the shape—few active dimensions out of many—and settles neither where the numbers came from nor whether the representation is meaning-aware.

A product advertises “semantic search over full text”. What two things must you establish?

:   What the indexed unit actually is — titles, abstracts, sections or passages — because this controls what can match at that stage; also ask whether later steps fetch full text or expand context.
    And how several matching chunks from one paper are turned back into a single article-level result.
:::

[^bm25-sparse-vector]: A simplified sparse-vector decomposition of BM25 can be written as:

    $$
    \operatorname{score}(q,d)=\sum_{t\in V}w_q(t)w_d(t),
    $$

    where $V$ is the vocabulary.
    The query weight is zero for terms absent from the query.
    The document weight is zero for terms absent from the document and otherwise stores the relevant BM25 contribution, including inverse document frequency, term-frequency saturation and length normalisation.
    Depending on the variant, query term-frequency weighting may be placed in $w_q(t)$.
    This formulation is asymmetric in spirit because query-side and document-side weights play different roles; it should not be confused with cosine similarity between symmetrically weighted TF-IDF vectors.
    Calling BM25 a sparse vector representation does not make it a learnt embedding model.

[^splade-mechanics]: SPLADE uses a transformer’s masked-language-modelling output vocabulary to produce vocabulary-aligned weights.
    Pooling combines token-level predictions into one sparse representation for the query or indexed unit.
    A transformation such as $\log(1+\operatorname{ReLU}(x))$ provides a saturation effect, while explicit regularisation encourages most vocabulary dimensions to remain inactive.
    The architecture and regularisation changed across SPLADE versions, but the central design remains learnt weighting and expansion in a sparse lexical space suitable for inverted-index retrieval.

[^embedding-terms]: **Embedding** is used inconsistently.
    In a broad mathematical sense, it names a mapping into a vector space.
    In machine-learning usage, it usually implies a learnt mapping, while the vector produced by that mapping is also commonly called an embedding.
    This book uses **representation** as the umbrella term, **vector** for the numerical object, **BM25 sparse representation** for lexical weights from a specified formula, **learnt sparse representation** for systems such as SPLADE, **single-vector dense embedding** for pooled learnt vectors, and **multi-vector dense representation** for late-interaction systems such as ColBERT.
    Other sources may use **sparse embedding** for SPLADE-style outputs.

[^chunking]: Chunking and retrieval granularity are not merely implementation details.
    A short indexed unit may represent one claim precisely but lose wider context.
    A long unit preserves more context but asks one representation to combine several topics and claims.
    Overlapping chunks reduce boundary problems but create duplication.
    Passage retrieval may suit factoid question answering or retrieval-augmented generation, whereas article-level retrieval may be preferable when relevance depends on study design, population, methods and findings spread across a paper.
    Systems that retrieve chunks but display source documents must also decide how to aggregate several chunk scores from one source.
    These choices can affect rankings and the apparent diversity of the results.
