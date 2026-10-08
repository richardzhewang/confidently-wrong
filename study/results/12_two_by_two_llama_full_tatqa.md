# 12_two_by_two_llama_full_tatqa

- generated: 2026-10-08T13:27:16
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/llama_full_tatqa.csv
- scores_header: condition=llama_full_tatqa probe_feature=L21_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- n: 1138
- correct_rate: 0.758
- documents: 278
- confidence_measured_on: 675/1138
- format: AUROC|PR-AUC (wrong-as-positive; PR baseline = printed prevalence)

```
[1] full population (n=1138, prevalence wrong=0.24):
    ans_mean_lp     0.648|0.431
    ans_min_lp      0.654|0.483
    gen_mean_lp     0.643|0.369
    p_true          0.726|0.476
    self-consist.   0.839|0.796  (conf-measured subset)
    PROBE           0.751|0.513
    probe+baselines 0.781|0.575

[2] 2x2 quadrants (confidence-measured subset; reweighted population shares live in results/quadrants.md):
    conf>=0.75: confident  436 (acc 80.0%) | unsure  239 (acc 21.3%) | confident-wrong = 87
    conf>=1.00: confident  307 (acc 85.7%) | unsure  368 (acc 37.2%) | confident-wrong = 44

[3] HEADLINE - confident stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR metrics population-reweighted):
    conf>=0.75 (n=436, 87 wrong, pop-prev=0.10):  best-baseline 0.600|0.169  probe 0.683|0.226  stacked 0.701|0.244
    conf>=1.00 (n=307, 44 wrong, pop-prev=0.07):  best-baseline 0.587|0.131  probe 0.708|0.222  stacked 0.693|0.213

[3a] unsure stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR population-reweighted):
    (n=368, 231 wrong, pop-prev=0.44):  best-cheap-baseline 0.679|0.656  probe 0.658|0.598  stacked 0.699|0.686  (self-consist ref 0.815|0.775 — stratifier, not competitor)

[3b] PR operating points, conf=1.00 stratum (probe; population-reweighted):
     trapezoidal PR area 0.216 (AP 0.222, pop-prev 0.07)
       budget  precision   recall   (weighted)
          5%       0.25     0.18
         10%       0.23     0.32
         20%       0.18     0.52
         30%       0.15     0.61
         50%       0.10     0.73

[4] specialist probe (confident-trained): 0.605|0.300 (general probe, same rows: 0.683|0.372)

[5] partial correlation of probe score with correctness:
    raw r=0.404 | partialling out all confidence measures r=0.119

[6] measure agreement (Spearman):
    self-consist vs p_true      0.494
    self-consist vs ans_mean_lp 0.338
    probe vs self-consist       0.484
```
