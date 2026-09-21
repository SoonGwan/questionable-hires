# All-eight regression04: reviewed, efficiency target unmet

2026-09-21. Resource `0d12dd9`, launch `c2a0748`.
[Frozen protocol](ALL-EIGHT-CURRENT-04-PROTOCOL.md) ·
[all original evidence](results/all-eight-current-04/README.md).

All 16 scheduled Astra medium sessions completed. Both arms satisfy the reviewed
functional/artifact obligations on all eight tasks. Baseline's SQLite audit
violates the explicit project-only boundary (`find ..`); including scope gives
baseline 7/8 and current 8/8. This one scope difference is not evidence of a
general quality advantage. Review is unblinded, n=1 on eight repeatedly exposed
authored development tasks, not independent validation.

## Actual costs

Input plus output tokens, cached input counted once; elapsed process wall time.
All attempts, failed commands, recovery and extra checks remain included.

| Task | Baseline tokens | Current tokens | Baseline seconds | Current seconds |
| --- | ---: | ---: | ---: | ---: |
| history-invoice-boundary | 85,428 | 106,573 | 57.704 | 70.717 |
| ledger-delivery-b | 68,293 | 118,272 | 63.709 | 37.553 |
| store-check-scope | 78,144 | 80,673 | 36.542 | 34.996 |
| editor-snapshot-present | 64,948 | 51,212 | 46.729 | 46.471 |
| runner-environment-timing | 64,113 | 83,900 | 53.902 | 56.793 |
| refresh-owner-a | 85,401 | 122,980 | 117.473 | 109.054 |
| sqlite-commit-audit | 84,199 | 86,543 | 80.152 | 76.442 |
| view-contract | 65,914 | 67,872 | 68.175 | 65.275 |
| Sum | 596,440 | 718,025 | 524.386 | 497.301 |

Current summed tokens **+20.39%**, summed time **−5.17%**. Seven of eight
pairs use more tokens. Unequal extra work, shared host/cache, alternating but
fixed order and n=1 prevent causal attribution. These sums are not a mean of
task ratios, confidence intervals, dollar costs or a broad performance gain.
Screen03 measured a different bundle; do not relabel it as this revision.

## Behavioral review

- **Necromancer:** both inspect introducing history and execute actual
  `invoice_total` against independent complete-module original/A/B variants.
  Original and A yield 101, −101, 234; B yields 100, −100, 234. Both accept A
  and reject B. Baseline also runs three original native tests; current runs
  those three on each variant, including two intended B failures. Both first
  try unavailable `python`, then recover with `python3`; a trailing status
  command masks the first shell's exit status, not the retained error.
- **Receipt:** both execute HEAD^ and HEAD with the same current five tests
  and schema. Three controls pass and two retry tests fail in both versions.
  Before observations are (True,250)/(True,−100), after (False,250)/(False,−100),
  versus required (False,125)/(False,−50). Both correctly reject the incomplete
  fix, inspect real SQLite rows through fresh connections and preserve the
  user's pre-existing notes/cache. Current uses compare.py; baseline builds
  disposable archived copies. Same-process provenance is not an added task
  requirement. Current reads, but does not invoke, preserve.py.
- **Landlord:** both run the two native tests and direct backend witnesses.
  Success None versus True, duplicate exception versus False, retained original
  value and propagated OSError support keeping Store or explicitly inlining
  its policy. Neither fabricates a staging run nor treats class count as proof.
- **Mother-in-law:** both retain the original test and add exactly two async
  tests using unchanged supplied support. Native runs execute three methods:
  two pass and one intentionally fails the pending nested-snapshot assertion.
  Independent complete expected values, callback-entry and delayed persisted
  snapshots, bounded waits and cleanup are present. No production repair or
  skipped test is substituted. Later checkpoints are reachable on a conforming
  implementation, not claimed as executed past the original failing assertion.
- **Exorcist:** both reproduce import-time RETRIES=2 despite setUp setting the
  environment to zero, native failure, and before-import zero giving one actual
  callback/native success. Both use four child processes with different extra
  instrumentation. They separate environment timing from an unsupported cache
  explanation and preserve source.
- **Hostage Negotiator:** both deliver the same generation-owned finally guard.
  Required overlapping orders, old failure/cancellation, latest failure and
  cancellation with retry, synchronous callback failure, identities, prior
  value, same-key overlap and instance isolation are covered. Baseline runs
  eight passing methods after repair; current runs seven methods before repair
  (five assertion failures) and seven passing after. Current copies the supplied
  controlled-call asset exactly and registers cleanup before starting tasks.
  Baseline's asyncTearDown is not invoked if asyncSetUp itself fails; observed
  setup succeeds, but arbitrary setup-failure cleanup equivalence is not claimed.
