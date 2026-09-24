# Information Retrieval Crash Course

A practical introduction to information retrieval architecture, written primarily for information literacy and evidence synthesis librarians, with a smaller secondary audience of systems/discovery librarians. It covers Boolean search, BM25, dense retrieval, hybrid search, reranking, query understanding, agentic search, retrieval failure and evaluation.

[**Read the textbook**](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/) — version 1.2.1, three parts, fifteen chapters and seven appendices.

New to the subject? Start with [**Read this first**](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/read-this-first.html): a 45-minute guided route through the chapter summaries and key distinctions, with every excerpt linked back to the book.

## Companions

- **Interactive labs** for Chapters 3, 7 and 10: the [BM25 Evidence Lab](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/bm25-evidence-lab.html), the [Vector Similarity Lab](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/vector-similarity-lab.html) and the [Rank Fusion Lab](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/rank-fusion-lab.html). Each opens with a short prediction tour, then a sandbox.
- **[Local retrieval evaluation kit](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/evaluation-kit.html):** a spreadsheet template, completed example and guide for comparing two search runs with your own relevance judgements. Start with one query, then build a reusable set.
- **[Vendor questionnaire](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/vendor-questionnaire.html):** Chapter 15's nineteen questions as a printable review record, with optional ranking-method and RAG sections. It keeps vendor answers, supporting evidence and the library's own verification separate.
- **[Teaching notes](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/teaching-notes.html):** a one-hour workshop, longer course shapes, exercises and a rubric. See [For instructors](#for-instructors).
- **[Product evidence and currency register](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#product-evidence-currency):** dated product claims, their evidence and recorded checks. Its [JSON source](data/product-claims.json) also generates the teaching notes' verification groups. [Report an error](https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/issues) with the claim ID and supporting evidence.
- **[Glossary](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#glossary)** of 84 terms, and **[Find a term or section](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#book-lookup)**, which searches definitions, acronyms and headings locally, including offline (not full text).

## Maintaining the book

`search-textbook.html` is the sole maintained edition and the source of truth for authored prose, including glossary definitions. Marked product-evidence blocks, glossary navigation, the lookup index, the digest and the questionnaire are generated from maintained mappings. The retired single-flow edition is in Git history, and its former URL redirects to the textbook. See [`tools/README.md`](tools/README.md) for the maintenance passes and [`CHANGELOG.md`](CHANGELOG.md) for what changed between versions.

## For instructors

Start with the [**one-hour workshop**](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/teaching-notes.html#one-hour-workshop), *Why did this search miss a paper?* It includes a prepared case, timed facilitator guidance, worked answers and a [two-page participant handout](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/teaching-workshop-handout.html), with no advance reading or subscription access required for participants. The [**teaching notes**](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/teaching-notes.html) also provide audience routes, three longer course shapes, an eight-point assessment rubric, discussion prompts, product-claim verification guidance and a record for improving the next delivery. Workshop timings are provisional pending teaching experience.

Chapters and appendices are written to be assignable on their own, and each has a stable link — use the **Copy link** control in any chapter heading. Every chapter ends with *Check yourself* questions whose answers stay hidden until opened. Three combinations stand alone particularly well: Part I (Chapters 1–4) as an information-literacy grounding in retrieval foundations and lexical search; Chapters 2, 11 and 13–15 with [Appendix F](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#appendix-evidence-synthesis-high-recall-retrieval) for evidence synthesis, where Appendix F should be treated as core rather than optional; and Chapter 15 with Appendix D for systems/discovery work on procurement and evaluation.

## Licence and reuse

The text, tables, diagrams and code are licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — copy, excerpt, translate, adapt and redistribute for any purpose, including commercially, with credit. No permission request is needed.

Reproduced research figures (including Figure 5.5 from Mikolov and colleagues) and screenshots of commercial products (scite, Google Scholar, Web of Science and others) are third-party material reproduced for comment and criticism, and are **not** covered. Product names and trademarks belong to their owners. See [`LICENSE`](LICENSE) for the full terms.

### Suggested citation

> Tay, A. C. H. (2026). *How search decides what you see: A librarian's guide to Boolean search, BM25, embeddings, reranking, and the retrieval pipelines behind hybrid and agentic search* (Version 1.2.1). https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/

## Generative AI use

Generative AI assisted with research, drafting, revision, code and original explanatory illustrations. The author reviewed the outputs, checked cited claims against the linked sources and takes responsibility for the final content. Read the [full generative-AI use disclosure](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#generative-ai-use-disclosure).
