"""Layer × pooling sweep: logistic-regression probes on every cached feature set.

For every (layer, pooling) feature set: 5-fold document-grouped CV AUROC/PR-AUC and
permuted-label control (selectivity). Layer 0 = non-contextual baseline.

Env: ACT_FILE / GEN_FILE / TAG (default = Qwen3-8B FinQA).
Writes study/results/03_layer_sweep_{TAG}.md
"""

import hashlib
import json
import os
import pathlib

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import Reporter

from common import CACHE, DATA as OUT
ACT_FILE = os.environ.get("ACT_FILE", "activations_qwen_full.npz")
GEN_FILE = os.environ.get("GEN_FILE", "generations_qwen_full.jsonl")
TAG = os.environ.get("TAG", "qwen_full_finqa")
RNG = np.random.default_rng(0)


def doc_groups(gen_file):
    recs = [json.loads(l) for l in (OUT / gen_file).open()]
    return np.array([
        hashlib.md5(r["prompt"].split("Context:")[1].split("Question:")[0].encode()).hexdigest()
        for r in recs
    ])


def cv_scores(X, y, groups):
    skf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)
    aucs, aps = [], []
    for tr, te in skf.split(X, y, groups=groups):
        clf = make_pipeline(
            StandardScaler(),
            LogisticRegression(C=0.1, max_iter=2000, class_weight="balanced"),
        )
        clf.fit(X[tr], y[tr])
        p = clf.predict_proba(X[te])[:, 1]
        aucs.append(roc_auc_score(y[te], p))
        aps.append(average_precision_score(1 - y[te], -p))
    return np.mean(aucs), np.std(aucs), np.mean(aps)


def main():
    data = np.load(CACHE / ACT_FILE, allow_pickle=True)
    y = data["labels"]
    groups = doc_groups(GEN_FILE)
    y_perm = RNG.permutation(y)
    rep = Reporter(f"03_layer_sweep_{TAG}", meta={
        "activations": ACT_FILE, "generations": GEN_FILE,
        "folds": "StratifiedGroupKFold(5) by document",
        "n": len(y), "base_rate_correct": round(float(y.mean()), 3),
    })

    keys = sorted(
        [k for k in data.files if k.startswith("L")],
        key=lambda k: (int(k.split("_")[0][1:]), k),
    )
    rep.log(f"{'feature':<18}{'AUROC':>8}{'±sd':>7}{'PR-AUC(wrong)':>14}"
            f"{'ctrl-AUROC':>12}{'select.':>9}")
    # 42 independent CV jobs (21 features x real+control) -> parallel across cores
    from joblib import Parallel, delayed

    jobs = [(k, lab) for k in keys for lab in ("real", "ctrl")]
    res = Parallel(n_jobs=10)(
        delayed(cv_scores)(data[k], y if lab == "real" else y_perm, groups)
        for k, lab in jobs
    )
    out = dict(zip(jobs, res))
    best_key, best_auc = None, 0
    for k in keys:
        auc, sd, ap = out[(k, "real")]
        ctrl, _, _ = out[(k, "ctrl")]
        rep.log(f"{k:<18}{auc:>8.3f}{sd:>7.3f}{ap:>14.3f}{ctrl:>12.3f}{auc - ctrl:>9.3f}")
        if auc > best_auc:
            best_key, best_auc = k, auc
    rep.log("")
    rep.log(f"best: {best_key} AUROC={best_auc:.3f}  "
            f"(PR-AUC prevalence baseline = {1 - y.mean():.3f})")
    rep.save()


if __name__ == "__main__":
    main()
