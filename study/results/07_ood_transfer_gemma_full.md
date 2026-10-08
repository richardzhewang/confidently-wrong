# 07_ood_transfer_gemma_full

- generated: 2026-07-09T20:25:22
- grader: v2 (x1000 scales, strict sign, 2% tol)
- A (FinQA): activations_gemma_full.npz, n=6110, correct=0.681
- B (TAT-QA): activations_gemma_full_tatqa.npz, n=1138, correct=0.837
- in-dist folds: StratifiedGroupKFold(5) by document

```
feature              A in-dist B in-dist    A->B    B->A
L0_ans_mean              0.665     0.518   0.530   0.568
L7_ans_mean              0.699     0.588   0.539   0.587
L14_ans_mean             0.731     0.646   0.514   0.586
L21_ans_mean             0.764     0.719   0.612   0.663
L28_ans_mean             0.776     0.735   0.606   0.703
L35_ans_mean             0.767     0.742   0.611   0.696
L42_ans_mean             0.761     0.740   0.606   0.690
L42_prompt_last          0.696     0.630   0.548   0.602
```
