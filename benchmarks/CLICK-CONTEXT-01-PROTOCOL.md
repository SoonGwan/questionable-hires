# Click nested-context audit 01 — freeze before model calls

2026-09-21. One author-selected real-source audit, no-skill baseline then current
Con Artist, one fresh serial GPT-6 Astra medium session each, 360 seconds each.
Click `6aabf099bfdd4c1e75fe8d0e0d4241372b988ab1`; skill snapshot `f253f38`.
This is neither an independent holdout nor an organic production bug report.

The neutral request and five criteria live in `run_click_context_01.py`. They ask
for actual nested-resource propagation/unwind sensitivity, existing correct/faulty
tests, additional assertions only if needed, neighboring controls, native copy
binding, source preservation and scratch cleanup. The author oracle, mutation
implementation and identified missing scope are not model inputs. No helper
adoption is required. No skill instruction candidate is being tested yet.

[Native preflight](CLICK-CONTEXT-PREFLIGHT-01.md) demonstrates existing 30 tests
passing correct/faulty code, then identical author checks producing 3 passes
correct and 1 actual assertion failure / 2 passes faulty. It uses the real Click
runtime. Freeze full output, interpreter/package versions, task/criteria, source
and skill digests and runner input hashes before launch. Source checkout must be
clean and pinned. Use the existing Python 3.11 environment; no dependency installs.

Preparation: invoke `run_click_context_01.py --source <pinned-checkout> --output
<new-local-run>` with the designated interpreter. Commit inputs before adding
`--execute`. Exclusive execution marker prevents restarting a measured pair;
observe a live handle instead. Keep failed, timed-out and unattempted cells.
No retries, substitutions, task/criterion edits or favorable-outcome selection.
Account limits stop remaining calls. There are no delegated workers.

Review original calls/results/artifacts against every criterion. Green exits,
test counts or an import-only precheck do not replace assertion/binding evidence.
Inspect recorded initial skill exposure and recover CLI omissions only from the
matching original records, never substitute replays. Preserve private sessions
locally but export no private initial messages. Author mutation/replay is separate.

Report each cell's input tokens (cache included once) plus output, process wall
time, responses, shell commands, extra reads, repairs and any unequal work. One
task, n=1, fixed order/shared host and unblinded author review cannot establish
causal or general percentage savings. Do not promote it into featured graphs.
Only an observed failure or repeated-work bottleneck justifies a later candidate;
do not prescribe the known answer as a new universal skill rule.

한국어: 실제 Click 소스의 감사 과제를 무스킬과 현재 스킬로 한 번씩 비교한다.
정답·작성자 변이·보강 검사는 모델에게 제공하지 않는다. 실패와 복구 비용도
보존하며 단일 유리한 결과를 전체 성능 개선이나 배포 완료로 주장하지 않는다.
