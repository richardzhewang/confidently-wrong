# Confidently Wrong: Detecting Hallucinations in Financial Question Answering from LLM Internal States

Code, per-example data, and result tables for the paper of the same title
(Richard Zhe Wang, ACM International Conference on AI in Finance, ICAIF 2026).

**Main result.** Among answers that a model reproduces in all eight resamples (confident
answers), a linear probe on the model's residual stream separates wrong from correct
answers at 0.70–0.77 AUROC on FinQA. The best single output-level confidence signal
reaches 0.55–0.62 on the same answers. The result holds for Qwen3-8B, Llama-3.1-8B, and
Gemma-2-9B.

## Layout

| path | contents |
|---|---|
| `study/code/` | pipeline scripts, numbered in pipeline order, plus `common.py` (prompt, parsing, grader) and `analysis_utils.py` |
| `study/data/` | model answers with grades (`generations_*`), eight-sample self-consistency (`selfcons_*`), output-level signals (`baselines_*`) |
| `study/data/pilot/` | 800-question Qwen3-8B FinQA pilot used by the placebo and the grader audit |
| `study/scores/` | one CSV per model and dataset with every per-example quantity; `extra/` holds the supervised comparison signals |
| `study/results/` | the result tables behind every number in the paper |
| `figures/` | figure script and the two paper figures |

Conditions are named `{qwen,llama,gemma}_full_{finqa,tatqa}`.

## What each paper item comes from

| paper item | script | output in `study/results/` |
|---|---|---|
| Table 1, confidence × correctness | `14_quadrant_table.py` | `quadrants.md` |
| Table 2, all answers and unsure answers | `12_two_by_two.py`, `19_supervised_baselines.py` | `12_two_by_two_*.md`, `19_supervised_baselines_*.md` |
| Table 3, confident answers, with intervals | `12_two_by_two.py`, `19_supervised_baselines.py`, `20_routing_and_uncertainty.py` | as above, `20_routing_and_uncertainty_*.md` section A |
| Table 4, error types | `21_error_types.py` | `21_error_types_*.md` |
| Table 5, review routing | `20_routing_and_uncertainty.py` | `20_routing_and_uncertainty_*.md` section B |
| Figure 1, precision and recall by review budget | `figures/make_figures.py` | `figures/fig1_operating_points.pdf` |
| Figure 2, layer and pooling sweep | `03_probe.py`, `figures/make_figures.py` | `03_layer_sweep_*.md`, `figures/fig2_depth_profiles.pdf` |
| Scale-convention audit and grading sensitivity | `18_scale_audit.py` | `18_scale_audit_*.md`, case lists in `18_scale_audit_cases_*.csv` |
| LLM-judge audit of the grader | `08_grader_audit.py` | `08_grader_audit_pilot.md` |
| Random-initialization placebo | `05_random_control.py` | `05_random_control_pilot.md` |
| Abstention robustness | `17_abstention_robustness.py` | `17_abstention_robustness_*.md` |
| Cross-dataset transfer | `07_ood_probe.py` | `07_ood_transfer_*.md` |
| Question-level versus document-grouped folds | `22_split_leakage.py` | `22_split_leakage_full.md` |
| Partial and rank correlations | `12_two_by_two.py` sections 5 and 6 | `12_two_by_two_*.md` |

## What you can rerun

**From the released files, on a CPU, in minutes.** These scripts read only `study/scores/`
and `study/data/`.

```bash
cd study/code
bash run_analyses.sh report      # scripts 12, 14, 17, 20, 21
cd ../../figures && uv run python make_figures.py
```

**With activations.** Probe fitting needs the residual-stream activations, which are about
22 GB and are not in the repository. Regenerate them with `02_extract.py` (see below).
Then `bash run_analyses.sh` also runs `fit_scores.py`, `03_probe.py`, `07_ood_probe.py`,
`18_scale_audit.py`, `19_supervised_baselines.py`, and `22_split_leakage.py`. The outputs of
all of these are included, so the first tier does not depend on them.

