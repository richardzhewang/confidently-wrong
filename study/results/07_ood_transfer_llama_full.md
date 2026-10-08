# 07_ood_transfer_llama_full

- generated: 2026-07-09T13:06:07
- grader: v2 (x1000 scales, strict sign, 2% tol)
- A (FinQA): activations_llama_full.npz, n=6114, correct=0.601
- B (TAT-QA): activations_llama_full_tatqa.npz, n=1138, correct=0.758
- in-dist folds: StratifiedGroupKFold(5) by document

```
feature              A in-dist B in-dist    A->B    B->A
L0_ans_mean              0.691     0.651   0.578   0.645
L5_ans_mean              0.729     0.711   0.627   0.674
L11_ans_mean             0.757     0.743   0.632   0.685
L16_ans_mean             0.778     0.759   0.655   0.692
L21_ans_mean             0.765     0.752   0.594   0.675
L27_ans_mean             0.757     0.748   0.611   0.680
L32_ans_mean             0.751     0.727   0.606   0.681
L32_prompt_last          0.652     0.624   0.589   0.579
```
