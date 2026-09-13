# Frozen duplicate-header equality audit

Use unchanged full HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177` and the
existing preinstalled interpreter. Candidate Con Artist resources: `400c7c3`,
including compact collector output and direct-read/optional-collector routing.
This is an author-selected different boundary in an already-exposed project,
not an independent holdout, maintainer ticket or all-eight confirmation.

The model-visible `header-equality-audit` task fixes the unchanged
tests/models/test_headers.py suite and pytest options, requests a single isolated
duplicate-multiplicity fault, same-process copied import provenance, two normal
controls on both versions, original preservation and owned-copy cleanup.
If coverage misses the fault, the same stronger assertion must pass correct code
and fail faulty code with relevant actual/expected values. No retained artifacts,
production fix, warning-policy change, installation or network are requested.

Author [oracle preflight](httpx-header-equality-oracle.json), not supplied to
model sessions: replacing sorted-list equality with set equality leaves all
**27 existing tests passing on both versions**. Comparing two identical repeated
pairs with one pair passes the stronger inequality assertion on correct code;
faulty code gives **AssertionError: actual_equal True, expected_equal False**.
Reordered/case-varied distinct pairs compare equal and differing values compare
unequal on both versions. All four checks verify copied imports, finish without
timeout/truncation, remove owned copies and leave upstream clean. This isolated
fault is not a claim that current upstream production equality is broken.

Freeze before execution: two fresh serial Astra medium sessions, one baseline
and one skill, seed 20260912 (skill first), 360 seconds each. No changes to skill
resources or task, author test workloads, retries or exclusions during timing.
Stop scheduling on account limits; preserve adverse/unequal/capture outcomes.
Review native assertions, provenance, original integrity and cleanup before
reporting input (cached included once) + output and process wall time. n=1,
shared host/cache and task selection prohibit generalizing a percentage win.
Existing featured results stay tied to their original revisions.

```sh
python3 -B benchmarks/run_httpx.py \
  --source /tmp/qh-httpx-preflight.3Slnqw/httpx \
  --python /tmp/qh-httpx-preflight.3Slnqw/venv/bin/python \
  --profile header-equality-audit --arms baseline skill --repeats 1 \
  --skill-revision 400c7c3 --output benchmarks/local-runs/httpx-header-equality-01
```

These paths identify the existing local environment, not portable installation
instructions. Runner repeats native correct-code preflight before scheduling.
