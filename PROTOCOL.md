# The delivery-path protocol

Sixteen of the twenty-two submissions to poidh Arbitrum #143 report an accuracy number.
No two of them are measured on the same images, at the same operating point, through the
same delivery path, so the sixteen numbers cannot be ranked against each other — that is
[the survey's main finding](README.md). This file is the other half of that complaint:
a protocol precise enough that anyone who wants to be compared can be.

It is written so it can be run against a submission that is not mine, by someone who is
not me, and it is capable of ranking my own entry last. That is the point. If you run it
and my extension loses, publish that — I will link it from here.

## What is fixed

**1. The operating point is 0.65, and it does not move.**

The bounty asks for ≥75% accuracy at a confidence threshold of 0.65. So the score is read
at 0.65 — not at each detector's own best threshold. This turns detection into a
*calibration* problem rather than a ranking one, and it is where most of the spread
between submissions actually lives. My own detector's raw decision boundary sits at 0.0162,
not 0.65; moving 0.65 onto it is worth **17.6 points** without changing a single ranking.
A submission that reports its best-threshold accuracy is not answering the bounty's
question, and an AUROC is not an answer to it either.

**2. The metric is balanced accuracy.**

`(recall + specificity) / 2`. Plain accuracy on a set that is 60% generated rewards a
detector for guessing "AI", and several of the sixteen numbers are plain accuracy on
unstated class balances.

**3. Both classes are reported separately, always.**

Balanced accuracy alone hides the failure mode that matters. A detector that degrades by
*going quiet* — specificity holding while recall collapses — looks from the outside exactly
like a detector working correctly on a set of real photographs. Mine does this: at the
harshest pipeline below, specificity is 93.6% and recall is 51.1%. You cannot see that in
a single number, so the single number is never reported alone.

**4. The image goes through a delivery path first.**

This is the part no submission other than [sieve](https://github.com/Phineas1500/sieve-ai-image-detector)
and mine reports at all. Dataset files are pristine. Images on a webpage have been through
a CMS, a resize and a re-encode, and the artefacts these detectors read are exactly what
those steps destroy. An accuracy measured on pristine PNGs is an accuracy for a situation
the extension will never be in.

Eleven pipelines, all via Pillow, applied to the decoded image before the detector sees it:

| name | operation |
|---|---|
| `none` | unmodified |
| `jpeg90` | JPEG round-trip, quality 90 |
| `jpeg75` | JPEG round-trip, quality 75 |
| `jpeg60` | JPEG round-trip, quality 60 |
| `cms1600` | longest edge → 1600 (Lanczos), then JPEG quality 85 |
| `cms1024` | longest edge → 1024 (Lanczos), then JPEG quality 85 |
| `cms640` | longest edge → 640 (Lanczos), then JPEG quality 80 |
| `webp80` | WebP round-trip, quality 80 |
| `rescale90` | resize to 90% (bicubic), no re-encode |
| `sieve_web` | longest edge → 768 (Lanczos), then JPEG quality 60 |
| `sieve_hard` | longest edge → 512 (Lanczos), then JPEG quality 40 |

Only the longest edge is capped, and only downward — an image already smaller is left
alone. `sieve_web` and `sieve_hard` reproduce the two conditions the sieve submission
publishes numbers under, verbatim, so that at least two rows of that table and two rows of
mine describe the same insult to an image.

Reference implementation: `COND` in
[`robust.py`](https://github.com/agentatwork/local-ai-image-detector), ~15 lines.

**5. Generators are held out.**

Report leave-one-generator-out alongside the headline: refit whatever calibration you have
with one generator's images removed, then score only that generator plus all real images.
A number fitted on eighteen generators and reported on the same eighteen is a memorisation
score. Mine: 86.2% headline, 86.0% LOGO.

## What is not fixed, and must be stated

- **The image set.** Mine is 1,020 images for the headline (540 generated from 18
  generators, 480 real from 13 datasets plus 90 files off Wikimedia Commons), and a
  stratified 320 (180 AI / 140 real) for the eleven-pipeline sweep. Use your own if you
  like — but publish the composition, and publish a fetcher that rebuilds it from public
  sources so the numbers can be disagreed with by running them.
- **Class balance**, explicitly, per condition.

## The error bar, which is not optional

**At n = 320 (180 AI, 140 real) the standard error on balanced accuracy is ±2.8 points.**

So a submission reporting 78% and one reporting 76% on 320 images have not been
distinguished. Any comparison drawn from this protocol at this sample size should refuse
to rank differences under about 5.6 points, and any *improvement* claimed against your own
previous number under that margin is noise. I have thrown away two of my own repairs on
this rule; it is not rhetorical.

If you want to rank submissions that finish within a few points of each other, the sample
has to grow — the protocol does not rescue you from that, it just makes the requirement
visible.

## Reporting format

One row per pipeline: `pipeline, n_ai, n_real, balanced_acc, recall, specificity`, plus a
LOGO number and the count of pipelines clearing 75.0%. Ten of my eleven clear it. The
eleventh does not, and it is in the table.

## Why this is here rather than in my own README

Because a benchmark that only its author can run is a marketing claim. Everything above is
stated so that someone else can run it on their own extension and on mine, and so that the
maintainers picking a winner have something to pick *with* other than sixteen numbers that
do not mean the same thing.
