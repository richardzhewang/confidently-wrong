# 20_routing_and_uncertainty_gemma_full_finqa

- generated: 2026-10-07T14:13:57
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 6110
- bootstrap: document-clustered, paired, 2000 replicates, seed 0

```
[A] AUROC and paired differences (probe minus comparison), 95% CI
  confident(8/8): n=2141 wrong=861  probe 0.755 [0.732, 0.777]
    vs best_single   0.624   delta +0.131 [+0.101, +0.160]   P(delta<=0)=0.000
    vs cheap_best    0.646   delta +0.109 [+0.079, +0.135]   P(delta<=0)=0.000
    vs pregen        0.715   delta +0.040 [+0.014, +0.065]   P(delta<=0)=0.001
    vs pregen_cheap  0.715   delta +0.040 [+0.014, +0.066]   P(delta<=0)=0.001
    stacked       0.762   stacked-probe +0.007 [-0.005, +0.019]
  unsure(<8/8): n=1307 wrong=1087  probe 0.715 [0.681, 0.750]
    vs best_single   0.651   delta +0.065 [+0.019, +0.111]   P(delta<=0)=0.003
    vs cheap_best    0.692   delta +0.024 [-0.016, +0.068]   P(delta<=0)=0.138
    vs pregen        0.626   delta +0.089 [+0.052, +0.127]   P(delta<=0)=0.000
    vs pregen_cheap  0.681   delta +0.034 [-0.002, +0.071]   P(delta<=0)=0.032
    stacked       0.736   stacked-probe +0.021 [+0.006, +0.036]
  full: n=6110 wrong=1948  probe 0.776 [0.762, 0.790]
    vs best_single   0.657   delta +0.120 [+0.099, +0.135]   P(delta<=0)=0.000
    vs cheap_best    0.724   delta +0.053 [+0.035, +0.069]   P(delta<=0)=0.000
    vs pregen        0.720   delta +0.057 [+0.040, +0.072]   P(delta<=0)=0.000
    vs pregen_cheap  0.750   delta +0.026 [+0.010, +0.042]   P(delta<=0)=0.001
    stacked       0.796   stacked-probe +0.020 [+0.013, +0.027]

[B] evaluation half: n=3054 wrong=973 confident-wrong=413
  capacity  alpha | share of ALL wrong caught:     p_true cheap_best     pregen      probe    stacked  two_stage
       10%    0.0 |                                 17.6%      21.3%      22.2%      25.7%      26.1%      25.7%
       20%    0.2 |                                 32.2%      38.1%      38.6%      44.2%      44.9%      44.6%
       30%    0.3 |                                 44.2%      52.7%      52.1%      58.0%      60.0%      59.5%
                  | share of CONFIDENT-WRONG caught:
       10%        |                                 11.4%       9.4%      17.4%      15.7%      12.1%      15.7%
       20%        |                                 21.8%      22.0%      34.4%      33.4%      30.5%      33.7%
       30%        |                                 33.4%      32.9%      47.2%      47.0%      47.5%      46.7%

  paired recall differences, 95% CI (document-clustered bootstrap):
   10%     probe - p_true     all-wrong +0.081 [+0.044, +0.120]   confident-wrong +0.044 [+0.000, +0.086]
   10%     probe - cheap_best all-wrong +0.044 [+0.012, +0.076]   confident-wrong +0.063 [+0.024, +0.101]
   10%     probe - pregen     all-wrong +0.035 [+0.004, +0.065]   confident-wrong -0.017 [-0.060, +0.023]
   10%   stacked - probe      all-wrong +0.004 [-0.022, +0.030]   confident-wrong -0.036 [-0.069, -0.003]
   10% two_stage - probe      all-wrong +0.000 [+0.000, +0.000]   confident-wrong +0.000 [+0.000, +0.000]
   20%     probe - p_true     all-wrong +0.120 [+0.076, +0.166]   confident-wrong +0.116 [+0.056, +0.175]
   20%     probe - cheap_best all-wrong +0.061 [+0.024, +0.098]   confident-wrong +0.114 [+0.061, +0.163]
   20%     probe - pregen     all-wrong +0.055 [+0.018, +0.093]   confident-wrong -0.010 [-0.065, +0.039]
   20%   stacked - probe      all-wrong +0.007 [-0.011, +0.025]   confident-wrong -0.029 [-0.058, +0.000]
   20% two_stage - probe      all-wrong +0.004 [-0.006, +0.015]   confident-wrong +0.002 [-0.013, +0.018]
   30%     probe - p_true     all-wrong +0.138 [+0.093, +0.181]   confident-wrong +0.136 [+0.071, +0.201]
   30%     probe - cheap_best all-wrong +0.052 [+0.013, +0.088]   confident-wrong +0.140 [+0.086, +0.196]
   30%     probe - pregen     all-wrong +0.059 [+0.019, +0.096]   confident-wrong -0.002 [-0.058, +0.052]
   30%   stacked - probe      all-wrong +0.021 [+0.006, +0.035]   confident-wrong +0.005 [-0.012, +0.022]
   30% two_stage - probe      all-wrong +0.015 [+0.000, +0.032]   confident-wrong -0.002 [-0.023, +0.019]
```
