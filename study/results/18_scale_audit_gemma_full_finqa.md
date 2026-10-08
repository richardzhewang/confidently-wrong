# 18_scale_audit_gemma_full_finqa

- generated: 2026-10-07T14:17:10
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 6110
- tolerance: 0.02

```
[1] how graded-correct answers are accepted (n correct = 4162):
    identity                1611   38.7% of correct   26.4% of all
    percent_supported       2481   59.6% of correct   40.6% of all
    percent_unsupported        4    0.1% of correct    0.1% of all
    thousand_scale            66    1.6% of correct    1.1% of all
    accepted only via rescaling: 2551 (61.3% of correct); of these supported percent matches 97.3%, unit-dependent 70 (1.15% of all answers)

[2] restricted grading: 70 labels flip correct->wrong; accuracy 0.681 -> 0.670; 8/8-confident (measured) 2141 -> 2103
[3] confident subgroup (8/8), AUROC:
  paper grading                      n= 2141 wrong=  861  best-baseline 0.624  probe 0.755  delta +0.131   | full-pop probe 0.776
  restricted labels, paper confidence n= 2141 wrong=  880  best-baseline 0.634  probe 0.760  delta +0.126   | full-pop probe 0.779
  restricted labels + confidence     n= 2103 wrong=  848  best-baseline 0.630  probe 0.760  delta +0.130   | full-pop probe 0.779
  delta: paper +0.131 | restricted labels +0.126 | restricted labels + confidence +0.130
```
