# Skip hunk regex work for ordinary patch rows

The selected excerpt parser now checks the literal `@@ -` prefix before invoking
the unchanged complete hunk-header regex. Every header accepted previously has
this prefix. Other rows still traverse the existing data/count validation, so this
does not skip parsing patch data, malformed tails or unselected regions.

Baseline e9d2476; candidate helper SHA-256
`d7e624c01cb6d2dd6367efa8a0080bef7da8cd29391281116cb5c2602e712c08`.
Existing benchmark_history_excerpt.py, Python 3.9.6, seven alternating calls per
version in each of five cases. Complete excerpt equality is checked each time.

| Targets | Baseline median seconds | Candidate median seconds |
| --- | ---: | ---: |
| One | 0.083112 | 0.056037 |
| 20 nearby | 0.082598 | 0.056311 |
| 20 distant | 0.089126 | 0.060993 |
| 100 nearby | 0.082552 | 0.056159 |
| 100 distant | 0.085634 | 0.058901 |

Local function time is approximately 31–33% lower in these cases. This is not a
model token saving. No model execution or instruction change was made.

## Complete collector

Existing benchmark_history_collector.py against e9d2476: actual disposable Git
history, 1,100,000-byte current file, lines 50000:50099, three alternating process
calls per version, identical complete JSON, source/status unchanged.
Input SHA-256: cde29c379cb2b3421e49058685ffe928852332f3852c49a99c31a558e4a4f4d5.

Baseline seconds: 0.326991625, 0.326991625, 0.328171458.
Candidate seconds: 0.275184458, 0.276226125, 0.274765000.
Medians: 0.326992 versus 0.275184, approximately 15.8% lower complete process time.
Full test workloads were started only after this timing finished. This one local
fixture does not establish session performance, memory savings or broad superiority.

The added header-gate regression preserves a context row containing header-like
text and rejects malformed prefixes, counts and endings. Existing every-budget
render equivalence, deletion/context/Unicode, malformed-tail and Git safety checks
remain; no test is weakened to accommodate the optimization.

All 167 repository tests pass in 21.163 seconds. Repository validation and diff
checks pass. Broad eight-skill model efficiency remains unproven.
