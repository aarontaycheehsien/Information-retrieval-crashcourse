---
key: "appendix-evidence-synthesis-high-recall-retrieval"
kind: "appendix"
eyebrow: "Appendix F"
meta: "About 17 min · core for the evidence-synthesis route"
section_id: "app-F"
---

## Evidence synthesis as a high-recall retrieval problem {#appendix-evidence-synthesis-high-recall-retrieval}

Systematic reviews make the boundaries of a retrieval pipeline unusually consequential.
Candidate retrieval determines which records enter the pool; technology-assisted review (TAR) determines which of those records are screened first; and a stopping rule determines which records, if any, are never screened.
These are distinct stages and distinct possible recall failures.

This appendix is not a guide to conducting a systematic review.
It applies the book’s earlier distinctions—candidate generation, ranking, retrieval feedback, screening feedback, recall and reproducibility—to a setting in which a missed record may change an evidence base.
The central question is not whether one method is labelled Boolean, BM25, dense, neural or AI.
It is where a workflow stops making potentially eligible evidence available for human assessment.

### Why systematic reviews stress-test retrieval systems {#systematic-reviews-stress-test-retrieval}

Ordinary ranked search often asks, “Which useful records should appear first?”
Evidence synthesis adds a second question: “Which potentially eligible records were never made available for assessment?”
A good first page is not enough if the task is to identify a broad body of studies rather than satisfy one information need quickly.

