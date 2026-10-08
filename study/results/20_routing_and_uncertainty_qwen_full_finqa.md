# 20_routing_and_uncertainty_qwen_full_finqa

- generated: 2026-10-07T14:12:10
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 6105
- bootstrap: document-clustered, paired, 2000 replicates, seed 0

```
[A] AUROC and paired differences (probe minus comparison), 95% CI
  confident(8/8): n=2503 wrong=1137  probe 0.766 [0.746, 0.786]
    vs best_single   0.615   delta +0.151 [+0.125, +0.178]   P(delta<=0)=0.000
    vs cheap_best    0.646   delta +0.120 [+0.094, +0.146]   P(delta<=0)=0.000
    vs pregen        0.727   delta +0.039 [+0.017, +0.061]   P(delta<=0)=0.001
    vs pregen_cheap  0.726   delta +0.040 [+0.016, +0.062]   P(delta<=0)=0.001
    stacked       0.761   stacked-probe -0.005 [-0.014, +0.003]
  unsure(<8/8): n=836 wrong=702  probe 0.722 [0.677, 0.763]
    vs best_single   0.669   delta +0.053 [-0.002, +0.106]   P(delta<=0)=0.030
    vs cheap_best    0.655   delta +0.067 [+0.012, +0.119]   P(delta<=0)=0.007
    vs pregen        0.620   delta +0.102 [+0.042, +0.166]   P(delta<=0)=0.001
    vs pregen_cheap  0.677   delta +0.045 [-0.012, +0.100]   P(delta<=0)=0.068
    stacked       0.726   stacked-probe +0.004 [-0.019, +0.026]
  full: n=6105 wrong=1839  probe 0.786 [0.772, 0.799]
    vs best_single   0.692   delta +0.094 [+0.076, +0.112]   P(delta<=0)=0.000
    vs cheap_best    0.705   delta +0.080 [+0.063, +0.098]   P(delta<=0)=0.000
    vs pregen        0.723   delta +0.062 [+0.046, +0.079]   P(delta<=0)=0.000
    vs pregen_cheap  0.754   delta +0.031 [+0.016, +0.047]   P(delta<=0)=0.000
    stacked       0.794   stacked-probe +0.008 [+0.002, +0.015]

[B] evaluation half: n=3046 wrong=931 confident-wrong=579
  capacity  alpha | share of ALL wrong caught:     p_true cheap_best     pregen      probe    stacked  two_stage
       10%    0.2 |                                 21.6%      22.0%      22.1%      26.6%      25.7%      26.9%
       20%    0.2 |                                 37.3%      38.1%      37.9%      44.8%      45.3%      45.2%
       30%    0.4 |                                 49.8%      50.7%      51.8%      58.0%      59.4%      58.3%
                  | share of CONFIDENT-WRONG caught:
       10%        |                                 10.2%      12.4%      21.9%      23.7%      15.4%      22.6%
       20%        |                                 22.6%      24.7%      37.8%      40.1%      37.0%      38.3%
       30%        |                                 35.4%      38.2%      49.2%      51.6%      50.4%      50.3%

  paired recall differences, 95% CI (document-clustered bootstrap):
   10%     probe - p_true     all-wrong +0.050 [+0.013, +0.088]   confident-wrong +0.135 [+0.096, +0.173]
   10%     probe - cheap_best all-wrong +0.046 [+0.011, +0.082]   confident-wrong +0.112 [+0.073, +0.150]
   10%     probe - pregen     all-wrong +0.045 [+0.010, +0.078]   confident-wrong +0.017 [-0.023, +0.057]
   10%   stacked - probe      all-wrong -0.010 [-0.040, +0.020]   confident-wrong -0.083 [-0.117, -0.050]
   10% two_stage - probe      all-wrong +0.002 [-0.008, +0.013]   confident-wrong -0.010 [-0.023, +0.002]
   20%     probe - p_true     all-wrong +0.075 [+0.034, +0.116]   confident-wrong +0.174 [+0.126, +0.221]
   20%     probe - cheap_best all-wrong +0.067 [+0.026, +0.105]   confident-wrong +0.154 [+0.108, +0.202]
   20%     probe - pregen     all-wrong +0.069 [+0.030, +0.105]   confident-wrong +0.022 [-0.027, +0.070]
   20%   stacked - probe      all-wrong +0.005 [-0.015, +0.025]   confident-wrong -0.031 [-0.054, -0.009]
   20% two_stage - probe      all-wrong +0.004 [-0.010, +0.018]   confident-wrong -0.017 [-0.033, -0.003]
   30%     probe - p_true     all-wrong +0.082 [+0.041, +0.123]   confident-wrong +0.162 [+0.108, +0.214]
   30%     probe - cheap_best all-wrong +0.073 [+0.033, +0.111]   confident-wrong +0.135 [+0.083, +0.183]
   30%     probe - pregen     all-wrong +0.062 [+0.022, +0.101]   confident-wrong +0.024 [-0.026, +0.074]
   30%   stacked - probe      all-wrong +0.014 [-0.002, +0.031]   confident-wrong -0.012 [-0.028, +0.005]
   30% two_stage - probe      all-wrong +0.003 [-0.018, +0.026]   confident-wrong -0.014 [-0.038, +0.012]
```
