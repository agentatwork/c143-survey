#!/usr/bin/env python3
"""Print the self-reported table with the interval each benchmark size implies.

The half-width is deliberately the most generous one available: it assumes a
perfectly balanced split and both class accuracies equal to the headline, which
minimises the variance. Any real split is wider than this. It is a floor on the
uncertainty, not an estimate of it.
"""
import json, math

def halfwidth(ba, n):
    if not (ba and n):
        return None
    # balanced accuracy = (tpr + tnr) / 2, so var = (var_tpr + var_tnr) / 4
    return 1.96 * 0.5 * math.sqrt(2 * ba * (1 - ba) / (n / 2))

d = json.load(open("dataset.json"))
rows = sorted(d["self_reported"], key=lambda e: -(e["headline_ba"] or 0))
print(f"{'project':44s} {'BA':>7s} {'n':>7s} {'+-95%':>7s}   worst degraded it publishes")
for e in rows:
    ba, n = e["headline_ba"], e["eval_n"]
    hw = halfwidth(ba, n)
    deg = min(e["degraded"].values()) if e.get("degraded") else None
    print(f"{(e.get('repo') or e.get('site')):44s} "
          f"{(f'{ba*100:.1f}%' if ba else '-'):>7s} {(str(n) if n else '-'):>7s} "
          f"{(f'+-{hw*100:.1f}' if hw else '-'):>7s}   {(f'{deg*100:.1f}%' if deg else '')}")

bas = [e["headline_ba"] for e in rows if e["headline_ba"]]
ns = [e["eval_n"] for e in rows if e["eval_n"]]
print(f"\nheadline spread: {(max(bas)-min(bas))*100:.1f} points "
      f"({min(bas)*100:.1f}% .. {max(bas)*100:.1f}%)")
print(f"lowest headline sits {(min(bas)-0.75)*100:.1f} points above the 75.0% bar")
print(f"benchmark sizes span {max(ns)/min(ns):.0f}x  ({min(ns)} .. {max(ns)})")
