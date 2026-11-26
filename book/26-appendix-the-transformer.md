---
key: "appendix-the-transformer"
kind: "appendix"
eyebrow: "Appendix A"
meta: "About 6 min · optional"
section_id: "app-A"
---

## The Transformer {#appendix-the-transformer}

Nearly every learnt model named in this book—BERT, the bi-encoders of Chapters 6 to 8, cross-encoders, ColBERT, and the large language models that rewrite queries or rerank shortlists—is built from the same architecture.
This optional appendix explains what that architecture does and why it mattered.
No mathematics is required, and none of it is needed to follow the main comparison between lexical and dense retrieval.

### The problem it solved {#appendix-transformer-problem}

Before 2017, the standard way to give a model a sense of context was a **recurrent** network: read the sequence one position at a time, carrying a running summary forward.
Two costs follow from reading in order.
Training cannot be parallelised across positions, because position ten cannot be computed until position nine is done.
And information from early in a sequence has to survive every intervening step to influence a later one, so long-range connections are weak in practice.

[Vaswani and colleagues](https://arxiv.org/abs/1706.03762) proposed dispensing with recurrence entirely.
Their title—*Attention is all you need*—is the claim: the attention mechanism that had been used to *supplement* recurrent models was sufficient on its own.

### What self-attention does {#appendix-transformer-attention}

In an encoder’s full **self-attention**, every position can attend to every other position in the input sequence in a single step.
A decoder’s causal mask restricts that view to the current and earlier positions, as explained below.
Each token’s new representation becomes a weighted blend of all the tokens around it, and—this is the important part—the weights are computed from the content rather than fixed by distance or grammar.
In *the bank refused the loan*, the representation of `bank` can draw heavily on `loan` and `refused`; in *the river bank*, it draws on `river` instead.
Nothing tells the model in advance which neighbours matter.
It learns that from data.

Two consequences matter for retrieval.
Because every position is computed against every other simultaneously, much of the work parallelises, which helped make training on very large corpora practical.
Self-attention also gives distant positions a direct interaction path rather than forcing information through every intervening recurrent step.
Distance can still matter through positional information, learnt attention patterns and finite context, so long-range influence is possible rather than cost-free.

The price is that cost grows with the square of sequence length: doubling the input roughly quadruples the attention work.
This is one reason retrieval systems [chunk long documents](#one-document-one-chunk-and-one-vector-are-not-the-same-thing) rather than encoding them whole, and one reason a [cross-encoder](#cross-encoder-reranking) is affordable over a shortlist but not over a collection.

:::: {.figure key="attention-context"}
The same word, two sentences, different neighbours

::: {.include src="figures/attention-context.html"}
:::

::: caption
Nothing in the architecture assigns these weights.
They are computed from the content, which is why the same token is represented differently in the two sentences, and why a model that had only distance or grammar to go on could not make the distinction.
The widths here illustrate the mechanism; they are not measurements taken from a particular model, and a real model spreads the work across many attention heads and layers rather than one comparison per word.
:::
::::

### Two strands: encoders and decoders {#appendix-transformer-halves}

The original paper describes a translation system with two halves.
An **encoder** reads the whole input sentence at once and builds a representation of it.
A **decoder** then writes the translation one word at a time, able to see only what it has produced so far, because a model that could read ahead to the answer would learn nothing about predicting it.

Within about a year of the paper, research had divided into two strands, each keeping one half and discarding the other.
Almost every model name a librarian encounters descends from one or the other, and knowing which explains most of what a model is good for.

Both strands kept the self-supervised arrangement described in [Chapter 5](#what-the-model-was-trained-to-predict).
Neither needed anyone to label anything in order to pretrain, because in both cases the corpus supplies its own answers: hide part of a text, then score the model on recovering it.
What separates them is only which part is hidden, and therefore how much of the text the model is allowed to see while recovering it.

**The decoder strand came first.** In June 2018 OpenAI published [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), keeping only the decoder and training it to predict the next token across a large corpus.
That model was GPT.
Scaling the same design produced GPT-2, GPT-3 and the systems now generally meant by *large language model*.
This is the strand behind the generation half that [this book set aside at the outset](#retrieval-not-generation)—and behind the parts of retrieval it does cover, where an LLM [rewrites a query](#beyond-one-query-expansion-decomposition-and-routing), [reranks a shortlist](#llms-as-rerankers) or [chooses the next action](#agentic-search-who-chooses-the-next-retrieval-action).

**The encoder strand followed four months later.** [BERT](https://aclanthology.org/N19-1423/), from Google, kept only the encoder and trained it by masking tokens rather than predicting the next token—which is what allows it to read in both directions at once.
Its paper argues directly against the decoder strand on this point: a left-to-right model is, in its terms, unnecessarily constrained when the task is to understand an existing text rather than continue it.
That strand produced the models used for classification, entity recognition and question answering, and later the retrieval encoders in this book: Sentence-BERT, dense bi-encoders, [ColBERT](#where-colbert-style-late-interaction-fits) and [cross-encoders](#cross-encoder-reranking).

| Half kept | How it reads | Trained to | What it suits | Where it leads |
|---|---|---|---|---|
| **Encoder** | All positions at once, both directions | Fill in masked tokens | Representing a text that already exists | BERT, and the retrieval encoders derived from it |
| **Decoder** | Causal attention: each position sees only earlier positions and itself | Predict the next token | Generating continuations | GPT and the large language models |

: The two halves of the original Transformer, and the strand of research that kept each.

One point about the decoder row resists compression into a table cell, and is worth making because it is commonly got wrong.
Reading left to right constrains what each position may see; it does not force training to proceed one position at a time.
A causal mask lets every position be trained in parallel while still hiding the future from each one.
Generation is the sequential part: at inference the model produces one token at a time, because each new token depends on the ones it has just written.

This is why an encoder is the natural starting point for a retrieval model: the task is to represent a query or a passage that already exists, not to continue it.
It is also why the bidirectional reading described in [Chapter 5’s section on BERT](#what-bert-is-and-what-it-still-needs) is available to an encoder and not to a decoder.

Two qualifications keep the split from being tidier than it is.
Some model families kept both halves—T5 and BART among them—and treat every task as text in, text out.
And the strands have partly converged since: several current embedding models are initialised from decoder-style models and adapted for retrieval, which is why a product using an LLM-derived encoder is not doing anything contradictory.
The distinction still explains what most documentation is referring to, but it describes a lineage rather than a rule.

### What this appendix leaves out {#appendix-transformer-scope}

Attention is usually described through three learnt projections of each token, conventionally called query, key and value; the weights come from comparing queries against keys.
Real implementations also run several attention operations in parallel (**multi-head** attention), add explicit **positional** information because attention alone is order-blind, and stack the whole arrangement in layers.
None of that changes the account above, and none of it is needed here.
Readers who want the mechanism in detail should go to [the paper itself](https://arxiv.org/abs/1706.03762), which is unusually readable, or to [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) for a diagrammatic walkthrough.
