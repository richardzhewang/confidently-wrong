# 18_scale_audit_qwen_full_tatqa

- generated: 2026-10-07T14:17:15
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 1138
- tolerance: 0.02

```
[1] how graded-correct answers are accepted (n correct = 1012):
    identity                 974   96.2% of correct   85.6% of all
    percent_supported          5    0.5% of correct    0.4% of all
    percent_unsupported        0    0.0% of correct    0.0% of all
    thousand_scale            33    3.3% of correct    2.9% of all
    accepted only via rescaling: 38 (3.8% of correct); of these supported percent matches 13.2%, unit-dependent 33 (2.90% of all answers)

[2] restricted grading: 33 labels flip correct->wrong; accuracy 0.889 -> 0.860; 8/8-confident (measured) 459 -> 456
[3] confident subgroup (8/8), AUROC:
  paper grading                      n=  459 wrong=   74  best-baseline 0.629  probe 0.687  delta +0.059   | full-pop probe 0.732
  restricted labels, paper confidence n=  459 wrong=   91  best-baseline 0.617  probe 0.780  delta +0.163   | full-pop probe 0.777
  restricted labels + confidence     n=  456 wrong=   89  best-baseline 0.614  probe 0.782  delta +0.168   | full-pop probe 0.777
  delta: paper +0.059 | restricted labels +0.163 | restricted labels + confidence +0.168
```
