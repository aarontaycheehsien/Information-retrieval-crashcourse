---
kind: "exercise"
id: "exercise3"
label: "End of Part III"
---

## Application exercise III — Diagnose a failure, then try to document it

Part III supplied a diagnosis (Chapter 13), a way to measure (Chapter 14) and a record (Chapter 15).
This exercise runs all three against a search that genuinely disappointed you.

1. Find a search where a product returned a poor result for a topic you know well enough to judge—ideally one where you can name a relevant record it missed.
2. Use Chapter 13’s diagnostic questions to determine whether the evidence points to a query–record vocabulary mismatch, a vocabulary or representation gap, training–deployment transfer, or a failure to preserve negation, relations or composition.
   More than one may apply.
   Record the evidence for each diagnosis, plausible alternatives and anything the product prevents you from establishing.
3. Apply one intervention that the diagnosis suggests.
   Treat it as a test rather than a guaranteed remedy, and record what changed.
4. Turn the failure into a measurement using the [evaluation kit’s workbook and guide](evaluation-kit.html).
   List five known relevant seed records and report their recovery separately.
   Pool and deduplicate the top ten results from both runs, then judge every pooled record against the same written relevance criteria, ideally without seeing which run retrieved it.
   Calculate precision@10 for each run from those judgements.
   If a run returns fewer than ten records, report the count and your denominator convention.
   Seed recovery is not precision@10 or an estimate of complete recall.
5. Now attempt the Chapter 15 record: query interpretation, candidate retrieval, ranking and fusion, and retrieval control (fixed, adaptive or agentic).
   Fill in everything the product will let you capture.

::: {.exercise-deliverable}
**Deliverable.** Two lists.
The diagnosis, alternatives and supporting evidence; and—more useful institutionally—a gap list of everything the product would not let you establish or record.
The second list is the practical case for or against renewal.
:::
