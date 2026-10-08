"""Cross-dataset OOD transfer: train probe on dataset A, test cold on dataset B.

In-distribution columns use document-grouped CV; transfer columns train on all of
one dataset, test on all of the other. Features: every ans_mean layer + final-layer
prompt_last (dynamic, so it works for any model's layer numbering).

Env: ACT_A/GEN_A (FinQA files), ACT_B/GEN_B (TAT-QA files), TAG.
Writes study/results/07_ood_transfer_{TAG}.md
"""

import hashlib
import json
import os
import pathlib

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import Reporter

from common import CACHE, DATA as OUT
ACT_A = os.environ.get("ACT_A", "activations_qwen_full.npz")
GEN_A = os.environ.get("GEN_A", "generations_qwen_full.jsonl")
ACT_B = os.environ.get("ACT_B", "activations_qwen_full_tatqa.npz")
GEN_B = os.environ.get("GEN_B", "generations_qwen_full_tatqa.jsonl")
TAG = os.environ.get("TAG", "qwen_full")


def doc_groups(gen_file):
    recs = [json.loads(l) for l in (OUT / gen_file).open()]
    return np.array([
        hashlib.md5(r["prompt"].split("Context:")[1].split("Question:")[0].encode()).hexdigest()
        for r in recs
    ])


def make_clf():
    return make_pipeline(
        StandardScaler(),
        LogisticRegression(C=0.1, max_iter=2000, class_weight="balanced"),
    )


def cv_auroc(X, y, groups):
    skf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)
    aucs = []
    for tr, te in skf.split(X, y, groups=groups):
        clf = make_clf()
        clf.fit(X[tr], y[tr])
        aucs.append(roc_auc_score(y[te], clf.predict_proba(X[te])[:, 1]))
    return np.mean(aucs)


def main():
    A = np.load(CACHE / ACT_A, allow_pickle=True)
    B = np.load(CACHE / ACT_B, allow_pickle=True)
    ga, gb = doc_groups(GEN_A), doc_groups(GEN_B)
    ya, yb = A["labels"], B["labels"]

    feats = sorted(
        [k for k in A.files if k.endswith("_ans_mean") and k in B.files],
        key=lambda k: int(k.split("_")[0][1:]),
    )
    max_l = max(int(k.split("_")[0][1:]) for k in feats)
    if f"L{max_l}_prompt_last" in A.files:
        feats.append(f"L{max_l}_prompt_last")
    if os.environ.get("FEATS"):  # optional comma-separated subset, e.g. FEATS=L24_ans_mean
        feats = [k for k in feats if k in os.environ["FEATS"].split(",")]

    rep = Reporter(f"07_ood_transfer_{TAG}", meta={
        "A (FinQA)": f"{ACT_A}, n={len(ya)}, correct={ya.mean():.3f}",
        "B (TAT-QA)": f"{ACT_B}, n={len(yb)}, correct={yb.mean():.3f}",
        "in-dist folds": "StratifiedGroupKFold(5) by document",
    })
    rep.log(f"{'feature':<20}{'A in-dist':>10}{'B in-dist':>10}{'A->B':>8}{'B->A':>8}")
    for k in feats:
        Xa, Xb = A[k], B[k]
        in_a, in_b = cv_auroc(Xa, ya, ga), cv_auroc(Xb, yb, gb)
        a2b = roc_auc_score(yb, make_clf().fit(Xa, ya).predict_proba(Xb)[:, 1])
        b2a = roc_auc_score(ya, make_clf().fit(Xb, yb).predict_proba(Xa)[:, 1])
        rep.log(f"{k:<20}{in_a:>10.3f}{in_b:>10.3f}{a2b:>8.3f}{b2a:>8.3f}")
    rep.save()


if __name__ == "__main__":
    main()
