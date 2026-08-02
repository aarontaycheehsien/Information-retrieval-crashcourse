# The Tokeniser Knows Every Piece, but Search Is Still Cooked

## What Gen Z slang teaches librarians about Boolean search, lexical ranking and dense retrieval

Most librarians understand Boolean searching.

We know what happens when we add another concept with `AND`, introduce alternatives with `OR`, or remove an unwanted meaning with `NOT`. We also know, often through painful experience, that a poor synonym can flood a search with irrelevant records, while insisting on the wrong term can make relevant material disappear entirely.

What is less obvious is what happens after Boolean retrieval — or what happens when a search product no longer asks us to write Boolean at all.

When relevance sorting is used, an academic database may rank eligible records using TF-IDF, BM25 or a proprietary mixture of lexical, field, date, citation and behavioural signals. Newer products increasingly advertise natural-language, semantic or AI-assisted discovery. [Web of Science Smart Search](https://clarivate.com/academia-government/blog/smart-search-designing-search-for-todays-scholars/), for example, combines vector and Boolean search. [Scopus with AI](https://www.elsevier.com/products/scopus/scopus-ai) accepts natural-language questions and uses a Copilot query tool to select vector search, keyword search or both before synthesising an answer from retrieved abstracts.

Those product labels are useful descriptions of the interface. They are not complete descriptions of the retrieval architecture.

Web of Science Smart Search retrieves and ranks documents. Scopus with AI generates a referenced response over retrieved records. One is primarily a search experience; the other combines retrieval with generation. Filing both under “AI search” hides more than it reveals.

The natural question for librarians is:

> What do embeddings do better than Boolean searching, and what do they do worse?

For most library search discussions, three approaches do most of the explanatory work:

1. **Strict Boolean retrieval**, where terms act as hard admission or exclusion rules.
2. **BM25 or similar lexical ranking**, where matching terms act as weighted clues.
3. **Single-vector dense retrieval**, usually implemented with a bi-encoder, where each indexed text unit is compressed into one learnt dense vector.

Two additional names—**learnt sparse retrieval** and **late interaction**—are useful to recognise because vendors or technical papers may mention them. They complicate the keyword-versus-vector story, but they are not the centre of this article.

The word **vector** does not by itself separate lexical ranking from semantic retrieval. BM25 can be represented using sparse vectors, while a conventional dense bi-encoder produces one dense vector for each indexed unit.

Nor is “vector” synonymous with “semantic”.

To see why, let us ask what each method preserves, what it learns and how it fails when the query contains a word such as `delulu`.

## Boolean search: words as admission rules

Consider the query:

> delulu AND job

A Boolean system requires a record to satisfy both conditions, subject to the database’s tokenisation, stemming, field searching, phrase handling and indexing rules.

Boolean operators create hard decisions:

- `AND` requires conditions to occur together.
- `OR` allows alternatives.
- `NOT` excludes records.

Boolean logic does not by itself decide which eligible record is most relevant. It decides whether a record satisfies the query.

Many database searches can therefore be understood, with some simplification, as two stages. First, the Boolean expression determines which records are eligible. If relevance sorting is then selected, the system orders those records using BM25 or another ranking function.

![Two stages of search: Boolean eligibility followed by relevance ranking](images/01%20Boolean%20search%20-%20words%20as%20admission%20rules/ChatGPT%20Image%20Jul%2026,%202026,%2009_49_01%20PM.png)

> Boolean decides who gets into the competition. Ranking decides who finishes first.

This distinction matters when query expansion goes wrong.

Suppose an LLM expands `delulu` into:

> delulu OR unrealistic OR irrational OR foolish

If `foolish` is a poor alternative, records containing it may enter the result set. Ranking may push them down, but Boolean has already admitted them.

![A poor synonym expansion changes which records can enter](images/01%20Boolean%20search%20-%20words%20as%20admission%20rules/ChatGPT%20Image%20Jul%2026,%202026,%2009_49_10%20PM.png)

The reverse error is more serious. If a relevant record fails a compulsory `AND` condition, ranking cannot rescue it. It never enters the competition.

This is why LLM-generated synonyms require particular care in formal Boolean strategies. A weak suggestion is not merely given a low weight. It changes which documents can be returned.

## BM25: words as weighted clues

BM25 is also a lexical method. It normally depends on the query and document sharing indexed terms. Unlike strict Boolean, however, BM25 uses those matches to calculate a graded score. Its origins lie in the probabilistic relevance framework, although a BM25 score should not normally be read as a calibrated probability that a document is relevant.[^bm25-probability]

In simplified form, it adds a contribution for each matching query term. That contribution depends mainly on:

- **Term frequency:** repeated occurrences can provide more evidence that the document concerns the term.
- **Inverse document frequency:** a term found in relatively few documents usually contributes more than one found almost everywhere.[^bm25-idf]
- **Term-frequency saturation:** repetitions continue to add evidence, but by progressively smaller amounts.
- **Document-length normalisation:** five occurrences in a short abstract may be stronger evidence than five occurrences in a very long document.

![The four main BM25 scoring ingredients](images/02%20BM25%20-%20words%20as%20weighted%20clues/ChatGPT%20Image%20Jul%2026,%202026,%2009_32_47%20PM.png)

Seeing `delulu` twice may be more informative than seeing it once. Seeing it 100 times does not make a document 100 times more relevant. BM25 builds this diminishing return into its standard scoring function ([Robertson and Zaragoza, 2009](https://doi.org/10.1561/1500000019)).

BM25 can rank records that were first admitted by a Boolean expression, but it can also be used directly for retrieval. Given the query:

> delulu job interview expectations

a BM25 system can treat the terms as weighted evidence and retrieve the highest-scoring documents without requiring every one of them to appear.

This makes it less brittle than strict Boolean, but not wise. BM25 does not know that `foolish` may be a poor substitute for `delulu`. If `foolish` is rare in the collection, its inverse-document-frequency weight could make it surprisingly influential.

![Rare query terms contribute stronger lexical evidence through IDF](images/02%20BM25%20-%20words%20as%20weighted%20clues/ChatGPT%20Image%20Jul%2026,%202026,%2009_33_13%20PM.png)

Term-frequency saturation does not identify weak query terms either. It limits the benefit of repeating a term within a document. It does not decide whether the term belonged in the query. Some BM25 formulations also give repeated query terms additional, saturating weight, although many contemporary implementations omit that factor.[^bm25-query-frequency]

BM25 is not semantic understanding. It is lexical evidence made less binary.

## A vector does not have to be dense or semantic

Imagine a collection vocabulary containing 50,000 terms. Each term can be treated as a dimension. A document about Gen Z job-search anxiety might have non-zero weights for `delulu`, `job`, `interview` and a few other terms. The remaining dimensions would be zero.

That is a **sparse vector**: extremely long in principle, but with relatively few active dimensions.

BM25 can be represented this way. The query activates dimensions corresponding to its terms; the document contains calculated weights for terms occurring in it; and their score can be expressed as a dot product between sparse representations.[^bm25-sparse-vector] In practice, BM25 is usually executed with an inverted index rather than a product marketed as a vector database.

Dense embeddings look different. They may have hundreds or thousands of dimensions, most of them non-zero. Those dimensions do not normally correspond directly to recognisable words such as `delulu`, `job` or `unrealistic`. Meaning and other learnt distinctions are distributed across the representation.

The terms **sparse** and **dense** therefore describe the shape of a representation. They do not tell us whether it is neural, learnt, semantic or interpretable.

![Sparse and dense vectors compared](images/03%20A%20vector%20does%20not%20have%20to%20be%20dense%20or%20semantic/ChatGPT%20Image%20Jul%2026,%202026,%2009_35_31%20PM.png)

| Method | Representation | How its weights arise | What its dimensions represent |
| --- | --- | --- | --- |
| Boolean | Not primarily graded vector ranking | Searcher-specified conditions | Indexed terms and logical conditions |
| BM25 | One sparse representation per indexed unit | Collection statistics and a scoring formula | Vocabulary terms |
| Dense bi-encoder | One dense vector per indexed unit | Neural training | Distributed latent features |

![Density and learning are separate axes of a representation](images/03%20A%20vector%20does%20not%20have%20to%20be%20dense%20or%20semantic/ChatGPT%20Image%20Jul%2026,%202026,%2009_35_47%20PM.png)

This article uses **embedding** for a learnt mapping into a vector space. BM25 is better described as a calculated sparse representation or scoring model; a dense bi-encoder produces learnt dense embeddings.[^embedding-terms]

## What a dense bi-encoder actually learns

It is tempting to say that dense embeddings represent “meaning”. That is useful shorthand, but it leaves out the most important question: meaning for what task?

A dense retriever commonly starts with a pretrained language model. Pretraining gives it broad linguistic patterns, but a model that predicts masked or next words does not automatically arrange its vectors well for search. Retrieval training changes the representation so that labelled relevant texts receive higher similarity scores than competing texts.[^retrieval-training]

![Pretraining gives language patterns; retrieval training teaches what should rank together](images/04%20What%20a%20dense%20bi-encoder%20actually%20learns/ChatGPT%20Image%20Jul%2026,%202026,%2009_34_01%20PM.png)

Suppose the query is:

> Am I being delulu about getting this job?

A training dataset might label this passage as relevant:

> How to recognise unrealistic expectations during a job search

It might contrast that passage with an easy negative:

> A history of agricultural employment

and a hard negative:

> Ten signs that you performed well in your job interview

The hard negative shares the broad topic and several important words, but it does not address whether the searcher’s expectations are unrealistic. Training encourages the model to score the labelled positive above both alternatives. Different systems implement this intuition with objectives such as triplet loss or contrastive softmax, and the selection of negative examples materially affects what the model learns.[^triplet-loss][^contrastive-loss][^hard-negatives]

![Retrieval training pulls labelled positives closer and pushes negatives away](images/04%20What%20a%20dense%20bi-encoder%20actually%20learns/ChatGPT%20Image%20Jul%2026,%202026,%2009_33_50%20PM.png)

Where did those labels come from? They might be based on human relevance judgements, clicked results, questions paired with answer passages, titles paired with abstracts, citations, automatically generated queries or neighbouring passages from the same document.

Those sources teach different ideas of relevance. Clicks can reward popularity and ranking position. Question–answer pairs favour answer-bearing passages. Citations may teach scholarly relatedness rather than direct relevance. Titles and abstracts may mainly teach topical similarity.

“Positive” and “negative” are training labels, not universal truths.[^training-labels]

A retrieval embedding therefore preserves the similarities and differences that its starting model, training pairs, negative examples, loss function and optimisation process taught it to preserve. If exact identifiers rarely matter during training, it may blur them. If negatives rarely contain contradictions or specialised senses, it may fail to preserve precisely those distinctions.

Every retrieval embedding space contains a theory of relevance, whether its users know what that theory is or not.

## One document, one chunk and one vector are not the same thing

Before looking more closely at dense retrieval, we need to stop using **document** as though it meant only one thing.

A source document might be an article, paper, report, webpage or book. The retrieval system may index its abstract, sections, paragraphs, sentences or overlapping token windows. Those are the **indexed units**.

A 20-page article might therefore produce one indexed abstract, ten section units or 50 overlapping passages. In a conventional dense bi-encoder, each of those indexed units receives one pooled vector.

![The same article indexed using different chunking strategies](images/05%20One%20document,%20one%20chunk%20and%20one%20vector%20are%20not%20the%20same%20thing/ChatGPT%20Image%20Jul%2026,%202026,%2009_41_43%20PM.png)

These are separate choices:

- **Source-document granularity:** the object a person thinks of as the document.
- **Indexed-unit granularity:** the text unit the system searches.
- **Representation granularity:** how each indexed unit is encoded.
- **Result aggregation:** whether matching passages are displayed separately or combined into one article-level result.

Chunking a paper into 50 passages creates 50 searchable units and, with a conventional bi-encoder, 50 independently searchable vectors. It does not mean that the complete paper has been captured faithfully in one vector, nor that evidence spread across different chunks will automatically be combined.

![A paper split into many searchable chunks and vectors](images/05%20One%20document,%20one%20chunk%20and%20one%20vector%20are%20not%20the%20same%20thing/ChatGPT%20Image%20Jul%2026,%202026,%2009_41_26%20PM.png)

For librarians evaluating semantic search, the immediate questions are therefore more practical than architectural: what text was embedded, how large was each unit, and how are several matching passages turned back into an article-level result?[^chunking]

## Single-vector dense retrieval: compress first, compare later

A conventional dense bi-encoder uses a query encoder and a document or passage encoder. They may share weights or use distinct parameter sets, while normally being trained jointly on the retrieval objective.[^bi-encoder]

Each indexed unit is encoded without seeing the query. Its vector can therefore be calculated in advance and stored. At search time, the system encodes the query and looks for nearby indexed vectors, usually with a dot product or cosine similarity and an approximate nearest-neighbour index.[^vector-similarity]

![The bi-encoder retrieval pipeline: encode independently, then compare vectors](images/06%20Single-vector%20dense%20retrieval%20-%20compress%20first,%20compare%20later/ChatGPT%20Image%20Jul%2026,%202026,%2009_42_53%20PM.png)

This makes large-scale retrieval efficient. It also creates an information bottleneck.

Each indexed passage must compress its topic, named entities, claims, qualifications and terminology into one point before it knows which query will arrive. Shorter chunks reduce that pressure, but each chunk is still represented by one pooled vector.

![The compression bottleneck in single-vector dense retrieval](images/06%20Single-vector%20dense%20retrieval%20-%20compress%20first,%20compare%20later/ChatGPT%20Image%20Jul%2026,%202026,%2009_44_01%20PM.png)

The advantage is vocabulary bridging. A suitably trained model may place:

> Am I being delulu about getting this job?

near:

> How to recognise unrealistic expectations during a job search

even though the important expressions do not overlap lexically.

![Dense retrieval can bridge different phrasings without lexical overlap](images/06%20Single-vector%20dense%20retrieval%20-%20compress%20first,%20compare%20later/ChatGPT%20Image%20Jul%2026,%202026,%2009_44_11%20PM.png)

The danger is that broad similarity may dominate a small but decisive detail. A model can recover the general meaning while blurring an exact code, a rare name, a negation or the difference between a question and its opposite.

### For awareness: two neural variants

The three-part comparison above is enough for most library discussions, but two additional terms may appear in technical documentation.

**Learnt sparse retrieval**, represented by systems such as [SPLADE](https://doi.org/10.1145/3404835.3463098), uses neural training to assign weights and predict useful expansions while retaining a sparse, vocabulary-aligned representation suitable for an inverted index.[^splade-mechanics] It can be understood as a learnt bridge between lexical matching and semantic expansion. It can also be more interpretable than a pooled dense embedding: its active dimensions are labelled with vocabulary terms, so an analyst can inspect which original or expanded terms received weight. That visibility does not make every expansion correct or explain the model’s complete decision process.[^splade-limitations]

![SPLADE learns a sparse, vocabulary-aligned expansion](images/06%20Single-vector%20dense%20retrieval%20-%20compress%20first,%20compare%20later/ChatGPT%20Image%20Jul%2026,%202026,%2009_44_49%20PM.png)

**Late-interaction retrieval**, represented by systems such as [ColBERT](https://doi.org/10.1145/3397271.3401075), retains several contextualised token vectors for each indexed unit instead of compressing everything into one pooled vector. This can preserve finer local evidence, but requires more storage and computation.[^colbert-maxsim] It can be more interpretable at the scoring layer because the score can be decomposed into the strongest document-token match for each query token. An analyst can inspect which token alignments contributed. The underlying vector dimensions remain latent, however, so ColBERT is not transparent end to end.

![ColBERT preserves local token-level matching evidence](images/06%20Single-vector%20dense%20retrieval%20-%20compress%20first,%20compare%20later/ChatGPT%20Image%20Jul%2026,%202026,%2009_45_04%20PM.png)

Both SPLADE and ColBERT remain dependent on model vocabulary and training data. The reason to know their names is simply to avoid a category error: neural retrieval is not always single-vector and semantic expansion is not always dense. Unless a library is developing or technically auditing a retrieval stack, their implementation details are unlikely to matter.

## Rerankers: compare more carefully after retrieval

A reranker usually does not search the complete collection. A fast first-stage retriever—perhaps BM25, a dense bi-encoder, ColBERT or a hybrid combination—first produces a shortlist. The reranker then spends more computation deciding how those candidates should be ordered.

This division of labour matters. First-stage retrieval is normally designed to balance speed with recall: get a manageable set containing as many relevant documents as possible. Reranking is more concerned with precision near the top: distinguish the best candidates from plausible but weaker ones. A reranker cannot rescue a relevant document that never entered the shortlist.

![Retrieve broadly, then rerank a shortlist more carefully](images/07%20Rerankers%20-%20compare%20more%20carefully%20after%20retrieval/ChatGPT%20Image%20Jul%2026,%202026,%2009_45_42%20PM.png)

### Cross-encoder reranking

A **bi-encoder** encodes the query and candidate independently. Document or passage vectors can therefore be calculated in advance, and search reduces to comparing the query vector with stored vectors. That is what makes large-scale dense retrieval practical. The cost is that the query and document do not interact until after each has already been compressed into its representation.

A **cross-encoder** does the opposite. It places the query and one candidate into the model together, typically as a single input sequence, and allows attention across all their tokens before producing a relevance score. The model can therefore examine whether a particular query term aligns with a particular passage, whether a qualifier changes the claim, or whether two otherwise similar texts differ in negation, entity or intent. This architecture became prominent in retrieval through BERT passage reranking ([Nogueira and Cho, 2019](https://arxiv.org/abs/1901.04085)).

The price is computation. The candidate representation cannot simply be precomputed and reused because its encoding depends on the query. Reranking 100 candidates requires roughly 100 query–candidate model evaluations. This is usually affordable for a shortlist, but not for millions of records. Cross-encoder scores also reflect their training data, text truncation and definition of relevance; joint attention makes finer comparison possible, not infallible.

![Bi-encoders precompute independent vectors; cross-encoders compare query and candidate together](images/07%20Rerankers%20-%20compare%20more%20carefully%20after%20retrieval/ChatGPT%20Image%20Jul%2026,%202026,%2009_45_53%20PM.png)

### Where ColBERT-style late interaction fits

ColBERT sits between the pooled bi-encoder and the full cross-encoder. Like a bi-encoder, it encodes the query and document independently, so document token vectors can be prepared before the query arrives. Unlike a conventional bi-encoder, it does not reduce each indexed unit to one vector. Its late-interaction score compares query-token vectors with document-token vectors after encoding.

This preserves more local matching evidence than a single pooled vector without paying the full cost of jointly encoding every query–document pair. ColBERT-style models can be used for first-stage retrieval or to rerank a shortlist, depending on the implementation and scale. They require more storage and computation than single-vector retrieval, but normally less query-time work than a cross-encoder over the same candidates.

![Where ColBERT-style late interaction sits between bi-encoders and cross-encoders](images/07%20Rerankers%20-%20compare%20more%20carefully%20after%20retrieval/ChatGPT%20Image%20Jul%2026,%202026,%2009_47_23%20PM.png)

### LLMs as rerankers

A general-purpose or specially trained large language model can also act as a reranker. Instead of merely comparing embeddings, it receives the query, candidate text and sometimes explicit relevance instructions. This makes it possible to ask the model to consider criteria such as population, method, date, study design or whether a passage actually answers the question rather than merely sharing its topic.

LLM reranking is commonly framed in three ways:

- **Pointwise:** judge or score each candidate independently. This scales linearly with the shortlist, but the scores may require calibration and the model does not directly compare candidates.
- **Pairwise:** compare two candidates and choose which is more relevant. Direct comparison can help with subtle distinctions, but many comparisons may be needed and preferences can be inconsistent.
- **Listwise:** present several candidates together and ask the model to return an ordering. This gives the model comparative context, but long lists exceed context limits, so systems often use sliding windows or repeated partial rankings. Input order can influence the result.

![Pointwise, pairwise, and listwise LLM reranking](images/07%20Rerankers%20-%20compare%20more%20carefully%20after%20retrieval/ChatGPT%20Image%20Jul%2026,%202026,%2009_46_17%20PM.png)

These are not merely prompting details. They create different costs and failure modes. Research has demonstrated both listwise and pairwise LLM reranking, including zero-shot listwise reranking ([Ma et al., 2023](https://arxiv.org/abs/2305.02156)) and pairwise ranking prompting ([Qin et al., 2024](https://aclanthology.org/2024.findings-naacl.97/)).

LLM rerankers can use richer instructions and longer textual context than many conventional rankers, but they are usually slower and more expensive. They may also be sensitive to prompt wording, candidate order, context-window limits, model updates and sampling settings. A generated explanation can make a decision easier to inspect, but a plausible explanation is not evidence that the ranking is correct.

The practical questions are therefore: what produced the shortlist, how many candidates reached the reranker, what text and metadata the reranker saw, which ranking formulation it used, and how the complete pipeline was evaluated.

> A sophisticated reranker can reorder only what the retriever allowed it to see.

## Three different ways vocabulary can go wrong

Discussions of semantic search often muddle three separate problems:

1. **Vocabulary mismatch:** the query and relevant document express the same idea differently.
2. **Vocabulary or representation gaps:** an important string is absent, fragmented or poorly represented somewhere in the system.
3. **Domain shift:** the model has learnt the wrong sense, register or definition of relevance.

They produce different failure modes and favour different remedies.

### 1. Vocabulary mismatch

Suppose the query says:

> Am I being delulu about getting this job?

while the relevant document says:

> How to recognise unrealistic expectations during a job search

Nothing needs to be unknown. Every term may be familiar to the system. The searcher and author have simply chosen different words.

Strict Boolean does not automatically connect `delulu` with `unrealistic expectations`. The searcher must supply alternatives, use a controlled vocabulary, rely on automatic expansion or hope that both formulations occur somewhere in the record.

BM25 has the same underlying limitation. It can score shared terms such as `job` and `search`, but `delulu` does not lexically match `unrealistic`.

A suitably trained dense bi-encoder offers a different bridge: it can place the complete query and document formulations near one another even when their important words do not overlap.

The same problem appears when a query says `this song slaps` and a review says `listeners found the track extremely enjoyable`, or when `improve my rizz` must retrieve advice about confidence and charm while flirting.

This problem is older than neural retrieval. [Furnas and colleagues](https://doi.org/10.1145/32206.32212) demonstrated in 1987 that people often choose different words for the same objects and operations. Librarians have long responded with controlled vocabularies, synonym expansion, citation searching, pearl growing and iterative searching.

Learned retrieval offers additional bridges. It does not invent the vocabulary problem.

### 2. Which vocabulary is “out”?

Now suppose someone searches for `delulu`, but the term does not occur anywhere in the indexed collection. For Boolean and BM25, the consequence is straightforward: the term supplies no lexical match. Other words in a longer query may still retrieve records, but `delulu` itself contributes no evidence.

Once dense retrieval is involved, at least two vocabularies matter:

1. **The collection vocabulary:** strings occurring in the indexed documents.
2. **The tokenizer vocabulary:** words or subword pieces the model can process directly.

A term can be absent from the collection but representable by the tokenizer. It can be tokenisable but poorly understood. It can appear exactly in the collection while being split awkwardly by the model’s tokenizer.

Modern tokenizers often divide unfamiliar strings into reusable subword or character-level pieces. This softens the boundary between known and unknown words. It does not erase it.

`rizzlord` is partly compositional. A model that knows something about `rizz` and `lord`, especially in an informative sentence, may infer a plausible meaning. But a model can process every character in `iykyk`, `frfr` or `skibidi` without knowing how the expression is being used.

> Tokenising a term is not the same as understanding it.

The reverse case is equally important. Suppose an identifier called `DELULU-427` appears in three indexed documents and exact identity matters.

If the query and documents are analysed consistently, a lexical system can match the surface form directly. A keyword field might preserve the complete string; an ordinary text field might split it into `delulu` and `427`. BM25 can give rare matching components substantial weight without ever having encountered the identifier during model training.

A standard single-vector dense retriever can encode the string, but may blur it with related strings or concepts. Research on salient-phrase-aware dense retrieval documents this weakness while also showing that better training can mitigate it ([Chen et al., 2022](https://aclanthology.org/2022.findings-emnlp.19/)).

This is why a lexical path remains important for gene and protein identifiers, chemical strings, dataset titles, model names, article identifiers, product codes, personal names and newly coined terminology.

The lesson is not that dense retrieval always fails on identifiers. It is that omitting exact lexical matching creates avoidable risk when exact identity determines relevance.

### 3. Out of domain

Learned retrieval gains power by importing linguistic and relevance patterns from training. It can also import the wrong ones.

Imagine a retriever trained mainly on encyclopaedias, news and conventional question-answering data. We apply it to Gen Z social-media posts and ask:

> Which person is cooked?

The collection contains:

> Jay cooked dinner for everyone.

> Jay failed every module and lost his internship. Bro is cooked.

Every word is familiar. Both passages contain a lexical match. The problem is that `cooked` has different senses.

A model trained mainly on formal prose may associate the word more strongly with food preparation than with being doomed. The scholarly equivalent is a general model encountering `consideration` in contract law, `expression` in molecular biology, `bias` in statistics or `depression` in economics.

Domain does not mean only subject. It can also mean genre, register, community, document type, query style or definition of relevance.

BM25 has a peculiar kind of robustness here because it understands nothing. It does not know which sense of `cooked` is intended, so it cannot disambiguate correctly. But it also cannot import an elaborate, inappropriate interpretation learnt from another dataset. Its principal statistics are calculated from the target collection.

This advantage is limited. BM25 still depends on analysers, fields, parameters and query formulation, and it cannot bridge `delulu` with `unrealistic expectations`. It is specifically less exposed to **learnt semantic domain shift**.

Changing the neural architecture does not remove this problem. Any learnt retriever can carry assumptions from its training data into a new setting.

[BEIR](https://arxiv.org/abs/2104.08663) found BM25 to be a robust zero-shot baseline, while some more computationally expensive neural and reranking approaches performed better on average. That is not a law that BM25 always transfers well or dense retrieval always transfers badly. Broadly trained, adapted and specially designed retrievers can behave very differently.

The safer conclusion is:

> A learnt retriever may transfer its theory of relevance badly.

> BM25 transfers less theory, but therefore has less learnt theory to transfer incorrectly.

## When every word is familiar and search still gets it wrong

Sometimes the problem is neither a missing term nor a specialised domain. Every word is ordinary, but the expression means something else as a whole.

Consider:

> Touch grass.

A tokenizer can represent `touch` and `grass` perfectly. Their ordinary meanings do not produce `spend less time online and reconnect with ordinary life`.

Basic unigram BM25 has an earlier problem: it treats the words as separate terms. A document saying `touch the button; the garden is covered in grass` may receive evidence for both even though the phrase never appears. Phrase operators, positional indexes, proximity scoring or n-grams can address adjacency, but recognising the phrase still does not explain its non-literal meaning.

The same applies to `she is mother`, `it’s giving librarian` and `bet, I’ll be there`. Subword tokenisation offers little special help because the pieces are already familiar.

A learnt system may know the construction from training and retrieve a formal paraphrase. It may also be confidently wrong.

Broad semantic similarity can itself become a trap. Compare:

> That story is cap.

> No cap, that story is true.

The sentences share a topic, register and much of their vocabulary, but their conclusions are opposite. A single pooled vector may place them close together because most of their features are similar.

This is not proof that embeddings are mathematically incapable of negation. Models trained with suitable contradiction and hard-negative examples can improve, although current dense retrievers still show marked weaknesses on Boolean logic ([Zhang et al., 2024](https://aclanthology.org/2024.findings-emnlp.156/)). It shows that broad semantic similarity and retrieval relevance are not identical. Sometimes one small difference must outweigh everything else two texts share.

Strict Boolean can express that difference only when the searcher anticipates it. BM25 will probably retrieve both because they overlap lexically. No approach guarantees that the feature most important to the searcher will dominate.

## Comparing the three main approaches

| Method | What it preserves best | Characteristic strength | Characteristic blind spot |
| --- | --- | --- | --- |
| Strict Boolean | Explicit terms and logic | Reproducible inclusion and exclusion | A weak `AND`, `OR` or `NOT` changes the eligible set completely |
| BM25 | Exact lexical evidence and rare matching terms | Strong first-stage ranking when wording overlaps | Weak vocabulary bridging and no inherent phrase meaning |
| Single-vector dense retrieval | Overall learnt similarity | Compact, efficient paraphrase retrieval | Pooling may blur exact identity or decisive local details |

These methods describe first-stage retrieval components, not mutually exclusive products. A reranker is not a fourth row in the table because it usually operates after one or more of these methods have produced candidates. A real system may combine them, add phrase features, rewrite the query, apply field boosts, incorporate controlled vocabulary and rerank a shortlist with a cross-encoder, a ColBERT-style model or an LLM.

That is why asking whether a product “uses vectors” tells us very little.

## Why hybrid retrieval remains attractive

The cleanest summary is more complicated than keywords versus semantics:

> A lexical system may preserve the word and miss the meaning.

> A single-vector dense system may recover the meaning and blur the exact word.

Hybrid retrieval protects against systems with different and partly complementary blind spots.

Boolean can provide explicit control. BM25 can preserve exact lexical evidence. Dense retrieval can bridge different formulations in a compact latent space. Rerankers and less common neural architectures may add further signals, but the main reason for combining lexical and dense retrieval is already clear: each can recover relevant material the other may miss.

The combination method matters too. A system may merge ranked lists with reciprocal rank fusion, combine normalised scores, use different retrievers for different query types, or run a cheap first stage and rerank only the leading candidates.

“Hybrid” is therefore not one architecture or a guarantee of quality. It is a design space.

## What to ask when choosing a search tool

Most librarians will never train a retriever. They will license one, or license a database containing one. The distinctions above become procurement and evaluation questions.

When a product advertises semantic, natural-language or AI search, ask:

1. **Which retrieval and ranking components are used?** Is there Boolean retrieval, BM25-like lexical ranking, dense retrieval or reranking? If there is a reranker, is it a cross-encoder, ColBERT-style model or LLM, how many candidates does it see, and does the system select components by query or always combine them?

2. **Is exact lexical matching retained?** Can users search identifiers, chemical strings, gene names, dataset titles and quoted phrases without semantic expansion quietly changing the task?

3. **What is the indexed unit?** Is the system retrieving titles, abstracts, passages, sections or complete articles? A product searching abstracts cannot retrieve evidence that occurs only in the full text, however sophisticated its vectors are.

4. **How are passage results assembled?** If five chunks from the same paper match, are their scores combined, is only the best retained, or are five near-duplicate results shown?

5. **What trained the relevance model?** Web queries, question–answer pairs, citation links and scholarly relevance judgements teach different behaviours. How was the model adapted to the disciplines and document types being searched?

6. **How are exactness, negation and exclusions tested?** Ask for examples involving identifiers, contradictory claims, `NOT`-like intent and near-duplicate names — not only attractive paraphrase demonstrations.

7. **How is the hybrid combined?** A product may call itself hybrid because it contains two retrievers even when one signal rarely affects the final ranking. Ask whether users can inspect, compare or control the component result sets.

8. **How is performance evaluated?** Average benchmark scores can hide failures on the query types that matter locally. A serious evaluation should include the institution’s disciplines, vocabulary, languages and known difficult searches.

None of these questions requires reading a loss function. All of them distinguish a retrieval design from a marketing label.

The tokeniser may recognise every piece of the query. The source article may be divided into sensible chunks. Each chunk may receive a dense vector, while a separate lexical system indexes its words. The final results may blend both signals.

That still does not mean the retrieval system has any rizz.

---

[^bm25-probability]: Calling BM25 a **probabilistic relevance model** does not mean that its final score is a calibrated probability of relevance. Its origins lie in the Probability Ranking Principle: documents should be ranked in decreasing order of their estimated probability of relevance to the information need. The earlier Binary Independence Model used binary term-presence features and derived query-term weights from the odds that a term occurred in relevant rather than non-relevant documents. When relevance judgements were unavailable, collection statistics produced the Robertson–Spärck Jones form of inverse document frequency. BM25 extended this framework with graded document term frequency, saturation and length normalisation. It is best understood as a practical ranking function derived from a probabilistic theory, not a model that directly outputs reliable relevance probabilities.

[^bm25-idf]: There is no universal BM25 inverse-document-frequency formula. A classic Robertson–Spärck Jones form, when relevance judgements are unavailable, is:

    $$
    \log\left(\frac{N-df+0.5}{df+0.5}\right)
    $$

    where $N$ is the number of documents and $df$ is the number containing the term. This value becomes negative when a term occurs in more than half the collection. Implementations respond differently. [Apache Lucene](https://lucene.apache.org/core/8_1_1/core/org/apache/lucene/search/similarities/BM25Similarity.html), for example, uses:

    $$
    \log\left(1+\frac{N-df+0.5}{df+0.5}\right),
    $$

    which remains positive. Other implementations use different smoothing, flooring or IDF variants. Two systems described as using BM25 can therefore produce different rankings even before differences in tokenisation, fields, $k_1$ or $b$ are considered.

[^bm25-query-frequency]: A fuller BM25 formulation can include a query term-frequency factor:

    $$
    \frac{(k_3+1)qtf}{k_3+qtf},
    $$

    where $qtf$ is the number of times the term occurs in the query. Like $k_1$, $k_3$ creates saturation: repeating a query term can increase its weight, but the increase eventually tails off. In practice, $k_3$ is rarely exposed to users, and many contemporary implementations omit this factor or effectively treat each distinct query term once. This usually matters little for short queries, but may matter more for verbose or automatically generated queries containing repeated terms.

[^bm25-sparse-vector]: A simplified sparse-vector decomposition of BM25 can be written as:

    $$
    \operatorname{score}(q,d)=\sum_{t\in V}w_q(t)w_d(t),
    $$

    where $V$ is the vocabulary. The query weight is zero for terms absent from the query. The document weight is zero for terms absent from the document and otherwise stores the relevant BM25 contribution, including inverse document frequency, term-frequency saturation and length normalisation. Depending on the variant, query term-frequency weighting may be placed in $w_q(t)$. This formulation is asymmetric in spirit because query-side and document-side weights play different roles; it should not be confused with cosine similarity between symmetrically weighted TF-IDF vectors. Calling BM25 a sparse vector representation does not make it a learnt embedding model.

[^embedding-terms]: **Embedding** is used inconsistently. In a broad mathematical sense, any mapping into a vector space may be called an embedding. In machine learning, the word usually implies a learnt representation. This article therefore uses **BM25 sparse vector representation** for calculated lexical weights, **learnt sparse representation** for systems such as SPLADE, **single-vector dense embedding** for pooled learnt vectors, and **multi-vector dense representation** for late-interaction systems such as ColBERT.

[^retrieval-training]: Language-model pretraining and retrieval training have different objectives. A model trained to predict masked words or the next token learns broad linguistic and factual patterns, but its raw sentence or document representations may be poorly organised for nearest-neighbour search. Retrieval-oriented training changes the model so that specified positive text pairs receive higher similarity scores than negatives. [Sentence-BERT](https://aclanthology.org/D19-1410/) was motivated partly by ordinary BERT’s impracticality and weak performance for large-scale semantic-similarity search without architectural and training changes.

[^chunking]: Chunking and retrieval granularity are not merely implementation details. A short indexed unit may represent one claim precisely but lose wider context. A long unit preserves more context but asks one representation to combine several topics and claims. Overlapping chunks reduce boundary problems but create duplication. Passage retrieval may suit factoid question answering or retrieval-augmented generation, whereas article-level retrieval may be preferable when relevance depends on study design, population, methods and findings spread across a paper. Systems that retrieve chunks but display source documents must also decide how to aggregate several chunk scores from one source. These choices can affect rankings and the apparent diversity of the results.

[^bi-encoder]: A dual encoder, also called a bi-encoder, encodes the query and each indexed text unit independently. The encoders may share all, some or none of their parameters. Independent encoding allows document or passage vectors to be precomputed, making first-stage retrieval efficient. A conventional single-vector bi-encoder produces one pooled vector per indexed unit. A late-interaction model retains several independently encoded token vectors. A cross-encoder instead processes the query and candidate text together, permitting detailed token interactions but normally at substantially greater computational cost.

[^triplet-loss]: A simplified triplet-loss formulation is:

    $$
    L=\max\left(0,\;m+s(q,d^-)-s(q,d^+)\right),
    $$

    where $q$ is the query or anchor, $d^+$ is a positive passage, $d^-$ is a negative passage, $s$ is the similarity function and $m$ is the desired margin. The loss is zero when the positive is already more similar to the query than the negative by at least the margin. Otherwise, training changes the model to increase that separation. This equation illustrates the intuition; it is not the objective used by every embedding model.

[^contrastive-loss]: A common contrastive softmax objective for query $q_i$, its positive passage $d_i^+$ and a set of candidates can be written as:

    $$
    L_i=-\log\frac{\exp(s(q_i,d_i^+)/\tau)}{\sum_j\exp(s(q_i,d_j)/\tau)},
    $$

    where $s$ is the similarity score and $\tau$ is a temperature parameter controlling how sharply score differences affect the loss. The numerator rewards similarity with the positive; the denominator makes that positive compete against other candidates, which may include in-batch negatives.

[^hard-negatives]: Negative passages may be selected randomly, retrieved by BM25, retrieved by an earlier dense model or mined repeatedly as training proceeds. Hard negatives often provide stronger learning signals because they resemble relevant passages. They also increase the risk of **false negatives**: passages treated as irrelevant even though they could satisfy the query. Dense Passage Retrieval compared random and BM25-derived negatives and used in-batch negatives during training.

[^vector-similarity]: Dense retrieval commonly compares vectors using a dot product or cosine similarity:

    $$
    \operatorname{cos}(q,d)=\frac{q\cdot d}{\lVert q\rVert\lVert d\rVert}.
    $$

    If every vector is normalised to unit length, ranking by cosine similarity is equivalent to ranking by dot product. Without normalisation, vector magnitude can also influence a dot-product score. The similarity function is part of the training setup: the model learns a geometry suited to the score on which it is optimised.

[^training-labels]: A passage containing an answer may be positive for open-domain question answering but inadequate for a systematic review. A clicked result may reflect relevance, curiosity, position bias or an attractive title. Large-scale weak supervision makes embedding training possible without human judgement for every pair, but it also imports the assumptions and noise of the proxy signal into the resulting vector space.

[^colbert-maxsim]: A simplified ColBERT late-interaction score is:

    $$
    \operatorname{score}(q,d)=\sum_{i\in q}\max_{j\in d}q_i\cdot d_j.
    $$

    Each query-token vector $q_i$ is compared with the document-token vectors $d_j$. For each query token, the strongest document-token similarity is retained, and these maxima are summed. This **MaxSim** decomposition is what makes the contributing token alignments inspectable. Because document-token vectors are computed without seeing the query, they can be indexed in advance. Practical implementations use approximation, compression and pruning rather than exhaustively comparing every stored token vector. ColBERTv2 uses residual compression, while [PLAID](https://arxiv.org/abs/2205.09707) uses centroid-based pruning to reduce search cost.

[^splade-mechanics]: SPLADE uses a transformer’s masked-language-modelling output vocabulary to produce vocabulary-aligned weights. Pooling combines token-level predictions into one sparse representation for the query or indexed unit. A transformation such as $\log(1+\operatorname{ReLU}(x))$ provides a saturation effect, while explicit regularisation encourages most vocabulary dimensions to remain inactive. The architecture and regularisation changed across SPLADE versions, but the central design remains learnt weighting and expansion in a sparse lexical space suitable for inverted-index retrieval.

[^splade-limitations]: Vocabulary-aligned dimensions make SPLADE’s terms and expansions inspectable, but learnt sparse models remain constrained by their output vocabularies. Rare names and identifiers may be divided into fragments that do not preserve an entity cleanly. The [DyVo study](https://aclanthology.org/2024.emnlp-main.45/) proposed dynamic entity vocabularies specifically to address that problem. Sparsity also does not remove domain shift: changes in vocabulary and word frequencies can degrade learnt expansions and weights, and low-frequency terms from the training data can remain difficult.

## References

Chen, X., Lakhotia, K., Oğuz, B., Gupta, A., Lewis, P., Peshterliev, S., Mehdad, Y., Gupta, S., and Yih, W. (2022). “[Salient phrase aware dense retrieval: Can a dense retriever imitate a sparse one?](https://aclanthology.org/2022.findings-emnlp.19/)” *Findings of EMNLP 2022*, 250–262.

Clarivate. (2025). “[Smart Search: Designing search for today’s scholars](https://clarivate.com/academia-government/blog/smart-search-designing-search-for-todays-scholars/).”

Elsevier. (n.d.). “[Scopus with AI](https://www.elsevier.com/products/scopus/scopus-ai).”

Formal, T., Piwowarski, B., and Clinchant, S. (2021). “[SPLADE: Sparse lexical and expansion model for first-stage ranking](https://doi.org/10.1145/3404835.3463098).” *Proceedings of SIGIR 2021*, 2288–2292.

Furnas, G. W., Landauer, T. K., Gomez, L. M., and Dumais, S. T. (1987). “[The vocabulary problem in human-system communication](https://doi.org/10.1145/32206.32212).” *Communications of the ACM, 30*(11), 964–971.

Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., and Yih, W. (2020). “[Dense passage retrieval for open-domain question answering](https://aclanthology.org/2020.emnlp-main.550/).” *Proceedings of EMNLP 2020*, 6769–6781.

Khattab, O., and Zaharia, M. (2020). “[ColBERT: Efficient and effective passage search via contextualized late interaction over BERT](https://doi.org/10.1145/3397271.3401075).” *Proceedings of SIGIR 2020*, 39–48.

Ma, X., Zhang, X., Pradeep, R., and Lin, J. (2023). “[Zero-shot listwise document reranking with a large language model](https://arxiv.org/abs/2305.02156).” *arXiv preprint arXiv:2305.02156*.

Nogueira, R., and Cho, K. (2019). “[Passage re-ranking with BERT](https://arxiv.org/abs/1901.04085).” *arXiv preprint arXiv:1901.04085*.

Qin, Z., Jagerman, R., Hui, K., Zhuang, H., Wu, J., Yan, L., Shen, J., Liu, T., Liu, J., Metzler, D., and Bendersky, M. (2024). “[Large language models are effective text rankers with pairwise ranking prompting](https://aclanthology.org/2024.findings-naacl.97/).” *Findings of NAACL 2024*, 1504–1518.

Reimers, N., and Gurevych, I. (2019). “[Sentence-BERT: Sentence embeddings using Siamese BERT-networks](https://aclanthology.org/D19-1410/).” *Proceedings of EMNLP-IJCNLP 2019*, 3982–3992.

Robertson, S., and Zaragoza, H. (2009). “[The probabilistic relevance framework: BM25 and beyond](https://doi.org/10.1561/1500000019).” *Foundations and Trends in Information Retrieval, 3*(4), 333–389.

Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., and Gurevych, I. (2021). “[BEIR: A heterogeneous benchmark for zero-shot evaluation of information retrieval models](https://arxiv.org/abs/2104.08663).” *NeurIPS 2021 Datasets and Benchmarks Track*.

Zhang, Z., Zhu, J., Zhou, W., Qi, X., Zhang, P., and Li, H. (2024). “[BoolQuestions: Does dense retrieval understand Boolean logic in language?](https://aclanthology.org/2024.findings-emnlp.156/).” *Findings of EMNLP 2024*, 2767–2779.
