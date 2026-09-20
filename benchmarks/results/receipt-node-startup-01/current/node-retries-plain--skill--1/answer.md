I’ll use the receipt skill to compare both revisions with the same current tests and native startup, then remove the disposable copies and check that the original state is preserved.


The change replaces `||` with `??`, so explicit zero is preserved while omitted and null retry values still default to three. The four current tests cover those cases plus a positive value. I’ll run the exact native command in each copy; the tests already print the imported module’s origin and their process PID.


Verified: HEAD^ reproduces the zero-retry defect; HEAD passes all four unchanged current tests.

Both copies ran Node v24.16.0 with exactly:
```sh
node --test --test-reporter=tap tests/policy.test.mjs
```

| Revision | Passed / Failed | Native exit |
|---|---:|---:|
| HEAD^ `62d7afb676b986d6905beb5ab177c4d3e3f702f1` | 3 / 1 | 1 |
| HEAD `6e4e4ece6400ec4b0aa65acea8988fbe70b8c6b5` | 4 / 0 | 0 |

Both discovered four tests, with zero skipped, cancelled, or todo.

| Actual strict-equality assertion | HEAD^ | HEAD |
|---|---|---|
| `retries({retries:0}) === 0` | Failed: actual `3` | Passed |
| `retries({retries:2}) === 2` | Passed | Passed |
| `retries() === 3` | Passed | Passed |
| `retries({retries:null}) === 3` | Passed | Passed |

The tests’ own `ACTUAL_MODULE` output identified these project-relative origins inside their native test processes:

- PID **10480**: `.receipt-q7dysmv7/before/policy.mjs`
- PID **10484**: `.receipt-q7dysmv7/after/policy.mjs`

These came from the imported policy’s `origin` and the test process’s `process.pid`; they are diagnostic identity, not tamper-proof attestation.

The fix replaces `||` with `??`: zero survives, while omitted/null retry values default to three. Positive integers remain unchanged; execution sampled `2`. Other input behavior was not evaluated. The before failure is an actual assertion failure, not missing setup.

Preservation checks confirmed original bytes/modes, notes, Git HEAD/index, and installed skill resources remained unchanged. `git diff --check` passed. Both copies were removed; no harness or report remains.
