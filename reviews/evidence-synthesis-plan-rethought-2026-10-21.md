# Evidence-synthesis specialisation plan — third iteration

Date: 2026-10-21  
Reviewed commit: `342cd92` (textbook unchanged since `99bfb9c`)  
Builds on: the [initial proposal](evidence-synthesis-plan-2026-10-21.md) and the [reconsidered recommendation](evidence-synthesis-plan-reconsidered-2026-10-21.md)  
Status: Editorial recommendation only. It does not change the textbook or its companions.

## Summary

The reconsidered plan fixed the first plan's main fault, which was discarding the mechanism explanations that make the book distinctive. It still has five problems:

1. It never decides what happens to the existing book, its other primary audience and its companions.
2. It reorders the book's chapters rather than organising around the reader's work. The retrieval systems evidence-synthesis librarians use daily, such as PubMed's query mapping, automated MeSH indexing, search filters and citation indexes, are barely covered.
3. It designs search validation from information-retrieval first principles and cites none of the information-specialist literature that already addresses it.
4. It treats stopping as a screening problem only. Searching has its own stopping problem.
5. Its AI guidance is not tied to the joint position statement and RAISE guidance that now govern AI use in evidence synthesis.

**Recommendation:** write the evidence-synthesis material first as a separate, shorter volume organised around the reader's toolchain, linking to the existing chapters for mechanism depth. Pilot it. Restructure the main book only if the pilot shows that readers cannot use the linked chapters as they stand.

## What to keep from the reconsidered plan

- The boundary framework (coverage, retrieval, deduplication, prioritisation, stopping) and the rule that a downstream stage cannot repair an upstream exclusion.
- The claim-specific evaluation table: supplement, replace, change a component, select a product, prioritise, stop, update.
- The synthetic 100/90/81 nested-set example and the record, report and study distinction.
- The three connected exercises, supplied materials rather than instructions to generate them, and a final assessment in which a well-justified decision not to adopt earns full credit.
- A non-health contrast case.

## Problem 1: decide the edition first

The README and the preface's "Who this is for" name information-literacy and evidence-synthesis librarians as the two primary audiences, with systems librarians secondary. Rebuilding the sole maintained edition around evidence synthesis drops the first of these. Neither earlier plan says so.

The coupling cost is also larger than "keep a migration map" suggests. At this commit:

| Dependency on current chapter numbering | Count |
|---|---|
| "Chapter N" references in root companion pages | 117 |
| "Chapter N" references in `tools/` and `data/` | 325 |
| Links from root companion pages to textbook fragment identifiers | 208 |
| Video tool directories named by chapter number | 16 |

These are `grep` counts that indicate scale; they are not a migration list. Chapters 2–11 hold about 32,000 words, including captions and evidence notes, and a full restructure would need new examples throughout.

| Option | Advantage | Cost |
|---|---|---|
| A. Restructure the sole edition | One source of truth and a self-contained textbook | Drops the information-literacy audience, breaks the companions above and rewrites the examples throughout Chapters 2–11 |
| B. Fork a second full edition | Serves both audiences | Every correction and product re-check must be made twice, and the tooling assumes one book. This combines the costs of A and C. |
| C. Separate evidence-synthesis volume that links to the existing mechanism chapters | New effort goes to what is missing; the existing book and companions keep working; the volume doubles as the pilot | Readers move between two books, and the mechanism chapters keep their general examples |

Use C for the build and pilot. Move to A only if the pilot shows that readers cannot apply the general chapters to review work. If A is chosen, tag v1.2.1 as the frozen general edition. Reject B.

## Problem 2: organise around the reader's toolchain

Evidence-synthesis librarians meet retrieval mechanisms through a small number of systems. The book explains the mechanisms well but rarely names them inside those systems. At this commit the book contains no mention of automatic term mapping, MEDLINE, automated indexing or search filters, and only six of MeSH.

