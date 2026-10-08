"""Extract residual-stream activations for each (prompt, generated answer) pair.

For every record in the generations file, run one forward pass over
prompt + generated answer and capture hidden states at selected layers with
three poolings:
  - prompt_last : last prompt token (pre-generation — could the DSS route the
                  question *before* paying for the answer?)
  - ans_last    : last token of the generated answer
  - ans_mean    : mean over generated-answer tokens

Output: study/cache/{ACT_FILE} (pooled features) and study/cache/{TOK_FILE} (per-token)
"""

import json
import os
import pathlib

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from common import MODEL_NAME, ensure_pad

# layers at relative depths {0, 1/6 .. 1}; 0 = embeddings (non-contextual baseline).
# TOKEN_LAYER (per-token capture) = 2/3 depth, matching Qwen3-8B's L24/36.
DEPTH_FRACS = [0, 1 / 6, 2 / 6, 3 / 6, 4 / 6, 5 / 6, 1.0]
BATCH_SIZE = int(os.environ.get("EXTRACT_BATCH", 4))
from common import CACHE, DATA as OUT
GEN_FILE = os.environ.get("GEN_FILE", "generations_qwen_full.jsonl")
ACT_FILE = os.environ.get("ACT_FILE", "activations_qwen_full.npz")
TOK_FILE = os.environ.get("TOK_FILE", "tokens_qwen_full.npz")


def main():
    # position indexing below assumes right padding; some tokenizers (Gemma)
    # default to LEFT and silently shift every slice into padding — force it.
    tok = ensure_pad(AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="right"))
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, dtype=torch.bfloat16, device_map="cuda"
    )
    model.eval()
    n_layers = model.config.num_hidden_layers
    LAYERS = sorted({round(f * n_layers) for f in DEPTH_FRACS})
    TOKEN_LAYER = round(2 / 3 * n_layers)
    print(f"{MODEL_NAME}: {n_layers} layers -> capture {LAYERS}, tokens at L{TOKEN_LAYER}")

    recs = [json.loads(l) for l in (OUT / GEN_FILE).open()]
    print(f"{len(recs)} records from {GEN_FILE}", flush=True)

    feats = {f"L{l}_{p}": [] for l in LAYERS for p in ("prompt_last", "ans_last", "ans_mean")}
    labels, ids = [], []
    tok_chunks, tok_lens = [], []  # ragged per-token answer activations at TOKEN_LAYER

    for i in range(0, len(recs), BATCH_SIZE):
        batch = recs[i : i + BATCH_SIZE]
        full_texts = [r["prompt"] + r["output"] for r in batch]
        prompt_lens = [len(tok(r["prompt"]).input_ids) for r in batch]
        enc = tok(full_texts, return_tensors="pt", padding=True).to("cuda")
        with torch.no_grad():
            # base transformer only: hidden states without the LM head — skips the
            # [B, T, vocab] logits tensor (~6 GB for 256k-vocab models like Gemma)
            out = model.model(**enc, output_hidden_states=True)
        hs = out.hidden_states  # tuple(n_layers+1) of [B, T, D]
        attn = enc.attention_mask
        seq_lens = attn.sum(dim=1)
        for l in LAYERS:
            h = hs[l].float()
            for j, r in enumerate(batch):
                pl, sl = prompt_lens[j], int(seq_lens[j])
                pl = min(pl, sl)
                feats[f"L{l}_prompt_last"].append(h[j, pl - 1].cpu().numpy())
                feats[f"L{l}_ans_last"].append(h[j, sl - 1].cpu().numpy())
                span = h[j, pl:sl] if sl > pl else h[j, pl - 1 : pl]
                feats[f"L{l}_ans_mean"].append(span.mean(dim=0).cpu().numpy())
                if l == TOKEN_LAYER:
                    tok_chunks.append(span.to(torch.float16).cpu().numpy())
                    tok_lens.append(span.shape[0])
        for r in batch:
            labels.append(int(r["correct"]))
            ids.append(r["id"])
        del out, hs
        if (i // BATCH_SIZE) % 20 == 0:
            print(f"{i + len(batch)}/{len(recs)}", flush=True)

    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        CACHE / ACT_FILE,
        labels=np.array(labels),
        ids=np.array(ids),
        **{k: np.stack(v).astype(np.float32) for k, v in feats.items()},
    )
    print("saved", CACHE / ACT_FILE)

    np.savez_compressed(
        CACHE / TOK_FILE,
        tokens=np.concatenate(tok_chunks, axis=0),
        lens=np.array(tok_lens),
        labels=np.array(labels),
    )
    print("saved", CACHE / TOK_FILE)


if __name__ == "__main__":
    main()
