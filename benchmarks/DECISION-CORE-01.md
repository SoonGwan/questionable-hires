# Decision-core variants: do not promote

Eight fresh Astra medium sessions followed the [frozen protocol](candidates/decision-core/PROTOCOL.md):
four unchanged exposed development cases, shipped versus isolated candidate,
one sample per cell, serial balanced order, no retries or exclusions. Both resource
trees were frozen at `bb6bd5c`. No no-skill arm; this is not superiority evidence.
Raw ignored evidence is under `local-runs/decision-core-01`.

| Case | Shipped tokens | Candidate tokens | Shipped seconds | Candidate seconds |
| --- | ---: | ---: | ---: | ---: |
| formatter-review | 49,302 | 65,000 | 20.880 | 24.055 |
| adapter-justified | 49,894 | 48,510 | 22.691 | 20.338 |
| label-change | 66,537 | 82,135 | 23.673 | 27.618 |
| necessary-state | 87,318 | 83,781 | 69.218 | 49.984 |
| Total | 253,051 | 279,426 | 136.462 | 121.995 |

Total tokens are input (cache included) plus output. The candidate uses **10.4%
more tokens**, with **10.6% less elapsed time**. These sums are not the original
chart's mean-of-task-ratios statistic. One sample per cell, patch rejections and
different verification depth prevent causal attribution. Shorter instruction
files have not established a better cost/outcome tradeoff.

## Behavior and controls

Both Landlord variants recommend replacing the unnecessary registry with a
separate USD formatting function, preserving current numerical behavior and
giving a concrete maintenance example. Both retain the justified adapter for
independently released provider versions. These are static reviews, with no
implementation edits or executable validation claimed.

Both label variants produce the identical Buy → Place order change and no state
redesign; original `git diff --check` succeeds. The candidate has one rejected
patch. Stderr says writing outside the project was rejected; the target is not
available in the retained trace. Correct final files do not prove every attempted
action was within scope.

Both state variants implement per-instance pending state, block duplicate saves,
preserve the result/exception, and clear pending in `finally`. Both originally
run passing unittest artifacts. Shipped uses one test with success, failure and
cancellation subtests; candidate uses three tests. Test counts are not quality
scores. Shipped checks duplicate prevention and retry in all three outcomes;
candidate explicitly checks duplicates on success and retry on success/failure,
but does not check retry after cancellation. Neither explicitly tests independent
instances. Candidate cleanup uses an unbounded cancel/gather; shipped wraps its
cleanup in `wait_for`, which is still not a hard process deadline against a task
that suppresses cancellation. Shipped has one rejected patch with the same
unknown-target limitation. The faster candidate is not equal verification depth.

After all model sessions, author replays of both retained unittest artifacts
pass under an external ten-second subprocess timeout. This checks reproducibility
of the retained files, not model-provided hard containment or fault sensitivity.

## Integrity and disposition

All eight sessions complete without timeout. All sixteen installed resource
instances match the frozen Git blobs, and before/after resource inventories
match. Completed shell commands stay within the project; three discovery commands
return 1 for absent matches, not failed behavior. Final diffs contain only the
requested label edit or state implementation and its new tests; review diffs are
empty. The two rejected patches remain adverse attempted-action evidence, not
discarded observations. Inventory equality cannot establish transient behavior.

Do not promote either decision-core variant. Keep the isolated files for
reproduction and leave shipped skills and the original comparison chart unchanged.
Landlord's pair is costlier overall; Hostage's token total also rises and its
state verification is less complete. Neither supports an efficiency acceptance.
The next substantive improvement must remove demonstrated task work, rather than
repeat compression and remeasure these exposed cases until favorable. Broad
performance improvement across eight skills remains unmet.
