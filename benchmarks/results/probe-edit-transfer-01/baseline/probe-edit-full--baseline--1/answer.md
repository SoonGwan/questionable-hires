I’ll run the selected test in fresh disposable copies and verify imports inside each pytest process. If the fault survives, I’ll strengthen only the copied test method and check both implementations, then remove the copies.

The existing selected test **does not detect the fault**: it only constructs `Specifier`, so the defective `__str__` survives.

Four actual pytest executions ran in fresh project-local copies; no observations were reused:

| Test | Implementation | Passed | Failed | Exit |
|---|---|---:|---:|---:|
| Original | Correct | 9 | 0 | 0 |
| Original | Faulty | 9 | 0 | 0 |
| Strengthened | Correct | 9 | 0 | 0 |
| Strengthened | Faulty | 0 | 9 | 1 |

The proposed change was confined to the existing method body:

```diff
-        Specifier(specifier)
+        assert str(Specifier(specifier)) == specifier
```

All nine faulty assertions compared actual `''` against these expected values:

```text
~=2.0
==2.1.*
==2.1.0.3
!=2.2.*
!=2.2.0.5
<=5
>=7.9a1
<1.0.dev1
>2.0.post1
```

Correct code returned each expected string exactly. There were no setup or collection errors.

Every execution used the supplied Python with `-B`, native `pytest.main`, and exactly the requested selector/options. Inside each pytest process, checks verified all three module paths belonged to that copy and the test’s `Specifier` binding was that implementation.

Scratch was removed. Original project bytes/modes, Git HEAD/index, imports, parameterization, and other file contents remain unchanged; neither proposed edit nor fault remains applied. This conclusion concerns only the selected test.
