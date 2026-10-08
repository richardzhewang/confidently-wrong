"""Random-initialization placebo.

Extract the same features from a RANDOMLY INITIALIZED Qwen3-8B (same
architecture, untrained weights) and probe them. The trained model's probe
AUROC only counts insofar as it exceeds this placebo — a random transformer
still exposes surface statistics of the text that a 4096-dim probe can use.

Provenance of the reported number (0.625 at layer 24): this script was run on the
800-question Qwen3-8B FinQA pilot (study/data/pilot/generations_qwen_finqa_pilot.jsonl)
with question-level stratified 5-fold CV. The console record is kept in
study/results/05_random_control_pilot.md.
"""

import json
import pathlib

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

from common import MODEL_NAME, PILOT

LAYERS = [18, 24]
BATCH_SIZE = 4
from common import DATA as OUT


def main():
    torch.manual_seed(0)
    tok = AutoTokenizer.from_pretrained(MODEL_NAME)
    cfg = AutoConfig.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_config(cfg, dtype=torch.bfloat16).to("cuda")
    model.eval()

    recs = [json.loads(l) for l in (PILOT / "generations_qwen_finqa_pilot.jsonl").open()]
    feats = {l: [] for l in LAYERS}
    y = []
    for i in range(0, len(recs), BATCH_SIZE):
        batch = recs[i : i + BATCH_SIZE]
        full_texts = [r["prompt"] + r["output"] for r in batch]
        prompt_lens = [len(tok(r["prompt"]).input_ids) for r in batch]
        enc = tok(full_texts, return_tensors="pt", padding=True).to("cuda")
        with torch.no_grad():
            out = model(**enc, output_hidden_states=True)
        seq_lens = enc.attention_mask.sum(dim=1)
        for l in LAYERS:
            h = out.hidden_states[l].float()
            for j in range(len(batch)):
                pl, sl = min(prompt_lens[j], int(seq_lens[j])), int(seq_lens[j])
                span = h[j, pl:sl] if sl > pl else h[j, pl - 1 : pl]
                feats[l].append(span.mean(dim=0).cpu().numpy())
        y.extend(int(r["correct"]) for r in batch)
        del out
        if (i // BATCH_SIZE) % 40 == 0:
            print(f"{i}/{len(recs)}", flush=True)

    y = np.array(y)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    for l in LAYERS:
        X = np.stack(feats[l]).astype(np.float32)
        # guard against NaN/inf from an untrained network
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
        aucs = []
        for tr, te in skf.split(X, y):
            clf = make_pipeline(
                StandardScaler(),
                LogisticRegression(C=0.1, max_iter=2000, class_weight="balanced"),
            )
            clf.fit(X[tr], y[tr])
            aucs.append(roc_auc_score(y[te], clf.predict_proba(X[te])[:, 1]))
        print(f"random-model L{l}_ans_mean AUROC: {np.mean(aucs):.3f} ± {np.std(aucs):.3f}")


if __name__ == "__main__":
    main()
