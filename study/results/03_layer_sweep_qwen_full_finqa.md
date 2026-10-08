# 03_layer_sweep_qwen_full_finqa

- generated: 2026-07-09T20:53:27
- grader: v2 (x1000 scales, strict sign, 2% tol)
- activations: activations_qwen_full.npz
- generations: generations_qwen_full.jsonl
- folds: StratifiedGroupKFold(5) by document
- n: 6105
- base_rate_correct: 0.699

```
feature              AUROC    ±sd PR-AUC(wrong)  ctrl-AUROC  select.
L0_ans_last          0.578  0.013         0.388       0.510    0.068
L0_ans_mean          0.699  0.014         0.556       0.498    0.201
L0_prompt_last       0.500  0.000         0.301       0.500    0.000
L6_ans_last          0.731  0.011         0.610       0.504    0.227
L6_ans_mean          0.723  0.013         0.591       0.506    0.217
L6_prompt_last       0.602  0.007         0.395       0.497    0.105
L12_ans_last         0.729  0.009         0.613       0.491    0.238
L12_ans_mean         0.764  0.007         0.637       0.487    0.277
L12_prompt_last      0.620  0.013         0.411       0.489    0.131
L18_ans_last         0.765  0.016         0.666       0.498    0.267
L18_ans_mean         0.777  0.015         0.660       0.513    0.265
L18_prompt_last      0.642  0.006         0.431       0.486    0.156
L24_ans_last         0.776  0.012         0.661       0.503    0.273
L24_ans_mean         0.785  0.009         0.660       0.517    0.268
L24_prompt_last      0.723  0.011         0.552       0.484    0.239
L30_ans_last         0.764  0.014         0.647       0.511    0.253
L30_ans_mean         0.777  0.011         0.666       0.501    0.276
L30_prompt_last      0.709  0.008         0.535       0.512    0.197
L36_ans_last         0.764  0.011         0.646       0.499    0.265
L36_ans_mean         0.785  0.013         0.660       0.499    0.286
L36_prompt_last      0.714  0.008         0.529       0.515    0.198

best: L24_ans_mean AUROC=0.785  (PR-AUC prevalence baseline = 0.301)
```
