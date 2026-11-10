# Appendix B (How neural models receive text): review

Reviewed 10 November 2026 against commit `5837cb5`. The appendix was about 770
words with one HTML figure and one table. Twelve findings were reported; a
recheck requested by the author softened one and confirmed the rest against the
source and against `tools/wordpiece_example.py`. The author then asked for all
to be applied.

## Applied

- **Normalisation.** The figure said the uncased tokeniser lowercases the text.
  It also strips accents, as the repository's script reproduces. The figure step
  now says so, and a new paragraph gives the example `Schütze` → `schutze`.
- **How the split is chosen.** The same paragraph states the rule: take the
  longest vocabulary piece that matches from the start of the word, then repeat
  on the remainder. The script documents this as greedy longest-match-first.
- **The unknown token.** The paragraph adds that a word is replaced by `[UNK]`
  when no piece fits what is left. The script does this, and also for words
  over 100 characters, which the appendix does not mention.
- **Table B.1.** The byte row now shows the eight byte values for `rizzlord` and
  notes that `é` takes two bytes. For a plain-ASCII string the character and
  byte sequences are the same length, so the earlier row could not show the
  difference.
- **Lead-in.** The character and byte section no longer opens with a table.
- **Citations.** WordPiece cites Wu et al. (2016); character-level models name
  CANINE (Clark et al., 2022); both have new reference entries. Byte-pair
  encoding and SentencePiece now cite Sennrich et al. (2016) and Kudo and
  Richardson (2018), which were in the reference list but cited nowhere in the
  book. "BPE" is spelt out.
- **Framing.** Two of three near-identical opening sentences were removed.
- **Links.** The sequence-length paragraph links Appendix A's sentence on
  maximum input length. The closing sentence links Chapter 13's section on
  out-of-vocabulary strings.

Visible words rise from about 770 to about 990. The reading-time label moves
from about 3 to about 4 minutes. No `id` was added or removed.

## Limits of what was verified

- **The token IDs in Figure B.1 were not checked.** huggingface.co was outside
  the review environment's allowed network domains and the `transformers`
  library was not installed, so `tools/wordpiece_example.py` could not be run
  against the real vocabulary.
- The three new statements about the tokeniser follow the repository's script,
  which says it mirrors the original BERT `tokenization.py`. They were not
  checked against that file.
- The accent example and the byte values were computed locally with Python's
  `unicodedata` and UTF-8 encoding.
- No cited paper was read. Wu et al. (2016) and Clark et al. (2022) were
  confirmed to exist in OpenAlex. That BERT's paper cites Wu et al. for
  WordPiece, and that CANINE is character-level, are stated from memory and
  from the latter's title. Wu et al. has 31 authors; the reference entry names
  the first five, as OpenAlex returned them, and counts the rest.

## Correction to the review as first reported

It was reported that the unknown token is never mentioned. The appendix does say
a byte-level model works "without needing an unknown token at the byte level".
What was missing was that BERT's own tokeniser still falls back to one.

## Reference-list check (follow-up, 10 November 2026)

The count of 21 uncited entries reported above was wrong. It searched only the
text before the reference list and missed the footnotes and evidence register
that follow it. A second pass searched everything outside the reference list,
and the product-claims data, for each entry's link, author and year, and title.

- The list had 167 entries. Five were cited nowhere.
- **Joachims et al. (2005)** is now cited in Chapter 6, where the text says
  clicks can reward ranking position. The paper was not read for this check.
- **Removed** at the author's instruction: Clarivate (2025a), "Smart Search:
  Designing search for today's scholars"; Lens (2026), "Search syntax";
  OpenAlex (n.d.), "Open source code repositories"; and Semantic Scholar
  (n.d.), "How are documents ranked?". The remaining Clarivate 2025 entry lost
  its "b" suffix. The list now has 163 entries.
- Six entries were reported as cited by name but not linked (Chen et al., 2017;
  Lee et al., 2019; Guu et al., 2020; Izacard and Grave, 2021; Borgeaud et al.,
  2022; Sen et al., 2026). That was also wrong: Appendix G links each of them,
  to its arXiv page, while the reference list gives the publisher's page.
  Nothing was changed. Aligning the two sets of links is open.

The check finds entries with no citation. It does not confirm that each
citation supports its sentence, and it does not find works named in the text
that have no reference entry.

## What was checked

- Every replacement was an exact match asserted to occur once.
- `tools/maintain.py`, the footnote check, the four builder `--check`s,
  `check-product-claims.py --as-of 2026-09-19` and the four Python test suites
  pass. The Node browser checks were not run, and the page was not inspected in
  a browser.
