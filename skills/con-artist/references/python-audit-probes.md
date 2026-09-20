# Native stronger probes

Read with the [common CLI contract](python-audit.md) when a stronger assertion
needs the project's native runner or fixtures. Supply `probe_files` (new relative
paths → source text) and `probe_tests` (arguments for the same runner), **instead
of** `probe`. Reuse the actual application call and relevant fixture, not a
replacement implementation. For example, with `runner: "unittest"`:

```json
{
  "probe_files": {
    "test_persistence_audit.py": "import unittest\nfrom service import save\n\nclass PersistenceTests(unittest.TestCase):\n    def test_persisted(self):\n        store = ['existing']\n        save(store, b'\\xff')\n        self.assertEqual(store, ['existing', b'\\xff'])\n"
  },
  "probe_tests": ["-v", "test_persistence_audit"],
  "probe_when": "survives"
}
```

These fields augment the common recipe; adapt paths, assertions and runner to
the project. Files exist only in fresh correct/faulty **probe** copies, never in
original-test checks or the source project. Existing paths, selected-file
collisions and traversal are refused before execution. Inputs plus probe files
share the 20 MB limit. Native runner exit status, including collection errors, is
preserved automatically; inspect actual failures and test counts. Normal JSON
escaping applies. Each probe copy is its working directory. Import verification
and the same-process precheck precede test bodies; for pytest they follow native
configuration/collection, but precede fixture setup.

`probe_when: "survives"` runs both probes only if mutant tests exit 0. A nonzero
mutant exit skips them with `probe_skipped`; inspect its failure rather than
automatically calling it detection or claiming the proposed probe was validated.
Omit this option (default `"always"`) when the probe must be verified regardless
of coverage. A timeout or failing correct check still stops as incomplete.

For installed pytest, supply pytest test arguments and retain its fixture/collection
behavior. Native file probes verify listed imports after collection to retain
assertion rewriting. Inline `probe` code executes as `__main__` with direct imports
and no native pytest setup; if it calls `pytest.main`,
propagate the exit with `raise SystemExit(pytest.main([...]))`, not an ignored
return. Native file probes already handle that propagation. Probe-created files
do not carry over to another check.

## Improve existing tests at their native paths

For an existing test-file improvement, use `probe_replacements` (selected relative
file path → complete proposed source text) with `probe_tests`, instead of copying
and modifying test suites manually. Original-test checks keep the original bytes;
both probe copies receive the proposed bytes at the same path and retain its mode.
This preserves native module names and fixture layout without editing the original.

```json
{
  "probe_replacements": {
    "test_service.py": "import unittest\nfrom service import save\nclass Tests(unittest.TestCase):\n    def test_saved(self):\n        values = []\n        self.assertTrue(save(values, 'item'))\n        self.assertEqual(values, ['item'])\n"
  },
  "probe_tests": ["-v", "test_service"]
}
```

Adapt the complete proposed test file, retaining required assertions/fixtures.
The replacement must name a selected existing file and cannot replace the mutation
target. Duplicate normalized paths, missing files, mixed inline `probe` mode and
oversized contents are rejected before execution. Original selected bytes plus
new/replacement probe contents share the 20 MB input budget. `probe_files` may
also supply new support files; it still never overwrites existing paths.

Use replacements for test/support changes, not to repair or bypass the production
fault. File roles and meaningful assertions are reviewed, not inferred from names.
This is trusted test execution, not a sandbox or proof of assertion quality.
The same copied imports/precheck and native runner apply to each phase. Correct
probe failure remains incomplete; changed replacement bytes invalidate batch
probe reuse. Applying a validated improvement to the source project is a separate,
authorized edit; this helper never applies it.

Only for several justified faults, [batch reuse](python-audit-batch.md)
includes probe contents and test arguments in its identity. For unexpected setup,
assertion or cleanup failures, read [diagnostics](python-audit-advanced.md#diagnostics-and-incomplete-evidence).
