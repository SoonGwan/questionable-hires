# Avoid repeated membership scans and unchanged renders

Collector 0e3c790 builds a set of selected line numbers once, rather than scanning
up to 100 requested numbers for every patch line. Neighbor expansion now skips
rows already in the chosen excerpt, avoiding repeated sorting/rendering of an
unchanged selection. Target coverage, full-tail validation, context priority and
the output budget remain unchanged; the preceding memory optimization is retained.

Five local function cases use the same prebuilt 100,000-row patch, default 8,000
character budget, and one/20/100 selected lines, contiguous or separated. Each
case verifies identical output before measurement and after every call. Seven
calls per version alternate order; medians from the reproducible comparison with
a16e57d are below. No model sessions or service calls were performed.

| Selection | Prior seconds | Candidate seconds | Same excerpt characters |
| --- | ---: | ---: | ---: |
| one | 0.082269 | 0.083076 | 293 |
| 20 contiguous | 0.099420 | 0.083173 | 977 |
| 20 separated | 0.104326 | 0.089549 | 5,446 |
| 100 contiguous | 0.182441 | 0.083377 | 3,857 |
| 100 separated | 0.203333 | 0.126497 | 7,994 |

The 100-contiguous case is about 54% faster here; the one-line case is about 1%
slower, essentially unchanged at this measurement scale. These are local function
timings, not a guaranteed speedup for all diffs, an end-to-end collector benchmark,
model token savings or whole-skill superiority. An earlier exploratory run gave
similar medians (one +1.0%, 20 contiguous -15.9%, 20 separated -14.2%, 100 contiguous
-53.9%, 100 separated -37.4%); it was not used to select or exclude cases.

Run the fixed five-case comparison with a trusted local baseline revision:

```sh
python3 -B benchmarks/benchmark_history_excerpt.py --baseline-revision a16e57d
```

The script executes the committed baseline helper, emits all seven timings per
case and fails if evidence changes. Its final reporting includes candidate SHA-256
and Python version; those metadata fields were added after the tabulated run,
without changing measured functions or schedule. Do not run arbitrary untrusted
revisions merely because this is a benchmark.

A durable regression checks 100 overlapping target windows, reversed/duplicate
target order, exact neighboring rows and an insufficient budget. All 20 history
tests and all 163 repository tests pass (18.639 seconds for the full suite).
Repository validation passes. Entrypoint, reference, UI and caller-visible output
contract are unchanged. Overall model/task efficiency remains unproven.
