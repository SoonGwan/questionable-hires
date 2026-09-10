# Generated descriptive tables

Rebuilt by `benchmarks/aggregate.py`. All raw values are in `aggregate.json`. No confidence intervals or dollar billing estimates.

## Normalized resource metrics

Equal-weight mean of task mean ratios. Brackets show task-ratio min–max, not confidence intervals.

| Metric | Baseline | Control | Skill | Tasks / complete blocks |
| --- | ---: | ---: | ---: | ---: |
| input_tokens | 100.0% [100.0, 100.0] | 111.8% [86.9, 142.1] | 111.3% [98.7, 133.5] | 8 / 24 |
| cached_input_tokens | 100.0% [100.0, 100.0] | 113.5% [88.9, 153.2] | 110.8% [98.4, 130.6] | 8 / 24 |
| output_tokens | 100.0% [100.0, 100.0] | 135.5% [100.1, 187.0] | 130.0% [115.2, 167.5] | 8 / 24 |
| total_tokens | 100.0% [100.0, 100.0] | 111.9% [87.3, 142.4] | 111.5% [98.9, 133.7] | 8 / 24 |
| elapsed_seconds | 100.0% [100.0, 100.0] | 125.1% [93.6, 168.1] | 117.6% [107.5, 127.3] | 8 / 24 |
| changed_loc | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 2 / 6 |

## Raw values by task and arm

Arithmetic mean ± sample SD over n=3; all observed values, including any censored termination times. LOC is implementation-only churn.

| Task | Arm | Total tokens | Wall seconds | Production / test changed LOC (mean) |
| --- | --- | ---: | ---: | ---: |
| boundary-fix | baseline | 78552.67 ± 723.58 (n=3) | 31.18 ± 1.94 (n=3) | 2.00 / 2.00 |
| boundary-fix | control | 79150.00 ± 113.05 (n=3) | 29.18 ± 1.15 (n=3) | 2.00 / 2.00 |
| boundary-fix | skill | 89756.33 ± 10331.85 (n=3) | 33.50 ± 2.85 (n=3) | 2.00 / 2.00 |
| formatter-review | baseline | 51614.67 ± 8956.08 (n=3) | 21.07 ± 3.33 (n=3) | N/A |
| formatter-review | control | 73505.67 ± 8918.70 (n=3) | 35.42 ± 3.02 (n=3) | N/A |
| formatter-review | skill | 60621.67 ± 9813.24 (n=3) | 24.46 ± 1.68 (n=3) | N/A |
| history-active | baseline | 63135.00 ± 548.75 (n=3) | 25.82 ± 1.53 (n=3) | N/A |
| history-active | control | 68182.00 ± 9669.20 (n=3) | 33.13 ± 3.00 (n=3) | N/A |
| history-active | skill | 67180.00 ± 168.57 (n=3) | 30.72 ± 1.66 (n=3) | N/A |
| label-change | baseline | 62177.00 ± 64.13 (n=3) | 23.47 ± 3.18 (n=3) | 2.00 / 0.00 |
| label-change | control | 68132.00 ± 8746.66 (n=3) | 29.59 ± 5.34 (n=3) | 2.00 / 0.00 |
| label-change | skill | 83114.00 ± 277.14 (n=3) | 29.87 ± 1.15 (n=3) | 2.00 / 0.00 |
| persistence-test | baseline | 73936.33 ± 8773.05 (n=3) | 38.40 ± 2.90 (n=3) | N/A |
| persistence-test | control | 90646.00 ± 9179.01 (n=3) | 49.88 ± 3.01 (n=3) | N/A |
| persistence-test | skill | 79249.00 ± 9648.21 (n=3) | 46.75 ± 3.93 (n=3) | N/A |
| rolling-schema | baseline | 73969.00 ± 9074.37 (n=3) | 34.93 ± 2.22 (n=3) | N/A |
| rolling-schema | control | 74526.33 ± 9006.52 (n=3) | 41.33 ± 2.72 (n=3) | N/A |
| rolling-schema | skill | 78617.00 ± 9575.87 (n=3) | 39.52 ± 2.61 (n=3) | N/A |
| search-diagnosis | baseline | 79353.00 ± 314.91 (n=3) | 44.58 ± 0.86 (n=3) | N/A |
| search-diagnosis | control | 69286.67 ± 9379.45 (n=3) | 52.62 ± 2.19 (n=3) | N/A |
| search-diagnosis | skill | 85274.67 ± 1709.24 (n=3) | 51.06 ± 3.13 (n=3) | N/A |
| search-order | baseline | 69088.33 ± 9483.38 (n=3) | 40.76 ± 4.76 (n=3) | N/A |
| search-order | control | 85714.33 ± 9433.89 (n=3) | 48.16 ± 2.25 (n=3) | N/A |
| search-order | skill | 68350.00 ± 289.50 (n=3) | 49.49 ± 5.54 (n=3) | N/A |

## Absolute quality and execution

Strict success requires completed execution, all three case criteria, and scope pass. Unknown is not success.

| Arm | Strict success | Scope pass | Scope fail / unknown | Observed regressions | Completed / timeout |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | 19/24 (79.2%) | 24/24 | 0 / 0 | 0 | 24 / 0 |
| control | 16/24 (66.7%) | 21/24 | 3 / 0 | 0 | 24 / 0 |
| skill | 18/24 (75.0%) | 20/24 | 0 / 4 | 0 | 24 / 0 |
