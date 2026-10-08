# 22_split_leakage_full

- generated: 2026-10-08T13:31:54
- grader: v2 (x1000 scales, strict sign, 2% tol)
- folds: 5-fold, class-stratified, seed 0; question-level vs document-grouped

```
condition             docs      n | pooled AUROC:  question  document  inflation | mean per-fold:  question  document  inflation
qwen_full_finqa       2099   6105 |                   0.799     0.786     +0.014 |                    0.799     0.785     +0.014
llama_full_finqa      2103   6114 |                   0.783     0.764     +0.019 |                    0.783     0.765     +0.018
gemma_full_finqa      2102   6110 |                   0.790     0.776     +0.014 |                    0.790     0.776     +0.014
qwen_full_tatqa        278   1138 |                   0.766     0.732     +0.034 |                    0.766     0.739     +0.027
llama_full_tatqa       278   1138 |                   0.763     0.751     +0.013 |                    0.763     0.752     +0.010
gemma_full_tatqa       278   1138 |                   0.746     0.733     +0.014 |                    0.745     0.735     +0.010
```
