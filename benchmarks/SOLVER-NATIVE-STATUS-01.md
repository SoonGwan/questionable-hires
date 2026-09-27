# Solver native status01 — 2026-09-27

Parent `01073474`; author-only Linux compatibility check, **zero model calls or
selected issue tests**. The [model authorization request](SOLVER-EXECUTION-ENVIRONMENT-REQUEST-01.md)
remains pending. This is an independent grading-support prerequisite; it does not
perform the rejected model uname call or substitute native execution for model
authorization. No approval settings or annotations changed.

[Previous status config01](NATIVE-STATUS-CONFIG-01.md) checked the seven-state
collector on two installed legacy pytest versions and modern pytest on Mac.
[Earlier Linux native controls](SOLVER-NATIVE-CONTROLS-01.md) checked normal and
deliberate assertion failure on the eight source trees. Neither covered these
status categories on all four actual project-local Linux pytest versions.

[Collector](results/solver-native-status-01/status-run.py) copies the prior exact
Capture class, including the config-consuming hook and matching configured
instance. [Seven-state fixture](results/solver-native-status-01/test_states.py)
is unchanged from status-capture01. An explicit empty config, disabled plugin
autoload/cache, plain assertions and control-local confcutdir avoid running
project conftest/configuration or designated issue regressions. Fresh isolated
Python3.9 processes import each actual `/solver/<issue>/src` pytest source; legacy
cases retain their existing `/runtime-compat` dependencies. Tests and logs are
created only under the guest's owned `/solver/status-controls` directory.

[Author controller](results/solver-native-status-01/control.py) reuses the existing
Guest serial transport directly for this fixed native experiment, with no MCP
server or model. [Pre-execution manifest](results/solver-native-status-01/launch.json)
freezes four scheduled issues and source/control/server hashes. No git discovery,
grading labels, gold patches, private case logs or histories are inputs. Each
request has10-second timeout; VM retains its45-second lifetime. Native test logs
are retrieved losslessly in bounded chunks, with no truncated response accepted.

[All four original outcomes](results/solver-native-status-01/result.json):

| Source identity | Actual pytest | Native test exit | Collector control |
| --- | --- | --- | --- |
| pytest5221 |4.4.2.dev174+g4a2fdce6|1|PASS|
| pytest5103 |4.5.1.dev40+g10ca84ff|1|PASS|
| pytest6116 |5.2.3.dev198+ge670ff76|1|PASS|
| pytest11143 |8.0.0.dev53+g6995257c|1|PASS|

Each control requires passed/failed/skipped/xfailed/xpassed call categories,
setup and teardown error categories, and native exit1. XPASS's native outcome is
passed in these versions, while the category remains xpassed. Author control0
means these deliberately mixed outcomes are classified correctly, not that all
tests passed. Logs retain their actual assertion and fixture-error diagnostics:
[5221](results/solver-native-status-01/pytest-dev__pytest-5221.log),
[5103](results/solver-native-status-01/pytest-dev__pytest-5103.log),
[6116](results/solver-native-status-01/pytest-dev__pytest-6116.log),
[11143](results/solver-native-status-01/pytest-dev__pytest-11143.log).
[Complete guest console](results/solver-native-status-01/guest.log) and result
observe graceful guest stop and exact probe absence, elapsed10.791s. No retry or
replacement run. No complete original issue grading, official parser acceptance,
model authorization, host-tool exclusion or all8 quality/cost/time claim follows.
Ordinary skills, README, frozen featured charts and hosted site stay unchanged.

한국어: Mac의 이전 상태 수집 검사와 Linux의 일반 성공/실패 검사에서 빠져 있던
네 가지 프로젝트 pytest의 상태 분류를 실제 게스트에서 확인했다. 동일한7상태
fixture·수집 클래스와 실제 source import를 사용해 모두 통과했고, 의도적인
테스트 실패 종료코드1도 그대로 보존한다. 모델·선택 이슈 실행은0회이며 승인
거절을 대신 실행하거나 전체 성능 개선으로 바꾸지 않는다.
