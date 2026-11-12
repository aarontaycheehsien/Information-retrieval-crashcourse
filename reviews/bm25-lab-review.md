# The BM25 Evidence Lab: evaluation

Evaluated 12 November 2026 against commit `ffd55a9`. The lab
(`bm25-evidence-lab.html`) was read in full, its test file
(`tools/test-labs.cjs`) was run, and the guided tour was driven step by step in
headless Chromium at desktop, tablet and phone widths. Eight findings were
reported; a recheck requested by the author confirmed all eight. Seven were
applied and one was left as it is.

## What was verified before any change

- Every number the tour quotes matches what the page computes: the rarity
  weight of `delulu` is about four times that of `job`; twenty repetitions raise
  the contribution from 1.88 to about 2.15, and by about 17% with length held
  fixed; Record D overtakes Record A at six appendix paragraphs; Record C ranks
  below Record F.
- The scoring form matches Chapter 3 and Appendix C.
- No page errors and no external requests.

## Applied

- **Step 7 could not be done.** The step says to use the synonym buttons. They
  were hidden at step 7 and shown at step 6, and the query box and term buttons
  are locked during the tour, so there was no way to add a synonym. The rule
  that shows the buttons named the sixth step by position and had not been
  updated when the boundary step was inserted before it. Each step now declares
  the controls it shows and unlocks (`use`), and one function,
  `stepControls`, reads those declarations for both visibility and locking. A
  step can no longer be left pointing at another step's controls.
- **Step 4 gave away step 5.** Step 4's appendix slider ran to 8, and Record D
  overtakes Record A at 6, which is the answer to step 5's question. The slider
  is capped at 5 during step 4 only.
- **Prompt and control were never on screen together.** At step 3 on a
  900-pixel-high window the tour panel ended at 812 pixels and the slider sat at
  1,459; on a phone the gap was about 1,830 pixels. Each step now has a button,
  "Go to this step's control", that scrolls to the control that step uses, and
  the results panel has "Back to the question" during the tour.
- **The Lucene numerator.** The lab says it uses the Lucene inverse-document-
  frequency form but keeps the classic (k₁ + 1) numerator, which Lucene removed
  in version 8.0. A note in the machinery section now says so and gives the
  factor of 2.2. Appendix C carries the same sentence.
- **Sideways overflow.** At 390 pixels wide the page was 409 pixels wide. The
  narrow layouts declared their columns as `1fr`, which cannot shrink below its
  content; they now use `minmax(0, 1fr)`.
- **Shared links.** A sandbox link stored the query, toggles and two sliders but
  not the candidate boundary or the selected record. Both are now stored
  (`n` and `s`) and validated on load.
- **Accents.** The hint under the query box now says that only unaccented
  letters and digits count as word characters, so an accented or hyphenated
  word is split.

## Tests added

`tools/test-labs.cjs` now checks that the last step shows the synonym buttons
and unlocks the admission toggle; that no other step shows the synonym
buttons; that the repetition, appendix and boundary steps unlock their own
sliders; that Record A still leads at step 4's slider limit and Record D leads
at step 5's; and that every step names a control to jump to. The earlier tests
exercised the scoring model only, which is why they passed with step 7 broken.

## Left as it is

- **Bar segments are mouse-only.** Their hover details have no keyboard
  equivalent. The "Why did this score?" table gives the same numbers.

## Change to the plan as proposed

The plan said to scroll the active control into view when a step opens. That
would have pushed the question off screen instead. The jump and return buttons
leave the learner in control of when to move.

## Limits of what was verified

- **Lucene.** The removal of (k₁ + 1) is taken from Lucene's issue tracker
  (LUCENE-8563, fixed in 8.0). The inverse-document-frequency form was checked
  against the Lucene 10.1 documentation. Elasticsearch's own output was not
  examined.
- The teaching notes were checked for statements that depend on the changed
  steps; none was found. Their timings were not retested.
- Screen-reader behaviour was not tested. Only headless Chromium was used.
- The Vector Similarity Lab and the Rank Fusion Lab were not evaluated.

## What was checked afterwards

- `node tools/test-labs.cjs` passes.
- In the browser, every step shows and unlocks the control its text names; the
  jump button brings the synonym buttons on screen at step 7; adding
  "unrealistic" there puts Record B first; a sandbox link with k = 2 and Record
  B selected reloads in that state; overflow is zero at 390 and 900 pixels; no
  page errors.
- The book's maintenance pass, builder checks and Python test suites pass
  after the Appendix C sentence.
