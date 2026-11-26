---
kind: "part"
id: "part2"
tag: "Part II"
blurb: "Suppose you search for *delulu* and retrieve a paper that uses the phrase *unrealistic expectations*. Did the system expand your query, compare learnt representations, or use both? The result alone leaves that question open. Chapter 5 begins with how a model learns a representation."
time: "Reading time: about 107 min"
---

## Representations and retrieval pipelines

```{=html}
<div class="stage-map" role="group" aria-label="Pipeline map for Part II: which chapter covers which stage"><div class="stage-controller off">Controller — who chooses and sequences these stages is Part III’s question</div><div class="stage-row"><a class="stage on" href="#query-transformation" title="Chapter 11 — the words you typed may be rewritten, expanded or split before retrieval sees them.">Query<br>transformation<span class="stage-ch">Ch 11</span></a><a class="stage on" href="#representations-and-units" title="Chapter 8 — what one stored item actually is, and how finely the collection was cut up.">Analysis &amp;<br>execution rules<span class="stage-ch">Ch 8</span></a><a class="stage on" href="#embeddings" title="Chapters 5 to 8 — the encoder, the search over a whole collection, and the representation underneath both.">First-stage<br>retrieval<span class="stage-ch">Ch 5–8</span></a><a class="stage on" href="#hybrid-and-fusion" title="Chapter 10 — several candidate lists are combined into one.">Fusion<span class="stage-ch">Ch 10</span></a><a class="stage on" href="#reranking-and-hybrid" title="Chapter 9 — a shortlist is compared again, more carefully than collection scale allowed.">Reranking<span class="stage-ch">Ch 9</span></a><a class="stage off" href="#library-practice" title="Chapter 15 — what the reader is finally shown, and what can be recorded about it.">Presentation<span class="stage-ch">Part III</span></a></div><p>Part II builds the pipeline from the middle outwards. Chapters 5 to 8 move from learnt geometry to a retrieval encoder, collection-scale search and the indexed units underneath them; Chapters 9 and 10 divide the later work between reranking and combining candidate lists; and Chapter 11 returns to what happens to your query before any of it starts. Who decides to run the pipeline this way is held over to Part III.</p></div>
```

::: {.part-recap label="Carried forward"}
#### Five things from Part I that Part II leans on {#part2-recap-title}

Analysed term
:   What a token becomes after tokenisation, case folding and stemming — and what a lexical index actually stores and matches.
    Part II asks what a *model* reads instead.

Posting list
:   The records containing one term, which is how an inverted-index engine reaches candidates without scanning every document.
    Dense retrieval has no equivalent pointer, which is most of why it needs different machinery.

Candidate set
:   The records a retrieval pass makes available to the next stage.
    Changing the query can change which records enter that set.
    A reranker can reorder only the candidates it receives.

Three separate controls
:   Admission decides who may compete, the ranking function orders them, and top-*k* decides how many are kept.
    Part II keeps all three apart, and so should a vendor.

Lexical retrieval
:   Evidence drawn from matching words or character sequences, directly or through analysed index terms.
    Part II is measured against it rather than replacing it.

If any of these is hazy, [Chapter 4’s summary](#beyond-boolean) restates all five in a page.
:::

:::: {.distinction-map}
#### What the words on the box do not name {#distinction-map-vocabulary}

Five confusions are left.
Part I settled a sixth by watching a system behave; none of these five can be settled that way, and none can be stated honestly before the mechanism exists.
They are the same category error every time: the vocabulary of modern retrieval names goals, representations, output boundaries and whole research fields—and product descriptions use all four as though they named an architecture.
Part II is where each acquires a mechanism, and the entries below link to the section that supplies it.

::: distinction-map-list
vector = embedding
:   An embedding produces a vector, but not every vector is an embedding; “embedding search” is informal and “vector embedding search” adds little precision. [Read the distinction in Chapter 5](#distinction-embedding-vector).

vector search = semantic search
:   Vectors can be sparse, calculated and lexical; using vectors does not establish semantic matching. [Read the distinction in Chapter 8](#distinction-vector-semantic).

semantic search = dense retrieval
:   Semantic names a goal; dense retrieval names one technical route towards it. [Read the distinction in Chapter 7](#distinction-semantic-dense).

top-*k* belongs to dense retrieval
:   Top-*k* is an output boundary for ranked results, regardless of how their scores were produced. [Read the distinction in Chapter 7](#distinction-top-k).

neural information retrieval = dense retrieval
:   Neural IR also includes learnt sparse retrieval, late interaction and neural reranking. [Read the distinction in Chapter 9](#distinction-neural-dense).
:::

Most of these will still mean nothing to you.
Read the panel now to know what Part II is arguing about, and again [at the end](#what-you-can-now-ask) to see whether you can state each one in your own words. [Appendix D](#appendix-search-terminology) maps the wider terminology overlaps.
::::
