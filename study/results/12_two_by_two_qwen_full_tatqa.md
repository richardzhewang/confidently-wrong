# 12_two_by_two_qwen_full_tatqa

- generated: 2026-10-08T13:27:16
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/qwen_full_tatqa.csv
- scores_header: condition=qwen_full_tatqa probe_feature=L24_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- n: 1138
- correct_rate: 0.889
- documents: 278
- confidence_measured_on: 526/1138
- format: AUROC|PR-AUC (wrong-as-positive; PR baseline = printed prevalence)

```
[1] full population (n=1138, prevalence wrong=0.11):
    ans_mean_lp     0.622|0.197
    ans_min_lp      0.619|0.209
    gen_mean_lp     0.649|0.220
    p_true          0.725|0.342
    self-consist.   0.689|0.491  (conf-measured subset)
    PROBE           0.732|0.340
    probe+baselines 0.752|0.400

[2] 2x2 quadrants (confidence-measured subset; reweighted population shares live in results/quadrants.md):
    conf>=0.75: confident  485 (acc 80.8%) | unsure   41 (acc 19.5%) | confident-wrong = 93
    conf>=1.00: confident  459 (acc 83.9%) | unsure   67 (acc 22.4%) | confident-wrong = 74

[3] HEADLINE - confident stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR metrics population-reweighted):
    conf>=0.75 (n=485, 93 wrong, pop-prev=0.09):  best-baseline 0.667|0.240  probe 0.710|0.269  stacked 0.706|0.272
    conf>=1.00 (n=459, 74 wrong, pop-prev=0.07):  best-baseline 0.629|0.183  probe 0.687|0.204  stacked 0.680|0.213

[3a] unsure stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR population-reweighted):
    (n=67, 52 wrong, pop-prev=0.58):  best-cheap-baseline 0.691|0.721  probe 0.697|0.759  stacked 0.658|0.743  (self-consist ref 0.587|0.706 — stratifier, not competitor)

[3b] PR operating points, conf=1.00 stratum (probe; population-reweighted):
     trapezoidal PR area 0.199 (AP 0.204, pop-prev 0.07)
       budget  precision   recall   (weighted)
          5%       0.26     0.19
         10%       0.24     0.34
         20%       0.16     0.45
         30%       0.14     0.58
         50%       0.10     0.73

[4] specialist probe (confident-trained): 0.730|0.410 (general probe, same rows: 0.710|0.440)

[5] partial correlation of probe score with correctness:
    raw r=0.408 | partialling out all confidence measures r=0.261

[6] measure agreement (Spearman):
    self-consist vs p_true      0.421
    self-consist vs ans_mean_lp 0.128
    probe vs self-consist       0.292
```
