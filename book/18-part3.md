---
kind: "part"
id: "part3"
tag: "Part III"
blurb: "Who chooses the next retrieval action, where retrieval goes wrong, and what libraries must record, inspect and require."
time: "Reading time: about 84 min"
---

## Control, failure and professional judgement

::: {.part-recap label="Carried forward"}
#### Five things from Part II that Part III leans on {#part3-recap-title}

Embedding
:   A learnt mapping into a vector space, and by shorthand the vector it produces.
    Part III asks what happens when the training behind one does not fit your collection.

Indexed unit
:   The text the system actually searches — an abstract, a section, a passage — which need not be a whole document.
    It is [Chapter 13’s](#diagnosing-failure) first diagnostic question.

The candidate boundary
:   Where the fixed pool’s recall ceiling is set.
    No reranker, fusion stage or generated answer recovers a record that no earlier route let in; [Chapter 14](#precision-and-recall) gives that its exact meaning.

Reranker
:   A later, more expensive stage reordering a shortlist an earlier retriever produced.
    It reorders; it never retrieves.

Hybrid and multi-stage
:   Hybrid combines candidate-generation routes; multi-stage means later operations process what an earlier one supplied. [Chapter 12](#agentic-search) adds a third, independent property: who chose the order.

Part II’s chapter summaries restate each of these, and the [glossary](#glossary) holds the short definitions.
:::
