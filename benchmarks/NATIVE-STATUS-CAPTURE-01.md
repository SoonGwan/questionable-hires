# Native status capture01 — 2026-09-27

Parent `8588e20b`; ordinary skills unchanged. This is an author grading correction,
not model evidence, an adopted efficiency optimization or a replacement grade.

The earlier [file-probe01](EXTERNAL-BUNDLE-02-FILE-PROBE-01.md) reconstructed test
statuses from `report.outcome` and `wasxfail`, incorrectly counting legacy XPASS as
failure. The original driver and recorded outcomes remain unchanged. A separate
future private driver captures the category returned by the installed native
`pytest_report_teststatus` hook, as these versions' terminal reporters do, rather
than inferring it from a generic report outcome.

[Actual control source](results/native-status-capture-01/control.py) and
[seven-test fixture](results/native-status-capture-01/test_states.py) check passing,
failing, skipped, XFAIL and XPASS calls, plus setup and teardown errors. The native
suite deliberately exits1; the author control exits0 only after asserting every
expected category and both error phases. Actual/expected failure values appear
in the retained output. Each subprocess has a30-second parent timeout and runs in
a fresh owned directory. It neither imports selected issue projects nor uses gold,
required labels, network service fixtures or any model.

| Actual runtime | Native XPASS outcome | Native category | Control |
| --- | --- | --- | --- |
| pytest2.8.7 / Python3.9.6 | `failed` | `xpassed` | PASS |
| pytest4.0.2 / Python3.9.6 | `passed` | `xpassed` | PASS |

The first2.8 control failed because its fixture used `pytest.mark.skip`, unsupported
by this installed legacy runner; that test actually passed. Preserve the initial
failure in `requests28-first.txt`. The corrected fixture uses native `pytest.skip`
inside the test. This correction precedes any new issue grading; it does not amend
older frozen tests or counts. Both corrected controls pass in checkout and again
from copies without Git history; source bytes remain unchanged. Old pytest still
loads its installed httpbin/mock plugins despite the modern auto-load environment
flag; neither supplied control requests their service fixtures. No runtime catalog
parity or general plugin isolation is claimed.

[Future driver check](results/native-status-capture-01/driver-check.json) records
original/future private driver hashes and unchanged original bytes. The new driver
syntax compiles, stores native categories, fails on unknown nonempty categories,
and prioritizes setup/teardown errors and failures over successful phases. It has
**not executed the external cohort**; the two controls establish native capture,
not full driver correctness. Cache inventory handling is deliberately still
unresolved, as are cohort grading and solver isolation. Only the two recorded
native versions are verified. No official parser or original reported identifier
has changed. The future driver stays private because its surrounding inputs access
answer-bearing grading data; public control sources contain no such inputs.

Evidence: `results/native-status-capture-01/` contains per-runtime native stdout,
summaries, Git-free checks and private-driver identities. All models:0. Skill,
README, featured and hosted performance claims remain unchanged. The next required
step is correcting the already observed cache guard separately, then verifying
the full grading contract and isolation before measuring distinct representative
workflows across all8 roles.

한국어: 구버전 pytest는 XPASS를 내부 `failed`로, 다른 버전은 `passed`로
기록하지만 실제 판정은 둘 다 `xpassed`다. 네이티브 상태를 직접 수집하는
방식을 두 실제 런타임과 Git 없는 복사본에서 검증했고, 기존 기록을 보존한
별도 다음 드라이버에 반영했다. 최초 skip 지원 차이로 실패한 검사도 보존한다.
외부 과제 실행·모델 호출은0회이며, 전체 드라이버와 cache 보존·평가 준비는
아직 미완료다. 토큰 절감·속도 개선·8개 역할 품질 향상 증거로 승격하지 않는다.
