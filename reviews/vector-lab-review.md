# The Vector Similarity Lab: evaluation

Evaluated 12 November 2026 against commit `4f2795c`. The lab
(`vector-similarity-lab.html`) was read in full and its tour and sandbox were
driven in headless Chromium at phone, tablet and desktop widths. Nine findings
were reported; a recheck requested by the author confirmed all nine. Eight were
applied. The ninth, adding Euclidean distance, was offered as optional and left
out.

## What was verified before any change

- Every score the tour quotes is what the page computes: cosine 0.914, 0.574
  and −0.530 for A, B and C; dot product 2.071 for B against 1.736 for A;
  identical scores after normalisation.
- The filter steps behave as described: B leads after the date filter and only
  C remains after both.
- The cut-off experiment works: with both filters and a limit of two, filtering
  first returns C and filtering afterwards returns nothing.
- No page errors, no external requests, and no sideways overflow at 390, 768 or
  1,024 pixels wide.

Nothing was broken in the way the BM25 lab's last step was.

## Applied

- **The cut-off experiment could not be found.** Chapter 13 sends readers to
  it, but linked the lab's front page, which opens the tour. The experiment sits
  in the sandbox inside a collapsed disclosure labelled "Optional". A link
  ending in `#cutoff-experiment` now opens the sandbox, loads the experiment,
  opens the disclosure and scrolls to it. Chapter 13 links there.
- **The tour was watch-only.** All seven controls were disabled at every step.
  Four steps now unlock one control each, once the prediction has been made:
  B's length at step 3, the normalisation switch at step 4, and one filter at
  each of steps 6 and 7. Step 4 now starts un-normalised, and steps 6 and 7 no
  longer apply their filter automatically; the answers tell the learner what to
  do and what to look for. A note under the tour's buttons says the other
  controls stay fixed until the sandbox.
- **Answers are remembered and steps can be skipped,** as in the BM25 lab.
- **Each step declares its own controls.** Visibility rules were keyed by step
  position, the design that broke the BM25 lab. A control now appears from the
  step that says it `introduces` it, and one function, `stepControls`, decides
  what is shown and unlocked.
- **Step 2 says that the arrows have moved.** B lengthens and C swings away
  between steps 1 and 2; only the lab's appendix mentioned it.
- **Layout.** The header is shorter, and the caveat that the vectors are
  teaching examples moved from under the header to beside the plot. At 1,280 by
  900 pixels the first question and the Next button are now on screen (862
  pixels; they were at 937). Below 1,180 pixels wide, where the tour sits above
  the lab, buttons jump between the question and the step's control.
- **The selected arrow's head.** Arrowheads scaled with the line, so the
  thicker selected line had a head several times too large. Markers now have a
  fixed size.

## Tests added

`tools/test-labs.cjs` now checks, for this lab, that each of the four acting
steps unlocks its own control and no other; that nothing is unlocked before a
prediction; that each control stays visible from the step introducing it; that
the eligibility warning appears only after a prediction on the steps that flag
it; that the acting steps start from the state their text describes; and that A
overtakes B under dot product when B is shorter than about 1.6, as step 3 now
says.

## Not applied

- **Euclidean distance as a third rule.** Figure 7.7 names it, and the lab
  could show that it agrees with cosine after normalisation. This is new
  teaching content and was left out.

## Limits of what was verified

- Screen-reader behaviour was not tested. Only headless Chromium was used.
- The teaching notes give the tour as seven prediction steps in about ten
  minutes. The count is unchanged; the timing was not retested, and four steps
  now ask the learner to do something as well as predict.
- The Rank Fusion Lab was not evaluated.

## What was checked afterwards

- `node tools/test-labs.cjs` passes.
- In the browser: each acting step unlocks its control only after an answer;
  shortening B to 1.5 at step 3 puts A first; ticking normalisation at step 4
  makes the two score columns identical; ticking the filters at steps 6 and 7
  gives B, then C alone; going back shows the earlier answer; a step can be
  skipped; the cut-off link opens the experiment in view; the phone jump
  buttons reach the plot and return to the question; no page errors.
- The book's maintenance pass, builder checks and Python test suites pass
  after the Chapter 13 link change.
