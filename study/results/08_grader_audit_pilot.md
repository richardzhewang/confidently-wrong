# 08_grader_audit (LLM-judge audit of the grader)

- script: study/code/08_grader_audit.py
- judge: gpt-5.4-mini
- data: study/data/pilot/generations_qwen_finqa_pilot.jsonl (800 FinQA questions, Qwen3-8B answers, grader v2 labels)
- sample: 60 graded-correct + 60 graded-incorrect answers, numpy seed 0
- per-item verdicts: study/data/pilot/grader_audit.jsonl

Console record of the run:

```
graded-correct: judge agrees 54/60 (90.0%)
   disagreement idx=555: gold=0.0175 pred=1.75
   disagreement idx=294: gold=0.56396 pred=56.4
   disagreement idx=212: gold=0.02231 pred=2.23
   disagreement idx=56: gold=0.01543 pred=1.54
   disagreement idx=222: gold=3.95 pred=395
   disagreement idx=63: gold=0.13393 pred=13.40
graded-incorrect: judge agrees 56/60 (93.3%)
   disagreement idx=648: gold=-0.16577 pred=16.58
   disagreement idx=579: gold=0.5183 pred=53.16
   disagreement idx=485: gold=148.27586 pred=148275862
   disagreement idx=355: gold=0.70705 pred=-70.7
```
