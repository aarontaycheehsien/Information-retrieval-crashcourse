# Evidence-synthesis specialization plan — initial proposal

Date: 2026-10-21  
Source branch: `fable-1`  
Reviewed commit: `99bfb9c5f4aaa8a9722c28559950ea17e8c399c5`  
Status: Initial proposal preserved from the conversation at the user's request. This document records a plan, not implemented textbook changes.

The proposal below preserves the initial recommendation. Any subsequent reconsideration is recorded separately.

---

I would make a **major structural revision, while reusing much of the conceptual material**. The central question would become: **“How do we find potentially eligible evidence, investigate what we missed, and justify the search process?”**

I reviewed the [`fable-1` textbook](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/fable-1/search-textbook.html), its orientation guide and teaching notes. It already contains much of the foundation: Appendix F distinguishes retrieval, screening prioritisation and stopping; Chapter 11 covers several routes beyond text queries; Chapters 13–15 address diagnosis, evaluation and documentation. The main issue is that readers encounter these applications after a substantial tour of retrieval architectures.

Assuming your readers already know basic database searching, I would aim for roughly **one-third retrieval mechanisms and two-thirds applied search decisions, validation and exercises**.

**The largest change would be making evidence synthesis the organizing structure.** Simply promoting Appendix F would help, but its emphasis on technology-assisted screening would leave search development and source selection comparatively underdeveloped.

Here is how I would treat the existing material:

| Existing material | What I would do |
|---|---|
| **Chapter 1: retrieval problem** | Rewrite around a review that misses an eligible study. Introduce coverage, query, ranking, export, deduplication and screening as places to investigate. |
| **Chapter 2: Boolean admission** | Retain and expand its practical implications: concept blocks, indexing, fields, proximity, subject headings and unintended exclusions. Shorten index mechanics. |
| **Chapters 3–4: BM25 and lexical search** | Combine into one shorter chapter explaining when ranking changes workload and when a cutoff changes the evidence available. |
| **Chapters 5–10: embeddings, encoders, dense retrieval, representations, reranking and fusion** | Compress into one or two core chapters. Preserve the distinctions that explain missed evidence; move detailed architectures into optional reading. |
| **Chapter 11: query transformation** | Expand and distribute across search development, supplementary searching and AI assistance. Its treatment of seeds, citations and feedback is especially useful here. |
| **Chapter 12: agentic search** | Reframe around evaluating an automated search process: sources reached, queries executed, additional eligible studies found and reasons for stopping. |
| **Chapters 13–15: diagnosis, evaluation and practice** | Make these central, introduce their principles early, and revisit them throughout the workflow. |
| **Appendix F: evidence synthesis** | Split between the opening framework and a dedicated chapter on screening prioritisation and stopping. |
| **Other appendices** | Retain a shortened terminology reference. Move Transformers, tokenisation internals, advanced index execution and detailed learning-to-rank material out of the required route. |

The additions I would prioritize are these.

1. **Turning eligibility criteria into a searchable strategy.**

   Explain why a review question and a database query represent different things. Not every eligibility criterion should become a compulsory search block.

   Use worked examples showing when population, outcomes, setting or study design are poorly represented in searchable metadata. Demonstrate how an apparently sensible extra `AND` loses eligible studies. Cover controlled vocabulary and free text together, indexing delays, changing terminology, and the appropriate use of validated search filters.

   Chapter 11 provides a foundation, but this needs a complete worked search-development example.

2. **Source coverage and the choice of complementary methods.**

   Give coverage its own chapter. Include disciplinary databases, trial registers where relevant, grey literature, dissertations, conference material, regional sources, websites and citation searching.

   The practical question should be: **What evidence could this additional source or method contribute that our existing approach is likely to miss?**

   Expand the existing citation and seed-search discussion into a reproducible procedure: seed selection, citation index, direction, iterations, dates, exports and stopping rationale. Include a non-health example so that “evidence synthesis” does not silently become synonymous with intervention reviews.

3. **Cross-database translation and search quality assurance.**

   Add a worked translation across platforms, showing that equivalent intent requires more than changing field tags. Subject headings, explosion, proximity, truncation, phrase handling and searchable fields can differ.

   Introduce **PRESS-based peer review alongside PRISMA-S reporting**, explaining their different functions. A fully reported strategy can still contain serious search errors.

   An excellent exercise would supply a plausible AI-generated translation containing several quiet mistakes and ask readers to diagnose their effects on retrieval.

