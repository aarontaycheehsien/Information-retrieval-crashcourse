# Chapters 2–12: recommendations for plainer prose

Reviewed: 18 October 2026 (Singapore).

**Purpose.** Turn the eleven existing AI-style reviews into specific editorial changes that make the chapters sound less formulaic and more like a librarian explaining how retrieval works. The request is interpreted as reducing “AI/Claude speak”, consistent with the supplied reviews. These are stylistic judgements, not evidence of authorship.

**Source checked.** `fable-1` at commit [`2343676f8136ecd7b6445c96ca0e0077159384d4`](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/commit/2343676f8136ecd7b6445c96ca0e0077159384d4); `search-textbook.html` blob `ec83886289897c795d42d7020c5e2299d5c16beb`. The textbook blob is unchanged from the snapshot named in the earlier reviews. Source links below are pinned to this commit.

**Status.** Recommendations only. The textbook, illustrations, exercises, citations and original review records have not been edited. Every flagged entry in the eleven reviews has a corresponding numbered recommendation below. Some entries concern the same paragraph and should be implemented together, not as successive independent replacements.

## Editorial approach

- Start with the mechanism, example or observation. Remove sentences that merely announce importance, sophistication or a forthcoming revelation.
- Reduce repeated slogans and conclusions. Keep necessary contrasts such as candidate retrieval versus reranking and similarity scores versus relevance judgements.
- Preserve the author’s concrete library examples, first-person experiments and useful teaching guidance. Use plain verbs without making the prose uniformly clipped or impersonal.
- Keep uncertainty, dates and citations. Several recommendations also narrow overstatements; these are identified in the relevant entries and are not claims of newly verified product behaviour.
- Retain UK spelling and existing technical terminology. Keep HTML anchors when changing headings, and retain figure links and attribution when changing captions.

## Chapter index

