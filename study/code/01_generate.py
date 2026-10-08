"""Generate greedy answers with MODEL_NAME and grade them against the gold answers.

Env: MODEL_NAME, DATASET, SPLIT, N_EXAMPLES, OUT_FILE, STRICT_NUMERIC, GEN_BATCH
(run_scaleup.sh sets these for every model x dataset).
Output: study/data/{OUT_FILE} with one record per question:
  {id, prompt, query, gold, output, pred, correct}
"""

import json
import pathlib
import time

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

from common import (
    MODEL_NAME,
    SYSTEM_PROMPT,
    build_messages,
    ensure_pad,
    extract_final_answer,
    grade,
    is_pure_number,
    parse_number,
)

import os

N_EXAMPLES = int(os.environ.get("N_EXAMPLES", 6200))
GEN_BATCH = int(os.environ.get("GEN_BATCH", 16))
DATASET = os.environ.get("DATASET", "ChanceFocus/flare-finqa")
SPLIT = os.environ.get("SPLIT", "train")
OUT_FILE = os.environ.get("OUT_FILE", "generations_qwen_full.jsonl")
STRICT_NUMERIC = os.environ.get("STRICT_NUMERIC", "0") == "1"
MAX_CTX_TOKENS = 2800
MAX_NEW_TOKENS = 400
BATCH_SIZE = GEN_BATCH
from common import DATA as OUT
OUT.mkdir(exist_ok=True)


def main():
    tok = ensure_pad(AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="left"))
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, dtype=torch.bfloat16, device_map="cuda"
    )
    model.eval()

    ds = load_dataset(DATASET, split=SPLIT)

    # keep only numeric-gold questions with manageable context length
    records = []
    for ex in ds:
        gold_val, _ = parse_number(ex["answer"])
        if gold_val is None:
            continue
        if STRICT_NUMERIC and not is_pure_number(ex["answer"]):
            continue
        records.append(ex)
        if len(records) >= N_EXAMPLES * 2:  # headroom for length filtering
            break

    prompts, kept = [], []
    for ex in records:
        msgs = build_messages(SYSTEM_PROMPT, ex["query"])
        text = tok.apply_chat_template(
            msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False
        )
        n_tok = len(tok(text).input_ids)
        if n_tok > MAX_CTX_TOKENS:
            continue
        prompts.append(text)
        kept.append(ex)
        if len(kept) >= N_EXAMPLES:
            break

    print(f"generating for {len(kept)} questions from {DATASET}:{SPLIT}", flush=True)
    out_path = OUT / OUT_FILE
    t0 = time.time()
    with out_path.open("w") as f:
        for i in range(0, len(kept), BATCH_SIZE):
            bp = prompts[i : i + BATCH_SIZE]
            be = kept[i : i + BATCH_SIZE]
            enc = tok(bp, return_tensors="pt", padding=True).to("cuda")
            with torch.no_grad():
                gen = model.generate(
                    **enc,
                    max_new_tokens=MAX_NEW_TOKENS,
                    do_sample=False,
                    temperature=None,
                    top_p=None,
                    top_k=None,
                    pad_token_id=tok.pad_token_id or tok.eos_token_id,
                )
            for j, ex in enumerate(be):
                out_ids = gen[j][enc.input_ids.shape[1] :]
                out_text = tok.decode(out_ids, skip_special_tokens=True)
                pred = extract_final_answer(out_text)
                rec = {
                    "id": ex["id"],
                    "prompt": bp[j],
                    "query": ex["query"],
                    "gold": ex["answer"],
                    "output": out_text,
                    "pred": pred,
                    "correct": grade(pred, ex["answer"]),
                }
                f.write(json.dumps(rec) + "\n")
            done = min(i + BATCH_SIZE, len(kept))
            rate = done / (time.time() - t0)
            print(
                f"{done}/{len(kept)}  ({rate:.1f} q/s, eta {(len(kept)-done)/rate/60:.1f} min)",
                flush=True,
            )

    # summary
    recs = [json.loads(l) for l in out_path.open()]
    acc = sum(r["correct"] for r in recs) / len(recs)
    print(f"\naccuracy: {acc:.3f}  ({sum(r['correct'] for r in recs)}/{len(recs)})")


if __name__ == "__main__":
    main()
