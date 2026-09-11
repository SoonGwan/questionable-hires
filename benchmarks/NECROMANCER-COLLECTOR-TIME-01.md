# Whole collector timing, not whole agent timing

The excerpt CPU change at 0e3c790 was compared with a16e57d in complete fresh Python
collector processes, including Git commands and JSON serialization. One temporary
Git repository has two actual commits replacing 100,000 old lines with 100,000 new
lines; the current file is 1,100,000 bytes. Each call requests lines 50000:50099.
All six parsed JSON evidence objects are identical and include selected excerpts.
Repository status and the source hash remain unchanged after collection.

Three calls per version alternate order by repeat. Python 3.9.6, shared local host:

| Version | All process seconds | Median seconds |
| --- | --- | ---: |
| a16e57d | 0.426759, 0.426157, 0.428103 | 0.426759 |
| 0e3c790 | 0.343490, 0.332922, 0.334522 | 0.334522 |

The candidate median is about **21.6% lower** for this fixture. Unlike the earlier
function timing, this includes collector startup, blame, show, filtering and
serialization. It still excludes model reasoning, skill loading, tool orchestration
and task verification. It does not establish model token savings, total-memory
bounds, all-repository performance or the overall project objective.

Reproduce with the committed comparison tool (trusted baseline revisions only):

```sh
python3 -B benchmarks/benchmark_history_collector.py --baseline-revision a16e57d
```

The tool creates and cleans only its own temporary fixture, freezes the current
helper bytes before calling either version, checks full evidence equality and
reports all timings. Input SHA-256 is
`cde29c379cb2b3421e49058685ffe928852332f3852c49a99c31a558e4a4f4d5`;
candidate helper SHA-256 is
`be6de59732e8256c1d1994958b4ff7928e6d2801ff0198d64e0bad12fc4412e5`.
Commit identities in generated evidence depend on fixture creation time; comparison
uses one shared fixture within each invocation, not mismatched histories.

A new integration test executes the actual Git comparison and validates complete
evidence matching, source size, resource identity and retained timing samples. It
does not assert a speedup or filter slow samples. All 164 tests pass (20.756 seconds).
Repository validation passes. No skill entrypoint or collector implementation was
changed in this turn; this verifies the scope of the existing implementation gain.
