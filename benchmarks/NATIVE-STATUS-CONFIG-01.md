# Native status config01 — 2026-09-27

Parent `f3abda01`; prospective author driver compatibility correction, zero models.
The [earlier native capture](NATIVE-STATUS-CAPTURE-01.md) verified two legacy pytest
versions only. The remaining prepared modern source's terminal reporter supplies
both `report` and `config` to `pytest_report_teststatus`. Its hook specification
permits implementations requiring config. The previous prospective collector
supplied only report.

Using the unchanged supported-built pytest source from
[pytest11143 bootstrap](EXTERNAL-BUNDLE-02-PYTEST11143-BUILD.md), actual version
`8.0.0.dev53+g6995257c`, register a synthetic hook implementation that requires config
and asserts identity with its configured instance. The old call fails during native
execution with `HookCallError: hook call must provide argument 'config'`; the author
control then lacks the first call report and fails. Both stdout and stderr remain
retained. This is a real controlled compatibility failure, not a claimed failure
of any original selected issue cell or an ordinary default-plugin run.

The corrected collector supplies `config=self.config`. The same seven-state native
fixture and config-consuming hook pass on the modern source. Actual pytest2.8.7
and4.0.2 also pass with the extra argument; their hook dispatch tolerates it. Each
control requires the deliberately failing native fixture to exit1 and checks passed,
failed, skipped, XFAIL, XPASS plus setup/teardown categories. Author control exits0
only after these assertions. The original missing-config control exits1 and remains
recorded as adverse, not omitted from the four scheduled observations.

[All four observations](results/native-status-config-01/summary.json), original
stdout/stderr and exact executed controls are retained in
`results/native-status-config-01/`. [Git-free copied controls](results/native-status-config-01/git-free.json)
verify the corrected call across all three runtimes. Each native subprocess has a
30-second parent timeout. Old runtime plugin auto-loading qualifications still apply.
The modern runtime uses its existing owned Python3.11 interpreter and the pristine
prepared source path, not a gold project; no selected tests, grading labels or gold
are loaded. An initial fresh import without that source path failed because the
owned modern environment does not have pytest installed; the explicit supported
source path is therefore part of this control's required runtime configuration.

[Private driver identities](results/native-status-config-01/driver-check.json) retain
unchanged completion04 and separate config05 hashes. Only the hook call and output
directory change. The next driver syntax compiles; the external cohort remains
unexecuted. These native collector controls do not validate full grading, genuine
solver isolation, role quality or whole-task cost/time. No original grade, official
parser, skill, README, featured chart or hosted performance claim changes.

한국어: 현대 pytest에서 config를 요구하는 실제 훅 구현을 넣자 기존 상태 수집이
내부 오류로 실패했다. config 인자 전달 후 현대·구버전 두 개 모두 같은 상태
검사를 통과했고, Git 없는 복사본에서도 확인했다. 기존 실패를 보존하고 별도
다음 드라이버만 수정했다. 전체 외부 과제·모델 비교는 미실행이며 전체8개 역할
토큰·속도·품질 개선 증거는 아니다.
