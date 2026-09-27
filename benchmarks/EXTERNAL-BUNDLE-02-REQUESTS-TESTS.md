# External bundle02 — Requests native test preparation, 2026-09-27

Parent `8e3e089d`; skill resource stays `7172b50c`. Author preparation only,
zero model calls or selected-issue correctness/performance claim.

Inspect each selected source's existing tests, requirements and server fixtures.
Requests0.14/2.3/2.7 use HTTPBIN_URL but also contain hard-coded external endpoints;
2.10 declares pytest-httpbin and wraps HTTP/HTTPS fixtures. Existing project's
historical requirements differ (nose/rudolf, pytest2.3.4, pytest2.8.7 respectively).
No external service, application code or test file was modified.

Using existing owned Python3.9 plus native pytest5.2 source, fresh public-entry
assertions identify each Requests source before collecting its original suite.
Supply an owned empty pytest config/TMPDIR/basetemp, disabled autoload flag and
HTTPBIN_URL pointing to unused loopback port1. Collection executes no test bodies.
Three suites collect successfully; Requests3362 fails because historical marked
parameter values are incompatible with pytest5.2. This is not an application bug.
All four original collection results remain available.

Prepare a separate owned Python3.9 venv with the source's exact declared
pytest2.8.7/py1.4.31 plus setuptools68.2.2. Installation and pip check pass;
actual freeze is retained. Its default assertion mode exits3 with an internal
AssertionError in the runner's missing-assertion check. Preserve this second
compatibility failure; do not relabel the earlier collection or patch the runner.

A **provisional** native `--assert=plain` route collects the original3362 suite
and passes its existing entrypoint test. This option retains Python assertions
while changing rewriting/diagnostics; it is not yet adopted for model evaluation.
Explicit fresh native controls prove1 passed/exit0 and1 failed/exit1 with
`AssertionError: actual=41 expected=42`, not a setup exception. No optimization,
application change or suppression of failing assertions is used. The old runner
may not honor PYTEST_DISABLE_PLUGIN_AUTOLOAD; its dedicated venv has no installed
third-party pytest plugin. Full required-issue grading still must validate this
route, or use a compatible interpreter, before any model execution.

Run unchanged existing local checks using the respective native routes:

| Selected source | Existing tests | Result |
| --- | --- | --- |
| Requests3362,pytest2.8/plain |tests/test_structures.py |20 passed |
| Requests863,pytest5.2/default |entrypoint and invalid URL methods |2 passed |
| Requests1963,pytest5.2/default |TestCaseInsensitiveDict |18 passed |
| Requests2674,pytest5.2/default |TestCaseInsensitiveDict |20 passed |

Total60 passed,zero failures; one earlier entrypoint pass and two authored controls
are separate and not included in60. The two smoke tests are narrower than full
modules. None of these selectors needs an HTTP service; this is not OS-level
network isolation. Exact Requests source provenance is asserted in each test
process. All121/132/140/167 archive file bytes remain identical after the checks,
with complete per-source hashes retained.

[Original collection](results/external-bundle-02-requests-tests/collection/summary.json),
[pytest2.8 attempts](results/external-bundle-02-requests-tests/pytest28/),
[local tests/controls](results/external-bundle-02-requests-tests/local-tests/summary.json)
and [source preservation](results/external-bundle-02-requests-tests/source-parity.json)
include every attempted path. Original raw-byte hashes plus deterministic gzip
reading copies retain native incompatibilities/assertions/results. No issue/gold
solution fields were examined. All author subprocesses terminate; raw logs and
owned environments remain local.

Remaining: actual HTTP/TLS fixtures and mock plugin compatibility, hard-coded
external endpoint treatment without project/test patches, complete selected issue
regression gates outside model contexts, fresh solver snapshots/history isolation,
frozen reproducible runtime and execution protocol. Existing-suite collection and
local passes are not full-suite success, equal-quality model work, or lower
whole-task tokens/faster completion across all8 roles. Website/featured claims and
skill READMEs are unchanged because no skill capability/model result changed.

한국어: Requests3개는 기존 테스트 수집이 됐고 한 개는 오래된 실행기·Python
호환 실패를 보존했다. plain assertion 경로는 실제 정상/실패를 구분하지만 평가용
채택은 미정이다. 원본 로컬 테스트60개가 통과했으며 전체 HTTP·HTTPS·mock
환경과 과제별 회귀 검사·모델 비교는 미완료다. 소스와 테스트를 바꾸지 않았다.
