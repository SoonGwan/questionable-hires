I’m using the receipt skill to compare both revisions with the unchanged current tests and required preload, then check that the original files and Git state are preserved.


The tests already report the imported module’s path and test-process PID. The bootstrap supplies the required default; without it, a startup error would be missing setup, not a regression. I’ll use the exact native command in each copy—the optional comparison helper adds runner options, so it does not fit this startup contract.


Verified: HEAD fixes explicit zero while preserving the other tested supported inputs.

- **HEAD^:** `003b6e42933fcbc2ce6fc1942a52a18a73d99b71`
- **HEAD:** `fefd22edd69e88626975ad7226918a2ccc063563`

Both disposable copies ran on Node **v24.16.0**, from their respective roots, using exactly:

```sh
NODE_OPTIONS='--import ./bootstrap.mjs' node --test --test-reporter=tap tests/policy.test.mjs
```

The current tests and bootstrap were byte-identical between copies.

| Actual strict-equality assertion | HEAD^ | HEAD |
|---|---|---|
| `retries({retries:0}) === 0` | Failed: actual `3` | Passed |
| `retries({retries:2}) === 2` | Passed | Passed |
| `retries() === 3` | Passed | Passed |
| `retries({retries:null}) === 3` | Passed | Passed |

Native results: **before 4 tests, 3 passed, 1 failed, exit 1; after 4 tests, 4 passed, exit 0**. Both reported zero skipped, cancelled, or todo tests.

Inside each native test process, the unchanged test reported the imported module’s `origin` and `process.pid`. Confirmed paths relative to the original project root:

- Before: `.receipt-mgp55adx/before/policy.mjs`, PID **11237**
- After: `.receipt-mgp55adx/after/policy.mjs`, PID **11242**

These are test-bound diagnostic identities, not tamper-proof attestation.

The fix replaces `||` with `??`: zero survives, while omitted/null retry values use the preloaded default of three. Positive integers remain unchanged; the suite exercises `2`. The before failure was an actual assertion failure with setup loaded, not a missing-bootstrap error. Other input behavior remains unspecified and unverified.

Original bytes, modes, notes, skill resources, Git HEAD/index, and existing untracked state were preserved. `git diff --check` exited **0**. Scratch was removed; no harness or report remains.