| What the reader already uses | Mechanism inside it | Current coverage | Gap |
|---|---|---|---|
| PubMed automatic term mapping | Query transformation before retrieval (National Library of Medicine [NLM], n.d.-a) | Chapters 4 and 11, generically | Not mentioned |
| PubMed Best Match | BM25 retrieval, then LambdaMART reranking of the top 500 using a model trained on search-log data (Fiorini et al., 2018) | Chapters 3 and 9; Appendix E on click logs | Small: add the consequence for sort order versus the exported set |
| MeSH indexing | Automated since 2022, with human quality assurance. MTIX, a neural model, replaced the rule-based MTIA in 2024. It was trained on 2007–2022 citations and indexes from title and abstract only (NLM, 2021, 2024, n.d.-b) | Six mentions, none on how headings are assigned | Large. A subject-heading block now inherits a learnt classifier's errors and training period. This is the natural bridge between Parts I and II |
| Study-design search filters and RCT classifiers | Hand-built Boolean classifiers and learnt classifiers, both judged by sensitivity and precision (Marshall et al., 2018; Thomas et al., 2021) | One passing reference to a "tested search hedge" | Large, and an ideal worked contrast |
| Platform syntax across Ovid, EBSCOhost, Embase, Scopus and Web of Science | Analyser and tokeniser decisions that fix what truncation, phrases and proximity mean | Chapter 2, in general terms | Connect the analyser to the operators the reader types |
| Objective search development and word-frequency tools | Term statistics from a development set of known records (Hausner et al., 2012) | None | Applies term weighting and relevance feedback the book already explains |
| LLM-drafted Boolean strategies | Generated queries that early tests found precise but at a cost to recall (Wang et al., 2023), with later work re-examining replicability (Staudinger et al., 2024) | Chapter 11, generically | Moderate |
| Google Scholar and AI research assistants | Ranked retrieval with display and export limits. Google Scholar was found unsuitable as a principal source for systematic searching (Gusenbauer & Haddaway, 2020) | Chapters 7 and 12 | Map mechanisms to suitability criteria |
| Citation searching | Graph traversal over an index with its own coverage (Hirt et al., 2024) | Chapter 11 | Treat citation-index coverage as a boundary |
| Deduplication | Record linkage, a matching task with its own errors in both directions (McKeown & Mir, 2021) | One paragraph in Appendix F | Moderate |

Each chapter in the new volume should open with one of these tools and then explain the mechanism with existing material.

## Problem 3: validation already has a literature

The reconsidered plan's eight-step protocol is sound, but it reads as though search validation began with information retrieval. Information specialists already have:

- relative recall against a reference set drawn from included studies (Sampson et al., 2006);
- development and validation sets in the objective approach, with a non-inferiority validation (Hausner et al., 2012, 2015);
- database-combination studies of which sources recover included studies (Bramer et al., 2017);
- suitability criteria for academic search systems (Gusenbauer & Haddaway, 2020);
- peer review of strategies (McGowan et al., 2016) and reporting standards (Rethlefsen et al., 2021).

The retrieval community has review-specific test collections with Boolean queries and relevance labels (Scells et al., 2017; Kanoulas et al., 2017) and large labelled screening datasets (De Bruin et al., 2023).

The book's distinctive contribution is to connect these. For example, relative recall inherits the bias of its reference set in the same way that pooled relevance judgements inherit the bias of the runs that were pooled, and a test set taken from one review's included studies measures known-item recovery rather than recall. Chapter 14 already supplies the retrieval half of that argument. The validation chapter should build on the specialist half rather than present a protocol as new.

## Problem 4: stopping applies to searching as well as screening

Appendix F and both earlier plans treat stopping as a screening decision. Deciding when to stop adding databases, supplementary sources or citation-searching iterations is the same kind of decision with the same unknown denominator (Booth, 2010). Capture–recapture has been proposed for search stopping (Kastner et al., 2009), not only for screening, and TARCiS addresses iteration in citation searching (Hirt et al., 2024). One chapter should treat both. That also corrects the impression that the hard statistical questions sit only with screening.

## Problem 5: anchor AI guidance to existing governance

Cochrane, the Campbell Collaboration, JBI and the Collaboration for Environmental Evidence now share a position statement. Reviewers remain responsible for any AI use, must be able to show that it does not compromise methodological rigour, and must report AI that makes or suggests judgements (Flemyng et al., 2025). The statement endorses the RAISE guidance, which separates the responsibilities of tool developers, evaluators and users (RAISE, 2025).

