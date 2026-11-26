---
key: "evaluation"
kind: "chapter"
eyebrow: "Chapter 14"
meta: "About 22 min"
question: "How would you know whether one retrieval system is better than another—and better at what?"
---

## Measuring whether retrieval worked {#evaluation}

::: {.stage-map on="query-transformation analysis first-stage fusion reranking presentation" controller="on"}
:::

::: chapter-orient
Every chapter so far has described what a system does.
None has said how you would know whether it does it well.
That is not an engineering detail: it is the question a library actually faces when a vendor claims an improvement, when a discovery layer is updated overnight, or when a colleague asks whether the new search is better than the old one.

This chapter supplies the measurement vocabulary the rest of the book has been using informally.
It defines precision and recall, then explains what the metrics quoted in vendor material actually reward—and what a benchmark number is really worth.
It ends with the only evaluation a library fully controls: a set of its own queries, judged by its own staff, rerun whenever something changes.
:::

### Relevance is a judgement, not a property {#relevance-is-a-judgement}

Earlier we separated matching from relevance and the query from the information need.
We can now look more carefully at what information-retrieval researchers mean by relevance.
A system can register that terms overlap, vectors are close or a reranker assigned a high score.
Those observations may be evidence about relevance, but none is the judgement itself.

No record is relevant in itself.
It is relevant to someone, for some purpose, at some point in their work.
The same paper can be exactly what a researcher tracing a method needs, useless to an undergraduate who wanted an overview, and excluded on sight by a systematic reviewer screening against inclusion criteria.
Three verdicts, one record, and none of them wrong.

Those three verdicts are not even the same kind of claim. [The first two differ because the readers know different amounts; the third differs because the task imposes criteria the other two do not have.]{} [The four perspectives named in Chapter 1 help separate them:]{}

**System or algorithmic relevance**
:   How strongly the retrieval system estimates that an item fits the query or another representation it can process.
    A BM25 score, vector similarity or reranker score belongs at this level.
    A system can also estimate topical or task-specific suitability, but those estimates are not identical to a person’s experienced usefulness.

**Topical relevance**
:   Whether the item is actually about the subject being sought.
    A topically relevant paper can still have the wrong population, method, date or document type.

**Cognitive relevance or pertinence**
:   Whether the item is informative to this reader, given what they already know.
    This is the level on which the researcher and the undergraduate disagree, and it is invisible to any system that has no model of who is asking.

**Situational relevance or usefulness**
:   Whether the information helps this person accomplish this task in this context.
    The answer may change with the searcher’s stage of work, constraints and purpose.
    The reviewer’s exclusion belongs here: nothing about the paper changed, only the criteria it was held against.

