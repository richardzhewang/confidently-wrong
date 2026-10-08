# 07_ood_transfer_qwen_full

- generated: 2026-10-07T14:21:10
- grader: v2 (x1000 scales, strict sign, 2% tol)
- A (FinQA): activations_qwen_full.npz, n=6105, correct=0.699
- B (TAT-QA): activations_qwen_full_tatqa.npz, n=1138, correct=0.889
- in-dist folds: StratifiedGroupKFold(5) by document

```
feature              A in-dist B in-dist    A->B    B->A
L18_ans_mean             0.777     0.723   0.584   0.642
L24_ans_mean             0.785     0.739   0.621   0.651
L30_ans_mean             0.777     0.726   0.621   0.664
```
