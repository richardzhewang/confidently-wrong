#!/bin/bash
# Two-stage analysis pipeline. All outputs -> ../results/.
#
#   bash run_analyses.sh          # both stages
#   bash run_analyses.sh report   # stage 2 only (CPU, reads ../scores and ../data)
#
# STAGE 1 (fit): needs ../cache/activations_*.npz (from 02_extract.py). Rerun whenever
#   generations, activations, labels, self-consistency or baseline files change.
# STAGE 2 (report): tables computed from the released score files only.
cd "$(dirname "$0")"
STAGE="${1:-all}"
TAGS=(qwen_full llama_full gemma_full)

if [ "$STAGE" != "report" ]; then
  for T in "${TAGS[@]}"; do
    [ -f "../cache/activations_${T}.npz" ] || { echo "-- skip $T (no activations in ../cache)"; continue; }
    echo "== FIT $T: probe scores =="
    MODEL_TAG="$T" uv run python fit_scores.py
    echo "== FIT $T: layer x pooling sweep (FinQA) =="
    ACT_FILE="activations_${T}.npz" GEN_FILE="generations_${T}.jsonl" TAG="${T}_finqa" \
      uv run python 03_probe.py
    echo "== FIT $T: cross-dataset transfer =="
    ACT_A="activations_${T}.npz" GEN_A="generations_${T}.jsonl" \
      ACT_B="activations_${T}_tatqa.npz" GEN_B="generations_${T}_tatqa.jsonl" TAG="$T" \
      uv run python 07_ood_probe.py
  done
  echo "== FIT: supervised comparison signals, scale audit, split leakage =="
  uv run python 19_supervised_baselines.py
  uv run python 18_scale_audit.py
  uv run python 22_split_leakage.py
fi

echo "== REPORT =="
uv run python 12_two_by_two.py
uv run python 14_quadrant_table.py
uv run python 17_abstention_robustness.py
uv run python 20_routing_and_uncertainty.py
uv run python 21_error_types.py
echo "== DONE -> ../results/ =="
