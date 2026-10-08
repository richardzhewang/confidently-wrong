# 17_abstention_robustness_qwen_full_finqa

- generated: 2026-10-08T13:27:18
- grader: v2 (x1000 scales, strict sign, 2% tol)
- scores_file: study/scores/qwen_full_finqa.csv
- scores_header: condition=qwen_full_finqa probe_feature=L24_ans_mean folds=StratifiedGroupKFold(5,doc) grader=v2
- generations_file: study/data/generations_qwen_full.jsonl
- abstain_rule: no ANSWER: line OR explicit 'not in filing' phrasing (common.is_abstention)
- metric: AUROC (wrong-as-positive); rank-based, no reweighting needed

```
[A] abstention prevalence (full population n=6105):
    wrong answers                 1839
    of which abstentions           181  (9.8% of wrong)

    conf>=0.75: confident-wrong 1384  abstention-wrongs  126  (9.1%)

    conf>=1.00: confident-wrong 1137  abstention-wrongs   97  (8.5%)

[B] are abstention-wrongs trivially detected? (positives = confident abstention-wrongs, negatives = confident-correct)
    conf>=0.75 (pos=126, neg=1443):  probe 0.969   best-baseline 0.944
    conf>=1.00 (pos=97, neg=1366):  probe 0.983   best-baseline 0.941

[C] headline robustness — confident-stratum AUROC, abstention-wrongs removed from the positive class:
    stratum                        n  wrong   probe    base       Δ
    conf>=0.75 all              2827   1384   0.765   0.640  +0.125
    conf>=0.75 no-abstain       2701   1258   0.744   0.609  +0.135
    conf>=1.00 all              2503   1137   0.766   0.615  +0.151
    conf>=1.00 no-abstain       2406   1040   0.746   0.585  +0.161
```
