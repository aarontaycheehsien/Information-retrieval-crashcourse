# Evidence-synthesis specialization plan — reconsidered recommendation

Date: 2026-10-21  
Source branch: `fable-1`  
Reviewed commit: `99bfb9c5f4aaa8a9722c28559950ea17e8c399c5`  
Working branch: `evidence-sythesis`  
Status: Revised editorial recommendation. The [initial proposal](evidence-synthesis-plan-2026-10-21.md) is preserved separately in commit `ce9db34b6f294c356e36d5d4355fa88f1fe8d962`. Neither document implements changes to the textbook.

The revised recommendation is to make a major change to the book's organizing questions, preserve more of its explanation of retrieval, and add a smaller amount of carefully chosen evidence-synthesis practice. The first proposal would expand into a broad search-methods manual while removing too much of the material that distinguishes this book.

A suitable working title is *How Search Finds and Misses Studies: Information Retrieval for Evidence Synthesis*.

The primary reader is a librarian who can construct Boolean searches and is developing or practising evidence-synthesis support. Readers need enough review-methods context to understand the examples, but they should not have to learn the entire review process here. A short prerequisite guide can support readers who are new to evidence synthesis.

The book's promise should be: **understand how retrieval decisions change the evidence available to a review, diagnose failures, and evaluate proposed improvements.**

**What changes after reconsideration**

| Initial recommendation | Revised recommendation | Reason |
|---|---|---|
| Roughly one-third mechanisms and two-thirds applied work | Allocate space according to the decisions a mechanism helps explain; set length targets after drafting a sample chapter | The ratio was an editorial guess. Removing explanatory dependencies can make the apparent simplification harder to learn. |
| Compress Chapters 5–10 into one or two core chapters | Retain a chapter on representations and retrieval training, a chapter on multi-stage and hybrid retrieval, and move indexed-unit material into the earlier coverage chapter | Task training, candidate selection and searchable evidence explain different failure modes. Combining them too tightly would obscure the distinctions. |
| Add several substantial chapters on established search practice | Use concise worked examples, method notes and a prerequisite companion; add fuller treatment where retrieval mechanics change a decision | The original book assumes search expertise. Re-teaching all search practice would enlarge its scope substantially. |
| Make Appendix F central | Split its opening framework, screening material and documentation guidance across the book | Its distinction between retrieval and screening is essential, but its concentration on TAR should not determine the balance of the whole edition. |
| Expand validation beyond the first page | Make evaluation design the main new contribution, distinguishing supplementary use, replacement and screening | These are different claims and require different comparisons. |
| Build toward a complete search-methods portfolio | Build toward a documented decision about one retrieval workflow, supported by a search record, comparisons and uncertainty | This directly tests the knowledge the book teaches. |

**The conceptual material that must survive**

