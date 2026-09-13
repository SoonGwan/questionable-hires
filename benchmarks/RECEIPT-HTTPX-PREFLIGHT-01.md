# Actual checkout, disclosed seeded query-parameter defect

Preparation only; no model session or performance result yet. This uses the
existing HTTPX checkout `26d48e0634e6ee9cdc0533996db289ce4b430177` and installed
Python environment. No network, dependency installation or source-checkout edits.
The shallow checkout does not supply actual pre-fix history, so this fixture must
not be represented as a historical upstream bug.

`prepare_httpx_receipt.py` copies the full clean checkout with independent Git
files, then injects one disclosed fault: `URL.copy_set_param` uses query-parameter
`add` instead of `set`. It preserves the supplied native tests and neighboring
methods, checks all 125 original tracked files, and makes a fixture-only commit.
The copy is not a published upstream change. The output cannot be inside the
original checkout; existing output directories are not overwritten.

The actual native pytest preflight uses these unchanged tests:

- `tests/models/test_url.py::test_url_set_param_manipulation`
- `tests/models/test_url.py::test_url_add_param_manipulation`
- `tests/models/test_url.py::test_url_remove_param_manipulation`

Original implementation: **3 passed**, exit 0. Seeded implementation: **1 failed,
2 passed**, exit 1. The failing assertion expects
`https://example.org:123/?a=456` but actually receives
`https://example.org:123/?a=123&a=456`. This is a behavioral assertion, not a
dependency or collection error. Neither control touches the network or creates
test scratch files. Pytest's cache provider is disabled consistently. No missing
dependency is installed to obtain this result.

The local retained output is `benchmarks/local-runs/receipt-httpx-preflight-01/`:
`preflight.json` contains both captured outputs/statuses; `fixture.json` contains
all source hashes, interpreter identity and the seeded commit
`8ed44f4f3d3c06bc408b378e435f9e106a7d4254`. The prepared project has a clean Git
status after that commit. The source checkout and all its tracked bytes remain
unchanged. Repreparing will create a different fixture commit timestamp; freeze
the actual prepared snapshot used by a future run rather than guessing its hash.

Next: freeze the model task, current Receipt revision, these equal required
before/after checks and scope before scheduling one baseline/skill pair. Ask for
the requested production fix, preserve all tests, require matching runner settings
and retain every outcome/cost. The model must perform its own before/after checks;
this author preflight is not model evidence. This is a real-code seeded development
task, not an independent organic bug or an all-eight superiority benchmark.
