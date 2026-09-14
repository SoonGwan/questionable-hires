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
escaping applies. Each probe copy is its working directory; listed imports and
the same-process precheck precede the native runner.

`probe_when: "survives"` runs both probes only if mutant tests exit 0. A nonzero
mutant exit skips them with `probe_skipped`; inspect its failure rather than
automatically calling it detection or claiming the proposed probe was validated.
Omit this option (default `"always"`) when the probe must be verified regardless
of coverage. A timeout or failing correct check still stops as incomplete.

For installed pytest, supply pytest test arguments and retain its fixture/collection
behavior. Do not pre-import test modules into `imports`; that bypasses assertion
rewriting. Inline `probe` code executes as `__main__`; if it calls `pytest.main`,
propagate the exit with `raise SystemExit(pytest.main([...]))`, not an ignored
return. Native file probes already handle that propagation. Probe-created files
do not carry over to another check.

Only for several justified faults, [batch reuse](python-audit-batch.md)
includes probe contents and test arguments in its identity. For unexpected setup,
assertion or cleanup failures, read [diagnostics](python-audit-advanced.md#diagnostics-and-incomplete-evidence).
