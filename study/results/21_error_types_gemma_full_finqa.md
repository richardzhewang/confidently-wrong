# 21_error_types_gemma_full_finqa

- generated: 2026-10-08T13:27:25
- grader: v2 (x1000 scales, strict sign, 2% tol)
- n_wrong: 1948
- n_confident_wrong: 861
- negatives: confident-correct (n=1280)

```
type                  wrong   share    CW   share conf.rate |    probe  P(True)    cheap   pregen
abstention              317   16.3%    90   10.5%     28.4% |    0.835    0.607    0.836    0.873
sign                    211   10.8%   103   12.0%     48.8% |    0.810    0.642    0.609    0.743
scale                    64    3.3%    37    4.3%     57.8% |    0.729    0.718    0.677    0.681
selection_same_row      238   12.2%    93   10.8%     39.1% |    0.735    0.595    0.644    0.700
selection_other         508   26.1%   211   24.5%     41.5% |    0.726    0.667    0.705    0.688
computation             610   31.3%   327   38.0%     53.6% |    0.744    0.593    0.564    0.688
selection (all)         746   38.3%   304   35.3%     40.8% |    0.729    0.645    0.686    0.692
all wrong              1948  100.0%   861  100.0%     44.2% |    0.755    0.624    0.646    0.715
```
