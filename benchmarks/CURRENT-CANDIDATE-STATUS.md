# Current candidate: whole-task performance remains unproven

The objective covers all eight hires: materially better real developer outcomes
at similar or lower token/time cost. Reliability fixes, passing tests and helper
microbenchmarks do **not** satisfy that objective. Recent work strengthens tools;
it has not established a broad 20–30% gain.

한국어 요약: 최근 오류 방지·도우미 개선은 검증됐지만, 8개 스킬 전체가 실제
개발에서 더 적은 토큰과 시간으로 좋은 결과를 낸다는 목표는 아직 미달이다.
개별 유리한 수치와 전체 성능을 구분하고, 불리한 결과도 그대로 보존한다.

## Evidence that determines the next work

- The latest completed [nine-task combined comparison](BUNDLE-CURRENT-02-REVIEW.md)
  belongs to frozen revision `417bdac`, **not today's resources**. It records
  **+10.33% tokens / +23.08% summed process time**, with outcome differences.
  A new current all-eight confirmation is missing; old numbers cannot be
  relabeled as the newest version's performance.
- The recent [cookie audit pair](results/httpx-cookies-01/README.md), Con Artist
  `36e201c`, records **−13.93% tokens / −36.91% time** with correct core outcomes.
  Baseline repairs, different pytest settings/provenance and n=1 prevent an
  accepted equal-work or broad gain. The short test confirms routing adoption,
  not the large-file route's efficiency.
- [Receipt's current-bug pair](results/receipt-current-bug-01/README.md),
  `7e1e1db`, records **+34.16% tokens / +6.48% time** with more complete before
  evidence than baseline. Later helpers and final-check instructions do not
  retroactively improve this result; their whole-task cost effects are unmeasured.
- `benchmarks/featured.json` remains the source of the landing-page comparison.
  No recent reliability check replaces its frozen experiment or changes its
  charts. Historical adverse results remain available.

## Current resource revisions and remaining gaps

Checked against Git at `1a7b72a`. Entry/resource revisions are maintenance
identities, **not** necessarily the versions measured by linked experiments.
The eight characters and automatic selection remain intact; helpers are optional.

| Skill | Entrypoint / latest supporting-resource change | Evidence and unresolved work |
| --- | --- | --- |
| Necromancer | `51ce19e` / `3157ee2` | [Discovery](NECROMANCER-DISCOVERY-01.md), [packaging](NECROMANCER-PACKAGING-REVIEW-01.md), [decision gate](NECROMANCER-DECISION-GATE-01.md): configured consumer retained; favorable pairs have unequal work/capture limits; broader savings unproven. |
| Receipt | `10d416f` / `3f936bf` | [Current-bug](results/receipt-current-bug-01/README.md), [invoice](results/receipt-invoice-01/README.md), [scope recheck](results/receipt-scope-recheck-01/README.md): higher recorded tokens or unpaired evidence. Recent bounded reads and empty/skip detection are tool behavior, not end-to-end gains. |
| Landlord | `26a310d` / no separate resources | [Application-first discovery](LANDLORD-SOURCE-SCOPE-01.md), [compact regression](LANDLORD-COMPACT-01.md), [auth design](HTTPX-AUTH-DESIGN-01.md): useful consumer inspection but adverse comparisons/nonpaired costs; resource-path discovery remains. |
| Mother-in-law | `b7058c6` / `b7058c6` | [Native integration](results/mother-native-project-01/README.md), [false-pass correction](MOTHER-SUCCESS-STATE-03.md): native runner reuse works on authored variants; unequal coverage/fixture defects limit lower recorded costs. |
| Exorcist | `ca2e179` / `cb10067` | [Signal transfer](EXORCIST-SIGNAL-01.md), [provenance](EXORCIST-PROVENANCE-01.md): small favorable signal result has baseline repair/unequal work; normal path remains costlier in tokens. |
| Hostage Negotiator | `6c5e452` / no separate resources | [Packaging repair](PACKAGING-REPAIR-01.md), [compact regression](HOSTAGE-COMPACT-01.md), [command transfer](HOSTAGE-COMMAND-01.md): modest favorable packaging pair has unequal coverage/test repairs; other tasks adverse. |
| Con Artist | `36e201c` / `1a7b72a` | [Cookies](results/httpx-cookies-01/README.md), [headers](results/httpx-headers-01/README.md), [qualified context](results/httpx-context-02/README.md): real adoption, mixed costs and unequal work. Latest schema, no-execution and evidence-retention guards are not measured model gains. |
| Friday | `9cae27c` / `fc2c205` | [Input budget](FRIDAY-INPUT-BUDGET-01.md), [changed paths](CHANGED-PATHS-03.md), [branch transfer](FRIDAY-BRANCH-01.md): helper behavior and narrow favorable results; branch transfer costlier, broader improvement unproven. |

## Verification and release gates

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
