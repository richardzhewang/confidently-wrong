# 18_scale_audit_qwen_full_finqa

- generated: 2026-10-07T14:16:35
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 6105
- tolerance: 0.02

```
[1] how graded-correct answers are accepted (n correct = 4266):
    identity                1804   42.3% of correct   29.5% of all
    percent_supported       2410   56.5% of correct   39.5% of all
    percent_unsupported        7    0.2% of correct    0.1% of all
    thousand_scale            45    1.1% of correct    0.7% of all
    accepted only via rescaling: 2462 (57.7% of correct); of these supported percent matches 97.9%, unit-dependent 52 (0.85% of all answers)

[2] restricted grading: 52 labels flip correct->wrong; accuracy 0.699 -> 0.690; 8/8-confident (measured) 2503 -> 2483
[3] confident subgroup (8/8), AUROC:
  paper grading                      n= 2503 wrong= 1137  best-baseline 0.615  probe 0.766  delta +0.151   | full-pop probe 0.786
  restricted labels, paper confidence n= 2503 wrong= 1154  best-baseline 0.616  probe 0.770  delta +0.154   | full-pop probe 0.785
  restricted labels + confidence     n= 2483 wrong= 1138  best-baseline 0.617  probe 0.769  delta +0.152   | full-pop probe 0.785
  delta: paper +0.151 | restricted labels +0.154 | restricted labels + confidence +0.152
```
