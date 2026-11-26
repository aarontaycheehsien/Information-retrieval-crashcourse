---
kind: "backsection"
nav: "both"
---

## What you can now ask {#what-you-can-now-ask}

[The Preface](#preface) set one test for this book: that by the end you could look at a search system and separate two questions that are usually blurred together. *Why did this record get into the candidate set at all*, and *why did it rank where it did?*

Both now have machinery behind them.
The first is settled by an admission rule and a candidate boundary: a compulsory Boolean clause, a minimum-match threshold, a first-stage retriever’s top-*k*, an approximate index that searched only part of the vector space, or a chunking decision that meant the sentence you wanted was never an indexed unit at all.
The second is settled by a scoring function and everything downstream of it: BM25’s weighted term evidence, a similarity between two pooled vectors, a cross-encoder reading query and candidate in one sequence, a fusion rule, a reranker working through a budget of thirty.

Keeping them apart matters because [candidate generation sets the ceiling on a fixed pool](#precision-and-recall).
Reranking and display cut-offs can improve precision and recall at a chosen depth, but cannot add a record absent from that fixed candidate pool.
A new retrieval route or round can add candidates.
That asymmetry is what most of this book has been elaborating, and it is the thing worth carrying out of it if nothing else survives.

[Chapter 5](#embeddings) and [Chapter 6](#retrieval-encoder) now let you ask two questions where one vague claim about embeddings used to suffice: what relationships the learnt geometry encodes, and what architecture, pooling and retrieval training turn that geometry into a searchable index?
A product that answers only the first has not yet described its retriever.

[Chapter 9](#reranking-and-hybrid) and [Chapter 10](#hybrid-and-fusion) likewise separate spending more computation on one shortlist from combining several candidate-generation routes.
You can now ask what retrieved each candidate, what the cut-offs excluded, whether routes were blended or selected, and whether fusion used ranks, normalised scores or a learnt rule.

[The three opening puzzles](#three-familiar-search-results-and-three-puzzles) are worth reading as a set rather than as three separate answers, because what separates them is not how hard each one was.
It is whether anything outside the result screen was available to settle it.

:::: {.distinction-map}
#### The three puzzles, and what each one settled {#closing-puzzle-map-title}

Chapter 1 posed three ordinary search behaviours and left them open.
This is where each of them ended up.

::: distinction-map-list
Puzzle 1 · scite[*Unresolved*]{.verdict}
:   An invented string did not empty a result list reporting millions of matches.
    Any of [Chapter 4’s four explanations for a missing word](#what-might-have-happened-to-a-missing-query-word) could account for it.
    The screen cannot separate them, and looking harder will not help. [Chapter 4’s verdict](#returning-to-the-opening-puzzles).

Puzzle 2 · Google Scholar[*Unresolved as to ranking*]{.verdict}
:   About 9.4 million results reported, with a documented limit of 1,000 shown.
    A display limit is an output boundary: it establishes what you may page through, and nothing whatever about which signals produced the order. [Chapter 4’s verdict](#returning-to-the-opening-puzzles).

Puzzle 3 · Semantic Scholar[*2025 pipeline documented · August 2026 query processing unresolved*]{.verdict}
:   In August 2026, a natural-language question returned 13 results where the keywords returned about 35,300.
    The 2025 technical account documents lexical first-stage retrieval and a learnt reranker over a capped candidate set for the main relevance search.
    Which pipeline handled the August 2026 queries and why the counts differed remain unproven. [Chapter 7’s account](#returning-to-puzzle-three-why-did-the-keyword-query-retrieve-more).
:::

The result screens leave the mechanisms behind all three observations open.
The Semantic Scholar account adds evidence about one documented pipeline at an earlier date.
::::

That is the finding, not a failure to reach one.
What changed between Chapter 1 and here is not that the screens became legible.
It is that you now know which questions a screen was never going to answer, and which document to go looking for instead.

[The Preface warned that the words on the box had stopped naming what is inside](#the-words-on-the-box), and promised six collapses would be named where they could be checked.
This is the point to go back and check, against [the distinction at the end of Part I](#distinction-map-interface) and [the five that open Part II](#distinction-map-vocabulary).
If you can now say why lexical search is broader than strict Boolean retrieval; why not every vector is an embedding and “vector embedding search” adds little precision; why a vector need not be dense or semantic; why *semantic* names a goal while *dense* names one route towards it; why top-*k* is an output boundary rather than a retrieval method; and why neural information retrieval covers several arrangements that behave quite differently—then the vocabulary is doing the work it was meant to do.
Every one of those confusions survives because it lets a vendor say something true and have it heard as something stronger.

Some things this does not give you.
You cannot read an architecture off an interface: the chapters that came closest managed it by reading documentation, not result screens.
Most vendors will not answer [the questions in Chapter 15](#choosing-and-governing-search-tools), and a refusal is itself something you can record.
Every claim here about a named product carries a date because it will age, while the mechanisms underneath move far more slowly than the products built on them.
And none of this establishes whether a particular search was any good.
It establishes how to ask, which is a smaller claim and a more durable one.

I began this book with a lecturer telling a room that vector search would not be examined.
That was a reasonable thing to say in the world it was said in.
When every academic database works the same way underneath, knowing the engine buys you nothing and knowing the syntax buys you everything—and the syntax is what we all learned, thoroughly and well.
What happened since is that the engines stopped agreeing with each other, fairly quietly, while the interfaces stayed roughly the same shape.
The training that was right then is simply no longer sufficient now, and that is the whole reason this book had to exist.

If you do one thing with it, make it [the evaluation set](#building-a-local-evaluation-set).
Thirty to fifty queries out of real practice, the handful of records that ought to surface for each, judged to a fixed depth, deliberately including the searches you already know go badly.
Building and judging the set takes time; an afternoon may suffice to rerun an established set, depending on the systems and judgement depth.
It is also the only measurement in this book whose definition of relevance your library chose, and the only one you can rerun the next time a system changes underneath a saved search without telling anybody.

Start with one comparison using the [evaluation kit’s template and worked example](evaluation-kit.html), then grow the set from searches that matter locally.