The initial plan was too aggressive about treating model training as expendable technical detail. [Chapter 6](../search-textbook.html#retrieval-encoder) explains that citation links, clicked results, answer passages and human relevance labels teach different notions of relevance. That is directly relevant to a librarian assessing a tool trained to find related papers but deployed to identify studies meeting explicit criteria.

Retain a simple account of positives and negatives, the task rewarded during training, and transfer across disciplines, languages and retrieval purposes. Remove the requirement to follow specific loss functions or the full history of language-model architectures. One worked contrast between a topically related report and an eligible report can carry the argument.

Similarly, [Chapter 8's distinction between source documents, indexed units and result aggregation](../search-textbook.html#one-document-one-chunk-and-one-vector-are-not-the-same-thing) belongs early in the core. The following are separate questions:

- Is a report covered by the source?
- Which fields or passages are actually searchable?
- What can the query or retriever match?
- How are matching passages grouped into reports?
- How do retrieved reports relate to studies?

A statement that a product searches full text does not answer all five. Some systems can retrieve an abstract and subsequently fetch full text; the text available at each stage needs to be explicit.

Preserve the practical explanations of Boolean eligibility, ranked lexical retrieval, dense and learnt sparse representations, reranking, hybrid retrieval and query transformation. Teach each through the evidence it preserves, the evidence it can lose, and the test a librarian could run. Keep a short architecture map for reading research and vendor documentation; reduce terminology recall as an assessment goal.

**A revised sequence of ten chapters**

Evaluation principles appear in Chapter 1 and in the exercises throughout; Chapter 9 brings them together into a complete comparison protocol.

| Chapter | Decision the reader should be able to make | Main source material and additions |
|---|---|---|
| 1. What counts as finding the evidence? | Distinguish topical relevance, review eligibility, candidate retrieval, screening and the unit being counted | Rework Chapter 1, the opening of Appendix F and the essential precision/recall concepts from Chapter 14 |
| 2. What the searchable collection makes possible | Identify coverage, indexing lag, field, passage and access limits before changing a query | Chapter 8's indexed units, Chapter 13's initial diagnostic checks, and a focused source-coverage case |
| 3. Queries as decisions about eligibility | Explain why a concept, heading, field, proximity rule, translation or limit excludes records | Chapters 2 and 11, one annotated search-development and translation case, and a short PRESS note |
| 4. Ranked lexical retrieval and result limits | Distinguish a ranking change from a change in the set available for export or screening | Combine Chapters 3–4 and selected candidate-boundary material from Chapter 7 |
| 5. What a representation learns to retrieve | Assess whether training signals and representations suit the review's task and vocabulary | Selected Chapters 5–8, with training-task mismatch and exact-match cases |
| 6. Candidate generation, reranking and hybrid retrieval | Locate which route can add evidence, which stage reorders it and where cutoffs remove access | Chapters 9–10, with a compact mechanism map and a controlled comparison |
| 7. Combining search routes and controlling automation | Choose and document complementary keyword, citation, similarity, feedback and agentic routes | Chapters 11–12, with source provenance, seed dependence and inspectable execution traces |
| 8. Screening prioritisation and stopping | Separate ranking efficiency from a defensible decision to leave records unexamined | Appendix F, with supplied screening logs, uncertainty and quality-control examples |
| 9. Validating a retrieval workflow | Design a comparison that supports the particular claim being made and investigate its misses | Substantial reworking of Chapters 13–14, plus the evaluation design below |
| 10. Documenting and maintaining the search | Preserve inputs, outputs, provenance, changes and enough evidence to compare an update | Selected Chapter 15 and Appendix F, PRISMA-S application, record reconciliation and an update case |

The source-coverage and query chapters should explain why familiar practices work and where they fail. They should not grow into catalogues of databases or comprehensive guides to every review type.

Different review traditions need short, explicit context notes. Do not generalise the existing Cochrane-style account into a universal hierarchy in which all citation searching is supplementary or all evidence syntheses use the same stopping logic. Explain the methodological role of each route in the particular review. Validate guidance against the applicable current methods source when drafting.

**The largest new contribution: evaluating the claim actually being made**

The current [Chapter 14](../search-textbook.html#evaluation) already explains unknown recall denominators, known-item recovery, pooling and the limits of aggregate scores. Preserve that work. Its top-ten or top-twenty comparison is appropriate for a local discovery regression check; a specialist edition needs additional evaluation designs.

| Proposed use | Main comparison | Essential qualification |
|---|---|---|
| Add a citation, semantic or agentic route | Eligible evidence added to the existing search, with additional screening and search effort | Useful additions do not establish complete recall or justify replacing the baseline |
| Replace an existing search route | Recovery and misses against a credible, explicitly bounded reference set across several relevant review topics, with comparable effort and scope reported | Recovering familiar seeds on one topic is insufficient evidence for broad substitution |
| Change a retrieval component | Compare methods over the same corpus, fields and eligibility labels, controlling other relevant settings | This isolates a mechanism but does not establish performance across different commercial collections |
| Select between complete products | Compare the available services as used, documenting differences in coverage, access, limits and workflows | Coverage differences are part of the service comparison; do not attribute the entire result to the ranking model |
| Prioritise screening | Relevant records found at fixed screening effort, with a fixed candidate pool | A better order does not enlarge the pool |
| Stop screening early | Misses at the stopping point in labelled simulations, variability and any method-specific uncertainty assessment | Good ranking efficiency does not establish that the target has been reached in a live review |
| Maintain a living or updated search | Newly found eligible reports, indexing delays, revised strategies and changed product behaviour | Reusing a saved query alone does not establish stable coverage |

Teach an evaluation protocol readers can actually complete:

1. Specify the task, eligibility criteria and unit of analysis before inspecting the comparison.
2. State whether the claim concerns supplementary discovery, replacement, mechanism performance, screening or updating.
3. Record corpus coverage, fields, query inputs, limits, seeds, transformations, export depth, dates and versions where available.
4. Separate search-development records from held-out validation records where feasible. If there are too few independent known records, report that limitation rather than manufacture independence.
5. Pool and reconcile the compared outputs while retaining all source memberships. Apply consistent eligibility judgements and record unresolved cases.
6. Report recovery against the stated reference set, eligible additions, workload and the characteristics of misses. Define denominators and distinguish known-item recovery from complete recall.
7. Test more than one topic when making broader claims. For stochastic or adaptive methods, examine variation across runs or initial seeds as appropriate.
8. Preserve a record of what remains unknowable from the available outputs.

Explain that unique contribution and incremental contribution are different. A route can overlap extensively with another while still finding important evidence. Incremental yield depends on the baseline and the order of addition; it is not a permanent property of a database or tool.

Include benchmark limitations: a published review's included studies are an incomplete reference standard, not the universe of eligible evidence. Development records and evaluation records can overlap; models may also have encountered public review topics or labels during training. These risks should limit the claim made, without making useful local comparisons impossible.

Use one simple, explicitly synthetic example throughout: a fully labelled teaching collection contains 100 eligible reports; retrieval admits 90, and screening stops after identifying 81 of those. Retrieval recall is 90%, recall within the retrieved pool is 90%, and end-to-end recovery is 81% against that teaching reference set. No independence assumption is required for this nested-set arithmetic. A live review normally does not know the corresponding total.

Also show retrieval feedback loops. Additional searches can expand the candidate pool after an initial failure; the teaching diagram must not imply an irreversible, one-pass sequence. A reranker acting on a fixed pool cannot recover an excluded report, while a fresh retrieval route may.

**Practice additions with a tighter scope**

- **Search construction and translation:** one complete annotated example, with an over-restrictive concept block, an indexing gap and a platform translation that changes eligibility. Give PRESS peer review and PRISMA-S reporting their distinct roles. Link to maintained methodological guidance for the full procedures.
- **Coverage and supplementary methods:** one coverage matrix and a reproducible citation/similarity-search record. Explain seed selection, graph gaps, iterations and diminishing yield without inventing a universal stopping threshold.
- **Records and provenance:** a compact exercise distinguishing duplicate records, multiple reports and studies. Retain all discovery routes, reconcile export and deduplication counts, and show how an erroneous merge can lose useful evidence. This does not need its own general reference-management chapter.
- **Automation:** a task-based table distinguishing suggestions, strategy construction, translation, retrieval, prioritisation and stopping. Require inspectable executed queries and outputs where they exist; distinguish documented, observed and unknown behaviour.
- **Reporting and updates:** a completed reporting package that includes conventional searches, supplementary routes, transformations, exports, screening status and later changes. Add one worked update with indexing lag and revised terminology.
- **Review-methods bridge:** brief notes on systematic, scoping, rapid and qualitative syntheses, together with a non-health case. Do not imply that a scoping review automatically needs less sensitive searching or that a rapid-review shortcut has no methodological cost.

**What to remove, shorten or keep optional**

Remove from the required learning objectives: the Word2Vec analogy sequence, detailed encoder/decoder history, manual vector arithmetic, advanced index-execution algorithms, loss-function calculations and memorisation of model families.

Keep optional reference material on Transformers, tokenisation, inverted-index optimisations, learning-to-rank methods and diversity metrics. Moving these outside the required route is preferable to discarding useful explanations before the revised core has been tested.

Shorten MRR, MAP and nDCG to a comparison that explains which task each metric rewards. Do not remove ranked evaluation entirely: ranking affects effort and interacts with cutoffs even in evidence synthesis. Preserve recall at stated depth, screening effort, recall at stopping and the distinction between WSS and a live stopping decision.

Retain enough of the vector and BM25 labs to demonstrate candidate boundaries, exact matching, representation loss and changed ordering. Keep the rank-fusion lab optional unless its exercise directly supports the decision being assessed. The existing labs already contain useful evidence-oriented distinctions and do not require wholesale replacement.

Reduce repeated product catalogues and general discovery procurement discussion. Preserve the questions that matter for evidence synthesis: accessible sources and fields, candidate and export limits, trace availability, model changes, costs that truncate a run, and continuity of saved searches.

Use review-relevant cases for the main explanation. A brief everyday analogy can remain where it helps; replacing every accessible analogy with specialist biomedical terminology would create a different barrier. Include terminology from education, social care or another non-health field.

**Teaching materials and the final assessment**

Use a small, fully labelled teaching collection for controlled experiments and a separate documented review case to expose the limits of transfer. Include a contrasting non-health example. Synthetic examples must be labelled as such; authentic records and labels need clear provenance and reuse permissions.

Supply prepared inputs, outputs and answers, not just instructions to obtain or generate them. The [teaching notes](../teaching-notes.html) currently say that instructors must prepare the TAR runs or screening logs. Providing those materials is a higher-priority improvement than adding another technical chapter.

Three connected exercises can carry the core:

1. Diagnose why a known eligible report was missed, test a remedy and state what the evidence establishes.
2. Evaluate an additional retrieval route against the baseline, retaining overlap, eligible additions, workload and unresolved recall limitations.
3. Compare screening order and stopping on the same labelled pool, identifying which reports each simulated stop leaves unseen.

The final assessment is a short recommendation to a review team about the proposed workflow, supported by the search record, comparison results, provenance and stated limitations. A well-supported decision not to adopt a tool should be able to earn the same credit as a well-supported adoption decision.

**A practical implementation sequence**

1. Define the reader, scope and chapter outcomes. Map every retained mechanism to at least one evidence-synthesis decision; avoid a fixed theory/practice quota.
2. Build the reusable case pack and completed evaluation worksheet. Adapt the existing evaluation kit to distinguish supplementary discovery, replacement and screening comparisons.
3. Draft the new opening chapter and validation chapter first. These establish the problem and the evidence required to assess a proposed solution.
4. Draft the representations/training chapter and test whether it gives readers enough explanation to interpret the validation case. Use that result to set the amount of technical compression.
5. Reorder and adapt the remaining material, keeping a migration map from existing chapters and fragment identifiers. Preserve useful inbound links where feasible.
6. Update the digest, teaching notes, glossary navigation, questionnaire and other generated companions through the repository's maintained tooling. Do not create an unsynchronised alternate source of authored prose.
7. Check source claims, methodological scope, links, accessible figures and agreement between exercises and worked answers. Run the relevant existing maintenance checks when the implementation actually changes the book.
8. Pilot the exercises with intended readers and revise the explanations they need to make a justified decision.

This task saves the planning records only. The sequence above describes later implementation work.

The amount of restructuring remains substantial, but the emphasis changes: **retain the explanations that make retrieval failures understandable, replace the general audience route with evidence-synthesis decisions, and invest the largest new effort in usable validation cases.** Search-development, translation, records and reporting belong in the edition in the amount needed to support those decisions.
