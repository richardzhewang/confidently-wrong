# 20_routing_and_uncertainty_qwen_full_tatqa

- generated: 2026-10-07T14:14:27
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 1138
- bootstrap: document-clustered, paired, 2000 replicates, seed 0

```
[A] AUROC and paired differences (probe minus comparison), 95% CI
  confident(8/8): n=459 wrong=74  probe 0.687 [0.614, 0.760]
    vs best_single   0.629   delta +0.059 [-0.034, +0.118]   P(delta<=0)=0.106
    vs cheap_best    0.642   delta +0.046 [-0.035, +0.124]   P(delta<=0)=0.133
    vs pregen        0.592   delta +0.096 [+0.013, +0.177]   P(delta<=0)=0.013
    vs pregen_cheap  0.652   delta +0.036 [-0.038, +0.115]   P(delta<=0)=0.185
    stacked       0.680   stacked-probe -0.007 [-0.066, +0.051]
  unsure(<8/8): n=67 wrong=52  probe 0.697 [0.523, 0.845]
    vs best_single   0.691   delta +0.006 [-0.244, +0.145]   P(delta<=0)=0.590
    vs cheap_best    0.715   delta -0.018 [-0.207, +0.172]   P(delta<=0)=0.579
    vs pregen        0.683   delta +0.014 [-0.170, +0.199]   P(delta<=0)=0.427
    vs pregen_cheap  0.669   delta +0.028 [-0.116, +0.176]   P(delta<=0)=0.355
    stacked       0.658   stacked-probe -0.040 [-0.136, +0.055]
  full: n=1138 wrong=126  probe 0.732 [0.672, 0.791]
    vs best_single   0.725   delta +0.008 [-0.052, +0.066]   P(delta<=0)=0.400
    vs cheap_best    0.735   delta -0.003 [-0.063, +0.058]   P(delta<=0)=0.549
    vs pregen        0.653   delta +0.079 [+0.019, +0.141]   P(delta<=0)=0.007
    vs pregen_cheap  0.725   delta +0.007 [-0.047, +0.062]   P(delta<=0)=0.406
    stacked       0.752   stacked-probe +0.019 [-0.022, +0.062]

[B] evaluation half: n=571 wrong=70 confident-wrong=38
  capacity  alpha | share of ALL wrong caught:     p_true cheap_best     pregen      probe    stacked  two_stage
       10%    0.0 |                                 30.0%      28.6%      24.3%      35.7%      38.6%      35.7%
       20%    0.6 |                                 51.4%      52.9%      37.1%      51.4%      54.3%      55.7%
       30%    0.6 |                                 64.3%      62.9%      47.1%      60.0%      64.3%      65.7%
                  | share of CONFIDENT-WRONG caught:
       10%        |                                 15.8%      15.8%      10.5%      23.7%      18.4%      23.7%
       20%        |                                 36.8%      31.6%      21.1%      34.2%      36.8%      34.2%
       30%        |                                 44.7%      42.1%      28.9%      44.7%      47.4%      47.4%

  paired recall differences, 95% CI (document-clustered bootstrap):
   10%     probe - p_true     all-wrong +0.057 [-0.112, +0.214]   confident-wrong +0.079 [-0.107, +0.280]
   10%     probe - cheap_best all-wrong +0.071 [-0.041, +0.182]   confident-wrong +0.079 [-0.029, +0.195]
   10%     probe - pregen     all-wrong +0.114 [-0.043, +0.257]   confident-wrong +0.132 [-0.020, +0.298]
   10%   stacked - probe      all-wrong +0.029 [-0.055, +0.117]   confident-wrong -0.053 [-0.162, +0.050]
   10% two_stage - probe      all-wrong +0.000 [+0.000, +0.000]   confident-wrong +0.000 [+0.000, +0.000]
   20%     probe - p_true     all-wrong +0.000 [-0.132, +0.133]   confident-wrong -0.026 [-0.238, +0.179]
   20%     probe - cheap_best all-wrong -0.014 [-0.148, +0.120]   confident-wrong +0.026 [-0.184, +0.231]
   20%     probe - pregen     all-wrong +0.143 [-0.017, +0.290]   confident-wrong +0.132 [+0.000, +0.296]
   20%   stacked - probe      all-wrong +0.029 [-0.048, +0.109]   confident-wrong +0.026 [-0.096, +0.135]
   20% two_stage - probe      all-wrong +0.043 [-0.031, +0.118]   confident-wrong +0.000 [-0.108, +0.107]
   30%     probe - p_true     all-wrong -0.043 [-0.162, +0.077]   confident-wrong +0.000 [-0.182, +0.182]
   30%     probe - cheap_best all-wrong -0.029 [-0.164, +0.104]   confident-wrong +0.026 [-0.189, +0.233]
   30%     probe - pregen     all-wrong +0.129 [-0.015, +0.273]   confident-wrong +0.158 [+0.000, +0.343]
   30%   stacked - probe      all-wrong +0.043 [-0.037, +0.128]   confident-wrong +0.026 [-0.111, +0.162]
   30% two_stage - probe      all-wrong +0.057 [-0.049, +0.169]   confident-wrong +0.026 [-0.156, +0.216]
```
