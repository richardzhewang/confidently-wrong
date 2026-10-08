"""Paired uncertainty and an executable routing policy (camera-ready analyses).

Reads scores/{condition}.csv and scores/extra/{condition}.csv only (no fitting).

[A] Confident / unsure / full-population AUROC of the answer-conditioned probe against
    four comparison signals, with document-clustered paired bootstrap intervals for
    each difference (2,000 replicates; source documents are resampled, so all
    questions on one document move together; both signals are scored on the same
    resample). "best single" is the maximum over the four individual output
    signals and is re-selected inside every replicate.

[B] Review routing at fixed capacity. Same protocol as 16_economics.py: documents are
    split into an optimization half and an evaluation half (seed 0); everything is
    reported on the evaluation half. Policies need no confidence label at deployment:
      P(True), cheap (supervised output combination), pregen, probe,
      stacked (probe + output signals, nested stacking), and
      two-stage: review the alpha*b answers with the lowest cheap score (the visibly
        uncertain answers), then fill the rest of the budget b with the lowest probe
        scores among the remaining answers. alpha is chosen on the optimization
        half (grid 0, 0.1, ..., 1) and applied unchanged to the evaluation half.
    Reported: share of all wrong answers caught, and share of confident-wrong (8/8)
    answers caught (the 8-sample label is used here only to score the outcome).
    Paired document-clustered bootstrap intervals for recall differences.

Writes results/20_routing_and_uncertainty_{condition}.md
"""

import sys

import numpy as np
import pandas as pd

from analysis_utils import BASE_KEYS, CONDITIONS, EXTRA, auroc, cluster_bootstrap, load_scores
from common import Reporter

N_BOOT = 2000
CAPACITIES = [0.10, 0.20, 0.30]
ALPHAS = np.round(np.linspace(0, 1, 11), 1)


