# 03_layer_sweep_llama_full_finqa

- generated: 2026-07-09T13:01:22
- grader: v2 (x1000 scales, strict sign, 2% tol)
- activations: activations_llama_full.npz
- generations: generations_llama_full.jsonl
- folds: StratifiedGroupKFold(5) by document
- n: 6114
- base_rate_correct: 0.601

```
feature              AUROC    ±sd PR-AUC(wrong)  ctrl-AUROC  select.
L0_ans_last          0.647  0.005         0.588       0.514    0.133
L0_ans_mean          0.691  0.015         0.589       0.516    0.175
L0_prompt_last       0.500  0.000         0.399       0.500    0.000
L5_ans_last          0.742  0.021         0.695       0.509    0.233
L5_ans_mean          0.729  0.005         0.644       0.501    0.228
L5_prompt_last       0.610  0.014         0.505       0.489    0.121
L11_ans_last         0.769  0.013         0.735       0.513    0.257
L11_ans_mean         0.757  0.006         0.687       0.508    0.249
L11_prompt_last      0.634  0.003         0.533       0.498    0.136
L16_ans_last         0.772  0.013         0.738       0.506    0.266
L16_ans_mean         0.778  0.003         0.715       0.512    0.266
L16_prompt_last      0.670  0.010         0.563       0.498    0.172
L21_ans_last         0.768  0.016         0.733       0.512    0.256
L21_ans_mean         0.765  0.011         0.699       0.513    0.252
L21_prompt_last      0.685  0.009         0.589       0.505    0.179
L27_ans_last         0.773  0.014         0.739       0.509    0.264
L27_ans_mean         0.757  0.016         0.683       0.505    0.253
L27_prompt_last      0.659  0.012         0.557       0.500    0.159
L32_ans_last         0.769  0.011         0.734       0.501    0.268
L32_ans_mean         0.751  0.014         0.674       0.503    0.247
L32_prompt_last      0.652  0.004         0.550       0.501    0.151

best: L16_ans_mean AUROC=0.778  (PR-AUC prevalence baseline = 0.399)
```
