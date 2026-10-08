"""STAGE 2 (instant, rerun freely): abstention robustness of the headline stratum.

Confirms the confident-stratum probe advantage (12_two_by_two.py [3]) is NOT just
"the probe reads refusals". Abstentions ("the filing does not provide...") are trivially
probe-detectable; if they dominated the confident-wrong cell the headline Delta would be an
artifact. We (a) measure their prevalence, (b) show they ARE near-perfectly detected, then
(c) recompute the confident-stratum AUROC with abstention-wrongs removed from the positive
(wrong) class. The gap should survive — and in fact widen.

Reads scores/{condition}.csv (fit_scores.py) + data/generations_*.jsonl (01_generate.py)
for the answer text. Abstention flag = common.is_abstention (canonical). AUROC is rank-based
so no population reweighting is needed (see 12_two_by_two.pr_auc_wrong docstring).

Env: MODEL_TAG. Default (no tag) runs all six definitive conditions.
Writes study/results/17_abstention_robustness_{condition}.md
"""

import json
import os

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from common import Reporter, generations_path, is_abstention, rel, score_csv_path

BASE_KEYS = ["ans_mean_lp", "ans_min_lp", "gen_mean_lp", "p_true"]


def best_baseline(y, df, mask):
    """Max AUROC over deployment-cheap baselines on `mask` (higher score = predict correct;
    equals wrong-as-positive AUROC by symmetry — matches 12_two_by_two [3])."""
    return max(roc_auc_score(y[mask], df[k].to_numpy()[mask]) for k in BASE_KEYS)


def analyze(name):
    spath = score_csv_path(name)
    gpath = generations_path(name)
    if not spath.exists():
        print(f"skip {name}: no {spath} (run fit_scores.py first)")
        return
    if not gpath.exists():
        print(f"skip {name}: no {gpath} (run 01_generate.py first)")
        return

    header = spath.open().readline().strip("# \n")
    df = pd.read_csv(spath, comment="#")
    outputs = {r["id"]: r.get("output", "") for r in (json.loads(l) for l in gpath.open())}
    df["abstains"] = df["id"].map(lambda i: is_abstention(outputs.get(i, ""))).to_numpy()

    y = df["correct"].to_numpy().astype(int)
    conf = df["conf_greedy"].to_numpy()
    probe = df["probe"].to_numpy()
    abst = df["abstains"].to_numpy()

    rep = Reporter(f"17_abstention_robustness_{name}", meta={
        "scores_file": rel(spath), "scores_header": header,
        "generations_file": rel(gpath),
        "abstain_rule": "no ANSWER: line OR explicit 'not in filing' phrasing (common.is_abstention)",
        "metric": "AUROC (wrong-as-positive); rank-based, no reweighting needed",
    })

    n_wrong = int((y == 0).sum())
    n_abst_wrong = int(((y == 0) & abst).sum())
    rep.log(f"[A] abstention prevalence (full population n={len(df)}):")
    rep.log(f"    wrong answers                {n_wrong:>5}")
    rep.log(f"    of which abstentions         {n_abst_wrong:>5}  "
            f"({n_abst_wrong / max(n_wrong, 1):.1%} of wrong)")

    for thr in (0.75, 1.0):
        c = conf >= thr
        cw = c & (y == 0)
        rep.log("")
        rep.log(f"    conf>={thr:.2f}: confident-wrong {int(cw.sum()):>4}  "
                f"abstention-wrongs {int((cw & abst).sum()):>4}  "
                f"({(cw & abst).sum() / max(cw.sum(), 1):.1%})")

    rep.log("")
    rep.log("[B] are abstention-wrongs trivially detected? "
            "(positives = confident abstention-wrongs, negatives = confident-correct)")
    for thr in (0.75, 1.0):
        c = conf >= thr
        pos = c & (y == 0) & abst
        neg = c & (y == 1)
        if pos.sum() < 5 or neg.sum() < 5:
            rep.log(f"    conf>={thr:.2f}: too few (pos={int(pos.sum())}, neg={int(neg.sum())})")
            continue
        sub = pos | neg
        au_probe = roc_auc_score(y[sub], probe[sub])
        au_base = best_baseline(y, df, sub)
        rep.log(f"    conf>={thr:.2f} (pos={int(pos.sum())}, neg={int(neg.sum())}):  "
                f"probe {au_probe:.3f}   best-baseline {au_base:.3f}")

    rep.log("")
    rep.log("[C] headline robustness — confident-stratum AUROC, abstention-wrongs removed "
            "from the positive class:")
    rep.log(f"    {'stratum':<26}{'n':>6}{'wrong':>7}{'probe':>8}{'base':>8}{'Δ':>8}")
    for thr in (0.75, 1.0):
        c = conf >= thr
        keep_no_abst = ~((y == 0) & abst)  # drop abstention-wrongs, keep everything else
        for label, mask in [(f"conf>={thr:.2f} all", c),
                            (f"conf>={thr:.2f} no-abstain", c & keep_no_abst)]:
            if len(np.unique(y[mask])) < 2:
                rep.log(f"    {label:<26}{int(mask.sum()):>6}  (single class)")
                continue
            au_p = roc_auc_score(y[mask], probe[mask])
            au_b = best_baseline(y, df, mask)
            rep.log(f"    {label:<26}{int(mask.sum()):>6}{int((y[mask]==0).sum()):>7}"
                    f"{au_p:>8.3f}{au_b:>8.3f}{au_p - au_b:>+8.3f}")

    rep.save()


def main():
    tag = os.environ.get("MODEL_TAG", "")
    if tag:
        names = [f"{tag}_finqa", f"{tag}_tatqa"]
    else:
        names = [f"{m}_full_{d}" for m in ("qwen", "llama", "gemma")
                 for d in ("finqa", "tatqa")]
    for n in names:
        analyze(n)


if __name__ == "__main__":
    main()
