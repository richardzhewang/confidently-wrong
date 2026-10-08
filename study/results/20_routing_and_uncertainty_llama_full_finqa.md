# 20_routing_and_uncertainty_llama_full_finqa

- generated: 2026-10-07T14:13:08
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 6114
- bootstrap: document-clustered, paired, 2000 replicates, seed 0

```
[A] AUROC and paired differences (probe minus comparison), 95% CI
  confident(8/8): n=1085 wrong=329  probe 0.701 [0.663, 0.739]
    vs best_single   0.550   delta +0.151 [+0.098, +0.201]   P(delta<=0)=0.000
    vs cheap_best    0.540   delta +0.161 [+0.110, +0.211]   P(delta<=0)=0.000
    vs pregen        0.699   delta +0.003 [-0.035, +0.041]   P(delta<=0)=0.452
    vs pregen_cheap  0.657   delta +0.044 [+0.003, +0.085]   P(delta<=0)=0.018
    stacked       0.671   stacked-probe -0.030 [-0.050, -0.010]
  unsure(<8/8): n=2856 wrong=2112  probe 0.730 [0.709, 0.752]
    vs best_single   0.680   delta +0.050 [+0.025, +0.076]   P(delta<=0)=0.000
    vs cheap_best    0.711   delta +0.019 [-0.005, +0.045]   P(delta<=0)=0.064
    vs pregen        0.640   delta +0.090 [+0.064, +0.117]   P(delta<=0)=0.000
    vs pregen_cheap  0.731   delta -0.001 [-0.023, +0.023]   P(delta<=0)=0.507
    stacked       0.755   stacked-probe +0.025 [+0.013, +0.036]
  full: n=6114 wrong=2441  probe 0.764 [0.751, 0.777]
    vs best_single   0.705   delta +0.059 [+0.042, +0.072]   P(delta<=0)=0.000
    vs cheap_best    0.749   delta +0.016 [+0.000, +0.031]   P(delta<=0)=0.025
    vs pregen        0.684   delta +0.080 [+0.064, +0.096]   P(delta<=0)=0.000
    vs pregen_cheap  0.773   delta -0.009 [-0.022, +0.005]   P(delta<=0)=0.882
    stacked       0.792   stacked-probe +0.028 [+0.021, +0.035]

[B] evaluation half: n=3036 wrong=1200 confident-wrong=149
  capacity  alpha | share of ALL wrong caught:     p_true cheap_best     pregen      probe    stacked  two_stage
       10%    0.7 |                                 21.2%      22.1%      17.6%      21.5%      22.2%      22.8%
       20%    0.8 |                                 35.8%      37.6%      32.6%      37.9%      39.7%      39.7%
       30%    0.6 |                                 47.8%      51.2%      45.4%      51.2%      54.1%      53.7%
                  | share of CONFIDENT-WRONG caught:
       10%        |                                  2.0%       4.7%      16.1%      10.7%       1.3%       6.0%
       20%        |                                  6.7%      11.4%      29.5%      25.5%       5.4%      16.1%
       30%        |                                 12.1%      15.4%      42.3%      35.6%      19.5%      30.9%

  paired recall differences, 95% CI (document-clustered bootstrap):
   10%     probe - p_true     all-wrong +0.003 [-0.026, +0.032]   confident-wrong +0.087 [+0.034, +0.149]
   10%     probe - cheap_best all-wrong -0.006 [-0.034, +0.023]   confident-wrong +0.060 [+0.007, +0.116]
   10%     probe - pregen     all-wrong +0.039 [+0.010, +0.069]   confident-wrong -0.054 [-0.122, +0.012]
   10%   stacked - probe      all-wrong +0.008 [-0.020, +0.035]   confident-wrong -0.094 [-0.156, -0.042]
   10% two_stage - probe      all-wrong +0.013 [-0.009, +0.035]   confident-wrong -0.047 [-0.098, +0.000]
   20%     probe - p_true     all-wrong +0.022 [-0.013, +0.058]   confident-wrong +0.188 [+0.107, +0.274]
   20%     probe - cheap_best all-wrong +0.003 [-0.031, +0.039]   confident-wrong +0.141 [+0.063, +0.224]
   20%     probe - pregen     all-wrong +0.053 [+0.018, +0.088]   confident-wrong -0.040 [-0.127, +0.053]
   20%   stacked - probe      all-wrong +0.018 [-0.010, +0.045]   confident-wrong -0.201 [-0.278, -0.132]
   20% two_stage - probe      all-wrong +0.018 [-0.012, +0.047]   confident-wrong -0.094 [-0.164, -0.027]
   30%     probe - p_true     all-wrong +0.035 [-0.001, +0.072]   confident-wrong +0.235 [+0.143, +0.331]
   30%     probe - cheap_best all-wrong +0.000 [-0.035, +0.034]   confident-wrong +0.201 [+0.116, +0.294]
   30%     probe - pregen     all-wrong +0.058 [+0.021, +0.097]   confident-wrong -0.067 [-0.155, +0.019]
   30%   stacked - probe      all-wrong +0.028 [+0.008, +0.048]   confident-wrong -0.161 [-0.236, -0.099]
   30% two_stage - probe      all-wrong +0.024 [+0.002, +0.047]   confident-wrong -0.047 [-0.104, +0.007]
```
