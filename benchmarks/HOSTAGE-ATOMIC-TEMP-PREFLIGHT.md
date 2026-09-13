# Explicit test scratch roots for future comparisons

The [measured atomic-export pair](results/hostage-atomic-export-01/README.md)
used fixture tests with default system temporary directories. Baseline later
changed TMPDIR and cleaned an Xcode-generated file; skill did not. Those inputs,
traces, scores and scope limitations are frozen and unchanged.

The separate [local-temp variant](hostage-atomic-export-local-temp-cases.json)
uses explicit project-local `TemporaryDirectory(dir=...)` in supplied tests and
tells new tests to do likewise, without changing global TMPDIR or launcher
settings. It preserves the implementation, task behavior, normal controls and
acceptance criteria. It is a corrected development fixture in an already exposed
task family, **not** an independent holdout or a new performance result. No model
cells are scheduled by this correction.

`tests/test_hostage_atomic_fixture.py` uses a child-process Python audit hook to
observe actual `tempfile.mkdtemp`/`tempfile.mkstemp` creation paths and reject paths
outside the project. Both before and after exercise four assertion-bearing tests:
before has two behavioral failures and zero support errors; after has four passes.
Each run creates four project-local temporary directories; the author replacement
also creates four project-local output files. None remain after the suite.
Author-only contract checks use the same explicit directory policy.

The existing frozen task SHA-256 is checked against
`c1057149df91fff55beeb9d8a108834f3c9a2f56c3d3b809e35efe76a385c3e2`.
The audit hook is preflight instrumentation, not model-visible code, an OS
sandbox or proof about arbitrary filesystem calls. This correction controls
fixture-generated scratch paths; it cannot guarantee future model-created tests
obey the instructions without reviewing their actual execution.

Benchmark authoring guidance now requires this explicit temporary-root contract
and actual path verification for project-only fixtures. Do not rerun the old
task until a lower score appears; use the controlled pattern in future distinct
developer tasks and retain any new failures or configuration differences.
