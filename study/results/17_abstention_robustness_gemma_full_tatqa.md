# 17_abstention_robustness_gemma_full_tatqa

- generated: 2026-10-08T13:27:19
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/gemma_full_tatqa.csv
- scores_header: condition=gemma_full_tatqa probe_feature=L28_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- generations_file: study/data/generations_gemma_full_tatqa.jsonl
- abstain_rule: no ANSWER: line OR explicit 'not in filing' phrasing (common.is_abstention)
- metric: AUROC (wrong-as-positive); rank-based, no reweighting needed

```
[A] abstention prevalence (full population n=1138):
    wrong answers                  186
    of which abstentions            12  (6.5% of wrong)

    conf>=0.75: confident-wrong  112  abstention-wrongs    5  (4.5%)

    conf>=1.00: confident-wrong   72  abstention-wrongs    5  (6.9%)

[B] are abstention-wrongs trivially detected? (positives = confident abstention-wrongs, negatives = confident-correct)
    conf>=0.75 (pos=5, neg=386):  probe 0.719   best-baseline 0.723
    conf>=1.00 (pos=5, neg=362):  probe 0.730   best-baseline 0.723

[C] headline robustness — confident-stratum AUROC, abstention-wrongs removed from the positive class:
    stratum                        n  wrong   probe    base       Δ
    conf>=0.75 all               498    112   0.697   0.637  +0.059
    conf>=0.75 no-abstain        493    107   0.696   0.635  +0.060
    conf>=1.00 all               434     72   0.684   0.593  +0.091
    conf>=1.00 no-abstain        429     67   0.680   0.586  +0.094
```
