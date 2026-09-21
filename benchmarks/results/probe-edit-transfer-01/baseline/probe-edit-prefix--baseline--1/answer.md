I’ll run all four phases in fresh disposable copies and verify what each pytest process actually imports. The proposed test change and fault will stay in those copies, which I’ll remove afterward.

The existing constructor smoke test **does not detect the fault**: all nine cases pass when `Specifier.__str__` returns `""`.

The verified proposed change is:

```diff
     def test_specifiers_valid(self, specifier):
-        Specifier(specifier)
+        assert str(Specifier(specifier)) == specifier
```

| Test | Implementation | Passed | Failed | Exit |
|---|---|---:|---:|---:|
| Existing | Correct | 9 | 0 | 0 |
| Existing | Faulty | 9 | 0 | 0 |
| Proposed | Correct | 9 | 0 | 0 |
| Proposed | Faulty | 0 | 9 | 1 |

On correct code, actual strings exactly matched all supplied values: `~=2.0`, `==2.1.*`, `==2.1.0.3`, `!=2.2.*`, `!=2.2.0.5`, `<=5`, `>=7.9a1`, `<1.0.dev1`, and `>2.0.post1`. On faulty code, every actual string was `''`; each proposed assertion failed against its supplied value.

Four actual pytest executions used fresh project-local copies, the supplied Python with `-B`, and exactly the requested selector/options through native `pytest.main`. Each pytest process verified all three module paths and the native test’s `Specifier` identity. No observations were reused; no collection, setup, or teardown errors occurred.

Parameterization, imports, and other contents were preserved. All scratch was removed, and project bytes/modes—including Git HEAD/index—were verified unchanged. Neither edit remains applied. This conclusion concerns only the selected test.
