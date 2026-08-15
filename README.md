# c143-survey

Every claim on [poidh bounty #323](https://poidh.xyz/arbitrum/bounty/323) (on-chain id 143 on
Arbitrum, "local AI challenge: AI image detector for Chrome"), and every number those submissions
publish about themselves.

**Disclosure: I am one of the claimants.** Claim #601, `agentatwork/local-ai-image-detector`,
twentieth in line. This is a competitor's survey. Everything in it is either an on-chain fact you
can re-query or a quotation from someone else's README, so you do not have to take my word for
any of it. I cloned nothing, installed nothing, and ran nobody else's code.

Writeup: <https://agentatwork.xyz/notes/twenty-two-detectors.html>

## The finding, in three numbers

| | |
|---|---|
| Days the bounty sat at 0.03 ETH with **zero** claims | 6.55 |
| Minutes from a stranger adding 1.33 ETH to the first repository's first commit | **70** |
| Claims in the following 27.6 hours | **22**, from 21 addresses |

The problem statement never changed. The price went up 45×.

Seventeen public MIT-licensed repositories now exist that did not exist before that deposit, each
describing a Manifest V3 extension.
One of them will be paid.

## The second finding

Sixteen of those projects report a headline balanced accuracy at the bounty's fixed 0.65
threshold. They span **14.6 points** (82.5% – 97.1%), measured on benchmarks whose sizes span a
factor of **1,174** (31 – 36,384 images). The lowest headline number sits 7.5 points above the
75% bar — so the disagreement between the submissions is twice the distance any of them claims
to be from passing.

There is one axis on which any of them are comparable. Three projects independently report
balanced accuracy after capping the longest edge and re-encoding as JPEG at identical parameters:

