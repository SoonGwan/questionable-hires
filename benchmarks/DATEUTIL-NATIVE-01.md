# Dateutil native audit01 — adoption, but not an efficiency win

Reviewed2026-09-21. Launch `fcd6c1e`; prior `1fa230c`, current `387c53b`.
[Frozen protocol](DATEUTIL-NATIVE-01-PROTOCOL.md),
[preflight](DATEUTIL-NATIVE-01-PREFLIGHT.md),
[all original-session exports](results/dateutil-native-01/),
[machine-readable comparison](results/dateutil-native-01/comparison.json).

**All three arms meet the five explicit criteria. Current actually uses the
native helper, but total tokens increase. Do not promote this as an efficiency
win or replace the featured chart.** One author-inspected upstream-source task,
n=1 per arm, shared host/cache, fixed serial prior/baseline/current order.
No timeout, account limit, retry, exclusion or replacement attempt occurred.

| Condition | Input | Cached subset | Output | Total | Seconds | Responses | Native processes / method executions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Prior |108,980|91,776|2,470|111,450|87.801|5|12 /12|
| Baseline |78,956|55,936|2,617|81,573|93.376|4|12 /12|
| Current |121,429|98,688|2,047|123,476|79.875|5|8 /12|

Current versus prior: **tokens+10.79%, time−9.03%**.
Current versus baseline: **tokens+51.37%, time−14.46%**.
Cached input is already included in input. Original response counters reconcile
with CLI totals in every arm. Wall time is the whole model process, not isolated
test execution or a causal estimate of helper savings. No dollar estimate.

## Original execution review

Every arm observes the unchanged selected tests on correct code and all three
independent faults. Day-cap and same-weekday faults survive both selected tests;
omitted-month fault fails `testNextMonth` and passes `testNextFriday`. All arms
reuse the two unchanged upstream witnesses: leap-year February end and same-day
Wednesday. Each witness passes correct code and fails its matching fault with
the intended `AssertionError`. No import/setup error or skip is counted as a kill.

- Prior writes a temporary `sitecustomize.py`, wrapping real unittest execution
  and assertions. It verifies copied test/implementation paths, imported class
  identity and `__add__` code path. Twelve individually selected native processes
  cover the same12 method executions; selected correct controls are reused.
- Baseline appends instrumentation to the disposable copy's `tests/__init__.py`,
  not the selected test bodies. It checks copied class/source identity and wraps
  assertions to print actual/expected operands. It also uses12 individual native
  processes for12 methods and identifies reused correct controls. Original
  initializers and all original files remain unchanged.
- Current reads the new native recipe, probe guide, advanced `src/` section,
  common contract and selected helper source matches. It invokes the production
  helper once with five batch entries: three faults against the two-method
  selected suite, followed by two fault/witness selections. It uses no probe-file
  mode. The selected suite has one correct execution, two later explicit correct
  references, and three mutant executions. Witness pairs add four processes.
  Thus8 processes execute12 methods, including every required assertion.
  Same-process precheck verifies all four methods' class globals and copied
  `__add__` path. Native suite results and real assertion failures are retained.

All mutations are confined to `relativedelta.__add__`; selected test file bytes
remain unchanged in copies. Prior/baseline also check AST equivalence outside that
method. Current's actual replacement strings are in the original command, and
its copied-source hashes distinguish each fault. Interpreter/startup/assertion
instrumentation differs; these are not untouched execution environments.
Process reduction is observed workload organization, not a coverage improvement
or proof of whole-task efficiency. Grouped suite method results were allowed by
the task; individual exit codes for every method were not required.

Original records show native assertions, cleanup and preservation—not author
replay. Author post-run inspection additionally confirms every supplied file's
bytes/mode, original HEAD, unchanged installed skill resources and no extra root
scratch/artifacts. Models' own before/after inventories include Git metadata;
current enables authorized `guard_project`. There is no pre-session binary-index
snapshot, so do not claim author-verified binary index identity across the session.

## Exposure, capture and limitations

Both skill arms contain their exact entry body in initial recorded skill messages
and reread it later. Baseline has no matching current body observation; that is
not proof of absence of all other context. Prior never reads/invokes the helper
or optional guides. Current's actual recipe read and helper invocation establish
adoption in this one case, unlike preceding edit/plan comparisons.

Eleven CLI shell outputs reconcile with stored original outputs:9 exact matches
and2 unique equal-exit nonempty suffix matches. Prior item5/original line38 omits
199 redacted characters of initial copy/command labels; baseline item4/line30
omits233 characters of first cwd/command labels. Actual first binding, assertions,
result and exit remain in CLI output. Full original tool records retain both
prefixes. No unmatched commands/outputs or duplicate/missing call records were
found. Current's four outputs match exactly; helper outputs report no truncation.

Raw full sessions remain private with mode0600. Public exports include redacted
tool records, usage/exposure/capture summaries, source snapshots with upstream
LICENSE/AUTHORS, answers and commands. Privacy-pattern scan has no hits and
manual review found task-local work plus the authorized interpreter/resources;
this is not a security certificate. No private initial instruction text is exported.

The task is one selected upstream tree with author-chosen faults, not a complete
dateutil suite, independent holdout or all-eight benchmark. Serial order/cache
and n=1 prevent strong causal or statistical claims. No new full-suite or hosted
CI result follows from this experiment.

## Decision and next mechanism

The new route is discoverable in this case, and native orchestration is genuinely
used. However, do not equate adoption or fewer processes with the requested token
efficiency. Current reads multiple guides including probe-file details despite
only reusing existing witness tests. A targeted next candidate can make those
already-supported native selections and source roots self-contained in the
native recipe, while preserving optional detail and justified inspection.
This is a testable next mechanism, not an estimated saving or a rule forbidding
reads. Check previous guide/routing failures before editing; do not retune and
report this exposed project as a fresh validation set.

한국어: 세 조건 모두 필수 검증5개를 충족했다. 현재 스킬이 실제 배치 도구를
사용해 같은12개 테스트 실행을8개 프로세스로 처리했다. 하지만 무스킬 대비
토큰+51.37%, 시간−14.46%로 비용 목표에는 미달이다. 여러 안내 문서 읽기가
관찰됐으며 실행 수 감소를 전체 성능 향상으로 포장하지 않는다. 불리한 결과도
보존했고 대표 그래프는 변경하지 않았다.
