# Receipt committed SQLite delivery transfer 01 — 2026-09-14

Freeze skill resources `ec0cc28` and collector behavior `4325a05`. New authored
cases `receipt-ledger-cases.json`, SHA-256:
`5aeac6200940dc4d29898920429aae684712afea753df12e7985862f5016b742`.
Generator: [receipt_ledger_cases.py](receipt_ledger_cases.py).

## Why this transfer

Move beyond the exposed source-layout string parser: verify committed revisions,
execute real file-backed SQLite transactions, and read committed balances through
fresh connections. Current tests are uncommitted and absent from the historical
implementation; both comparison copies must use these same current assertions
and schema. Ignored cache and unrelated owner notes must remain unchanged.

Two correlated variants, not two independent domains: `ledger-delivery-a` prevents
duplicate mutation; `ledger-delivery-b` fixes acknowledgement but still mutates
the balance twice. The task asks whether the change works, explicitly accepts
reporting an incomplete fix and prohibits implementing a repair. Do not reward
all-green prose, a helper's CLI 0, static reasoning alone or narrower assertions.

## Frozen obligations and author preflight

Both before revisions: five native methods, two retry assertion failures and
three passing controls. Case a after: all five pass. Case b after: two retry
balance assertions still fail despite a False acknowledgement; three controls
pass. Controls cover same event across different accounts, distinct equal-value
events and a zero delta. Positive/negative retries are observed, with a separate
connection after each tested write. Expected errors are actual/expected tuple
assertions, not import/setup exceptions.

Author preflight `tests/test_receipt_ledger_fixture.py`: **2 tests / 0.760s**,
covering both variants plus generator/frozen equality. Actual helper comparisons
run all native SQLite tests with copy-local imports, identical test/schema bytes,
unchanged complete original inventory and cleaned databases/comparison copies.
Every test creates its database under its own comparison root, asserts that
location, closes its connections and registers cleanup. Native error output shows
`(True, 250)` / `(True, -100)` before versus expected `(False, 125)` /
`(False, -50)`; incomplete after shows `(False, 250)` / `(False, -100)`.
Repository validation and featured EN/KO sync also pass.

This preflight validates fixtures, **not model behavior or relative efficiency**.
The tasks are newly authored but not independent third-party or production data.
Sequential existing-account operations only; concurrency, crash recovery, changed
retry payloads and network delivery are explicitly out of scope.

## Scheduled model screen

Two cases × baseline/skill × one repeat = four independent sessions; serial,
Astra medium, seed20260911, 240 seconds each, no retries or favorable selection.
Use unchanged fixtures and no author workloads/resource edits during timing.
Review full original native tests, assertions, copied imports, actual revisions,
original preservation and cleanup. Adoption of tree guard is recorded separately,
not required for success: another valid native route is acceptable.

After timing reconcile frozen resources, raw/events, usage, initial/project bytes
and local pre-collection index evidence. Replay literal programs/recipes separately
on disposable copies, preserving mismatches and original capture gaps. Restore a
captured index only into a disposable replay when justified, never into originals;
retain before/after identities and inspect any remaining difference.

Report every scheduled cell, costs and actual extra work. Cost ratios alone do
not establish superiority, especially if success/evidence/coverage differ. n=1,
correlated cases, shared host/cache and authored selection prevent broad claims.
Keep historical/featured graphs unchanged; record review in dated report/current
status in both languages. Do not promote this small screen as all-eight efficacy.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/receipt-ledger-cases.json --output benchmarks/local-runs/receipt-ledger-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
