# The Rank Fusion Lab: evaluation

Evaluated 12 November 2026 against commit `5b5abe4`. The lab
(`rank-fusion-lab.html`, `assets/rank-fusion-core.js`,
`assets/rank-fusion-lab.js`) was read in full, its unit test
(`tools/test-rank-fusion.cjs`) was run, and it was driven in headless Chromium
at phone, tablet and desktop widths. Eight findings were reported; a recheck
requested by the author confirmed all eight. Five were applied and three were
left out.

## What was verified before any change

- The four experiments behave as described: the book's order A, C, B, D; C
  overtaking A and D when c moves from 0 to 60, with a tie at c = 1; A losing a
  contribution and D disappearing when list B supplies one record; scores
  unchanged when output depth falls to 1.
- Ties are detected with exact fractions and labelled.
- Input errors are reported clearly.
- No page errors, no external requests, no sideways overflow at 390 or 768
  pixels.

This was the soundest of the three labs.

## Applied

- **The result was far from the action.** On a 1,280 by 900 screen an
  experiment's button sat at 728 pixels and the first results row at 1,977, with
  both list boxes and the controls between them; the page did not scroll on
  click. Each experiment now writes its fused order beside the explanation:
  before and after the change for experiments 2 to 5, and the order alone for
  experiment 1. The line is announced to screen readers.
- **The first experiment's answer was on the page.** It asks the learner to
  predict the fused order, which the results table already showed. Moving the
  order next to the button would have made that worse, so the two were fixed
  together: for an experiment that changes nothing, the results table is hidden
  until the reveal, with a note saying why. Only experiment 1 is of that kind,
  and a test now asserts it.
- **A fifth experiment, "Agreement against one high rank".** X is first in list
  A only; Y is 20th in list A and is list B's 20th record, which list B
  initially withholds. Raising list B's depth to 20 moves Y from 1/80 = 0.01250
  to 2/80 = 0.02500, above X's 1/61 = 0.01639. It matches Chapter 10's
  self-check within the lab's limit of 20 records per list, and the
  explanation says so.
- **Score fusion.** The closing section now links Chapter 10's section on
  combining scores instead of ranks.
- **Shared links.** Editing the lists or controls writes them to the page
  address, as the other two labs do; opening such a link restores them, and an
  invalid link shows the ordinary input error. Choosing an experiment clears the
  address.

`tools/test-rank-fusion.cjs` checks the fifth experiment's numbers and that
only experiment 1 conceals its result. `tools/check-rank-fusion.mjs` now loops
over all experiments instead of exactly four. The teaching notes say "Five
experiments, about 12 minutes" and name the fifth.

## Left out

- **Answer choices for the predictions.** Predictions stay free-form.
- **A score-fusion mode.** The lab holds ranks only, so it still cannot show the
  score gaps RRF discards. Adding scores is new teaching content.
- **A weight control.** Lists keep equal weight.

## Limits of what was verified

- `tools/check-rank-fusion.mjs` was edited but not run: it needs Microsoft Edge.
- The new twelve-minute timing is an estimate, not a classroom measurement.
- Screen-reader behaviour was not tested beyond the markup.

## What was checked afterwards

- `node tools/test-rank-fusion.cjs` passes.
- In the browser: experiment 1 hides the results until revealed; experiments 2
  to 5 report the before-and-after order beside the explanation, on screen at
  desktop and phone widths; a shared link restores the lists and constant; an
  invalid link reports a duplicate identifier; no page errors; no overflow at
  390 pixels.
- A first version read the shared link after opening experiment 1, which had
  already cleared the address. The order was corrected and the link rechecked.
