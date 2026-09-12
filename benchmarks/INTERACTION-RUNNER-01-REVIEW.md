# Existing runner: adoption observed, costs mixed

[Frozen protocol](INTERACTION-RUNNER-01-PROTOCOL.md), revision `6a5ff98`.
Both scheduled sessions completed without outer timeout, retries or exclusions.
Original evidence remains in `benchmarks/local-runs/interaction-runner-01/`;
logs require privacy review before publication.

| Arm | Input + output tokens | Process seconds | Shell commands |
| --- | ---: | ---: | ---: |
| Baseline | 103,138 | 50.524 | 5 |
| Mother-in-law | 89,512 | 61.925 | 7 |

Skill uses **13.21% fewer tokens and 22.57% more time**. Input already includes
cached input (baseline 93,952; skill 78,848); reasoning output is not added again.
Single repeat, shared host/cache, explicit invocation and deliberately supplied
runner limit inference. This is neither a broad win nor a causal old/new skill
comparison. Baseline also reuses the runner, so adoption is not unique to the skill.

## Reviewed behavior

Both use actual `Search` with controlled futures and events, exercising sequential
requests, overlapping requests completed in order, and newer-before-older
completion. Both retain the intermediate newest result assertion in the reversed
case, then fail on the actual stale overwrite. Original runner JSON captures
three executed tests, two passes and one intended assertion failure; child exit 1,
`timed_out: false`, `cleanup_complete: true`, `output_truncated: false`.
This is direct original output, unlike the earlier bundle's missing QA output.

Both run `python3 -B tools/check.py --timeout 3 -- python3 -B TEST.py`, with no
self-spawning wrapper in the added test. Baseline retains `test_search_qa.py`;
skill retains `qa_search.py`. Baseline uses async setup/teardown; skill uses a
parameterized sequence with finally cleanup and explicitly checks submitted order
and initial empty state. They cover the same three sequence categories but their
assertions and generated code are not identical. Both cancel owned pending work;
the existing process deadline covers behavior-dependent waits and cleanup.
Browser behavior and cancellation-resistant application behavior are not tested
by these model sessions. Author-side runner tests are separate evidence.

All four original fixture files are byte-identical in both retained projects.
Reviewed commands stay within the project, with no installs or external actions.
The skill's instruction search returns 1 for no AGENTS.md match; this is retained,
not described as a failed QA assertion. Both inspect the runner source. Skill
spends more shell calls on discovery, and its broader local file listing includes
installed skill paths. Final answers preserve the runner command and name the
tested state boundary rather than claiming browser coverage.

## Decision

Keep the candidate's sufficient-existing-runner route: it was followed without
losing the intended failure evidence. Do not claim the edit caused token savings
or fixed earlier capture loss. Do not repeat this unchanged exposed task to chase
a time win. Further optimization should address demonstrated discovery work on
representative project layouts while preserving applicable instruction discovery.
