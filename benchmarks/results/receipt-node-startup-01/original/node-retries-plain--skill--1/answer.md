I’m using the receipt skill to compare both revisions with the same current tests and native startup command, then check that the original project is unchanged and remove the disposable copies.

The fix replaces `||` with `??`, preserving explicit zero while keeping the default for omitted and null values. The four current tests already print the imported module’s origin and their process PID, so I can use the exact native command without adding instrumentation.

Verified: HEAD^ reproduces the zero-retries defect; HEAD passes all four unchanged current tests. No setup failure occurred.

- **Before:** `62d7afb676b986d6905beb5ab177c4d3e3f702f1`
- **After:** `6e4e4ece6400ec4b0aa65acea8988fbe70b8c6b5`

Both copies used Node **v24.16.0**, identical test bytes, and this exact command from their respective roots:

```sh
node --test --test-reporter=tap tests/policy.test.mjs
```

| Native test identity | Actual assertion | Before | After |
|---|---|---|---|
| explicit zero disables retries | `retries({retries:0}) === 0` | Failed: actual `3` | Passed |
| explicit positive survives | `retries({retries:2}) === 2` | Passed | Passed |
| omitted value uses default | `retries() === 3` | Passed | Passed |
| null uses default | `retries({retries:null}) === 3` | Passed | Passed |

Before: **4 tests, 3 passed, 1 failed, exit 1**. After: **4 tests, 4 passed, exit 0**. Neither run skipped, cancelled, or marked tests TODO.

Each native test process printed the origin of its imported `policy` module and its own PID:
- PID **9887**: `<project>/.receipt-_6wjkx8o/before/policy.mjs`
- PID **9891**: `<project>/.receipt-_6wjkx8o/after/policy.mjs`

Both origins matched the corresponding copied implementation. This is same-process diagnostic identity, not tamper-proof attestation.

The fix changes `||` to `??`: zero survives, omitted/null values default to three, and positive integers survive. The tests exercise positive integer `2`; other input behavior is unspecified.

The preservation check confirmed unchanged original bytes/modes, notes, Git metadata including HEAD/index, and skill resources. Scratch was removed; no harness or report remains. `git diff --check` passed.
