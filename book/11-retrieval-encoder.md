---
key: "retrieval-encoder"
kind: "chapter"
eyebrow: "Chapter 6"
meta: "About 8 min"
question: "How does a language model's internal representation become something a search index can use?"
---

## From language model to retrieval encoder {#retrieval-encoder}

::: {.stage-map on="first-stage"}
:::

::: chapter-orient
Chapter 5 ended with a contextual language model and two unanswered retrieval questions: what should one vector represent, and what training makes nearby vectors useful for search?
This chapter follows those decisions from model tokens through pooling, separate query and document encoding, similarity, and retrieval-oriented examples.

The `delulu` example remains a teaching case, not evidence that a pretrained model already understands the query.
Its point is to make the desired ranking explicit.
Positive pairs and hard negatives provide examples of the distinction we want the model to learn.
Training aims to give the passage about unrealistic expectations a higher score for this query than the superficially similar alternative.
:::

::: {#how-dense-models-receive-text .legacy-anchor}
:::

### Model tokens are not indexed terms {#model-tokens-are-not-indexed-terms}

Classic Word2Vec uses a fixed word vocabulary, so an unseen complete word may map to an unknown token.[^lexical-oov] Modern encoders usually divide unfamiliar strings into reusable subwords, characters or bytes.
This improves coverage but does not imply understanding: a tokeniser can split a string even when the encoder has learnt little about its use. [Appendix B](#appendix-character-and-byte-tokenisation) gives the detailed worked example.

The word **token** is also used in lexical indexing, but the units perform different jobs:

::: {.table table-class="token-comparison"}
| Lexical index | Dense encoder |
|---|---|
| Analysis produces indexed terms such as `delulu` or `job`. | The model tokeniser produces vocabulary IDs for words, subwords, characters or bytes. |
| An indexed term can point directly to a [posting list](#from-analysed-tokens-to-a-term-first-map). | A model token is processed with surrounding tokens inside the encoder. |
| Exact overlap can provide transparent lexical evidence. | Token information contributes to a learnt representation and may not remain separately inspectable after pooling. |
| The collection determines which analysed terms have postings. | The pretrained model has a fixed input-token vocabulary or byte inventory. |

: Lexical index terms and dense model tokens are produced by different processes and are not interchangeable.
:::

For a conventional single-vector dense retriever, the path from text to one stored vector runs like this:

:::: {.figure .query-flow key="encoder-assembly-line"}
From text to one stored vector: what the encoder does in order

::: {.track}
- **Text** the query or passage as written
- **Model tokens** the tokeniser splits it into words, subwords, characters or bytes
- **Token IDs** each token is looked up in the model’s fixed input vocabulary
- **Token vectors** one initial embedding per token, before any context is read
:::

::: {.track}
- **Token vectors** where the first row stopped
- **In context** self-attention turns them into contextual token representations
- **Pooling** those representations are combined into one
- **One embedding** the single query or passage vector that is stored and compared
:::

::: caption
The second row picks up where the first stops.
Only the last box is stored and compared at search time; everything before it is working material inside the encoder.
Two boundaries matter for this chapter: model tokens enter at the second box and do not themselves become searchable index terms here, and pooling combines token representations into one vector, whereas [late-interaction methods](#where-colbert-style-late-interaction-fits) retain multiple token vectors for comparison.
:::
::::

The model tokens are therefore inputs to the encoder.
They are not the dimensions of the final pooled vector, and they are not automatically searchable terms in [an inverted index](#how-boolean-search-uses-an-inverted-index).

A contextual encoder combines these input units and pools them into one representation for the complete query or passage.
The next section explains the training that makes distances between those representations useful for retrieval.

::: {#what-a-dense-bi-encoder-actually-learns .legacy-anchor}
:::

### How a contextual encoder becomes a retrieval encoder {#how-a-contextual-encoder-becomes-a-retrieval-encoder}

What an embedding captures depends partly on the task used to train it.
For retrieval, training should favour the query–document relationships the system needs to recognise.

A dense retriever commonly starts with a pretrained language model.
Producing one vector for a whole text requires a **pooling** step that combines the contextual token representations—commonly by averaging them, or by taking the representation computed at the sequence-opening position.
Pooling on its own is not enough.
Pretraining gives the model broad linguistic patterns, but a model that predicts masked or next tokens does not automatically arrange its pooled vectors well for search.
Two texts can sit close together for reasons that have nothing to do with one answering a search for the other.
Retrieval training changes the representation so that labelled relevant texts receive higher similarity scores than competing texts.[^retrieval-training]

Two influential examples make that transition concrete. **Sentence-BERT (SBERT)** adapted BERT so that independently encoded sentences could be compared efficiently. **Dense Passage Retrieval (DPR)** applied the bi-encoder approach directly to retrieval: a question encoder and a passage encoder are trained so that relevant passages score above competing passages.
Both approaches train independently encoded representations so that their similarity scores are useful for the intended task.

:::: {.figure key="pretraining-vs-retrieval-training"}
Pretraining gives language patterns; retrieval training teaches what should rank together

![Pretraining gives language patterns; retrieval training teaches what should rank together](images/06%20From%20language%20model%20to%20retrieval%20encoder/ChatGPT%20Image%20Jul%2026,%202026,%2009_34_01%20PM.png){width="1448" height="1086"}

::: caption
Pooling a pretrained model’s token representations is not enough; retrieval training shapes what ends up close together.
:::
::::

#### A worked training example {#a-worked-training-example}

Suppose the query is:

> Am I being delulu about getting this job?

Take the underlying need to be *help me judge whether my expectations are unrealistic*.
A training dataset might then label this passage as relevant:

> How to recognise unrealistic expectations during a job search

It might contrast that passage with an easy negative:

> A history of agricultural employment

and a hard negative:

> Ten signs that you performed well in your job interview

The hard negative shares the broad topic and several important words, but it does not address whether the searcher’s expectations are unrealistic.
Under a different reading of the need—someone gauging their chances from how the interview went—it might well be useful, so this example assigns the label for the stated information need.
Training encourages the model to score the labelled positive above both alternatives.
Different systems implement this intuition with objectives such as triplet loss or contrastive softmax, and the selection of negative examples materially affects what the model learns.[^triplet-loss][^contrastive-loss][^hard-negatives]

:::: {.figure key="positives-and-negatives"}
Retrieval training pulls labelled positives closer and pushes negatives away

![Retrieval training pulls labelled positives closer and pushes negatives away](images/06%20From%20language%20model%20to%20retrieval%20encoder/ChatGPT%20Image%20Jul%2026,%202026,%2009_33_50%20PM.png){width="1448" height="1086"}

::: caption
The hard negative shares the broad topic and much of the vocabulary but does not address the question asked.
Which examples are chosen as negatives materially affects what the model learns.
:::
::::

#### Where the training signal comes from {#where-the-training-signal-comes-from}

Where did those labels come from?
They might be based on human relevance judgements, clicked results, questions paired with answer passages, titles paired with abstracts, citations, automatically generated queries or neighbouring passages from the same document.

Those sources teach different ideas of relevance.
Clicks can reward popularity and ranking position.
Question–answer pairs favour answer-bearing passages.
Citations may teach scholarly relatedness rather than direct relevance.
Titles and abstracts may mainly teach topical similarity.

Training pairs are drawn from a particular literature, genre and style of question, and the model learns from the proxies available *there*.
A retriever trained on web question–answer pairs has learnt what a good answer to a general-knowledge question looks like.
That is not the same as what a useful paper looks like to a systematic reviewer, what a relevant record looks like to someone tracing a chemical compound, or what a good match looks like in a language or discipline barely present in the training data.
Changing the training examples can change which records the model ranks highly, even with the same architecture.

This can be exploited deliberately. [SPECTER](https://aclanthology.org/2020.acl-main.207/) trains document-level embeddings of papers on the citation graph, so that papers citing one another are pulled together—a definition of relatedness drawn from scholarly practice rather than from web behaviour.[^specter] However, a model that performs well on the benchmark it was tuned for may transfer poorly to a different collection, query population or retrieval task, which [Chapter 13’s discussion of out-of-distribution transfer](#out-of-distribution) examines.

Positive and negative labels record the task’s intended distinction; a negative example may still be useful for a different information need.[^training-labels]

#### What the embedding space ends up preserving {#what-the-space-ends-up-preserving}

A retrieval embedding therefore preserves the similarities and differences that its starting model, training pairs, negative examples, loss function and optimisation process taught it to preserve.
If exact identifiers rarely matter during training, it may blur them.
If negatives rarely contain contradictions or specialised senses, it may fail to preserve precisely those distinctions.

The training data and objective give a retrieval model an **operational model of relevance**: they influence which query–document relationships it scores highly.
Clicks, answer pairs, citations and other labels are proxies for a useful result, not direct observations of relevance itself.

:::: chapter-close
1. Contextual encoding and retrieval are separate things.
   A pretrained encoder supplies representations; retrieval training gives the model an operational model of relevance, influencing which query–document relationships receive high similarity scores.
2. Model tokenisation and index analysis are different processes producing different units.
   A model token is not an indexed term.

::: {.chapter-transition}
Chapter 7 puts such an encoder to work across a whole collection and shows why semantic search need not mean dense retrieval.
Chapter 8 asks what a stored *vector* represents, how it was produced and which document units were indexed.
:::
::::

::: self-check
One encoder is trained on citation-linked papers; another on question–answer pairs. Why might they rank the same collection differently?

:   Citation-linked pairs reward scholarly relatedness; question–answer pairs reward answer-bearing matches.
    The positives and negatives change which relationships receive high scores, even with the same encoder architecture.
    Test the fit to the intended task rather than treating the model family as a guarantee.

A retriever trained on web question–answer pairs is deployed over a chemistry collection and performs poorly. What should you investigate before attributing the failure to training?

:   Domain or task mismatch is a plausible hypothesis, not an established cause.
    Check coverage, searchable fields, query processing and candidate cut-offs, then compare performance across a local set of queries.
    The scenario identifies the retrieval-training data but does not say whether domain pretraining occurred.
    Neither training lever alone guarantees a fit to the target collection.

Why is a model token not an indexed term?

:   They are produced by different processes and do different jobs.
    An indexed term comes out of analysis and points straight at a posting list.
    A model token is a vocabulary ID fed into an encoder, combined with its neighbours and then pooled away — it has no posting list and is usually not separately inspectable in the final vector.
:::

[^lexical-oov]: Lexical search systems may also use word-level tokens, but an unseen term does not create the same fixed-vocabulary problem.
    When a new document is indexed, the engine can add the term to its dictionary and create or update its posting list, recording the document identifiers and often the term frequency and positions of its occurrences.
    A frozen Word2Vec model cannot add a new word merely by recording where it appears: it must learn a meaningful vector from the word’s distributional contexts, usually through retraining or vocabulary extension.

[^retrieval-training]: Language-model pretraining and retrieval training have different objectives.
    A model trained to predict masked words or the next token learns broad linguistic and factual patterns, but its raw sentence or document representations may be poorly organised for nearest-neighbour search.
    Retrieval-oriented training changes the model so that specified positive text pairs receive higher similarity scores than negatives. [Sentence-BERT](https://aclanthology.org/D19-1410/) was motivated partly by ordinary BERT’s impracticality and weak performance for large-scale semantic-similarity search without architectural and training changes.

[^triplet-loss]: A simplified triplet-loss formulation is:

    $$
    L=\max\left(0,\;m+s(q,d^-)-s(q,d^+)\right),
    $$

    where $q$ is the query or anchor, $d^+$ is a positive passage, $d^-$ is a negative passage, $s$ is the similarity function and $m$ is the desired margin.
    The loss is zero when the positive is already more similar to the query than the negative by at least the margin.
    Otherwise, training changes the model to increase that separation.
    This equation illustrates the intuition; it is not the objective used by every embedding model.

[^contrastive-loss]: A common contrastive softmax objective for query $q_i$, its positive passage $d_i^+$ and a set of candidates can be written as:

    $$
    L_i=-\log\frac{\exp(s(q_i,d_i^+)/\tau)}{\sum_j\exp(s(q_i,d_j)/\tau)},
    $$

    where $s$ is the similarity score and $\tau$ is a temperature parameter controlling how sharply score differences affect the loss.
    The numerator rewards similarity with the positive; the denominator makes that positive compete against other candidates, which may include in-batch negatives.

[^hard-negatives]: Negative passages may be selected randomly, retrieved by BM25, retrieved by an earlier dense model or mined repeatedly as training proceeds.
    Hard negatives often provide stronger learning signals because they resemble relevant passages.
    They also increase the risk of **false negatives**: passages treated as irrelevant even though they could satisfy the query.
    Dense Passage Retrieval compared random and BM25-derived negatives and used in-batch negatives during training.

[^specter]: **SPECTER** produces one embedding per paper rather than per passage, and takes its training signal from the citation graph: papers that cite one another are treated as related and pulled together in the space, with harder negatives drawn from citations of citations.
    The resulting vectors are intended to be usable directly, without task-specific fine-tuning, for recommendation, classification and search over scholarly documents.
    It is a clear example of a relevance definition imported from scholarly practice rather than from click behaviour—and equally, of a definition that suits citation-like relatedness better than it suits a precise factual lookup.
    See Cohan et al., “[SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://aclanthology.org/2020.acl-main.207/),” ACL 2020.

[^training-labels]: A passage containing an answer may be positive for open-domain question answering but inadequate for a systematic review.
    A clicked result may reflect relevance, curiosity, position bias or an attractive title.
    Large-scale weak supervision makes embedding training possible without human judgement for every pair, but it also imports the assumptions and noise of the proxy signal into the resulting vector space.
