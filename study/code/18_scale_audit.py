"""Scale-convention audit and grading sensitivity (camera-ready analysis).

The grader (common.grade) accepts a prediction that matches the gold answer within 2%
after multiplying by any s in {1, 100, 0.01, 1000, 0.001}. This script audits every
graded-correct answer that is accepted ONLY through a non-identity scale and asks
whether the rescaling is an equivalent representation or a possible magnitude error.

Audit rule (mechanical, reproducible):
  * percent-type question: the quantity is a percentage or ratio, so "0.532" and
    "53.2" are the same answer. A question is percent-type if
      - FinQA: the annotators' own answer string in the original FinQA release is
        written in percent form (contains '%'; the executable gold answer used for
        grading is the decimal fraction), or the question asks for a percent, rate,
        ratio, proportion, portion, growth, margin, return or yield;
      - TAT-QA: the gold string carries '%' or the question uses those words.
  * a x100 / x0.01 match on a percent-type question is SUPPORTED (equivalent
    representation).
  * every other non-identity match (x1000 / x0.001 thousand-scale matches, and
    x100 / x0.01 matches on questions that are not percent-type) is UNIT-DEPENDENT:
    whether it is correct depends on the unit fixed by the context.

Sensitivity ("restricted grading"): every unit-dependent match is relabelled WRONG,
the 8-sample confidence is recomputed with the same restricted matching rule, the
probe is refit on the new labels with the same folds protocol, and the confident-
subgroup comparison is recomputed. This is a bound: it treats every unit-dependent
match as a magnitude error.

Usage: python 18_scale_audit.py [condition ...]
Writes results/18_scale_audit_{condition}.md and results/18_scale_audit_cases_{condition}.csv
"""

import json
import re
import sys

import numpy as np
import pandas as pd

from analysis_utils import (BASE_KEYS, CONDITIONS, act_path, auroc, correct_sampling_rate,
                            doc_folds, finqa_original, load_generations, load_scores,
                            load_selfcons, oof_scores)
from common import DATA, RESULTS_DIR, Reporter, parse_number, pick_probe_feat

TOL = 0.02
PCT_Q = re.compile(r"percent|%|\brate\b|ratio|proportion|portion|growth|margin|\breturn\b|yield",
                   re.IGNORECASE)


def close(a, b):
    if b == 0:
        return abs(a) < 1e-6
    return abs(a - b) / max(abs(b), 1e-12) <= TOL


def scale_hit(pred_str, gold_str):
    """Return the first scale under which pred matches gold (identity first), else None."""
    p, _ = parse_number(str(pred_str))
    g, _ = parse_number(str(gold_str))
    if p is None or g is None:
        return None
    for s in (1.0, 100.0, 0.01, 1000.0, 0.001):
        if close(p * s, g):
            return s
    return None


def grade_restricted(pred_str, gold_str, pct_ok):
    s = scale_hit(pred_str, gold_str)
    return s == 1.0 or (pct_ok and s in (100.0, 0.01))


def question_of(rec):
    q = rec["query"]
    return q[q.rfind("Question:"):] if "Question:" in q else q


def percent_type(cond, recs):
    if cond.endswith("_finqa"):
        orig = finqa_original()
        out = []
        for r in recs:
            o = orig[int(r["id"].replace("finqa", ""))]["qa"]
            assert o["question"].strip().lower()[:40] in r["query"].lower()
            out.append("%" in str(o["answer"]) or bool(PCT_Q.search(o["question"])))
        return np.array(out)
    return np.array(["%" in str(r["gold"]) or bool(PCT_Q.search(question_of(r))) for r in recs])


def confident_table(rep, tag, y, conf, probe, df, w):
    c = conf >= 1.0
    best = max(auroc(y[c], df[k].to_numpy()[c], w[c]) for k in BASE_KEYS)
    pa = auroc(y[c], probe[c], w[c])
    rep.log(f"  {tag:<34} n={int(c.sum()):>5} wrong={int((y[c] == 0).sum()):>5}  "
            f"best-baseline {best:.3f}  probe {pa:.3f}  delta {pa - best:+.3f}   "
            f"| full-pop probe {auroc(y, probe):.3f}")
    return pa - best


