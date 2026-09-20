# All-eight screen 03: functional success, efficiency target still unmet

2026-09-20. Launch `94da6b1`; skill resources `ee5eb28`.
[Protocol](../../ALL-EIGHT-CURRENT-03-PROTOCOL.md), [frozen inputs and schedule](run.json),
[native preflight](preflight.json), [all reviewed rows](comparison.json),
[separate author controls](author-controls.json).

Sixteen fresh GPT-6 Astra medium sessions completed: eight **previously exposed,
authored development tasks**, once per baseline/current arm. Serial execution,
alternating pair order, shared host/cache. No timeouts, account-limit stops,
excluded cells, retries or replacement runs. This is not held-out real-project
evidence, a significance test or a release readiness certificate.

Both arms meet all eight full-task and scope requirements. Current summed tokens
are **20.34% higher**, summed process wall time **3.61% lower**. Every individual
pair uses more tokens with the skill. None reduces both tokens and elapsed time.
This is **not an accepted overall efficiency improvement**. Existing featured
charts stay tied to their original experiments; no new broad performance claim.

## Every pair

Tokens are input plus output; cached input is included once, not added again.
Times are process wall seconds. Sums are accounting across heterogeneous tasks,
not causal or task-weighted estimates. Different extra checks also limit comparison.

| Role | Baseline tokens / seconds | Current tokens / seconds | Full task B/C |
| --- | ---: | ---: | --- |
| Necromancer | 86,366 / 52.561 | 90,729 / 60.185 | pass / pass |
| Receipt | 68,192 / 61.998 | 88,838 / 42.564 | pass / pass |
| Landlord | 63,355 / 34.051 | 66,556 / 39.337 | pass / pass |
| Mother-in-law | 64,747 / 43.404 | 71,078 / 48.883 | pass / pass |
| Exorcist | 63,558 / 53.122 | 67,940 / 43.851 | pass / pass |
| Hostage Negotiator | 87,521 / 125.181 | 131,015 / 111.098 | pass / pass |
| Con Artist | 65,592 / 67.318 | 91,363 / 80.831 | pass / pass |
| Friday | 65,694 / 66.942 | 72,451 / 59.615 | pass / pass |
| **Sum** | **565,025 / 504.577** | **679,970 / 486.364** | **8/8 / 8/8** |

## What actually ran

- **Necromancer:** introducing integer/rounding changes and current supported
  caller established; all nine independent current/A/B observations through the
  actual invoice function. Three native tests per variant, pass/pass/two expected
  failures. Both recover from unavailable `python` to `python3`; costs retained.
  Current uses exact AST substitution, baseline exact-once text replacement.
  Neither invokes the recently optimized excerpt helper.
- **Receipt:** same current five tests/schema against both full revisions, actual
  fresh-connection SQLite reads, two retry failures and three controls each.
  Both identify incomplete fix and clean copies. Current uses `compare.py` with
  whole-tree preservation and same-process import instrumentation. Baseline uses
  separate import/binding prechecks before native processes; those prechecks are
  not same-process instrumentation. Original source and copied traceback evidence
  support its conclusions. Neither uses the new optional `preserve.py` helper.
- **Landlord:** native two-test group and direct backend observations establish
  needed boolean/exception translation, original-value preservation and operational
  error propagation. Both leave staging unknown and discuss policy relocation.
  Current adds a consumer search; baseline rereads line-numbered source. Both
  have five shell commands in three outer calls, including final parallel checks.
- **Mother-in-law:** exactly two added tests, original initial-state test preserved,
  actual controlled persistence and full independent expected payloads. One native
  run each produces two passes and one real nested-payload assertion failure;
  later assertions remain in code and are honestly reported as unreached. Current
  first tries unavailable `python` (exit127), then runs with `python3`; baseline
  uses `python3` with bytecode disabled. Separate author copies reject the original
  and pass all three with a deep-copy correction. No production edit by the models.
- **Exorcist:** actual absent-environment native failure `3 != 1`, standalone
  pre-import environment control with one callback, and actual fixture timing.
  Baseline repeats three absent-env traces and uses a configured-startup test;
  current exercises actual setup/body then temporarily patches effective RETRIES.
  Neither invents cache causality or requires unspecified live configuration.
