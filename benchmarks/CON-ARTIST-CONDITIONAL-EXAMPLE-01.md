# Conditional stronger-probe example — 2026-09-15 KST

Parent `eca85cd`. The common Python audit example included a stronger probe but
omitted `probe_when`, so the helper's unchanged default always executed that probe
on correct and faulty code, even when existing tests already detected the fault.
The candidate adds `"probe_when":"survives"` to this example and clarifies that
requests to validate the stronger assertion regardless use `always` or omit the
field. No helper default, implementation, skill entrypoint or coverage rule changes.

`tests/test_audit_documented_probe.py` parses the actual first documentation recipe
and executes native checks in disposable project-local copies. It verifies actual
test binding, assertion failures, native test count, no timeout/output truncation,
original preservation and scratch cleanup, rather than matching instruction words.

| Test contract / requested probe | Native checks | Observed failure |
| --- | --- | --- |
| Acknowledgment-only test, conditional probe | 4 | Stronger persisted-list assertion |
| Persistence-sensitive test, conditional probe | 2 | Existing persisted-list assertion |
| Persistence-sensitive test, unconditional probe | 4 | Existing and stronger assertions |

The candidate test passes in 0.418s (three subcases). Replacing only the test's
read of the guide with `git show HEAD:skills/con-artist/references/python-audit.md`
from the parent reproduces exactly one failing subcase: the sensitive conditional
case instead runs four checks. Its original native checks still detect the fault;
this is avoidable execution, not a false pass. The checked-out guide is not reverted.

Regression checks: 76 mutation-helper tests pass in 13.605s and 12 build tests
pass in 3.300s. Skill validation, repository validation, featured-language sync
and whitespace checks pass. These supplement the parent revision's separately
recorded full-suite run; they do not relabel that run as this candidate's suite.

This demonstrates two unnecessary helper executions removed from one documented
workflow, not a new caching capability, a general 50% speedup or model-token gain.
The helper already supported conditional probes. Skipped probes remain explicitly
unvalidated; a nonzero mutant result still needs failure inspection. No model run,
independent real-user task, favorable retry or featured-chart update is involved.
Future model evidence must establish actual uptake and equivalent requested work.

한국어: 첫 실행 예제가 기존 조건부 검증 기능을 사용하도록 바꿨다. 기존 테스트가
실제 결함을 잡으면 실행 4회가 2회가 되고, 놓치면 추가 검증까지 4회를 유지한다.
추가 검증 자체의 확인을 요청한 경우도 4회를 유지한다. 문서 JSON을 실제 실행한
세 대조가 통과했고, 이전 문서는 불필요한 두 실행이 남는 것을 재현했다. 모델
토큰·시간 절감은 아직 미측정이며, 건너뛴 검증을 통과로 표시하지 않는다.