4. **Validation designed for high recall.**

   This requires a substantial rewrite of [Chapter 14’s local evaluation approach](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/fable-1/search-textbook.html#L3149). Comparing the top ten or twenty results is useful for monitoring discovery systems, but insufficient for assessing an evidence-synthesis search.

   Build on the book’s existing cautions about recall denominators and add:

   - Development records versus held-out validation records, avoiding validation solely on papers used to construct the search.
   - Known-item recovery, relative recall and their respective limitations.
   - Additional eligible studies contributed by each source or method.
   - Screening workload alongside retrieval gains.
   - Analysis of what was missed: particular populations, languages, study designs or terminology.
   - Evaluation across several review topics before recommending a tool broadly.

   **A method’s most consequential misses may matter more than its average ranking score.**

5. **Managing records without losing evidence.**

   Expand Appendix F’s useful deduplication discussion into practical treatment of exports, missing abstracts, identifiers, provenance and record reconciliation.

   Make **record, report and study** explicit. Duplicate database records and multiple reports of one study require different handling. A conference abstract and a journal article should not disappear into an undocumented merge.

   Readers should be able to trace a record from its discovery route through deduplication and screening, with counts that reconcile.

6. **Review-specific decisions, updates and automation.**

   Explain how the search requirements differ across systematic, scoping, rapid and qualitative evidence syntheses. Make any methodological shortcuts explicit and justified.

   Add updating and living-review workflows: saved strategies, indexing lag, date overlap, changed subject headings, revised eligibility and versioned exports.

   For AI, assess separate tasks separately: term suggestion, strategy drafting, translation, supplementary discovery, screening prioritisation and early stopping. Success at one provides limited evidence about another. Preserve the book’s existing insistence on saving executed searches and traces.

I would **remove or sharply reduce several things from the main reading path**:

- **The extended Word2Vec-to-BERT progression**, detailed training mechanics and similarity calculations. Retain enough to explain vocabulary bridging, exact-match failures, compression and transfer to unfamiliar tasks.
- **Architecture taxonomy as a learning objective.** Librarians need to understand consequences of SPLADE, ColBERT or cross-encoders when evaluating a workflow; recalling the taxonomy should carry little assessment weight.
- **Detailed MRR, MAP and nDCG treatment.** Keep a short explanation for interpreting research papers. Give more space to sensitivity, additional eligible studies, workload and uncertainty about unseen evidence.
- **General discovery procurement material.** Retain coverage, export limits, audit trails, version changes and continuity. Move broader procurement questions into a companion.
- **Most slang examples and extended product tours.** Use changing disease terminology, drug names, ambiguous acronyms, qualitative concepts and multilingual records. Keep dated product examples where they demonstrate a specific search decision.

I would preserve the underlying explanations of **Boolean eligibility versus ranking, indexed evidence versus full text, candidate limits, training-dependent relevance and reranking’s inability to recover excluded candidates**. Those distinctions give this book its value for evidence-synthesis librarians.

A possible revised sequence would be:

| Chapter | Main question |
|---|---|
| 1. Evidence synthesis as a retrieval problem | Where can eligible evidence disappear? |
| 2. Sources and coverage | Where could the required evidence exist? |
| 3. Building sensitive structured searches | Which concepts and constraints should we search? |
| 4. Translation and peer review | Does the strategy work as intended across platforms? |
| 5. Ranked lexical retrieval | When does ranking affect access to evidence? |
| 6. Neural and hybrid retrieval | What can these methods recover, and what can they miss? |
| 7. Supplementary and agentic searching | What additional evidence does each route contribute? |
| 8. Diagnosing and validating searches | How do we investigate misses and assess adequacy? |
| 9. Records, reports and studies | How do we preserve evidence and provenance? |
| 10. Screening prioritisation and stopping | What changes when some records remain unexamined? |
| 11. Reporting, updating and maintaining searches | Can another librarian inspect, rerun and extend the work? |

Finally, I would change the assessments. Use one continuing review case, with a second contrasting discipline, and have readers produce a **search strategy, translation, peer-review response, validation record and reporting package**.

Keep the interactive labs, but connect each to a decision about evidence. For Appendix F’s screening exercise, supply prepared datasets and screening logs—the [current teaching notes](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/blob/fable-1/teaching-notes.html) acknowledge that instructors must prepare these themselves. Making that exercise usable without coding would be a particularly valuable addition.
