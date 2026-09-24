# Chapter 4: second readability pass

Reviewed 24 September 2026 against commit `47bf5cc`, with the Preface and
Chapters 5–11 read for context. The findings below **have been applied** in
commit `98234f4`.

The brief was readability with the content held fixed. The Part I pass
(`part-i-readability-review.md`) had already merged the chapter's duplicated
puzzle verdicts. The main problem left was that the reader met the same lists
several times over: the three admission rules three times on the first page,
and the four explanations for a missing word three times in the body.

## Applied

- **4.1** Removed the sentence before the admission-rule list that previewed
  the list.
- **4.2** The paragraph after the list no longer carries the missing-word
  checklist. It links to the section that sets it out.
- **4.3** "Any-match ranked retrieval" is now tied to Chapter 3's "direct BM25
  retrieval", with a link. The glossary's *ranked retrieval* first-use mark is
  kept.
- **4.4** The term-frequency saturation caveat now sits before Figure 4.2, next
  to the IDF point it qualifies. The section ends on "Good retrieval over a bad
  representation is still a bad search."
- **4.5** Figure 4.2's caption is two sentences instead of four.
- **4.6** Tightened missing-word items 2 and 3. Item 2 no longer quotes a
  section title inline. Item 3 separates the optional and unmatched cases from
  the strict-`AND` contrast.
- **4.7** "Early Google" is now a historical-example panel at the end of the
  lexical ≠ Boolean section, with its `id` kept on the panel's h4. The table of
  contents loses one h3. Footnotes 12–13 keep their order.
- **4.8** The rewriting section opens with its point instead of announcing
  itself. The claim excerpt for `primo-query-conversion` was updated.
- **4.9** The paragraph restating all four missing-word explanations is now
  one sentence: rewriting is story 2, and understanding alone removes nothing.
- **4.10** "Semantic Scholar remains unresolved" is stated once. The four open
  possibilities moved into the third-temptation paragraph (new anchor
  `#third-temptation`). The claim excerpt for
  `semantic-scholar-question-counts` was updated.
- **4.11** The first sentence of the "What a result screen can settle" panel is
  now a full sentence. The digest excerpt was rebuilt.
- **4.12** The "What Part I settles" introduction is two short sentences. It no
  longer repeats Chapter 1's display-versus-machinery line.
- **4.13** The Part II opener said Chapter 4's summary restates five Part I
  ideas, but it covered only two. The summary now also restates analysed terms,
  posting lists and candidate sets. The digest was rebuilt.

## Verification

- `maintain.py` found no problems. The product-claims, glossary and digest
  build `--check`s pass, as do `check-product-claims.py --as-of 2026-09-19` and
  the three Python test suites.
- The three Playwright checks pass: `check-product-claims.mjs`,
  `check-digest.mjs` and `check-glossary-hub.mjs`.
- Rendered page: no console errors and no broken internal links. There are 224
  `.term-mark`s, as before; Chapter 4 keeps all 12 of its marks. Chapter 4's
  rendered text went from about 3,155 to 3,049 words.
