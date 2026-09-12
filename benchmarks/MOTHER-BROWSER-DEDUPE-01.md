# Mother-in-law browser evidence deduplication

Reviewed September 12, 2026 KST. This is candidate-development evidence, not a
replacement for the published five-case checkpoint.

Revision `948431c` tells rendered-browser QA to retain detailed evidence while
reporting complete compact statuses, and not to reopen the detail file merely to
repeat it. A fresh GPT-6 Astra medium skill session used the same pinned Linux
browser fixture and container as the earlier checkpoint.

## Focused browser result

The session reproduced all three target defects with trusted browser input:

- older success replaced a newer success;
- older failure surfaced after a newer success;
- older success repopulated results after clear.

The nearby normal success, current failure and retry behaviors passed. Input and
focus remained correct, source and dependency inventories were unchanged, and
all owned browser contexts and the browser closed. The runner's compact output
contained every case and cleanup state; the model did not reopen its detailed
JSON evidence after execution.

| Measure | Previous skill | Revision `948431c` | Change |
|---|---:|---:|---:|
| Target defects | 3/3 | 3/3 | preserved |
| Total tokens | 129,874 | 106,372 | -18.1% |
| Elapsed seconds | 100.108 | 105.765 | +5.7% |

Against the frozen baseline, the new browser cell used 85.9% of tokens and 72.7%
of elapsed time. This supports the evidence-deduplication direction for the
focused browser task, but one fresh session does not establish its expected
effect.

## Same-snapshot five-case check

To avoid combining cells from different skill resource hashes, the four Python
skill arms were also rerun once at `948431c`; their frozen baselines were not
rerun. All four retained their required behavioral outcome. Together with the new
browser cell, the equal-task ratios are 88.2% tokens and 68.4% elapsed time
(-11.8% and -31.6%). The token result is worse than the published checkpoint's
84.5%, despite similar commands and smaller or comparable captured output.

Therefore the published graph remains unchanged. The favorable browser cell is
not cherry-picked into older Python cells, and the unfavorable same-snapshot run
is retained. A separately frozen confirmation batch is required before replacing
the checkpoint.
