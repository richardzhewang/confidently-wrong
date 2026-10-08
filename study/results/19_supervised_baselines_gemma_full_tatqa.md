# 19_supervised_baselines_gemma_full_tatqa

- generated: 2026-10-07T14:09:49
- grader: v2 (x1000 scales, strict sign, 2% tol)
- probe_feature: L28_ans_mean
- pregen_feature: L28_prompt_last
- n: 1138

```
check: refit probe vs released column  max|diff|=1.59e-02  AUROC refit 0.7326 released 0.7326
signal                            full  confident(8/8)    unsure(<8/8)
ans_mean_lp                      0.533           0.494           0.446
ans_min_lp                       0.513           0.500           0.442
gen_mean_lp                      0.588           0.543           0.544
p_true                           0.696           0.593           0.613
cheap_lr                         0.614           0.529           0.563
cheap_lrq                        0.704           0.602           0.621
cheap_gbm                        0.658           0.596           0.554
cheap_best(=cheap_lrq)           0.704           0.602           0.621
pregen                           0.660           0.640           0.468
pregen_cheap                     0.683           0.596           0.498
probe                            0.733           0.684           0.543
probe_cheap(stacked)             0.714           0.631           0.545
n (wrong):                  1138 (186)        434 (72)       152 (114)
```
