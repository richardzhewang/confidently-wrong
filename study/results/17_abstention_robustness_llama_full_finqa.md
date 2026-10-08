# 17_abstention_robustness_llama_full_finqa

- generated: 2026-10-08T13:27:18
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/llama_full_finqa.csv
- scores_header: condition=llama_full_finqa probe_feature=L21_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- generations_file: study/data/generations_llama_full.jsonl
- abstain_rule: no ANSWER: line OR explicit 'not in filing' phrasing (common.is_abstention)
- metric: AUROC (wrong-as-positive); rank-based, no reweighting needed

```
[A] abstention prevalence (full population n=6114):
    wrong answers                 2441
    of which abstentions           739  (30.3% of wrong)

    conf>=0.75: confident-wrong  702  abstention-wrongs   50  (7.1%)

    conf>=1.00: confident-wrong  329  abstention-wrongs   14  (4.3%)

[B] are abstention-wrongs trivially detected? (positives = confident abstention-wrongs, negatives = confident-correct)
    conf>=0.75 (pos=50, neg=1200):  probe 0.840   best-baseline 0.857
    conf>=1.00 (pos=14, neg=756):  probe 0.898   best-baseline 0.931

[C] headline robustness — confident-stratum AUROC, abstention-wrongs removed from the positive class:
    stratum                        n  wrong   probe    base       Δ
    conf>=0.75 all              1902    702   0.699   0.569  +0.130
    conf>=0.75 no-abstain       1852    652   0.688   0.554  +0.135
    conf>=1.00 all              1085    329   0.701   0.550  +0.151
    conf>=1.00 no-abstain       1071    315   0.692   0.537  +0.156
```
