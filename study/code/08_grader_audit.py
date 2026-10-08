"""Audit the programmatic grader with an LLM judge (gpt-5.4-mini).

Stratified sample: 60 graded-correct + 60 graded-incorrect records from the
800-question Qwen3-8B FinQA pilot (study/data/pilot/). The judge verdicts behind the
reported agreement rates are kept in study/data/pilot/grader_audit.jsonl and summarized
in study/results/08_grader_audit_pilot.md.
The judge sees the question, gold answer, and the model's final answer (with
the tail of its reasoning) and rules correct/incorrect under FinQA numeric
conventions. Reports agreement per stratum -> estimated label-noise rates.
"""

import json
import pathlib
import re

import numpy as np
from openai import OpenAI

from common import PILOT
N_PER_STRATUM = 60
JUDGE = "gpt-5.4-mini"

PROMPT = """You are auditing an automatic grader for financial QA.

Question: {question}
Gold answer: {gold}
Model's final answer: {pred}
Tail of model's reasoning: {tail}

Under FinQA conventions, percent-scale differences (0.53 vs 53.2%), sign phrasing \
(a "decrease of 5" vs -5), rounding to ~1% relative tolerance, and unit scale \
(millions vs raw) are all considered EQUIVALENT to the gold answer.

Is the model's final answer correct? Reply with JSON only: {{"correct": true/false, "reason": "<15 words"}}"""


def main():
    rng = np.random.default_rng(0)
    recs = [json.loads(l) for l in (PILOT / "generations_qwen_finqa_pilot.jsonl").open()]
    for i, r in enumerate(recs):
        r["_idx"] = i

    pos = [r for r in recs if r["correct"]]
    neg = [r for r in recs if not r["correct"]]
    sample = list(rng.choice(pos, N_PER_STRATUM, replace=False)) + list(
        rng.choice(neg, N_PER_STRATUM, replace=False)
    )

    client = OpenAI()
    results = []
    for k, r in enumerate(sample):
        m = re.search(r"Question:\s*(.+?)\nAnswer:", r["prompt"], re.DOTALL)
        question = m.group(1).strip() if m else "(unavailable)"
        msg = PROMPT.format(
            question=question, gold=r["gold"], pred=r["pred"], tail=r["output"][-600:]
        )
        resp = client.chat.completions.create(
            model=JUDGE, messages=[{"role": "user", "content": msg}]
        )
        txt = resp.choices[0].message.content
        try:
            verdict = json.loads(re.search(r"\{.*\}", txt, re.DOTALL).group(0))["correct"]
        except Exception:
            verdict = None
        results.append({"idx": r["_idx"], "grader": r["correct"], "judge": verdict,
                        "gold": r["gold"], "pred": r["pred"]})
        if (k + 1) % 20 == 0:
            print(f"{k + 1}/{len(sample)}", flush=True)

    with (PILOT / "grader_audit.jsonl").open("w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    ok = [r for r in results if r["judge"] is not None]
    for stratum, val in (("graded-correct", True), ("graded-incorrect", False)):
        s = [r for r in ok if r["grader"] == val]
        agree = sum(r["judge"] == r["grader"] for r in s)
        print(f"{stratum}: judge agrees {agree}/{len(s)} ({agree / len(s):.1%})")
        for r in s:
            if r["judge"] != r["grader"]:
                print(f"   disagreement idx={r['idx']}: gold={r['gold']} pred={r['pred']}")


if __name__ == "__main__":
    main()
