"""STAGE 1 (slow, rerun only when data/labels change): fit probes, write scores CSV.

For one condition (model x dataset), computes every per-example quantity the
reports need and writes study/scores/{condition}.csv — one row per question:

  id, doc_group, correct, conf_greedy,
  ans_mean_lp, ans_min_lp, gen_mean_lp, p_true,     (output-level baselines)
  probe,                                            (out-of-fold P(correct))
  stacked,                                          (probe+baselines, nested CV)
  specialist                                        (probe trained on confident-only
                                                     examples; NaN outside stratum)

STAGE 2 scripts (12_two_by_two.py, 14_quadrant_table.py, 17, 20, 21) read this CSV
only — no model fitting. The CSV is also the paper's replication artifact.

Rule of thumb: rerun this whenever generations_*, activations_*, selfcons_* or
baselines_* files change. Env: MODEL_TAG (qwen_full | llama_full | gemma_full; default =
all three), PROBE_FEAT (default: layer nearest 2/3 depth, ans_mean pooling).
"""

import hashlib
import json
import os
import pathlib

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import CACHE, SCORES, pick_probe_feat, score_csv_path
from common import DATA as OUT
BASE_KEYS = ["ans_mean_lp", "ans_min_lp", "gen_mean_lp", "p_true"]


def make_clf():
    return make_pipeline(
        StandardScaler(),
        LogisticRegression(C=0.1, max_iter=2000, class_weight="balanced"),
    )


def oof_scores(X, y, folds):
    p = np.full(len(y), np.nan)
    for tr, te in folds:
        clf = make_clf().fit(X[tr], y[tr])
        p[te] = clf.predict_proba(X[te])[:, 1]
    return p


def stacked_oof(X, B, y, folds):
    p = np.full(len(y), np.nan)
    for tr, te in folds:
        probe = make_clf().fit(X[tr], y[tr])
        inner = np.zeros(len(tr))
        for itr, ite in StratifiedKFold(3, shuffle=True, random_state=1).split(X[tr], y[tr]):
            c = make_clf().fit(X[tr][itr], y[tr][itr])
            inner[ite] = c.predict_proba(X[tr][ite])[:, 1]
        stack = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
        stack.fit(np.column_stack([inner, B[tr]]), y[tr])
        p[te] = stack.predict_proba(
            np.column_stack([probe.predict_proba(X[te])[:, 1], B[te]])
        )[:, 1]
    return p


def fit_condition(name, act_file, gen_file):
    act = np.load(CACHE / act_file, allow_pickle=True)
    base = {r["id"]: r for r in map(json.loads, (OUT / f"baselines_{name}.jsonl").open())}
    sc = {r["id"]: r for r in map(json.loads, (OUT / f"selfcons_{name}.jsonl").open())}
    recs = [json.loads(l) for l in (OUT / gen_file).open()]
    groups = np.array([
        hashlib.md5(r["prompt"].split("Context:")[1].split("Question:")[0].encode()).hexdigest()
        for r in recs
    ])
    ids = list(act["ids"])
    feat = os.environ.get("PROBE_FEAT") or pick_probe_feat(act.files)
    X, y = act[feat], act["labels"]
    B = np.array([[base[i][k] for k in BASE_KEYS] for i in ids])
    conf = np.array([sc[i]["conf_greedy"] if i in sc else np.nan for i in ids])

    folds = list(StratifiedGroupKFold(5, shuffle=True, random_state=0)
                 .split(X, y, groups=groups))
    print(f"{name}: fitting probe ({feat}) + stacked ...", flush=True)
    probe = oof_scores(X, y, folds)
    stacked = stacked_oof(X, B, y, folds)

    specialist = np.full(len(y), np.nan)
    c = (conf >= 0.75) & ~np.isnan(conf)
    if len(np.unique(y[c])) == 2 and (y[c] == 0).sum() >= 15:
        sfolds = list(StratifiedGroupKFold(5, shuffle=True, random_state=0)
                      .split(X[c], y[c], groups=groups[c]))
        specialist[c] = oof_scores(X[c], y[c], sfolds)

    df = pd.DataFrame({
        "id": ids, "doc_group": groups, "correct": y, "conf_greedy": conf,
        **{k: B[:, i] for i, k in enumerate(BASE_KEYS)},
        "probe": probe, "stacked": stacked, "specialist": specialist,
    })
    df.attrs["probe_feature"] = feat
    SCORES.mkdir(parents=True, exist_ok=True)
    path = score_csv_path(name)
    with path.open("w") as f:
        f.write(f"# condition={name} probe_feature={feat} "
                f"folds=StratifiedGroupKFold(5,doc) grader=v2\n")
        df.to_csv(f, index=False)
    print(f"wrote {path} (n={len(df)})", flush=True)


def main():
    tag = os.environ.get("MODEL_TAG", "")
    for tag in ([tag] if tag else ["qwen_full", "llama_full", "gemma_full"]):
        fit_condition(f"{tag}_finqa", f"activations_{tag}.npz", f"generations_{tag}.jsonl")
        fit_condition(f"{tag}_tatqa", f"activations_{tag}_tatqa.npz",
                      f"generations_{tag}_tatqa.jsonl")


if __name__ == "__main__":
    main()
