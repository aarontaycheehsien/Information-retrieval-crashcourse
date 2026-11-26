---
kind: "backsection"
---

## Where to go deeper {#where-to-go-deeper}

The [reference list](#references) records the sources cited in the main text; a source cited in full inside a footnote is not repeated here.
This is a shorter set of entry points for reading further, grouped by what you would be trying to learn, with a line on what each is good for.
Some are practical companions rather than evidential sources used in the main text.

### Foundations and lexical retrieval {#deeper-lexical}

- **Manning, Raghavan and Schütze, [*Introduction to Information Retrieval*](https://nlp.stanford.edu/IR-book/).** The standard textbook, free online.
  Start here for indexing, analysis and query processing in far more depth than Chapters 2 to 4 attempt.
  Chapters 1, 2 and 6 are the closest match to this book’s Part I.
- **Robertson and Zaragoza, [“The probabilistic relevance framework: BM25 and beyond”](https://doi.org/10.1561/1500000019).** Where BM25 comes from, by the people it came from.
  Read it when you want to know why the formula has the shape it does rather than how to use it.
- **Furnas and colleagues, [“The vocabulary problem in human-system communication”](https://doi.org/10.1145/32206.32212).** The 1987 paper establishing that people spontaneously choose different words for the same thing.
  Everything semantic retrieval claims to solve is a restatement of this result.

### Neural retrieval {#deeper-neural}

- **Alammar, [“The Illustrated Word2vec”](https://jalammar.github.io/illustrated-word2vec/).** The gentlest available walk through what Word2Vec’s training task actually does, diagram by diagram.
  Read it when [Chapter 5](#from-word2vec-to-retrieval-embeddings) leaves you wanting the mechanism rather than the consequence.
- **Vaswani and colleagues, [“Attention is all you need”](https://arxiv.org/abs/1706.03762).** The Transformer paper, and unusually readable. [Appendix A](#appendix-the-transformer) is the version without mathematics; this is the original.
- **Devlin and colleagues, [“BERT”](https://aclanthology.org/N19-1423/).** Worth reading for its argument about why bidirectional reading suits representing an existing text, which is the reason encoders became the basis for retrieval models.
- **Karpukhin and colleagues, [“Dense passage retrieval”](https://aclanthology.org/2020.emnlp-main.550/).** The clearest single account of the bi-encoder pattern and of how negative examples are chosen — the design decision that most shapes what a retriever learns.
- **Nogueira and Cho, [“Passage re-ranking with BERT”](https://arxiv.org/abs/1901.04085);** **Khattab and Zaharia, [“ColBERT”](https://doi.org/10.1145/3397271.3401075);** **Formal and colleagues, [“SPLADE”](https://doi.org/10.1145/3404835.3463098).** The three arrangements of [Chapter 9](#reranking-and-hybrid) in their original form: joint encoding, late interaction, and learnt sparse representations.
- **Malkov and Yashunin, [“Efficient and robust approximate nearest neighbor search using HNSW graphs”](https://doi.org/10.1109/TPAMI.2018.2889473).** For what an ANN index actually does, when the summary in [Chapter 7](#how-nearest-neighbour-indexing-makes-dense-retrieval-practical) stops being enough.

### Result diversification {#deeper-diversification}

- **Carbonell and Goldstein, [“The use of MMR”](https://doi.org/10.1145/290941.291025).** The two-page origin of maximal marginal relevance: a direct relevance–redundancy trade-off that remains the easiest diversification method to understand and implement.
- **Agrawal and colleagues, [“Diversifying search results”](https://doi.org/10.1145/1498759.1498766);** **Santos and colleagues, [“Explicit search result diversification through sub-queries”](https://doi.org/10.1007/978-3-642-12275-0_11).** IA-Select and xQuAD as the two classic explicitly intent-aware alternatives to MMR.
- **Kulesza and Taskar, [“Determinantal point processes for machine learning”](https://doi.org/10.1561/2200000044).** A tutorial treatment of probabilistic subset selection in which quality and diversity are modelled jointly.
- **Clarke and colleagues, [“Novelty and diversity in information retrieval evaluation”](https://doi.org/10.1145/1390334.1390446).** The evaluation counterpart: why independent relevance judgements miss redundancy, and how α-nDCG rewards new aspect coverage.

### Relevance {#deeper-relevance}

- **Taylor, [“Question-Negotiation and Information Seeking in Libraries”](https://hdl.handle.net/2142/38236).** Especially useful for librarians: the visceral need, conscious need, formalised question and compromised question show why the request presented to a system is not identical to the underlying need.
- **Mizzaro, [“Relevance: The Whole History”](https://doi.org/10.1002/%28SICI%291097-4571%28199709%2948%3A9%3C810%3A%3AAID-ASI6%3E3.0.CO%3B2-U).** A historical and theoretical map of the many ways relevance has been defined in information science and retrieval.
- **Saracevic, [“Relevance: A review of the literature and a framework for thinking on the notion in information science.
  Part II”](https://onlinelibrary.wiley.com/doi/10.1002/asi.20682).** The fuller account behind the system-oriented and user-oriented manifestations simplified in Chapters 1 and 14.

### Evaluation {#deeper-evaluation}

- **Cleverdon, [“The Cranfield tests on index language devices”](https://doi.org/10.1108/eb050097).** The experimental design that all retrieval evaluation still uses, described before it became an assumption nobody states.
- **Järvelin and Kekäläinen, [“Cumulated gain-based evaluation of IR techniques”](https://doi.org/10.1145/582415.582418).** Where nDCG comes from, and the reasoning behind graded relevance and a positional discount.
- **Buckley and Voorhees, [“Retrieval evaluation with incomplete information”](https://doi.org/10.1145/1008992.1009000).** What pooling does to a comparison, and why a system unlike the ones in the pool is the one most likely to be scored unfairly.
- **Thakur and colleagues, [“BEIR”](https://arxiv.org/abs/2104.08663).** Read the task descriptions, not only the results table.
  Seeing which collections and question styles were used is what makes the transfer argument in [Chapter 14](#test-collections-and-benchmarks) concrete.

### Evidence synthesis and TAR {#deeper-evidence-synthesis}

- **Lefebvre and colleagues, [Cochrane Handbook Chapter 4](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04).** The current methodological baseline for searching and selecting studies in Cochrane intervention reviews.
  Read the database-searching and automation sections together.
- **van de Schoot and colleagues, [“An open source machine learning framework for efficient and transparent systematic reviews”](https://doi.org/10.1038/s42256-020-00287-7).** The clearest account of ASReview’s modular active-learning pipeline and its place after the initial search.
- **Fütterer and colleagues, [“Fast-track your abstract screening”](https://doi.org/10.1177/25152459261442150).** A practical ASReview tutorial for researchers, including guidance on evaluating and documenting stopping decisions.
- **Boetje and van de Schoot, [“The SAFE procedure”](https://doi.org/10.1186/s13643-024-02502-7).** A practical composite stopping framework whose example thresholds are explicitly not universal rules.
- **Repke and colleagues, [“Don’t stop me now”](https://doi.org/10.1002/cesm.70068).** A 2026 evaluation of 15 stopping methods over 81 datasets, useful for seeing why safe stopping remains harder than efficient ranking.

### Library practice {#deeper-practice}

- **Rethlefsen and colleagues, [“PRISMA-S”](https://pmc.ncbi.nlm.nih.gov/articles/PMC7839230/).** The reporting standard for search strategies in evidence syntheses, and the closest existing answer to what [Chapter 15](#reproducibility-implication-title) asks a library to record.
  Note what it already concedes about proprietary and similarity-based operations.

### Retrieval-augmented generation {#deeper-rag}

- **Lewis et al., [“Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks”](https://arxiv.org/abs/2005.11401).** The paper that named the family.
  Read it after [Chapter 7](#dense-at-scale): its retriever is a dense bi-encoder, and everything this book says about dense retrieval applies to it.
- **Rackauckas, [“RAG-Fusion: A New Take on Retrieval-Augmented Generation”](https://arxiv.org/abs/2402.03367).** The published description of the technique behind Scopus AI’s search module, worked through against this book’s chapters in [Appendix G](#appendix-rag-scopus).