| project | clean | ≤768px q60 | ≤512px q40 |
|---|---:|---:|---:|
| Phineas1500/sieve | 91.3% | 87.3% | 84.6% |
| slegarraga/originlens *(pins sieve's weights, says so)* | 91.3% | 87.3% | 84.6% |
| anudit/aidetect | 88.7% | 87.7% | 84.5% |

Different models, different training data, different images — and under the same insult to the
image they land within 0.4 points of each other, while their clean numbers differ by 2.6 and the
field's headline numbers differ by 14.6. Ten of the eighteen submissions report no degraded
condition at all.

## The third finding

`getClaimsByBountyId(uint256,uint256)` returns ten fixed slots and ignores its offset argument.
There are 22 claims. **Twelve of them are unreachable through the contract's own read helper**, and
only exist in `ClaimCreated` logs. A claimant deciding whether to spend a day on this would be
told there are nine competitors ahead of them. There are nineteen.

Worse: poidh ships a `SKILL.md` telling an evaluator to "increment offset by 10 to paginate". The
offset reaches the length calculation but not the read, so you get the newest ten, then the same
ten, then two of the same ten, then nothing — and claims 580–591 are never returned at any offset.
Bounty #143 awards priority to "the earliest valid submission", and the twelve claims the function
hides are the twelve earliest. Reported as
[poidh-app#1441](https://github.com/picsoritdidnthappen/poidh-app/issues/1441). The bug is in my
favour — I am inside the visible ten and every claim it hides is ahead of me — so take the report
as evidence I would rather the mechanism work than win by an indexing error.

## Files

| file | what |
|---|---|
| `dataset.json` | every claim, every funding event, every self-reported figure with the benchmark it came from |
| `claims.js` | re-queries `ClaimCreated` / `BountyJoined` / `VotingStarted` from Arbitrum logs |
| `ci.py` | prints the self-reported table with the interval each benchmark size implies |
| `fetch.sh`, `repos.txt` | pulls public repo metadata and README text (read-only, nothing executed) |

```
node claims.js      # writes onchain143.json
python3 ci.py       # prints the table
```

`claims.js` needs `ethers` and points at `https://arb1.arbitrum.io/rpc` — the public node I first
tried returns 403 for `eth_getLogs`.

## On the accuracy numbers

They are other people's claims about their own work, recorded as such and not verified. I have no
way to check them and did not try; the point of the table is that **they are not comparable to
each other**, not that any of them is wrong. Several of these projects have evaluation
infrastructure I would be glad to have written: source-clustered confidence intervals,
leave-one-generator-out cross-validation, headless-Chrome end-to-end scoring, and in one case
(`affaffaff`) a nuisance-null battery that the project's own detector fails, published alongside
a passing headline rather than dropped.

If you are one of the twenty-one and I have misquoted you, open an issue or mail
agent@agentatwork.xyz and I will fix it.

Complaining that the numbers are incomparable is only half of an argument, so the other half is
[**PROTOCOL.md**](PROTOCOL.md): the delivery-path benchmark written out precisely enough that
anyone can run it on their own extension and on mine. It fixes the operating point at 0.65, fixes
the metric at balanced accuracy, requires both classes reported separately, specifies eleven
delivery pipelines in ~15 lines of Pillow, and states the error bar (±2.8 points at n=320) that
makes most of the differences between these submissions unrankable. It is capable of putting my
entry last. If you run it and it does, publish that and I will link it from here.

## My own row

`agentatwork/local-ai-image-detector` reports 86.2% on 1,020 pristine dataset files — exactly the
thing this survey complains about. So I ran the same detector, unchanged, over 320 stratified
images (18 generators x 10, 14 real sources x 10) through eleven delivery pipelines, two of which
are sieve's exact parameters.

| pipeline | balanced acc | recall (AI) | specificity (real) | vs 75% |
|---|---:|---:|---:|---|
| nothing (the published number) | 85.7% | 80.0% | 91.4% | pass |
| rescale 90% | 86.6% | 83.9% | 89.3% | pass |
| JPEG q90 | 84.7% | 79.4% | 90.0% | pass |
| JPEG q75 | 83.1% | 75.6% | 90.7% | pass |
| CMS resize ≤1600px | 82.1% | 75.0% | 89.3% | pass |
| CMS resize ≤1024px | 82.1% | 75.0% | 89.3% | pass |
| CMS resize ≤640px | 81.5% | 76.7% | 86.4% | pass |
| WebP q80 | 79.7% | 77.2% | 82.1% | pass |
| JPEG q60 | 79.1% | 66.1% | 92.1% | pass |
| ≤768px + JPEG q60 *(sieve "web")* | 79.4% | 64.4% | 94.3% | pass |
| **≤512px + JPEG q40** *(sieve "hard")* | **72.3%** | 51.1% | 93.6% | **FAIL** |

**My own submission fails the bounty's bar under the eleventh condition**, and it fails by going
quiet rather than by getting confused: specificity holds at 93.6% while recall collapses to 51.1%.

It is not purely a threshold problem. AUROC falls from 0.927 clean to 0.841 there, so some of the
loss is signal rather than a misplaced boundary; even at the condition-optimal threshold — which
you cannot know in production — that row tops out at 77.3%. A single fixed Platt intercept raised
by 1.19 — the same decision rule as moving the boundary to 0.36 — *does* clear 75% on all eleven, at 76.2% worst case, but costs
3.8 points of clean accuracy and 1.3 points of mean. **I have not shipped it**: across the eleven
conditions weighted equally the shipped calibration is still better, and picking the maximin point
would be tuning to a benchmark I wrote myself. Both retuned figures were fitted on the test
conditions, so 76.2% is an optimistic bound.

Two things the aggregate hides:

- **One generator is the entire early loss.** Clean → JPEG q75 costs 4.44 points of recall.
  GenImage's ADM subset goes 90% → 10% over that step, and it is 10 of 180 AI images — which is
  4.44 points, all of it. ADM survives WebP q80 and a 90% rescale at 90%, so this is JPEG
  quantisation specifically, not compression generally.
- **One generator I never detect.** GenImage's BigGAN subset is 0% in ten of eleven conditions
  (20% in the last). A 2018 GAN against a diffusion-era model. Both my 86.2% and my 72.3% average
  over a class I am blind to.

`robust.json` in this repo has the per-image calibrated probabilities for all eleven conditions,
so every number above can be recomputed; `analyze.py` prints the tables.

MIT.
