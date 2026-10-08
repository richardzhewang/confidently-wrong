# 19_supervised_baselines_gemma_full_finqa

- generated: 2026-10-07T14:07:36
- grader: v2 (x1000 scales, strict sign, 2% tol)
- probe_feature: L28_ans_mean
- pregen_feature: L28_prompt_last
- n: 6110

```
check: refit probe vs released column  max|diff|=2.16e-02  AUROC refit 0.7761 released 0.7761
signal                            full  confident(8/8)    unsure(<8/8)
ans_mean_lp                      0.578           0.504           0.610
ans_min_lp                       0.543           0.508           0.507
gen_mean_lp                      0.651           0.564           0.651
p_true                           0.657           0.624           0.573
cheap_lr                         0.671           0.577           0.674
cheap_lrq                        0.695           0.617           0.641
cheap_gbm                        0.724           0.646           0.692
cheap_best(=cheap_gbm)           0.724           0.646           0.692
pregen                           0.720           0.715           0.626
pregen_cheap                     0.750           0.715           0.681
probe                            0.776           0.755           0.715
probe_cheap(stacked)             0.796           0.762           0.736
n (wrong):                 6110 (1948)      2141 (861)     1307 (1087)
```
