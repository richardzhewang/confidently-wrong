"""Paper figures, generated from pipeline outputs (never hardcoded numbers).

Fig 1: precision & recall vs review budget, confident answers, Qwen3-8B on FinQA
       (population-reweighted), probe vs P(True).      <- scores CSV + meta
Fig 2: depth profiles, answer-conditioned vs pre-generation probes, three
       families, with random-init placebo reference.   <- results/03_layer_sweep_*.md

Okabe-Ito palette (CVD-validated); direct labels; one axis per panel.
"""

import json
import pathlib
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

STUDY = pathlib.Path(__file__).parent.parent / "study"
SCORES = STUDY / "scores"
RESULTS = STUDY / "results"
META = STUDY / "data"
FIGS = pathlib.Path(__file__).parent

BLUE, VERM, GREEN, GRAY = "#0072B2", "#D55E00", "#009E73", "#7f7f7f"

plt.rcParams.update({
    "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#dddddd", "grid.linewidth": 0.5,
    "lines.linewidth": 1.4, "pdf.fonttype": 42,
})


def fig1_operating_points():
    df = pd.read_csv(SCORES / "qwen_full_finqa.csv", comment="#")
    meta = json.loads((META / "selfcons_qwen_full_finqa_meta.json").read_text())
    w_corr = 1.0 / meta["correct_sampling_rate"]
    m = (df["conf_greedy"] >= 1.0) & df["conf_greedy"].notna()
    d = df[m]
    y = d["correct"].to_numpy()
    w = np.where(y == 1, w_corr, 1.0)
    wrong = y == 0
    budgets = np.linspace(0.02, 0.5, 25)

    fig, axes = plt.subplots(1, 2, figsize=(6.8, 1.85))
    for sig, color, label in [("probe", BLUE, "probe"), ("p_true", VERM, "P(True)")]:
        order = np.argsort(d[sig].to_numpy())  # most suspicious first
        cw = np.cumsum(w[order])
        cum_tp = np.cumsum(w[order] * wrong[order])
        tot_w, wrong_w = w.sum(), w[wrong].sum()
        prec, rec = [], []
        for b in budgets:
            k = int(np.searchsorted(cw, b * tot_w)) + 1
            prec.append(cum_tp[k - 1] / cw[k - 1])
            rec.append(cum_tp[k - 1] / wrong_w)
        axes[0].plot(budgets * 100, prec, color=color)
        axes[1].plot(budgets * 100, rec, color=color)
        axes[0].annotate(label, (budgets[-1] * 100, prec[-1]), xytext=(3, 0),
                         textcoords="offset points", color=color, va="center")
    prev = w[wrong].sum() / w.sum()
    axes[0].axhline(prev, color=GRAY, ls=":", lw=1)
    axes[0].annotate("prevalence", (2, prev), xytext=(2, 3),
                     textcoords="offset points", color=GRAY)
    axes[1].plot([0, 50], [0, 0.5], color=GRAY, ls=":", lw=1)
    axes[1].annotate("random", (38, 0.36), color=GRAY)
    axes[0].set(xlabel="review budget (% of confident answers)", ylabel="precision",
                ylim=(0, 1))
    axes[1].set(xlabel="review budget (% of confident answers)", ylabel="recall",
                ylim=(0, 1))
    fig.tight_layout()
    fig.savefig(FIGS / "fig1_operating_points.pdf", bbox_inches="tight")
    print("fig1 done")


def fig2_depth_profiles():
    """AUROC vs relative depth: answer-conditioned (ans_mean) and pre-generation
    (prompt_last) probes, three families, FinQA definitive scale. Placebo line =
    random-init-model probe (05_random_control.py, Qwen3-8B pilot, layer 24 = 0.625)."""
    files = {"Qwen3-8B": "03_layer_sweep_qwen_full_finqa.md",
             "Llama-3.1-8B": "03_layer_sweep_llama_full_finqa.md",
             "Gemma-2-9B": "03_layer_sweep_gemma_full_finqa.md"}
    colors = {"Qwen3-8B": BLUE, "Llama-3.1-8B": VERM, "Gemma-2-9B": GREEN}
    PLACEBO = 0.625
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.2), sharey=True)
    for name, f in files.items():
        txt = (RESULTS / f).read_text()
        rows = re.findall(r"L(\d+)_(ans_mean|prompt_last)\s+(0\.\d+)", txt)
        layers = sorted({int(l) for l, _, _ in rows})
        n_layers = max(layers)
        for ax, pool in zip(axes, ("ans_mean", "prompt_last")):
            d = {int(l): float(a) for l, p, a in rows if p == pool}
            xs = [l / n_layers for l in layers]
            ys = [d[l] for l in layers]
            ax.plot(xs, ys, color=colors[name], marker="o", ms=2.5,
                    label=name if pool == "ans_mean" else None)
    for ax, title in zip(axes, ("answer-conditioned (mean over answer tokens)",
                                "pre-generation (last prompt token)")):
        ax.axhline(PLACEBO, color=GRAY, ls="--", lw=1)
        ax.axvline(2 / 3, color=GRAY, ls=":", lw=0.8)
        ax.set(xlabel="relative layer depth", title=title, ylim=(0.48, 0.82),
               xticks=[0, 1 / 3, 2 / 3, 1])
        ax.set_xticklabels(["0", "1/3", "2/3", "1"])
    axes[0].set_ylabel("AUROC")
    axes[0].legend(loc="lower right", frameon=False, handlelength=1.4)
    axes[0].annotate("random-init placebo", (0.02, PLACEBO), xytext=(2, -9),
                     textcoords="offset points", color=GRAY, fontsize=7)
    fig.tight_layout()
    fig.savefig(FIGS / "fig2_depth_profiles.pdf", bbox_inches="tight")
    print("fig2 done")


if __name__ == "__main__":
    fig1_operating_points()
    fig2_depth_profiles()
