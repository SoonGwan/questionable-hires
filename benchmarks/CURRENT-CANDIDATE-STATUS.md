# Current candidate: whole-task performance remains unproven

The objective covers all eight hires: materially better real developer outcomes
at similar or lower token/time cost. Reliability fixes, passing tests and helper
microbenchmarks do **not** satisfy that objective. Recent work strengthens tools;
it has not established a broad 20–30% gain.

한국어 요약: 최근 오류 방지·도우미 개선은 검증됐지만, 8개 스킬 전체가 실제
개발에서 더 적은 토큰과 시간으로 좋은 결과를 낸다는 목표는 아직 미달이다.
개별 유리한 수치와 전체 성능을 구분하고, 불리한 결과도 그대로 보존한다.

## Evidence that determines the next work

- [Account-panel delivery transfer](results/mother-panel-01/README.md), Mother
  entry `eefc721`: **−40.38% tokens / −18.76% time**, five native tests pass per
  arm, direct project-test delivery without helper duplication. Author fault replay
  reveals both arms shadow unittest.fail and lose intended assertion diagnostics;
  not accepted equal-quality superiority. Name-only author repair verifies the
  cause. Later runner-method/failure-path guidance is not model-measured. N=1
  targeted synthetic task, not real-project or all-eight confirmation.
- Latest [all-eight explicit-contract gate](results/bundle-contract-03/README.md),
  resources `557f012`: all 18 cells reviewed; **+16.17% tokens / −12.43% summed
  process time**. Core outcomes supported, one baseline scope violation and
  differing extra work retained. Exposed n=1 synthetic gate, not independent
  real-development confirmation or overall efficiency acceptance. QA duplication
  and caller-binding support are next concrete engineering targets.
- The earlier [nine-task combined comparison](BUNDLE-CURRENT-02-REVIEW.md)
  belongs to frozen revision `417bdac`, **not today's resources**. It records
  **+10.33% tokens / +23.08% summed process time**, with outcome differences.
  Revised-contract evidence above does not retroactively change it; old numbers
  cannot be relabeled as the newest version's performance.
- The recent [cookie audit pair](results/httpx-cookies-01/README.md), Con Artist
  `36e201c`, records **−13.93% tokens / −36.91% time** with correct core outcomes.
  Baseline repairs, different pytest settings/provenance and n=1 prevent an
  accepted equal-work or broad gain. The short test confirms routing adoption,
  not the large-file route's efficiency.
