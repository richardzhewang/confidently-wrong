"""Output-level confidence signals.

For every cached generation:
  - gen_mean_lp   : mean logprob of all generated tokens
  - ans_mean_lp   : mean logprob of the final-answer span (after last 'ANSWER:')
  - ans_min_lp    : min logprob in that span
  - p_true        : Kadavath-style self-assessment — model shown its own answer,
                    asked True/False, relative prob of True at the first position

Output: study/data/baselines_{name}.jsonl
"""

import json
import os
import pathlib

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from common import MODEL_NAME, build_messages, ensure_pad

GEN_FILE = os.environ.get("GEN_FILE", "generations_qwen_full.jsonl")
OUT_NAME = os.environ.get("OUT_NAME", "qwen_full_finqa")
BATCH_SIZE = 2
from common import DATA as OUT

PTRUE_SYSTEM = "You are grading a financial QA answer."
PTRUE_USER = """{query}

Proposed solution:
{output}

Is the proposed final answer correct? Reply with exactly one word, True or False."""


def token_group_ids(tok, words):
    ids = set()
    for w in words:
        for v in (w, " " + w):
            t = tok(v, add_special_tokens=False).input_ids
            if len(t) == 1:
                ids.add(t[0])
    return sorted(ids)


def main():
    # token-position indexing assumes right padding (Gemma defaults LEFT — force it)
    tok = ensure_pad(AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="right"))
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, dtype=torch.bfloat16, device_map="cuda"
    )
    model.eval()

    true_ids = token_group_ids(tok, ["True", "TRUE", "true"])
    false_ids = token_group_ids(tok, ["False", "FALSE", "false"])

    recs = [json.loads(l) for l in (OUT / GEN_FILE).open()]
    results = []
    for i in range(0, len(recs), BATCH_SIZE):
        batch = recs[i : i + BATCH_SIZE]

        # --- generated-token logprobs -------------------------------------
        full = [r["prompt"] + r["output"] for r in batch]
        enc = tok(full, return_tensors="pt", padding=True,
                  return_offsets_mapping=True).to("cuda")
        with torch.no_grad():
            logits = model(input_ids=enc.input_ids,
                           attention_mask=enc.attention_mask).logits
        # bf16 log-softmax: fp32 would OOM on 256k-vocab models (Gemma); AUROC is
        # rank-based so bf16 precision suffices
        lp = torch.log_softmax(logits, dim=-1)
        for j, r in enumerate(batch):
            sl = int(enc.attention_mask[j].sum())
            pl = len(tok(r["prompt"]).input_ids)
            # token t is predicted at position t-1
            tok_lp = lp[j, pl - 1 : sl - 1].gather(
                1, enc.input_ids[j, pl:sl].unsqueeze(1)
            ).squeeze(1).float()
            # final-answer span via char offsets of last 'ANSWER:' in the output
            if "ANSWER:" in r["output"]:
                char0 = len(r["prompt"]) + r["output"].rfind("ANSWER:")
                offs = enc.offset_mapping[j, pl:sl, 0]
                span = offs >= char0
                span_lp = tok_lp[span] if bool(span.any()) else tok_lp
            else:
                span_lp = tok_lp  # no marker: use the whole generated span
            results.append({
                "id": r["id"],
                "correct": r["correct"],
                "gen_mean_lp": float(tok_lp.mean()),
                "ans_mean_lp": float(span_lp.mean()),
                "ans_min_lp": float(span_lp.min()),
            })
        del logits, lp

        # --- P(True) -------------------------------------------------------
        ptrue_prompts = []
        for r in batch:
            q = r.get("query") or r["prompt"].split("<|im_start|>user")[1].split("<|im_end|>")[0].strip()
            msgs = build_messages(PTRUE_SYSTEM, PTRUE_USER.format(query=q, output=r["output"]))
            ptrue_prompts.append(tok.apply_chat_template(
                msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False
            ))
        enc2 = tok(ptrue_prompts, return_tensors="pt", padding=True).to("cuda")
        with torch.no_grad():
            logits2 = model(**enc2).logits
        for j in range(len(batch)):
            sl = int(enc2.attention_mask[j].sum())
            last = logits2[j, sl - 1].float()
            lt = torch.logsumexp(last[true_ids], 0)
            lf = torch.logsumexp(last[false_ids], 0)
            results[i + j]["p_true"] = float(torch.sigmoid(lt - lf))
        del logits2

        if (i // BATCH_SIZE) % 50 == 0:
            print(f"{i + len(batch)}/{len(recs)}", flush=True)

    with (OUT / f"baselines_{OUT_NAME}.jsonl").open("w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    y = np.array([r["correct"] for r in results], dtype=int)
    from sklearn.metrics import roc_auc_score
    for k in ("gen_mean_lp", "ans_mean_lp", "ans_min_lp", "p_true"):
        x = np.array([r[k] for r in results])
        print(f"{OUT_NAME} {k:<12} AUROC {roc_auc_score(y, x):.3f}")


if __name__ == "__main__":
    main()
