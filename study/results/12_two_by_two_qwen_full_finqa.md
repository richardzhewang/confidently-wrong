# 12_two_by_two_qwen_full_finqa

- generated: 2026-10-08T13:27:16
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/qwen_full_finqa.csv
- scores_header: condition=qwen_full_finqa probe_feature=L24_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- n: 6105
- correct_rate: 0.699
- documents: 2099
- confidence_measured_on: 3339/6105
- format: AUROC|PR-AUC (wrong-as-positive; PR baseline = printed prevalence)

```
[1] full population (n=6105, prevalence wrong=0.30):
    ans_mean_lp     0.575|0.341
    ans_min_lp      0.567|0.339
    gen_mean_lp     0.605|0.442
    p_true          0.692|0.521
    self-consist.   0.651|0.683  (conf-measured subset)
    PROBE           0.786|0.660
    probe+baselines 0.794|0.659

[2] 2x2 quadrants (confidence-measured subset; reweighted population shares live in results/quadrants.md):
    conf>=0.75: confident 2827 (acc 51.0%) | unsure  512 (acc 11.1%) | confident-wrong = 1384
    conf>=1.00: confident 2503 (acc 54.6%) | unsure  836 (acc 16.0%) | confident-wrong = 1137

[3] HEADLINE - confident stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR metrics population-reweighted):
    conf>=0.75 (n=2827, 1384 wrong, pop-prev=0.25):  best-baseline 0.640|0.414  probe 0.765|0.595  stacked 0.765|0.570
    conf>=1.00 (n=2503, 1137 wrong, pop-prev=0.23):  best-baseline 0.615|0.348  probe 0.766|0.563  stacked 0.761|0.530

[3a] unsure stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR population-reweighted):
    (n=836, 702 wrong, pop-prev=0.65):  best-cheap-baseline 0.669|0.794  probe 0.722|0.841  stacked 0.726|0.827  (self-consist ref 0.645|0.761 — stratifier, not competitor)

[3b] PR operating points, conf=1.00 stratum (probe; population-reweighted):
     trapezoidal PR area 0.562 (AP 0.563, pop-prev 0.23)
       budget  precision   recall   (weighted)
          5%       0.79     0.17
         10%       0.69     0.31
         20%       0.54     0.47
         30%       0.45     0.60
         50%       0.36     0.80

[4] specialist probe (confident-trained): 0.765|0.776 (general probe, same rows: 0.765|0.778)

[5] partial correlation of probe score with correctness:
    raw r=0.461 | partialling out all confidence measures r=0.382

[6] measure agreement (Spearman):
    self-consist vs p_true      0.460
    self-consist vs ans_mean_lp 0.181
    probe vs self-consist       0.275
```