- [Receipt's current-bug pair](results/receipt-current-bug-01/README.md),
  `7e1e1db`, records **+34.16% tokens / +6.48% time** with more complete before
  evidence than baseline. Later helpers and final-check instructions do not
  retroactively improve this result; their whole-task cost effects are unmeasured.
- [Receipt frame parsing](results/receipt-frame-01/README.md), resources at
  `f13a097`: same supplied before/after coverage, 6 versus 3 shell calls, but
  **+4.01% tokens / +9.81% time**. Final-check batching is adopted without a
  measured saving on this new authored n=1 task. Instruction-loading overhead
  and applicability remain priorities; fewer commands alone are not acceptance.
- [Receipt seeded HTTPX fix](results/receipt-httpx-02/README.md), consolidated
  entry `f32de37`: identical final fix and required three-test before/after
  coverage; 8 versus 4 shell calls, but **+61.61% tokens / +112.05% time**.
  Extra context/inventory work, n=1 and shared conditions prevent causal claims;
  this actual-code seeded task does not support efficiency acceptance.
- [Uncommitted settings comparison](results/receipt-uncommitted-01/README.md),
  `75c8718`: both verify core failures/passes and preserve the initial working
  files; **+9.09% tokens / +3.38% time**. Receipt reads the new procedure but
  writes native comparison code instead of using its helper. Cleanup/extra-work
  differences and a missing output prefix remain explicit; no efficiency win.
- [Hostage atomic-export pair](results/hostage-atomic-export-01/README.md),
  `5867752`: −12.85% tokens / −8.43% time with correct core behavior. Both arms
  use two preparation calls; baseline cleanup work, additional skill exception
  coverage and fixture temporary-root inconsistency prevent a causal efficiency
  or strict-scope claim. Separate author contract replay passes both solutions.
- [Uncommitted graph comparison](results/receipt-graph-01/README.md), Receipt
  reference `077805c`: working-tree helper adopted, same six native tests and
  final cleanup, but **+15.49% tokens / +28.15% time**. Baseline interpreter
  repair and skill launcher-file cleanup remain included; n=1 is not acceptance.
- `benchmarks/featured.json` remains the source of the landing-page comparison.
  No recent reliability check replaces its frozen experiment or changes its
  charts. Historical adverse results remain available.
- [Range verification](results/receipt-ranges-01/README.md), `cf4c2c0`: watch/report
  adopted without a custom wrapper; same core seven-test coverage, **+43.79%
  tokens / −39.99% time**. Targeted synthetic n=1 and baseline's broader integrity
  work limit attribution; this tradeoff is not accepted overall efficiency.

## Current resource revisions and remaining gaps

Checked against Git at `1a7b72a`, with the Hostage candidate linked below. Entry/resource revisions are maintenance
identities, **not** necessarily the versions measured by linked experiments.
The eight characters and automatic selection remain intact; helpers are optional.

| Skill | Entrypoint / latest supporting-resource change | Evidence and unresolved work |
| --- | --- | --- |
| Necromancer | `51ce19e` / [presentation correction](NECROMANCER-PRESENTATION-01.md) after `3157ee2` | [Discovery](NECROMANCER-DISCOVERY-01.md), [packaging](NECROMANCER-PACKAGING-REVIEW-01.md), [decision gate](NECROMANCER-DECISION-GATE-01.md): configured consumer retained; favorable pairs have unequal work/capture limits; broader savings unproven. Git color/prefix regression is author-tested, not model-measured. |
| Receipt | `75c8718` / [reference consolidation](RECEIPT-REFERENCE-COMPACT-01.md) after `cf4c2c0` | [Ranges](results/receipt-ranges-01/README.md): earlier watch/report adopted, faster time but substantially more tokens; unequal extra work, no accepted overall gain. Smaller reference is not yet model-measured. [Graph](results/receipt-graph-01/README.md), [settings](results/receipt-uncommitted-01/README.md), [seeded HTTPX](results/receipt-httpx-02/README.md) and [frame](results/receipt-frame-01/README.md) remain adverse. |
| Landlord | `26a310d` / no separate resources | [Application-first discovery](LANDLORD-SOURCE-SCOPE-01.md), [compact regression](LANDLORD-COMPACT-01.md), [auth design](HTTPX-AUTH-DESIGN-01.md): useful consumer inspection but adverse comparisons/nonpaired costs; resource-path discovery remains. |
| Mother-in-law | [runner-method correction](results/mother-panel-01/README.md) after `eefc721` / helper `b7058c6` | [Panel transfer](results/mother-panel-01/README.md): delivery-first routing adopted, lower raw cost, but both generated suites have assertion-plumbing errors on faulty code. Author name-only repair validated; later guidance adoption unmeasured. [Whole gate](BUNDLE-CONTRACT-03-REVIEW.md), [native integration](results/mother-native-project-01/README.md) and [false-pass correction](MOTHER-SUCCESS-STATE-03.md) retain their historical limits. |
| Exorcist | `ca2e179` / `cb10067` | [Signal transfer](EXORCIST-SIGNAL-01.md), [provenance](EXORCIST-PROVENANCE-01.md): small favorable signal result has baseline repair/unequal work; normal path remains costlier in tokens. |
| Hostage Negotiator | `5867752` / no separate resources | [Atomic export](results/hostage-atomic-export-01/README.md): direct-read adoption, same preparation call count as baseline, qualified lower raw cost. [Packaging repair](PACKAGING-REPAIR-01.md) also has unequal coverage; [compact regression](HOSTAGE-COMPACT-01.md) and other tasks do not establish broad gains. |
| Con Artist | [assertion-path guidance](results/mother-panel-01/README.md#follow-up-con-artist-assertion-path-regression) after `36e201c` / helper [same-process precheck](CON-ARTIST-PRECHECK-01.md) | Author checks reproduce coroutine false passes and support errors; independent probe detects missing append. Helper unchanged; new interpretation guidance and precheck adoption/savings unmeasured. [Current gate](BUNDLE-CONTRACT-03-REVIEW.md), [cookies](results/httpx-cookies-01/README.md), [headers](results/httpx-headers-01/README.md) and [context](results/httpx-context-02/README.md) retain mixed costs and unequal-work limits. |
| Friday | `9cae27c` / `fc2c205` | [Input budget](FRIDAY-INPUT-BUDGET-01.md), [changed paths](CHANGED-PATHS-03.md), [branch transfer](FRIDAY-BRANCH-01.md): helper behavior and narrow favorable results; branch transfer costlier, broader improvement unproven. |

## Verification and release gates

- [Future fixture scratch policy](HOSTAGE-ATOMIC-TEMP-PREFLIGHT.md) corrects
  project-local temporary-output control without editing the measured export
  task. Actual creation-path preflight preserves two before failures/four after
  passes. No new model run or improvement claim follows from this correction.
- Local checkout at `1a7b72a`: **330 tests pass** (45.072 seconds). Catalog,
  resource links and featured/localization checks pass. Test count is not a
  model-performance metric or proof of target-assertion coverage.
- [Linux source archive](../docs/RELEASE-READINESS.md), `5b78fef`:
  **326 pass / two Git-history skips** (328 discovered), Python 3.12.3,
  network disabled, existing image/read-only PyYAML mount. No Git/local-run
  state or overlays. This predates the unknown-field validation change and is
  not a fresh dependency install or current host registration.
- Hosted run `34743404198` at `5b78fef`: all four jobs have zero steps. The
  archive annotation reports failed payments **or** a spending-limit issue.
  Private visibility was verified then. Owner authorization is required for
  billing/visibility/publication changes; no release has been authorized here.
- [Executable example](../examples/con-artist.md) and historical
  [installation evidence](../docs/INSTALLATION-TEST.md) are usable references,
  not current remote-installation or universal-superiority claims.

## Next acceptance work — full scope retained

1. Reduce demonstrated end-to-end work on real developer tasks across all eight
   hires while preserving required behavior, scope and character identities.
   Prioritize observed unnecessary discovery, repeated setup and missing checks;
   do not substitute more helper tests for this outcome.
2. Freeze fewer than ten development tasks, versions and criteria before running.
   Compare contemporary baselines at equivalent requested outcomes; verify
   interpreter, runner settings and provenance requirements. Retain every cell,
   repair, failure and differing workload. Do not rerun exposed tasks for scores.
3. Use a separate confirmation set and a current combined all-eight gate.
   Inspect actual assertions, artifacts, scope, capture quality and costs. Total
   tokens include cached input once plus output; missing usage is not zero.
   Reused observations are not independent executions or causal savings.
4. Finish release/installation gates for the intended revision with owner
   authorization. Local tests cannot substitute for hosted CI or publication.

## Preserved detail

The [September 13 development archive](CANDIDATE-DEVELOPMENT-2026-09-13.md)
preserves the previous 400-line status page byte-for-byte, including all adverse
results and intermediate test counts. Its uses of “current” refer to their
historical entries. The [earlier development log](CANDIDATE-DEVELOPMENT-LOG.md)
and linked raw experiment reports remain intact. No experiment was deleted or
re-scored by this summary update.
