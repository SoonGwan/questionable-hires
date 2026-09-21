# Partial package initialization: local helper correction

Checkpoint: 2026-09-21. Parent revision: `2bd4b58`.
This is a deterministic helper regression test, not a model benchmark.

## Reproduced failure

The urllib3 history investigation exposed unittest's retry behavior after a
test-module import fails. A package initializer can load its `util` child and
then fail importing absent generated metadata. The root package disappears from
`sys.modules`, but the child remains. A repeated test import can use that child.

The new `test_cached_child_of_failed_package_is_not_complete_setup` exercised
the actual Con Artist helper with this arrangement. Before correction it failed:
the helper returned `observed` instead of `incomplete`. The correct check passed,
and the mutation produced a real `AssertionError: 18 != 17`; neither established
successful package initialization. The pre-fix test completed in 0.107 seconds.

## Narrow correction and controls

After resolving an explicitly listed qualified import, shared setup checks every
parent prefix in `sys.modules`. An absent parent raises a setup error, mapped to
check exit7 and `incomplete`; the failed normal setup stops mutation execution.
This adds no subprocess or repeated package import.

Tests cover a missing root and missing intermediate parent. Adding the required
generated metadata is a positive control: the real correct test passes and the
mutant fails with the intended assertion. Selected original bytes/modes remain
unchanged and owned scratch is removed in both outcomes.

Reproduction commands:

```sh
python3 -B -m unittest discover -s tests -p 'test_audit*.py'
benchmarks/local-runs/receipt-provenance-venv/bin/python -B -m unittest discover -s tests -p test_audit_module_invocation.py -v
```

Python3.9: 106 audit tests, 11 skipped, 11.912 seconds; all executed tests pass.
Python3.11: 14 native-module tests, 3.300 seconds; all pass.
Python3.11 shared audit suite: 106 tests, 16.046 seconds; all pass, no skips.
Packaging: 13 build tests and 4 standalone-archive tests pass. Skill metadata,
repository documentation links and bilingual featured synchronization validate.
Skipped tests are not counted as successful executions.

## Limits

The guard checks only parent-cache presence for listed qualified imports. It
does not independently cold-import the public package, validate every dependency
or ancestor location, or protect against malicious tests and later rebinding.
The fixture is a regression control derived from a known failure, not independent
generalization evidence. No new token, latency or model-accuracy gain is claimed;
frozen benchmark results and featured charts remain unchanged.
