"""Supervised comparison signals trained with the probe's labels and folds.

Adds, per condition, out-of-fold scores for three deployable alternatives that use
no answer-conditioned internal state:

  cheap_lr      logistic regression on the four output signals (three token
                log-probability scores + P(True))
  cheap_lrq     the same after a rank-based (quantile-to-normal) transform fit on
                the training fold, which removes the heavy tails of the raw signals
  cheap_gbm     gradient-boosted trees on the four output signals
  cheap_best    the supervised output combination reported in the paper: per
                condition, the cheap_* variant with the highest full-population AUROC
                (a choice that favours the baseline)
  pregen        the pre-generation probe: same linear probe, same 2/3-depth layer,
                read at the last prompt token before any answer token exists
  pregen_cheap  nested stack of pregen + the four output signals

All use the paper's document-grouped, class-stratified 5 folds (seed 0) and the
same classifier settings as the answer-conditioned probe. As a check, the script
refits the answer-conditioned probe and compares it with the released `probe` column.

Writes scores/extra/{condition}.csv and results/19_supervised_baselines_{condition}.md
"""

import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import QuantileTransformer

from analysis_utils import (BASE_KEYS, CONDITIONS, EXTRA, act_path, auroc, doc_folds,
                            load_scores, oof_scores, stacked_oof)
from common import Reporter, pick_probe_feat


def oof_with(make, X, y, folds):
    p = np.full(len(y), np.nan)
    for tr, te in folds:
        p[te] = make().fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
    return p


def make_lrq():
    return make_pipeline(
        QuantileTransformer(n_quantiles=200, output_distribution="normal", random_state=0),
        LogisticRegression(C=1.0, max_iter=2000, class_weight="balanced"))


def make_gbm():
    return HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=200,
                                          class_weight="balanced", random_state=0)


def run(cond):
    df = load_scores(cond)
    act = np.load(act_path(cond), allow_pickle=True)
    assert list(act["ids"]) == list(df["id"]), "row order mismatch"
    y = df["correct"].to_numpy()
    assert (act["labels"] == y).all()
    groups = df["doc_group"].to_numpy()
    folds = doc_folds(y, groups)
    B = df[BASE_KEYS].to_numpy()
    feat = pick_probe_feat(act.files)                       # e.g. L24_ans_mean
    pre_feat = pick_probe_feat(act.files, "prompt_last")    # same layer, last prompt token

    probe_refit = oof_scores(act[feat], y, folds)
    Xpre = act[pre_feat]
    out = pd.DataFrame({
        "id": df["id"],
        "cheap_lr": oof_scores(B, y, folds),
        "cheap_lrq": oof_with(make_lrq, B, y, folds),
        "cheap_gbm": oof_with(make_gbm, B, y, folds),
        "pregen": oof_scores(Xpre, y, folds),
        "pregen_cheap": stacked_oof(Xpre, B, y, folds),
    })
    cheap_names = ["cheap_lr", "cheap_lrq", "cheap_gbm"]
    best = max(cheap_names, key=lambda k: auroc(y, out[k].to_numpy()))
    out["cheap_best"] = out[best]
    EXTRA.mkdir(parents=True, exist_ok=True)
    with (EXTRA / f"{cond}.csv").open("w") as f:
        f.write(f"# condition={cond} pregen_feature={pre_feat} "
                f"cheap_best={best} folds=StratifiedGroupKFold(5,doc,seed0) grader=v2\n")
        out.to_csv(f, index=False)

    rep = Reporter(f"19_supervised_baselines_{cond}", meta={
        "probe_feature": feat, "pregen_feature": pre_feat, "n": len(y)})
    rep.log(f"check: refit probe vs released column  max|diff|="
            f"{np.abs(probe_refit - df['probe']).max():.2e}  "
            f"AUROC refit {auroc(y, probe_refit):.4f} released {auroc(y, df['probe']):.4f}")
    conf = df["conf_greedy"].to_numpy()
    strata = {"full": np.ones(len(y), bool), "confident(8/8)": conf >= 1.0,
              "unsure(<8/8)": conf < 1.0}
    sig = {**{k: df[k].to_numpy() for k in BASE_KEYS},
           **{k: out[k].to_numpy() for k in cheap_names},
           f"cheap_best(={best})": out["cheap_best"].to_numpy(),
           "pregen": out["pregen"].to_numpy(),
           "pregen_cheap": out["pregen_cheap"].to_numpy(),
           "probe": df["probe"].to_numpy(), "probe_cheap(stacked)": df["stacked"].to_numpy()}
    rep.log(f"{'signal':<22}" + "".join(f"{s:>16}" for s in strata))
    for k, v in sig.items():
        rep.log(f"{k:<22}" + "".join(f"{auroc(y[m], v[m]):>16.3f}" for m in strata.values()))
    rep.log("n (wrong):            " + "".join(
        f"{f'{int(m.sum())} ({int((y[m] == 0).sum())})':>16}" for m in strata.values()))
    rep.save()


if __name__ == "__main__":
    for c in (sys.argv[1:] or CONDITIONS):
        run(c)
