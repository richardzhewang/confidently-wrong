# 18_scale_audit_llama_full_tatqa

- generated: 2026-10-07T14:17:20
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 1138
- tolerance: 0.02

```
[1] how graded-correct answers are accepted (n correct = 863):
    identity                 816   94.6% of correct   71.7% of all
    percent_supported          6    0.7% of correct    0.5% of all
    percent_unsupported        0    0.0% of correct    0.0% of all
    thousand_scale            41    4.8% of correct    3.6% of all
    accepted only via rescaling: 47 (5.4% of correct); of these supported percent matches 12.8%, unit-dependent 41 (3.60% of all answers)

[2] restricted grading: 41 labels flip correct->wrong; accuracy 0.758 -> 0.722; 8/8-confident (measured) 307 -> 285
[3] confident subgroup (8/8), AUROC:
  paper grading                      n=  307 wrong=   44  best-baseline 0.587  probe 0.708  delta +0.122   | full-pop probe 0.751
  restricted labels, paper confidence n=  307 wrong=   53  best-baseline 0.546  probe 0.726  delta +0.180   | full-pop probe 0.739
  restricted labels + confidence     n=  285 wrong=   44  best-baseline 0.577  probe 0.694  delta +0.117   | full-pop probe 0.739
  delta: paper +0.122 | restricted labels +0.180 | restricted labels + confidence +0.117
```
