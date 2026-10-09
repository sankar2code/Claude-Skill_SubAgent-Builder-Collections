#!/usr/bin/env python3
"""Score options against pre-agreed weighted criteria and test how fragile the winner is.

Weights must sum to 100 and should be agreed at Gate 1, before evidence arrives.
Scores are 1-5 per option per criterion, each with a short evidence note.

Fragility test: every weight is moved up and down by --shift points (the others
rescaled to keep the total at 100). If the winner changes, the result is fragile
and the owner should look hard at that criterion.

Usage:
    python weighted_score.py criteria.json [--shift 10]

Input format: see assets/templates/criteria.json
Standard library only.
"""
import argparse
import json
import sys


def totals(weights, scores):
    return {o: sum(weights[c] * s[c] for c in weights) / 100 for o, s in scores.items()}


def shifted(weights, crit, delta):
    w = dict(weights)
    new = max(0.0, min(100.0, w[crit] + delta))
    rest = 100 - w[crit]
    w[crit] = new
    for c in w:
        if c != crit:
            w[c] = (weights[c] / rest * (100 - new)) if rest else 0
    return w


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--shift", type=float, default=10)
    a = ap.parse_args()
    spec = json.load(open(a.file))
    weights = {k: float(v) for k, v in spec["weights"].items()}
    problems = []
    if abs(sum(weights.values()) - 100) > 0.01:
        problems.append(f"weights sum to {sum(weights.values())}, not 100")
    if not spec.get("weights_agreed_by"):
        problems.append("weights_agreed_by is empty: weights must be agreed by the owner before scoring")

    scores, notes = {}, {}
    for o, crits in spec["options"].items():
        scores[o], notes[o] = {}, {}
        for c in weights:
            if c not in crits:
                problems.append(f"{o}: no score for '{c}'")
                scores[o][c] = 0
                continue
            item = crits[c]
            val = item["score"] if isinstance(item, dict) else item
            if not 1 <= float(val) <= 5:
                problems.append(f"{o}.{c}: score {val} outside 1-5")
            if not (isinstance(item, dict) and item.get("evidence")):
                problems.append(f"{o}.{c}: score has no evidence note")
            scores[o][c] = float(val)
    if not any("status quo" in o.lower() or "do nothing" in o.lower() for o in scores):
        problems.append("no status quo / do-nothing option scored")

    t = totals(weights, scores)
    ranked = sorted(t.items(), key=lambda x: -x[1])
    print("Weights: " + ", ".join(f"{c} {w:g}" for c, w in weights.items()))
    print("\n== Ranking (weighted score out of 5) ==")
    for i, (o, v) in enumerate(ranked, 1):
        print(f"  {i}. {o:<32} {v:.2f}")
    if len(ranked) > 1:
        margin = ranked[0][1] - ranked[1][1]
        print(f"\n  Lead over #2: {margin:.2f} points")

    winner = ranked[0][0]
    flips = []
    for c in weights:
        for d in (a.shift, -a.shift):
            w2 = shifted(weights, c, d)
            t2 = totals(w2, scores)
            top = max(t2, key=t2.get)
            if top != winner:
                flips.append(f"{c} {d:+g} pts -> {top} wins")
    print(f"\n== Fragility (each weight +/-{a.shift:g} pts) ==")
    if flips:
        print("  FRAGILE. Winner changes when:")
        for f in flips:
            print(f"    - {f}")
    else:
        print(f"  ROBUST. {winner} stays first under every shift.")

    print()
    if problems:
        print("WARNINGS:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("RESULT: scored. This ranks options; it does not choose. The owner decides at Gate 2.")


if __name__ == "__main__":
    main()