This is the precision–recall choice from [Chapter 14](#precision-and-recall) under unusually demanding conditions.
Searchers aim for high sensitivity, commonly accepting a large screening burden to reduce the chance of missing eligible studies.
Yet literal 100% recall is neither observable nor assured.
The true denominator—every relevant study that exists—is normally unknown.
Even a fully screened database result set says nothing about studies absent from that database, records indexed inadequately, unpublished studies or reports expressed in language the strategy missed.

> **High recall is an objective, not a guarantee.**

Coverage and retrieval must therefore be kept apart.
Source selection decides which records could in principle be found.
Candidate generation decides which indexed records enter the result set.
In a multi-stage ranked pipeline, the first candidate set creates a [recall ceiling](#why-search-systems-use-multiple-stages) for every reranker and generator downstream.
Relative recall, known relevant studies and fully labelled benchmark datasets can test parts of that process, but none reveals every relevant item in the world.

Reading a supplied collection in a [long context window](#appendix-rag-long-context), or searching local files with an agent, does not establish how that collection was assembled.
Assess discovery coverage separately from the quality of answers about the documents already available.

### Current practice as of August 2026 {#evidence-synthesis-current-practice-august-2026}

The current [Cochrane Handbook](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04), checked in August 2026, requires extensive searching of bibliographic databases and other sources, describes strategies built from free-text and controlled-vocabulary terms joined with Boolean operators, and treats machine learning primarily as a way to categorise or prioritise the results of broad, sensitive searches.
On that basis, conventional structured database searching remains the formal retrieval core for Cochrane-style systematic reviews.
Citation searching, registers, websites and other supplementary sources are also important; “core” does not mean “only.”

:::: {.figure key="evidence-synthesis-workflow"}
Formal retrieval and supplementary discovery both contribute candidates

::: {.include src="figures/evidence-synthesis-workflow.html"}
:::

::: caption
The distinction is methodological rather than architectural.
Current Cochrane-style practice gives structured database strategies a formal primary role while allowing other routes to add candidates.
:::
::::

This is a statement about current evidence-synthesis methodology, not an immutable law of information retrieval and not proof that Boolean retrieval inherently has higher recall.
Neural, semantic and agentic systems should currently be presented as supplementary rather than general replacements for the formal primary search.
Future neural or hybrid systems could take a larger role if their sensitivity, robustness across topics and populations, coverage, documentation and reproducibility are demonstrated adequately for high-recall use.

### Boolean admission versus ranked candidate boundaries {#boolean-admission-and-ranked-candidate-boundaries}

A structured Boolean strategy defines an explicit inclusion rule over the records represented in a database’s index.
Its lines can combine subject headings, free-text synonyms, phrases, fields, proximity, limits and exclusions using the syntax that database supports.
A searcher can inspect the rule, edit it, peer-review it and report it.
That makes the admission boundary visible.

Visibility is not completeness.
A missing synonym, an over-restrictive concept block, a mistaken `NOT`, poor subject indexing, a field that omits useful text, terminology mismatch or incomplete database coverage can exclude an eligible study.
The rule may also behave differently as indexing and platform implementations change.

> **Boolean retrieval gives an explicit admission rule, not guaranteed completeness.**

Ranked retrieval creates a different kind of boundary when only part of the ranking is exposed.
BM25, learnt sparse, dense and hybrid systems can all score records and return the leading *k*.
Suppose a pipeline sends its first 2,000 candidates to a later stage and an eligible study is ranked 2,001st.
A reranker cannot recover that study because it never received it.
The example does not show that 2,000 is inadequate; it shows what must be tested.
The question is whether the chosen boundary has adequate empirical sensitivity on the task and population at hand.

> **Top-*k* is not a dense-retrieval issue.
> It is a ranked-retrieval boundary issue.**

### Candidate retrieval is not screening prioritisation {#candidate-retrieval-is-not-screening-prioritisation}

Candidate retrieval asks, “Which records enter the screening pool?”
TAR or active-learning screening asks, “Given that pool, which record should be screened next?”
Collapsing the two hides where a miss occurred.
A screening model cannot learn from or promote a record that the searches never retrieved.

:::: {.figure key="tar-active-learning-loop"}
Active learning repeatedly reprioritises a fixed candidate pool

::: {.include src="figures/tar-active-learning-loop.html"}
:::

::: caption
Labels from screening become screening feedback.
The loop changes the order of the records that remain; it does not inherently add records to the original candidate pool.
:::
::::

::: {.orientation tag="div"}
**A quieter decision in the same place:** the pool reaches screening *deduplicated*, and near-duplicate matching across databases is a rule someone chose.
Records are merged on identifiers, or on title, author and year compared with some tolerance.
Set that tolerance loosely and a conference abstract can be absorbed into a later journal article, or two genuinely different papers merged on similar titles; set it tightly and the screening burden rises.
Either way, no human eligibility judgement was made about a record that disappeared here.

This is not a fourth boundary in the sense of the three below — it removes records thought to be copies of ones already in the pool, not records the workflow never reached — but it is worth recording with the same care: which fields were compared, at what tolerance, in which software, and how many records it removed.
That is why deduplication appears in the reporting list further on rather than only in a methods sentence.
:::

If every candidate is eventually screened, active learning changes order and workload distribution, not the final coverage of the pool.
It may find eligible studies much earlier, which is valuable for efficiency and living reviews, but no record is excluded solely because of its model score.
Coverage changes only if another retrieval route adds records, a reviewer makes a screening error, or screening stops before the pool is exhausted.

### TAR describes a workflow, not a representation {#tar-is-a-workflow-not-a-representation}

TAR names an arrangement of human judgements, model updates and prioritised screening.
It does not identify how text is represented or which classifier is fitted.
Implementations have used bag-of-words and TF-IDF features, logistic regression, Naive Bayes and support-vector machines, as well as dense embeddings, Transformer encoders and neural classifiers.

[ASReview](https://doi.org/10.1038/s42256-020-00287-7) makes this modularity concrete.
Its pipeline separates a feature extractor, classifier, query strategy and balancing method. [Current ASReview workflows](https://asreview.nl/blog/asreview-model-selection-guide/) include sparse lexical feature representations such as TF-IDF and dense embedding options such as SBERT or LaBSE, sometimes through an extension.
A sparse feature extractor can feed a learnt classifier; a dense embedding does not by itself decide which record is shown next.

::: {.table scope="row"}
| Stage | Sparse representation | Dense representation |
|---|---|---|
| Candidate retrieval | Structured Boolean retrieval; BM25 or learnt sparse ranking | Dense-vector retrieval |
| TAR screening | TF-IDF or bag-of-words features with a classifier | Dense embeddings with a classifier |

: Retrieval stage and representation are independent dimensions.
:::

Hybrid retrieval can combine sparse and dense representations.
Neural models can produce either: learnt sparse retrieval belongs in the sparse column even though its weights are learnt by a neural network.

### Prioritisation versus early stopping {#prioritisation-versus-early-stopping}

The central methodological distinction within TAR is between ranking the queue and deciding not to finish it.
If TAR merely changes the screening order, no record is excluded solely because of the model.
If screening stops early, the unscreened tail has effectively been excluded even though no record in it received a human eligibility judgement.

:::: {.figure key="evidence-boundaries"}
Three boundaries can remove relevant evidence

::: {.include src="figures/evidence-boundaries.html"}
:::

::: caption
A relevant study may be absent from the available sources, excluded during candidate retrieval, or left in the unscreened tail.
Prioritisation is shown separately because reordering the queue does not itself remove records.
A downstream stage cannot repair an upstream exclusion.
:::
::::

Retrieval top-*k* and TAR stopping are different mechanisms, but both create recall boundaries.
A candidate limit prevents records from entering the screening pool.
A stopping rule acts later, after the records have entered, by determining how much of a prioritised queue will actually be assessed.

### How ASReview active learning works {#how-asreview-active-learning-works}

ASReview begins with a candidate dataset, normally containing titles and abstracts produced by searches and deduplication.
The reviewer supplies initial prior knowledge or screens enough records to obtain relevant and irrelevant labels.
The selected feature extractor represents the records, the classifier learns from the labelled examples, and the query strategy selects which unscreened record to present.
Because relevant records are usually rare, a balancing method may alter how the labelled classes contribute during fitting.

The reviewer labels the presented record relevant or irrelevant.
ASReview adds that judgement to the training data, refits the model and reorders the remaining records.
The human remains the source of the eligibility decision; the model estimates which record is most useful to show next.
The cycle continues until the candidate pool is exhausted or the reviewer decides to stop.

This modular account is more informative than saying the software “uses AI.”
TF-IDF with Naive Bayes and SBERT embeddings with a classifier can participate in the same active-learning workflow.
Their representations and ranking behaviour differ, but neither changes the fact that ASReview operates on an imported pool rather than replacing the searches that formed it.

### When is it safe to stop? {#when-is-it-safe-to-stop-screening}

Ranking performance and stopping are separate problems.
A model may bring relevant records forward efficiently while leaving a few unusual ones deep in the queue.
The reviewer cannot see that tail’s true relevance labels without screening it, so the moment at which all—or enough—eligible records have been found is unknown in a live review. [Byrne and colleagues’ time-to-discovery study](https://doi.org/10.1186/s13643-024-02587-0)—not a proposal for a stopping rule—found that active-learning model choice, especially the feature representation, materially affected how late elusive relevant papers were discovered.
An apparently barren stretch can therefore reflect the ranking and representation rather than an empty tail.

#### Fixed effort

A team may stop after screening a fixed number or percentage of records.
This is easy to plan and report, but the threshold is unrelated to how many relevant records remain.
The same percentage can be ample in one dataset and unsafe in another.

#### Consecutive irrelevant records

A long run without a newly relevant record suggests that the ranking has become less productive.
It does not prove that no relevant record remains farther down.
Clusters of terminology, study design or population can separate relevant records within the representation space.

#### Known-item or key-study rules

Reviewers can hold out studies already known to meet the criteria and test whether the workflow recovers them.
This checks the system against concrete failures and is useful for search validation.
Recovering known studies does not establish that unknown eligible studies are absent, and known items may be more prominent or lexically typical than the studies most likely to be missed.

#### Estimated recall and population estimation

Other approaches estimate how many relevant records exist in total or remain unseen, then stop when the estimated recall reaches a target:

::: {.math tag="div"}
$$
\widehat{\mathrm{Recall}} = \frac{\text{relevant records found}}{\text{estimated total relevant records}}.
$$
:::

The denominator is an estimate, not a newly discovered ground truth.
Proposed methods include random sampling with confidence bounds, capture–recapture, Chao-type population estimation and probabilistic models of remaining relevance.
Their assumptions and uncertainty determine what the resulting recall claim means.

#### ASReview’s stopping interface {#asreview-stopping-interface}

In the [ASReview LAB interface](https://asreview.readthedocs.io/en/stable/lab/progress.html), a reviewer can set a threshold for the number of consecutive irrelevant records since the most recent relevant record.
Reaching the threshold triggers a prompt; the user decides whether to stop or continue.
No threshold is set by default, and the documentation describes the ideal value as an active research question.[Interface documentation checked August 2026.]{.as-of}

This is a useful signal of declining yield, but it remains a heuristic unless a stronger validation supports the chosen threshold in the relevant context.
“The ranking has become less productive” and “we have demonstrated sufficient recall” are not the same claim.

### SAFE as a more conservative stopping framework {#safe-as-a-conservative-stopping-framework}

The [SAFE procedure](https://doi.org/10.1186/s13643-024-02502-7) is named for its four phases: **screen** a random training set, **apply** active learning, **find** more relevant records with a different model, and **evaluate** quality.
It responds to the weakness of single signals by combining several checks.
The procedure begins with an initial sample for training and calibration, proceeds through active-learning screening with several provisional conditions, switches to a different model to look for records the first configuration may have buried, and ends with a quality-control phase that revisits possible false exclusions and can incorporate citation searching.

The published procedure supplies example percentages, minimum counts and irrelevant-record runs, but explicitly warns that those numbers are arbitrary rather than universal rules.
Its enduring lesson is architectural: stopping deserves its own method, evidence and audit trail.

### There is no magic *k* and no magic streak length {#no-magic-k-and-no-magic-streak}

Recent validation makes the variation visible. [Kempny and colleagues](https://doi.org/10.1186/s12874-026-02866-5) ran 35,000 ASReview simulations over five fully labelled datasets.
The average proportion needing screening before the last known relevant record appeared ranged from 2.9% to 76.9%, and none of the tested fixed-percentage, consecutive-irrelevant or estimated-count criteria worked universally. [König and colleagues](https://doi.org/10.1002/jrsm.1762) likewise found that knee, heuristic and prevalence-estimation stopping rules behaved differently across psychological meta-analysis datasets and prevalence levels.

Stopping performance varies with the dataset, prevalence of relevant studies, heterogeneity of the review question, clustering of relevant records, initial labels, model choice and feature representation.
A method that works for a narrow, cohesive topic can perform differently when eligible studies use several vocabularies or span disciplines and designs.

> **There is no universal magic “*k*” for retrieval, and there is no universal magic number of irrelevant records after which screening is safely complete.**

::: {#statistical-and-decision-based-stopping .legacy-anchor}
:::

### For awareness: statistical and decision-based stopping {#for-awareness-statistical-and-decision-based-stopping}

Stopping remains an active research problem.
Statistical target-recall approaches, such as the [Callaghan–Müller-Hansen (CMH) method](https://doi.org/10.1186/s13643-020-01521-4), use information from the remaining unseen records to ask whether a specified recall target has probably been reached at a stated confidence level.
The original CMH workflow combines prioritised active-learning screening with random sampling of the remaining unseen records; it does not treat a long run of exclusions as proof that few relevant records remain.
A [2026 comparison by Repke and colleagues](https://doi.org/10.1002/cesm.70068) evaluated 15 stopping methods in simulations using 81 real-world datasets.
CMH was the only evaluated method that consistently met the specified recall targets in those simulations, but it did so conservatively, often requiring substantially more screening than the theoretical minimum.
A stopping method can therefore be safer precisely because it gives up some potential workload reduction.
Other statistical approaches make different assumptions.
Capture–recapture and [Chao-type estimators](https://doi.org/10.1145/3724116) treat the unseen relevant population as something to estimate from observed discoveries. [Point-process stopping methods](https://doi.org/10.1145/3631990) instead model where relevant records occur along the ranked screening sequence and use that distribution to estimate when sufficiently few remain.
These methods all address stopping, but they do not estimate exactly the same thing or provide identical guarantees.

A different family asks what continued screening is worth. [Decision-theoretic stopping](https://doi.org/10.1145/3805712.3809548) represents the costs of continued screening, the costs of missing evidence and the expected value of further information explicitly.
Related but conceptually distinct [conclusion-oriented approaches](https://doi.org/10.1145/3805712.3809924), such as Fletcher and Stevenson’s confidence-based methods, ask whether the accumulated evidence is sufficient to support the substantive conclusion rather than whether a target fraction of relevant documents has been found.
Target-recall stopping asks, “Have we probably found at least 95% of the relevant records?”
Conclusion-oriented stopping instead asks, “Would additional evidence probably change the conclusion?”
The latter may fit some decision tasks, but it changes the claim being made; it is not a replacement for high-recall stopping in conventional systematic reviews and should not be presented as solved or universally accepted practice.

### Metrics commonly encountered in TAR research {#metrics-in-tar-research}

TAR papers often use the same words as general retrieval evaluation but measure them at a screening depth or stopping point.
The denominator normally comes from a fully labelled evaluation dataset, not from all relevant literature that might exist.

::: {.table scope="row"}
| Measure | What it reports | Important limitation |
|---|---|---|
| Recall@*k* | $$R@k = \frac{\text{known relevant records in the top }k}{\text{known relevant records}}$$ | Recall against the evaluation set at depth *k*; not proof of complete real-world recall. |
| Recall at stopping | The proportion of known relevant records found before a stopping rule terminates screening. | Requires labels for the records that the simulated stop would have left unseen. |
| WSS@95 | Work saved over random sampling at the same 95% recall target in the known evaluation set: conventionally, 0.95 minus the fraction screened to reach that target. | Shows ranking efficiency at that target, not whether a live reviewer can know safely when 95% has been reached. |

: Three measures used to interpret TAR experiments.
:::

For example, suppose 95 of 100 known relevant records have been found after screening 300 of 1,000 records.
The screened fraction is 0.30, so **WSS@95 = 0.95 − 0.30 = 0.65**: 65 percentage points of the pool saved over the random-sampling baseline.
The fraction left unscreened is 70%, a different quantity; random sampling would itself leave 5% unscreened at 95% expected recall.
This is the [conventional WSS definition](https://dmice.ohsu.edu/hersh/jamia-06-sysrev.pdf), which counts records rather than minutes of reviewer time.

### Applying Chapter 15 to active learning {#reproducibility-of-active-learning-screening}

[Chapter 15’s principle](#reproducibility-implication-title) still applies: reproducibility depends on what was fixed, documented, exportable and versioned.
TAR adds a changing ranking and a human–model interaction, so recording only the database strategies or final included studies leaves a large part of the process invisible.

A useful TAR record should identify:

- the original candidate pool, databases, platforms, searches, dates and supplementary methods that generated it;
- deduplication and any removal or enrichment before screening;
- software and version, feature representation, classifier, query or sampling strategy and balancing method;
- initial seeds or prior records, including how they were selected;
- screening labels and order, including corrections and reviewer reconciliation;
- the stopping rule, threshold, rationale and any model switch or final quality-control pass;
- the number screened, the number left unscreened and the status of those remaining records; and
- an exported project, dataset or audit log sufficient to reconstruct the sequence where licensing permits.

PRISMA-S supplies the reporting logic for searches; it neither prohibits neural discovery nor makes a stopping decision reproducible by itself.
TAR documentation extends the execution record downstream from retrieval into screening.

::: {.orientation tag="div"}
**For the TAR comparison:** use a classifier that accepts both non-negative TF–IDF and signed dense features, such as a consistently configured linear classifier.
Do not feed signed embeddings to a multinomial naïve Bayes model.
Keep seeds, labels, candidate pool and evaluation depth fixed.

**A non-coding route:** give students screening logs from two prepared runs and ask them to plot relevant records found against records screened, then compare performance at fixed screening budgets.
In a fully labelled teaching collection, calculate achieved recall directly.
If a stopping condition uses estimated recall instead, specify the estimator, implementation version, confidence rule and threshold; do not treat an unspecified estimate as reproducible or guaranteed.
:::

### A controlled TAR comparison {#controlled-tar-comparison}

A useful exercise can separate representation from stopping without attributing corpus differences to algorithms.
Use the fully labelled `synergy:van_de_schoot_2018` benchmark available through [ASReview’s simulation interface](https://asreview.readthedocs.io/en/stable/lab/simulation_overview.html).
Treat its labels as the known evaluation set, not as a complete gold standard for every relevant publication.

1. Fix the corpus, deduplication, text fields, initial relevant and irrelevant seeds, random seeds, classifier, query strategy and balancing method.
2. Compare random screening order, TF-IDF active learning and dense-embedding active learning.
   Between the two active learners, vary only the feature representation.
3. Record how quickly known relevant studies are found and calculate recall after screening 10%, 20% and 30% of the pool.
4. Apply four clearly illustrative stopping procedures: a fixed 20% effort limit, a run of 50 consecutive irrelevant records, recovery of held-out known studies, and an estimated-recall target.
   For each, report the known relevant records left unseen.
5. Ask: did the representation mainly affect ranking efficiency, or did the stopping rule determine final recall?

The numerical thresholds are experimental conditions, not recommendations.
Because the dataset is fully labelled, the exercise can reveal what each simulated stop would have missed; a live review cannot inspect that counterfactual tail without doing the work it hoped to save.

An optional second experiment can compare Boolean, BM25, dense and hybrid candidate retrieval over the same document corpus.
Keep it separate from the TAR experiment.
Candidate retrieval changes what enters the pool; active learning changes the order within a supplied pool.
Combining both interventions in one comparison would make the source of any recall difference ambiguous.

### Candidate retrieval and TAR compared {#candidate-retrieval-and-tar-compared}

::: {.table scope="row"}
| Dimension | Candidate retrieval | TAR screening |
|---|---|---|
| Input | Information need and searchable sources | Retrieved candidate pool |
| Main question | What enters the pool? | What should be screened next? |
| Main recall risk | A relevant record lies outside the candidate boundary. | Screening stops before a relevant record is assessed. |
| Can downstream stages recover the miss? | No—not unless another retrieval route adds the record before the pool is fixed. | No—not after the queue has been closed and the tail left unscreened. |
| Current evidence-synthesis role | Structured searching remains the formal primary approach; neural and agentic retrieval are supplementary. | Machine-learning prioritisation is accepted more readily; safe early stopping remains methodologically difficult. |

: Candidate retrieval and TAR create different decision points and different recall risks.
:::

::: pull-quote
> The central high-recall problem is not whether a system is Boolean, BM25, neural, dense or AI.
> It is where the workflow creates a boundary beyond which potentially relevant evidence is no longer examined, and what evidence justifies that boundary.
:::

---
