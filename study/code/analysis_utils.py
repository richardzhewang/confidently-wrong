"""Shared helpers for the camera-ready analyses (scripts 18-22).

Everything here is CPU-only and reads the released artifacts: scores/*.csv,
data/generations_*.jsonl, data/selfcons_*.jsonl and (where a refit is needed)
cache/activations_*.npz.
"""

import json

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import CACHE, DATA, SCORES, generations_path, pick_probe_feat, score_csv_path

BASE_KEYS = ["ans_mean_lp", "ans_min_lp", "gen_mean_lp", "p_true"]
MODELS = ["qwen", "llama", "gemma"]
CONDITIONS = [f"{m}_full_{d}" for d in ("finqa", "tatqa") for m in MODELS]
PRETTY = {"qwen": "Qwen3-8B", "llama": "Llama-3.1-8B", "gemma": "Gemma-2-9B"}
EXTRA = SCORES / "extra"  # per-example scores added for the camera-ready version


def act_path(cond):
    stem = cond[: -len("_finqa")] if cond.endswith("_finqa") else cond
    return CACHE / f"activations_{stem}.npz"


def load_scores(cond):
    return pd.read_csv(score_csv_path(cond), comment="#")


def load_generations(cond):
    return [json.loads(l) for l in generations_path(cond).open()]


def load_selfcons(cond):
    return {r["id"]: r for r in map(json.loads, (DATA / f"selfcons_{cond}.jsonl").open())}


def correct_sampling_rate(cond):
    p = DATA / f"selfcons_{cond}_meta.json"
    return json.loads(p.read_text())["correct_sampling_rate"] if p.exists() else 1.0


FINQA_ORIG_URL = "https://raw.githubusercontent.com/czyssrs/FinQA/main/dataset/train.json"


def finqa_original():
    """Original FinQA train.json (gold programs, tables, annotated answers). Row N of
    flare-finqa is row N of this file. Downloaded on first use (about 78 MB)."""
    p = DATA / "finqa_original_train.json"
    if not p.exists():
        import urllib.request
        print(f"downloading original FinQA annotations from {FINQA_ORIG_URL} ...", flush=True)
        urllib.request.urlretrieve(FINQA_ORIG_URL, p)
    return json.load(p.open())


def make_clf():
    return make_pipeline(
        StandardScaler(),
        LogisticRegression(C=0.1, max_iter=2000, class_weight="balanced"),
    )


def doc_folds(y, groups):
    """The paper's folds: 5-fold, document-grouped, class-stratified, seed 0.
    The split depends only on (y, groups) and row order, so it is reproducible
    from the scores CSV alone."""
    return list(StratifiedGroupKFold(5, shuffle=True, random_state=0)
                .split(np.zeros(len(y)), y, groups=groups))


def oof_scores(X, y, folds):
    p = np.full(len(y), np.nan)
    for tr, te in folds:
        p[te] = make_clf().fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
    return p


def stacked_oof(X, B, y, folds):
    """Nested stacking, identical to fit_scores.stacked_oof: an inner 3-fold CV inside
    each training fold produces the first-stage scores the combiner is trained on."""
    p = np.full(len(y), np.nan)
    for tr, te in folds:
        first = make_clf().fit(X[tr], y[tr])
        inner = np.zeros(len(tr))
        for itr, ite in StratifiedKFold(3, shuffle=True, random_state=1).split(X[tr], y[tr]):
            inner[ite] = make_clf().fit(X[tr][itr], y[tr][itr]).predict_proba(X[tr][ite])[:, 1]
        stack = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
        stack.fit(np.column_stack([inner, B[tr]]), y[tr])
        p[te] = stack.predict_proba(
            np.column_stack([first.predict_proba(X[te])[:, 1], B[te]]))[:, 1]
    return p


def auroc(y, s, w=None):
    return roc_auc_score(y, s, sample_weight=w)


def cluster_bootstrap(groups, n_boot=2000, seed=0):
    """Yield row-index arrays for a document-clustered bootstrap: source documents are
    resampled with replacement and all of a document's questions move together."""
    rng = np.random.default_rng(seed)
    groups = np.asarray(groups)
    uniq, inv = np.unique(groups, return_inverse=True)
    members = [np.flatnonzero(inv == g) for g in range(len(uniq))]
    for _ in range(n_boot):
        pick = rng.integers(0, len(uniq), len(uniq))
        yield np.concatenate([members[g] for g in pick])
