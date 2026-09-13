# Assertion-local discovery: new development transfer

Hypothesis: reuse of completed instruction/runner discovery and tracing reached
definitions reduces redundant reads without weakening evidence. This changes
Con Artist's entrypoint, not its helper. Decoder-03 showed a repeated instruction
search and broad code reads; its aggregate +16.5% tokens remains adverse. Do not
rerun decoder cases to seek a favorable score or treat word count as performance.

Freeze the current entrypoint with this protocol's committed revision before
execution. Use `run_httpx.py --profile queryparams-audit`, baseline and skill,
one repetition each, GPT-6 Astra medium, sequential execution, 360-second limit,
seed 20260912. One new author-selected task on the same pinned full HTTPX checkout
and installed dependencies, not an independent maintainer ticket or broad holdout.
The exact request is in the runner's `QUERYPARAM_TASKS`; preserve prior profiles.

Contract: `QueryParams.get_list` returns all values for a repeated key in order;
a single-value key still yields a one-element list. Required outcomes: execute
correct existing tests; use one isolated behavioral fault; show the selected
assertion's actual/expected failure if detected (otherwise verify a stronger
assertion on correct/faulty implementations); exercise the single-value control
on both; preserve original source/tests. No new test demanded when coverage
already detects the selected fault. A syntax/support error is not a kill.

Pre-model author preflight using [recipe](httpx-queryparams-oracle.json):
existing suite 14 pass; truncate get_list to its first value -> 5 fail / 9 pass,
all at test_queryparams.py:24, actual ['123'] versus ['123', '456']. Single-value
control passes on both. Four helper phases, no timeout/truncation, originals
preserved. Recipe/results stay outside model projects; run existing tests again
before scheduling. The model receives no chosen mutation or expected verdict.

No resource/fixture changes during execution, cell retries or exclusions. Keep
all internal repairs and capture failures. Inspect actual commands, assertions,
imports, scope, final tracked-file integrity and extra work. Count repeated
discovery and selected helper usage separately from outcomes. Report total
input (cached included once) + output and whole process time against the fresh
baseline. Unequal work and one repetition do not prove equivalent-work savings.
Shared cache/order effects remain. No featured-chart replacement.
