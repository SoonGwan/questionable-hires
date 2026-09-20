I’ll inspect the project’s startup contract, then run the current tests against both revisions in separate local copies and remove the copies afterward.

The fix changes `||` to `??`, preserving explicit zero while retaining the default for omitted or null retry values. The four current tests cover zero, positive `2`, omission, and null. They also print the imported module’s origin and the test process PID. No `NODE_OPTIONS` value is set; I’ll use the exact native command in each copy.

Verified: HEAD^ reproduces the zero-retry defect; HEAD passes all four unchanged current tests. Both native runs completed setup and reached assertions.

Used Node v24.16.0 from each separate copied project root:
```sh
node --test --test-reporter=tap tests/policy.test.mjs
```

| Variant | Full revision | Tests | Pass/fail | Exit |
|---|---|---:|---|---:|
| HEAD^ | `62d7afb676b986d6905beb5ab177c4d3e3f702f1` | 4 | 3/1 | 1 |
| HEAD | `6e4e4ece6400ec4b0aa65acea8988fbe70b8c6b5` | 4 | 4/0 | 0 |

Neither run skipped, cancelled, or marked tests TODO.

| Strict assertion | HEAD^ actual | HEAD actual |
|---|---:|---:|
| `retries({retries:0}) === 0` | **3 — failed** | 0 |
| `retries({retries:2}) === 2` | 2 | 2 |
| `retries() === 3` | 3 | 3 |
| `retries({retries:null}) === 3` | 3 | 3 |

The tests’ native `ACTUAL_MODULE` output identified these paths relative to the original project root:

- HEAD^: `.policy-verification-tv9uhnjz/parent/policy.mjs`, test-process PID **9246**.
- HEAD: `.policy-verification-tv9uhnjz/head/policy.mjs`, test-process PID **9249**.

These identities came from the imported module’s `origin` and `process.pid` inside each native test process. They confirm the corresponding copy diagnostically, not as tamper-proof attestation.

The fix replaces `||` with `??`: zero survives, while undefined/null retry values use three. Positive integers pass through; the tests specifically verify `2`. Other input behavior remains unspecified.

Original file bytes/modes, notes, and Git HEAD/index were unchanged. The existing `?? tests/` status was preserved. All owned scratch was removed; no harness or report remains.
