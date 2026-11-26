---
key: "beyond-boolean"
kind: "chapter"
eyebrow: "Chapter 4"
meta: "About 16 min"
question: "How can a search remain lexical without behaving like strict Boolean?"
legacy_anchors: ["ch3"]
---

## Lexical search beyond strict Boolean {#beyond-boolean}

::: {.stage-map on="query-transformation analysis first-stage"}
:::

::: chapter-orient
Librarians routinely treat *lexical* and *Boolean* as synonyms.
The reasoning feels natural: if a system returns records that lack one of my words, it can’t be matching words—so it must be doing something semantic.

Yet a lexical system can return a record that lacks one of the query terms.
It may require every term, some terms, or any one matching term, while using term matches to calculate scores.
This chapter separates four things that the word “search” usually blurs together: query understanding, transformation, analysis and execution rules.
It then uses them to show exactly how far the first two opening puzzles can be taken, and where the interface stops answering.
The Semantic Scholar example also requires evidence about the retrieval pipeline, which is examined in Chapter 7.
:::

::: {#distinction-lexical-boolean .key-distinction-label}
Key distinction
:::

### Lexical search does not have to mean Boolean search {#lexical-search-does-not-have-to-mean-boolean-search}

**Lexical retrieval draws matching evidence from the text’s words or character sequences.** It includes [direct string and pattern matching with grep](#grep-searching-text-directly) as well as matching analysed query terms against indexed document terms.
Boolean retrieval and BM25 belong to this family: Boolean conditions govern admission, while BM25 assigns weights to term evidence.
An index changes how matches are found efficiently; it is not a requirement for a method to be lexical.

The arrangement librarians know best combines the two: a Boolean expression decides who is eligible, then a ranker orders the survivors.
BM25 can also gather and rank candidates directly from records matching any analysed query term.

Suppose the analysed query is:

> apple orange banana

A familiar academic-search interpretation is:

> apple `AND` orange `AND` banana

Under that model, the implied `AND` admits only records containing every term, and a ranker orders the survivors. *A relevance-ranked result list can look similar under different admission rules.* The same vocabulary, the same analysis pipeline and the same inverted index support at least three different rules:

1. **All terms required** (implied `AND`, then ranking).
   A record missing `banana` is out before the ranker ever sees it.
2. **Some terms required** (minimum match).
   The system sets a threshold—say, two of three terms—and a record clearing it becomes a candidate.
3. **Any term suffices** (any-match ranked retrieval—what Chapter 3 called [direct BM25 retrieval](#how-bm25-uses-the-same-inverted-index)).
   One matching term makes a record a candidate; every further match adds weighted evidence.
   BM25 commonly runs this way, gathering candidates from the *union* of the posting lists rather than waiting at an `AND` gate.[^bm25-one-term-floor]

All three are lexical.
Not one of them needs embeddings, neural networks or “semantics”.
A record lacking a typed word therefore does not establish semantic matching; [What might have happened to a missing query word](#what-might-have-happened-to-a-missing-query-word) sets out what to check first.

:::: {.figure .worked-figure key="admission-worked"}
Keep the records fixed; change the admission rule

::: {.include src="figures/admission-worked.html"}
:::

::: caption
All three admission arrangements remain lexical.
The ranking B, A, C is stipulated to illustrate the separate output step, not calculated from these cards.
Matching more distinct terms does not guarantee a higher BM25 score: rarity, term frequency and document length also matter.
:::
::::

An **admission rule**, a **ranking function** and a **top-*k* output boundary** therefore solve different problems: who may compete, how candidates are ordered, and how many leaders are retained.
A production system can control all three independently.

In the terminology introduced in Chapters 2 and 3, `apple OR orange OR banana` is still an [exact-match Boolean specification](#exact-match-retrieval): A, B and C satisfy it.
A separate scoring rule can then provide [best-match ranking](#best-match-retrieval).
Any-match eligibility alone does not supply that ranking.

::: {.common-confusion label="Historical example"}
#### Early Google: a useful counterexample {#early-google-non-boolean-did-not-mean-non-lexical}

Google once described multiword searches as `AND` queries, but later began silently omitting some terms and was described as behaving like a “soft AND.”
Ranked lexical retrieval could still order the remaining matches.[^google-apparent-nonlexical] Google introduced BERT into query understanding and ranking only in 2019, though machine-learning ranking components predate it.[^according-to-some-reports-google-s-rankbrain-int]
:::

::: {#what-bm25-can-and-cannot-do .legacy-anchor}
:::

### A bad term: exclusion under AND, distortion under BM25 {#impact-of-bm25-compared-to-boolean-on-poor-query-terms}

Consider this query, where `foolish` is someone’s weak attempt at a synonym for `delulu`:

> delulu job interview expectations foolish

The same bad term does different damage under different rules.

Under implied `AND`, `foolish` is compulsory.
Relevant records that never use the word are excluded before ranking begins—and nothing downstream can recover them, because no ranker can rank what it never received.

Under any-match BM25, a record can remain eligible through its other matching terms.
The added term `foolish` can still change the ranking: if it is rare in the collection, its high IDF can increase the scores of records containing it, even though it poorly represents the searcher’s need.
The [Evidence Lab](bm25-evidence-lab.html) demonstrates the effect.

Term-frequency saturation cannot identify a weak query term; it only limits the benefit of repeating that term inside a document.
BM25 is lexical evidence made less binary, not semantic understanding.

:::: {.figure .worked-figure key="poor-term-two-rules"}
One weak query term, two different consequences

::: {.include src="figures/poor-term-two-rules.html"}
:::

::: caption
In the lab collection, only F contains `foolish`; its rarity does not make it a good synonym or F a better answer.
No numerical ranking is asserted here.
:::
::::

Both systems can handle the query as designed and still return poor results because `foolish` poorly represents the searcher’s need.

::: {#what-happened-to-the-missing-word .legacy-anchor}
:::

### What might have happened to a missing query word {#what-might-have-happened-to-a-missing-query-word}

So a result comes back without one of the words you typed.
What happened to the word?
Four explanations are consistent with what you can see:

- **It was removed during analysis**—discarded as a stop word or punctuation before retrieval began.
- **It was removed or changed during rewriting**—an upstream component shortened, expanded or reformulated the query.
  Unlike routine analysis, this is explicit rewriting, which [a later section](#words-sent-to-retrieval-may-not-be-the-words-you-typed) takes up.
- **It survived, but was optional**—nothing required it.
  Matching it could have improved a score, or it may have matched nothing at all, finding no posting list.
  Either way, other results survive; under strict `AND`, a required unmatched term would have emptied the result set.
- **It matched evidence outside the visible excerpt**—another indexed field, an expanded term, an older indexed version or off-page evidence.
  Inspect the searchable fields before concluding that no lexical match occurred.

:::: {.figure .worked-figure key="missing-word-paths"}
A missing word can have four different histories

::: {.include src="figures/missing-word-paths.html"}
:::

::: caption
A result snippet cannot distinguish these explanations.
Several may operate in one query.
Inspect the processed query, admission rules and indexed fields before inferring a retrieval architecture.
:::
::::

Several explanations may operate in the same search: a system may discard some terms, require only a subset of the survivors, and rank by weighted matches.
This is the scite puzzle in miniature.

### The words sent to retrieval may not be the words you typed {#words-sent-to-retrieval-may-not-be-the-words-you-typed}

Drop the assumption that the words reaching the index are the words you typed.
Many systems first *interpret* what you typed, then build a different internal query—one better suited to the index behind it.
Like analysis, this explicit rewriting changes what reaches retrieval, but it does so by reformulating the request.
The book has met it twice already: as one of the four explanations above, and as the first step of Primo Research Assistant’s pipeline in [Chapter 1](#anatomy-of-a-cited-answer).

That puts four distinct jobs between your keyboard and the posting lists.
Each has now appeared in this book; here they are in the order they run.

- **Query understanding**—interpreting the request: spotting a phrase, an entity, a date, an intent.
  Understanding can inform a decision without altering a single word of the query.
- **Query transformation** (query rewriting)—actually changing what retrieval receives: correcting, mapping, expanding, restructuring or splitting what you entered.
- **Query analysis**—the routine plumbing of Chapter 2: [tokenisation](#before-the-index-text-becomes-tokens), normalisation, [stemming and lemmatisation](#after-tokenisation-stemming-and-lemmatisation), stop-words.
  It prepares strings for matching.
  It implies no AI and no understanding of meaning.
- **Query execution rules**—this chapter’s dial: are the resulting clauses required, optional, or subject to a [minimum match](#lexical-search-does-not-have-to-mean-boolean-search)?

:::: {.figure .query-flow key="lexical-query-flow"}
Interpretation may lead to transformation before lexical retrieval

::: {.track .five-step}
- **User input** keywords, a question or a longer description
- **Query understanding** recognise phrases, entities, dates, intent or constraints
- **Query transformation** correct, map, expand, restructure or add fields and filters
- **Analysis and execution rules** tokenise and stem; apply required, optional or minimum-match rules
- **Lexical retrieval** Boolean admission, BM25 ranking or both
:::

::: caption
Understanding interprets the request; transformation changes what is sent to a retrieval pass.
The retrieval method still determines how documents become candidates and receive scores. [A later chapter](#beyond-one-query-expansion-decomposition-and-routing) adds route selection and feedback from an earlier pass.
:::
::::

A contemporary interface may accept a natural-language question, identify its dates or proposed filters, and use a parser or language model to construct a Boolean expression.
Natural-language input therefore does not imply a non-lexical engine: the transformed query may still go to Boolean admission and BM25 ranking.

Rewriting is the second of [the four explanations for a missing word](#what-might-have-happened-to-a-missing-query-word).
Understanding alone does not remove a typed word; it matters only when its interpretation causes one of those changes.
Chapter 11 returns to these operations with multi-query, routed and feedback-based retrieval available.

The overview below brings the separate controls together, now that each has been explained.

:::: {.figure .worked-figure key="three-lexical-admission-rules"}
Overview: from query processing to ranked lexical results

::: {.include src="figures/three-lexical-admission-rules.html"}
:::

::: caption
A recap of possible arrangements, not a mandatory sequence.
Admission, ranking and the output boundary are separate controls, and direct BM25 retrieval gathers and scores candidates together.
Citation and recency signals can supplement lexical evidence but are not themselves lexical matches.
:::
::::

### Returning to the first two opening puzzles {#returning-to-the-opening-puzzles}

[**Scite:**]{#returning-to-scite} the invented string in the [opening screenshot](#scite-opening-caption) was not compulsory.
It may have been removed during analysis, removed or changed by an upstream rewrite of the query, retained as optional evidence, or retained without matching a posting.
The screen cannot distinguish those explanations or identify BM25, dense retrieval or any other architecture.[^scite-lexical-suggestive]

[**Google Scholar:**]{#returning-to-google-scholar} the [reported hit count](#scholar-opening-caption), relevance ordering and viewable set are different properties.
Google Scholar reports millions of matches but documents a display limit of [1,000 results](https://scholar.google.com/intl/us/scholar/help.html).
That is an observable output boundary, but it does not reveal the scoring signals, whether every match received a final score, or whether the displayed records are a global top-*k*.

[**Semantic Scholar remains unresolved:**]{#returning-to-semantic-scholar} the [August 2026 result counts](#semantic-scholar-opening-caption) tell us what happened, not where meaning entered the pipeline. [The end of this chapter](#third-temptation) explains why it waits for Part II.

::: pull-quote
> A result can look as though it ignored one of your words even when the search used lexical matching throughout.
> The screenshot alone cannot tell us how scite handled the invented string.
:::

::: {#two-category-errors-to-avoid .legacy-anchor}
:::

### What Part I settles, and what it hands on {#one-category-error-resolved-and-one-still-ahead}

[The first two puzzles from Chapter 1](#a-map-of-the-arguments-ahead), scite and Google Scholar, can be explained using the distinctions introduced in Part I.

:::: {.distinction-map}
#### What a result screen can settle {#distinction-map-interface}

This is the one confusion of the six [listed at the start of Part I](#core-distinction-checklist) that you can catch from a result screen, which is why it is settled here rather than held over to Part II.
It needs nothing a vendor had to write down—only the recognition that a result can lack a typed term for several reasons, including an admission rule other than strict all-term conjunction.

::: distinction-map-list
lexical search = Boolean search
:   A record can come back missing one of your words while the system is scoring on nothing but words.
    Boolean retrieval is one form of lexical retrieval; minimum-match rules and BM25 ranking can remain lexical too, and only the all-term conjunction requires every processed term.
    Any-match eligibility can also be expressed as Boolean OR; the separate ranking function supplies graded scores.
    See [*Lexical search does not have to mean Boolean search*](#distinction-lexical-boolean).
:::

The Google Scholar example separates the reported match count from the number of results a user can view.
A reported count is an estimate of matches, and a display limit is a display boundary rather than a scoring decision. [The verdict above](#returning-to-the-opening-puzzles) sets out the general form: admission decides who competes, the ranking function orders them, and the output boundary decides how many are kept—three separate controls, of which an interface reports only the last.
::::

::: {#third-temptation}
The Semantic Scholar puzzle is not of this kind.
A product named *Semantic Scholar* tempts you to read a label as an architecture, and nothing visible on its interface can confirm or refute the reading.
We do not yet have the distinctions needed to ask whether retrieval itself was lexical, whether it used dense representations, whether semantic processing occurred only after retrieval, or whether several stages were combined.
That is why the remaining five confusions wait for [the opening of Part II](#distinction-map-vocabulary).
Two of them already matter for what follows. **Semantic search does not mean dense retrieval**: semantic names a goal, and dense retrieval names one technical route towards it. **Vector does not automatically mean dense, learnt or semantic**: lexical term weights such as BM25’s can themselves be held in vectors, as [Chapter 8](#distinction-vector-semantic) shows.
:::

The remaining problem is vocabulary mismatch: a paper about `unrealistic expectations` may stay out of reach of a search for `delulu`.
A system can bridge that gap in two places:

- **Change the query, keep the index.** Correct, expand or map the query, then match terms as before.
- **Change the representation.** Encode queries and documents so that texts expressing the same idea are placed near one another whether or not they share any words, and retrieve by proximity rather than by matching.

The next chapters examine the second route while keeping the first in view.

:::: chapter-close
1. Lexical retrieval includes direct string or pattern matching and matching analysed terms through an index.
   In the indexed systems developed here, posting lists identify the records containing each term.
   Boolean-then-ranking is a common academic-search pattern, but minimum-match and any-match ranking are lexical too.
2. Analysis, execution rules, query transformation — or a term that simply matched no posting list — can explain a missing typed word without implying dense or semantic retrieval.
   Understanding matters when its interpretation triggers one of those changes.
3. Admission, ranking and the top-*k* output boundary are separate controls: admission forms the candidate set of records that may compete, ranking orders it, and the boundary decides how many are kept.
4. Part I explains the scite and Google Scholar behaviours — and shows why the interface alone cannot identify the mechanism behind either.
   The Semantic Scholar observation remains open until semantic capability, dense representation and pipeline stage can be separated.

::: {.chapter-transition}
Non-Boolean does not mean non-lexical.
Part II next asks how a learnt representation can connect texts that share no analysed terms, then whether that mechanism is the same thing as semantic search.
:::
::::

::: self-check
A result lacks one of the words you typed. Name the four lexical explanations to exhaust before reaching for a semantic one.

:   Analysis may have removed it, transformation may have rewritten it, or it may be optional (including when it has no posting list).
    Alternatively, it may match an indexed field or version not visible in the excerpt.
    Query understanding alone is not a fifth explanation unless its interpretation triggered one of those changes.
    None of these observations identifies the complete retrieval architecture.

What are the three independent controls in a ranked lexical search?

:   The admission rule decides who may compete, the ranking function orders the candidates, and the top-*k* output boundary decides how many leaders are retained.

An interface accepts a natural-language question and produces an editable Boolean query. What changed?

:   Query understanding may have recognised concepts or constraints; query transformation produced the changed Boolean retrieval input.
    The retriever may still use Boolean admission and lexical ranking over an inverted index.
:::

[^bm25-one-term-floor]: This weighted evidence still has a floor.
    A pure TF-IDF or BM25 score is a sum of contributions from matching terms, so a document matching none of the analysed query terms has nothing to contribute and scores zero.
    In practice such a document is never even considered: the engine assembles its candidates from the posting lists of the query terms, which is an implicit `OR`.
    Retrieval and ranking under a purely lexical scoring model therefore still require at least one matching term.
    This is not a minimum-match rule of the kind described above, but simply where the arithmetic bottoms out; a configured minimum-match rule raises the floor above one.
    The terms in question are those surviving analysis and any query rewriting, not necessarily the words as typed.

[^google-apparent-nonlexical]: An apparently missing query term on the live page is not conclusive evidence that Google ignored the term or matched the page semantically.
    Google’s indexed version may differ from the current page because recrawling and reindexing are not immediate; Google notes that crawling can take from a few days to a few weeks.
    Google also [uses links as a relevance signal](https://developers.google.com/search/docs/crawling-indexing/links-crawlable), and anchor text provides information about the page being linked to.
    “Googlebombs” were an extreme illustration: coordinated links could associate a target page with an obscure or meaningless phrase, even when that phrase was not visible on the target page, although Google [introduced changes in 2007 to reduce their effect](https://developers.google.com/search/blog/2007/01/quick-word-about-googlebombs).
    The absence of a visible query term on the current page therefore does not by itself distinguish term dropping, semantic matching or lexical matching against older or off-page indexed evidence.
    See also Google’s guidance on [recrawling and reindexing](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl).

[^according-to-some-reports-google-s-rankbrain-int]: Google’s own [guide to Google Search ranking systems](https://developers.google.com/search/docs/appearance/ranking-systems-guide) lists RankBrain, neural matching and BERT as separate AI systems used in ranking.
    RankBrain was introduced in 2015, four years before BERT, so machine-learning components were part of ranking well before the transformer era.[]{.backref-space}

[^scite-lexical-suggestive]: We cannot tell from the screenshot whether Scite is using only lexical retrieval.
    Highlighting the words that matched is suggestive that lexical evidence contributes somewhere in the pipeline, because a conventional pooled dense bi-encoder does not itself require or expose exact word matches.
    It is not conclusive, however.
    Highlighting can be added separately after retrieval, and neural methods can also preserve inspectable word-level evidence: [ColBERT-style late interaction](https://doi.org/10.1145/3397271.3401075) scores contextualised token alignments, while [learnt sparse retrieval such as SPLADE](https://doi.org/10.1145/3404835.3463098) produces vocabulary-aligned weights.
    Scite could therefore still use dense retrieval, a hybrid lexical–dense system or a multi-stage pipeline.