**From scratch.** Generation, activation extraction, output-level signals, and
self-consistency sampling take about 50 GPU-hours on one 32 GB GPU.

```bash
cd study/code
bash run_scaleup.sh              # all three models; or: bash run_scaleup.sh qwen|llama|gemma
bash run_analyses.sh
```

## Setup

Python 3.13 with [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env             # then add your Hugging Face token
```

The cross-validation folds depend on the scikit-learn version. `uv.lock` pins the versions
used for the paper (scikit-learn 1.9.0, numpy 2.5.1). With those versions the released
score files reproduce exactly.

## Pipeline

| script | stage | needs |
|---|---|---|
| `01_generate.py` | greedy answers, parsed and graded | GPU |
| `02_extract.py` | residual-stream activations at seven relative depths, three poolings | GPU |
| `11_logit_baselines.py` | token log-probability scores and P(True) | GPU |
| `10_selfconsistency.py` | eight resamples per question (temperature 0.7, top-p 0.8, top-k 20) | GPU |
| `fit_scores.py` | out-of-fold probe scores, written to `study/scores/` | activations |
| `03_probe.py`, `07_ood_probe.py`, `22_split_leakage.py` | layer sweep, transfer, fold comparison | activations |
| `18_scale_audit.py`, `19_supervised_baselines.py` | grading sensitivity, supervised comparison signals | activations |
| `05_random_control.py` | random-initialization placebo | GPU |
| `08_grader_audit.py` | LLM-judge audit | OpenAI API key |
| `12`, `14`, `17`, `20`, `21` | tables from the score files | CPU |

## Models and data

Models, by Hugging Face identifier: `Qwen/Qwen3-8B`, `meta-llama/Llama-3.1-8B-Instruct`,
`google/gemma-2-9b-it`. All run in bfloat16 with one shared system prompt
(`SYSTEM_PROMPT` in `common.py`). Qwen3's reasoning mode is off.

Questions come from the FLARE releases on the Hugging Face Hub: the training split of
`ChanceFocus/flare-finqa` (6,251 questions) and the single split of
`ChanceFocus/flare-tatqa` (1,668 questions). Questions with a non-numeric gold answer or a
context over 2,800 tokens are dropped. The length filter uses each model's tokenizer, so the
FinQA pool has 6,105 (Qwen3), 6,114 (Llama-3.1), or 6,110 (Gemma-2) questions. The TAT-QA
pool has 1,138 questions for every model.

The files in `study/data/` contain the question and context text of these datasets together
with the model outputs.

| source | license |
|---|---|
| FinQA (Chen et al., EMNLP 2021), https://github.com/czyssrs/FinQA | MIT |
| TAT-QA (Zhu et al., ACL 2021), https://github.com/NExTplusplus/TAT-QA | CC BY 4.0 |
| FLARE / PIXIU prompt format (Xie et al., NeurIPS 2023) | the dataset cards list no license |

## Provenance notes

- The correct-answer subsample for self-consistency is seeded. Self-consistency was
  measured on every wrong answer and on a seeded random subset of correct answers
  (1,500 on FinQA, 400 on TAT-QA). The sampling rate is stored in `selfcons_*_meta.json`,
  and population shares and precision–recall metrics are reweighted with it.
- The sampled generations themselves were not seeded. Rerunning `10_selfconsistency.py`
  gives different resamples.
- Model revisions were not pinned. The runs used the Hub versions available in July 2026.
- The random-initialization placebo and the LLM-judge audit were run on the 800-question
  Qwen3-8B FinQA pilot in `study/data/pilot/`. Everything else uses the full pools.
- Scripts that index token positions force right padding. Generation scripts use left
  padding, which decoder-only `generate` requires.

## Citation

```bibtex
@inproceedings{wang2026confidentlywrong,
  title     = {Confidently Wrong: Detecting Hallucinations in Financial Question Answering from {LLM} Internal States},
  author    = {Wang, Richard Zhe},
  booktitle = {Proceedings of the ACM International Conference on AI in Finance (ICAIF '26)},
  year      = {2026}
}
```
