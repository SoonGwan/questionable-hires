# All-eight contract gate 03: frozen prospective protocol

Use `bundle-contract-cases.json`, nine exposed authored tasks covering all eight
hires. Candidate resources are `557f012`; no subsequent skill edits precede this
protocol. The [draft](BUNDLE-CONTRACT-03-DRAFT.md) explains why task obligations
changed. Previous fixtures, measurements and scores remain untouched.

This is development regression evidence, **not held-out, organic real-repository
or causal confirmation**. The revised task obligations invalidate direct cost
attribution against older bundle runs. Compare contemporary baseline/skill cells
at their reviewed requested outcomes; keep extra work and limitations visible.
Helper use is optional and is neither an outcome nor an efficiency criterion.

## Author preflight, separate from model evidence

`tests/test_bundle_contract_preflight.py`: seven tests exercise all nine cases.

- Real prepared Git history contains the fallback/consumer change; actual caller
  returns Ada, and in-memory fallback removal breaks that result.
- Actual existing eligibility tests plus exactly-18 assertion: two controls pass
  and the new assertion fails (`False != True`); the same suite passes with >=.
- Actual formatter consumer preserves the documented expression on representative
  positive/zero/negative values. This is not a universal numerical proof.
- Actual Search and transport run normal/reversed controlled completions. Broken
  search yields old instead of new; protected search retains existing output while
  newer work is pending and keeps new output after reversal. Actual no-cache
  headers are recorded. One-second waits/cleanup and three-second scenario bounds
  finish with owned tasks done; assertions detect the intended stale value.
- Original Form lacks pending state. A separate author-only implementation
  satisfies pending/duplicate/instance/return/error/retry/cancellation assertions;
  removing finally cleanup fails (`True is not false`). This witness is not a
  model implementation or part of the supplied task. No claim that original Form
  already implements the feature follows.
- Actual supplied save test survives removal of the reachable append, with its
  imported binding confirmed. A stronger exact-record check passes correct code
  and fails the mutant, retaining the pre-existing record in the observed output.
- Actual supplied SQL/readers run on in-memory initial/up/down states, yielding
  intended missing-column errors and preserving representative updated/new records
  through down. No unprovided application writer or production state is simulated.

Focused preflight: **seven tests pass (0.166 seconds)**. Original fixtures are not
edited; deliberate changes are in-memory author copies. Async tests need no disk
scratch. The history repository uses an owned temporary directory cleaned by the
test. This validates support/contract feasibility, not model behavior or savings.
Generator test separately verifies nine cases/eight skills, visible appended
obligations and unchanged original code/history/criteria. Review decisions remain
human/model assessments, not automated correctness derived from these test counts.

## Execution and review rules

One baseline and one corresponding explicit-skill session per case: 18 total,
Astra medium, repeats=1, jobs=1, seed=20260911, 240-second cell limits. Freeze this
protocol before execution; use recorded fixture/resource hashes and shuffled
schedule. No automatic-selection/control arm, thus no routing-recall claim.
No retries, exclusions, candidate/fixture edits or concurrent author tests during
timing. Retain failures, repairs and partial output; stop new scheduling after
recognized account limits. Re-poll live runs, never restart after observation loss.

Inspect actual assertions, command statuses, provenance, final files, scope,
original preservation and required delivery. Do not replace missing output with
final-answer claims or author replay. Unverified outcomes stay unverified and
included in cost accounting. For each pair record remaining unequal extra work.
Tokens are input plus output, cached input once, reasoning output not added twice;
time is process wall time. Shared host/cache/order and n=1 limit inference.
Do not rerun this exposed gate for favorable scores. No automatic featured graph
replacement; broader real-development confirmation and all-eight goal remain.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/bundle-contract-cases.json \
  --output benchmarks/local-runs/bundle-contract-03 --arms baseline skill \
  --repeats 1 --jobs 1 --seed 20260911 --timeout 240 \
  --model gpt-6-astra --effort medium
```
