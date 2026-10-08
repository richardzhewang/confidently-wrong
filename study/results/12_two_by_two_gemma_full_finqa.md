# 12_two_by_two_gemma_full_finqa

- generated: 2026-10-08T13:27:16
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/gemma_full_finqa.csv
- scores_header: condition=gemma_full_finqa probe_feature=L28_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- n: 6110
- correct_rate: 0.681
- documents: 2102
- confidence_measured_on: 3448/6110
- format: AUROC|PR-AUC (wrong-as-positive; PR baseline = printed prevalence)

```
[1] full population (n=6110, prevalence wrong=0.32):
    ans_mean_lp     0.578|0.440
    ans_min_lp      0.543|0.374
    gen_mean_lp     0.651|0.510
    p_true          0.657|0.480
    self-consist.   0.724|0.764  (conf-measured subset)
    PROBE           0.776|0.677
    probe+baselines 0.796|0.664

[2] 2x2 quadrants (confidence-measured subset; reweighted population shares live in results/quadrants.md):
    conf>=0.75: confident 2574 (acc 54.9%) | unsure  874 (acc 10.1%) | confident-wrong = 1162
    conf>=1.00: confident 2141 (acc 59.8%) | unsure 1307 (acc 16.8%) | confident-wrong = 861

[3] HEADLINE - confident stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR metrics population-reweighted):
    conf>=0.75 (n=2574, 1162 wrong, pop-prev=0.23):  best-baseline 0.641|0.346  probe 0.755|0.538  stacked 0.766|0.507
    conf>=1.00 (n=2141, 861 wrong, pop-prev=0.20):  best-baseline 0.624|0.292  probe 0.755|0.499  stacked 0.762|0.453

[3a] unsure stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR population-reweighted):
    (n=1307, 1087 wrong, pop-prev=0.64):  best-cheap-baseline 0.651|0.785  probe 0.715|0.832  stacked 0.736|0.843  (self-consist ref 0.729|0.818 — stratifier, not competitor)

[3b] PR operating points, conf=1.00 stratum (probe; population-reweighted):
     trapezoidal PR area 0.499 (AP 0.499, pop-prev 0.20)
       budget  precision   recall   (weighted)
          5%       0.67     0.17
         10%       0.62     0.32
         20%       0.47     0.48
         30%       0.40     0.62
         50%       0.31     0.79

[4] specialist probe (confident-trained): 0.757|0.737 (general probe, same rows: 0.755|0.738)

[5] partial correlation of probe score with correctness:
    raw r=0.478 | partialling out all confidence measures r=0.359

[6] measure agreement (Spearman):
    self-consist vs p_true      0.302
    self-consist vs ans_mean_lp 0.278
    probe vs self-consist       0.385
```
