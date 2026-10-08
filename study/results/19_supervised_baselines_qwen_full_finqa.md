# 19_supervised_baselines_qwen_full_finqa

- generated: 2026-10-07T14:03:24
- grader: v2 (x1000 scales, strict sign, 2% tol)
- probe_feature: L24_ans_mean
- pregen_feature: L24_prompt_last
- n: 6105

```
check: refit probe vs released column  max|diff|=1.49e-02  AUROC refit 0.7856 released 0.7856
signal                            full  confident(8/8)    unsure(<8/8)
ans_mean_lp                      0.575           0.556           0.508
ans_min_lp                       0.567           0.547           0.503
gen_mean_lp                      0.605           0.536           0.547
p_true                           0.692           0.615           0.669
cheap_lr                         0.654           0.574           0.637
cheap_lrq                        0.686           0.614           0.611
cheap_gbm                        0.705           0.646           0.655
cheap_best(=cheap_gbm)           0.705           0.646           0.655
pregen                           0.723           0.727           0.620
pregen_cheap                     0.754           0.726           0.677
probe                            0.786           0.766           0.722
probe_cheap(stacked)             0.794           0.761           0.726
n (wrong):                 6105 (1839)     2503 (1137)       836 (702)
```
