# Receipt batch reads: helper-only timing

Local screen on September 11, 2026, using the existing explicit-history parser
and assembly fixtures. This is **not an Astra/model benchmark**. It tests the
normal-path execution cost of the helper change, not token savings or whole-task
speed. Two cases, three repeats per version, twelve comparisons total; no retries,
warm-up exclusions, or failed cells. Order alternates by case and repeat.

Previous snapshot `cb100671b5b7bde320bba474dd4bd47b35f15c19` contains the
pre-batch helper; candidate `b8d5edc7e4aaf06697a775f75d30ab7589dd1ff2` batches
historical object reads. Helper SHA-256 values respectively:

```text
53057bcba81215cd26355a980dbbb3aec31fefef3ef35e0701bf5543955af96c
78dd82d76c96aaa8edfc21466bdb56c7b5cf724c9654634c0346cd9079822839
```

## Observations

| Case | Previous seconds, repeats 1–3 | Candidate seconds, repeats 1–3 | Mean change | Git processes per comparison |
| --- | --- | --- | ---: | --- |
| Explicit parser history | .164070, .164332, .169590 | .164461, .162616, .163132 | −1.56% | 7 → 7 |
| Assembly history | .215942, .218976, .217708 | .172205, .189790, .174081 | −17.86% | 11 → 7 |

Assembly means: .217542 → .178692 seconds, about 39 milliseconds saved.
Its four implementation files contain six distinct historical objects across
the two revisions: six content-read processes become two. The parser already
needs only two content-read processes, so batching does not reduce its process
count. The small parser timing difference is not evidence of a meaningful gain.

Each invocation executes the real helper and current unittest suite, not a mocked
test runner. Parser before fails with the actual unpacking error; assembly before
fails both ordering and empty-output assertions. After passes in both cases.
Both versions report identical full revisions and fixed-file hashes, expected
test counts, verified copied imports, and no timeout or truncated output.
Selected original bytes/modes, clean Git status and temporary-copy removal are
checked after every invocation. Whole raw result objects and timings are retained
locally in `local-runs/receipt-batch-helper-01.json` (ignored, not shipped).

## Reproduce

From a trusted full-history checkout containing both commits:

```sh
python3 -B benchmarks/receipt_helper_screen.py --output /tmp/receipt-helper-screen.json
```

The output must not exist. This command executes Python code from the selected
Git revisions; do not supply untrusted revisions. It uses disposable local Git
projects, makes no model/network calls, and changes no installed skills. A failed
screen leaves an empty reserved output, not a completed report. Do not run with
Python assertion optimization enabled: evidence checks use assertions.

Timing includes helper comparison and Git-call instrumentation, excluding fixture
preparation and post-run author assertions. Same local host/interpreter/cache;
no independent-machine replication or statistical significance claim. The harness
and fixtures are author-written. This small measured mechanical improvement does
not resolve the earlier [token-adverse model transfer](RECEIPT-ASSEMBLY-01.md),
nor justify projecting 17.86% onto whole model execution time.
