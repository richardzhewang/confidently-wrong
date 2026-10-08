# 19_supervised_baselines_llama_full_finqa

- generated: 2026-10-07T14:05:39
- grader: v2 (x1000 scales, strict sign, 2% tol)
- probe_feature: L21_ans_mean
- pregen_feature: L21_prompt_last
- n: 6114

```
check: refit probe vs released column  max|diff|=1.45e-02  AUROC refit 0.7641 released 0.7641
signal                            full  confident(8/8)    unsure(<8/8)
ans_mean_lp                      0.666           0.550           0.637
ans_min_lp                       0.665           0.526           0.647
gen_mean_lp                      0.705           0.496           0.659
p_true                           0.703           0.469           0.680
cheap_lr                         0.736           0.498           0.703
cheap_lrq                        0.728           0.481           0.696
cheap_gbm                        0.749           0.540           0.711
cheap_best(=cheap_gbm)           0.749           0.540           0.711
pregen                           0.684           0.699           0.640
pregen_cheap                     0.773           0.657           0.731
probe                            0.764           0.701           0.730
probe_cheap(stacked)             0.792           0.671           0.755
n (wrong):                 6114 (2441)      1085 (329)     2856 (2112)
```
