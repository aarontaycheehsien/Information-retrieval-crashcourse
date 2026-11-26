---
key: "boolean-admission"
kind: "chapter"
eyebrow: "Chapter 2"
meta: "About 17 min"
question: "How does a system decide which records are eligible?"
legacy_anchors: ["ch1"]
---

## Boolean admission and the inverted index {#boolean-admission}

::: {.stage-map on="analysis" label="Pipeline map highlighting analysis and execution rules"}
:::

::: chapter-orient
Strict Boolean retrieval is the oldest answer to the retrieval problem and still the clearest.
A query states conditions; a record either satisfies them or it does not.
There is no notion of a better or a worse match, only membership of an eligible set.

That simplicity is worth understanding precisely, because everything later in this book is a departure from it.
This chapter follows a document from raw text through tokenisation, stemming and indexing, then shows how Boolean conditions are evaluated over the resulting structure—and why the answer arrives so quickly.
:::

### Strict Boolean search: words as admission rules {#strict-boolean-search-words-as-admission-rules}

Consider this query, in which `delulu` is internet slang for “delusional”:

> delulu AND job

A Boolean system requires a record to satisfy both conditions.

Boolean operators create hard decisions:

- `AND` requires conditions to occur together.
- `OR` allows alternatives.
- `NOT` excludes records.

A record that passes all of the query’s hard conditions is **eligible** to enter the result set.

