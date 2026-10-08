# 21_error_types_qwen_full_finqa

- generated: 2026-10-08T13:27:23
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n_wrong: 1839
- n_confident_wrong: 1137
- negatives: confident-correct (n=1366)

```
type                  wrong   share    CW   share conf.rate |    probe  P(True)    cheap   pregen
abstention              181    9.8%    97    8.5%     53.6% |    0.983    0.941    0.959    0.884
sign                    188   10.2%   130   11.4%     69.1% |    0.757    0.581    0.553    0.702
scale                    65    3.5%    45    4.0%     69.2% |    0.720    0.689    0.731    0.717
selection_same_row      244   13.3%   144   12.7%     59.0% |    0.742    0.660    0.669    0.710
selection_other         491   26.7%   286   25.2%     58.2% |    0.773    0.634    0.693    0.729
computation             670   36.4%   435   38.3%     64.9% |    0.728    0.518    0.558    0.704
selection (all)         735   40.0%   430   37.8%     58.5% |    0.763    0.643    0.685    0.723
all wrong              1839  100.0%  1137  100.0%     61.8% |    0.766    0.615    0.646    0.727
```
