# 19_supervised_baselines_qwen_full_tatqa

- generated: 2026-10-07T14:08:20
- grader: v2 (x1000 scales, strict sign, 2% tol)
- probe_feature: L24_ans_mean
- pregen_feature: L24_prompt_last
- n: 1138

```
check: refit probe vs released column  max|diff|=2.33e-02  AUROC refit 0.7318 released 0.7325
signal                            full  confident(8/8)    unsure(<8/8)
ans_mean_lp                      0.622           0.594           0.691
ans_min_lp                       0.619           0.594           0.687
gen_mean_lp                      0.649           0.576           0.582
p_true                           0.725           0.629           0.660
cheap_lr                         0.706           0.637           0.622
cheap_lrq                        0.735           0.642           0.715
cheap_gbm                        0.718           0.666           0.629
cheap_best(=cheap_lrq)           0.735           0.642           0.715
pregen                           0.653           0.592           0.683
pregen_cheap                     0.725           0.652           0.669
probe                            0.732           0.687           0.697
probe_cheap(stacked)             0.752           0.680           0.658
n (wrong):                  1138 (126)        459 (74)         67 (52)
```
