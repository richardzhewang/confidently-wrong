"""Split leakage check: question-level folds vs document-grouped folds.

Both benchmarks ask several questions about the same source document. With
question-level folds, questions on one document land in both the training and the
test fold. This script fits the probe (2/3-depth layer, mean over generated tokens)
under both fold schemes and reports the pooled out-of-fold AUROC and the mean
per-fold AUROC, so the inflation caused by question-level folds can be read directly.

Needs study/cache/activations_*.npz. Usage: python 22_split_leakage.py [condition ...]
Writes study/results/22_split_leakage.md
"""

import sys

import numpy as np
from sklearn.model_selection import StratifiedKFold

from analysis_utils import CONDITIONS, act_path, auroc, doc_folds, load_scores, make_clf
from common import Reporter, pick_probe_feat


def cv(X, y, folds):
    p = np.full(len(y), np.nan)
    per_fold = []
    for tr, te in folds:
        p[te] = make_clf().fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
        per_fold.append(auroc(y[te], p[te]))
    return auroc(y, p), float(np.mean(per_fold))


def main():
    rep = Reporter("22_split_leakage_full", meta={
        "folds": "5-fold, class-stratified, seed 0; question-level vs document-grouped"})
    rep.log(f"{'condition':<20}{'docs':>6}{'n':>7} | pooled AUROC: {'question':>9}{'document':>10}"
            f"{'inflation':>11} | mean per-fold: {'question':>9}{'document':>10}{'inflation':>11}")
    for cond in (sys.argv[1:] or CONDITIONS):
        df = load_scores(cond)
        act = np.load(act_path(cond), allow_pickle=True)
        assert list(act["ids"]) == list(df["id"])
        X, y = act[pick_probe_feat(act.files)], df["correct"].to_numpy()
        groups = df["doc_group"].to_numpy()
        q = cv(X, y, list(StratifiedKFold(5, shuffle=True, random_state=0).split(X, y)))
        d = cv(X, y, doc_folds(y, groups))
        rep.log(f"{cond:<20}{len(set(groups)):>6}{len(y):>7} | {'':>14}{q[0]:>9.3f}{d[0]:>10.3f}"
                f"{q[0] - d[0]:>+11.3f} | {'':>15}{q[1]:>9.3f}{d[1]:>10.3f}{q[1] - d[1]:>+11.3f}")
    rep.save()


if __name__ == "__main__":
    main()
