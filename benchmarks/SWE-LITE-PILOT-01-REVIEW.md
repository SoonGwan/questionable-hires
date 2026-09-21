# SWE-Lite pilot01: both fixes pass; no broad efficiency win

2026-09-22. Measured eight-skill resource **`8ee6c56`**, runner **`796926e`**,
GPT-6 Astra/medium, CLI0.153.4. Two public external issues, one pair each, reversed
order. [Frozen protocol](SWE-LITE-PILOT-01-PROTOCOL.md),
[reviewed evidence](results/swe-lite-pilot-01/run.json).

**Decision:** both conditions resolve both required issue contracts. Summed
tokens decrease only0.71%; wall time increases2.43%. Pytest's broader validation
also encountered a fixture-induced path problem in both conditions. Do not
promote this as a clean efficiency comparison, general skill benefit,20–30%
improvement or release-readiness proof. Featured charts remain unchanged.

## Original model observations

| Task | Baseline tokens | Current tokens | Change | Baseline seconds | Current seconds | Change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Requests bytes method |164,972 |133,027 |−19.36% |70.735 |64.611 |−8.66% |
| pytest skip location |240,489 |269,575 |+12.09% |94.360 |104.489 |+10.73% |
| Sum |405,461 |402,602 |−0.71% |165.095 |169.100 |+2.43% |

Tokens=input including cached input+output; cache is not added twice. Times cover
the runner/container lifecycle as predeclared, not author grading. Matching
private session counters reconcile with each original CLI total; all4 sessions
completed without timeouts, account limits, OOM or missing session captures.
No model cell was retried. These descriptive single pairs cannot separate skill
effects from stochastic behavior, cache/order, different verification choices or
the disclosed fixture problem.

Before these cells, the first execution envelope stopped at service readiness
exit127 (`python` absent; `python3` available). All4 were unrun. Its
[record](results/swe-lite-pilot-01/pre-model-failure.json) remains; the corrected
launch02 is a new exclusive envelope. It is not a discarded model answer.

## Separate native grading

Each unchanged model patch was applied to a new private grader using the pinned
dataset eval/test patch and reviewed official parser extraction. Setup succeeded,
fresh package imports were project-local, and collection hooks checked the
actual test-module/package bindings in the same native process. No gold patch
was substituted for a model patch. Raw logs containing hidden tests stay private;
patch/log hashes, setup evidence and counts are in the
[grading summary](results/swe-lite-pilot-01/grading-summary.json).

| Task | Baseline required checks | Current required checks | Outer native result |
| --- | ---: | ---: | --- |
| Requests |141/141 |141/141 |143passed in each condition |
| pytest |78/78 |78/78 |79passed in each condition |

Required labels have no failures, errors, missing or skipped results. Extra
native items are not extra scored obligations. Requests'8 nominal fail-to-pass
labels contained only1 distinguishing base failure in the corrected runtime.
Pytest self-tests intentionally run failing child suites; those child summaries
are not failures of the enclosing79-test native run. This uses the selected
official parser functions, not the full official harness/leaderboard workflow.

## Scope, verification and adoption

- Both Requests patches make the same implementation change, using the existing
  native-string conversion helper. Baseline adds byte GET/POST cases; current
  adds byte/text GET cases. Original model logs show pre-fix failures and14/26
  passing selected checks afterward respectively. Neither claims the full suite
  or Python2.6/3.4 verification during its own session.
- Both pytest patches make skip-location handling independent of the xfail
  branch and add6 focused cases. Current also expands an existing explicit-skip
  check. Both original sessions reproduce3 pre-fix failures/3passes, then broader
  verification and original-implementation controls. Their reported remaining
  runner-test failures are real, not hidden by the later grader pass.
- Requests/baseline explicitly searches `/run` for `AGENTS.md` in addition to the
  project. This is a project-only scope deviation. Recorded output does not show
  credential contents; do not inflate it into an observed secret disclosure.
  No comparable outside-project search or upstream solution lookup is observed
  in current's recorded commands. Absence in traces is not enforced isolation.
- Both current sessions expose all8 catalog entries and read the complete
  **receipt** body via a tool. Neither invokes a bundled helper in the recorded
  tool calls. No other full skill body is observed. Baseline's recorded initial
  messages have no matching entries from our eight-skill catalog. This confirms
  routing/exposure here, not the effect of all8 roles or every possible context.
- Installed resources are unchanged. Although Git index bytes changed, retained
  before-model/pre-collector indexes have identical staged entries, and HEAD is
  unchanged in all4 cells. Byte refresh is not evidence of staging or a commit.

Details: [reviewed command/exposure/index observations](results/swe-lite-pilot-01/review.json),
with per-cell CLI events, tool records, usage, answers and patches in the evidence
directory. Issue bodies, private initial instructions, raw auth and hidden test
logs are excluded. Upstream license files accompany Requests/pytest evidence.

## Post-run fixture limitation: broader pytest tests

The empty config at `.git/qh-tmp` prevented inheritance of the outer repository's
strict options and let the predeclared77-test skipping file pass. It does **not**
fully reproduce system-temp behavior for neighboring runner tests: their nested
projects inherit that temporary config root, changing expected relative paths.
Both models expanded validation to `testing/test_runner.py`, hit the same3
path-expectation failures, and spent additional work checking original behavior.

This defect was discovered in post-run trace review; the automated OOM/lifecycle
gate did not catch semantic fixture failures during model execution. The fixed
schedule therefore already completed before the author recognized it. Do not
rewrite frozen inputs, subtract investigation tokens/time, drop pytest, or rerun
this pair and call it fresh validation. Required issue grading still passes, but
the cost comparison is confounded and neither model's broader suite is wholly
green. A future environment must test neighboring native behavior as well as
the hidden-label file; these exposed cases are now development cases.

## Next action

The bundle selected Receipt automatically, but its added machinery was not used.
Inspect actual verification/context costs before changing the skill; do not
force helper invocation or optimize an expected answer to these two bugs. Any
future skill change needs a concrete mechanism and separately selected validation.
Do not turn the favorable Requests pair into the headline while omitting pytest.
The owner's broad efficiency/usefulness objective remains unfinished.

한국어: 두 조건 모두 Requests141개/pytest78개 기준 검사를 통과했다. Requests에서는
스킬 조건이 적은 비용을 썼지만 pytest에서는 더 썼다. 합계는 토큰−0.71%, 시간+2.43%로
큰 개선이 아니다. 양쪽 pytest가 실험용 임시 경로 설정 때문에 추가 테스트 실패와
진단 비용을 겪은 한계도 보존한다. 현재 조건은 Receipt만 읽었고 helper를 실행하지
않았다. 유리한 한 쌍만 홍보하거나 같은 과제를 고쳐 재실행한 결과를 독립 검증으로
바꾸지 않는다. 기존 그래프·전체 개선 주장·공개 배포 상태는 변경하지 않는다.