| Chapter | Flagged entries addressed | Main change |
|---|---:|---|
| [2. Boolean admission and the inverted index](#chapter-2) | 10 | Remove repeated ranking transitions. |
| [3. BM25 and ranked lexical retrieval](#chapter-3) | 15 | Replace historical reassurance with the documented examples. |
| [4. Lexical search beyond strict Boolean](#chapter-4) | 19 | Cut dramatic framing around lexical/Boolean distinctions. |
| [5. Embeddings: what the learnt geometry encodes](#chapter-5) | 17 | Keep learning guidance; simplify coaching and metaphors. |
| [6. From language model to retrieval encoder](#chapter-6) | 13 | Explain training and pooling directly. |
| [7. Dense retrieval at collection scale](#chapter-7) | 17 | Name operations and preserve uncertainty about product behaviour. |
| [8. Representations and indexed units](#chapter-8) | 15 | Keep representation distinctions; remove abstract slogans. |
| [9. Reranking and multi-stage retrieval](#chapter-9) | 16 | Explain candidate limits once, then demonstrate them. |
| [10. Hybrid retrieval and rank fusion](#chapter-10) | 15 | Focus on fusion, scores, cut-offs and route selection. |
| [11. Understanding, transforming and routing queries](#chapter-11) | 15 | Name query objects and mechanisms; remove door metaphors. |
| [12. Agentic search](#chapter-12) | 22 | Describe observable control and recovery without overclaiming. |

**Total: 174 review entries addressed.**

Read the “Original” passages as locators. They reproduce the review’s wording, which sometimes combines separate phrases. “Delete” means remove the specified prose while preserving adjoining evidence and links. A replacement of a whole paragraph takes precedence over changes to individual phrases in that paragraph.

<a id="chapter-2"></a>

## Chapter 2: Boolean admission and the inverted index

Original review: [chapter-2-ai-phrasing-review.md](chapter-2-ai-phrasing-review.md).

Reduce the repeated eligibility-versus-ranking explanation. Keep the inverted-index examples and the distinction between processed terms and visible text. The summary should recap those mechanisms without dismissing large result sets, which can be appropriate for evidence synthesis.

### 2.1 — Delete and join

**Original** ([source, line 1379](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1379)): “This is not a historical curiosity.”

**Recommendation:** Delete the opening sentence. Begin the paragraph: “Boolean logic underlies the advanced-search interfaces librarians use most: PubMed’s Advanced Search with its search-history builder and MeSH terms, Web of Science Advanced Search with its field tags, and the equivalent screens in Scopus, EBSCOhost and Ovid.” Keep the systematic-review explanation and its links.

### 2.2 — Delete duplicate

**Original** ([source, line 1382](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1382)): “Boolean decides who gets into the competition. Ranking decides who finishes first.”

**Recommendation:** Remove this pull quote. The preceding paragraph already explains that Boolean logic supplies no ranking rule. If a standalone teaching cue is needed, use “Boolean conditions determine which records qualify; a ranking method orders those records.” Use that explanation once, rather than retaining both versions.

### 2.3 — Delete

**Original** ([source, line 1402](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1402)): “The admission decision is now clear, but the ordering problem is still open.”

**Recommendation:** Remove the sentence. The next heading introduces the inverted index, so an announcement about the unresolved ordering problem interrupts the sequence.

### 2.4 — Replace

**Original** ([source, line 1523](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1523)): “Text is not searched; analysed terms are.”

**Recommendation:** “In this lexical index, matching uses the terms produced by text analysis.” This scopes the claim to the mechanism being taught.

### 2.5 — Replace

**Original** ([source, line 1523](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1523)): “An eligible set of forty thousand records is not a result list anyone can use. The next chapter asks what has to be added to turn matching into ranking.”

**Recommendation:** “A large matching set can be difficult to browse. Chapter 3 explains how a lexical ranking method orders the matching records.” Avoid claiming that nobody can use a large result set.

### 2.6 — Replace

**Original** ([source, line 1522](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1522)): “The inverted index gets us quickly to the eligible set. But if several records pass, the posting lists do not inherently say which one deserves first place. What is missing is a graded ranking rule.”

**Recommendation:** “The posting lists identify matching records. To order those records by estimated relevance, the system also needs a scoring rule.” Keep this at the end of the explanation and remove the duplicate sentence “Nothing in the mechanism says which eligible record should appear first” from the following summary.

### 2.7 — Replace

**Original** ([source, line 1378](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1378)): “This does not make Boolean retrieval inferior: explicit eligibility rules remain valuable when a task requires inspectable, reproducible control over who may enter the result set.”

**Recommendation:** “Boolean conditions let a searcher specify and inspect the rules for including records, then rerun the same strategy.” This retains the practical value without implying that rerunning always reproduces an identical result set.

### 2.8 — Keep, optionally simplify

**Original** ([source, line 1426](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1426)): “Text becomes tokens; analysis turns selected tokens into searchable terms.”

**Recommendation:** This is a useful caption-sized recap of a process. It need not be removed merely because it is balanced. If retained, write “Tokenisation divides text into units; further analysis determines which terms enter the index.” Do not repeat it again in the next paragraph.

### 2.9 — Replace

**Original** ([source, line 1438](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1438)): “Lemmatisation uses more linguistic information than stemming, but it is not automatically correct, semantic or superior for every collection.”

**Recommendation:** “Lemmatisation uses grammatical information to choose a base form. An incorrect interpretation can still produce a poor match, so it needs testing on the collection.” Keep the preceding stemming examples and precision/recall explanation.

### 2.10 — Replace

**Original** ([source, line 1506](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1506)): “That is a question about coverage. FTS is a description of a search capability.”

**Recommendation:** “Here, ‘full text’ concerns how much of the publication is covered, whereas ‘full-text search’ names a way of searching text fields.” Keep the following titles-and-abstracts example; it makes the distinction concrete.


<a id="chapter-3"></a>

## Chapter 3: BM25 and ranked lexical retrieval

Original review: [chapter-3-ai-phrasing-review.md](chapter-3-ai-phrasing-review.md).

Remove the three versions of “this is not history” and let the documented product examples establish practical relevance. Retain the probabilistic-history caveat and the warning against treating a BM25 score as a probability.

### 3.1 — Delete duplicate

**Original** ([source, line 1524](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1524)): “The ranking is added; the index is not replaced.”

**Recommendation:** Remove the sentence. The preceding sentence already says that BM25 uses the same inverted index. Keep the fuller explanation later in the chapter.

### 3.2 — Delete

**Original** ([source, line 1536](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1536)): “It is also, quietly, one of the most consequential algorithms a librarian never sees named.”

**Recommendation:** Remove this sentence and begin with the existing concrete claim about Lucene’s default text-scoring model, keeping its citation.

### 3.3 — Delete fragment

**Original** ([source, line 1537](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1537)): “no shared term, no evidence.”

**Recommendation:** Delete “: no shared term, no evidence”. End the preceding sentence after “share”. The explanation is already complete.

### 3.4 — Replace lead-in

**Original** ([source, line 1537](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1537)): “A caution for the historically minded”

**Recommendation:** Replace “A caution for the historically minded:” with “Historically,” and retain the explanation that BM25 developed within probabilistic retrieval research.

### 3.5 — Replace

**Original** ([source, line 1537](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1537)): “the resemblance is convergent, not genealogical.”

**Recommendation:** Replace the historical aside as a whole with “BM25 developed within the probabilistic relevance tradition, independently of TF-IDF, although the two use some similar signals.” Retain citation 5. This implements the preceding entry too.

### 3.6 — Replace paragraph

**Original** ([source, line 1538](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1538)): “But it is not relevance, and it is not a probability of relevance—it is lexical evidence, added up.”

**Recommendation:** “BM25 combines weighted term matches into a score used to rank candidates. The score is neither a probability of relevance nor a direct judgement of whether the record meets the reader’s need.” The contrast is technically necessary; remove the theatrical delivery, not the caveat.

### 3.7 — Replace

**Original** ([source, line 1546](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1546)): “What makes BM25 BM25 is how it answers the last two”

**Recommendation:** “BM25 specifies a particular way to combine term-frequency saturation with document-length normalisation.” Keep the preceding sentence acknowledging TF-IDF variants, and retain the parameter definitions and defaults.

### 3.8 — Delete

**Original** ([source, line 1546](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1546)): “A librarian inspecting a search engine’s ranking configuration will meet these two letters.”

**Recommendation:** Remove the final sentence. The definitions of k₁ and b already explain what a librarian needs to recognise in a configuration.

### 3.9 — Delete lead-in

**Original** ([source, line 1570](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1570)): “Try it: the formula is easier to understand when you can interfere with it.”

**Recommendation:** Delete the first sentence. Start with “The BM25 Evidence Lab lets you change one source of evidence at a time”. Retain the activities, time estimates and reassurance that the equation is not required.

### 3.10 — Delete lead-in

**Original** ([source, line 1574](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1574)): “None of this is textbook history.”

**Recommendation:** Delete “None of this is textbook history.” Let the existing next sentence introduce the documented academic-search examples.

### 3.11 — Delete lead-in

**Original** ([source, line 1581](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1581)): “The TF-IDF intuition is not textbook history.”

**Recommendation:** Delete the first sentence of the caption. Start with “Scholarly products describe live ranking pipelines”. Keep the signals listed in the caption.

### 3.12 — Delete duplicate

**Original** ([source, line 1583](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1583)): “A production ranking pipeline should not be reduced to one formula.”

**Recommendation:** Remove this sentence from the caption. The preceding PubMed discussion already explains the combination of BM25 and later ranking stages. Retain the caption’s description of the screenshot and its attribution.

### 3.13 — Replace clause

**Original** ([source, line 1610](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1610)): “they do not turn BM25 into semantic retrieval.”

**Recommendation:** Replace the semicolon and final corrective clause with “ while preserving BM25’s term-based scoring.” Keep the explanation of compression, bounds and pruning.

### 3.14 — Delete duplicate

**Original** ([source, line 1612](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1612)): “BM25 is not a historical curiosity.”

**Recommendation:** Delete “BM25 is not a historical curiosity.” Retain the specific summary sentence about PubMed and other academic systems.

### 3.15 — Replace

**Original** ([source, line 1612](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1612)): “Ranking changes what a result list looks like. It also changes what happens to a query term the system cannot match at all—and that is where the central misconception of this book begins.”

**Recommendation:** “Chapter 4 examines lexical searches in which some query terms are optional, including what happens when a term matches no record.” This identifies the next topic without wrongly making optionality a consequence of ranking alone.


<a id="chapter-4"></a>

## Chapter 4: Lexical search beyond strict Boolean

Original review: [chapter-4-ai-style-review.md](chapter-4-ai-style-review.md).

This chapter needs the largest reduction in rhetorical framing. Preserve the distinction between lexical evidence, Boolean conditions, ranking and output depth. Keep the worked examples and Figures 4.1–4.5; shorten the narration around them. Treat the interface examples as observations with several possible explanations.

### 4.1 — Replace surrounding opening

**Original** ([source, line 1613](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1613)): “That inference is wrong, and correcting it is the most important thing this book does early.”

**Recommendation:** Replace the sentence and “Here is the correction in one sentence:” with “A lexical system can return a record that lacks one of the query terms.” Follow with “It may require every term, some terms, or any one matching term, while still using term matches to calculate scores.” This removes self-praise and states the mechanism.

### 4.2 — Replace

**Original** ([source, line 1613](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1613)): “The third stays open, on purpose: by the end you will see why no amount of squinting at the screen could ever settle it.”

**Recommendation:** “The Semantic Scholar example also requires evidence about the retrieval pipeline, which is examined in Chapter 7.” Keep the purpose of the later discussion without withholding an answer for suspense.

### 4.3 — Replace

**Original** ([source, line 1614](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1614)): “Boolean uses words as gates, BM25 uses words as weights.”

**Recommendation:** “Boolean conditions determine whether a record qualifies. BM25 assigns a score from its matching terms.” Keep the following paragraph explaining that the two can be used together.

### 4.4 — Replace paragraph ending

**Original** ([source, line 1615](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1615)): “That arrangement is common, but it is a choice, not a law.”

**Recommendation:** After the existing description of Boolean filtering followed by ranking, write “Other lexical arrangements make some query terms optional.” This leads directly to the examples.

### 4.5 — Delete lead-in

**Original** ([source, line 1620](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1620)): “But here is the trap:”

**Recommendation:** Delete “But here is the trap:”. Start the sentence “A relevance-ranked result list can look similar under different admission rules.” “Similar” avoids an unnecessary claim that the lists must look exactly identical.

### 4.6 — Delete duplicate

**Original** ([source, line 1627](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1627)): “Same analysed terms. Same inverted index. Different rules for admission and scoring.”

**Recommendation:** Remove this pull quote. The three-item list and Figure 4.1 already demonstrate that the same index supports different rules. If a caption needs a short introduction, use “The three examples use the same terms and index, with different matching requirements.”

### 4.7 — Replace

**Original** ([source, line 1653](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1653)): “The lesson is narrow but important:”

**Recommendation:** “Non-Boolean behaviour alone does not identify the retrieval method.” Keep the historical evidence and citations before it; the rest of the chapter supplies the alternatives.

### 4.8 — Delete bridge

**Original** ([source, line 1663](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1663)): “But the bad term does not become harmless; it changes jobs.”

**Recommendation:** Delete “But the bad term does not become harmless; it changes jobs.” The following sentence about BM25 and the rarity of foolish supplies the mechanism.

### 4.9 — Replace whole paragraph

**Original** ([source, line 1663](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1663)): “The bad term stops deciding who competes and starts distorting who wins.”

**Recommendation:** “Under any-match BM25, a record can remain eligible through its other matching terms. The added term foolish can still change the ranking: if it is rare in the collection, its high IDF can increase the scores of records containing it, even though it poorly represents the searcher’s need. The Evidence Lab demonstrates the effect.” This also implements the preceding entry and avoids asserting that the ranking must change in every case.

### 4.10 — Replace paragraph

**Original** ([source, line 1679](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1679)): “Good retrieval over a bad representation is still a bad search.”

**Recommendation:** “Both systems handled the query as designed. The poor results arose because foolish was a weak representation of the searcher’s need.” Remove the final slogan and keep the connection to query formulation.

### 4.11 — Replace

**Original** ([source, line 1700](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1700)): “Four stories, one screen—and the screen looks identical under all of them.”

**Recommendation:** “The visible result is consistent with all four explanations, and several may operate in the same search.” Retain the following example of combined analysis and optional terms, but avoid restating the same point twice.

### 4.12 — Replace ending

**Original** ([source, line 1700](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1700)): “the question is not hard, it is undecidable from the evidence the interface provides.”

**Recommendation:** “The scite screenshot alone does not show which explanation applies.” Use this after the combined-mechanisms example. It is an evidential limit, not mathematical undecidability.

### 4.13 — Replace

**Original** ([source, line 1715](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1715)): “understanding is what the system concludes, transformation is what it does about it”

**Recommendation:** “Query understanding interprets the request; query transformation changes the input sent to retrieval.” This is a useful technical contrast and can remain concise.

### 4.14 — Replace following explanation

**Original** ([source, line 1715](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1715)): “And note what transformation is not: query transformation is not a kind of retrieval.”

**Recommendation:** “The transformed input is then passed to a retriever, which may use Boolean conditions, BM25 or another method.” Remove “And note what transformation is not”.

### 4.15 — Replace

**Original** ([source, line 1715](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1715)): “A system can rewrite your query with a large language model and still search with 1970s mathematics.”

**Recommendation:** “An LLM can therefore rewrite a query that is subsequently processed by Boolean or BM25 retrieval.” The preceding two recommendations and this one should be combined into one short paragraph, retaining the interpretation-versus-transformation distinction.

### 4.16 — Replace

**Original** ([source, line 1750](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1750)): “Chapter 1 named three temptations and left them standing until you had watched a lexical system behave. Two of the three fall here, settled by ordinary lexical retrieval with no appeal to meaning at all.”

**Recommendation:** “The scite and Google Scholar examples can be explained using the distinctions introduced in Part I.” Follow with the specific observations; do not imply that either product’s architecture has been established from its result screen.

### 4.17 — Replace first sentence

**Original** ([source, line 1757](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1757)): “The second puzzle points the same way, though it settles into an observation rather than a confusion worth naming.”

**Recommendation:** “The Google Scholar example separates the reported match count from the number of results a user can view.” Keep the explanation of admission, ranking and output limits, with the product name explicit so the reader need not recall “the second puzzle”.

### 4.18 — Delete and simplify

**Original** ([source, line 1758](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1758)): “That is the finding, not a shortfall.”

**Recommendation:** Delete “That is the finding, not a shortfall.” Rewrite the preceding sentence as “These observations do not establish the products’ retrieval architectures.”

### 4.19 — Delete coda

**Original** ([source, line 1760](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1760)): “Related claims, but not the same claim.”

**Recommendation:** Delete “Related claims, but not the same claim.” Retain the two explicit distinctions about semantic search and vector representations.


<a id="chapter-5"></a>

## Chapter 5: Embeddings: what the learnt geometry encodes

Original review: [chapter-5-ai-style-review.md](chapter-5-ai-style-review.md).

Keep the orientation box: this chapter introduces unfamiliar concepts to Boolean-trained readers. Replace its coaching voice with clear learning priorities. Explain Word2Vec, contextualisation and pretraining through their mechanisms; do not replace the existing demonstrations with more abstractions.

### 5.1 — Replace roadmap sentence

**Original** ([source, line 1778](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1778)): “This chapter builds that encoder in three moves”

**Recommendation:** “The chapter introduces word vectors, shows how representations can depend on context, and explains how training shapes those representations.” Avoid implying that the chapter constructs or trains an encoder.

### 5.2 — Delete reassurance, retain guidance

**Original** ([source, line 1781](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1781)): “If it feels harder than what came before, that is the material and not you.”

**Recommendation:** Delete the flagged sentence. Retain the explanation that this chapter introduces more new vocabulary, followed by the learning priorities below.

### 5.3 — Replace lead-in

**Original** ([source, line 1782](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1782)): “It is worth knowing in advance what has to survive the chapter and what does not. Three things to carry forward:”

**Recommendation:** “The later chapters rely on three ideas:” Keep the existing three-item list.

### 5.4 — Replace paragraph

**Original** ([source, line 1788](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1788)): “What you can read once and let go:”

**Recommendation:** “The Word2Vec prediction examples, the king − man + woman calculation, and the comparison of masked and next-token prediction explain how training works. You will not need to reproduce those details in later chapters.” Preserve the distinction between core learning and optional detail.

### 5.5 — Replace lead-in

**Original** ([source, line 1796](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1796)): “The three terms nest, and the nesting is the part worth holding on to”

**Recommendation:** Replace “The three terms nest, and the nesting is the part worth holding on to:” with “In this book,” and continue with the existing relationship between embeddings, vectors and representations. Retain the BM25 example and the qualification “in this book”.

### 5.6 — Replace question

**Original** ([source, line 1805](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1805)): “The question that has to be settled before any of this can begin is therefore an awkwardly practical one: what target can a body of text supply for itself?”

**Recommendation:** “How can text provide the target examples needed for training?” Keep the preceding explanation of predictions, targets and parameter updates.

### 5.7 — Delete bridge

**Original** ([source, line 1806](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1806)): “Its value here is that it replaces an unanswerable question with an answerable one.”

**Recommendation:** Delete this sentence. The following explanation of predicting neighbouring words already shows how text supplies training targets.

### 5.8 — Replace caption opening

**Original** ([source, line 1810](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1810)): “The substitution in the second panel is the whole move: a question no one can answer at scale is exchanged for one the text answers by itself”

**Recommendation:** “Predicting a word from its context provides a training target available in the text itself, without manual labels.” Retain the full-resolution link and any attribution.

### 5.9 — Replace caption

**Original** ([source, line 1816](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1816)): “CBOW and Skip-gram are the two arrangements of the same bargain, and the fourth stage is the part that matters here”

**Recommendation:** “CBOW predicts a target word from its neighbours; Skip-gram predicts neighbouring words from a target word. After training, the learnt word vectors can be reused without the prediction machinery. The Illustrated Word2Vec explains the prediction step in more detail.” Retain the existing external and full-resolution links.

### 5.10 — Delete sentence, keep qualification

**Original** ([source, line 1833](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1833)): “‘Appear to’ is the right strength of claim.”

**Recommendation:** Delete “ ‘Appear to’ is the right strength of claim.” Keep the explanation that the model was trained to predict co-occurrence and that the demonstrated relationships are not guaranteed, with citation 15.

### 5.11 — Replace concluding explanation

**Original** ([source, line 1833](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1833)): “What the demonstrations establish for retrieval is narrower, and more useful, than the arithmetic suggests”

**Recommendation:** “Predicting word co-occurrence can produce vectors that capture useful relationships between words. Retrieval models require training and evaluation for the query–document comparisons they will make.” Use this after the existing caveat and in place of both the “narrower, and more useful” sentence and the final “bet” sentence.

### 5.12 — Delete duplicate

**Original** ([source, line 1833](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1833)): “That is the bet dense retrieval makes.”

**Recommendation:** Delete this sentence as part of the preceding replacement. The link from language-model training to retrieval remains explicit.

### 5.13 — Replace opening

**Original** ([source, line 1839](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1839)): “Self-attention describes how a model reads. It says nothing about what the model was scored on while it was learning to read that way, and that is the other half of the account.”

**Recommendation:** “Self-attention lets a model combine information from tokens in a sequence. The training objective specifies what it must predict, and helps determine which representations it learns.” Retain the explanation of pretraining that follows.

### 5.14 — Replace and qualify

**Original** ([source, line 1840](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1840)): “Only the shape of the blank differs.”

**Recommendation:** “These objectives differ in what is predicted and which context is available.” Also replace the nearby blanket description of Word2Vec hiding a word with “CBOW predicts a word from surrounding words; Skip-gram predicts surrounding words from a target word.” Keep the separate BERT and GPT descriptions. The original wording should not imply that all Word2Vec training is CBOW.

### 5.15 — Delete lead-in

**Original** ([source, line 1917](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1917)): “The difference between the second shape and the third is not an implementation detail.”

**Recommendation:** Delete the flagged sentence. Begin directly with the explanation that masked-token prediction can use both left and right context, whereas next-token prediction uses preceding context. Retain the Appendix A link; avoid suggesting this difference alone explains every encoder/decoder application.

### 5.16 — Replace

**Original** ([source, line 1923](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1923)): “Contextualisation supplies information a model could use. Task training decides what it becomes good at.”

**Recommendation:** “A contextual representation incorporates the surrounding text. Further training adapts it to tasks such as comparing a query with a relevant passage.” This states the relationship without making training sound like a conscious decision.

### 5.17 — Replace transition

**Original** ([source, line 1925](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1925)): “The encoder now exists, but it is not yet retrieval infrastructure.”

**Recommendation:** “Chapter 6 explains how a contextual encoder can be trained to produce query and document vectors suitable for retrieval.” The chapter reference and its practical purpose are sufficient.


<a id="chapter-6"></a>

## Chapter 6: From language model to retrieval encoder

Original review: [chapter-6-ai-style-review.md](chapter-6-ai-style-review.md).

Make training, pooling and relevance labels concrete. Preserve the warning that labels reflect a task and that domain transfer can fail. Do not imply that retrieval training guarantees useful embeddings or that citations directly measure relevance.

### 6.1 — Replace

**Original** ([source, line 1938](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1938)): “Only then can the resulting vectors become retrieval infrastructure that a collection-scale index can use.”

**Recommendation:** “Training on these comparisons aims to make relevant passages score above misleading alternatives when their vectors are compared.” This describes the intended effect without treating training as a guarantee or a universal prerequisite for indexing vectors.

### 6.2 — Replace caption clause

**Original** ([source, line 1956](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1956)): “pooling is where the per-token detail is spent—which is what late interaction later declines to do.”

**Recommendation:** Replace the clause beginning “pooling is where” with “pooling combines token representations into one vector; late-interaction methods retain multiple token vectors for comparison.” Keep the distinction between model tokens and lexical index terms.

### 6.3 — Replace both sentences

**Original** ([source, line 1961](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1961)): “It is tempting to say that dense embeddings represent ‘meaning’.” / “That is useful shorthand, but it leaves out the most important question: meaning for what task?”

**Recommendation:** “What an embedding captures depends partly on the task used to train it. For retrieval, training should favour the query–document relationships the system needs to recognise.”

### 6.4 — Replace

**Original** ([source, line 1963](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1963)): “The important step in both cases is not simply using BERT, but training the independently produced representations for the comparison the system needs to make.”

**Recommendation:** “Both approaches train independently encoded representations so that their similarity scores are useful for the intended task.” Keep the preceding SBERT and DPR descriptions and citations; their training tasks are not identical.

### 6.5 — Replace clause

**Original** ([source, line 1986](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1986)): “which is why the label here is stipulated rather than derived.”

**Recommendation:** Replace “which is why the label here is stipulated rather than derived” with “so this example assigns the label for the stated information need”. Retain the alternative interpretation of the need.

### 6.6 — Delete lead-in

**Original** ([source, line 1995](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1995)): “Where the training data came from matters as much as what it taught.”

**Recommendation:** Delete the sentence. Begin with “Training pairs are drawn from a particular literature, genre and style of question”. The following examples explain why this affects transfer.

### 6.7 — Replace or omit

**Original** ([source, line 1995](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1995)): “The same architecture, trained on different material, becomes a different retriever.”

**Recommendation:** If a closing sentence is needed, use “Changing the training examples can change which records the model ranks highly, even with the same architecture.” Otherwise omit it: the paragraph already demonstrates the point.

### 6.8 — Replace lead-in

**Original** ([source, line 1996](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1996)): “It can also be a trap:”

**Recommendation:** Replace “It can also be a trap:” with “However,” and retain the explanation of poor transfer to another collection or task.

### 6.9 — Delete phrase

**Original** ([source, line 1996](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1996)): “once the whole pipeline is in view.”

**Recommendation:** Delete “once the whole pipeline is in view”. Keep the direct cross-reference to Chapter 13’s discussion of out-of-distribution transfer.

### 6.10 — Replace

**Original** ([source, line 1997](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L1997)): “‘Positive’ and ‘negative’ are training labels, not universal truths.”

**Recommendation:** “A positive or negative label records how a training example was classified for a particular task.” Retain the footnote and the nearby explanation of noisy or incomplete labels.

### 6.11 — Replace

**Original** ([source, line 2000](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2000)): “Every retrieval embedding space embodies an operational model of relevance”

**Recommendation:** “The training data and objective influence which query–document relationships a retrieval model scores highly.” Keep the next sentence about clicks, answer pairs and citations as proxies. Use the same concrete formulation in the summary.

### 6.12 — Delete transition

**Original** ([source, line 2001](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2001)): “That is an encoder, not yet a retrieval system.”

**Recommendation:** Delete “That is an encoder, not yet a retrieval system.” The next sentence can name the additional components without staging a correction.

### 6.13 — Replace

**Original** ([source, line 2001](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2001)): “The next two chapters put one to work against a whole collection and then open the stored representation itself, resolving both distinctions promised in Chapter 4”

**Recommendation:** “Chapter 7 explains collection-scale search over these vectors. Chapter 8 examines how representations and indexed units differ.” Keep the two conceptual distinctions elsewhere in the summary, rather than repeating them as promises to be resolved.


<a id="chapter-7"></a>

## Chapter 7: Dense retrieval at collection scale

Original review: [chapter-7-ai-phrasing-review.md](chapter-7-ai-phrasing-review.md).

Concentrate on what is stored, what is compared and what limits the returned set. Preserve the distinction between similarity scores and relevance, and keep the date and uncertainty attached to the Semantic Scholar observations.

### 7.1 — Delete

**Original** ([source, line 2007](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2007)): “This chapter deploys that encoder.”

**Recommendation:** Delete this sentence. The following sentence already introduces storage, comparison, nearest-neighbour indexing and top-k.

### 7.2 — Replace

**Original** ([source, line 2007](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2007)): “The second—that a vector need not be dense, learnt or semantic—is the next chapter’s opening business.”

**Recommendation:** “Chapter 8 examines sparse and dense representations, including vectors calculated without learning.” This replaces the “opening business” phrasing without another formal promise.

### 7.3 — Replace caption opening

**Original** ([source, line 2022](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2022)): “Human vision stops at three spatial dimensions; the arithmetic does not.”

**Recommendation:** “The same vector operations extend from two or three coordinates to n coordinates.” Keep the coordinate examples and the warning that the toy axes have no semantic labels.

### 7.4 — Replace

**Original** ([source, line 2030](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2030)): “The word semantic does not tell us which one, or where in the pipeline meaning enters.”

**Recommendation:** “The label ‘semantic’ does not identify which of these components the product uses or at which stage.” The preceding examples supply the detail.

### 7.5 — Delete setup

**Original** ([source, line 2044](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2044)): “Encoding each passage before any query arrives buys one thing and costs another.”

**Recommendation:** Delete this sentence. Let the following paragraphs name the benefit of precomputing passage vectors and the compression cost directly.

### 7.6 — Replace

**Original** ([source, line 2064](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2064)): “Topic, named entities, claims, qualifications and terminology are all squeezed into one point before the passage knows which query will arrive.”

**Recommendation:** “A single vector represents the passage’s topics, entities and qualifications without being tailored to the incoming query.” Retain the following examples of details that pooling may lose.

### 7.7 — Replace

**Original** ([source, line 2079](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2079)): “Nearest means best available, not necessarily relevant.”

**Recommendation:** “Even the closest stored vectors may correspond to irrelevant records.” Place this beside the explanation of nearest-neighbour results; it need not be a standalone pull quote.

### 7.8 — Replace

**Original** ([source, line 2129](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2129)): “k says how many leaders were requested—not who could compete, how relevance was calculated or how much work was done.”

**Recommendation:** “k specifies the requested result count. It does not identify the candidate-selection rule, scoring method or search cost.” Retain this distinction, but use “records” rather than “leaders” elsewhere in the paragraph.

### 7.9 — Delete lead-in

**Original** ([source, line 2134](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2134)): “Puzzle 3 set a name against two result counts and an inspection of search quality.”

**Recommendation:** Delete the first sentence. Start with the existing Semantic Scholar example, preserving the August 2026 date, both queries and both reported result counts.

### 7.10 — Replace, merge caveats

**Original** ([source, line 2138](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2138)): “This is the strongest documented explanation for why the dense-retrieval intuition is unsafe, but it is not proof of the exact August 2026 cause.”

**Recommendation:** Replace this sentence and the following sentence with “The 2025 account documents keyword candidate retrieval, but it does not establish how the August 2026 interface processed these two queries.” Retain the separate observations about result quality and the warning against generalising to all questions.

### 7.11 — Replace

**Original** ([source, line 2140](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2140)): “OpenAlex Alice semantic search supplies a deliberately stark contrast in which the documentation does identify dense first-stage retrieval.”

**Recommendation:** “OpenAlex’s documentation describes dense first-stage retrieval for Alice semantic search.” Retain the documented date and steps that follow.

### 7.12 — Replace pull quote

**Original** ([source, line 2156](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2156)): “The search box tells you how the user can express the query. ‘Semantic search’ tells you what kind of matching the system aspires to provide. Dense retrieval, lexical retrieval and reranking tell you how particular stages may actually do the work.”

**Recommendation:** “A natural-language input box and the label ‘semantic search’ do not identify the retrieval method. To establish that, inspect how the product forms candidates and ranks them.” Avoid repeating this as another closing slogan if the same point remains in the summary.

### 7.13 — Replace

**Original** ([source, line 2157](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2157)): “Similarity is a comparison rule applied to stored vectors, not a verdict about them.”

**Recommendation:** “Cosine similarity and dot product assign scores to pairs of vectors.” Keep the following explanation of direction, length and differing rankings; retain the relevance caveat in its earlier, fuller location.

### 7.14 — Replace transition

**Original** ([source, line 2157](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2157)): “Both routes compared stored representations without ever asking what one of those representations contains, or what a single stored item stands for in the collection a reader believes they are searching. The next chapter opens the stored object itself.”

**Recommendation:** “Chapter 8 examines what the vectors represent and whether each indexed item is a whole document, a record or a passage.” This is enough to connect the chapters.

### 7.15 — Delete duplicate

**Original** ([source, line 2007](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2007)): “That is not yet a search system.”

**Recommendation:** Delete “That is not yet a search system.” The following sentence already explains that large-scale storage, comparison and result selection are still needed.

### 7.16 — Replace

**Original** ([source, line 2024](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2024)): “The resulting number is meaningful only within the representation and comparison rule that produced it.”

**Recommendation:** “Interpret a similarity score using the model and comparison rule that produced it.” Keep the following warning that scores need not be comparable across models or searches and are not calibrated relevance probabilities.

### 7.17 — Delete lead-in

**Original** ([source, line 2139](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2139)): “The point is not that Semantic Scholar lacks semantic capabilities.”

**Recommendation:** Delete the first sentence. Begin “The platform also uses SPECTER embeddings for author disambiguation and recommendations.” Preserve the distinction between these applications and candidate retrieval in the main search.


<a id="chapter-8"></a>

## Chapter 8: Representations and indexed units

Original review: [chapter-8-ai-style-review.md](chapter-8-ai-style-review.md).

Keep the four representation questions and the distinction between documents, indexed units and displayed results. These are useful teaching structures. Replace claims about what density “decides” with explicit statements about what it does and does not describe.

### 8.1 — Replace

**Original** ([source, line 2158](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2158)): “Both are load-bearing: a claim about what a search system can find is really a claim about what was stored and how finely it was cut up.”

**Recommendation:** “What a retrieval stage can match depends on the indexed text, how it is divided into units and how those units are represented.” This states the dependency without suggesting that storage alone determines everything a system can find.

### 8.2 — Replace preview

**Original** ([source, line 2158](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2158)): “It then separates the source document from the indexed unit, the indexed unit from its representation, and both from the result a reader is finally shown.”

**Recommendation:** “The chapter also distinguishes a source document from its searchable units and explains how matches from those units become displayed results.” Keep the detailed distinctions in the relevant section.

### 8.3 — Delete

**Original** ([source, line 2211](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2211)): “That is the contrast the next figure draws.”

**Recommendation:** Remove this sentence. The following figure and its caption supply the comparison.

### 8.4 — Replace heading

**Original** ([source, line 2217](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2217)): “Now separate four questions that are often collapsed”

**Recommendation:** “Four questions about a representation”. Preserve the existing HTML anchor if the heading is later edited, so links continue to work.

### 8.5 — Replace

**Original** ([source, line 2220](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2220)): “This describes shape, not quality or meaning.”

**Recommendation:** “Sparse and dense describe how many dimensions are active. They do not, by themselves, establish retrieval quality or semantic capability.” This preserves a necessary distinction in plain language.

### 8.6 — Delete lead-in

**Original** ([source, line 2232](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2232)): “The converse is also possible, and it is the case the four questions were separated for.”

**Recommendation:** Delete the first sentence. Start with the existing explanation that a sparse, vocabulary-aligned representation can be produced by a learnt mapping.

### 8.7 — Replace opening pair

**Original** ([source, line 2234](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2234)): “What the two share is the shape: sparse, and aligned to a named vocabulary. What changes is where the value comes from.”

**Recommendation:** “BM25 and learnt sparse models both use sparse, vocabulary-aligned representations, but calculate their weights differently.” Keep the following explanation of counts, predicted weights and sparsity penalties.

### 8.8 — Delete

**Original** ([source, line 2241](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2241)): “Knowing only its density would have predicted none of this.”

**Recommendation:** Remove the sentence. The preceding comparison has already demonstrated that density, learning and semantic capability are distinct properties.

### 8.9 — Replace cross-reference

**Original** ([source, line 2241](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2241)): “what that buys a pipeline is taken up in Chapter 9, just before hybrid retrieval, and what the expansion costs at query time is worked through in Appendix C.”

**Recommendation:** “Chapter 9 discusses the use of learnt sparse retrieval in a pipeline; Appendix C explains the query-time cost of expansion.” Keep both links.

### 8.10 — Delete takeaway

**Original** ([source, line 2259](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2259)): “Here the lesson is simply: the representation supplies the evidence, the comparison rule supplies a score, and the retrieval rule decides how the score is used.”

**Recommendation:** Delete this sentence. The paragraph already explains that dot product and cosine can compare different representations. Retain the worked-example links.

### 8.11 — Delete lead-in

**Original** ([source, line 2282](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2282)): “This is not a theoretical distinction, and current products sit at very different points on it.”

**Recommendation:** Delete the first sentence. Begin directly with the Wiley AI Gateway example and retain its documentation. The product examples establish practical relevance themselves.

### 8.12 — Replace lead-in

**Original** ([source, line 2284](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2284)): “the immediate questions are therefore more practical than architectural”

**Recommendation:** “When evaluating a product, ask what text was embedded, how large each unit was, and how matching passages are combined into article-level results.” Retain the citation and avoid opposing practical questions to architectural ones.

### 8.13 — Replace ending

**Original** ([source, line 2284](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2284)): “so a chunking choice silently becomes an answer-quality choice. Appendix G follows the chunk that far.”

**Recommendation:** “These choices affect the evidence supplied to the answer generator. Appendix G examines how retrieved passages become context for generation.” Keep the preceding alternatives: supplying a chunk, fetching more text or compressing several units.

### 8.14 — Replace both phrases

**Original** ([source, line 2285](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2285)): “A vector is an ordered list of numbers and nothing more.” / “Density decides nothing about meaning.”

**Recommendation:** Use “A vector is an ordered list of numbers” and “Whether a representation supports semantic matching depends on more than its density.” Retain the bibliographic-facts and learnt-sparse examples; they explain the qualification.

### 8.15 — Delete coda

**Original** ([source, line 2285](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2285)): “Those are three further questions, and the phrase answers none of them.”

**Recommendation:** Delete the final sentence. The answer already lists the three questions the vendor’s wording leaves unresolved.


<a id="chapter-9"></a>

## Chapter 9: Reranking and multi-stage retrieval

Original review: [chapter-9-ai-style-review.md](chapter-9-ai-style-review.md).

State the candidate-pool limitation clearly near the beginning, then show its consequences in the academic examples. Repeating it as a slogan after every model adds little. Keep both model questions and candidate-depth questions when advising librarians.

### 9.1 — Replace answer

**Original** ([source, line 2292](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2292)): “Because scale and care trade against each other—and because every shortlist is also a ceiling.”

**Recommendation:** “A shortlist makes more expensive query–document comparisons affordable. Reranking can then reorder only the records on that shortlist.” Keep the question as part of the orientation box.

### 9.2 — Replace question and answer

**Original** ([source, line 2294](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2294)): “Is a good list simply a list of good items? Not for exploration, which is what diversification is for.”

**Recommendation:** “How can a result list cover several aspects of a topic? Diversification considers what each candidate adds to the items already selected.” This gives readers a substantive question rather than a staged paradox.

### 9.3 — Delete

**Original** ([source, line 2301](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2301)): “That constraint is the whole reason rerankers exist in the form they do—and the reason they cannot fix certain problems at all.”

**Recommendation:** Delete the sentence. The preceding definition and the following section already explain the computational benefit and candidate-pool limit.

### 9.4 — Replace the two-sentence explanation

**Original** ([source, line 2339](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2339)): “A cross-encoder is not making a better guess about the same evidence. It is reading the query and one candidate in the same sequence”

**Recommendation:** “A cross-encoder processes the query and candidate together, allowing token-level interactions before it produces a score. In this example it can compare ‘whether the expectations are unrealistic’ with ‘you performed well’, rather than relying only on two independently pooled vectors.” Retain the example and the subsequent warning that joint attention is not infallible.

### 9.5 — Delete setup

**Original** ([source, line 2356](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2356)): “Two consequences matter to a librarian, and they pull in opposite directions.”

**Recommendation:** Delete the sentence. The following paragraphs can introduce storage and comparison costs directly.

### 9.6 — Delete two flourishes

**Original** ([source, line 2357](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2357)): “The storage bill is real.” / “A vendor who has deployed late interaction has spent something to do it.”

**Recommendation:** Delete “The storage bill is real” and “A vendor who has deployed late interaction has spent something to do it.” Keep the concrete explanation of token-vector storage and the cited ColBERTv2 compression results.

### 9.7 — Replace opening

**Original** ([source, line 2359](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2359)): “The choice is not a detail of implementation. It fixes what the system can afford”

**Recommendation:** “The encoding arrangement affects computational cost and which details remain available for comparison.” Follow with the specific consequences for independent, joint and token-level encoding. Prefer “usually too costly across a large collection” to the absolute statement that joint encoding does not scale.

### 9.8 — Replace

**Original** ([source, line 2361](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2361)): “Naming the model identifies the family it came from. What determines behaviour is which of these arrangements it was placed in”

**Recommendation:** “To understand the system’s behaviour, ask how query and document representations are compared and what ranking task the model was trained on.” Retain the model-family context if needed, but avoid making model identity sound irrelevant.

### 9.9 — Replace

**Original** ([source, line 2376](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2376)): “These are not merely prompting details. They create different costs and failure modes.”

**Recommendation:** “Pointwise, pairwise and listwise prompting differ in computational cost and failure modes.” Keep the supporting research examples and citations.

### 9.10 — Delete duplicate

**Original** ([source, line 2381](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2381)): “A sophisticated reranker can reorder only what the retriever allowed it to see.”

**Recommendation:** Remove the pull quote. The candidate-pool limit is already explained in the introduction and is demonstrated again by the product pipelines.

### 9.11 — Keep with minor edit

**Original** ([source, line 2386](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2386)): “Relevance asks how well each item fits the query. Diversity asks what it adds to the items already selected.”

**Recommendation:** “Diversification considers both a candidate’s relevance to the query and what it adds to the results already selected.” This is a useful distinction; retain the concrete examples that follow rather than eliminating the concept to avoid parallelism.

### 9.12 — Replace

**Original** ([source, line 2398](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2398)): “When a vendor says its search ‘uses AI reranking’, the useful follow-up is not which model but how many candidates reached it.”

**Recommendation:** “When a vendor says its search uses AI reranking, ask which model is used and how many candidates it receives.” Both questions are relevant, and neither substitutes for inspecting the earlier retrieval stage.

### 9.13 — Replace

**Original** ([source, line 2418](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2418)): “A tool can be accurately described as using AI at three separate stages and still be governed, at the point that matters most, by lexical retrieval and a pair of cut-offs.”

**Recommendation:** “In this documented pipeline, CDI supplies at most 30 candidates for reranking, and five abstracts reach the answer generator.” Keep the preceding explanation of the consequences and the product citation. Remove the claim about which stage matters most.

### 9.14 — Delete narrative bridge

**Original** ([source, line 2427](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2427)): “Chapter 8 built the representation; this is where it earns its place in a pipeline.”

**Recommendation:** Delete this sentence. The surrounding paragraph already connects Chapter 8’s representation to the pipeline. Keep its cross-reference as “For the representation itself, see Chapter 8.”

### 9.15 — Replace paragraph opening

**Original** ([source, line 2428](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2428)): “The lexical floor survives the learning.”

**Recommendation:** “Matching still requires overlap between active vocabulary dimensions in the query and document representations. Learnt expansion can create that overlap even when the original texts share no query term.” Retain the inverted-index explanation and the qualified Elicit example; avoid presenting ordinary word matching as unchanged in every respect.

### 9.16 — Delete setup

**Original** ([source, line 2431](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2431)): “The two variants are not equally visible in this sector, and the asymmetry itself tells you something.”

**Recommendation:** Delete the first sentence. Begin with the specific Elicit documentation and its deployment caveat. Keep the date-sensitive distinction between absence of public documentation and absence of use; do not strengthen it into a current market claim.


<a id="chapter-10"></a>

## Chapter 10: Hybrid retrieval and rank fusion

Original review: [chapter-10-ai-style-review.md](chapter-10-ai-style-review.md).

Explain why routes can complement each other, how RRF combines ranks and how routing differs from fusion. Keep the worked calculation unchanged. Remove repeated roadmaps and avoid suggesting that lexical retrieval always misses meaning or that dense retrieval reliably captures it.

### 10.1 — Replace question

**Original** ([source, line 2442](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2442)): “and what does the combination hide?”

**Recommendation:** “When a system runs more than one retriever, how does it combine their results, and what information does the combination preserve or discard?” This names the issue later illustrated by RRF.

### 10.2 — Replace

**Original** ([source, line 2445](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2445)): “Running both creates two candidate lists, not one answer.”

**Recommendation:** “The two retrievers return separate candidate lists that must be combined.” Keep the following design questions about depth, deduplication and scores.

### 10.3 — Replace lead-in

**Original** ([source, line 2449](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2449)): “The cleanest summary is more complicated than keywords versus semantics:”

**Recommendation:** “The two methods can fail on different records:” This introduces the two concrete limitations below.

### 10.4 — Replace paired bullets

**Original** ([source, line 2452](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2452)): “A lexical system may preserve the word and miss the meaning.” / “A single-vector dense system may recover the meaning and blur the exact word.”

**Recommendation:** “A lexical retriever can match an exact identifier but may miss a paraphrase with no shared analysed terms.” / “A single-vector dense retriever may find that paraphrase but fail to preserve a decisive identifier or qualifier.” This avoids treating word and meaning as mutually exclusive evidence.

### 10.5 — Replace closing clause

**Original** ([source, line 2455](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2455)): “but the main reason for combining lexical and dense retrieval is already clear:”

**Recommendation:** Replace the clause beginning “but the main reason” with “and combining lexical and dense routes can recover relevant material missed by either route alone”. Preserve “can”; improvement must be evaluated.

### 10.6 — Replace

**Original** ([source, line 2474](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2474)): “Sixty is therefore a conventional setting, not a universal law.”

**Recommendation:** “The constant can be tuned for a different collection or task.” Keep the explanation that the original paper used 60 after pilot testing and that this book writes c to avoid confusion with result depth.

### 10.7 — Delete bridge

**Original** ([source, line 2499](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2499)): “That convenience is also the trade-off.”

**Recommendation:** Delete the first sentence. Start with “Once scores have become ranks, RRF cannot distinguish a narrow first–second gap from an overwhelming one.”

### 10.8 — Replace

**Original** ([source, line 2499](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2499)): “RRF is therefore a strong simple baseline, not proof that fusion will improve every query; it must be evaluated on the collection and tasks that matter.”

**Recommendation:** “Use RRF as a baseline and compare it with the individual retrievers on representative queries.” This makes the evaluation advice actionable without claiming universal superiority.

### 10.9 — Delete duplicate

**Original** ([source, line 2507](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2507)): “One interface, one question, two kinds of evidence contributing to a single ranking.”

**Recommendation:** Remove the sentence. The preceding Web of Science description already explains the two routes and their combination.

### 10.10 — Delete tail

**Original** ([source, line 2508](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2508)): “and neither answer is wrong.”

**Recommendation:** Delete “and neither answer is wrong”. The preceding explanation of query-dependent route selection is sufficient.

### 10.11 — Delete transition

**Original** ([source, line 2509](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2509)): “That second pattern is doing something the first is not.”

**Recommendation:** Delete the first sentence. Start with the existing distinction between combining prescribed paths and selecting routes for a query.

### 10.12 — Delete repeated close

**Original** ([source, line 2510](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2510)): ““Hybrid” is therefore not one architecture or a guarantee of quality. It is a design space—and, as Chapter 12 will add, it still says nothing about who decided to search this way in the first place.”

**Recommendation:** Remove this paragraph. The following summary already states that hybrid retrieval is not a quality guarantee, and the preceding paragraph covers control. Keep one chapter cross-reference, as specified below.

### 10.13 — Replace phrase

**Original** ([source, line 2512](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2512)): “it avoids pretending unlike scores are commensurable”

**Recommendation:** Replace “it avoids pretending unlike scores are commensurable” with “it does not require the input scores to be on the same scale”.

### 10.14 — Replace

**Original** ([source, line 2512](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2512)): “Routing adds another decision: which evidence was allowed to compete at all.”

**Recommendation:** “Routing determines which retrievers contribute candidates for a particular query.” This names the decision directly.

### 10.15 — Replace and consolidate roadmap

**Original** ([source, line 2512](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2512)): “Chapter 11 therefore separates interpretation, transformation and routing before Chapter 12 asks who chooses the next action.”

**Recommendation:** “Chapter 11 examines query interpretation, transformation and routing.” Keep this summary link and remove the duplicated Chapter 11/12 roadmap from the preceding routing discussion. Chapter 12 can introduce its own control question.


<a id="chapter-11"></a>

## Chapter 11: Understanding, transforming and routing queries

Original review: [chapter-11-ai-phrasing-review.md](chapter-11-ai-phrasing-review.md).

Keep the eight query-object examples and the open-access citation-advantage question. They help readers see alternatives to typing keywords. Use the names of mechanisms instead of the recurring door metaphor, and avoid claiming that different studies all prove the same three lessons.

### 11.1 — Replace

**Original** ([source, line 2531](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2531)): “The relation is the route.”

**Recommendation:** “Citation searching follows relationships between papers.” Keep the explanation of vocabulary-independent discovery and citation-graph coverage limits.

### 11.2 — Delete metaphor

**Original** ([source, line 2538](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2538)): “They become eight different doors.”

**Recommendation:** Delete “They become eight different doors.” Rewrite the surrounding introduction as specified in entry 13.

### 11.3 — Replace lead-in

**Original** ([source, line 2547](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2547)): “One caution on the seventh door:”

**Recommendation:** Replace “One caution on the seventh door:” with “For the API example,”. Keep the explanation that filtering for open-access papers would exclude paywalled studies of the open-access citation advantage.

### 11.4 — Replace

**Original** ([source, line 2552](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2552)): “The lesson is mechanism diversity, not that one citation method always wins.”

**Recommendation:** “In that evaluation, combining citation relationships improved retrieval over individual relations.” Keep the preceding qualification about adding PubMed’s text-based score on some measures. Do not turn a particular evaluation into a universal recommendation.

### 11.5 — Replace

**Original** ([source, line 2553](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2553)): “Calling every step a reformulated query erases the evidence the searcher actually used.”

**Recommendation:** “Describing these steps only as changes to query wording leaves out the papers, citation links and relevance judgements used to guide the search.” Retain the connection to Bates’s berrypicking account.

### 11.6 — Replace heading

**Original** ([source, line 2554](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2554)): “Phrase for the mechanism, not the box”

**Recommendation:** “Choosing wording for the retrieval method”. Preserve the existing HTML anchor when implementing the heading change.

### 11.7 — Replace joint conclusion

**Original** ([source, line 2566](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2566)): “Each says the same three things: match the expression to the component that receives it, inspect any transformation, and test the resulting route on the actual task.”

**Recommendation:** “These studies address different components and tasks. For a particular product, test input variants against known relevant records and inspect any generated search strategy.” Use after the replacement in entry 14; remove the claim that each study says the same three things.

### 11.8 — Delete opener

**Original** ([source, line 2567](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2567)): “The box shows an interface.”

**Recommendation:** Delete “The box shows an interface.” Begin the next sentence “The input box does not tell you what object the system will construct from your input”. Keep the concrete questions that follow.

### 11.9 — Replace

**Original** ([source, line 2661](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2661)): “Pseudo-relevance feedback breaks an upstream-only picture.”

**Recommendation:** “Pseudo-relevance feedback constructs a later query from the results of an earlier retrieval pass.” Remove the next sentence if it only repeats this dependency. Keep the explanation that a prescribed two-pass sequence can still be fixed and non-agentic.

### 11.10 — Delete

**Original** ([source, line 2670](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2670)): “The distinction matters.”

**Recommendation:** Delete “The distinction matters.” The next sentence states the actual difference between Query2doc and HyDE.

### 11.11 — Replace

**Original** ([source, line 2516](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2516)): “This chapter starts one step earlier: not every search begins with a string.”

**Recommendation:** “Search can begin with a seed paper, citation relationship, relevance judgement or structured condition as well as a text query.” Let the next paragraph explain how these inputs reach different mechanisms.

### 11.12 — Replace paragraph

**Original** ([source, line 2521](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2521)): “They are still strings.” / “Phrasing comes last, after both.”

**Recommendation:** “Keywords, questions and prompts are text inputs. Before choosing wording, establish which retrieval method will receive the input and whether another query object, such as a seed paper, would suit the task.” This absorbs both flagged fragments.

### 11.13 — Replace whole introduction

**Original** ([source, line 2538](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2538)): “Eight categories are a lot to hold at once, so run one need through all of them.”

**Recommendation:** “The question ‘Is there an open access citation advantage?’ can be approached using each of the eight query objects below.” Replace the complete paragraph, including the “doors” sentence covered in entry 2. Keep the figure’s qualification that the categories overlap.

### 11.14 — Replace

**Original** ([source, line 2566](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2566)): “None of these results licenses the rule ‘write naturally’ or ‘write more.’”

**Recommendation:** “The findings do not support a general rule that longer or more natural-language queries work better.” This preserves the limitation without the elevated “licenses” phrasing; follow with entry 7’s practical advice.

### 11.15 — Replace

**Original** ([source, line 2670](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2670)): “Both can bridge vocabulary gaps, but both can also import unsupported assumptions.”

**Recommendation:** “Generated text can supply useful search vocabulary, but it can also add details that the user did not specify and that may be false.” Keep the warning that retrieving real documents does not validate the generated text.


<a id="chapter-12"></a>

## Chapter 12: Agentic search

Original review: [chapter-12-ai-style-review.md](chapter-12-ai-style-review.md).

Retain the distinction between fixed, adaptive and agentic control, but explain the observable actions rather than repeatedly announcing conceptual revelations. Keep product observations dated and separate from architecture claims. The catalogue experiment is valuable first-person material; preserve its limits and the concrete examples.

### 12.1 — Replace and harmonise

**Original** ([source, line 2761](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2761)): “Read the three rows as landmarks on a continuum, not three species.”

**Recommendation:** “These are reference points along a continuum. A product’s position may vary by mode and by how much of the sequence its designers prescribe.” Use the same terminology in Table 12.3’s caption and the summary; remove repeated “species” comparisons.

### 12.2 — Replace paragraph opening

**Original** ([source, line 2765](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2765)): “That definition deliberately withholds two things.”

**Recommendation:** “An agent works within limits on available tools, accessible sources, rounds and stopping conditions.” Remove “First” and “Second” when restructuring the paragraph. Keep the concrete tool examples and explain separately that planning may follow instructions or heuristics rather than reasoning from first principles.

### 12.3 — Delete duplicate

**Original** ([source, line 2778](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2778)): “Deep tells us how far the search goes. Agentic tells us how the next direction is chosen.”

**Recommendation:** Delete this pull quote. Table 12.2 and the following paragraph already distinguish retrieval depth, iteration and control.

### 12.4 — Delete staged question

**Original** ([source, line 2789](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2789)): “Do products sort themselves neatly into these distinctions? It is worth testing.”

**Recommendation:** Delete the first two sentences. Begin “I tested the tools with a task: find papers that could have been cited by a particular article but were not.” Retain the linked write-up, procedure and observation dates.

### 12.5 — Replace

**Original** ([source, line 2790](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2790)): “Most of the specialised academic tools failed it, and the shape of each failure is more informative than the verdict.”

**Recommendation:** “Most of the specialised academic tools did not complete the task.” Follow with the existing tool-by-tool observations; they show how the failures differed.

### 12.6 — Delete setup

**Original** ([source, line 2791](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2791)): “That last result is worth sitting with, because the obvious reading of it is wrong.”

**Recommendation:** Delete “That last result is worth sitting with, because the obvious reading of it is wrong.” Start with the observed behaviours and their possible explanations.

### 12.7 — Replace surrounding explanation

**Original** ([source, line 2791](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2791)): “The academic tools were not out-thought.”

**Recommendation:** “Several tools appeared to understand the request but did not complete the comparison. For example, Undermind asked relevant clarifying questions but did not subtract the article’s references from the related papers it found. This behaviour alone does not establish whether the cause was a missing operation, a workflow restriction or a poor choice of actions.” Replace the categorical diagnosis in the same paragraph too; the observations do not reveal every internal capability.

### 12.8 — Delete flourish

**Original** ([source, line 2806](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2806)): “The cell exists, and it is occupied.”

**Recommendation:** Delete the final sentence. The preceding Asta example already demonstrates iterative retrieval within a prescribed workflow.

### 12.9 — Replace

**Original** ([source, line 2810](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2810)): “The point of reading the description rather than the adjective is not to catch anyone out. It is that the description is the part you can check.”

**Recommendation:** “Use the documented operations to assess the control arrangement, and record what the description leaves uncertain.” Keep the qualifications about vendor terminology and the ambiguous “or something else entirely” clause.

### 12.10 — Replace

**Original** ([source, line 2825](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2825)): “As with every other distinction in this book, the interface label settles none of it.”

**Recommendation:** “The product label alone does not establish these properties.” Remove the reference to every other distinction in the book.

### 12.11 — Replace conclusion

**Original** ([source, line 2827](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2827)): “That is the whole of what agency contributes—and it is why an agentic system built on a weak retriever is still a weak search.”

**Recommendation:** “The controller can change queries, choose among available sources and decide whether to search again. These actions may improve the combined results, while the scoring rule used by each retriever remains unchanged.” This avoids contradicting the later catalogue example. Also qualify the adjacent interface/MCP claim: “If both access paths use the same endpoint and parameters, the underlying retrieval operation may be the same; the controller changes how it is used.” Do not assert endpoint parity without documentation.

### 12.12 — Delete cue

**Original** ([source, line 2840](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2840)): “But it is worth being honest about how often that applies.”

**Recommendation:** Delete “But it is worth being honest about how often that applies.” Keep the practical question of whether the task fits an existing procedure; prefer a conditional cost comparison over claiming that most academic searches are a poor use of agents.

### 12.13 — Replace

**Original** ([source, line 2841](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2841)): “Three further difficulties are specific to retrieval. The last two are the serious ones.”

**Recommendation:** “For retrieval, inspect the available actions, the effect of earlier results on later searches, and the stopping conditions.” This introduces the three subsections without ranking their seriousness in advance.

### 12.14 — Replace contrast pair

**Original** ([source, line 2842](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2842)): “This is not the black-box problem. The issue is hidden capability, not hidden reasoning.”

**Recommendation:** “A run trace shows actions taken, but may omit other actions the system could have used.” Delete the two flagged contrast sentences and merge with the preceding trace explanation to avoid duplication. Treat hidden capabilities as one aspect of limited transparency, not a wholly separate problem.

### 12.15 — Replace sentence

**Original** ([source, line 2844](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2844)): “the loop is where that separation acquires teeth”

**Recommendation:** “Chapter 1 distinguished matching from relevance. Here, the model may use its own assessment of the results to decide whether to continue searching.” Retain the discussion of budgets, user interruption and uncertainty about model-chosen stopping criteria.

### 12.16 — Replace phrase

**Original** ([source, line 2844](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2844)): “when the answer actually matters”

**Recommendation:** Replace “when the answer actually matters” with “for evidence-synthesis tasks that require high recall”. Keep the Appendix F link.

### 12.17 — Replace

**Original** ([source, line 2845](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2845)): “None of this is an argument against agentic search. It is an argument for asking which arrangement a task actually needs—and, when the answer is agency, for asking to see the trajectory.”

**Recommendation:** “Choose the control arrangement for the task. For agentic searches, record the actions, intermediate results and stopping conditions.” This supplies practical advice without a reassurance pivot.

### 12.18 — Replace paragraph

**Original** ([source, line 2851](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2851)): “This chapter has been careful about what agency does not do. But that leaves the balance wrong”

**Recommendation:** “An agentic loop can respond to a weak result by selecting another available action, such as broadening the query or trying a different source.” Keep the later qualification that fixed or adaptive workflows can also implement useful retries.

### 12.19 — Replace pair

**Original** ([source, line 2855](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2855)): “One-shot transformation cannot learn from a failure it does not see. The loop can, because it reads the empty result and treats it as information.”

**Recommendation:** “The single-pass rewrite did not use the zero-result response to revise its query. The loop did, broadening the search to related subject areas.” Scope the claim to the observed comparison; avoid implying that only agentic control can use feedback.

### 12.20 — Replace connected sentences

**Original** ([source, line 2860](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2860)): “The work does not disappear. It moves”

**Recommendation:** Replace “The work does not disappear. It moves” and its continuation with “Librarians still need to supply current coverage and entitlement information, document local search behaviour, and handle specialised requests that the system cannot resolve.” Retain the concrete specialised-query example if useful. Do not imply that routine enquiry work has been shown to disappear.

### 12.21 — Replace closing line

**Original** ([source, line 2862](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2862)): “Agency does not improve the retriever’s scoring function. It can improve the search process by giving a failed attempt somewhere to go.”

**Recommendation:** “In these examples, feedback and reformulation helped recover useful results from unsuccessful queries over the same index.” Keep the preceding limitations; this is evidence about the overall process, not a general guarantee of recovery.

### 12.22 — Replace answer opening

**Original** ([source, line 2865](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/2343676f8136ecd7b6445c96ca0e0077159384d4/search-textbook.html#L2865)): “Nothing at all — and that is the point.”

**Recommendation:** “The comparison concerns the search process: both runs used the same underlying retriever.” Retain the final qualification that the examples do not establish that recovery requires agentic control. Replace the intervening categorical explanation with “The observed benefit was consistent with using feedback to revise the query; the comparisons did not isolate that as the sole cause.”

## Implementation and checking

Apply the paragraph-level replacements before the phrase-level deletions, checking the overlap notes. Read the affected paragraph and its neighbours aloud after each group of edits; remove stranded pronouns, duplicated conclusions and unnecessary transitions. Do not replace every contrast with the same sentence pattern.

For any later implementation, preserve the existing examples, numerical results, citations, footnote identifiers, heading anchors and figure references. Heading and caption changes should be checked against the contents list and accessibility text. Product descriptions here retain the textbook’s evidential scope and dates; this editorial review does not refresh those claims against current vendor documentation.

This recommendations-only change requires checking coverage, source locators, Markdown structure and the Git diff. It does not change executable code or the published textbook.

*Original passages by Aaron Tay Chee Hsien, from the textbook and associated reviews, under [CC BY 4.0](../LICENSE).*
