# All-eight checkpoint 08 — 2026-09-14

Launch `de3cbc0`, resources `ecff8a8`; [prospective protocol](BUNDLE-CONTRACT-08-PROTOCOL.md).
All 18 scheduled sessions completed, no timeouts/exclusions, all usage known.
Timing ended at 2026-09-14 11:11:34 UTC before author replay or repository edits.
These are nine unchanged, exposed authored tasks, one baseline/skill session each,
not an independent holdout or a real-developer trial. No favorable retries.

## Outcome: broad efficiency still unproven

| Case | Baseline tokens | Skill tokens | Token change | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Boundary fix | 80,067 | 84,466 | +5.49% | 33.734 | 33.835 |
| Formatter review | 62,933 | 49,657 | −21.10% | 29.053 | 23.868 |
| Active history | 63,926 | 67,493 | +5.58% | 24.934 | 28.747 |
| Pending form | 84,261 | 94,373 | +12.00% | 75.903 | 73.530 |
| Persistence audit | 82,484 | 102,509 | +24.28% | 62.819 | 38.544 |
| Rolling schema | 83,973 | 108,299 | +28.97% | 70.500 | 47.820 |
| Search diagnosis | 121,649 | 71,058 | −41.59% | 100.184 | 58.335 |
| Search-order QA | 84,716 | 72,635 | −14.26% | 68.762 | 70.293 |
| Protected QA | 83,421 | 92,578 | +10.98% | 67.598 | 78.092 |
| **Sum** | **747,430** | **743,068** | **−0.58%** | **533.487** | **453.064** |

Summed process time is **15.08% lower**. Input tokens include cached input once,
plus output. Ratios of sums across every scheduled cell, not success-only costs
or the historical chart's means of task ratios. Six pairs use more tokens; three
cost more on both axes. Shared host/cache, n=1, exposed tasks and unequal extra
work prevent a causal/general 20–30% gain claim. Comparing this checkpoint with
[07](BUNDLE-CONTRACT-07-REVIEW.md) does not isolate any individual instruction edit.

## Original evidence and separate author controls

All raw terminal usage/events and frozen installed resource bytes/modes reconcile.
Installed resources did not change. Full retained inventories match the reviewed
files; original modes are preserved. Only requested boundary files and form.py
changed. Hostage's copied Python asset is byte-identical; Mother's embedded
Request/ControlledFetch runtime AST matches the frozen asset after removing
docstrings. No observed out-of-scope file modification.

Two original capture gaps remain **unverified**, not passes inferred from prose:

- Protected-search baseline item 6 contains no output at all despite a native
  test/hash/status/diff command and exit zero. Its final claim of three passes
  cannot establish original test execution evidence.
- Pending-form skill item 7 contains only status lines after an `&&` chain of
  copy, tests, copy comparison and diff checks. No native test names/count or diff
  is captured. Its final claim of six passes does not repair the missing output.

By contrast, empty commands that redirect into baseline search/SQL result files
are followed by captured reads of those files. They are not equivalent gaps.
Persistence baseline lacks its first printed section banner, but the first
native body/summary and binding evidence are present; do not claim byte-complete
capture. Several final semicolon chains cannot prove every preceding check's exit.

[Separate author reconciliation/replay](results/bundle-contract-08/author-replay.json)
uses unchanged retained tests in disposable project-local copies, explicit native
discovery/counts and 20-second process bounds. **22/22 expected outcomes match**:

- Both search-order suites reject stale original behavior and accept a valid
  generation guard (two native tests each).
- Protected suites accept final code and reject transient stale overwrite while
  the newest request remains pending, with actual value AssertionErrors (baseline
  three tests; skill seven).
- Both boundary suites accept final code and reject exactly-18 original behavior
  using the same three assertions.
- Both form suites run six tests, accept final code and a valid duplicate returning
  False, and reject original missing pending, missing guard and missing cleanup.
  Missing guard reaches owned wait deadlines (baseline two seconds, skill one),
  not a direct callback-count failure. Missing cleanup produces True-is-not-False
  assertions. Original missing pending produces AttributeErrors; baseline also
  reaches an entry timeout. No secondary UnboundLocalError was observed.