def halves(df):
    docs = sorted(df["doc_group"].unique())
    rng = np.random.default_rng(0)
    rng.shuffle(docs)
    m = df["doc_group"].isin(set(docs[: len(docs) // 2])).to_numpy()
    return m, ~m


def ci(a):
    lo, hi = np.percentile(a, [2.5, 97.5])
    return f"[{lo:+.3f}, {hi:+.3f}]"


def top_k(score, k):
    return np.argsort(score)[:k]            # lowest P(correct) first


def two_stage(cheap, probe, k, alpha):
    k1 = int(round(alpha * k))
    first = np.argsort(cheap)[:k1]
    rest = np.ones(len(cheap), bool)
    rest[first] = False
    rest = np.flatnonzero(rest)
    return np.concatenate([first, rest[np.argsort(probe[rest])[: k - k1]]])


def recall(y, picked, target=None):
    t = (y == 0) if target is None else target
    return t[picked].sum() / max(t.sum(), 1)


def run(cond):
    df = load_scores(cond).merge(pd.read_csv(EXTRA / f"{cond}.csv", comment="#"), on="id")
    y = df["correct"].to_numpy()
    conf = df["conf_greedy"].to_numpy()
    groups = df["doc_group"].to_numpy()
    S = {k: df[k].to_numpy() for k in BASE_KEYS + ["cheap_best", "pregen", "pregen_cheap",
                                                    "probe", "stacked"]}
    rep = Reporter(f"20_routing_and_uncertainty_{cond}", meta={
        "n": len(y), "bootstrap": f"document-clustered, paired, {N_BOOT} replicates, seed 0"})

    # ---------------- [A] AUROC differences with paired bootstrap CIs -----------------
    strata = {"confident(8/8)": conf >= 1.0, "unsure(<8/8)": conf < 1.0,
              "full": np.ones(len(y), bool)}
    comps = ["best_single", "cheap_best", "pregen", "pregen_cheap"]

    def stats(idx, m):
        yy = y[idx][m[idx]]
        if len(np.unique(yy)) < 2:
            return None
        a = {k: auroc(yy, v[idx][m[idx]]) for k, v in S.items()}
        a["best_single"] = max(a[k] for k in BASE_KEYS)
        return a

    boots = list(cluster_bootstrap(groups, N_BOOT, seed=0))
    rep.log("[A] AUROC and paired differences (probe minus comparison), 95% CI")
    for name, m in strata.items():
        point = stats(np.arange(len(y)), m)
        bs = [s for s in (stats(b, m) for b in boots) if s is not None]
        rep.log(f"  {name}: n={int(m.sum())} wrong={int((y[m] == 0).sum())}  "
                f"probe {point['probe']:.3f} {ci([s['probe'] for s in bs]).replace('+', '')}")
        for c in comps:
            d = [s["probe"] - s[c] for s in bs]
            rep.log(f"    vs {c:<13} {point[c]:.3f}   delta {point['probe'] - point[c]:+.3f} "
                    f"{ci(d)}   P(delta<=0)={np.mean(np.array(d) <= 0):.3f}")
        d = [s["stacked"] - s["probe"] for s in bs]
        rep.log(f"    stacked       {point['stacked']:.3f}   stacked-probe "
                f"{point['stacked'] - point['probe']:+.3f} {ci(d)}")

    # ---------------- [B] routing at fixed capacity ----------------------------------
    opt, ev = halves(df)
    yo, ye = y[opt], y[ev]
    cw_e = (ye == 0) & (conf[ev] >= 1.0)
    So = {k: v[opt] for k, v in S.items()}
    Se = {k: v[ev] for k, v in S.items()}
    ge = groups[ev]
    eboots = list(cluster_bootstrap(ge, N_BOOT, seed=1))
    pol = ["p_true", "cheap_best", "pregen", "probe", "stacked", "two_stage"]
    rep.log("")
    rep.log(f"[B] evaluation half: n={int(ev.sum())} wrong={int((ye == 0).sum())} "
            f"confident-wrong={int(cw_e.sum())}")
    rep.log(f"  {'capacity':>8} {'alpha':>6} | share of ALL wrong caught: "
            + " ".join(f"{p:>10}" for p in pol))
    rows_cw, diffs = [], []
    for b in CAPACITIES:
        ko, ke = int(round(b * opt.sum())), int(round(b * ev.sum()))
        alpha = max(ALPHAS, key=lambda a: (recall(yo, two_stage(So["cheap_best"], So["probe"],
                                                               ko, a)), -a))
        mask = {}
        for p in pol:
            picked = (two_stage(Se["cheap_best"], Se["probe"], ke, alpha) if p == "two_stage"
                      else top_k(Se[p], ke))
            mk = np.zeros(len(ye), bool)
            mk[picked] = True
            mask[p] = mk
        rep.log(f"  {b:>8.0%} {alpha:>6.1f} | {'':>27}"
                + " ".join(f"{recall(ye, mask[p]):>10.1%}" for p in pol))
        rows_cw.append(f"  {b:>8.0%} {'':>6} | {'':>27}"
                       + " ".join(f"{recall(ye, mask[p], cw_e):>10.1%}" for p in pol))
        # paired bootstrap: reviewed sets are fixed, documents are resampled
        w = (ye == 0)
        for a_, b_ in [("probe", "p_true"), ("probe", "cheap_best"), ("probe", "pregen"),
                       ("stacked", "probe"), ("two_stage", "probe")]:
            d_all = [(w[i] & mask[a_][i]).sum() / w[i].sum() - (w[i] & mask[b_][i]).sum() / w[i].sum()
                     for i in eboots]
            d_cw = [(cw_e[i] & mask[a_][i]).sum() / max(cw_e[i].sum(), 1)
                    - (cw_e[i] & mask[b_][i]).sum() / max(cw_e[i].sum(), 1) for i in eboots]
            diffs.append(f"  {b:>4.0%} {a_:>9} - {b_:<10} all-wrong "
                         f"{recall(ye, mask[a_]) - recall(ye, mask[b_]):+.3f} {ci(d_all)}   "
                         f"confident-wrong "
                         f"{recall(ye, mask[a_], cw_e) - recall(ye, mask[b_], cw_e):+.3f} {ci(d_cw)}")
    rep.log(f"  {'':>15} | share of CONFIDENT-WRONG caught:")
    for r in rows_cw:
        rep.log(r)
    rep.log("")
    rep.log("  paired recall differences, 95% CI (document-clustered bootstrap):")
    for d in diffs:
        rep.log(d)
    rep.save()


if __name__ == "__main__":
    for c in (sys.argv[1:] or CONDITIONS):
        run(c)
