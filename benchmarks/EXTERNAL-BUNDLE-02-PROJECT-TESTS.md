# External bundle02 — existing pytest tests, 2026-09-27

Parent `5a7e6fc3`; unchanged skill resource `7172b50c`. Author preparation only,
zero model calls and no selected-issue correctness or efficiency claim.

Initial full `testing` collection against the unpatched selected sources fails
on missing testing extras: hypothesis in all3 legacy sources; xmlschema also in
5.2; attrs/xmlschema/hypothesis in8.0. Original four exit2 attempts are retained.
The actual sources' `testing` extras declare these dependencies. Add pinned test
packages to the **owned preparation venvs only**, downloading hashed binary wheels
with isolated pip/no cache/zero retries/timeouts and installing offline. Both pip
checks pass. Earlier bootstrap freezes remain historical; those are not the new
runtime identity. Download hashes, initial/current freezes and requirements are
under [testing dependencies](results/external-bundle-02-project-tests/testing-dependencies/).

The second full collection succeeds for modern pytest (3,468 tests collected),
but all3 legacy sources exit2: hypothesis4.38.1 calls attrs' deprecated `cmp`,
and the native project treats that warning as an error. Preserve all four results.
Do not suppress project warnings or patch tests. Hypothesis requires attrs>=16,
and each legacy pytest requires attrs>=17.4. A final legacy pin attrs19.1.0
satisfies both and avoids the deprecated interface warning introduced by later
attrs; pip check passes. Both prior pins/freezes remain visible. This is a native
compatibility repair, not proof that all allowed version combinations work.

Full legacy `testing` collection now exits0 for all3 selected bases. No tests are
executed by collection. All processes import/assert the public source entrypoint
at the same base before invoking native pytest. Owned HOME/TMPDIR/basetemp, disabled
plugin autoload and unchanged project configuration prevent accidental external
plugins/configuration from determining the result. Each subprocess is bounded;
all processes terminate without timeouts.

Next run the existing, unchanged `testing/test_mark.py` module on all4 bases:

| Selected issue | Native existing-module result |
| --- | --- |
| pytest5221 |73 passed,1 xfailed |
| pytest5103 |74 passed,1 xfailed |
| pytest6116 |74 passed,1 xfailed |
| pytest11143 |90 passed,1 xfailed |

Total311 passed,4 expected failures,zero actual failures. The retained native
outputs show the xfail identifiers. Xfails are not counted as passes. These are
common existing-project checks, not each selected issue's required regressions,
full-suite execution or a repaired application. No answer-bearing patch or issue
solution was examined. Source path assertions run in the test process. All tracked
source hashes still match exact base archives (433/418/474/578 files); generated
metadata and test artifacts are separately owned/untracked.

[Initial collection](results/external-bundle-02-project-tests/collection-initial/summary.json),
[second collection](results/external-bundle-02-project-tests/collection-testing-deps/summary.json),
[final collection/mark](results/external-bundle-02-project-tests/collection-and-mark/summary.json)
and [source parity](results/external-bundle-02-project-tests/source-parity.json)
retain every attempted cell. Per-phase deterministic gzip reading copies preserve
native errors/assertions/results with original-byte hashes and owned path redaction.
The [executed mark driver](results/external-bundle-02-project-tests/native-mark-driver.py)
is author preparation tooling with fixed local roots, not a general solver launcher.

Before model execution, validate selected issue tests outside solver contexts,
Requests' native suite/service and older dependencies, fresh solver snapshots
without upstream history, complete frozen runtime identities and a distinct
execution protocol. All8 role-specific quality and lower whole-task tokens plus
faster completion still require actual model evidence; this checkpoint proves none
of those outcomes. Featured charts, website claims and both skill READMEs remain
unchanged because no skill capability or measured model result changed.

한국어: 원본 pytest4개 모두 기존 테스트 수집이 성공했고 실제 mark 테스트는
311개 통과·예상 실패4개·실제 실패0개였다. 누락 의존성과 구버전 호환 실패도
모두 보존하며 경고·테스트·소스를 바꾸지 않았다. 과제별 필수 회귀 검사와
Requests 실행 환경·모델 비교·전체8개 역할 개선 검증은 아직 남아 있다.
