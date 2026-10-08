# 19_supervised_baselines_llama_full_tatqa

- generated: 2026-10-07T14:09:09
- grader: v2 (x1000 scales, strict sign, 2% tol)
- probe_feature: L21_ans_mean
- pregen_feature: L21_prompt_last
- n: 1138

```
check: refit probe vs released column  max|diff|=1.38e-02  AUROC refit 0.7507 released 0.7507
signal                            full  confident(8/8)    unsure(<8/8)
ans_mean_lp                      0.648           0.532           0.613
ans_min_lp                       0.654           0.553           0.631
gen_mean_lp                      0.643           0.542           0.608
p_true                           0.726           0.587           0.679
cheap_lr                         0.718           0.586           0.680
cheap_lrq                        0.758           0.617           0.692
cheap_gbm                        0.726           0.591           0.647
cheap_best(=cheap_lrq)           0.758           0.617           0.692
pregen                           0.648           0.613           0.558
pregen_cheap                     0.742           0.664           0.675
probe                            0.751           0.708           0.658
probe_cheap(stacked)             0.781           0.693           0.699
n (wrong):                  1138 (275)        307 (44)       368 (231)
```
