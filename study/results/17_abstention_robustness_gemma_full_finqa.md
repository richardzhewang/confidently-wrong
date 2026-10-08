# 17_abstention_robustness_gemma_full_finqa

- generated: 2026-10-08T13:27:19
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/gemma_full_finqa.csv
- scores_header: condition=gemma_full_finqa probe_feature=L28_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- generations_file: study/data/generations_gemma_full.jsonl
- abstain_rule: no ANSWER: line OR explicit 'not in filing' phrasing (common.is_abstention)
- metric: AUROC (wrong-as-positive); rank-based, no reweighting needed

```
[A] abstention prevalence (full population n=6110):
    wrong answers                 1948
    of which abstentions           310  (15.9% of wrong)

    conf>=0.75: confident-wrong 1162  abstention-wrongs  109  (9.4%)

    conf>=1.00: confident-wrong  861  abstention-wrongs   90  (10.5%)

[B] are abstention-wrongs trivially detected? (positives = confident abstention-wrongs, negatives = confident-correct)
    conf>=0.75 (pos=109, neg=1412):  probe 0.826   best-baseline 0.836
    conf>=1.00 (pos=90, neg=1280):  probe 0.835   best-baseline 0.817

[C] headline robustness — confident-stratum AUROC, abstention-wrongs removed from the positive class:
    stratum                        n  wrong   probe    base       Δ
    conf>=0.75 all              2574   1162   0.755   0.641  +0.114
    conf>=0.75 no-abstain       2465   1053   0.748   0.644  +0.103
    conf>=1.00 all              2141    861   0.755   0.624  +0.131
    conf>=1.00 no-abstain       2051    771   0.746   0.626  +0.120
```
