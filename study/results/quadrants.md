# Confidence × correctness quadrants

Confidence = self-consistency (k=8, agreement with greedy answer); 'confident' = 8/8 unless noted. Cells: count (population share — reweighted for subsampled correct class where marked ®).

| condition | n | confident-correct | confident-WRONG | unsure-correct | unsure-wrong |
|---|---|---|---|---|---|
| gemma_full_finqa ® | 3448 | 1280 (58%) | **861 (14%)** | 220 (10%) | 1087 (18%) |
| gemma_full_tatqa ® | 586 | 362 (76%) | **72 (6%)** | 38 (8%) | 114 (10%) |
| llama_full_finqa ® | 3941 | 756 (30%) | **329 (5%)** | 744 (30%) | 2112 (35%) |
| llama_full_tatqa ® | 675 | 263 (50%) | **44 (4%)** | 137 (26%) | 231 (20%) |
| qwen_full_finqa ® | 3339 | 1366 (64%) | **1137 (19%)** | 134 (6%) | 702 (11%) |
| qwen_full_tatqa ® | 526 | 385 (86%) | **74 (7%)** | 15 (3%) | 52 (5%) |

Sensitivity (confident = ≥6/8):

| condition | confident-WRONG share (8/8) | (≥6/8) |
|---|---|---|
| gemma_full_finqa | 14.1% | 19.0% |
| gemma_full_tatqa | 6.3% | 9.8% |
| llama_full_finqa | 5.4% | 11.5% |
| llama_full_tatqa | 3.9% | 7.6% |
| qwen_full_finqa | 18.6% | 22.7% |
| qwen_full_tatqa | 6.5% | 8.2% |
