# 17_abstention_robustness_qwen_full_tatqa

- generated: 2026-10-08T13:27:18
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/qwen_full_tatqa.csv
- scores_header: condition=qwen_full_tatqa probe_feature=L24_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- generations_file: study/data/generations_qwen_full_tatqa.jsonl
- abstain_rule: no ANSWER: line OR explicit 'not in filing' phrasing (common.is_abstention)
- metric: AUROC (wrong-as-positive); rank-based, no reweighting needed

```
[A] abstention prevalence (full population n=1138):
    wrong answers                  126
    of which abstentions            10  (7.9% of wrong)

    conf>=0.75: confident-wrong   93  abstention-wrongs    4  (4.3%)

    conf>=1.00: confident-wrong   74  abstention-wrongs    3  (4.1%)

[B] are abstention-wrongs trivially detected? (positives = confident abstention-wrongs, negatives = confident-correct)
    conf>=0.75: too few (pos=4, neg=392)
    conf>=1.00: too few (pos=3, neg=385)

[C] headline robustness — confident-stratum AUROC, abstention-wrongs removed from the positive class:
    stratum                        n  wrong   probe    base       Δ
    conf>=0.75 all               485     93   0.710   0.667  +0.043
    conf>=0.75 no-abstain        481     89   0.698   0.660  +0.038
    conf>=1.00 all               459     74   0.687   0.629  +0.059
    conf>=1.00 no-abstain        456     71   0.675   0.622  +0.053
```
