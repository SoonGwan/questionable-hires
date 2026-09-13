# Frozen real-code URL representation audit

Use full clean HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177` at the existing
local checkout and its preinstalled interpreter. Con Artist resources freeze at
`1a75a03` (including assertion-helper guidance and same-process prechecks).
No production source or tests are seeded/changed for model input. This is a new
author-selected task in an already-exposed upstream project, not a maintainer
ticket, independent holdout or all-eight confirmation.

The `url-repr-audit` profile requests the same existing 91-test selection on
correct and faulty implementations: tests/models/test_url.py plus
tests/client/test_auth.py::test_auth_hidden_url. The task fixes pytest options,
requires copied-implementation provenance in check processes, username-only and
no-userinfo controls on both versions, removal of owned copies, preserved
originals and actual detecting assertion evidence. No stronger/new test is needed
if existing coverage detects the fault; no retained report is required. Only
synthetic example credentials and local execution are permitted.

Preflight [oracle recipe](httpx-url-repr-oracle.json) runs four project-local copied
checks. Original suite: **91 pass**. Omitting URL.__repr__'s password-masking
assignment: **1 failure / 90 pass**, actual expected masked URL versus observed
example-password at tests/client/test_auth.py:307. Both normal URL controls pass
against original and faulty implementations. Each phase verifies copied
httpx._urls import; no timeouts or output truncation, original checkout remains
clean. The oracle recipe/outcome is not supplied to evaluated agents. This is
not discovery of a production vulnerability: the deliberate fault is isolated.

Run two fresh serial Astra medium sessions, baseline and skill once, fixed
seed 20260912 (skill first), 360-second limit each. No candidate/fixture edits,
author test workloads, retries or exclusions during model timing. Preserve both
cells, repairs, captures and unequal work; stop scheduling on account limits.
Review actual assertions, interpreter/import provenance, cleanup and original-file
integrity before comparing input (cached included once) + output and process
wall time. n=1, shared host/cache, order and authored selection limit attribution.
Do not update featured figures or relabel earlier experiments with this candidate.

```sh
python3 -B benchmarks/run_httpx.py \
  --source /tmp/qh-httpx-preflight.3Slnqw/httpx \
  --python /tmp/qh-httpx-preflight.3Slnqw/venv/bin/python \
  --profile url-repr-audit --arms baseline skill --repeats 1 \
  --skill-revision 1a75a03 --output benchmarks/local-runs/httpx-url-repr-01
```

Paths above describe the existing local environment, not a portable installation
command. Runner validates the pinned clean source and repeats the original native
preflight before scheduling. Schedule/profile regression: 16 tests pass (0.630s).
Before freeze: full repository suite **378 tests pass (52.651s)**; catalog/local
links, featured synchronization and whitespace checks pass.
