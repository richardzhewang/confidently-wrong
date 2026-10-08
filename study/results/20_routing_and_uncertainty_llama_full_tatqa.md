# 20_routing_and_uncertainty_llama_full_tatqa

- generated: 2026-10-07T14:14:56
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 1138
- bootstrap: document-clustered, paired, 2000 replicates, seed 0

```
[A] AUROC and paired differences (probe minus comparison), 95% CI
  confident(8/8): n=307 wrong=44  probe 0.708 [0.620, 0.795]
    vs best_single   0.587   delta +0.122 [-0.011, +0.205]   P(delta<=0)=0.039
    vs cheap_best    0.617   delta +0.091 [-0.026, +0.208]   P(delta<=0)=0.058
    vs pregen        0.613   delta +0.095 [-0.009, +0.208]   P(delta<=0)=0.041
    vs pregen_cheap  0.664   delta +0.044 [-0.044, +0.140]   P(delta<=0)=0.163
    stacked       0.693   stacked-probe -0.015 [-0.081, +0.056]
  unsure(<8/8): n=368 wrong=231  probe 0.658 [0.600, 0.716]
    vs best_single   0.679   delta -0.021 [-0.095, +0.049]   P(delta<=0)=0.702
    vs cheap_best    0.692   delta -0.034 [-0.108, +0.041]   P(delta<=0)=0.793
    vs pregen        0.558   delta +0.100 [+0.036, +0.166]   P(delta<=0)=0.002
    vs pregen_cheap  0.675   delta -0.017 [-0.082, +0.049]   P(delta<=0)=0.663
    stacked       0.699   stacked-probe +0.041 [+0.006, +0.077]
  full: n=1138 wrong=275  probe 0.751 [0.715, 0.787]
    vs best_single   0.726   delta +0.025 [-0.023, +0.072]   P(delta<=0)=0.142
    vs cheap_best    0.758   delta -0.007 [-0.051, +0.038]   P(delta<=0)=0.621
    vs pregen        0.648   delta +0.103 [+0.062, +0.146]   P(delta<=0)=0.000
    vs pregen_cheap  0.742   delta +0.009 [-0.030, +0.048]   P(delta<=0)=0.302
    stacked       0.781   stacked-probe +0.030 [+0.007, +0.054]

[B] evaluation half: n=571 wrong=146 confident-wrong=20
  capacity  alpha | share of ALL wrong caught:     p_true cheap_best     pregen      probe    stacked  two_stage
       10%    1.0 |                                 24.0%      25.3%      17.8%      25.3%      28.1%      25.3%
       20%    0.5 |                                 37.0%      39.0%      30.8%      42.5%      43.2%      43.8%
       30%    0.4 |                                 52.1%      53.4%      43.8%      57.5%      59.6%      56.8%
                  | share of CONFIDENT-WRONG caught:
       10%        |                                 20.0%       5.0%      15.0%      15.0%      20.0%       5.0%
       20%        |                                 20.0%      10.0%      20.0%      20.0%      25.0%      20.0%
       30%        |                                 30.0%      30.0%      35.0%      40.0%      35.0%      25.0%

  paired recall differences, 95% CI (document-clustered bootstrap):
   10%     probe - p_true     all-wrong +0.014 [-0.063, +0.094]   confident-wrong -0.050 [-0.174, +0.000]
   10%     probe - cheap_best all-wrong +0.000 [-0.082, +0.083]   confident-wrong +0.100 [+0.000, +0.250]
   10%     probe - pregen     all-wrong +0.075 [-0.007, +0.157]   confident-wrong +0.000 [-0.238, +0.250]
   10%   stacked - probe      all-wrong +0.027 [-0.040, +0.090]   confident-wrong +0.050 [+0.000, +0.167]
   10% two_stage - probe      all-wrong +0.000 [-0.083, +0.082]   confident-wrong -0.100 [-0.250, +0.000]
   20%     probe - p_true     all-wrong +0.055 [-0.050, +0.160]   confident-wrong +0.000 [-0.143, +0.150]
   20%     probe - cheap_best all-wrong +0.034 [-0.070, +0.141]   confident-wrong +0.100 [+0.000, +0.250]
   20%     probe - pregen     all-wrong +0.116 [+0.029, +0.207]   confident-wrong +0.000 [-0.250, +0.250]
   20%   stacked - probe      all-wrong +0.007 [-0.054, +0.069]   confident-wrong +0.050 [+0.000, +0.174]
   20% two_stage - probe      all-wrong +0.014 [-0.055, +0.083]   confident-wrong +0.000 [+0.000, +0.000]
   30%     probe - p_true     all-wrong +0.055 [-0.073, +0.179]   confident-wrong +0.100 [-0.091, +0.312]
   30%     probe - cheap_best all-wrong +0.041 [-0.071, +0.158]   confident-wrong +0.100 [+0.000, +0.261]
   30%     probe - pregen     all-wrong +0.137 [+0.034, +0.237]   confident-wrong +0.050 [-0.211, +0.316]
   30%   stacked - probe      all-wrong +0.021 [-0.031, +0.076]   confident-wrong -0.050 [-0.167, +0.000]
   30% two_stage - probe      all-wrong -0.007 [-0.068, +0.058]   confident-wrong -0.150 [-0.333, +0.000]
```
