"""Self-consistency confidence.

k=8 sampled answers per question (temp 0.7, top_p 0.8, top_k 20 — Qwen3
non-thinking recommended params). Confidence = fraction of samples whose parsed
answer matches the greedy answer (grade()-equivalence, symmetric conventions).
Also reports modal agreement (consistency of samples with each other).

Output: study/data/selfcons_{name}.jsonl (+ selfcons_{name}_meta.json when subsampling)
"""

import json
import os
import pathlib
import time
from collections import Counter

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from common import MODEL_NAME, ensure_pad, extract_final_answer, grade

GEN_FILE = os.environ.get("GEN_FILE", "generations_qwen_full.jsonl")
OUT_NAME = os.environ.get("OUT_NAME", "qwen_full_finqa")
K = 8
MAX_NEW_TOKENS = 400
# token budget per batch: (prompt_len + MAX_NEW) * n_questions * K <= BUDGET
SEQ_TOKEN_BUDGET = int(os.environ.get("SEQ_TOKEN_BUDGET", 70_000))
from common import DATA as OUT


def main():
    tok = ensure_pad(AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="left"))
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, dtype=torch.bfloat16, device_map="cuda"
    )
    model.eval()

    recs = [json.loads(l) for l in (OUT / GEN_FILE).open()]
    out_path = OUT / f"selfcons_{OUT_NAME}.jsonl"

    # stratified subsample (scale-up mode): confidence is measured on ALL wrong
    # answers but only SC_CORRECT_N sampled correct ones. Within-stratum AUROC is
    # unbiased under one-class random subsampling; population (quadrant) estimates
    # must reweight the correct class by 1/correct_sampling_rate (rate saved to meta).
    sc_correct_n = int(os.environ.get("SC_CORRECT_N", 0))  # 0 = measure everything
    if sc_correct_n:
        import numpy as np
        rng = np.random.default_rng(int(os.environ.get("SC_SEED", 0)))
        wrong = [r for r in recs if not r["correct"]]
        right = [r for r in recs if r["correct"]]
        keep = min(sc_correct_n, len(right))
        idx = set(rng.choice(len(right), keep, replace=False).tolist())
        meta = {
            "n_wrong_total": len(wrong),
            "n_correct_total": len(right),
            "n_correct_sampled": keep,
            "correct_sampling_rate": keep / max(len(right), 1),
        }
        (OUT / f"selfcons_{OUT_NAME}_meta.json").write_text(json.dumps(meta))
        recs = wrong + [r for i, r in enumerate(right) if i in idx]
        print(f"stratified subsample: all {len(wrong)} wrong + {keep}/{len(right)} correct",
              flush=True)

    # resume: skip ids already done
    done_ids = set()
    if out_path.exists():
        done_ids = {json.loads(l)["id"] for l in out_path.open()}
        print(f"resuming: {len(done_ids)} already done", flush=True)
    recs = [r for r in recs if r["id"] not in done_ids]

    # sort longest-first (fail fast on OOM, minimal padding waste), batch by budget
    for r in recs:
        r["_ntok"] = len(tok(r["prompt"]).input_ids)
    recs.sort(key=lambda r: -r["_ntok"])
    batches, cur = [], []
    for r in recs:
        trial = cur + [r]
        if cur and (trial[0]["_ntok"] + MAX_NEW_TOKENS) * len(trial) * K > SEQ_TOKEN_BUDGET:
            batches.append(cur)
            cur = [r]
        else:
            cur = trial
    if cur:
        batches.append(cur)

    t0, n_done = time.time(), 0
    with out_path.open("a") as f:
        for batch in batches:
            enc = tok([r["prompt"] for r in batch], return_tensors="pt",
                      padding=True).to("cuda")
            with torch.no_grad():
                gen = model.generate(
                    **enc,
                    max_new_tokens=MAX_NEW_TOKENS,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.8,
                    top_k=20,
                    num_return_sequences=K,
                    pad_token_id=tok.pad_token_id or tok.eos_token_id,
                )
            plen = enc.input_ids.shape[1]
            for j, r in enumerate(batch):
                preds = []
                for s in range(K):
                    txt = tok.decode(gen[j * K + s][plen:], skip_special_tokens=True)
                    preds.append(extract_final_answer(txt))
                agree_greedy = sum(grade(p, r["pred"]) for p in preds) / K
                # modal agreement: largest cluster of mutually-equivalent answers
                clusters = []
                for p in preds:
                    for c in clusters:
                        if grade(p, c[0]):
                            c.append(p)
                            break
                    else:
                        clusters.append([p])
                modal = max(len(c) for c in clusters) / K
                f.write(json.dumps({
                    "id": r["id"], "correct": r["correct"],
                    "conf_greedy": agree_greedy, "conf_modal": modal,
                    "samples": preds,
                }) + "\n")
            f.flush()  # a killed run must not lose buffered records (resume reads this file)
            n_done += len(batch)
            rate = n_done / (time.time() - t0)
            print(f"{n_done}/{len(recs)} (batch={len(batch)}, {rate:.2f} q/s, "
                  f"eta {(len(recs) - n_done) / rate / 60:.0f} min)", flush=True)

    import numpy as np
    from sklearn.metrics import roc_auc_score
    rows = [json.loads(l) for l in out_path.open()]
    y = np.array([r["correct"] for r in rows], dtype=int)
    for k in ("conf_greedy", "conf_modal"):
        x = np.array([r[k] for r in rows])
        print(f"{OUT_NAME} {k:<12} AUROC {roc_auc_score(y, x):.3f}  "
              f"mean={x.mean():.3f}")


if __name__ == "__main__":
    main()
