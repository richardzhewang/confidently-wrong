# 18_scale_audit_gemma_full_tatqa

- generated: 2026-10-07T14:17:26
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 1138
- tolerance: 0.02

```
[1] how graded-correct answers are accepted (n correct = 952):
    identity                 889   93.4% of correct   78.1% of all
    percent_supported          5    0.5% of correct    0.4% of all
    percent_unsupported        1    0.1% of correct    0.1% of all
    thousand_scale            57    6.0% of correct    5.0% of all
    accepted only via rescaling: 63 (6.6% of correct); of these supported percent matches 7.9%, unit-dependent 58 (5.10% of all answers)

[2] restricted grading: 58 labels flip correct->wrong; accuracy 0.837 -> 0.786; 8/8-confident (measured) 434 -> 407
[3] confident subgroup (8/8), AUROC:
  paper grading                      n=  434 wrong=   72  best-baseline 0.593  probe 0.684  delta +0.091   | full-pop probe 0.733
  restricted labels, paper confidence n=  434 wrong=   96  best-baseline 0.646  probe 0.829  delta +0.183   | full-pop probe 0.774
  restricted labels + confidence     n=  407 wrong=   83  best-baseline 0.646  probe 0.804  delta +0.158   | full-pop probe 0.774
  delta: paper +0.091 | restricted labels +0.183 | restricted labels + confidence +0.158
```
