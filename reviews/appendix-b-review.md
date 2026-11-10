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

## Open, beyond this appendix

Of 127 reference entries with a link, 21 have a link that is used nowhere in the
main text. The match was on the link only, so some may be cited by name alone;
only Sennrich and Kudo were checked properly, and both are now cited. The rest
need a separate pass.

## What was checked

- Every replacement was an exact match asserted to occur once.
- `tools/maintain.py`, the footnote check, the four builder `--check`s,
  `check-product-claims.py --as-of 2026-09-19` and the four Python test suites
  pass. The Node browser checks were not run, and the page was not inspected in
  a browser.
