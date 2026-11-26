---
kind: "glossary"
nav: "target"
---

Complete glossary of terms

For the overlapping labels used in research papers and product descriptions, see [Appendix D: A librarian’s map of search terminology](#appendix-search-terminology).

Agentic RAG
:   RAG in which a model chooses or sequences retrieval actions from the task and what it finds while working towards a generated response.
    A narrower case of agentic search; a fixed multi-step RAG workflow is not agentic RAG.

Agentic search
:   Search in which a model plans at least part of a multi-action retrieval sequence from the task and observations, using the tools its harness permits.
    A model selecting only among branches enumerated in advance is adaptive under this book’s convention; multiple steps or model involvement alone do not establish agency.

AI-powered search
:   A claim that some machine-learnt component is present somewhere in the product.
    It identifies no representation, no matching method and no stage, and remains compatible with a system whose retrieval is entirely lexical, which is what makes it the least informative label of this group.

Analysis
:   The full pipeline turning raw text into searchable terms: tokenisation, lowercasing, stop-word removal, stemming and similar steps.

ANN (approximate nearest neighbour)
:   An index reducing vector comparisons by searching only part of the collection, at the risk of missing a true nearest neighbour.

API (application programming interface)
:   A published contract by which one program offers a service to another, written for a developer to build against.

Best-match retrieval
:   Retrieval using graded scores to rank candidates by estimated relevance, allowing partial query matches.
    Also called partial-match retrieval in traditional IR terminology.
    It can be lexical and coexist with Boolean filters; PubMed’s Best Match is a particular product label.

Bi-encoder
:   A model encoding query and document separately, so document vectors can be computed in advance.

Blending / routing
:   Two ways to run more than one retrieval path.
    A blend runs prescribed paths on every query and combines them; a route decides per query which path or paths run.
    The difference shows up when you try to explain one result: with a route, “was this lexical or vector?” can have a different answer each time.

BM25
:   The long-standing default ranking function for lexical retrieval.
    It scores a document from how often a query term occurs in it, how rare the term is in the collection, and how long the document is.

Candidate set / candidate boundary
:   The records available to the next stage of a search pipeline, and the boundary that fixed them.
    Within a fixed candidate set, reranking and generation can reorder but cannot add; only another retrieval route or round can.

Chunk
:   An indexed unit produced by splitting a longer source document.

Cognitive relevance (pertinence)
:   Whether an item is informative to this reader given what they already know.

Context window
:   The limit on how much material a model can work with, measured in tokens.
    Instructions, conversation, tool results and supplied evidence consume part of the budget; room must remain for the response.
    Fitting material into it does not establish that every passage will be used reliably.

Controlled vocabulary
:   A curated set of preferred labels assigned to records and used in searching, so the query addresses an annotation layer rather than relying only on words found in the text.

Cosine similarity
:   A vector comparison based on directional alignment.
    It ignores vector magnitude and ranges mathematically from −1 for opposite directions through 0 for perpendicular vectors to 1 for the same direction.

Cross-encoder
:   A model reading query and candidate together, allowing finer comparison at much greater cost.

Dense retrieval
:   Retrieval comparing learnt dense vector representations, which can match texts sharing no words.

df (document frequency)
:   How many documents in the collection contain a term.

Dictionary
:   The list of searchable terms in an inverted index; each entry points to a posting list.

Distributional hypothesis
:   The claim that words appearing in similar contexts tend to be used in similar ways.
    It supplies the training target that makes a learnt word embedding possible: ask a model to predict a word’s neighbours, and the text itself provides the answers without human labelling.

Dot product
:   A vector comparison that multiplies corresponding coordinates and adds the results.
    It reflects direction and, unless vectors are normalised, magnitude; it can be negative and has no fixed range.
    For unit-length vectors it equals cosine similarity.

Embedding
:   A learnt mapping into a vector space and, by common shorthand, the vector produced by that mapping.

Embedding search
:   Vector search where the vectors are embeddings, meaning learnt mappings rather than counts.
    Narrower than vector search and usually a synonym for dense retrieval in product copy, though it still leaves open which stage performs the comparison.

Exact-match retrieval
:   Retrieval based on whether a record satisfies the complete query specification, as in the Boolean model.
    This need not mean literal string matching or containing every named term.
    Boolean admission alone supplies no relevance ranking.

Generation
:   Producing model output, such as prose.
    RAG conditions that output on retrieved evidence, but generation can also use supplied material without a retrieval step.
    Generation is separate from retrieval and is not this book’s main subject.

Grep / ripgrep
:   Tools for searching text for literal strings or regular-expression patterns, normally returning matching lines without relevance scores.
    Ordinary grep and ripgrep scan without a persistent content index; a product’s grep-like interface may use an index.

Hard negative
:   A training example that shares a query’s topic and much of its vocabulary without answering it.
    Contrasting a labelled positive against hard rather than obvious negatives is what teaches a retriever the distinctions it will need, so the choice of negatives materially shapes what the model learns.

Harness
:   The limits an agent works inside: which tools it may call, which sources it can reach, how many rounds it gets and when it must stop.

Hybrid / multi-stage
:   Hybrid combines candidates or scores from multiple candidate-generation routes.
    Multi-stage means later operations process candidates supplied by an earlier stage.
    A BM25 shortlist followed by a cross-encoder is multi-stage, not necessarily hybrid; vendor usage of “hybrid” is inconsistent.

IDF (inverse document frequency)
:   A weight derived from df, giving rarer terms more influence.

Indexed unit
:   The unit represented in an index for matching, such as an abstract, section or passage.
    It need not be a whole document, and may differ from the text later supplied as context.
    Direct file scanning does not require indexed units.

Information need
:   What the person is actually trying to know or accomplish.
    A system never observes it; it observes a query or other representation standing in for it.

Inverted index
:   A map running from each term to the documents containing it, instead of from documents to their words.

*k*~1~ and *b*
:   The two main BM25 tuning parameters, controlling term-frequency saturation and document-length normalisation.

Late interaction
:   An arrangement keeping one vector per token rather than one per passage, and comparing query-token vectors with document-token vectors after each side has been encoded separately.
    It preserves more local matching evidence than a pooled bi-encoder without jointly encoding every pair, at a large cost in storage.
    ColBERT is the standard example.

Latent dimension
:   A coordinate of a learnt representation that carries no name of its own.
    A lexical vector’s dimensions stand for stated vocabulary terms; a dense embedding’s are settled during training, and what any single one contributes is spread across the representation rather than readable from that coordinate alone.

Learning to rank (LTR)
:   Supervised machine learning that learns a ranking function from examples, often by combining several query, document and query–document signals.

Learnt sparse retrieval
:   Retrieval over representations that are sparse and vocabulary-aligned as BM25’s are, but whose coordinates come from the model’s own vocabulary and whose every weight is predicted by a trained model.
    Because the prediction ranges over the whole vocabulary, weight can fall on a term the text never contained.
    SPLADE is this book’s example.

Lexical retrieval
:   Retrieval drawing matching evidence from words or character sequences, either by direct string/pattern matching or by matching analysed terms through an index.
    A pipeline may combine lexical retrieval with meaning-aware query expansion, dense retrieval or reranking.

Masked language modelling
:   A self-supervised objective that hides tokens anywhere in a sequence and asks the model to recover each from the words on both sides.
    It is what allows an encoder such as BERT to read in both directions.

MCP (Model Context Protocol)
:   A convention for describing a service so a model can read the description while working and decide whether to call it.
    A description layer over an interface, not a retrieval method and not a way past a subscription.

MRR, MAP, nDCG
:   Rank-aware measures rewarding, respectively, an early first hit, many relevant records placed high, and highly relevant records placed high on a graded scale.

Neural information retrieval
:   An umbrella category for the use of neural networks in retrieval or ranking.
    It includes dense retrieval, learnt sparse retrieval, late interaction and neural reranking, so the label identifies neither one representation nor one pipeline stage.

Neural search
:   A product-facing label for retrieval that uses a neural network somewhere.
    It names neither a representation nor a stage: the neural component may generate candidates, rerank a lexical shortlist or only rewrite the query.
    Neural information retrieval describes the same territory as a technical category.

Next-token prediction
:   A self-supervised objective that hides everything after a position and asks the model to produce the next token from what came before.
    It is the objective behind GPT-style models, and the reason they read left to right.

Normalisation (vector)
:   Rescaling a vector to length one without changing its direction.
    Comparisons between unit-length vectors cannot respond to magnitude, which is why cosine similarity and dot product then return identical scores and the same ranking.
    Distinct from BM25’s document-length normalisation, which adjusts term-frequency evidence for how long a document is.

OOD (out of distribution)
:   In neural IR, a broad label for applying a learnt system where deployment differs from the distributions or retrieval conditions represented during training.
    The shift may involve queries or corpora and, in some IR work, the retrieval task or relevance pattern.

OOV (out of vocabulary)
:   Absent from a specified vocabulary.
    The label is incomplete unless it names the vocabulary: for example, an index dictionary or a model tokeniser’s vocabulary.

Pooling (encoder)
:   The step that combines an encoder’s contextual token representations into one vector for a whole query or passage—commonly by averaging them, or by taking the representation computed at the sequence-opening position.
    It is what makes a single-vector embedding out of a sequence, and what discards the local detail late interaction keeps.
    Distinct from pooling in test collections, which is a way of choosing what to judge.

Pooling (test collections)
:   Judging only the records that several systems ranked highly and treating the rest as irrelevant, which is how large test collections stay affordable.

Posting / posting list
:   One entry recording that a term occurs in a document, and the ordered list of all such entries for that term.

Precision
:   The proportion of retrieved records that were judged relevant.

Precision@k
:   Precision calculated over the first k results only, rather than the whole result set.

Pretraining
:   The first and largest stage of training a language model, in which it learns general patterns of language from a broad corpus rather than anything about a particular task.

Query by example / seed-based retrieval
:   Retrieval that starts from a known document and finds related records through text similarity, citation relations or both, rather than starting from a typed topic query.

Query transformation
:   Changing or creating the input a retrieval pass actually receives: correcting, mapping to controlled terms, expanding, decomposing, rewriting into Boolean, or generating alternative formulations.
    It changes the retrieval input and may change the candidate set.
    Understanding can instead inform a routing decision without rewriting the input.

Query understanding
:   Interpreting a request—recognising phrases, entities, dates, languages, document types, intent or proposed constraints.
    Interpretation may inform a later step without changing anything the retriever receives.

RAG (retrieval-augmented generation)
:   Retrieve external material and supply selected evidence to a model generating an answer.
    This book uses the broad pipeline sense, which can include file/pattern search and does not require embeddings.
    Source support must still be checked; the arrangement alone does not guarantee it.

RAG Fusion
:   A RAG pipeline that generates several variants of the user’s query, retrieves for each, merges the ranked lists with reciprocal rank fusion and generates from the merged top results.
    A composition of existing retrieval techniques, not a new retrieval method.

Ranked retrieval
:   A broad form of retrieval in which candidates receive graded scores and are ordered from higher to lower scoring.
    The label does not specify how those scores were calculated.

Recall
:   The proportion of all judged-relevant records that were retrieved.
    Within a fixed candidate set, reranking and generation cannot recover excluded records.
    Additional retrieval routes or rounds can expand the cumulative candidate set and increase recall.

Regular expression
:   A pattern specifying character sequences to match, such as alternatives or word boundaries.
    It expresses text conditions rather than automatically supplying synonyms or understanding a passage.

Relevance
:   A relationship among an item, a represented need, a person and a situation—not a property stored inside a document.
    Term overlap, similarity and reranker scores are evidence about it, never the thing itself.

Relevance judgement
:   A recorded decision that a particular record does or does not satisfy the relevance criteria for a represented information need.
    Retrieval metrics compare systems against these operational judgements rather than objective truth.

Representation
:   Any form a system uses to stand for an item.
    It is the broadest of three nested terms: representation, vector and embedding.

Reranker
:   A later, more expensive stage reordering a shortlist that an earlier retriever produced.

Result diversification
:   Ranking or selecting a set so that each additional result contributes useful novelty or aspect coverage as well as individual relevance.
    It is an objective applied to a result set, not a dense or neural retrieval method.

Retrieval
:   Finding records, files or passages for an information need.
    Retrieval may return an unranked set or matching lines; ranked retrieval also orders candidates by score.

Retrieval control
:   Deciding where retrieval inputs go—which path or paths run, whether several run in parallel, and whether another search happens at all.
    Routing is a control decision, not a transformation, and not by itself evidence of agency.

Retrieval feedback
:   A later retrieval pass constructed from records judged relevant or non-relevant after an initial search.
    It can add candidates by changing what is retrieved.
    Pseudo-relevance feedback makes the unverified assumption that highly ranked records are relevant.

RRF (reciprocal rank fusion)
:   A rule for merging several ranked lists using result positions rather than their raw scores.
    The lists may come from different retrievers or from several queries run through the same one.

Screening feedback
:   Judgements used to reprioritise records inside an existing candidate pool, as in active-learning screening.
    It changes what is screened next but does not inherently add candidates.

Self-supervised learning
:   Training in which the data supplies its own targets, so no human labelling is needed.
    Hiding part of a text and scoring a model on recovering it is the example used throughout this book.

Semantic search
:   An intended capability or goal—matching by meaning rather than only literal words—usually contrasted with lexical retrieval, but not a particular retrieval method.
    Today it is commonly implemented using dense retrieval over embeddings, while ontology or query expansion, learnt-sparse retrieval, neural reranking and hybrid combinations may also contribute.
    A lexical retriever may still supply the candidates.

Situational relevance (usefulness)
:   Whether an item helps this person accomplish this task under this task’s constraints and criteria.

Sparse vector / dense vector
:   A description of a representation’s shape—few active dimensions versus mostly non-zero ones—not of whether it was learnt.

System or algorithmic relevance
:   How strongly a retrieval system estimates that an item fits the representation it was given.
    A system can also estimate topical or task-specific suitability, but no estimate is the reader’s judgement.

Term
:   What a token becomes after analysis, and what a lexical index actually stores and matches.

Test collection
:   A fixed set of documents, topics and relevance judgements, which is what makes two systems comparable at all.

tf (term frequency)
:   How often a term occurs within one document.

TF-IDF
:   An earlier family of lexical weighting schemes, multiplying term frequency by inverse document frequency.
    BM25 weighs the same two signals, with saturation and length normalisation added, and has largely replaced TF-IDF for ranked retrieval—though it was not derived from the TF-IDF formula.

Token
:   A unit of text produced by splitting a string—often a word, but possibly punctuation or part of a word.

Tool (agent sense)
:   One operation a model has been given permission to invoke, such as running a search or fetching a record’s references—not a product a library licenses.

top-*k*
:   A request for the *k* highest-scoring results rather than a complete ordering.
    A result boundary, not a retrieval method.

Topical relevance
:   Whether an item is about the subject being sought, independently of who is asking.

Vector
:   A numerical representation consisting of an ordered list of numbers.

Vector search
:   Retrieval that compares vector representations, usually by nearest-neighbour search.
    The label describes the comparison rather than the representation—the vectors may be learnt and dense, or sparse and vocabulary-aligned—so it does not by itself imply matching by meaning.

Vocabulary mismatch
:   A query and a relevant document express the same or a sufficiently related concept using different lexical forms.