def run(cond):
    df = load_scores(cond)
    recs = load_generations(cond)
    assert [r["id"] for r in recs] == list(df["id"])
    sc = load_selfcons(cond)
    y0 = df["correct"].to_numpy().astype(int)
    pct = percent_type(cond, recs)
    hits = [scale_hit(r["pred"], r["gold"]) for r in recs]
    assert all((h is not None) == bool(c) for h, c in zip(hits, y0)), "grader mismatch"

    kind = np.array(["wrong" if h is None else "identity" if h == 1.0 else
                     ("percent_supported" if p else "percent_unsupported") if h in (100.0, 0.01)
                     else "thousand_scale" for h, p in zip(hits, pct)])
    rep = Reporter(f"18_scale_audit_{cond}", meta={"n": len(y0), "tolerance": TOL})
    n_corr = int(y0.sum())
    rep.log(f"[1] how graded-correct answers are accepted (n correct = {n_corr}):")
    for k in ["identity", "percent_supported", "percent_unsupported", "thousand_scale"]:
        n = int((kind == k).sum())
        rep.log(f"    {k:<22}{n:>6}  {n / n_corr:6.1%} of correct  {n / len(y0):6.1%} of all")
    nonid = (y0 == 1) & (kind != "identity")
    unit_dep = np.isin(kind, ["percent_unsupported", "thousand_scale"])
    rep.log(f"    accepted only via rescaling: {int(nonid.sum())} "
            f"({nonid.sum() / n_corr:.1%} of correct); of these supported percent matches "
            f"{(kind == 'percent_supported').sum() / max(nonid.sum(), 1):.1%}, "
            f"unit-dependent {int(unit_dep.sum())} ({unit_dep.sum() / len(y0):.2%} of all answers)")

    pd.DataFrame([{"id": r["id"], "gold": r["gold"], "pred": r["pred"], "scale": h, "kind": k,
                   "question": question_of(r)[:300]}
                  for r, h, k in zip(recs, hits, kind) if k in ("percent_unsupported",
                                                                "thousand_scale")]
                 ).to_csv(RESULTS_DIR / f"18_scale_audit_cases_{cond}.csv", index=False)

    # ---- restricted grading: labels, confidence, probe refit -------------------------
    yR = np.array([int(grade_restricted(r["pred"], r["gold"], p)) for r, p in zip(recs, pct)])
    assert (yR <= y0).all() and int((y0 - yR).sum()) == int(unit_dep.sum())
    conf0 = df["conf_greedy"].to_numpy()
    confR = np.full(len(y0), np.nan)
    for i, (r, p) in enumerate(zip(recs, pct)):
        if r["id"] in sc:
            s = sc[r["id"]]["samples"]
            confR[i] = sum(grade_restricted(x, r["pred"], p) for x in s) / len(s)
    assert (np.isnan(confR) == np.isnan(conf0)).all()

    act = np.load(act_path(cond), allow_pickle=True)
    assert list(act["ids"]) == list(df["id"])
    X = act[pick_probe_feat(act.files)]
    groups = df["doc_group"].to_numpy()
    probeR = oof_scores(X, yR, doc_folds(yR, groups))
    # confidence was measured on all wrong answers and a random subsample of correct
    # ones; relabelled answers come from the subsampled class, so weight by 1/rate
    w = np.where(y0 == 1, 1.0 / correct_sampling_rate(cond), 1.0)

    rep.log("")
    rep.log(f"[2] restricted grading: {int(unit_dep.sum())} labels flip correct->wrong; "
            f"accuracy {y0.mean():.3f} -> {yR.mean():.3f}; "
            f"8/8-confident (measured) {int((conf0 >= 1).sum())} -> {int((confR >= 1).sum())}")
    rep.log("[3] confident subgroup (8/8), AUROC:")
    d0 = confident_table(rep, "paper grading", y0, conf0, df["probe"].to_numpy(), df, w)
    d1 = confident_table(rep, "restricted labels, paper confidence", yR, conf0, probeR, df, w)
    d2 = confident_table(rep, "restricted labels + confidence", yR, confR, probeR, df, w)
    rep.log(f"  delta: paper {d0:+.3f} | restricted labels {d1:+.3f} | "
            f"restricted labels + confidence {d2:+.3f}")
    rep.save()


if __name__ == "__main__":
    for c in (sys.argv[1:] or CONDITIONS):
        run(c)
