"""Which FinQA errors does the probe detect? (camera-ready analysis)

Mechanical error typing of every wrong FinQA answer, using the annotations of the
original FinQA release (gold reasoning program and table; row N of flare-finqa is
row N of the original train.json, checked on the question text). No LLM labelling.

Mutually exclusive types, assigned in this order:
  abstention   the model declines or gives no ANSWER line (common.is_abstention)
  sign         |prediction| matches |gold| under the grader's scale set, sign differs
  scale        prediction/gold is a power of ten the grader does not forgive (2% tol)
  selection    at least one operand of the gold program never appears in the model's
               written reasoning: the model worked from a different reporting item or
               period. Split by where the missing operand sits in the table:
                 selection_same_row   another number from the same table row appears
                                      in the reasoning (same line item, other column)
                 selection_other      otherwise
  computation  every gold operand appears in the reasoning but the final value is
               wrong (formula or arithmetic error)

For each type: share of all wrong answers and of the confident-wrong (8/8) cell, and
AUROC for separating confident-wrong answers of that type from confident-correct
answers, for the probe, P(True), the supervised output combination and the
pre-generation probe.

Usage: python 21_error_types.py [qwen|llama|gemma ...]
Writes results/21_error_types_{model}_full_finqa.md
"""

import json
import re
import sys

import numpy as np
import pandas as pd

from analysis_utils import (EXTRA, MODELS, auroc, finqa_original, load_generations,
                            load_scores)
from common import DATA, Reporter, is_abstention, parse_number

NUM = re.compile(r"\d[\d,]*\.?\d*")
TYPES = ["abstention", "sign", "scale", "selection_same_row", "selection_other", "computation"]


def numbers_in(text):
    out = set()
    for m in NUM.findall(text):
        try:
            out.add(abs(float(m.replace(",", "").rstrip("."))))
        except ValueError:
            pass
    return out


def has(nums, v, tol=0.005):
    v = abs(v)
    return any(abs(n - v) <= tol * max(v, 1e-9) for n in nums)


def close(a, b, tol=0.02):
    if b == 0:
        return abs(a) < 1e-6
    return abs(a - b) / abs(b) <= tol


def gold_operands(o):
    """Numeric operands the gold program reads from the filing, with table rows."""
    table = o["table"]
    ops = []
    for arg in re.findall(r"\(([^()]*)\)", o["qa"]["program"]):
        for a in arg.split(","):
            a = a.strip()
            if not a or a.startswith("#") or a.startswith("const_") or a == "none":
                continue
            v, _ = parse_number(a)
            if v is not None and re.fullmatch(r"-?\$?\(?[\d,.]+\)?%?", a.replace(" ", "")):
                ops.append(abs(v))
            else:                                    # table_* op: operand is a row label
                for row in table:
                    if row and row[0].strip().lower() == a.lower():
                        ops += [abs(x) for x in (parse_number(c)[0] for c in row[1:])
                                if x is not None]
    return ops


def row_of(table, v):
    for row in table:
        vals = [abs(x) for x in (parse_number(c)[0] for c in row[1:]) if x is not None]
        if has(set(vals), v):
            return [x for x in vals if not has({v}, x)]
    return None


def classify(rec, o):
    if is_abstention(rec["output"]):
        return "abstention"
    p, _ = parse_number(str(rec["pred"]))
    g, _ = parse_number(str(rec["gold"]))
    if p is None or g is None:
        return "abstention"
    if g != 0 and p != 0:
        if any(close(-p * s, g) for s in (1.0, 100.0, 0.01, 1000.0, 0.001)):
            return "sign"
        k = np.log10(abs(p / g))
        if abs(k - round(k)) < np.log10(1.02) and round(k) != 0:
            return "scale"
    nums = numbers_in(rec["output"])
    missing = [v for v in gold_operands(o) if not has(nums, v)]
    if not missing:
        return "computation"
    for v in missing:
        others = row_of(o["table"], v)
        if others and any(has(nums, x) for x in others):
            return "selection_same_row"
    return "selection_other"


def run(model):
    cond = f"{model}_full_finqa"
    df = load_scores(cond).merge(pd.read_csv(EXTRA / f"{cond}.csv", comment="#"), on="id")
    recs = load_generations(cond)
    orig = finqa_original()
    y = df["correct"].to_numpy()
    conf = df["conf_greedy"].to_numpy()
    typ = np.array(["correct"] * len(y), dtype=object)
    for i, r in enumerate(recs):
        if y[i] == 0:
            o = orig[int(r["id"].replace("finqa", ""))]
            assert o["qa"]["question"].strip().lower()[:40] in r["query"].lower()
            typ[i] = classify(r, o)
    wrong, cw, cc = y == 0, (y == 0) & (conf >= 1.0), (y == 1) & (conf >= 1.0)
    sig = {"probe": "probe", "p_true": "P(True)", "cheap_best": "cheap", "pregen": "pregen"}
    rep = Reporter(f"21_error_types_{cond}", meta={
        "n_wrong": int(wrong.sum()), "n_confident_wrong": int(cw.sum()),
        "negatives": f"confident-correct (n={int(cc.sum())})"})
    rep.log(f"{'type':<20}{'wrong':>7}{'share':>8}{'CW':>6}{'share':>8}{'conf.rate':>10} |"
            + "".join(f"{v:>9}" for v in sig.values()))
    for t in TYPES + ["selection (all)", "all wrong"]:
        m = (np.isin(typ, ["selection_same_row", "selection_other"]) if t == "selection (all)"
             else wrong if t == "all wrong" else typ == t)
        pos = m & cw
        line = (f"{t:<20}{int(m.sum()):>7}{m.sum() / wrong.sum():>8.1%}{int(pos.sum()):>6}"
                f"{pos.sum() / cw.sum():>8.1%}{pos.sum() / max(m.sum(), 1):>10.1%} |")
        if pos.sum() >= 20:
            sel = pos | cc
            line += "".join(f"{auroc(y[sel], df[k].to_numpy()[sel]):>9.3f}" for k in sig)
        else:
            line += "   (fewer than 20 confident-wrong)"
        rep.log(line)
    rep.save()


if __name__ == "__main__":
    for m in (sys.argv[1:] or MODELS):
        run(m)
