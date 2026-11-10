# Appendix G (Retrieval-augmented generation): review

Reviewed 10 November 2026 against commit `8f2162f`. The appendix was about
2,670 words with one HTML figure and one table. Eight findings were reported. A
recheck requested by the author withdrew one and verified the source for
another. The author then asked for all to be applied.

## What was verified before any change

- **LaRA (2025)**, from the publisher's abstract: 2,326 test cases, eleven
  models, and a preferred approach that depends on model, context length, task
  and retrieval characteristics.
- **Li et al. (2024)**, from the abstract: long context outperformed on average
  when sufficiently resourced, with lower cost for retrieval.
- **Sen et al. (2026), "Is Grep All You Need?"**, read through its first
  experiment: a 116-question sample; a regular-expression tool scoring by match
  count over prepared conversation data; "inline grep exceeds inline vector for
  every harness–model pair"; and file-based delivery reversing the order on
  five of ten pairs. The appendix's account matches.
- **Rackauckas (2024)**, from the abstract: a manual evaluation of a
  product-information chatbot at Infineon, reporting that some answers strayed
  off topic.
- **Liu, Zhang and Liang (2023)**, from the abstract: the figures now quoted.

## Applied

- **The MCP section.** Its first paragraph repeated Appendix D's entry almost
  word for word and linked the top of that appendix's overlaps. It is now two
  sentences linking the entry itself (`#overlap-mcp-rag`), followed by the
  material that is new here: how the two compose.
- **A misfiled conclusion.** Two paragraphs that close the whole section on
  long context and agentic search sat under its last sub-question. They now
  have their own heading, *What the debate leaves in place*
  (`#appendix-rag-what-the-debate-leaves`).
- **The worked example.** RAG Fusion was presented with no weakness, and
  Rackauckas (2024) was called "a published description and evaluation" with
  no indication of what was evaluated. A new paragraph says the evaluation was
  of an Infineon chatbot, not of Scopus AI or scholarly search, reports the
  off-topic weakness, and links Chapter 11's table of risks. It was added as a
  separate paragraph so that the four product-claim excerpts quoting the
  preceding one are untouched.
- **Evaluation.** The 200-word opening paragraph is split in three. A new
  paragraph cites Liu, Zhang and Liang (2023): 51.5% of generated sentences
  fully supported by citations and 74.5% of citations supporting their
  sentence, across four generative search engines. It states that these were
  general web products in 2023, not scholarly tools. A reference entry was
  added.
- **History links.** DrQA, ORQA, REALM, Fusion-in-Decoder and RETRO linked
  arXiv while the reference list gave publishers' pages. The text now uses the
  reference list's links.

Visible words rise to about 2,810. The reading-time label moves from about 12
to about 13 minutes. One `id` was added; none was removed.

## Correction to the review as first reported

"Inline grep wins across the reported model–harness pairs" was reported as
stronger than the preprint's abstract, which says "generally". The preprint's
results section supports the appendix's wording exactly. The finding was
withdrawn.

## Limits of what was verified

- Liu, Zhang and Liang (2023), Li et al. (2024), LaRA and Rackauckas (2024)
  were read as abstracts only.
- The Scopus AI account was not rechecked against Elsevier's sources; the
  appendix dates it to 2024.
- RAGAs and Attributable to Identified Sources were not read.
- The page was not inspected in a browser.

## What was checked

- Every replacement was an exact match asserted to occur once.
- `tools/maintain.py`, the footnote check, the four builder `--check`s,
  `check-product-claims.py --as-of 2026-09-19` and the four Python test suites
  pass. The Node browser checks were not run.
