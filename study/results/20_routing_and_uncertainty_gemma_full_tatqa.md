# 20_routing_and_uncertainty_gemma_full_tatqa

- generated: 2026-10-08T13:28:31
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n: 1138
- bootstrap: document-clustered, paired, 2000 replicates, seed 0

```
[A] AUROC and paired differences (probe minus comparison), 95% CI
  confident(8/8): n=434 wrong=72  probe 0.684 [0.619, 0.751]
    vs best_single   0.593   delta +0.091 [+0.002, +0.164]   P(delta<=0)=0.022
    vs cheap_best    0.602   delta +0.082 [-0.005, +0.163]   P(delta<=0)=0.038
    vs pregen        0.640   delta +0.044 [-0.033, +0.120]   P(delta<=0)=0.125
    vs pregen_cheap  0.596   delta +0.088 [-0.006, +0.174]   P(delta<=0)=0.034
    stacked       0.631   stacked-probe -0.053 [-0.116, +0.006]
  unsure(<8/8): n=152 wrong=114  probe 0.543 [0.430, 0.657]
    vs best_single   0.613   delta -0.070 [-0.212, +0.047]   P(delta<=0)=0.887
    vs cheap_best    0.621   delta -0.078 [-0.209, +0.058]   P(delta<=0)=0.879
    vs pregen        0.468   delta +0.075 [-0.039, +0.197]   P(delta<=0)=0.102
    vs pregen_cheap  0.498   delta +0.045 [-0.070, +0.153]   P(delta<=0)=0.220
    stacked       0.545   stacked-probe +0.002 [-0.042, +0.053]
  full: n=1138 wrong=186  probe 0.733 [0.688, 0.777]
    vs best_single   0.696   delta +0.037 [-0.014, +0.088]   P(delta<=0)=0.080
    vs cheap_best    0.704   delta +0.029 [-0.024, +0.080]   P(delta<=0)=0.141
    vs pregen        0.660   delta +0.073 [+0.023, +0.125]   P(delta<=0)=0.004
    vs pregen_cheap  0.683   delta +0.050 [+0.002, +0.097]   P(delta<=0)=0.021
    stacked       0.714   stacked-probe -0.019 [-0.048, +0.009]

[B] evaluation half: n=571 wrong=104 confident-wrong=37
  capacity  alpha | share of ALL wrong caught:     p_true cheap_best     pregen      probe    stacked  two_stage
       10%    0.1 |                                 22.1%      25.0%      20.2%      27.9%      26.9%      27.9%
       20%    0.0 |                                 42.3%      41.3%      35.6%      49.0%      46.2%      49.0%
       30%    0.6 |                                 56.7%      51.0%      51.0%      60.6%      59.6%      59.6%
                  | share of CONFIDENT-WRONG caught:
       10%        |                                  5.4%       5.4%      16.2%      16.2%      10.8%      16.2%
       20%        |                                 24.3%      13.5%      27.0%      35.1%      29.7%      35.1%
       30%        |                                 40.5%      29.7%      37.8%      45.9%      40.5%      37.8%

  paired recall differences, 95% CI (document-clustered bootstrap):
   10%     probe - p_true     all-wrong +0.058 [-0.064, +0.170]   confident-wrong +0.108 [+0.000, +0.243]
   10%     probe - cheap_best all-wrong +0.029 [-0.087, +0.147]   confident-wrong +0.108 [+0.000, +0.250]
   10%     probe - pregen     all-wrong +0.077 [-0.011, +0.171]   confident-wrong +0.000 [-0.111, +0.108]
   10%   stacked - probe      all-wrong -0.010 [-0.075, +0.059]   confident-wrong -0.054 [-0.146, +0.000]
   10% two_stage - probe      all-wrong +0.000 [-0.026, +0.029]   confident-wrong +0.000 [+0.000, +0.000]
   20%     probe - p_true     all-wrong +0.067 [-0.056, +0.179]   confident-wrong +0.108 [-0.059, +0.263]
   20%     probe - cheap_best all-wrong +0.077 [-0.043, +0.193]   confident-wrong +0.216 [+0.059, +0.387]
   20%     probe - pregen     all-wrong +0.135 [+0.000, +0.257]   confident-wrong +0.081 [-0.111, +0.260]
   20%   stacked - probe      all-wrong -0.029 [-0.066, +0.000]   confident-wrong -0.054 [-0.130, +0.000]
   20% two_stage - probe      all-wrong +0.000 [+0.000, +0.000]   confident-wrong +0.000 [+0.000, +0.000]
   30%     probe - p_true     all-wrong +0.038 [-0.075, +0.142]   confident-wrong +0.054 [-0.133, +0.250]
   30%     probe - cheap_best all-wrong +0.096 [-0.033, +0.221]   confident-wrong +0.162 [-0.057, +0.379]
   30%     probe - pregen     all-wrong +0.096 [-0.043, +0.225]   confident-wrong +0.081 [-0.133, +0.277]
   30%   stacked - probe      all-wrong -0.010 [-0.074, +0.048]   confident-wrong -0.054 [-0.143, +0.000]
   30% two_stage - probe      all-wrong -0.010 [-0.094, +0.078]   confident-wrong -0.081 [-0.207, +0.031]
```