The book should not build a parallel framework. Its contribution is to explain which retrieval mechanism a tool uses, so that a librarian can answer RAISE's questions about it, and to supply the evaluation design each claim requires.

## Revised structure for the evidence-synthesis volume

Eight chapters. "Draws on" names existing material, which is linked under option C or rewritten under option A.

| Chapter | Opening case | Decision the reader can make | Draws on | New material |
|---|---|---|---|---|
| 1. Where eligible studies go missing | A review that missed an eligible study | Locate a loss at coverage, indexing, query, ranking or export limit, deduplication, prioritisation or stopping | Chapters 1 and 14; Appendix F | Boundary diagram covering search stopping and deduplication; record, report and study |
| 2. PubMed as a retrieval system | One question run as typed, after term mapping, and under Best Match and date sort | Predict what term mapping, Best Match and Similar Articles change, and what they cannot change | Chapters 3, 4, 9 and 11; Appendix E | Term mapping; export consequences; a contrasting non-health database |
| 3. Classifiers you inherit | A MeSH-only block that misses recent or newly named concepts | Judge when a subject heading, search filter or RCT classifier can be relied on, and how to test it | Chapters 5, 6 and 13 | Automated MeSH; filter evaluation; RCT classifiers; retrievers trained on PubMed search logs, which learn what searchers clicked rather than what met eligibility criteria (Jin et al., 2023) |
| 4. Building and translating the strategy | A strategy translated across two platforms with one quiet error | Explain how concept blocks, analysers, fields and proximity change admission; use term mining and LLM drafting with checks | Chapters 2, 4 and 11 | Objective approach; evidence on LLM query generation; the separate roles of PRESS and PRISMA-S |
| 5. Supplementary routes | A citation search and an AI research assistant run from the same seeds | Decide what each route can add, under what coverage and limits, and how to record it | Chapters 7, 9, 10, 11 and 12 | TARCiS; citation-index coverage; display and export limits |
| 6. Stopping in searching and screening | Two screening logs on the same pool | Separate ranking efficiency from a defensible decision to stop | Appendix F | Search stopping; prepared screening logs |
| 7. Validating a search, route or tool | A vendor's performance claim | Choose the comparison the claim needs and state what it cannot show | Chapter 14; the reconsidered plan's table and protocol | Specialist validation literature; retrieval test collections; RAISE |
| 8. Recording, reporting and updating | An update two years later after MeSH, Best Match and a tool have all changed | Produce a record another librarian can rerun, audit and update | Chapter 15; Appendix F | PRISMA-S with AI reporting under the position statement; deduplication record; update case |

Records and provenance sit in Chapters 1 and 8 rather than in a chapter of their own, as the reconsidered plan proposed. Screening receives one chapter, shared with search stopping, because librarians more often advise on screening tools than operate them. Query formulation and its automation receive a full chapter, because that is the librarian's own task.

## Case pack: reuse labelled public data

The teaching notes ask instructors to prepare screening logs themselves. Public data can close that gap faster than new writing can.

- **SYNERGY** (De Bruin et al., 2023): 26 reviews, 169,288 records and 2,834 inclusions, released under CC0. Run the ASReview simulations once and publish the logs so that the stopping exercises need no code.
- **CLEF TAR 2017–2019** (Kanoulas et al., 2017) and **Scells et al. (2017)**: review topics with Boolean queries, PubMed identifiers and relevance labels. Suitable for query-diagnosis, translation and validation exercises. Confirm reuse terms before redistributing, and state that public labels may have appeared in model training data.
- **Non-health contrast:** check whether any SYNERGY topic outside health suits the contrast case before building a new one. If a new one is needed, keep it small and document its labelling.

## Revised implementation sequence

