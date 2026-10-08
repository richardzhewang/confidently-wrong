# 12_two_by_two_gemma_full_tatqa

- generated: 2026-10-08T13:27:16
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/gemma_full_tatqa.csv
- scores_header: condition=gemma_full_tatqa probe_feature=L28_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- n: 1138
- correct_rate: 0.837
- documents: 278
- confidence_measured_on: 586/1138
- format: AUROC|PR-AUC (wrong-as-positive; PR baseline = printed prevalence)

```
[1] full population (n=1138, prevalence wrong=0.16):
    ans_mean_lp     0.533|0.223
    ans_min_lp      0.513|0.196
    gen_mean_lp     0.588|0.238
    p_true          0.696|0.313
    self-consist.   0.770|0.646  (conf-measured subset)
    PROBE           0.733|0.388
    probe+baselines 0.714|0.398

[2] 2x2 quadrants (confidence-measured subset; reweighted population shares live in results/quadrants.md):
    conf>=0.75: confident  498 (acc 77.5%) | unsure   88 (acc 15.9%) | confident-wrong = 112
    conf>=1.00: confident  434 (acc 83.4%) | unsure  152 (acc 25.0%) | confident-wrong = 72

[3] HEADLINE - confident stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR metrics population-reweighted):
    conf>=0.75 (n=498, 112 wrong, pop-prev=0.11):  best-baseline 0.637|0.172  probe 0.697|0.274  stacked 0.651|0.243
    conf>=1.00 (n=434, 72 wrong, pop-prev=0.08):  best-baseline 0.593|0.104  probe 0.684|0.218  stacked 0.631|0.187

[3a] unsure stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR population-reweighted):
    (n=152, 114 wrong, pop-prev=0.56):  best-cheap-baseline 0.613|0.648  probe 0.543|0.640  stacked 0.545|0.641  (self-consist ref 0.686|0.722 — stratifier, not competitor)

[3b] PR operating points, conf=1.00 stratum (probe; population-reweighted):
     trapezoidal PR area 0.210 (AP 0.218, pop-prev 0.08)
       budget  precision   recall   (weighted)
          5%       0.30     0.19
         10%       0.24     0.31
         20%       0.18     0.46
         30%       0.13     0.51
         50%       0.11     0.71

[4] specialist probe (confident-trained): 0.697|0.418 (general probe, same rows: 0.697|0.445)

[5] partial correlation of probe score with correctness:
    raw r=0.399 | partialling out all confidence measures r=0.219

[6] measure agreement (Spearman):
    self-consist vs p_true      0.379
    self-consist vs ans_mean_lp 0.094
    probe vs self-consist       0.437
```
