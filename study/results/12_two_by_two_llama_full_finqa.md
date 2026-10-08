# 12_two_by_two_llama_full_finqa

- generated: 2026-10-08T13:27:16
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/llama_full_finqa.csv
- scores_header: condition=llama_full_finqa probe_feature=L21_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- n: 6114
- correct_rate: 0.601
- documents: 2103
- confidence_measured_on: 3941/6114
- format: AUROC|PR-AUC (wrong-as-positive; PR baseline = printed prevalence)

```
[1] full population (n=6114, prevalence wrong=0.40):
    ans_mean_lp     0.666|0.577
    ans_min_lp      0.665|0.617
    gen_mean_lp     0.705|0.612
    p_true          0.703|0.659
    self-consist.   0.820|0.879  (conf-measured subset)
    PROBE           0.764|0.698
    probe+baselines 0.792|0.734

[2] 2x2 quadrants (confidence-measured subset; reweighted population shares live in results/quadrants.md):
    conf>=0.75: confident 1902 (acc 63.1%) | unsure 2039 (acc 14.7%) | confident-wrong = 702
    conf>=1.00: confident 1085 (acc 69.7%) | unsure 2856 (acc 26.1%) | confident-wrong = 329

[3] HEADLINE - confident stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR metrics population-reweighted):
    conf>=0.75 (n=1902, 702 wrong, pop-prev=0.19):  best-baseline 0.569|0.260  probe 0.699|0.414  stacked 0.688|0.359
    conf>=1.00 (n=1085, 329 wrong, pop-prev=0.15):  best-baseline 0.550|0.183  probe 0.701|0.368  stacked 0.671|0.307

[3a] unsure stratum (best-baseline = deployment-cheap set, excludes self-consistency; PR population-reweighted):
    (n=2856, 2112 wrong, pop-prev=0.54):  best-cheap-baseline 0.680|0.730  probe 0.730|0.759  stacked 0.755|0.782  (self-consist ref 0.815|0.838 — stratifier, not competitor)

[3b] PR operating points, conf=1.00 stratum (probe; population-reweighted):
     trapezoidal PR area 0.367 (AP 0.368, pop-prev 0.15)
       budget  precision   recall   (weighted)
          5%       0.58     0.19
         10%       0.46     0.31
         20%       0.33     0.44
         30%       0.27     0.54
         50%       0.21     0.71

[4] specialist probe (confident-trained): 0.716|0.601 (general probe, same rows: 0.699|0.607)

[5] partial correlation of probe score with correctness:
    raw r=0.428 | partialling out all confidence measures r=0.227

[6] measure agreement (Spearman):
    self-consist vs p_true      0.591
    self-consist vs ans_mean_lp 0.417
    probe vs self-consist       0.482
```
