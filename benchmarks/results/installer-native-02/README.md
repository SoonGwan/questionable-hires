# Native routing screen 02 — reviewed 2026-09-15 KST

**Tool-selection adoption observed; whole-task gains remain mixed.** Launch and
skill resource `89a45f5`. The [single routing change and preregistration](../../CON-ARTIST-NATIVE-ROUTING-01.md)
follow the [adverse transfer 01](../installer-audit-01/README.md). Same frozen two
authored tasks, four fresh sessions, Astra medium, serial, n=1 per arm/case, no
author reruns, exclusions or timeouts. [Manifest](run.json), [metadata](summary.json).

| Task | Baseline tokens | Skill tokens | Change | Baseline seconds | Skill seconds | Change |
|---|---:|---:|---:|---:|---:|---:|
| Copy-error rollback | 87,959 | 96,380 | +9.57% | 79.966 | 71.392 | −10.72% |
| Cancellation | 144,153 | 127,451 | −11.59% | 117.751 | 87.458 | −25.73% |

Total tokens = input (cache included once) + output; full process elapsed time.
Against the historical previous skill, rollback tokens/time fall 53.48%/17.72%;
cancellation tokens fall 17.10% but time **increases 7.71%**. These are observations,
not isolated causal effects. The fresh cancellation baseline also repairs a failed
diagnostic callback, so its total includes extra work. Keep that failure and cost.

Both skill sessions now use native unittest directly with project-local copies,
without reading the helper guide/source or repeating helper CLI recipes. Command
counts are 4/6 (rollback/cancellation), versus 12/11 in transfer 01. No command-count
target was imposed and fewer commands alone is not success. All four final audits
provide real defect detection; no stronger probe is needed for already-killed faults.

## Original evidence review

- Rollback [skill item_5](installer-audit-rollback--skill--1/commands.json) and
  [baseline item_4](installer-audit-rollback--baseline--1/commands.json): both move
  rollback registration after copying. Both execute a four-test correct suite
  (4 pass, exit 0), four-test faulty suite (1 pass/3 fail, exit 1), plus eight
  single-method processes with matching exits. Sixteen native test executions
  per session, with no setup errors/skips. Actual failures at lines 278/303 show
  leftover `receipt`; line 325 observes `['necromancer']` cleanup attempts instead
  of `['receipt', 'necromancer']`. Same-process trace/path evidence establishes
  copied implementation execution and filesystem effects.
- Cancellation [skill items 5/6/8](installer-audit-cancellation--skill--1/commands.json):
  only the outer handler changes `BaseException` to `Exception`. Eight individual
  processes, then both four-method suites: correct 4 pass/exit 0; faulty 3 pass,
  one actual line-303 assertion failure/exit 1. No setup errors. Trace shows both
  targets left behind and marker content `keep`, while exception identity passes
  before the detecting assertion. Copied code/module paths and ROOT are checked
  in the actual executing process, not a separate import-only process.
- Cancellation [baseline item_5](installer-audit-cancellation--baseline--1/commands.json)
  initially overrides `addFailure` to read the destination after unittest cleanup.
  Both faulty grouped/individual cancellation runs abort with `FileNotFoundError`
  in that diagnostic, not usable native detection summaries. Other checks execute;
  all original outputs and costs remain. Item_7 repairs the callback by using the
  standard result handler and observing state at installer exit. It reruns all ten
  processes, establishing 4-pass correct / 3-pass, 1-fail mutant suites and matching
  individual exits, actual line-303 assertion, copied execution and marker bytes.
  This is model-in-session recovery, not author replacement evidence.

The requested per-method process exits account for individual checks. Grouped
suite + individual methods duplicate executions but satisfy the same explicit
task. The cancellation baseline's initial aborted runs make total work unequal.
Only four authorized test methods ran. Disk/cancellation errors are injected by
existing tests, not physical disk exhaustion or real OS signal delivery. Other
interruption timings, cleanup combinations and clean-case false positives are not
measured. Two exposed tasks share one installer; no independent holdout, broad
eight-skill claim, reliable effect size or featured graph promotion is justified.

## Preservation and export

All 12 supplied final files match the frozen input bytes in each cell, with no
retained scratch. Original native commands also perform before/after checks:
rollback skill checks file hashes/modes; cancellation skill checks file set/hashes;
baselines check hashes/modes and rollback baseline also directory structure.
Installed skill resource manifests are unchanged. This is not whole-filesystem
race protection. The collector's shell exit is not a substitute for native exits.

Every original completed-command object/output and final usage reconciles with
the path-redacted export. Each source-hash manifest matches retained raw artifacts.
Full fixture files and unfiltered command streams are included. Native unittest
abbreviates long paths/diffs; model traces retain actual leftover entries. No
author replay was used to repair missing native evidence or score a synthetic kill.

Decision: keep proportional tooling provisionally; it removed observed helper
adoption overhead without losing these faults. Do not repeatedly tune these exposed
installer cases. The next useful comparison must move to a different workflow and
include tasks where the helper's capabilities matter, to check under-use as well
as overhead. Overall goal remains unmet; charts stay frozen.

한국어: 도우미 강제 도입을 줄인 안내는 두 실행에 반영됐다. 새 기본 모델 대비
오류 과제는 토큰 +9.57%·시간 −10.72%, 취소 과제는 토큰 −11.59%·시간 −25.73%다.
이전 스킬보다 토큰은 두 과제 모두 감소했지만 취소 시간은 증가했다. 기본 모델의
취소 비교에는 진단 코드 오류·복구 비용도 포함되므로 일반적 25% 향상 주장은
불가하다. 실제 결함 탐지·원본 보존은 확인했고 모든 실패 기록을 남겼다. 후보는
잠정 유지하되 같은 문제 반복 대신 다른 작업 및 도우미가 필요한 작업으로 검증을 넓힌다.
