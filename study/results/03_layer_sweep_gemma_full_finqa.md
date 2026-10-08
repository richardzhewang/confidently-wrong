# 03_layer_sweep_gemma_full_finqa

- generated: 2026-07-09T20:20:26
- grader: v2 (x1000 scales, strict sign, 2% tol)
- activations: activations_gemma_full.npz
- generations: generations_gemma_full.jsonl
- folds: StratifiedGroupKFold(5) by document
- n: 6110
- base_rate_correct: 0.681

```
feature              AUROC    ±sd PR-AUC(wrong)  ctrl-AUROC  select.
L0_ans_last          0.511  0.003         0.330       0.506    0.005
L0_ans_mean          0.665  0.018         0.524       0.495    0.170
L0_prompt_last       0.500  0.000         0.319       0.500    0.000
L7_ans_last          0.722  0.011         0.611       0.492    0.230
L7_ans_mean          0.699  0.011         0.572       0.498    0.201
L7_prompt_last       0.619  0.019         0.443       0.497    0.121
L14_ans_last         0.726  0.008         0.625       0.503    0.223
L14_ans_mean         0.731  0.008         0.624       0.503    0.228
L14_prompt_last      0.634  0.011         0.461       0.504    0.130
L21_ans_last         0.738  0.007         0.629       0.500    0.238
L21_ans_mean         0.764  0.016         0.658       0.496    0.267
L21_prompt_last      0.682  0.004         0.518       0.494    0.188
L28_ans_last         0.757  0.011         0.655       0.500    0.258
L28_ans_mean         0.776  0.008         0.678       0.513    0.264
L28_prompt_last      0.720  0.015         0.580       0.502    0.217
L35_ans_last         0.759  0.008         0.652       0.496    0.262
L35_ans_mean         0.767  0.015         0.653       0.496    0.271
L35_prompt_last      0.718  0.012         0.566       0.492    0.226
L42_ans_last         0.763  0.014         0.662       0.495    0.268
L42_ans_mean         0.761  0.014         0.643       0.494    0.267
L42_prompt_last      0.696  0.014         0.520       0.493    0.203

best: L28_ans_mean AUROC=0.776  (PR-AUC prevalence baseline = 0.319)
```
