# 21_error_types_llama_full_finqa

- generated: 2026-10-08T13:27:24
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n_wrong: 2441
- n_confident_wrong: 329
- negatives: confident-correct (n=756)

```
type                  wrong   share    CW   share conf.rate |    probe  P(True)    cheap   pregen
abstention              740   30.3%    14    4.3%      1.9% |   (fewer than 20 confident-wrong)
sign                    208    8.5%    40   12.2%     19.2% |    0.738    0.465    0.475    0.750
scale                    68    2.8%    11    3.3%     16.2% |   (fewer than 20 confident-wrong)
selection_same_row      222    9.1%    32    9.7%     14.4% |    0.733    0.446    0.564    0.754
selection_other         365   15.0%    57   17.3%     15.6% |    0.619    0.504    0.570    0.678
computation             838   34.3%   175   53.2%     20.9% |    0.705    0.441    0.496    0.679
selection (all)         587   24.0%    89   27.1%     15.2% |    0.660    0.483    0.568    0.705
all wrong              2441  100.0%   329  100.0%     13.5% |    0.701    0.469    0.540    0.699
```
