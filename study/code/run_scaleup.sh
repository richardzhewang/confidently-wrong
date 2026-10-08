#!/bin/bash
# Full data generation on one GPU. FinQA (~6.1k numeric questions) + TAT-QA numerics
# (~1.1k) for all three models. Self-consistency uses the stratified subsample: ALL wrong
# answers + 1500 (FinQA) / 400 (TAT-QA) random correct answers.
# Total ETA: roughly 25-30 h. Resumable: rerun the script; self-consistency resumes
# from its output file, other steps redo their stage from scratch.
#
# Usage: bash run_scaleup.sh [qwen|llama|gemma]   (no arg = all three)
set -a; source ../../.env; set +a
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
cd "$(dirname "$0")"

run_model () {  # $1 model name, $2 tag, $3 gen_batch, $4 sc_budget
  export MODEL_NAME="$1"
  local TAG="$2"
  echo "=== $TAG: generate finqa (full) ==="
  GEN_BATCH="$3" N_EXAMPLES=6200 OUT_FILE="generations_${TAG}.jsonl" \
    uv run python 01_generate.py || { echo "$TAG FAILED gen finqa"; return 1; }
  echo "=== $TAG: generate tatqa (full numerics) ==="
  GEN_BATCH="$3" DATASET=ChanceFocus/flare-tatqa SPLIT=test N_EXAMPLES=1200 \
    STRICT_NUMERIC=1 OUT_FILE="generations_${TAG}_tatqa.jsonl" \
    uv run python 01_generate.py || { echo "$TAG FAILED gen tatqa"; return 1; }
  echo "=== $TAG: extract ==="
  GEN_FILE="generations_${TAG}.jsonl" ACT_FILE="activations_${TAG}.npz" \
    TOK_FILE="tokens_${TAG}.npz" uv run python 02_extract.py \
    || { echo "$TAG FAILED extract finqa"; return 1; }
  GEN_FILE="generations_${TAG}_tatqa.jsonl" ACT_FILE="activations_${TAG}_tatqa.npz" \
    TOK_FILE="tokens_${TAG}_tatqa.npz" uv run python 02_extract.py \
    || { echo "$TAG FAILED extract tatqa"; return 1; }
  echo "=== $TAG: logit baselines ==="
  GEN_FILE="generations_${TAG}.jsonl" OUT_NAME="${TAG}_finqa" \
    uv run python 11_logit_baselines.py || { echo "$TAG FAILED baselines finqa"; return 1; }
  GEN_FILE="generations_${TAG}_tatqa.jsonl" OUT_NAME="${TAG}_tatqa" \
    uv run python 11_logit_baselines.py || { echo "$TAG FAILED baselines tatqa"; return 1; }
  echo "=== $TAG: self-consistency (stratified subsample) ==="
  GEN_FILE="generations_${TAG}.jsonl" OUT_NAME="${TAG}_finqa" SEQ_TOKEN_BUDGET="$4" \
    SC_CORRECT_N=1500 uv run python 10_selfconsistency.py \
    || { echo "$TAG FAILED selfcons finqa"; return 1; }
  GEN_FILE="generations_${TAG}_tatqa.jsonl" OUT_NAME="${TAG}_tatqa" SEQ_TOKEN_BUDGET="$4" \
    SC_CORRECT_N=400 uv run python 10_selfconsistency.py \
    || { echo "$TAG FAILED selfcons tatqa"; return 1; }
  echo "=== $TAG: DONE ==="
}

ONLY="${1:-all}"
[ "$ONLY" = all ] || [ "$ONLY" = qwen ]  && run_model Qwen/Qwen3-8B                       qwen_full  16 60000
[ "$ONLY" = all ] || [ "$ONLY" = llama ] && run_model meta-llama/Llama-3.1-8B-Instruct   llama_full 16 60000
[ "$ONLY" = all ] || [ "$ONLY" = gemma ] && run_model google/gemma-2-9b-it               gemma_full  6 25000
echo "=== regenerating paper tables ==="
uv run python 14_quadrant_table.py
echo "=== SCALE-UP CHAIN COMPLETE ==="