All retained projects remain unchanged. These controls establish behavior of the
retained artifacts; they **cannot fill the two original capture gaps**. No strict
18/18 success claim or headline win-rate is assigned from completion/replay.

## Pair review and unequal work

**Boundary / Receipt:** both add the exactly-18 test before editing implementation,
capture its intended failure alongside passing 17/19 checks, change `>` to `>=`,
and capture the same three passing assertions afterward. Both final `&&` chains
preserve failure status. Skill reads only its entry, no historical helper.

**Formatter / Landlord:** both inspect all three actual files and consumer/contract
references, recommend plain `format_usd` preserving the exact formatting expression
and `total_label` API. Both explicitly perform static review, no edits/tests.
Skill has four shell calls versus baseline three despite lower token usage.

**History / Necromancer:** both cite actual name-only partner input and the relevant
compatibility patch, separating current necessity from historical intent. Both
observe current Ada versus None/KeyError alternatives. Skill substitutes the
consumer binding in memory; baseline evaluates the same payload directly.
Skill uses native Git, not the optional collector. No files change.

**Form / Hostage:** both add six native tests covering pending/duplicates/instances,
success/error identity, synchronous failure and cancellation/retry. Neither asserts
an unspecified duplicate return value. Baseline uses owned events; skill uses the
task-aware copied callback asset and three duplicate calls. Skill adopts one final
failure-preserving batch, but its original output gap remains. Its initial broad
discovery still lists installed assets and reads requirements in a later call.

**Persistence / Con Artist:** both observe correct-existing pass, faulty-existing
pass, correct-stronger pass and faulty-stronger stored-list AssertionError. Same
stronger assertion preserves a pre-existing record. Binding/path evidence identifies
the actual loaded copied service/test. Baseline uses line/call tracing with local
scratch cleanup; its children have no individual deadline (outer model bound only).
Skill uses the installed audit helper once with same-process test-global binding
prechecks and bounded children, preserving original bytes/modes and removing scratch.
It reads the core guide **and the entire 27,725-character audit implementation**;
no specific trust/adaptation problem was stated. That extra reading is a concrete
cost candidate, not proof that legitimate source inspection should be forbidden.
Unlike checkpoint 07 baseline, this baseline needs no observed tracing repair.

**Schema / Friday:** both exercise actual reader queries in four schema/data states,
capture all eight reader outcomes, verify insert/update/untouched data survives
down, and block both documented rollout and rollback ordering. Writers and staging
remain explicitly unverified. Baseline retains a script and verbose JSON including
PRAGMA schema rows; skill reads only the shortened core guide, executes the matrix
API once, and reuses results for column/value/truncation assertions without a new
artifact. Skill still lists installed resources during discovery. Core-only adoption
does not guarantee lower total session tokens.

**Diagnosis / Exorcist:** both use actual Search and transport through controlled
request stubs, capture no-cache headers and both completion orders, and reproduce
stale final results independently of a cache. Two-second owned waits/cleanup;
production behavior beyond the local probe remains unknown. Baseline retains a
script, JSON and README; skill retains only a script and prints the evidence.
That difference limits interpretation of the favorable token/time pair.

**QA / Mother-in-law:** both search-order suites use actual Search and bounded
owned requests without inventing intermediate-display requirements. Both capture
the intended older-versus-latest failure; baseline also saves a duplicate log file.
Protected baseline has three methods, skill seven including repeated-query and
seeded order variants. Both retain prior display through older completion while
newer is pending. Additional skill witnesses are useful but are not equal work;
baseline's original passing output remains missing despite a successful replay.

## Next decisions

Investigate costly discovery/source-reading paths and why model final claims ignore
missing native output. Keep required checks, caller binding and failure evidence.
Do not rerun this unchanged suite until a favorable headline appears. Future new
capabilities need focused fault controls and a fresh, frozen transfer task; independent
real-project validation is still needed. Featured and historical images are unchanged.

Reproduce the author controls with `python3 -B benchmarks/replay_bundle_contract_08.py
--run benchmarks/local-runs/bundle-contract-08 --output <new-output.json>` using the
original local run. Public [export](results/bundle-contract-08/run.json) preserves all
18 cells, redacted commands/events, source hashes and retained projects; raw original
path-containing logs remain local. Local validation is not hosted CI/release proof.
