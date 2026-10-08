"""Confidence x correctness quadrant table across all conditions (paper Table 1).

Scans study/data/selfcons_*.jsonl, computes confidence x correctness cell counts at the
8/8 threshold (and ≥6/8 as sensitivity), and writes a markdown table to
study/results/quadrants.md. If a selfcons_*_meta.json exists (stratified subsample:
all wrong + sampled correct), population SHARES reweight the correct class by
1/sampling_rate; raw counts are always shown as-is.
"""

import json
import pathlib

from common import DATA as OUT, RESULTS_DIR
THRESHOLDS = [1.0, 0.75]
PAPER_ONLY = True  # quadrants.md lists definitive-scale (_full) conditions only


def condition(sc_path):
    name = sc_path.stem.replace("selfcons_", "")
    rows = [json.loads(l) for l in sc_path.open()]
    if not rows:
        return None
    meta_path = OUT / f"selfcons_{name}_meta.json"
    w_correct = 1.0
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        w_correct = 1.0 / meta["correct_sampling_rate"]
    out = {"name": name, "n": len(rows), "reweighted": w_correct != 1.0}
    for thr in THRESHOLDS:
        cells = {"cc": 0, "cw": 0, "uc": 0, "uw": 0}
        wcells = {k: 0.0 for k in cells}
        for r in rows:
            key = ("c" if r["conf_greedy"] >= thr else "u") + ("c" if r["correct"] else "w")
            cells[key] += 1
            wcells[key] += w_correct if r["correct"] else 1.0
        tot = sum(wcells.values())
        out[thr] = {k: (cells[k], wcells[k] / tot) for k in cells}
    return out


def main():
    conds = sorted(
        p for p in OUT.glob("selfcons_*.jsonl") if not p.stem.endswith("_meta")
    )
    if PAPER_ONLY:
        conds = [p for p in conds if "_full" in p.stem.replace("selfcons_", "")]
    lines = [
        "# Confidence × correctness quadrants",
        "",
        "Confidence = self-consistency (k=8, agreement with greedy answer); "
        "'confident' = 8/8 unless noted. Cells: count (population share"
        " — reweighted for subsampled correct class where marked ®).",
        "",
        "| condition | n | confident-correct | confident-WRONG | unsure-correct | unsure-wrong |",
        "|---|---|---|---|---|---|",
    ]
    print(f"{'condition':<24}{'n':>6} | conf-correct  conf-WRONG  unsure-correct  unsure-wrong")
    for p in conds:
        c = condition(p)
        if c is None:
            continue
        q = c[1.0]
        mark = " ®" if c["reweighted"] else ""
        cells_txt = {k: f"{q[k][0]} ({q[k][1]:.0%})" for k in ("cc", "cw", "uc", "uw")}
        lines.append(
            f"| {c['name']}{mark} | {c['n']} | {cells_txt['cc']} | **{cells_txt['cw']}** "
            f"| {cells_txt['uc']} | {cells_txt['uw']} |"
        )
        print(f"{c['name'] + mark:<24}{c['n']:>6} | {cells_txt['cc']:>12}  "
              f"{cells_txt['cw']:>10}  {cells_txt['uc']:>14}  {cells_txt['uw']:>12}")

    lines += ["", "Sensitivity (confident = ≥6/8):", ""]
    lines += ["| condition | confident-WRONG share (8/8) | (≥6/8) |", "|---|---|---|"]
    for p in conds:
        c = condition(p)
        if c is None:
            continue
        lines.append(f"| {c['name']} | {c[1.0]['cw'][1]:.1%} | {c[0.75]['cw'][1]:.1%} |")

    (RESULTS_DIR / "quadrants.md").write_text("\n".join(lines) + "\n")
    print(f"\nwrote {RESULTS_DIR / 'quadrants.md'}")


if __name__ == "__main__":
    main()