These levels are a teaching simplification, not a complete taxonomy. [Mizzaro’s historical review](https://doi.org/10.1002/%28SICI%291097-4571%28199709%2948%3A9%3C810%3A%3AAID-ASI6%3E3.0.CO%3B2-U) maps several ways relevance has been defined, while [Saracevic’s framework](https://onlinelibrary.wiley.com/doi/10.1002/asi.20682) distinguishes system-oriented and user-oriented manifestations and relates algorithmic, topical, cognitive, situational and affective dimensions. [The affective or motivational dimension—what the searcher intends and how they feel about the task—is the one this book leaves out.]{} Relevance can also change over time as a person learns or the task develops.
The important common point is that relevance names a relationship among information, a representation of a need, a person and a situation—not a substance stored inside a document.

This has a consequence that governs everything else in the chapter.
A retrieval system cannot be simply correct in the abstract.
It can only be closer to or further from somebody’s judgement under specified criteria.
Every number below is downstream of those criteria and inherits whatever the assessors understood the question and task to be.

Librarians are already practised at this.
A reference interview is relevance elicitation: establishing what would count as a useful answer before going to look for one.
What research evaluation adds is only that the judgements get written down, so that two systems can be compared against the same ones.

Which of these levels a measurement uses matters.
Many standard test collections operationalise relevance mainly through topical judgements, so a superseded or retracted paper, or one answering a neighbouring question, can still count as relevant; other evaluations use detailed task or inclusion criteria.
The metric cannot tell which conception was used.
It can only score against the judgements it receives.

Retrieval metrics measure performance against an **operational definition of relevance encoded in the relevance judgements**.
Put more simply:

> A metric does not measure relevance.
> It measures agreement with whoever judged relevance.

### Precision and recall, and the choice librarians already make {#precision-and-recall}

Given a set of results and a set of judgements, two questions can be asked. **Precision is the fraction of retrieved documents that are judged relevant.** **Recall is the fraction of all judged-relevant documents that were retrieved.** What counts as judged relevant depends on the evaluation protocol and the criteria given to the assessors.[^precision-recall-definitions]

| Measure | The question it answers | What a bad score costs | The task that leans on it |
|---|---|---|---|
| **Precision** | Of what was retrieved, how much was judged relevant? | Wasted screening time; a searcher who stops reading before reaching the good material. | Ready reference, known-item lookup, anything feeding a short answer. |
| **Recall** | Of everything judged relevant, how much was retrieved? | Evidence that was never seen, and a conclusion drawn without it. | Systematic and scoping reviews, patent and legal searching, due diligence. |

: Precision and recall: what each counts, what it costs, and which library task leans on it.

The two errors described in [Chapter 2](#strict-boolean-search-words-as-admission-rules) can now be named.
A weak alternative added to an `OR` admits records that should not have been competing, which costs precision.
A relevant record failing a compulsory `AND` never enters that result set, which costs recall.
Screening can remove false positives from what a person ultimately uses, but merely looking farther down a ranking does not improve retrieval precision.

Changing the cut-off on one ranking often trades precision against recall: admitting more records can recover relevant material while adding screening work.
This is not an unavoidable trade between different systems.
A better representation or ranking can improve both at a chosen depth.
Returning the whole indexed collection maximises recall within that collection; returning one highly scored record does not guarantee that it is relevant.

Recall has an awkward practical problem that precision does not.
Measuring it requires knowing how many relevant records the collection holds, and in a live database of hundreds of millions of records nobody knows that number.
Precision only requires judging what came back.
Because of this asymmetry, serious searchers rarely measure recall in the absolute.
They compare instead: run two strategies and see what each finds that the other missed, or seed the evaluation with records already known to be relevant and check how many are recovered.[^recall-denominator] Both are practical.
Neither yields the true denominator.
A reported recall figure should always prompt one question: where did its denominator come from?

#### Where recall is decided {#where-recall-is-decided}

This also settles something left loose in [Chapter 9](#why-search-systems-use-multiple-stages).
A first-stage retriever is fast, shallow and broad; a reranker is slow, careful and narrow.
Their division of labour is exactly the trade above, split across two stages.
A candidate-generating route sets a recall ceiling for everything that processes its fixed output.
Parallel routes or a later retrieval round can expand the cumulative candidate set; reranking the existing set cannot.

Figure 14.1 makes that asymmetry arithmetic: reranking lifts precision@10 and recall@10 together, while recall over the whole candidate pool does not move.

Reranking can bring a relevant paper above the display cut-off only if the paper is already in the candidate pool.
To find a paper missing from that pool, the system needs another retrieval route or search round.

In [hybrid retrieval](#why-hybrid-retrieval-remains-attractive), a second retriever can find a relevant paper the first missed.
In an [agentic loop](#agency-changes-the-sequence-not-the-retrieval), a later search can find one that earlier rounds missed.
Either raises candidate-pool recall when it adds a previously unretrieved relevant paper.
Retrieving duplicates or irrelevant papers leaves that measure unchanged.
Which relevant papers the reader sees still depends on their final ranks and the display cut-off.

:::: {.figure .worked-figure key="reranking-recall-worked"}
Reranking changes what reaches the first page

::: {.include src="figures/reranking-recall-worked.html"}
:::

::: caption
Reranking changes order and therefore which records cross the display boundary.
It adds no candidate.
Precision@10 and recall@10 rise together here, while recall over the full candidate pool remains unchanged.
:::
::::

:::: {.figure .query-flow key="recall-boundary"}
Candidate recall and recall at the displayed depth

::: {.track}
- **Before the boundary** recall is decided here
- **The collection** everything the system could in principle return
- **Candidate generation** one retriever, or several routes pooled together
- **The candidate set** from here on, this is the whole world
:::

::: {.track}
- **After the boundary** ordering and cut-offs determine precision@k and recall@k
- **Fusion order and reranking** the same records, better arranged
- **Cut-off and presentation** how many of them the searcher is shown
- **What the searcher sees** a good ranking of a poor candidate set is still a poor search
:::

::: {.track}
- **Back across the boundary** how to raise the candidate-pool recall ceiling
- **A fresh retrieval pass** a different query, an added source, another route
- **A new candidate set** which starts the top track again
- **Hybrid routes and agentic rounds** both are this, not a later stage of the old set
:::

::: caption
Fusion can raise recall when it is fed by two retrievers, and cannot when it merely orders one list.
:::
::::

The [BM25 Evidence Lab](bm25-evidence-lab.html)’s tour step *The boundary that scoring cannot cross* makes this concrete with six records: set *k* to one and ask what any later stage could do for the record just below the line.

::: {.practice-callout label="Dated methodological note"}
#### Evidence synthesis: current practice, August 2026 {#evidence-synthesis-current-practice}

Cochrane-style systematic reviews still use conventional structured database searching as the formal retrieval core.
In bibliographic databases, those strategies usually combine Boolean logic with controlled vocabulary, free-text terms, fields, proximity and other database-specific operators.
Citation searching and other sources supplement that core.
Neural, semantic and agentic search can also support discovery, query development or screening, but they are not yet generally accepted replacements for the formal primary search.

This describes current methodological practice, not an inherent recall advantage for Boolean retrieval.
A Boolean strategy can miss synonyms, misuse an operator, depend on incomplete indexing or search a database that never contained the study.
Its distinctive property is an inspectable admission rule: within the indexed collection, the conditions for entry can be recorded and examined.

A ranked retriever instead orders records and may expose only a candidate set such as the top *k*.
That boundary is not unique to dense retrieval; BM25 and other ranked methods can impose it too.
High-recall searching is where that boundary costs most, and the empirical question it raises is whether the complete workflow has adequate sensitivity for the task. [Appendix F follows that boundary through retrieval, active-learning screening and stopping](#appendix-evidence-synthesis-high-recall-retrieval).
:::

### Rank changes the question {#rank-changes-the-question}

As [Chapter 3 established](#bm25-ranking), ranked retrieval makes position part of the result.
Precision and recall treat a result list as a bag: a record is either in it or not, and the order is irrelevant.
That is a reasonable description of a Boolean result set exported for screening.
It is a poor description of a ranked list.
There, [position strongly determines what gets looked at](#top-k-is-a-result-boundary-not-a-dense-retrieval-method), and the difference between first place and fortieth matters enormously even though both are in the set.

The simplest repair is to stop measuring the whole list. **Precision@k** is precision calculated over the first *k* results only.
Precision@10 is the usual choice, because ten roughly matches a first page.
Here *k* is an **evaluation depth**: it need not equal the retriever’s top-*k* output boundary or a reranker’s candidate budget.
The measure is easy to explain, and it captures what informal first-page comparisons are usually doing.

Its weakness is that it treats every position inside the cut-off as equal.
A relevant record at rank 1 and the same record at rank 10 score identically; anything at rank 11 scores nothing at all.
Three conventional relevance-only refinements are common enough that a librarian will meet them in vendor material and research papers.
Each encodes a different idea of what a good ranking is.

**Mean reciprocal rank (MRR)** looks only at where the *first* result judged relevant appears, and rewards it for appearing early.
It suits tasks with essentially one right answer: finding a known paper, resolving a citation, answering a factual question.
It is also the natural metric behind a familiar complaint—the right record was there, just too far down.
It is blind by construction to everything after that first hit, so it says nothing about whether a system found one judged-relevant record or fifty.[^mrr-definition]

**Mean average precision (MAP)** rewards a system for placing *many* relevant records high, not merely the first one.
It is the closer fit for the literature-search tasks librarians support, where the aim is a good set rather than a single answer.
Its limitation is that it treats relevance as binary: a record is judged relevant or it is not, and a marginally relevant paper counts the same as a decisive one.[^map-definition]

**Normalised discounted cumulative gain (nDCG)** removes both restrictions.
It accepts graded judgements—highly relevant, partly relevant, not relevant—and discounts each record’s contribution by how far down the list it sits.
A decisive paper at rank 2 therefore counts for more than a marginal one at rank 9.
It is the metric most often quoted when a retrieval system reports an improvement, and the one most worth recognising for that reason alone.[^ndcg-definition]

| Metric | What it rewards | What it ignores | Ask for it when |
|---|---|---|---|
| **Precision@k** | Judged-relevant records inside the cut-off. | Order within the cut-off, and everything beyond it. | You want one number that matches what a user sees on the first page. |
| **MRR** | The first judged-relevant record appearing early. | Every judged-relevant record after the first. | The task has one right answer: a known item, a citation, a lookup. |
| **MAP** | Many judged-relevant records placed high. | Degrees of relevance—everything is relevant or not. | The task is to assemble a set, as in a literature search. |
| **nDCG** | Records with higher relevance grades placed high, discounted by position. | Whether several relevant results repeat the same aspect. | Some records are judged decisively better than others and you can say so. |

: Metrics for a ranked list: what each rewards, what it ignores, and when a librarian would ask for it.

These four measures still treat each record’s judgement independently. [Appendix E explains diversity-aware metrics](#appendix-diversity-aware-ranking-metrics) for tasks that value coverage of several known aspects rather than repeated evidence for only one.

Two cautions about the linked explanations above.
First, they are written for recommender systems, so they speak of *users* and *recommendations* where this book would say *queries* and *results*.
The arithmetic is identical and the substitution is safe.
Second, all four measures need judgements before they can produce anything at all.
That returns the problem to the first section of this chapter: someone has to decide what counted.

> Quoting a metric is choosing a definition of better.
> Ask which one, and whether it is the one your task cares about.

### Test collections, and what a benchmark number is worth {#test-collections-and-benchmarks}

To compare two retrieval systems, something has to be held still.
The standard arrangement fixes three things: a collection of documents, a set of topics or queries, and a set of relevance judgements pairing the two.
Run both systems over the same collection with the same topics, score them against the same judgements, and the difference is attributable to the systems.
That arrangement is the Cranfield paradigm, named for the experiments that established it in the 1960s.
It underpins much offline retrieval evaluation; user studies, online experiments and task-based evaluations ask complementary questions.[^cranfield]

One step in it does not scale.
Judging every document in a collection against every topic is impossible once the collection is large, so evaluations instead use **pooling**: run many different systems, collect the union of their highest-ranked results, judge that pool, and treat everything unjudged as not relevant.
This is a different operation from the pooling that compresses token representations into one vector in [Chapter 6](#model-tokens-are-not-indexed-terms).

That last move is a convenience with a consequence worth stating plainly.
Unjudged is not the same as irrelevant, but the scoring cannot tell them apart.
A retriever that surfaces something genuinely useful which no pooled system found is scored as though it found nothing at all.
That biases the measurement—mildly, and systematically—against approaches unlike the ones already in the pool.[^pooling]

This is the machinery behind the [BEIR](https://arxiv.org/abs/2104.08663) result cited in [Chapter 13](#out-of-distribution) when OOD transfer was introduced.
BEIR assembles retrieval tasks from a range of domains and tests models on collections they were not trained on.
Read the finding properly: BM25 held up across collections it had never seen, judged by other people’s assessors, on other people’s topics.
Several more expensive neural systems did better on average across the same set.
Both halves of that finding are conditional on the same apparatus.

That is why a leaderboard position transfers so poorly to a library.
It is the measurement counterpart of [Chapter 6](#where-the-training-signal-comes-from)’s argument about training data: a model trained on one literature learns that literature’s notion of relevance, and a model *evaluated* on one set of topics has been shown to work for those topics.
Neither says much about a collection of chemistry theses, a non-English corpus, or the queries your researchers actually type.

> A benchmark result is evidence about a benchmark.
> It becomes evidence about your library only when your queries resemble its topics.

### Building an evaluation set you own {#building-a-local-evaluation-set}

The practical response is not to distrust benchmarks but to build a small one of your own.
It need not be a research instrument.
What a library needs is closer to a regression test: a fixed set of queries whose good answers are known, which can be rerun whenever something changes.

The [Local retrieval evaluation kit](evaluation-kit.html) supplies a spreadsheet template, a completed example using Figure 14.1 and a guide to comparing two runs.
It keeps precision at a fixed depth separate from known-seed recovery and shows which judgements or capture details are still missing.

**The queries.** Thirty to fifty is a practical starting range.
Rerunning an established set may fit an afternoon; constructing the needs and judging hundreds of results can take much longer.
Take them from real practice: reference enquiries, interlibrary loan requests, search consultations, questions from database training.
They will then carry the disciplines, languages and document types the library actually holds.
Include, deliberately, the searches already known to go badly.
Those are the ones a vendor demonstration will never contain, and the ones a regression will show up first.

**The judgements.** For each query, record the handful of items that ought to surface.
Exhaustive judgement is neither achievable nor necessary here; known relevant records are enough to detect a system getting worse.
Where staff can distinguish a decisive record from a merely useful one, mark that too—it is what makes graded measures available later.

**The depth.** Judge to a fixed cut-off, ten or twenty results, and keep it fixed.
A stable depth is what makes the exercise both affordable and comparable across runs; a depth that drifts turns a regression test back into an anecdote.
Pool and deduplicate both runs’ results at that depth, then judge every pooled record against the same written criteria, ideally without seeing which run supplied it.
Calculate precision at that depth from those judgements and report known-seed recovery separately.
If a run returns fewer records, report the count and denominator convention, as in [Application exercise III](#exercise3).

Four probes are worth planting on purpose, because each tests a failure this book has already described and no vendor demonstration will include them:

1. An identifier, gene name, chemical string or product code, where exact identity decides relevance—the [gap](#vocabulary-and-representation-gaps) case, and the quickest test of whether an exact lexical route survives.
2. A phrase occurring only in the full text of a paper you hold, which is evidence about the [indexed unit](#one-document-one-chunk-and-one-vector-are-not-the-same-thing) rather than about the ranking.
3. A query whose known relevant record shares almost none of its words—the [mismatch](#vocabulary-mismatch) case, and the one semantic retrieval is supposed to fix.
4. Two near-identical queries with opposite meaning, to see whether [composition](#composition-failure) survives.

| Query | Where it came from, and what it probes | Known relevant | Before: precision@10 | After: precision@10 | What the row records |
|---|---|---|---|---|---|
| `SLC6A4 promoter polymorphism` | Reference enquiry, March 2026. Identifier, where exact identity decides relevance. | 3 | 0.3 | 0.1 | The new expansion drops the gene symbol. This is the regression, and nothing in the release note mentioned it. |
| barriers to adopting learning analytics in further education | Search consultation, January 2026. Vocabulary mismatch: the known relevant records share almost none of these words. | 5 | 0.2 | 0.5 | The intended gain, and the reason the average moved at all. |
| peer support *reduces* readmission / peer support *increases* readmission | Written for the set. Composition: two near-identical queries with opposite meaning, each judged separately; this row reports their mean precision@10. | 4 | 0.4 | 0.4 | No change. Worth keeping precisely because it does not move. |

: Three illustrative rows of a local evaluation set, judged to a fixed depth of ten before and after a hypothetical discovery-layer update.

Six columns, three rows, and a spreadsheet is enough to hold it.
Note what the averages do.
The equally weighted mean of the three displayed rows rises from 0.30 to 0.33 (the third row averages two queries), which a vendor could report as a modest improvement.
Meanwhile the first row lost two thirds of its precision.
That is the asymmetry this chapter has been describing.
The mean is the least informative number in the table, and the row that moved sharply is the one to take to the renewal conversation.

What this produces is not a score worth publishing.
It is a baseline.
Rerun it after a model update, an index change, a platform migration or before a renewal, and a regression that no release note mentioned becomes visible.
That is precisely the failure a library has no other way to catch: [the system underneath a saved search can change without notice](#reproducibility-implication-title).

The obvious objection is that such a set measures your queries against your judgements and generalises to nobody.
That is correct, and it is the point rather than a defect.
It is the only evaluation whose definition of relevance the library chose.

::: {.practice-callout label="Comparison prompt" label-class="callout-label"}
#### Compare ways of supplying evidence {#comparing-evidence-supply}

Using the local needs and relevance judgements developed above, compare an indexed retriever, a file-search agent and, where the collection fits, supplying all its text.
Keep the corpus snapshot, access permissions and answer model fixed.
Document preparation, search-round and context budgets, and how each system stops.
Repeat agent runs to expose variation.

Measure evidence recall against the judged set, support for answer claims, elapsed time and total cost—including preparation, search and generation.
Inspect what was retrieved, what reached context and what the answer used.
Report whole-system results separately from a controlled comparison that changes only the retrieval tool.
A single grep call against a complete vector-search pipeline would not isolate the effect of retrieval method. [Appendix G](#appendix-rag-alternatives) explains the architectural choices.
:::

### What a number cannot settle {#what-a-number-cannot-settle}

Measurement answers a narrow question well: on these queries, against these judgements, which system ranked better.
It does not explain why one lost; that is the diagnosis of [Chapter 13](#diagnosing-failure).
A metric will happily report a decline without indicating whether the cause was vocabulary mismatch, an OOV or representation problem, OOD transfer, a logic failure or a changed cut-off.

Averages are the most common way to be misled.
A benchmark gain of two points is entirely compatible with a system that has become systematically worse on one discipline, one language or one document type, because the mean absorbs it.
The per-query differences are where the information is: a handful of queries that moved sharply matters more than a small shift in the average.
A difference smaller than the run-to-run variation may not be distinguishable from that variation without further evidence.[^significance]

So when a vendor reports an improvement, the useful questions are the ones this chapter has supplied.
On which queries, drawn from where?
Judged by whom, to what depth, and with graded or binary judgements?
Which metric, and against which baseline?
And, most usefully of all: does the gain survive on the queries the library already knows to be hard?

None of this requires reading a loss function or running a significance test.
It requires knowing that a number is a claim about a specific comparison, and asking which comparison it was.

When the product generates an answer as well as a list, a second layer of evaluation questions appears—is the answer faithful to what was retrieved, and does each claim trace to a source that contains it?
Those questions are real, but they are conditioned on the shortlist: a perfectly faithful summary of the wrong ten documents is still the wrong answer. [Appendix G](#appendix-rag-evaluation) explains why groundedness metrics inherit, and cannot detect, the retrieval failures of Chapter 13.

:::: chapter-close
1. Relevance is a relationship among information, a represented need, a person and a situation—not an intrinsic document property.
2. Retrieval metrics measure performance against an operational definition of relevance encoded in human judgements, not objective correctness.
3. Extending a fixed ranking cannot decrease recall, but precision can rise or fall; depth often trades screening burden against recall, and library tasks sit at opposite ends of that trade; a better system can improve both at the same depth.
4. Within a fixed candidate set, later stages can improve ordering but cannot recover exclusions; additional retrieval routes or rounds can expand the cumulative set and increase recall.
5. MRR, MAP and nDCG encode different definitions of a good ranking, so quoting one is choosing one.
6. A benchmark measures performance on someone else’s topics, judged by someone else’s assessors, which is why a leaderboard position does not transfer.
7. A local evaluation set is the one measurement whose definition of relevance the library chose, and its value lies in being rerun.

::: {.chapter-transition}
Measurement can tell a library which system to prefer.
It cannot say what happened inside any particular search, or make that search repeatable a year from now.
The final chapter turns to what has to be recorded, inspected and required.
:::
::::

::: self-check
Within a fixed candidate set, what creates the recall ceiling—and how can cumulative recall still increase later?

:   The candidate-generating route creates the ceiling for stages that only process its fixed output: reranking and generation cannot recover excluded records.
    Another retrieval route or round can expand the cumulative candidate set and increase recall.

A vendor reports a 3% nDCG improvement. Name three things you must know before that number says anything about your library.

:   Which collection and which topics; whose relevance judgements, binary or graded, and to what depth they were judged; and which baseline the gain is measured against.
    Then a fourth: whether it survives per-query on the searches you already know to be hard, because a mean can hide one discipline getting steadily worse.

Why is recall harder to measure than precision in a live database, and what do practitioners use instead?

:   Recall needs the number of relevant records the collection holds, and nobody knows that for a database of hundreds of millions.
    Precision only needs judging what came back.
    The substitutes are relative recall — scoring against the relevant records identified in the pooled union of several strategies — and known-item seeding.
:::

[^precision-recall-definitions]: **Precision** is the proportion of retrieved records that were judged relevant; **recall** is the proportion of all judged-relevant records that were retrieved.
    As fractions, both share the numerator “judged relevant and retrieved” and differ only in the denominator—everything retrieved, against everything judged relevant.
    The two are sometimes combined into an **F-measure**, their harmonic mean, which is convenient for reporting a single number and obscures exactly the trade-off this section is about.

[^recall-denominator]: Two substitutes are common. **Relative recall** uses the judged-relevant records in the deduplicated union of several strategies as the denominator, scoring a strategy against its peers rather than against the truth. **Known-item seeding** fixes a small set of records known in advance to be relevant and measures how many are recovered — the approach behind both the seed-testing step in systematic-review search validation and the local evaluation set described later in this chapter.

[^mrr-definition]: For each query, take the rank of the first result judged relevant and use its reciprocal: rank 1 scores 1, rank 2 scores 0.5, rank 4 scores 0.25. **Mean reciprocal rank** averages that across queries.
    Note how fast it decays—the penalty for slipping from first to second place exceeds the penalty for slipping from fifth to fiftieth.
    Evidently AI, “[Mean Reciprocal Rank (MRR) explained](https://www.evidentlyai.com/ranking-metrics/mean-reciprocal-rank-mrr).”

[^map-definition]: **Average precision** for one query sums the precision values at ranks where judged-relevant records appear, then divides by the total number of known relevant records; known relevant records not retrieved contribute zero; **mean average precision** averages that across queries.
    Because precision is recomputed at every hit, records found early lift the score more than records found late.
    Evidently AI, “[Mean Average Precision (MAP) in ranking and recommendations](https://www.evidentlyai.com/ranking-metrics/mean-average-precision-map).”

[^ndcg-definition]: **Discounted cumulative gain** sums the judged relevance grade of each result divided by a logarithm of its position, so later positions contribute less. **Normalising** it against the score the ideal ranking would have achieved puts the result on a 0–1 scale comparable across queries holding different numbers of judged-relevant records.
    Proposed by Järvelin and Kekäläinen (2002).
    The logarithmic discount is conventional rather than derived from anything, which is the standard criticism of it.
    Evidently AI, “[Normalized Discounted Cumulative Gain (NDCG) explained](https://www.evidentlyai.com/ranking-metrics/ndcg-metric).”

[^cranfield]: The Cranfield experiments, run by Cyril Cleverdon at the College of Aeronautics through the 1960s, compared indexing languages over a fixed document set with fixed questions and judgements.
    It is the experimental design rather than the findings that endured; TREC has run the same arrangement at far larger scale since 1992.

[^pooling]: The distortion has been measured rather than merely worried about.
    Buckley and Voorhees examined how far incomplete judgements affect system comparisons and proposed measures less sensitive to unjudged documents.
    The practical caution stands: the system whose results overlap least with the pool is the one most likely to be scored unfairly.

[^significance]: Retrieval scores vary with the sample of queries, so a small difference between two means may not survive a different query set.
    Research papers normally report a significance test over per-query scores for that reason.
    A library rerunning its own set needs the instinct rather than the statistics: look at which queries moved, and by how much, before believing a change in the average.