1. Decide the edition strategy and whether the information-literacy audience stays. Everything else depends on this.
2. Build the case pack: published screening logs, one CLEF TAR or Scells topic with its query and labels, and the contrast case. Record provenance and licences.
3. Draft Chapters 1 and 7 first, as the reconsidered plan proposed.
4. Draft Chapters 2 and 3, the largest gaps. Add every PubMed and NLM claim to the product-evidence register with a check date.
5. Pilot with a small group of practising evidence-synthesis librarians. The test is whether they can complete the three exercises using links into the existing chapters. Record where they fail.
6. Decide on option A only from the pilot evidence. If it is chosen, migrate the companions through the maintained tooling with redirects, as the reconsidered plan specified.

## Questions for the author

- Is the information-literacy audience still wanted? This decides between options A and C.
- Is a health-led book with one non-health contrast acceptable, or should coverage be balanced across disciplines? Balance roughly doubles the case work, because the controlled vocabularies and labelled datasets differ.
- Who will re-check PubMed, NLM and tool claims each year? This volume adds many fast-changing product claims.

## References

Booth, A. (2010). How much searching is enough? Comprehensive versus optimal retrieval for technology assessments. *International Journal of Technology Assessment in Health Care, 26*(4), 431–435. https://doi.org/10.1017/S0266462310000966

Bramer, W. M., Rethlefsen, M. L., Kleijnen, J., & Franco, O. H. (2017). Optimal database combinations for literature searches in systematic reviews: A prospective exploratory study. *Systematic Reviews, 6*, 245. https://doi.org/10.1186/s13643-017-0644-y

De Bruin, J., Ma, Y., Ferdinands, G., Teijema, J., & Van de Schoot, R. (2023). *SYNERGY: Open machine learning dataset on study selection in systematic reviews* [Data set]. DataverseNL. https://doi.org/10.34894/HE6NAQ

Fiorini, N., Canese, K., Starchenko, G., Kireev, E., Kim, W., Miller, V., et al. (2018). Best Match: New relevance search for PubMed. *PLOS Biology, 16*(8), e2005343. https://doi.org/10.1371/journal.pbio.2005343

Flemyng, E., Noel-Storr, A., Macura, B., Gartlehner, G., Thomas, J., et al. (2025). Position statement on artificial intelligence (AI) use in evidence synthesis across Cochrane, the Campbell Collaboration, JBI and the Collaboration for Environmental Evidence 2025. *Environmental Evidence*. https://doi.org/10.1186/s13750-025-00374-5

Gusenbauer, M., & Haddaway, N. R. (2020). Which academic search systems are suitable for systematic reviews or meta-analyses? Evaluating retrieval qualities of Google Scholar, PubMed, and 26 other resources. *Research Synthesis Methods, 11*(2), 181–217. https://doi.org/10.1002/jrsm.1378

Hausner, E., Guddat, C., Hermanns, T., Lampert, U., & Waffenschmidt, S. (2015). Development of search strategies for systematic reviews: Validation showed the noninferiority of the objective approach. *Journal of Clinical Epidemiology, 68*(2), 191–199. https://doi.org/10.1016/j.jclinepi.2014.09.016

Hausner, E., Waffenschmidt, S., Kaiser, T., & Simon, M. (2012). Routine development of objectively derived search strategies. *Systematic Reviews, 1*, 19. https://doi.org/10.1186/2046-4053-1-19

Hirt, J., Nordhausen, T., Fuerst, T., Ewald, H., & Appenzeller-Herzog, C. (2024). Guidance on terminology, application, and reporting of citation searching: The TARCiS statement. *BMJ, 385*, e078384. https://doi.org/10.1136/bmj-2023-078384

Jin, Q., Kim, W., Chen, Q., Comeau, D. C., Yeganova, L., et al. (2023). MedCPT: Contrastive pre-trained transformers with large-scale PubMed search logs for zero-shot biomedical information retrieval. *Bioinformatics, 39*(11), btad651. https://doi.org/10.1093/bioinformatics/btad651

Kanoulas, E., Li, D., Azzopardi, L., & Spijker, R. (2017). CLEF 2017 technologically assisted reviews in empirical medicine overview. In *CLEF 2017 Working Notes* (CEUR Workshop Proceedings). https://openalex.org/W2785937154