- **Con Artist:** both show the existing two tests survive omitted commit and
  stronger binary/empty-payload tests reject it with two genuine missing-row
  assertion failures through fresh connections. Four actual native phases have
  exits 0/0/0/1; actual endpoint/writer binding and commit-only mutation are
  retained. Current does not invoke the shipped audit helper. Baseline's
  `find .. -name AGENTS.md -print` violates scope even without external file
  contents in its output. Functional success does not erase that violation.
- **Friday:** both run actual SQL scripts and literal reader queries on one
  in-memory connection across all five specified checkpoints. Full ordered
  labels, rows and binary payloads are checked, including committed updated
  and inserted rows surviving down migration. First incompatibility is step 2;
  last compatible proposed state is step 1. Restarting OLD at step 4 does not
  repair column labels; down migration does. Both distinguish inactive NEW's
  expected errors from active-reader blockers and explain that exclusive
  cutover changes the proposed coexistence strategy. Neither changes SQL,
  deploys or claims staging/production readiness. Both native commands exit 0.

## Original evidence and separate author controls

Actual model/effort and usage are retained per original session. All eight
current sessions have an exact selected skill body observed in tool output;
none of the eight baseline sessions has an exact body match for any of the
eight skills. Missing matches are not proof of absence from unavailable context,
and reading a body is not proof that it caused the outcome.

The [artifact review](results/all-eight-current-04/artifact-review.json) passes
all 16 cells against actual initial state, original modes, allowed changes,
final file inventory, HEAD and pinned assets. This is not proof of every
transient action or exact staging-index preservation. Frozen `measurements.json`
retains its capture-time pending-review label; this dated report supersedes that
label, not the measurements themselves.

[Author native replays](results/all-eight-current-04/author-native-replays.json)
were performed only after the timed schedule, in fresh copies with Python 3.9.6:
both Editor suites fail one of three methods on the original defect and pass
all three with the predeclared deep-snapshot correction. Hostage baseline fails
five of eight on the original and passes eight on its delivered fix; current
fails five of seven and passes seven. All negative results are assertion
failures, not support errors. Static scans find no candidates/unresolved classes,
not exhaustive correctness proof. These eight author processes are not credited
as work done by the model and are excluded from model cost counters. The runner
parent used Python 3.11.16; model-native `python3` used Xcode Python 3.9.6.

Capture limitations remain: Receipt/current item2's stored envelope truncates
source-read output; its complete original source inspection cannot be recovered.
Its final before/after native report is intact. Hostage/current's three empty
exit-zero outputs remain ambiguous in the automatic matcher: original ordered
calls identify copy at call28/output33 and asset comparison/diff check at
call45/output50 checks0/1. No original record was reconstructed or rerun.
Other captured CLI shell outputs match originals. Pattern scans are not a
security certification.

## Decision

Retain the regression evidence; **do not promote an efficiency claim or replace
the featured chart**. No timeout, retry, excluded role or favorable replacement
was used. The token-cost objective and independent validation remain unfinished;
hosted release checks are a separate unresolved requirement.

Next optimization must target an observed avoidable operation while preserving
the actual consumer checks. Receipt's source/guide reads and Hostage's additional
before-fix work are concrete cost differences, not permission to remove required
evidence. Con Artist and Friday do not use their shipped helpers in this screen,
so helper microbenchmarks cannot explain their model costs. Do not repeat the
unchanged exposed screen until favorable or infer a global compression win from
the single Editor pair. Test a distinct mechanism locally before a newly frozen
small model comparison, then seek unexposed validation.

한국어: 16회 상세 검토를 마쳤다. 기능·파일 보존 기준은 양쪽 모두 충족했지만
무스킬 SQLite 실행에 작업 범위 위반이 있어 범위 포함 결과는 7/8 대 8/8이다.
이 차이를 일반적인 품질 우위로 주장하지 않는다. 스킬의 합산 토큰은 20.39%
늘고 시간은 5.17% 줄어 비용 목표에는 미달했다. 사후 테스트 대조는 모델 실행과
분리했다. 잘린 원본 출력과 불리한 결과도 보존하며 대표 그래프는 변경하지 않는다.
