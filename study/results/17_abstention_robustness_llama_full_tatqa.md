# 17_abstention_robustness_llama_full_tatqa

- generated: 2026-10-08T13:27:18
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/llama_full_tatqa.csv
- scores_header: condition=llama_full_tatqa probe_feature=L21_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- generations_file: study/data/generations_llama_full_tatqa.jsonl
- abstain_rule: no ANSWER: line OR explicit 'not in filing' phrasing (common.is_abstention)
- metric: AUROC (wrong-as-positive); rank-based, no reweighting needed

```
[A] abstention prevalence (full population n=1138):
    wrong answers                  275
    of which abstentions            54  (19.6% of wrong)

    conf>=0.75: confident-wrong   87  abstention-wrongs    2  (2.3%)

    conf>=1.00: confident-wrong   44  abstention-wrongs    1  (2.3%)

[B] are abstention-wrongs trivially detected? (positives = confident abstention-wrongs, negatives = confident-correct)
    conf>=0.75: too few (pos=2, neg=349)
    conf>=1.00: too few (pos=1, neg=263)

[C] headline robustness — confident-stratum AUROC, abstention-wrongs removed from the positive class:
    stratum                        n  wrong   probe    base       Δ
    conf>=0.75 all               436     87   0.683   0.600  +0.082
    conf>=0.75 no-abstain        434     85   0.680   0.600  +0.081
    conf>=1.00 all               307     44   0.708   0.587  +0.122
    conf>=1.00 no-abstain        306     43   0.701   0.577  +0.124
```
