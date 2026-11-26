---
key: "appendix-advanced-inverted-index-execution"
kind: "appendix"
eyebrow: "Appendix C"
meta: "About 11 min · optional"
section_id: "app-C"
---

## Advanced inverted-index execution {#appendix-advanced-inverted-index-execution}

This optional appendix looks beneath the main explanation.
It first shows how ordered posting lists support a Boolean `AND` query, then traces how BM25 obtains and retains scores before introducing index compression and exact top-*k* pruning.
None of these implementation details is required for understanding the comparison between lexical and dense retrieval in the main text.

### How two ordered posting lists are intersected {#how-two-ordered-posting-lists-are-intersected}

For a Boolean `AND` query, the engine must find the document identifiers that occur in both posting lists.
The procedure below is often called a **two-pointer** or **two-cursor** intersection.
A cursor is simply a temporary bookmark showing which identifier in each list is being compared.

The example below uses a larger collection than the four records in the main text, so that the posting lists are long enough for the cursor rule to be visible.
The identifiers are therefore not the same as those in the [earlier `delulu AND interview` example](#boolean-treats-postings-as-sets).

Posting lists are normally sorted by document identifier.
To intersect two lists, the engine places a cursor at the start of each.
If the identifiers match, it keeps that document and advances both cursors.
If they differ, it advances only the cursor pointing to the smaller identifier.
Because both lists are ordered, neither cursor needs to move backwards or restart from the beginning.

:::: {.figure key="two-pointer"}
How two ordered posting lists are intersected

::: {.include src="figures/two-pointer.html"}
:::

::: caption
At each comparison, the engine either records a match or advances the list with the smaller current identifier.
Ordering makes earlier identifiers safe to leave behind.
The records shown here come from a larger collection than the four used in the main text, so that two matches rather than one are available to illustrate the rule.
:::
::::

This procedure explains Boolean intersection.
BM25 uses ordered posting lists differently: it normally gathers evidence from documents appearing in any of the query-term lists and combines the contributions belonging to each document.
The next section shows that ranked process.

### How BM25 actually uses the posting lists {#how-bm25-actually-uses-the-posting-lists}

Consider the same four records and the unquoted ranked query:

> `delulu job interview`

A simplified query-time path has five stages:

1. **Analyse the query.** The query becomes the three indexed terms `delulu`, `job` and `interview`.
2. **Look up those terms.** The term dictionary leads directly to three posting lists.
   The dictionary also supplies each term’s document frequency, from which inverse document frequency can be calculated.
3. **Traverse the ordered postings.** The engine encounters documents containing at least one query term.
   A document absent from all three lists cannot receive a lexical score and is never a candidate.
4. **Add the matching contributions.** A posting can supply the term frequency in that document; separate document metadata supplies document length.
   BM25 combines these with inverse document frequency.
   A missing query term contributes zero rather than automatically excluding the document.
5. **Retain the best *k* scores.** If the request asks for the top two results, the engine need not keep a fully sorted list of every score.
   It can maintain a small top-two structure, commonly a min-heap.

:::: {.figure key="inverted-index-anatomy"}
Anatomy of an inverted index at query time

::: {.include src="figures/inverted-index-anatomy.html"}
:::

::: caption
The dictionary answers “where is this term’s list and how rare is it?”
Postings answer “which documents contain it, and how often?”
Document metadata supplies facts such as length.
The lower row previews three storage and access techniques explained below; they are related, but they do different jobs.
:::
::::

We can now reproduce a small ranking rather than treating “the postings provide evidence” as a black box.
For this worked example, suppose the analyser lowercases the text but retains all the displayed words when calculating field length; the dictionary table above shows only selected terms.
The illustration uses the positive Lucene-style IDF, *k*~1~=1.2, *b*=0.75, *N*=4 and an average document length of four tokens.
Every matching query term occurs once.
The numbers are rounded to three decimal places and are only a teaching example; other analysis choices, BM25 variants or parameter settings can give different values.

:::: {.figure key="bm25-top-k"}
How BM25 turns postings into a top-two ranking

::: {.include src="figures/bm25-top-k.html"}
:::

::: caption
D1 wins because it matches all three terms.
The rarer terms `delulu` and `interview` contribute much more than `job`, which appears in every record.
D3 and D4 are slightly shorter or longer than average, so length normalisation adjusts their one-occurrence contributions.
Because each contribution is rounded to three decimal places independently, the displayed components may not sum exactly to the displayed totals; the totals are computed from the unrounded values.
:::
::::

At first the top-two heap has empty slots, so its competitive threshold is effectively zero.
Once D1 and D2 fill it, the lower of their scores—D2’s 0.799—becomes the threshold, conventionally written **θ** (theta).
A later candidate must beat θ to enter the top two.
If that happens, the displaced score leaves the heap and θ can rise.

This walkthrough uses a simple document-at-a-time view: move through ordered document identifiers and sum the query-term contributions for each candidate.
Production engines may organise traversal differently, but they still obtain lexical evidence from the term dictionary, postings and document statistics.

| Boolean use of postings | BM25 use of postings |
|---|---|
| Determine whether a document satisfies the logical expression. | Find documents with matching evidence and calculate graded term contributions. |
| A compulsory missing term excludes the document. | A missing term normally contributes zero, but does not necessarily exclude the document. |
| Boolean alone produces an eligible set; a later ranker may order it. | BM25 assigns graded scores; the system may completely order the candidates or retain a top-*k*. |

: The same posting lists used for Boolean evaluation and for BM25 scoring.

The underlying postings have not changed.
Boolean and BM25 apply different retrieval rules to them.

**Try it:** [The BM25 Evidence Lab](bm25-evidence-lab.html) is this walkthrough made live.
It uses the same positive Lucene-style inverse document frequency, the same *k*~1~ and *b*, and the same scoring calculation on a different six-record collection small enough to check by hand.
The lab calculates term counts and scores directly; it does not implement the posting-list traversal or pruning explained here.

### Compression, skipping and blocks solve different problems {#compression-skipping-and-blocks-solve-different-problems}

Posting lists are sorted by document identifier.
Systems commonly store the **gaps** between identifiers rather than every full identifier: `101, 104, 105` becomes `101, +3, +1`.
Small gaps can be encoded compactly.
This reduces storage and memory traffic; it does not omit any matching document.

**Skip information** supports an operation such as “advance this list to document 104 or beyond” without decoding every intervening posting one by one.
It is useful when intersecting Boolean lists and when ranked-query algorithms need to align their cursors.

**Blocks** divide a long posting list into independently accessible or decodable groups.
This can improve locality and make jumping into the list cheaper.
Blocks can also store metadata such as the largest possible score contribution within each block.
Blocks by themselves, however, do not imply score-based pruning: safe pruning requires suitable upper-bound information and an algorithm that uses it.

### For awareness: MaxScore, WAND and block-max pruning {#for-awareness-maxscore-wand-and-block-max-pruning}

The four-record example is tiny, so scoring every candidate is easy.
At web or library scale, an engine would prefer not to calculate a complete score for a document that cannot possibly enter the requested top *k*. **Dynamic pruning** methods combine the current threshold θ with safe upper bounds on the contribution still available.

> If a candidate’s score so far plus its maximum possible remaining contribution cannot beat θ, it is safe to skip that work.

Three names are worth recognising:

- **MaxScore** orders term lists by their maximum possible contribution and separates them into essential and non-essential lists.
  A document found only in non-essential lists cannot beat the threshold.
  Their evidence is consulted only when it could still change the top *k*.
- **WAND**—short for *Weak AND*, although it is a ranked-query execution strategy rather than Boolean `AND`—orders the current posting-list cursors by document identifier.
  It accumulates upper bounds until it finds a pivot that could beat θ, then advances earlier cursors towards that pivot instead of fully scoring hopeless candidates.
- **Block-Max WAND** adds tighter upper bounds for smaller blocks of a posting list.
  If the best possible combined score in the current blocks cannot beat θ, the engine can skip the whole block rather than examining its documents individually.

:::: {.figure key="dynamic-pruning"}
Same top-two result, less scoring work

::: {.include src="figures/dynamic-pruning.html"}
:::

::: caption
MaxScore and WAND use term-level bounds; Block-Max WAND can use tighter local bounds.
The block panel is a schematic extension to a larger collection, because four documents are too few to make block skipping useful.
:::
::::

With valid upper bounds, these methods change the work performed, not the answer: they return the same exact top *k* as exhaustive scoring.
That guarantee is different from approximate early termination, which may deliberately trade some result quality for speed.
The original methods are described by [Turtle and Flood’s MaxScore work](<https://doi.org/10.1016/0306-4573(95)00020-H>), [Broder and colleagues’ WAND paper](https://doi.org/10.1145/956863.956944) and [Ding and Suel’s Block-Max indexes paper](https://doi.org/10.1145/2009916.2010048).

### Why learnt sparse queries cost more to run {#appendix-learnt-sparse-query-cost}

Everything above assumed a query of a few typed terms. [Learnt sparse retrieval](#learnt-sparse-representations) breaks that assumption, and the machinery just described explains what follows.

The efficiency problem is structural rather than incidental.
A learnt sparse model earns its recall by activating vocabulary dimensions the searcher did not type.
Those dimensions are ordinary index terms, so the engine reaches them in the ordinary way—but the terms such a model adds are disproportionately *frequent* ones, and frequent terms are precisely those with the longest posting lists.
A three-word query that expands to thirty weighted terms does not simply do ten times the work; it traverses the union of thirty lists, several of which may be among the longest the collection holds.

Expansion can make dynamic pruning less effective by activating more posting lists and more candidate documents.
Even when each added term has a small contribution, several contributions can combine to exceed the current threshold.
A lower individual upper bound does not itself make a term harder to dismiss: pruning depends on joint bounds, their distribution across blocks and the current top-k threshold.

Published measurements have put SPLADE-style latency at several times BM25’s on comparable hardware, with short queries the worst case.
Lassance and Clinchant’s “[An Efficiency Study for SPLADE Models](https://arxiv.org/abs/2207.03834)” (SIGIR 2022) reports closing much of that gap through three moves: query-side regularisation, which penalises activating too many query terms in the first place; disjoint query and document encoders, so the query side can be made deliberately cheaper than the document side; and pruning of the longest posting lists.

The practical reading for a library is that learnt sparse retrieval is familiar to *host* and not automatically cheap to *query*, and that the two questions should be asked separately.
A vendor claim that a method “runs on standard inverted-index infrastructure” answers only the first.

---
