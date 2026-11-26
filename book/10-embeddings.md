---
key: "embeddings"
kind: "chapter"
eyebrow: "Chapter 5"
meta: "About 15 min"
question: "How does a model learn to place related texts near one another?"
legacy_anchors: ["ch4", "dense-retrieval"]
---

## Embeddings: what the learnt geometry encodes {#embeddings}

::: {.stage-map on="first-stage"}
:::

::: chapter-orient
The lexical methods so far match words or character sequences.
An indexed term matcher needs overlap between analysed query and document terms; grep needs text that satisfies its literal string or pattern.
Without a match under the chosen rule, or a reformulation that creates one, these methods have no direct lexical evidence connecting the query and document.
Dense retrieval attacks that limitation directly: instead of matching terms, it converts text into a vector of numbers and compares positions in a space where proximity encodes the query–document relationships that training taught the model to reward.

Before any of that can be searched, something has to produce the vectors.
The chapter introduces word vectors, shows how representations can depend on context, and explains how training shapes those representations.
:::

::: {.orientation label="Before you start"}
#### The steepest chapter, and what to carry out of it {#chapter-5-orientation-title}

Part I stayed with visible text: strings and patterns, terms in an index, and rules about which records they admit.
This is where the book stops being only about words, and it introduces more new vocabulary than any other chapter.

**The later chapters rely on three ideas:**

1. An encoder *computes* an embedding using a mapping learnt during training.
   BM25 uses a specified formula and collection statistics.
   The difference is how the mapping is obtained, not whether the output is calculated.
2. What a model places near what is shaped by **training**, not by meaning.
   Two texts can sit close together for reasons that have nothing to do with one answering a search for the other.
3. The units a model reads are not the terms an index stores.
   They look alike and they are produced by different processes.