Boolean retrieval tells us whether a record meets the conditions the searcher expressed, [not whether it is relevant to the underlying need](#distinction-match-relevance).
Boolean conditions let a searcher specify and inspect the rules for including records, then rerun the same strategy.

Boolean logic underlies the advanced-search interfaces librarians use most: [PubMed’s Advanced Search](https://pubmed.ncbi.nlm.nih.gov/advanced/) with its search-history builder and MeSH terms, [Web of Science Advanced Search](https://webofscience.zendesk.com/hc/en-us/articles/28470463061265-Advanced-Search) with its field tags, and the equivalent screens in Scopus, EBSCOhost and Ovid.
Conventional bibliographic database strategies for systematic reviews typically combine Boolean logic with controlled vocabulary, free-text terms, fields, proximity operators and other database-specific syntax.
These explicit admission rules are only one part of systematic study identification; [Appendix F treats the wider process as a high-recall retrieval problem](#appendix-evidence-synthesis-high-recall-retrieval).

**Boolean logic does not by itself assign graded ranking scores.** Once several records are eligible, Boolean alone supplies no rule for deciding which should appear first.

> Boolean conditions decide which records may compete; ranking decides their order.

This distinction matters when query expansion goes wrong.

Suppose an LLM expands `delulu` into:

> delulu OR unrealistic OR irrational OR foolish

If `foolish` is a poor alternative, records containing it may enter the result set.
Ranking may push them down, but Boolean has already admitted them.

:::: {.figure key="poor-synonym-expansion"}
A poor synonym expansion changes which records can enter

![Infographic comparing two Boolean gates. Left, the original query delulu OR unrealistic OR irrational: a tighter gate admits three records, labelled mostly relevant. Centre, an LLM adds the weak synonym foolish. Right, the expanded query delulu OR unrealistic OR irrational OR foolish: a wider gate admits the same three records plus four that match only foolish, each marked as noise. A banner reads: a weak OR synonym is not just low-weighted; it changes which records can enter.](images/02%20Boolean%20search%20-%20words%20as%20admission%20rules/ChatGPT%20Image%20Jul%2026,%202026,%2009_49_10%20PM.png){width="1448" height="1086"}

::: caption
Ranking can push a weakly matched record down, but Boolean has already admitted it.
:::
::::

The reverse error is more serious.
If a relevant record fails a compulsory `AND` condition, ranking cannot rescue it.
It never enters the competition.

This is why LLM-generated synonyms require particular care in formal Boolean strategies.
A weak suggestion is not merely given a low weight.
It changes which documents can be returned.

:::: {.common-confusion label="IR terminology"}
#### Exact-match retrieval: satisfy the query’s specification {#exact-match-retrieval}

In traditional IR terminology, Boolean retrieval is an **exact-match** model: a record either satisfies the query’s complete specification or it does not.
For `A OR B`, containing A alone can satisfy that specification.
Exact does not mean containing every named term.

::: {#boolean-matching-in-practice-title}
**What counts as satisfying a condition depends on how the database represents and interprets text.**
:::

Before the Boolean operators are applied, the database will usually\ [tokenise and normalise](#before-the-index-text-becomes-tokens) the query and records, apply [stemming or lemmatisation](#after-tokenisation-stemming-and-lemmatisation), interpret quotation marks as phrase instructions and restrict matching to [particular fields](#words-sent-to-retrieval-may-not-be-the-words-you-typed).
Its [indexing choices](#from-analysed-tokens-to-a-term-first-map) determine which analysed query terms can meet which indexed document terms.

The final Boolean decision is still yes or no.
Here, “exact” refers to the processed query conditions, not necessarily to a literal string as typed.
Neither meaning alone supplies a relevance ranking.
::::

::: {#how-boolean-and-bm25-use-an-inverted-index .legacy-anchor}
:::

### How Boolean search uses an inverted index {#how-boolean-search-uses-an-inverted-index}

Large academic indexes like OpenAlex, Semantic Scholar and Ex Libris CDI span hundreds of millions of records.
To answer queries as quickly as possible, Boolean search does not normally reread every record whenever a query arrives.

::: {.common-confusion label="A simpler way to search" label-class="callout-label"}
#### Searching the text directly: grep {#grep-searching-text-directly}

You can search a collection without building an index. **grep** is a command-line tool that searches text for a pattern and normally prints the matching lines.
Imagine four tiny records saved in a text file called `records.txt`, one record per line, each with a D1–D4 label first:

```
D1 Delulu job interview expectations
D2 Job interview preparation guide
D3 Unrealistic job expectations
D4 Delulu about my dream job
```

This command is an illustration; you do not need to install anything to follow it:

```
grep -niF 'delulu' records.txt
```

`-n` prints line numbers, `-i` ignores case, and `-F` treats the search text as a literal string.
Literal-string matching is a different sense of “exact” from [exact-match retrieval](#exact-match-retrieval) above, which concerns the processed query conditions.
The output is:

```
1:D1 Delulu job interview expectations
4:D4 Delulu about my dream job
```

The command finds the letters in *Delulu*.
It does not connect them with *Unrealistic* in D3.
Without `-F`, grep interprets a **regular expression**: a pattern specifying allowed character sequences.
Patterns can express alternatives or word boundaries, but they do not automatically add stemming, synonyms or an understanding of negation.
See the [GNU grep manual](https://www.gnu.org/software/grep/manual/) for the syntax.

This is lexical retrieval by scanning text.
Ordinary grep, and the related tool [ripgrep](https://github.com/BurntSushi/ripgrep) (`rg`), search without a persistent content index.
An inverted index instead prepares term-to-record pointers before the query arrives.
Scanning avoids that preparation and can suit a local collection; an index can avoid repeatedly scanning the collection for many queries.
Neither choice alone determines relevance.

Grep normally returns matching lines in input order, not a relevance ranking.
A line is also not necessarily a complete record: we deliberately put one record on each line here.
Finding a line, finding its document and obtaining enough evidence to answer a question are different achievements. [Chapter 12 returns to grep](#agent-grep-search) when a model chooses the patterns and reads beyond the matches.
:::

Boolean search over a large collection instead uses an **inverted index**: a structure that starts with searchable terms and points to the records containing them.
The next five sections build it in order: text becomes tokens; tokens may be reduced by stemming or lemmatisation; the analysed terms become a term-first map, over which Boolean operators work as sets; truncation, phrase and proximity operators run over that same map; and the map’s ordering is what makes the answer fast.

### Before the index: text becomes tokens {#before-the-index-text-becomes-tokens}

A computer does not begin with an intuitive understanding of words.
It needs a rule for dividing a string of text into units it can process. **Tokenisation** is that division, and each resulting unit is a **token**.
A token is often a word, but it can also be punctuation, part of a word, a character or another unit chosen by the system.

For a simple English lexical index, the analysis might proceed as follows:

| Stage | Illustrative output |
|---|---|
| Original text | `Delulu about jobs!` |
| Tokenisation | `Delulu` · `about` · `jobs` · `!` |
| Case normalisation | `delulu` · `about` · `jobs` · `!` |
| Optional stop-word and punctuation removal | `delulu` · `jobs` |
| Optional stemming | `delulu` · `job` |
| Terms entered in this index | `delulu` · `job` |

: Stages of lexical analysis, and what a sample string looks like after each.

There are different ways to do tokenisation.
A different analyser might retain `about`, keep `jobs` unchanged, treat the exclamation mark as a token or preserve the complete string in a keyword field.
Languages without spaces between every word require different boundary rules, while names, apostrophes, hyphens, URLs and identifiers create choices even in English.

**Tokenisation is only the first step.** Lowercasing, stemming, stop-word removal and synonym or controlled-vocabulary mapping are separate operations.
The broader sequence is often called **text analysis**.
Its final output supplies the terms that can enter a lexical index.

At search time, the query is also tokenised and analysed.
Lexical matching becomes possible when a resulting query term corresponds to an indexed document term.
Query and document analysis need not be identical in every system, but incompatible choices can create missed or unexpected matches.

> Text becomes tokens; analysis turns selected tokens into searchable terms.

### After tokenisation: stemming and lemmatisation {#after-tokenisation-stemming-and-lemmatisation}

Tokenisation decides where one unit ends and another begins. **Stemming** and **lemmatisation** are later analysis steps that may transform some of those units before matching.
Their practical purpose is to let related grammatical forms share searchable evidence even when the user and the document do not contain exactly the same surface form.

| Method | How it works | Illustrative output | What to remember |
|---|---|---|---|
| **Stemming** | Uses rules or heuristics to remove or replace common endings. | `studies`, `studying` and `studied` might become `studi`. | The stem is a matching key and need not be a valid word. |
| **Lemmatisation** | Uses vocabulary and morphological analysis, often including part of speech, to identify a dictionary form. | The same forms might become `study`; adjectival `better` may become `good`. | The output is a word, but the analyser must still choose the correct grammatical interpretation. |

: Stemming and lemmatisation compared: how each reduces a word, and what to remember about the difference.

These outputs are illustrative rather than guaranteed.
Algorithms, dictionaries and languages differ, and a product may use neither method or may apply different analysers to different fields.
A title-and-abstract field might reduce `jobs` to `job`, while an exact-name, code or identifier field deliberately preserves the original string.

The benefit is usually recall.
If both query and document analysis reduce `jobs` and `job` to the same term, either form can retrieve the other.
The risk is lost precision through **over-stemming**, when unrelated words collapse to the same term.
The reverse problem is **under-stemming**: related forms remain separate and a potentially useful match is missed.
Lemmatisation uses grammatical information to choose a base form.
An incorrect interpretation can still produce a poor match, so it needs testing on the collection.

Compatibility matters: Figure 2.2, below, shows what happens when the two analysers disagree.
When forms do converge, the analysed term determines which indexed-term entry is consulted, how occurrences are counted and how many documents contain that term.
These choices affect Boolean matching and the collection statistics used by ranked lexical methods introduced later.

Neither technique is the same as [user-entered truncation](#truncation-phrases-and-proximity-over-the-index) such as `librar*`, whose expansion depends on database syntax.
Nor are they synonym expansion, controlled-vocabulary mapping, semantic query rewriting or dense retrieval.
Those operations can connect different expressions or concepts; stemming and lemmatisation primarily normalise grammatical form within a lexical analysis pipeline.
For a fuller technical account, see Manning, Raghavan and Schütze, “[Stemming and lemmatization](https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html)”, in *Introduction to Information Retrieval*.

:::: {.figure .worked-figure key="compatible-analysis"}
Different surface forms can meet at the same indexed term

::: {.include src="figures/compatible-analysis.html"}
:::

::: caption
Illustrative analysis choices.
The match is between processed terms, so the query and the displayed text need not have identical surface forms.
Stemming is optional and is separate from user-entered truncation such as `librar*`.
:::
::::

Whatever analysis choices are made, their final terms become the keys used to build the inverted index.

### From analysed tokens to a term-first map {#from-analysed-tokens-to-a-term-first-map}

A collection is naturally organised document first: open a record, then read the words inside it.
An inverted index reverses that direction for searching.
It starts with an analysed term and points to the documents in which that term occurs.

Take the four records from the grep example as a tiny collection:

| Record | Text |
|---|---|
| D1 | Delulu job interview expectations |
| D2 | Job interview preparation guide |
| D3 | Unrealistic job expectations |
| D4 | Delulu about my dream job |

: A miniature four-record collection, used throughout this chapter and returned to in Appendix C.

After the analysis described above (without the optional stemming step), the index maintains a **dictionary** of searchable terms.
Each dictionary term points to a **posting list**: an ordered list of entries identifying the documents that contain it.
A selected part of the dictionary for these records might look like this:

| Indexed term | Posting list |
|---|---|
| `delulu` | D1, D4 |
| `job` | D1, D2, D3, D4 |
| `interview` | D1, D2 |
| `expectations` | D1, D3 |
| `unrealistic` | D3 |
| `preparation` | D2 |

: The same four records as an inverted index: each term paired with its posting list.

:::: {.figure .worked-figure key="records-to-postings"}
The same collection, viewed in two directions

::: {.include src="figures/records-to-postings.html"}
:::

::: caption
The same D1–D4 records as the tables above.
The direction reverses from records containing words to terms pointing at records—like a book’s back-of-book index, but pointing to records instead of pages.
Highlighting follows the two queried terms; identifiers establish the match.
:::
::::

::: {#boolean-treats-postings-as-sets}
The search in Figure 2.3 shows Boolean operators treating postings as sets.
For `delulu AND interview`, the engine looks up two posting lists and intersects their ordered document identifiers. `OR` combines lists, while `NOT` removes documents found in an excluded list.
At this level, Boolean retrieval is largely set processing over postings.
:::

A **posting** is one entry in such a list.
Real postings normally store more than a document identifier.
They may also record how often the term occurs, which field contains it and the positions at which it appears.
Those additions support later relevance scoring, field weighting, phrase searching, proximity scoring and result highlighting.

The earlier analysis choices determine which dictionary term and posting list a query consults.
They can therefore change which records match even before any ranking method is applied.

> An inverted index is best understood as a term-to-document map built from analysed text.

:::: {.common-confusion label="Terminology" aria-labelledby="what-full-text-search-means-in-ir"}
::: {#what-full-text-search-means-in-ir}
**Information retrieval often uses the term FTS, or full-text search.
What does that mean?**
:::

In search engineering, **full-text search** usually means a facility for searching natural-language text rather than looking up only exact database values, such as the record whose DOI is `10.1234/example` or the records whose publication year equals `2025`.
Full-text search instead analyses words inside fields such as titles, abstracts or document text so that a query can match within their language.
The text is analysed into searchable terms, associated with documents in an index and matched against an analysed query; the matches may then be ranked.

[PostgreSQL, for example, describes full-text search](https://www.postgresql.org/docs/current/textsearch-intro.html) as finding natural-language documents that satisfy a query and optionally ordering them by relevance.
Its searchable “document” may be one text field or a combination of several fields rather than a complete publication.

This can be confusing for librarians, because **full text** commonly means the complete content of an article, book or report rather than a citation or abstract.
Here, “full text” concerns how much of the publication is covered, whereas “full-text search” names a way of searching text fields.
A system may call its facility full-text search even when the indexed text consists only of titles and abstracts, selected database fields, OCR text or passages.
Conversely, possessing a complete article does not guarantee that every part of it has been indexed or made searchable.

FTS also does not identify one query rule or ranking method.
A full-text engine may apply strict Boolean conditions or require only some of the query terms, may score matches with BM25 or another lexical method, and may participate in a hybrid pipeline.
Nor does “full” guarantee that every word survives analysis: stop-word removal, normalisation and stemming may change the indexed terms.
The practical questions are therefore **which text is indexed, what is the indexed unit, and how are matches admitted and ranked?** The distinction between a source document and its searchable units is developed in [Chapter 8](#one-document-one-chunk-and-one-vector-are-not-the-same-thing).
::::

### Truncation, phrases and proximity use the same map {#truncation-phrases-and-proximity-over-the-index}

Three operators that librarians use daily run over this same structure.

**Truncation looks in the dictionary, not in the records.** For `librar*`, the engine first finds the dictionary terms that begin with `librar`, then retrieves the records on any of their posting lists, as it would for `OR`.
Two consequences follow.
The pattern is compared with the terms the index stores, so analysis matters: where a field stores only the stem `studi`, the pattern `studie*` has no stored term to match.
And a short pattern can expand to a very large number of terms, which is why some databases require a minimum number of characters before the truncation symbol or limit how many variants one pattern may expand to.
Systems differ on both points, so check the database’s own documentation.

**Phrase and proximity operators use positions.** Postings that record where a term appears let the engine test more than co-occurrence.
For `"open access"`, it finds the records containing both terms, as for `AND`, then keeps those in which `access` occupies the position immediately after `open`.
A proximity operator relaxes that test to “within *k* positions”.
The test is applied to analysed terms, so stop-word removal or stemming can make a phrase search looser than its quotation marks suggest.

In each case the decision is still yes or no: these operators refine admission, and none of them ranks.
For fuller accounts, see Manning, Raghavan and Schütze, [“Wildcard queries”](https://nlp.stanford.edu/IR-book/html/htmledition/wildcard-queries-1.html) and [“Positional indexes”](https://nlp.stanford.edu/IR-book/html/htmledition/positional-indexes-1.html), in *Introduction to Information Retrieval*.

### Why inverted indexes can be so fast {#why-inverted-indexes-can-be-so-fast}

The first advantage is **selective access**.
The engine goes directly from each analysed query term to its posting list rather than scanning every document.
Rare terms are especially selective because their lists are short.

The second advantage is **ordered access**.
Posting lists are normally sorted by document identifier.
For a Boolean `AND` query, this makes it quick to find identifiers that appear in every required term’s posting list: the engine can work forwards through the lists instead of repeatedly searching earlier entries.
A worked two-list example appears in [Appendix C](#how-two-ordered-posting-lists-are-intersected).

The posting lists identify the eligible set.
To order it by estimated relevance, the system also needs a scoring rule.

:::: chapter-close
1. In this lexical index, matching uses the terms produced by text analysis.
   Tokenisation, case folding, stop-word handling and stemming all happen before anything is indexed.
2. Query and document must be analysed compatibly.
   A mismatch between the two is a silent and common source of retrieval failure.
3. An inverted index maps terms to posting lists, which is why Boolean evaluation is set intersection and union rather than a scan of documents.
4. Truncation expands a pattern against the dictionary, and phrase and proximity operators test stored positions.
   All three act on analysed terms.
5. Boolean retrieval is traditionally called exact-match retrieval: records satisfy the processed query specification or do not.
   It produces an eligible set, not an ordering; “exact” need not mean a literal string match.

::: {.chapter-transition}
A large eligible set can be hard to browse.
Chapter 3 asks how a lexical system can order it.
:::
::::

::: self-check
A truncated search for `librar*` returns records containing “library” and “librarian” but not “libraries”. Which layer would you look at first, and why is it not the Boolean operator?

:   Analysis — how the truncation is expanded, and which surface forms the index actually holds as terms.
    Boolean operators only combine whatever posting lists analysis produced. `AND`, `OR` and `NOT` never decide which forms of a word map to which term.

A query analyser stems *jobs* to *job*, but the index stored *jobs* unstemmed. What happens, and why is this failure easy to miss?

:   The query consults a dictionary entry that does not exist, finds no posting list, and the term contributes nothing.
    It is analyser incompatibility between the query and document sides.
    It is easy to miss because there is no error — only a smaller result set than expected.

Why can a Boolean system answer a query over two hundred million records in under a second without reading any of them?

:   Two properties of the inverted index.
    Selective access: it goes straight from each analysed term to that term’s posting list rather than scanning documents.
    And ordered access: posting lists are sorted by document identifier, so an intersection moves forward through both lists without ever going back.

Grep finds D1 and D4 for “delulu”. Has it ranked them by relevance, and must it have used an inverted index?

:   Neither follows.
    The example prints matching lines in input order, with no relevance score or persistent content index.
    It misses D3’s “Unrealistic” because the literal pattern does not match that expression.
    Whether any of these records answers a need requires a separate judgement.

A record contains A but not B. Can it be an exact match to `A OR B`?

:   Yes.
    It satisfies the complete Boolean specification.
    “Exact-match retrieval” concerns that decision, not whether every named term occurs.
    Boolean alone supplies no relevance ranking.
:::
