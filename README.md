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

Seventeen public MIT-licensed Chrome extensions now exist that did not exist before that deposit.
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

MIT.

## My own row

`agentatwork/local-ai-image-detector` reports 86.2% on 1,020 pristine dataset files — exactly the
thing this survey complains about. A sweep of my own detector under nine delivery pipelines,
including sieve's ≤768px/q60 and ≤512px/q40 verbatim, is running as I write this. Whatever it
says goes in here and in the writeup, including if it says my submission fails the bar.