The Word2Vec prediction examples and the comparison of masked and next-token prediction explain how training works.
The king\ −\ man\ +\ woman example illustrates relationships found in learnt vectors.
Later chapters do not require you to reproduce these calculations or training details. [Appendix A](#appendix-transformer-halves) builds on the contrast between masked and next-token prediction for readers who want more.

The payoff is in [Chapter 7](#dense-at-scale), which shows how such an encoder is used to search a whole collection.
If you want to see what all this is *for* before working through how it is built, read that chapter’s opening first and come back.
:::

::: {.orientation tag="div"}
**Start with the output.** An encoder takes a query such as `delulu job expectations` and produces a list of numbers.
It can encode a passage about unrealistic job expectations into another list of the same length.
A comparison rule scores the two vectors.
The numbers are computed; training determines which relationships their geometry tends to preserve.
Chapter 6 opens that computation and Chapter 7 uses it for retrieval.
:::

### From Word2Vec to retrieval embeddings {#from-word2vec-to-retrieval-embeddings}

Before comparing kinds of vectors, it helps to separate three related terms.
A **representation** is any form a system uses to stand for an item.
In this chapter, the representations of interest are usually **vectors**: ordered lists of numbers.
In a simple diagram, two numbers could give an object horizontal and vertical coordinates.
Machine-learning vectors usually have hundreds or thousands of dimensions, so we cannot draw them directly, but the same idea remains.

An **embedding** is a mapping that places an item—such as a word, query or passage—into a vector space.
In modern NLP, that mapping is usually learnt from data during model training.
By common shorthand, the resulting vector is also called an embedding.
Items placed near one another are treated as similar according to whatever patterns the model learnt.

::: {.common-confusion label="Key distinction" label-class="key-distinction-label" label-id="distinction-embedding-vector"}
#### Representation, vector and embedding {#representation-vector-embedding-title}

In this book, an embedding maps an item to a vector, and a vector is one form of representation.
Other representations are possible, and **a vector need not come from a learnt embedding**. [BM25](#bm25-words-as-weighted-clues) weights can be written as a sparse vector without being an embedding, because they are calculated from term frequencies, document lengths and collection statistics rather than learnt during model training.
In informal product language, **embedding search** usually means comparing vectors produced by learnt mappings; **vector embedding search** is largely redundant because embeddings already inhabit vector spaces. [Chapter 8](#a-vector-does-not-have-to-be-dense-or-semantic) returns to why that distinction matters.
:::

A learnt mapping is still a calculation: with the same model, preprocessing and inference settings, an encoder’s output can be reproduced.
Understanding what each of its dimensions represents is a separate, harder question.

```{=html}
<figure aria-labelledby="calculated-weights-and-learnt-parameters-title">
<p class="figure-title" id="calculated-weights-and-learnt-parameters-title">Where the numbers come from</p>
<div class="orientation"><p><strong>BM25:</strong> term counts + document lengths + collection statistics → specified weighting formula → term scores.</p><p><strong>Neural encoder:</strong> text + tokenisation + learnt model parameters → encoder computation and pooling → embedding vector.</p><p><strong>Training:</strong> examples + targets → compare predictions with targets → adjust model parameters. The trained mapping is then used to compute new outputs.</p></div>
<figcaption><span class="asset-label-inline" id="fig-5-1">Figure 5.1</span> Both routes calculate outputs. BM25 specifies the weighting rule explicitly; a neural encoder uses a mapping fitted during training. A reproducible output need not have easily interpretable dimensions.</figcaption>
</figure>
```

#### Text that supplies its own targets {#text-that-supplies-its-own-targets}

Training, though, is not a matter of instructing a network to learn meaning.
It works by comparing what the model currently produces against what it was supposed to produce, then adjusting the parameters to make the gap smaller.
That requires a target for every example, and nobody has labelled the meaning of every word in English.
What prediction target can we obtain from the text itself?

The answer comes from linguistics rather than from machine learning.
Firth’s formulation is the one usually quoted—“You shall know a word by the company it keeps”—and the claim beneath it, the **distributional hypothesis**, is that words appearing in similar contexts tend to be used in similar ways.
Harris had argued much the same in 1954.
Rather than asking a model what a word means, ask it to predict which words occur around it.
The text already contains the answers, so no human labelling is required.

:::: {.figure key="distributional-hypothesis-training-signal"}
Text supplying its own training targets

![A five-part diagram. The first part quotes Firth, “You shall know a word by the company it keeps”, and notes Harris’s 1954 argument that words used in similar contexts tend to be used in similar ways. The second replaces the question of what the word heart means with the question of which words occur around it, noting that the corpus already contains the answers. The third shows two sentences in which heart and cancer appear in the same frame of surrounding words, with overlapping context circles. The fourth shows a context window over one sentence and the two prediction directions, context-to-centre and centre-to-context. The fifth notes that the model is never told explicit meanings and that the vectors are a by-product of reducing prediction error.](images/05%20Embeddings%20-%20what%20the%20learnt%20geometry%20encodes/distributional-hypothesis-training-signal.png){width="1448" height="1086"}

::: caption
Predicting a word from its context provides a training target available in the text itself, without manual labels. [Open the full-resolution figure.](images/05%20Embeddings%20-%20what%20the%20learnt%20geometry%20encodes/distributional-hypothesis-training-signal.png)
:::
::::

[Word2Vec](https://arxiv.org/abs/1301.3781) acts on that hypothesis directly.
It is trained on exactly that prediction task—recovering a word from the words surrounding it, or the surrounding words from the word—across a large corpus, and on nothing else.
Predicting context is not itself the point: the vectors are a *by-product*, kept once training ends and put to work elsewhere.
Earlier neural language models, recurrent ones among them, had thrown off word vectors the same incidental way while being trained to predict the next word. [The Illustrated Word2Vec](https://jalammar.github.io/illustrated-word2vec/) works through the mechanism step by step; what matters here is that the training target came out of the text itself.

:::: {.figure key="word2vec-predicting-context"}
The prediction task is the training; the vectors are what is kept

![A four-stage diagram. The first stage states the distributional hypothesis. The second shows a sliding context window of size two over the sentence “The patient received heart treatment after the attack”, with heart as the target word, and sets out the two training arrangements: CBOW, in which the context words predict the centre word, and Skip-gram, in which the centre word predicts the context words. The third shows the resulting embedding matrix as a table of words against short example vectors. The fourth shows the prediction head crossed out and discarded after training while the word vectors are kept, with heart, cancer and treatment clustered apart from job and interview in a two-dimensional plot.](images/05%20Embeddings%20-%20what%20the%20learnt%20geometry%20encodes/word2vec-predicting-context.png){width="1448" height="1086"}

::: caption
CBOW predicts a target word from its neighbours; Skip-gram predicts neighbouring words from a target word.
After training, the learnt word vectors can be reused without the prediction machinery. [The Illustrated Word2Vec](https://jalammar.github.io/illustrated-word2vec/) explains the prediction step in more detail. [Open the full-resolution figure.](images/05%20Embeddings%20-%20what%20the%20learnt%20geometry%20encodes/word2vec-predicting-context.png)
:::
::::

The individual dimensions of a Word2Vec vector are not normally labelled *occupation*, *emotion* or *age*.
The learnt pattern is distributed across many dimensions, most of whose values are non-zero.
That is why it is called a **dense word embedding**.

### What the learnt geometry appears to encode {#what-the-learnt-geometry-appears-to-encode}

What came out of that training was more than the expected result that words used alike end up near one another.
The positions carried regularities nobody had specified.
Words related to each other in a consistent way turned out to be separated by a consistent *direction*, so that arithmetic performed on the vectors tracked the relationship between the words.

The familiar demonstration is the one about royalty.
Take the vector for `king`, subtract `man`, add `woman`, and—excluding the three input words from the candidate answers—the vector nearest the result is `queen`.
Read geometrically, the step from `man` to `woman` and the step from `king` to `queen` are close to the same move through the space.
The behaviour was [first reported for vectors taken from a recurrent language model](https://aclanthology.org/N13-1090/), and the Word2Vec papers then [demonstrated it at much larger scale](https://arxiv.org/abs/1310.4546).

:::: {.figure key="word2vec-analogy-offsets"}
The same relationship as the same move through the space

![A schematic three-axis space holding four labelled points. A dashed arrow runs from man to woman, and a second dashed arrow of similar length and direction runs from king to queen. The two arrows are close to parallel, which presents the relationship as a repeated step through the space rather than as a property of any single point.](images/05%20Embeddings%20-%20what%20the%20learnt%20geometry%20encodes/word2vec-analogy-offsets.png){width="314" height="268"}

::: caption
If `king` minus `man` plus `woman` lands nearest `queen`, what the space holds is a direction that can be reused, not four unrelated positions.
The drawing is a schematic: the axes are anonymous, the positions are illustrative rather than plotted from a trained model, and a real word embedding has hundreds of dimensions that cannot be drawn at all. [Open the full-resolution figure.](images/05%20Embeddings%20-%20what%20the%20learnt%20geometry%20encodes/word2vec-analogy-offsets.png)
:::
::::

The regularity is not confined to one hand-picked pair.
Projecting the trained vectors for a set of countries and their capital cities down to two dimensions produces a set of roughly parallel country-to-capital arrows.
The model was given co-occurring words and nothing else; the relationship it appears to have picked up was not supplied as an explicit training label.

:::: {.figure key="word2vec-country-capital-pca"}
Countries and their capitals, projected down to two dimensions

![A scatter plot of Skip-gram vectors reduced to two principal components. Country names including China, Russia, Japan, Turkey, Poland, Germany, France, Italy, Greece, Spain and Portugal sit towards the left of the plot; their capitals, including Beijing, Moscow, Tokyo, Ankara, Warsaw, Berlin, Paris, Rome, Athens, Madrid and Lisbon, sit towards the right. A dashed arrow joins each country to its capital, and the arrows run roughly parallel to one another.](images/05%20Embeddings%20-%20what%20the%20learnt%20geometry%20encodes/word2vec-country-capital-pca.png){width="1480" height="1030"}

::: caption
The country-to-capital arrows point in much the same direction for every pair, although the model was never told what a capital city is.
Two cautions: this is a two-dimensional PCA projection of 1000-dimensional Skip-gram vectors, so the picture is a shadow of the space rather than the space itself, and the pairs shown were chosen for the demonstration.
Reproduced from Mikolov, Sutskever, Chen, Corrado and Dean, “[Distributed representations of words and phrases and their compositionality](https://arxiv.org/abs/1310.4546),” NIPS 2013, Figure 2. [Open the full-resolution figure.](images/05%20Embeddings%20-%20what%20the%20learnt%20geometry%20encodes/word2vec-country-capital-pca.png)
:::
::::

The model was optimised to predict co-occurring words; the relational structure is a consequence of having done that well, not something it was asked for and not something it can be relied upon to get right.[^analogy-caveat] Predicting word co-occurrence can produce vectors that capture useful relationships between words.
Whether those vectors support effective retrieval must be tested using queries and relevance judgements.

Word2Vec is only a stepping stone to modern dense retrieval.
Classic Word2Vec gives a word essentially the same stored vector wherever it appears and represents individual words rather than complete information needs.
Modern encoders can instead read a whole query or passage in context and be adapted, through pooling and task training, to produce one vector for that complete text unit.

### Context changes the representation {#context-changes-the-representation}

Consider `bank` in *the river bank* and in *the bank refused the loan*.
Classic Word2Vec holds one stored vector for that string, so both uses begin from the same location and nothing in the model separates them.
A **contextual encoder** instead computes a fresh representation for each occurrence from the sequence it appears in.
The two instances of `bank` receive different vectors because the words around them differ.

These context-dependent vectors are often called **contextual embeddings**.
More precisely, the encoder transforms its initial token embeddings into contextual token representations; obtaining one embedding for a complete query or passage requires a later pooling step.

The architecture that made this practical at scale is the [Transformer](https://arxiv.org/abs/1706.03762), whose **self-attention** mechanism allows each token’s representation to draw on the other tokens in the sequence instead of being fixed in advance. [ELMo](https://aclanthology.org/N18-1202/), published in 2018, produced contextual representations using stacked bidirectional recurrent networks.
Transformer-based encoders subsequently became dominant because self-attention made sequence processing more parallelisable and scalable for large-scale pretraining.[^elmo] [Appendix A](#appendix-the-transformer) sets out what self-attention does and why nearly every model named in this book is built from it.

### What the model was trained to predict {#what-the-model-was-trained-to-predict}

Self-attention lets a model combine information from tokens in a sequence.
The training objective specifies what it must predict, and helps determine which representations it learns.
Every encoder named in this chapter arrives already **pretrained**, and what it was pretrained to predict shapes the representations it produces long before any retrieval training is applied to them.

Word2Vec, BERT and the GPT family share one arrangement, and it is the arrangement [this chapter opened with](#from-word2vec-to-retrieval-embeddings): part of a text is hidden, and the model is scored on recovering what was hidden.
These objectives differ in what is predicted and which context is available.
In Word2Vec, CBOW predicts a word from surrounding words; Skip-gram predicts surrounding words from a target word. **Masked language modelling**, the objective BERT is pretrained with, hides tokens anywhere in the sequence and recovers each one from the words on both sides of it. **Next-token prediction**, the objective behind GPT-style models, hides everything to the right of a position and recovers the next token from the left alone.

In these pretraining examples, the text supplies its own targets: this is **self-supervised learning**.
Retrieval training also needs a training signal, but that signal need not be a human relevance label.
It may come from human judgements, behaviour, weak or synthetic labels, or self-supervised pairs.
The question to carry into [retrieval training](#how-a-contextual-encoder-becomes-a-retrieval-encoder) is what relationship those targets teach the model to preserve.

:::: {.figure key="shapes-of-the-blank"}
One training arrangement, three shapes of blank

::: {.include src="figures/shapes-of-the-blank.html"}
:::

::: caption
The same sentence, hidden three different ways.
How much the model may look at is the difference this diagram draws: the neighbours on either side, the rest of the sentence in both directions, or only what came before.
The Word2Vec row shows the CBOW arrangement; Skip-gram reverses the direction.
In none of the three does a person supply the answer—the hidden word is its own label.
:::
::::

Masked-token prediction can use context on both sides of a masked position.
Next-token prediction uses preceding context; exposing the next token would reveal the target.
For several years this difference largely separated two strands of Transformer research: bidirectional encoders became the usual starting point for retrieval models, and decoders for generation.
The division has since blurred, as [Appendix A](#appendix-transformer-halves) explains.

::: {#bert-is-a-model-not-a-retrieval-method .legacy-anchor}
:::

### What BERT is, and what it still needs {#what-bert-is-and-what-it-still-needs}

[BERT](https://aclanthology.org/N19-1423/) is a [Transformer](#appendix-the-transformer) encoder pretrained to learn general language patterns, chiefly by [masked language modelling](#what-the-model-was-trained-to-predict): predicting masked tokens from both sides of their context.[^not-all-bert] That produces a general-purpose language model, not a search system.

Turning a pretrained encoder into a classifier, named-entity recogniser or retriever requires task training on labelled examples.
Generic BERT is a poor retriever because masked-word prediction gives it no reason to place independently encoded questions near relevant passages.
Models such as [Sentence-BERT](https://aclanthology.org/D19-1410/) change the architecture and training for that purpose.

Domain pretraining is a separate lever.
BioBERT continues pretraining on biomedical literature,[^biobert] BiomedBERT starts from biomedical text and vocabulary,[^pubmedbert] and SciBERT does the same across scientific literature.[^scibert] This changes what the model knows, not what it should rank; each still needs retrieval-oriented training.

“Uses BERT” therefore leaves two decisive questions unanswered: **was it trained for retrieval**, and **where does it sit in the pipeline**?
The same family can interpret a query, produce first-stage vectors or compare a shortlist as a reranker.[^retrieval-chronology]

> A contextual representation incorporates the surrounding text.
> Further training adapts it to tasks such as comparing a query with a relevant passage.

:::: chapter-close
1. A dense retriever compares learnt representations rather than strings, which is what allows it to bridge paraphrase.
2. Context changes a token’s representation, but contextualisation alone does not decide what evidence retrieval should reward.
3. Pretraining supplies broad language patterns; domain pretraining changes the text and vocabulary behind those patterns; neither by itself creates a retriever.
4. A model name such as BERT therefore leaves both its task training and its place in the search pipeline unknown.

::: {.chapter-transition}
Chapter 6 asks what one vector should represent and what training makes nearby vectors useful for search.
:::
::::

::: self-check
BERT produces contextual representations. Why does that not make generic BERT a retriever?

:   Contextualisation lets a token representation depend on surrounding words, but masked-language pretraining does not teach independently encoded queries and passages to rank together.
    Retrieval needs an architecture and task training whose positives, negatives and labels reward the relationships the search should recover.

A vendor says its search “uses BERT”. Which two questions remain unanswered?

:   Ask how the model was trained for the retrieval task and where it sits in the pipeline.
    The same model family can interpret or transform a query, encode first-stage candidates, or compare an existing shortlist as a reranker.
:::

[^analogy-caveat]: The demonstration is real and reproducible, but it is normally reported with a step that is easy to miss: the nearest-neighbour search that returns `queen` excludes `king`, `man` and `woman` from the candidate set, and without that exclusion the vector closest to the computed point is frequently one of the three inputs.
    Levy and Goldberg, “[Linguistic regularities in sparse and explicit word representations](https://aclanthology.org/W14-1618/),” CoNLL 2014, show that the method’s apparent success also depends on how the component similarities are combined; Linzen, “[Issues in evaluating semantic spaces using word analogies](https://aclanthology.org/W16-2503/),” RepEval 2016, shows that several analogy categories are solved by plain proximity, with the offset contributing nothing; and Nissim, van Noord and van der Goot, “[Fair is better than sensational: Man is to doctor as woman is to doctor](https://aclanthology.org/2020.cl-2.7/),” *Computational Linguistics* 46(2), 2020, document how the convention has been used to produce sensational analogies that the vectors do not actually support.
    The regularity in the space is genuine; what it is not is evidence that the model has learnt relations as such.

[^elmo]: ELMo derived each token’s representation from a bidirectional recurrent language model rather than from self-attention.
    Its objective was next-word prediction run in both directions and the two halves combined, rather than the masked prediction BERT later used.
    It was normally used to supply features to a task-specific model instead of being fine-tuned wholesale.
    The idea that a word’s representation should depend on its sentence is therefore older than the Transformer; what changed afterwards was how cheaply and how deeply it could be done.

[^not-all-bert]: Not every current embedding model is BERT-based or bidirectional.
    Several widely used retrieval encoders are initialised from decoder-style models that read left to right, and others use Transformer encoders trained differently from BERT.
    BERT is used here because it is the clearest teaching example and the name librarians actually encounter in product documentation, not because it is the only or the current architecture. [Appendix A](#appendix-transformer-halves) traces the decoder strand and its next-token objective, and [Appendix D](#appendix-misleading-overlaps) gives current examples of embedding models built on decoder backbones.

[^biobert]: **BioBERT** is the continual-pretraining case.
    It is initialised from the general BERT-base weights and then pretrained further on PubMed abstracts (about 4.5 billion words) and PubMed Central full-text articles (about 13.5 billion words).
    It deliberately keeps BERT’s original WordPiece vocabulary, on the argument that unfamiliar biomedical words can be assembled from existing subword pieces.
    See Lee et al., “[BioBERT: a pre-trained biomedical language representation model for biomedical text mining](https://doi.org/10.1093/bioinformatics/btz682),” *Bioinformatics* 36(4), 2020.

[^pubmedbert]: **PubMedBERT** argues the opposite case, and the disagreement is the interesting part.
    Gu and colleagues show that where a domain has abundant text of its own, pretraining from scratch beats continuing the pretraining of a general model, because the general start carries vocabulary and usage that the domain does not need.
    It is pretrained on PubMed abstracts and PubMed Central full text with a vocabulary derived from that corpus rather than from ordinary English.
    Microsoft has since renamed the released model **BiomedBERT**.
    See Gu et al., “[Domain-Specific Language Model Pretraining for Biomedical Natural Language Processing](https://arxiv.org/abs/2007.15779),” *ACM Transactions on Computing for Healthcare* 3(1), 2021.

[^scibert]: **SciBERT** is the multi-disciplinary case.
    It is pretrained from scratch on a random sample of 1.14 million full-text papers from Semantic Scholar—82% biomedical and 18% computer science, roughly 3.17 billion tokens, a corpus comparable in size to BERT’s own.
    Like PubMedBERT it builds its own vocabulary, *scivocab*, from that corpus; the authors report that this generally outperforms the same model using BERT’s original vocabulary.
    Note what the disciplinary split implies: a “scientific” model is not evenly scientific, and its coverage reflects whatever was sampled.
    See Beltagy, Lo and Cohan, “[SciBERT: A Pretrained Language Model for Scientific Text](https://aclanthology.org/D19-1371/),” EMNLP-IJCNLP 2019.

[^retrieval-chronology]: The chronology of retrieval runs the other way round from the order used here: [joint query–passage scoring for reranking](https://arxiv.org/abs/1901.04085) was demonstrated before [dense bi-encoder retrieval](https://aclanthology.org/2020.emnlp-main.550/).
    This book follows the independent-encoding branch first because its subject at this point is candidate retrieval across a whole collection, not because that branch came first.
