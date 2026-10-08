# 18_scale_audit_llama_full_finqa

- generated: 2026-10-07T14:16:54
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 6114
- tolerance: 0.02

```
[1] how graded-correct answers are accepted (n correct = 3673):
    identity                1460   39.7% of correct   23.9% of all
    percent_supported       2125   57.9% of correct   34.8% of all
    percent_unsupported       11    0.3% of correct    0.2% of all
    thousand_scale            77    2.1% of correct    1.3% of all
    accepted only via rescaling: 2213 (60.3% of correct); of these supported percent matches 96.0%, unit-dependent 88 (1.44% of all answers)

[2] restricted grading: 88 labels flip correct->wrong; accuracy 0.601 -> 0.586; 8/8-confident (measured) 1085 -> 1064
[3] confident subgroup (8/8), AUROC:
  paper grading                      n= 1085 wrong=  329  best-baseline 0.550  probe 0.701  delta +0.151   | full-pop probe 0.764
  restricted labels, paper confidence n= 1085 wrong=  338  best-baseline 0.548  probe 0.732  delta +0.185   | full-pop probe 0.769
  restricted labels + confidence     n= 1064 wrong=  326  best-baseline 0.548  probe 0.729  delta +0.180   | full-pop probe 0.769
  delta: paper +0.151 | restricted labels +0.185 | restricted labels + confidence +0.180
```