- **Hostage:** both add only latest-generation ownership guard in `finally`.
  Baseline five methods/subtests: four original failures, then five passes.
  Current eight methods: five original failures, then eight passes. No test
  framework collision, patch repair or scope expansion. Required overlap orders,
  failure/cancellation/retry, identity, prior state and isolation are covered with
  bounded owned-task cleanup. Current copies and uses `OwnedTasks` and sequences
  edit/native test in one interaction. Separate author checks reject broken owner,
  accept a valid counter-step alternative and pass the six-test author oracle on
  each delivered implementation. Method counts are not coverage scores. Different
  extra retry sequencing remains; current uses five outer calls, baseline four.
- **Con Artist:** all four native phases establish same-process test/endpoint/writer
  bindings. Existing acknowledgment tests survive commit omission; identical
  stronger full ordered row assertions pass correct code and fail on the missing
  binary row via fresh connections. Current additionally traces two actual calls
  per phase and strengthens/reruns both existing tests; baseline runs one separate
  stronger method. Copies and databases removed, originals preserved. Neither
  uses the changed collector, so its optimization is not measured here.
- **Friday:** both execute literal readers and actual scripts at all five phases,
  including no-op phase4, comparing full rows/columns and native BLOB bytes. OLD
  columns fail phases2–4 despite correct data; inactive NEW errors1/5 are not
  blockers. Down preserves committed writes. Current uses the optional matrix;
  baseline also checks backing table/view definitions. Proposed query/cutover
  mitigations are explicitly changes to the proposal, not executed repairs.

## Evidence and limitations

Each cell includes original CLI events, commands, answer, project snapshot,
metadata/source hashes, selected stored tool records, usage reconciliation and
exact skill-body exposure observations. Full original rollouts/private initial
instructions are **not exported**. All sixteen recorded usage totals reconcile.
Every current entry body exactly matches its installed resource before the first
tool; matching baseline bodies are unobserved, not proof of all-context absence.

Three CLI prefix omissions retain decisive evidence in matching original calls:

- Baseline Exorcist `item_3`: original tool-record line28 has absent-env native failure.
- Baseline Con Artist `item_4`: line30 has the correct original suite and all phases.
- Current Con Artist `item_6`: line37 has the correct original suite and all phases.

Landlord both arms, Exorcist current and Hostage current final checks have parallel
completion ordering different from original result-array order. Manual mappings
are retained in `comparison.json`; all mapped output/exit pairs match. An arbitrary
matching empty output is not accepted as command-correlated evidence. Separate
author replays never substitute for original model execution.

All original files/modes, dirty Receipt notes, ignored owner file, HEAD and installed
resources are preserved except authorized Editor test additions and Hostage repair.
Only permitted Hostage test/support files are extra. Privacy pattern scanning and
manual evidence review preceded publication; neither certifies universal correctness.

Four roles changed since screen02: Hostage, Receipt, Con Artist and Necromancer.
Unchanged Landlord, Mother-in-law, Exorcist and Friday variation is not attributable
to edits elsewhere. Do not compare old wall times as contemporaneous baselines.

## Decision after this screen

Do not promote this bundle as a general efficiency win, retune Receipt on the same
ledger/startup tasks, or rerun these unchanged eight tasks until favorable. The
new helper microbenchmarks did not translate into a demonstrated bundle win;
several helpers were not even used. Full helper-source reads, extra discovery and
additional model round trips are observed costs, not proof another generic prompt
rule will remove them. Future work needs a concrete repeated-work bottleneck in a
different realistic task, a scoped implementation change, and frozen equivalent
outcome/cost checks before measuring. Release/archive validation remains separate.

한국어: 동일한 개발용 8문제를 새 baseline과 비교한 결과, 양쪽 모두 작업·범위
요구는 8/8 충족했지만 스킬 토큰은 **20.34% 증가**, 시간은 **3.61% 감소**했다.
어느 문제에서도 토큰과 시간이 함께 줄지 않았다. 최근 도우미 개선을 사용하지
않은 작업도 많아 전체 성능 향상으로 해석할 수 없다. 실패·복구·추가 검증 비용과
CLI 누락을 원본 기록으로 확인해 보존했다. 기존 그래프를 교체하거나 이 결과를
일반적인 20–30% 개선으로 홍보하지 않는다. 같은 문제를 유리할 때까지 재실행하지
않고, 다른 현실적인 작업의 반복 비용을 근거로 다음 변경을 설계해야 한다.
