"""STAGE 2 (instant, rerun freely): the stratified analysis suite [1]-[6].

Reads ONLY study/scores/{condition}.csv (produced by fit_scores.py) — no model
fitting happens here; every number is arithmetic on that table. Sections:

[1] full-population AUROC|PR-AUC   [3b] PR operating points (confident)
[2] 2x2 quadrant populations       [4]  specialist probe
[3] HEADLINE (confident stratum)   [5]  partial correlation
[3a] unsure stratum                [6]  measure agreement

Env: MODEL_TAG (qwen_full | llama_full | gemma_full; default = all three).
Writes study/results/12_two_by_two_{condition}.md
"""

import json
import os
import pathlib

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import (auc, average_precision_score, precision_recall_curve,
                             roc_auc_score)

from common import Reporter

from common import DATA, rel, score_csv_path
BASE_KEYS = ["ans_mean_lp", "ans_min_lp", "gen_mean_lp", "p_true"]


def pr_auc_wrong(y, p_correct, w=None):
    """AP for retrieving wrong answers. When the correct class was subsampled
    (see 10_selfconsistency.py), pass importance weights w = 1/sampling_rate for correct rows so
    precision reflects POPULATION prevalence, not the wrong-enriched subsample.
    (AUROC is rank-based and unaffected by one-class subsampling.)"""
    return average_precision_score(1 - np.asarray(y), -np.asarray(p_correct),
                                   sample_weight=w)


def both(y, s, w=None):
    return f"{roc_auc_score(y, s):.3f}|{pr_auc_wrong(y, s, w):.3f}"


def load_weights(name, df):
    """Importance weights from the self-consistency subsample meta file:
    correct rows weight 1/rate, wrong rows 1. All-ones if no subsampling."""
    meta_path = DATA / f"selfcons_{name}_meta.json"
    w = np.ones(len(df))
    if meta_path.exists():
        rate = json.loads(meta_path.read_text())["correct_sampling_rate"]
        w[df["correct"].to_numpy() == 1] = 1.0 / rate
    return w


