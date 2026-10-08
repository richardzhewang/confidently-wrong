# 05_random_control (random-initialization placebo)

- script: study/code/05_random_control.py
- model: randomly initialized Qwen3-8B (same architecture, untrained weights, torch seed 0)
- data: study/data/pilot/generations_qwen_finqa_pilot.jsonl (800 FinQA questions, Qwen3-8B answers)
- folds: 5-fold, class-stratified, question-level, seed 0
- feature: mean over generated tokens, layers 18 and 24

Console record of the run:

```
random-model L18_ans_mean AUROC: 0.636 ± 0.030
random-model L24_ans_mean AUROC: 0.625 ± 0.027
```

The paper reports the layer-24 value (0.625), the 2/3-depth layer of Qwen3-8B.
