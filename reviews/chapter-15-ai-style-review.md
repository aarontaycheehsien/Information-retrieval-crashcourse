# Chapter 15: AI-style phrasing review

Reviewed and applied: 22 October 2026, on `opus5.5-readabilty` after commit `5b708c0`. These are stylistic flags, not evidence of AI authorship. The rules match the Chapter 13 and 14 reviews.

The patterns found:
- “does not mean X; it means Y” corrections;
- “worth…” cues;
- aphoristic captions and asides;
- grand framing of what the book “was for”;
- the same “no loss function needed” point made three times.

Kept deliberately:
- The two bold key questions set as blockquotes (“Which parts of the retrieval pipeline were fixed…?” and “Can a librarian trace why a record was included…?”). They organise the first two sections.
- The single pull quote on reproducibility versus understanding.
- The “enough visibility / documentation / control” formula in the body, the summary and the check-yourself answer. It is the chapter’s stated minimum, and the summary is copied into Read this first.
- The closing “rizz” line, a deliberate callback to the Preface and Chapter 13.
- “what was actually searched”, where “actually” marks the difference between the typed and the executed query.
- Vendor question 16, which the evidence register quotes.

| # | Location | Passage | Why it stands out | Applied change |
|---|---|---|---|---|
| 1 | Opening | “The technical content of this book exists to make those four things possible.” | Grand framing | “The technical chapters are there to support those four tasks.” |
| 2 | Opening | “The third reads like procurement, and it is—but… the section is the shortest statement of what the preceding fourteen chapters were for. It converts every distinction…” | Staged concession; grand self-description | “The third is written for procurement, but its questions also help anyone at a renewal meeting make sense of a vendor’s answer. It turns the distinctions drawn in the preceding fourteen chapters into things a library can ask for and check.” |
| 3 | Reproducibility | “The useful question is therefore not simply ‘Is this search reproducible?’ but:” | “Not simply X but” | “A more useful question than ‘Is this search reproducible?’ is:” |
| 4 | Reproducibility | “This does not mean that every LLM call must vary; it means that identical output should not be assumed…” | “Does not mean X; it means Y” | “Not every LLM call will vary, but identical output should not be assumed…” |
| 5 | Reproducibility | Empty `<blockquote>` after the “Across all methods” paragraph | Markup left by commit `7d9bddb` | Removed |
| 6 | Interpretability | “Documentation records what was done. It does not, on its own, explain… Explaining is a separate property, and it needs separate vocabulary.” | Three-beat cadence | “Documentation records what was done but does not, on its own, explain why a particular record appeared. That needs separate vocabulary.” |
| 7 | Interpretability | “The second and third columns are worth reading together: the value of an explanation lies as much in what it rules out as in what it shows.” | “Worth” cue; aphorism | “Read the second and third columns together: an explanation is useful for what it rules out as well as for what it shows.” |
| 8 | Figure 15.2 caption | “…one that can show a matched term but not the transformed query has answered a question you did not ask.” | Aphoristic kicker | “How far back the trail goes is a useful measure of a product: showing a matched term without the transformed query leaves the earlier stages unexplained.” |
| 9 | Choosing tools | “…and is worth having to hand while the questions are being asked.” | “Worth” cue | “…; keep it to hand while asking them.” |
| 10 | Vendor question 15 | “…a product that cannot report it has settled that trade on your behalf.” | Aphoristic kicker | “…so a product that cannot report cost leaves the library unable to weigh it.” |
| 11 | After the questions | “None of these questions requires reading a loss function. All of them distinguish a retrieval design from a marketing label.” | Third statement of the same point (summary and check-yourself) | Paragraph removed |
| 12 | Summary | “…and the willingness to ask which one a vendor’s word names.” | Earnest flourish | “…and the habit of asking which one a vendor’s word names.” Read this first regenerated |
| 13 | Check yourself | “None of that requires reading a loss function.” | Repeats the summary | Sentence removed |

*Source text by Aaron Tay Chee Hsien, used under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*