def analyze(name):
    path = score_csv_path(name)
    if not path.exists():
        print(f"skip {name}: no {path} (run fit_scores.py first)")
        return
    header = path.open().readline().strip("# \n")
    df = pd.read_csv(path, comment="#")
    y = df["correct"].to_numpy()
    conf = df["conf_greedy"].to_numpy()
    has_conf = ~np.isnan(conf)
    p_probe = df["probe"].to_numpy()
    p_stack = df["stacked"].to_numpy()
    w = load_weights(name, df)

    rep = Reporter(f"12_two_by_two_{name}", meta={
        "scores_file": rel(path), "scores_header": header,
        "n": len(y), "correct_rate": round(float(y.mean()), 3),
        "documents": df["doc_group"].nunique(),
        "confidence_measured_on": f"{int(has_conf.sum())}/{len(y)}",
        "format": "AUROC|PR-AUC (wrong-as-positive; PR baseline = printed prevalence)",
    })

    rep.log(f"[1] full population (n={len(y)}, prevalence wrong={1 - y.mean():.2f}):")
    for k in BASE_KEYS:
        rep.log(f"    {k:<15} {both(y, df[k])}")
    if has_conf.any():
        rep.log(f"    {'self-consist.':<15} {both(y[has_conf], conf[has_conf])}"
                + ("  (conf-measured subset)" if not has_conf.all() else ""))
    rep.log(f"    {'PROBE':<15} {both(y, p_probe)}")
    rep.log(f"    {'probe+baselines':<15} {both(y, p_stack)}")

    rep.log("")
    rep.log("[2] 2x2 quadrants (confidence-measured subset; reweighted population "
            "shares live in results/quadrants.md):")
    for thr in (0.75, 1.0):
        c = (conf >= thr) & has_conf
        u = (conf < thr) & has_conf
        line = (f"    conf>={thr:.2f}: confident {int(c.sum()):4d} "
                f"(acc {y[c].mean():.1%}) | unsure {int(u.sum()):4d}")
        if u.any():
            line += f" (acc {y[u].mean():.1%})"
        line += f" | confident-wrong = {int(((y == 0) & c).sum())}"
        rep.log(line)

    rep.log("")
    rep.log("[3] HEADLINE - confident stratum (best-baseline = deployment-cheap set, "
            "excludes self-consistency; PR metrics population-reweighted):")
    for thr in (0.75, 1.0):
        c = (conf >= thr) & has_conf
        if len(np.unique(y[c])) < 2:
            continue
        wc = w[c]
        prev_w = wc[y[c] == 0].sum() / wc.sum()
        bb = max(roc_auc_score(y[c], df[k][c]) for k in BASE_KEYS)
        bbp = max(pr_auc_wrong(y[c], df[k][c], wc) for k in BASE_KEYS)
        rep.log(f"    conf>={thr:.2f} (n={int(c.sum())}, {int((y[c]==0).sum())} wrong, "
                f"pop-prev={prev_w:.2f}):  best-baseline {bb:.3f}|{bbp:.3f}  "
                f"probe {both(y[c], p_probe[c], wc)}  stacked {both(y[c], p_stack[c], wc)}")

    rep.log("")
    rep.log("[3a] unsure stratum (best-baseline = deployment-cheap set, excludes "
            "self-consistency; PR population-reweighted):")
    u = (conf < 1.0) & has_conf
    if len(np.unique(y[u])) == 2:
        wu = w[u]
        prev_w = wu[y[u] == 0].sum() / wu.sum()
        bb = max(roc_auc_score(y[u], df[k][u]) for k in BASE_KEYS)
        bbp = max(pr_auc_wrong(y[u], df[k][u], wu) for k in BASE_KEYS)
        rep.log(f"    (n={int(u.sum())}, {int((y[u]==0).sum())} wrong, "
                f"pop-prev={prev_w:.2f}):  best-cheap-baseline {bb:.3f}|{bbp:.3f}  "
                f"probe {both(y[u], p_probe[u], wu)}  "
                f"stacked {both(y[u], p_stack[u], wu)}  "
                f"(self-consist ref {both(y[u], conf[u], wu)} — stratifier, not competitor)")

    rep.log("")
    rep.log("[3b] PR operating points, conf=1.00 stratum (probe; population-reweighted):")
    c = (conf >= 1.0) & has_conf
    if len(np.unique(y[c])) == 2:
        yc, sc_, wc = y[c], -p_probe[c], w[c]
        wrong = yc == 0
        order = np.argsort(-sc_)
        prec, rec, _ = precision_recall_curve(wrong.astype(int), sc_, sample_weight=wc)
        prev_w = wc[wrong].sum() / wc.sum()
        rep.log(f"     trapezoidal PR area {auc(rec, prec):.3f} "
                f"(AP {pr_auc_wrong(yc, p_probe[c], wc):.3f}, pop-prev {prev_w:.2f})")
        rep.log(f"     {'budget':>8}{'precision':>11}{'recall':>9}   (weighted)")
        cw = np.cumsum(wc[order])
        tot_w, wrong_w = wc.sum(), wc[wrong].sum()
        for b in (0.05, 0.10, 0.20, 0.30, 0.50):
            k = int(np.searchsorted(cw, b * tot_w)) + 1
            flagged = order[:k]
            tp_w = wc[flagged][wrong[flagged]].sum()
            rep.log(f"     {b:>7.0%}{tp_w / cw[k - 1]:>11.2f}{tp_w / wrong_w:>9.2f}")

    spec = df["specialist"].to_numpy()
    m_spec = ~np.isnan(spec)
    if m_spec.sum() > 30 and len(np.unique(y[m_spec])) == 2:
        rep.log("")
        rep.log(f"[4] specialist probe (confident-trained): {both(y[m_spec], spec[m_spec])} "
                f"(general probe, same rows: {both(y[m_spec], p_probe[m_spec])})")

    rep.log("")
    rep.log("[5] partial correlation of probe score with correctness:")
    m = has_conf
    r_raw = pearsonr(p_probe[m], y[m])[0]
    Z = np.column_stack([conf[m]] + [df[k][m] for k in BASE_KEYS])
    Z = (Z - Z.mean(0)) / (Z.std(0) + 1e-9)
    beta_p, *_ = np.linalg.lstsq(Z, p_probe[m] - p_probe[m].mean(), rcond=None)
    beta_y, *_ = np.linalg.lstsq(Z, y[m] - y[m].mean(), rcond=None)
    r_part = pearsonr(p_probe[m] - Z @ beta_p, y[m] - Z @ beta_y)[0]
    rep.log(f"    raw r={r_raw:.3f} | partialling out all confidence measures r={r_part:.3f}")

    rep.log("")
    rep.log("[6] measure agreement (Spearman):")
    rep.log(f"    self-consist vs p_true      {spearmanr(conf[m], df['p_true'][m]).statistic:.3f}")
    rep.log(f"    self-consist vs ans_mean_lp {spearmanr(conf[m], df['ans_mean_lp'][m]).statistic:.3f}")
    rep.log(f"    probe vs self-consist       {spearmanr(p_probe[m], conf[m]).statistic:.3f}")
    rep.save()


def main():
    tag = os.environ.get("MODEL_TAG", "")
    tags = [tag] if tag else ["qwen_full", "llama_full", "gemma_full"]
    names = [f"{t}_{d}" for t in tags for d in ("finqa", "tatqa")]
    for n in names:
        analyze(n)


if __name__ == "__main__":
    main()
