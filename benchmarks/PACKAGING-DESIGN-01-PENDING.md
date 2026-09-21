# Packaging design01 — original sessions completed, review pending

2026-09-21. Frozen protocol: [PACKAGING-DESIGN-01-PROTOCOL.md](PACKAGING-DESIGN-01-PROTOCOL.md).
Launch `d9a9a6e`; skill resources `a545a53`. All three scheduled original sessions
completed without timeout/account limit. The runner is terminal; do not restart.

These are unadjusted process measurements, **not scored task-success results**:

| Arm | Input tokens, cache included | Output tokens | Total | Wall seconds |
| --- | ---: | ---: | ---: | ---: |
| No-skill |74478|1595|76073|59.042|
| Candidate |80367|1580|81947|61.405|
| Prior |87448|1865|89313|66.403|

Candidate costs less than prior but more than no-skill. No causal/general gain
is established: one author-selected task,n=1,fixed order and shared host/cache.
The candidate's original three tool calls show direct source reads and native
observations, **no collector execution or reference read**. Adding the optional
helper therefore has no demonstrated adoption benefit in this task. It remains
an experiment, not a production upgrade. Do not force an unnecessary collector
call merely to obtain adoption on a file that can be read directly.

All original native records and private original sessions are retained locally
under `benchmarks/local-runs/packaging-design-01`, six original tool records per
arm. Private session files are mode0600 and must not be published wholesale.
Initial answer inspection shows each distinguishes original execution from static
proposal reasoning. Final claims alone do not complete evidence review.

Outstanding before scored publication: check every native result and binding,
criterion evidence, full original-vs-CLI output correspondence, usage agreement,
original file/mode and Git/index/resource integrity and scratch cleanup; publish
redacted evidence with the complete frozen manifest and all limitations. Preserve
these original attempts, including failures or gaps discovered during review.
No rerun is authorized as a replacement for missing capture. Featured graphs and
production Landlord remain unchanged; all-eight performance remains unproven.
