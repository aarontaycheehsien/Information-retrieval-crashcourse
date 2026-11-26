---
key: "preface"
kind: "chapter"
eyebrow: "Preface"
meta: "About 8 min"
---

## Why this book exists {#preface}

When a search system hands you a ranked list — or an answer with citations — two questions are hiding inside it, and they are almost always blurred together: *why did this record get into the candidate set at all*, and *why did it rank where it did?* This book exists to teach you to keep those two questions apart.
By the end, you should be able to look at any search tool your library licenses — Boolean, “semantic,” “AI-powered,” or all three at once — and ask which decision happened at which layer, what the vendor has actually documented, and what nobody outside the company can know.

It took me three years to acquire that skill the slow way.
Here is why.

Years ago, in library school, information retrieval got perhaps five minutes of a course called *Information Searching & Sources*.
TF-IDF got those five minutes and a formula; vector search got one slide near the end.
When someone in class asked the lecturer to explain it:

::: pull-quote
> Don’t worry about it.
> You won’t be examined on it.
:::

That was the right call at the time.
Academic databases behaved alike underneath — words as admission rules, and a ranking assembled from how often a term appears and how rare it is.
When every engine works the same way, knowing the engine buys you nothing and knowing the syntax buys you everything, and the syntax is what we all learned, thoroughly and well.
I went on to spend years as an academic librarian, teaching classes and studying discovery systems, and nothing in the job required me to understand the retrieval mechanics under the hood.
I argued this at more length in “[‘We’re Good at Search’… Just Not the Kind That the AI Era Demands](https://aarontay.substack.com/p/were-good-at-search-just-not-the),” which ended by calling for real information-retrieval competence in the profession.
This book is my attempt to answer my own provocation.

Around 2022, knowing the engine stopped being unimportant.
I have spent the years since learning this material the slow way: introductory retrieval courses, engineering blogs from the companies that build search infrastructure, conference talks, vendor documentation, and peer-reviewed papers on Transformer-based retrieval.
The climb is steep — not because the ideas are especially difficult, but because the material is scattered across communities that rarely cite one another, pitched at readers with a mathematics or computer-science background, and almost never written with a librarian’s questions in mind.
The questions I actually had were more fundamental. *How is this different from Boolean search?
How should I enter my queries now?
And how does this change which papers my researchers find?* Answering any of them usually meant reading three things that were mostly about something else.

This book is that climb, compressed.
It is what I wanted in 2022 and could not find.

### The words on the box stopped meaning anything {#the-words-on-the-box}

Since pretrained Transformer models entered text ranking around 2019, the field has moved unusually quickly, and it still feels a little like the Wild West.
No single neural architecture has simply replaced lexical retrieval.[^post-transformer-plurality] Instead we have an expanding pile of overlapping labels — *neural search*, *vector search*, *embedding search*, *semantic search*, *agentic search*, and the least helpful of all, *AI-powered search* — used interchangeably while describing entirely different things: a representation, a matching method, a stage in a pipeline, or simply a capability someone wants to market.
The words on the outside of the box no longer tell you much about what is inside it.

Six of these confusions recur often enough to be worth naming — treating *semantic search* as another name for dense retrieval is one — and the book names each one at the point where you can check it against a real mechanism. [The start of Part I](#core-distinction-checklist) lists all six.
They survive for the same reason: each lets a vendor say something true and have it heard as something stronger. ([Appendix D, A librarian’s map of search terminology](#appendix-search-terminology) maps the terminology in one place.)

### The half nobody is watching {#the-half-nobody-is-watching}

Ask an AI search tool a question and two quite separate things happen: something selects a handful of papers, and something else writes about them.
Almost every conversation about these tools — in the profession, in the press, in the fast-growing literature on hallucination — is about the writing.

But the two steps do not fail in the same way.
Checking whether a reference exists can expose a fabricated citation, but a real source can still be misrepresented.
Missing evidence is often harder to notice: the answer does not show you the papers it never received.
The answer is just as fluent, just as neatly cited, and quietly built on the wrong papers — or on a set missing the one everybody in the field would name.
Both failures require investigation.
A citation list alone establishes neither faithful writing nor adequate retrieval.

The generation half already has a crowd around it: computer scientists measuring fabrication rates, journalists stress-testing chatbots, an ethics literature several years deep.
The retrieval half has almost nobody — and it is the half libraries license, configure, evaluate and pay for.
If we do not ask which papers a system was able to reach, it is not obvious who will.
That does not mean librarians need to become retrieval engineers.
It means somebody in the library needs to understand enough of the stack to ask sensible questions, compare systems, and work out which layer a problem actually belongs to — the case I made in “[AI Search Is Rebundling Everything Libraries Know About Discovery](https://aarontay.substack.com/p/eleven-ways-of-looking-at-academic).” [Chapter 15](#library-practice) sets out what that takes in practice.

### Who this is for {#who-this-is-for}

Librarians are genuinely expert searchers, though that expertise takes different forms, and this book is written for three of them:

- **Information literacy librarians**, who teach people to turn questions into workable searches and to understand what different interfaces invite them to do;
- **Evidence synthesis librarians**, who build high-recall strategies across databases, controlled vocabularies and platform syntax, then document them so somebody else can rerun them;
- **Systems and discovery librarians**, who see search from the other side—configuration, indexes, integrations, and the questions vendors do or do not answer.

[There are many ways to be expert in search](https://aarontay.substack.com/p/i-built-an-elaborate-librarian-recommender).
This book assumes that professional knowledge and begins where those forms of expertise meet the retrieval machinery under the interface.
The first two audiences are primary; the third will find the procurement and evaluation chapters written with them in mind.

### What this book is, and what it is not {#what-this-book-is}

Because it is written for the readers described above, this is not a typical Information Retrieval 101 text.
It follows three deliberate principles.

- **Understanding before detailed mechanism.** The inverted index is explained in enough detail to show why it is fast and what it structurally can and cannot do — not enough for you to build one.
  You will get a sense of the latency and other trade-offs behind different indexing and retrieval choices; where the fuller machinery matters, it lives in [the appendices](#backmatter) rather than interrupting the main argument.
- **Examples familiar to librarians.** Wherever possible, I tie a concept to what a named library or academic search system is documented to do, together with the date I checked it.
  When the documentation runs out, I say so rather than infer what is happening.
  This is the part of the book that will age fastest, and it is dated so you can see it ageing; the mechanisms underneath move far more slowly than the products built on them.
- **Formulas only where they carry an argument.** A formula is a kind of compression: useful if you already read formulas fluently, an obstacle if you do not.
  A librarian assessing a search system needs to understand what BM25 responds to and what it is blind to, not how to calculate it by hand.

Equally, there are things this book is not:

- **Not an implementation guide.** You will not come out able to build a retriever.
- **Not a product review.** Named systems appear as dated illustrations of mechanisms, not as recommendations.
- **Not a substitute for a graduate course in information retrieval.** Specialists will find simplifications throughout.
- **Not a book about answer generation.** Chapter 1 opens with answer-generating RAG assistants, but the step in which a model writes the final prose stays outside the book’s scope.
  The book concentrates on how evidence becomes available before an answer is written.

It is meant to give you a floor to stand on: enough to follow a technical conversation, interrogate a vendor claim, and recognise when one of your own search problems is really a retrieval problem. [Where to go deeper](#where-to-go-deeper) lists what to read next.

::: {.orientation label="Before you start"}
#### How to read this {#orientation-title}

**No prior knowledge of information retrieval is assumed.** You should be able to start here knowing little more than Boolean searching. **No mathematics is required** either: formulas and worked examples are accompanied by explanations in words, and no calculation is required to follow the main argument.
Most mathematical detail is in the footnotes and appendices; Chapter 10 includes an optional RRF calculation.
Appendix F is core reading for the evidence-synthesis route.
Sections marked “for awareness” go a level deeper again, and sit inside the appendices.

The book divides naturally into three sittings — about 71 minutes for the Preface and Part I, about 107 for Part II, and about 84 for Part III — and you lose nothing by stopping between them.
Each chapter carries an estimated reading time beside its number, so you can also just pick one that fits the time you actually have.
Each part ends with an application exercise asking you to run real searches in a system available to you and write down what you find; the teaching notes include a public-access route.
These are probably the slowest part of the book and the part most likely to teach you something about your own tools, but you can skip them without losing the main argument.

**Reading straight through is the default route.** If you are here with a narrower purpose, there are five shorter routes:

- **Short orientation**—take the [45-minute reading-and-reflection route](read-this-first.html): the chapter summaries, key distinctions and closing puzzle map, with links back to the full explanations.
- **Instruction**—teaching information literacy?
  Protect [Part I](#part1), then [Chapter 11](#query-transformation) on query transformation and [Chapters 13](#diagnosing-failure) to [15](#library-practice) on failure, evaluation and professional practice.
- **Evidence synthesis**—focus on [Chapter 2](#boolean-admission), [Chapter 11](#query-transformation) and [Chapters 13](#diagnosing-failure) to [15](#library-practice), then read [Appendix F](#appendix-evidence-synthesis-high-recall-retrieval) as the application that connects candidate retrieval, high recall, screening and stopping.
  On this route, Appendix F is core rather than optional.
- **Procurement**—focus on [the category errors and distinctions](#one-category-error-resolved-and-one-still-ahead), [diagnosing where retrieval goes wrong](#diagnosing-where-retrieval-goes-wrong) and [the implications for library practice](#implications-for-library-practice).
  Those carry the vocabulary and the questions; the mechanics can wait until a vendor’s answer puzzles you.
  Keep [Appendix D](#appendix-search-terminology) open alongside them, and use [Chapter 10](#hybrid-and-fusion) and [Appendix E](#appendix-rank-fusion-and-learning-to-rank) when a system combines or reranks candidate lists.
- **Curiosity**—already comfortable with Boolean retrieval and BM25?
  Start at [learnt representations](#from-word2vec-to-retrieval-embeddings).
  Everything before that is largely devoted to establishing that lexical retrieval is broader than Boolean retrieval, which you may already accept.

Most examples come from scholarly and library search, though I occasionally use newer internet slang such as `delulu`{dir="ltr"} and `rizz`{dir="ltr"} — deliberately, because unfamiliar words make useful stress tests for search systems.
:::

*Now, to the machine itself.*

[^post-transformer-plurality]: “Wild West” is an editorial metaphor, not a claim that retrieval lacks standards, benchmarks or mature techniques. [Nogueira and Cho’s BERT reranker](https://arxiv.org/abs/1901.04085) appeared in 2019; [Lin, Nogueira and Yates](https://arxiv.org/abs/2010.06467) survey multi-stage reranking and dense retrieval as distinct Transformer applications; and [BEIR](https://arxiv.org/abs/2104.08663) compares lexical, learnt sparse, dense, late-interaction and reranking systems across 18 datasets, finding BM25 a robust baseline and substantial effectiveness–cost trade-offs among the neural approaches.
    The narrower claim is that no single neural architecture has displaced the lexical stack as the standard design.