Kastner, M., Straus, S. E., McKibbon, K. A., & Goldsmith, C. H. (2009). The capture–mark–recapture technique can be used as a stopping rule when searching in systematic reviews. *Journal of Clinical Epidemiology, 62*(2), 149–157. https://doi.org/10.1016/j.jclinepi.2008.06.001

Marshall, I. J., Noel-Storr, A., Kuiper, J., Thomas, J., & Wallace, B. C. (2018). Machine learning for identifying randomized controlled trials: An evaluation and practitioner's guide. *Research Synthesis Methods, 9*(4), 602–614. https://doi.org/10.1002/jrsm.1287

McGowan, J., Sampson, M., Salzwedel, D. M., Cogo, E., Foerster, V., & Lefebvre, C. (2016). PRESS Peer Review of Electronic Search Strategies: 2015 guideline statement. *Journal of Clinical Epidemiology, 75*, 40–46. https://doi.org/10.1016/j.jclinepi.2016.01.021

McKeown, S., & Mir, Z. M. (2021). Considerations for conducting systematic reviews: Evaluating the performance of different methods for de-duplicating references. *Systematic Reviews, 10*, 38. https://doi.org/10.1186/s13643-021-01583-y

National Library of Medicine. (2021). MEDLINE 2022 initiative: Transition to automated indexing. *NLM Technical Bulletin*, (443). https://www.nlm.nih.gov/pubs/techbull/nd21/nd21_medline_2022.html

National Library of Medicine. (2024). MTIX: The next-generation algorithm for automated indexing of MEDLINE. *NLM Technical Bulletin*, (457). https://www.nlm.nih.gov/pubs/techbull/ma24/ma24_mtix.html

National Library of Medicine. (n.d.-a). *PubMed user guide*. Retrieved 21 October 2026, from https://pubmed.ncbi.nlm.nih.gov/help/

National Library of Medicine. (n.d.-b). *Frequently asked questions about indexing for MEDLINE*. Retrieved 21 October 2026, from https://www.nlm.nih.gov/bsd/indexfaq.html

RAISE. (2025). *Responsible use of AI in evidence synthesis (RAISE): Recommendations and guidance*. Open Science Framework. https://osf.io/fwaud/

Rethlefsen, M. L., Kirtley, S., Waffenschmidt, S., Ayala, A. P., Moher, D., Page, M. J., Koffel, J. B., & PRISMA-S Group. (2021). PRISMA-S: An extension to the PRISMA statement for reporting literature searches in systematic reviews. *Systematic Reviews, 10*, 39. https://doi.org/10.1186/s13643-020-01542-z

Sampson, M., Zhang, L., Morrison, A., Barrowman, N. J., Clifford, T. J., Platt, R. W., Klassen, T. P., & Moher, D. (2006). An alternative to the hand searching gold standard: Validating methodological search filters using relative recall. *BMC Medical Research Methodology, 6*, 33. https://doi.org/10.1186/1471-2288-6-33

Scells, H., Zuccon, G., Koopman, B., Deacon, A., Azzopardi, L., & Geva, S. (2017). A test collection for evaluating retrieval of studies for inclusion in systematic reviews. In *Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 1237–1240). https://doi.org/10.1145/3077136.3080707

Staudinger, M., Kusa, W., Piroi, F., Lipani, A., & Hanbury, A. (2024). A reproducibility and generalizability study of large language models for query generation. In *Proceedings of the 2024 Annual International ACM SIGIR Conference on Research and Development in Information Retrieval in the Asia Pacific Region* (pp. 186–196). https://doi.org/10.1145/3673791.3698432

Thomas, J., McDonald, S., Noel-Storr, A., Shemilt, I., Elliott, J., Mavergames, C., & Marshall, I. J. (2021). Machine learning reduced workload with minimal risk of missing studies: Development and evaluation of a randomized controlled trial classifier for Cochrane Reviews. *Journal of Clinical Epidemiology, 133*, 140–151. https://doi.org/10.1016/j.jclinepi.2020.11.003

Wang, S., Scells, H., Koopman, B., & Zuccon, G. (2023). Can ChatGPT write a good Boolean query for systematic review literature search? In *Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 1426–1436). https://doi.org/10.1145/3539618.3591703
