#!/usr/bin/env python3
"""Recompute every number in the "My own row" section from robust.json.

robust.json holds the raw two-view mean probability for each of 320 images under each
of 11 delivery pipelines, plus the labels and source names. Nothing here re-runs the
model; it is all arithmetic on stored scores, so anyone can check the tables without
downloading an 87 MB ONNX file.

    python3 analyze.py            # the three tables
    python3 analyze.py --sources  # per-source accuracy, every condition
"""
import json
import math
import sys

import numpy as np

# The shipped Platt parameters, from the extension's model.json.
CAL_A, CAL_B = 0.4644135546564986, 2.5266054348274327
THR = 0.65

d = json.load(open("robust.json"))
y = np.array(d["_meta"]["labels"])
srcs = np.array(d["_meta"]["sources"])
CONDS = [k for k in d if k != "_meta"]


def calibrated(p, a=CAL_A, b=CAL_B):
    m = np.clip(np.asarray(p), 1e-12, 1 - 1e-12)
    z = np.log(m / (1 - m))
    return 1 / (1 + np.exp(-(a * z + b)))


def ba(p, thr=THR):
    pred = p >= thr
    tpr = pred[y == 1].mean()
    tnr = (~pred)[y == 0].mean()
    return (tpr + tnr) / 2, tpr, tnr


def auroc(p):
    order = np.argsort(p)
    ranks = np.empty(len(p))
    ranks[order] = np.arange(1, len(p) + 1)
    n1, n0 = (y == 1).sum(), (y == 0).sum()
    return (ranks[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


P = {c: calibrated(d[c]["probs"]) for c in CONDS}


def table_headline():
    print(f"{'pipeline':12s} {'bal acc':>8s} {'recall':>7s} {'spec':>7s}   vs 75%")
    for c in CONDS:
        b, tpr, tnr = ba(P[c])
        print(f"{c:12s} {b*100:7.1f}% {tpr*100:6.1f}% {tnr*100:6.1f}%   "
              f"{'pass' if b >= 0.75 else 'FAIL'}")


def table_ceiling():
    print(f"\n{'pipeline':12s} {'at 0.65':>8s} {'best':>7s} {'@thr':>6s} {'AUROC':>7s}")
    for c in CONDS:
        p = P[c]
        best = max((ba(p, t)[0], t) for t in np.unique(np.round(p, 6)))
        print(f"{c:12s} {ba(p)[0]*100:7.1f}% {best[0]*100:6.1f}% {best[1]:6.3f} "
              f"{auroc(p):7.3f}")


def table_tradeoff():
    """The only free knob is the Platt intercept; moving it moves the boundary."""
    print("\nsingle fixed calibration, no knowledge of the pipeline:")
    # Raising b by logit(0.65) - logit(0.36) at a fixed 0.65 threshold is exactly the
    # same decision rule as leaving b alone and moving the boundary down to 0.36.
    shift = math.log(THR / (1 - THR)) - math.log(0.36 / 0.64)
    for label, b in (("as shipped", CAL_B), ("shifted", CAL_B + shift)):
        v = [ba(calibrated(d[c]["probs"], CAL_A, b))[0] for c in CONDS]
        print(f"  {label:11s} b={b:+.4f}  worst {min(v)*100:5.1f}%  "
              f"mean {np.mean(v)*100:5.1f}%  clean {v[0]*100:5.1f}%")


def table_sources():
    print(f"\n{'source':32s} lab " + " ".join(f"{c[:7]:>7s}" for c in CONDS))
    for s in sorted(set(srcs)):
        m = srcs == s
        lab = int(y[m][0])
        cells = []
        for c in CONDS:
            p = P[c][m]
            acc = (p >= THR).mean() if lab else (p < THR).mean()
            cells.append(f"{acc*100:6.0f}%")
        print(f"{s[:32]:32s} {'ai  ' if lab else 'real'} " + " ".join(cells))


def adm_share():
    """How much of each condition's recall loss is one generator."""
    print("\nshare of recall loss attributable to GenImage_ADM:")
    base = P["none"] >= THR
    ai, adm = y == 1, srcs == "GenImage_ADM"
    for c in CONDS[1:]:
        pred = P[c] >= THR
        d_all = pred[ai].mean() - base[ai].mean()
        d_adm = (pred[adm].mean() - base[adm].mean()) * adm.sum() / ai.sum()
        share = f"{d_adm/d_all*100:4.0f}%" if d_all else "   -"
        print(f"  {c:12s} recall {d_all*100:+6.2f}pt   ADM {d_adm*100:+6.2f}pt  {share}")


if __name__ == "__main__":
    table_headline()
    if "--sources" in sys.argv:
        table_sources()
    else:
        table_ceiling()
        table_tradeoff()
        adm_share()
